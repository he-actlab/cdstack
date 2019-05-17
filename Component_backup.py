from antlr4.tree.Trees import Trees
from antlr4.tree.Tree import Tree, TerminalNode
from CMLang.CMLangVisitor import CMLangVisitor
from CMLang.Node import Node
from collections import deque
import ast




class Component:
    bin_expr_instructions = {"*": "mul",
                         "/": "div",
                         "+": "add",
                         "-": "sub",
                         "<": "tlt",
                         ">": "tgt",
                         "<=": "tlte",
                         ">=": "tgte",
                         "^": "exp"
                         }

    unary_expr_instructions = {"+":"mov",
                               "-": "neg"}
    function_expr_instructions = { "pi": "mov",
                                   "sum" : "sum",
                                   "log" : "mov",
                                   "log2" : "mov",
                                   "float" : "cast",
                                   "int" : "cast",
                                   "bin" : "cast",
                                   "random" : "rand",
                                   "ceiling" : "ceil",
                                   "floor" : "floor",
                                   "e": "mov"}
    def __init__(self,name, comp_def, global_queues, tree, flows,commented=True):
        self.commented = commented
        self.vars = comp_def['vars']
        self.args = comp_def['args']
        self.primitives = comp_def['primitives']
        self.instances = comp_def['instances']
        self.predicate = None
        self.predicate_iter = None
        self.predicate_reg = None
        self.assignee = False
        self.name = name
        self.start = ".cbegin " + name
        self.end = ".cend"
        self.header = []
        self.body = deque()
        self.footer = []
        self.constants = []
        self.tree = tree
        self.declarations = {}
        self.temps = {}
        self.iters = {}
        self.global_flows = flows
        self.flows = []

        # keep track of iterators
        self.ids = 0


        # Keep mapping of registers, iterators, and flows to identifiers
        self.edges = 0
        self.registers = 0
        self.iterators = 0
        self.iter_map = {}
        self.reg_map = {}
        self.temp_iter = {}

        self.edge_map = {}

        self.body_nodes = []
        self.header_nodes= []
        self.footer_nodes= []

        # Track instance name in instance list
        self.instance_count = 0

        # Keep track of dimensionality in recursion


        self.add_header()
        self.add_body()
        self.set_parameters()
        self.add_footer()

    def get_number(self, number):
        if number.integer():
            return ('int', int(number.integer().getText()))
        elif number.FLOAT_NUMBER():
            return ('float', float(number.FLOAT_NUMBER().getText()))
        else:
            return ('imag', complex(number.getText()))



    def eval_comp(self, component_inst):
        self.expr = []
        instance_name = self.instances[self.instance_count]

        self.instruction = Node(self.ids, 'wait', instance_name=instance_name)
        self.add_instruction('body')
        self.ids += 1
        self.instance_count += 1

    def eval_loop(self, loop):
        pass

    # TODO: Determine iterator over expressions
    def eval_assign(self, assignee, expression):
        self.expr = []
        self.handle_logic(expression)
        self.handle_var(assignee)




    def eval_predicate(self, assignee, expression):

        # Boolean
        self.handle_logic(expression.expr()[0])
        self.predicate_iter = self.body_nodes[-1].dest_iter
        self.predicate_reg = self.body_nodes[-1].dest
        # True
        self.expr = []
        self.predicate = 't'
        self.handle_logic(expression.expr()[1])
        if len(self.expr) == 0:

            op1 = expression.expr()[1].getText()
            dest = self.get_register(op1)
            self.instruction = Node(self.ids, 'mov', predicate_register=self.predicate_reg, predicate_iterator=self.predicate_iter,
                                predicate=self.predicate, op1=op1, dest=dest)
            comment = ''
            self.add_instruction('body', comment)
            self.ids += 1

        self.expr = []

        # False
        self.predicate = 'f'
        self.handle_logic(expression.expr()[2])
        if len(self.expr) == 0:
            op1 = expression.expr()[2].getText()
            dest, dest_iter = self.add_destination(assignee, op1)
            self.instruction = Node(self.ids, 'mov', predicate_register=self.predicate_reg, predicate_iterator=self.predicate_iter,
                                predicate=self.predicate, op1=op1, dest=dest, dest_iter=dest_iter)
            comment = ''
            self.add_instruction('body', comment)
            self.ids += 1


        self.expr = []

        self.predicate = None
        self.predicate_iter = None
        self.predicate_reg = None
        self.handle_var(assignee)

    def eval_file_op(self, file):
        pass

    # TODO: Assert dimensions of iterators and flows are not on critical path
    def eval_data_decl(self, data_decl):


        if data_decl.flow_declaration():
            self.type = data_decl.flow_declaration().val_type().getText()
            flow = data_decl.flow_declaration().var_list_flow()
            self.eval_flow(flow.flow())
            flow = flow.var_list_flow_tail()

            while flow.var_list_flow():
                self.eval_flow(flow.var_list_flow().flow())
                flow = flow.var_list_flow().var_list_flow_tail()

    def eval_flow(self, flow):
        self.flows.append(self.global_flows[self.name + ':' + flow.ID().getText()])

    def get_iterator(self, expr):

        if len(expr) == 0:
            print('error! empty list for dimensions')
        elif len(expr) == 1:
            expression = str(expr).replace('[','').replace(']','')
            if expression not in self.iters.keys():
                self.iters[expression] = "$i" + str(self.iterators)
                self.temp_iter[ast.literal_eval(expression)] = (self.iters[expression], None)
                self.iterators += 1
        else:
            expression = str(expr).replace('[','').replace(']','')
            if expression not in self.iters.keys():
                self.iters[expression] = '$i' + str(self.iterators)
                self.temp_iter[expression] = (self.iters[expression], None)

                dest = self.iters[expression]
                op2_var = str(expr[:-1]).replace('[','').replace(']','')
                op1_var = str(expr[-1:]).replace('[','').replace(']','')

                op2 = self.iters[op2_var]
                op1 = self.iters[op1_var]
                self.instruction = Node(self.ids, 'iter',
                                        predicate=self.predicate, predicate_iterator=self.predicate_iter,
                                        predicate_register=self.predicate_reg,dest=dest,
                                        op1=op1, op2=op2)
                self.add_instruction('body', expression)

                self.ids += 1
                self.iterators += 1


        return self.iters[expression]

    def get_register(self, expr):

        if expr not in self.temps.keys():
            self.temps[expr] = "$t" + str(self.registers)
            self.registers += 1
        return self.temps[expr]

    def get_temp_iter(self, expr):

        if expr[0] == '(' and expr[-1] == ')':
            expr = expr[1:-1]
        if expr not in self.temp_iter.keys():
            print('Expression \"{}\" not found!'.format(expr))
        return self.temp_iter[expr]

    def add_destination(self, expr, op1=None, op2=None):
        # TODO: Get the larger dimensioned op, set as new operand
        # TODO: check if doing iterator operation



        if op2 and op2[0] == '(' and op2[-1] == ')':
            op2 = op2[1:-1]

        if op1 and op1[0] == '(' and op1[-1] == ')':
            op1 = op1[1:-1]

        if op1 in self.vars.keys() and self.vars[op1]['type'] == 'iterator':
            temp = self.get_iterator([expr])
            iter = None

        else:
            temp = self.get_register(expr)
            if op1 and self.temp_iter[op1][1]:
                _, iter = self.temp_iter[op1]
            elif op2 and self.temp_iter[op2][1]:
                _, iter = self.temp_iter[op2]
            else:
                iter = None


        self.temp_iter[expr] = (temp, iter)


        return temp, iter

    def handle_logic(self, expr):

        if expr.logic():

            self.handle_addsub(expr.logical_expr()[0])
            self.handle_addsub(expr.logical_expr()[1])

            op1, op1_iter = self.get_temp_iter(expr.logical_expr()[0].getText())
            op2, op2_iter = self.get_temp_iter(expr.logical_expr()[1].getText())
            dest, dest_iter  = self.add_destination(expr.getText(), op1=expr.logical_expr()[0].getText(),
                                                    op2=expr.logical_expr()[1].getText())

            self.instruction = Node(self.ids, self.bin_expr_instructions[expr.logic()[0].getText()],
                                    predicate=self.predicate, predicate_register=self.predicate_reg,
                                    predicate_iterator=self.predicate_iter,dest=dest,dest_iter=dest_iter,
                                    op1=op1,op1_iter=op1_iter,op2=op2, op2_iter=op2_iter)
            self.ids += 1
            comment = expr.getText()
            self.add_instruction('body', comment)
        else:
            self.handle_addsub(expr.logical_expr()[0])


    def handle_addsub(self, expr):

        if expr.add_sub():

            self.handle_muldiv(expr.add_sub_expr()[0])
            self.handle_muldiv(expr.add_sub_expr()[1])

            ## TODO: Make sure destination is added, but ops exist

            op1, op1_iter = self.get_temp_iter(expr.add_sub_expr()[0].getText())
            op2, op2_iter = self.get_temp_iter(expr.add_sub_expr()[1].getText())
            dest, dest_iter = self.add_destination(expr.getText(), op1=expr.add_sub_expr()[0].getText(),
                                                   op2=expr.add_sub_expr()[1].getText())

            self.instruction = Node(self.ids, self.bin_expr_instructions[expr.add_sub()[0].getText()],
                                    predicate=self.predicate,predicate_register=self.predicate_reg,
                                    predicate_iterator=self.predicate_iter, dest=dest,dest_iter=dest_iter,
                                    op1=op1,op1_iter=op1_iter,op2=op2, op2_iter=op2_iter)
            self.ids += 1

            comment = expr.getText()
            self.add_instruction('body', comment)
        else:
            self.handle_muldiv(expr.add_sub_expr()[0])


    def handle_muldiv(self, expr):

        if expr.mul_div():

            self.handle_factor(expr.factor()[0])
            self.handle_factor(expr.factor()[1])

            op1, op1_iter = self.get_temp_iter(expr.factor()[0].getText())
            op2, op2_iter = self.get_temp_iter(expr.factor()[1].getText())

            dest, dest_iter = self.add_destination(expr.getText(), op1 = expr.factor()[0].getText(),
                                                   op2=expr.factor()[1].getText())
            self.instruction = Node(self.ids, self.bin_expr_instructions[expr.mul_div()[0].getText()],
                                    predicate_iterator=self.predicate_iter, predicate_register=self.predicate_reg,
                                    predicate=self.predicate, dest=dest,dest_iter=dest_iter,
                                    op1=op1,op1_iter=op1_iter,op2=op2, op2_iter=op2_iter)
            self.ids += 1

            comment = expr.getText()
            self.add_instruction('body', comment)
        else:
            self.handle_factor(expr.factor()[0])

    def handle_factor(self, expr):

        if expr.power():
            self.handle_signedval(expr.signed_value()[0])
            self.handle_signedval(expr.signed_value()[1])

            op1, op1_iter = self.get_temp_iter(expr.signed_value()[0].getText())
            op2, op2_iter = self.get_temp_iter(expr.signed_value()[1].getText())

            dest, dest_iter = self.add_destination(expr.getText(), op1 = expr.signed_value()[0].getText(),
                                                   op2=expr.signed_value()[1].getText())
            self.instruction = Node(self.ids, self.bin_expr_instructions[expr.power()[0].getText()],
                                    predicate_register=self.predicate_reg, predicate_iterator=self.predicate_iter,
                                    predicate=self.predicate, dest=dest,dest_iter=dest_iter,
                                    op1=op1,op1_iter=op1_iter,op2=op2, op2_iter=op2_iter)
            self.ids += 1

            comment = expr.getText()
            self.add_instruction('body', comment)
        else:
            self.handle_signedval(expr.signed_value()[0])


    def handle_signedval(self, expr):

        if expr.add_sub():
            self.handle_signedval(expr.signed_value())

            op1, op1_iter = self.get_temp_iter(expr.signed_value().getText())
            dest, dest_iter = self.add_destination(expr.getText(), op1=expr.signed_value().getText())


            self.instruction = Node(self.ids, self.unary_expr_instructions[expr.add_sub().getText()],
                                    predicate_iterator=self.predicate_iter, predicate_register=self.predicate_reg,
                                    predicate=self.predicate, dest=dest, dest_iter=dest_iter,
                                    op1=op1, op1_iter=op1_iter)
            self.ids += 1

            comment = expr.getText()
            self.add_instruction('body', comment)
        else:
            self.handle_atom(expr.atom())

    def handle_atom(self, expr):
        if expr.number():
            # TODO: Figure out how to handle complex numbers

            self.temps[expr.number().getText()] = str(self.get_number(expr.number())[1])
            self.temp_iter[expr.number().getText()] = (str(self.get_number(expr.number())[1]), None)

        elif expr.var():
            self.handle_var(expr.var())
        elif expr.file_operation():
            # TODO: Add file function params
            self.instruction = Node(self.ids, expr.file_operation().file_function().getText(),
                                    predicate_register=self.predicate_reg, predicate_iterator=self.predicate_iter,
                                    predicate=self.predicate)
            self.ids += 1

            comment = expr.getText()
            self.add_instruction('body', comment)

        # TODO: handle functions
        elif expr.function():

            self.handle_function(expr)
        else:
            # TODO: figure out what this does
            self.handle_logic(expr.expr())


    def handle_function(self, expr):



        if expr.function_args().expr() and expr.function_args().ID():
            # TODO: Handle iterated function

            self.handle_logic(expr.function_args().expr())
            op1, op1_iter = self.get_temp_iter(expr.function_args().expr().getText())
            dimensions = []
            for i in range(len(expr.function_args().ID())):
                dimensions.append(expr.function_args().ID()[i].getText())

            op2 = self.get_iterator(dimensions)
            op2_iter = None

        elif expr.function_args().expr():
            self.handle_logic(expr.function_args().expr())
            op2 = expr.function().getText().replace('(', '').replace(')', '')
            op2_iter = None
            op1, op1_iter = self.get_temp_iter(expr.function_args().expr().getText())

        else:
            op1 = expr.function().getText().replace('(', '').replace(')', '')
            op1_iter = None
            op2 = None
            op2_iter = None
        dest, dest_iter = self.add_destination(expr.getText())

        self.instruction = Node(self.ids, self.function_expr_instructions[expr.function().getText()],
                                predicate_iterator=self.predicate_iter,
                                predicate_register=self.predicate_reg, predicate=self.predicate, dest=dest,
                                dest_iter=dest_iter, op1=op1, op1_iter=op1_iter, op2=op2, op2_iter=op2_iter)
        self.ids += 1
        comment = expr.getText()
        self.add_instruction('body', comment)
    def handle_var(self, var):
        ## TODO: Check if iterator



        # TODO: need test for number value of expressions
        # TODO: Test for dimensionality
        if var.getText() in self.temp_iter.keys():
            temp, iter = self.temp_iter[var.getText()]
        else:
            temp = self.get_register(var.var_id().ID().getText())
            self.temp_iter[var.var_id().ID().getText()] = (temp, None)
            iter = None
            id_tail = var.var_id().id_tail()
            dimensions = []
            while id_tail.flow_index():

                itervar = id_tail.flow_index().getText()
                self.handle_logic(var.var_id().id_tail().flow_index().expr())
                self.index = True
                if itervar not in dimensions:
                    dimensions.append(itervar)
                iter = self.get_iterator(dimensions)

                id_tail = id_tail.id_tail()


            self.temp_iter[var.getText()] = (temp, iter)

    def add_instruction(self,part, comment=''):
        # TODO: Add typed instructions
        self.expr.append(self.instruction)
        if part == 'body':
            self.body_nodes.append(self.instruction)
            if self.commented:
                self.body.append("{:<40s} ; {:<45s}".format(self.instruction.create_instruction(), comment))
            else:
                self.body.append(self.instruction.create_instruction())
        elif part == 'header':
            self.header_nodes.append(self.instruction)
            if self.commented:
                self.header.append("{:<40s} ; {:<45s}".format(self.instruction.create_instruction(), comment))

            else:
                self.header.append(self.instruction.create_instruction())
        elif part == 'footer':
            self.footer_nodes.append(self.instruction)
            if self.commented:
                self.footer.append("{:<40s} ; {:<45s}".format(self.instruction.create_instruction(), comment))

            else:
                self.footer.append(self.instruction.create_instruction())

    def add_header(self):
        op = "read"
        self.expr = []
        for arg_name in self.args.keys():
            queue_name = "$c" + str(self.args[arg_name]['position'])
            target_name = "$t" + str(self.registers)
            if self.args[arg_name]['edge_type'] == 'input':
                self.instruction = Node(self.ids, op, dest=target_name, op1=queue_name)
                self.edge_map[arg_name] = queue_name
                self.temps[arg_name] = target_name
                self.edges += 1
                self.registers += 1
                self.add_instruction('header', arg_name)

    def set_parameters(self):
        for arg_name in self.args.keys():
            queue_name = "$c" + str(self.edges)
            if self.args[arg_name]['edge_type'] == 'parameter':
                self.edge_map[arg_name] = queue_name
                self.edges += 1

    def add_footer(self):
        op = "write"

        for arg_name in self.args.keys():
            queue_name = "$c" + str(self.edges)

            if self.args[arg_name]['edge_type'] == 'output':
                if arg_name in self.temp_iter.keys():
                    self.instruction = Node(self.ids, op, dest=queue_name, op1=self.temp_iter[arg_name][0])
                    self.edge_map[arg_name] = queue_name
                    self.edges += 1
                    self.registers += 1
                    self.add_instruction('footer', arg_name)

    def add_body(self):
        for it in self.vars.keys():
            if self.vars[it]['type'] == 'iterator':
                self.get_iterator([it])

        for i in self.primitives:
            if i[0] == 'comp':
                self.eval_comp(i[1])
            elif i[0] == 'loop':
                self.eval_loop(i[1])
            elif i[0] == 'assign':
                self.eval_assign(i[1], i[2])
            elif i[0] == 'predicate':
                self.eval_predicate(i[1], i[2])
            elif i[0] == 'file':
                self.eval_file_op(i[1])
            elif i[0] == 'decl':
                self.eval_data_decl(i[1])
            else:
                print('Error, undefined primitive')
