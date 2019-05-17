from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CMLangv2Parser import CMLangv2Parser
    from .CMLangv2Lexer import CMLangv2Lexer
    from .CMLangv2Listener import CMLangv2Listener
else:
    from CMLangv2Parser import CMLangv2Parser
    from CMLangv2Lexer import CMLangv2Lexer
    from CMLangv2Listener import CMLangv2Listener

import graphviz as gz
import pprint
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
# from utils import hierarchy_pos

class CMLangCompiler(CMLangv2Listener):

    group_functions = [ "sum", "argmin", "argmax", "max", "min", "prod"]
    functions = { "pi": "mov",
                   "log" : "mov",
                   "log2" : "mov",
                   "float" : "cast",
                   "int" : "cast",
                   "bin" : "cast",
                   "random" : "rand",
                   "ceiling" : "ceil",
                   "floor" : "floor",
                   "e": "mov",
                   "fread" : "fread",
                   "fwrite" : "fwrite"}

    def __init__(self, draw=False):
        self.component_definition_id = 0

        self.def_nodes = {}
        self.graph = nx.MultiDiGraph()
        self.global_instances = {}
        self.draw = draw

    def add_local(self, id, check_exists=False):

        if id not in self.local_variables.keys():
            if check_exists:
                print("Use of undeclared variable {}!".format(id))
            self.local_variables[id] = len(self.local_variables.keys())
            self.uses[id] = 1
        else:
            self.uses[id] += 1


    def getText(self, context):
        if context.getText()[0] == '(' and context.getText()[-1] == ')':
            return context.getText()[1:-1]
        else:
            return context.getText()

    def get_time(self, parents):
        times = []
        for i in range(len(parents)):
            if parents[i] not in self.dfg.nodes.keys():
                print("Error, parent not found: {} in scope {}".format(parents[i], self.scope))
            else:
                times.append(self.dfg.nodes[parents[i]]['time'])
        return np.max(times)

    # TODO: Fill this out to correctly infer types
    def get_dtype(self, id):
        return 'Type'

    def get_dims(self, idx_list):
        dims = []
        id = idx_list.getText()
        self.add_local(id)

        for dim in idx_list.index_expression():
            dimtext = self.getText(dim.expression())
            self.dfg.add_node(dimtext,
                              op='index',
                              id=self.local_variables[id],
                              dtype='index',
                              ntype='node',
                              time=self.get_time([dimtext]) + 1)
            dims.append(dimtext)
        self.dfg.add_node(id,
                          op=id,
                          id=self.local_variables[id],
                          dtype='index',
                          dims=dims,
                          ntype='node',
                          time=self.get_time(dims) + 1)
        for d in dims:
            self.dfg.add_edge(d, id, label=d)


        return dims

    def get_args(self, expr_list):
        args = []
        for arg in expr_list.expression():
            args.append(self.getText(arg))
        return args

    # Enter a parse tree produced by CMLangv2Parser#component_definition.
    def enterComponent_definition(self, ctx:CMLangv2Parser.Component_definitionContext):
        self.scope = ctx.IDENTIFIER().getText()
        self.component_type = ctx.component_type().getText()
        self.inputs = {}
        self.outputs = {}
        self.states = {}
        self.parameters = {}
        self.instances = []
        self.indices = {}
        self.flows = []
        self.dfg = nx.DiGraph()
        self.local_variables = {}
        self.uses = {}
        self.times = {}
        self.assign=False
        self.flow_declaration=False


    # Exit a parse tree produced by CMLangv2Parser#component_definition.
    def exitComponent_definition(self, ctx:CMLangv2Parser.Component_definitionContext):
        self.def_nodes[self.scope] = {'id': self.component_definition_id,
                                          'component_type': self.component_type,
                                          'inputs': self.inputs,
                                          'outputs': self.outputs,
                                          'states' : self.states,
                                          'parameters': self.parameters,
                                          'instances': self.instances,
                                          'flows' : self.flows,
                                          'indices' : self.indices,
                                          'DFG': self.dfg,
                                          'locals' : self.local_variables
                                      }

        self.component_definition_id += 1
        if self.draw:
            labels = nx.get_node_attributes(self.dfg, 'op')
            for n in self.dfg.nodes:
                self.dfg.nodes[n]['label'] = labels[n]

            A = nx.drawing.nx_agraph.to_agraph(self.dfg)
            A.layout('dot')

            A.draw('graphs/{}.png'.format(self.scope))

        del self.scope
        del self.inputs
        del self.states
        del self.outputs
        del self.parameters
        del self.instances
        del self.dfg
        del self.flows
        del self.indices
        del self.local_variables
        del self.assign

    # Enter a parse tree produced by CMLangv2Parser#flow.
    def enterFlow(self, ctx:CMLangv2Parser.FlowContext):
        self.ftype = ctx.flow_type().getText()
        self.dtype = ctx.dtype_specifier().getText()
        self.default = None
        self.fdims = []


    # Exit a parse tree produced by CMLangv2Parser#flow.
    def exitFlow(self, ctx:CMLangv2Parser.FlowContext):
        if self.ftype == 'input':
            self.inputs[self.fid] = {
                'dtype' : self.dtype,
                'dims' : self.fdims
            }
            self.add_local(self.fid)
            self.dfg.add_node(self.fid, id=self.local_variables[self.fid],
                              op=self.fid,
                              dtype=self.dtype,
                              dims=self.fdims,
                              ntype='ileaf',
                              time=1)
        elif self.ftype == 'state':
            self.parameters[self.fid] = {
                'dtype': self.dtype,
                'dims': self.fdims,
            }
            self.add_local(self.fid)
            self.dfg.add_node(self.fid, id=self.local_variables[self.fid],
                              op=self.fid,
                              dtype=self.dtype,
                              dims=self.fdims,
                              ntype='ileaf',
                              time=1)
        elif self.ftype == 'output':
            self.outputs[self.fid] = {
                'dtype': self.dtype,
                'dims': self.fdims
            }
            self.add_local(self.fid)
            self.dfg.add_node(self.fid, id=self.local_variables[self.fid],
                              op=self.fid,
                              dims=self.fdims,
                              dtype=self.dtype,
                              ntype='oleaf')
        elif self.ftype == 'param':
            self.parameters[self.fid] = {
                'dtype': self.dtype,
                'dims': self.fdims,
                'default' : self.default
            }
            self.add_local(self.fid)
            self.dfg.add_node(self.fid, id=self.local_variables[self.fid],
                              op=self.fid,
                              dtype=self.dtype,
                              default=self.default,
                              dims=self.fdims,
                              ntype='ileaf',
                              time=1)
        else:
            print('Invalid flow type: {}'.format(self.ftype))

        self.flows.append(self.fid)
        del self.ftype
        del self.fdims


    # Enter a parse tree produced by CMLangv2Parser#flow_expression.
    def enterFlow_expression(self, ctx:CMLangv2Parser.Flow_expressionContext):
        self.fid = ctx.IDENTIFIER().getText()

        # TODO: Evaluate literal and error when non-param has default
        if ctx.EQ():
            self.default = ctx.literal()

    def enterFlow_index(self, ctx: CMLangv2Parser.Flow_indexContext):
        id = ctx.IDENTIFIER().getText()
        self.fdims.append(id)
        self.add_local(id)
        self.dfg.add_node(id,
                          op=id,
                          id=self.local_variables[id],
                          dtype='int',
                          dims=[],
                          ntype='ileaf',
                          time=1)

    # Exit a parse tree produced by CMLangv2Parser#flow_declaration_list.
    def exitFlow_declaration_list(self, ctx:CMLangv2Parser.Flow_declaration_listContext):
        self.flow_declaration = True
        for arr in ctx.array_expression():
            self.handle_array(arr)
        self.flow_declaration = False



    # Enter a parse tree produced by CMLangv2Parser#index_declaration.
    def enterIndex_declaration(self, ctx:CMLangv2Parser.Index_declarationContext):
        if ctx.IDENTIFIER().getText() in self.local_variables.keys():
            print("Redeclaration of index {}".format(ctx.IDENTIFIER().getText()))
        else:
            self.idx_id = ctx.IDENTIFIER().getText()
            self.add_local(self.idx_id)


    # Exit a parse tree produced by CMLangv2Parser#index_declaration.
    #TODO: add node for index
    def exitIndex_declaration(self, ctx:CMLangv2Parser.Index_declarationContext):
        upper = ctx.expression()[1].getText()
        lower = ctx.expression()[0].getText()
        time = self.get_time([lower, upper])
        self.dfg.add_node(self.idx_id,
                          op=self.idx_id,
                          dims=[],
                          lower=lower,
                          upper=upper,
                          dtype='int',
                          ntype='ileaf',
                          time=time+1)
        self.dfg.add_edge(lower, self.idx_id, label=lower)
        self.dfg.add_edge(upper, self.idx_id, label=upper)

        del self.idx_id



    # Enter a parse tree produced by CMLangv2Parser#prefix_expression.
    def enterPrefix_expression(self, ctx:CMLangv2Parser.Prefix_expressionContext):
        self.assign=True
        if ctx.array_expression():
            self.fid = ctx.array_expression().IDENTIFIER().getText()
            self.handle_array(ctx.array_expression())
        else:
            self.fid = ctx.IDENTIFIER().getText()

    # Exit a parse tree produced by CMLangv2Parser#prefix_expression.
    def exitPrefix_expression(self, ctx:CMLangv2Parser.Prefix_expressionContext):
        self.assign=False

    def handle_function(self, expr):
        if expr.function_id().getText() not in self.functions.keys():
            self.instances.append(self.getText(expr.function_id()))
        else:
            id = expr.getText()
            self.add_local(id)
            if expr.expression_list():
                arguments = self.get_args(expr.expression_list())
                fname = expr.function_id().getText()
                self.add_local(fname)

                self.dfg.add_node(fname, op=fname,
                                  id=self.local_variables[id],
                                  dtype=self.get_dtype(fname),
                                  ntype='fnode',
                                  time=1)
                self.dfg.add_node(id, op=id,
                                  id=self.local_variables[id],
                                  dtype=self.get_dtype(fname),
                                  args=arguments,
                                  ntype='node',
                                  time=self.get_time(arguments) + 1)
                self.dfg.add_edge(fname, id, label=fname)
                for arg in arguments:
                    self.dfg.add_edge(arg, id, label=arg)

            else:
                self.dfg.add_node(id, op=id,
                                  id=self.local_variables[id],
                                  dtype=self.get_dtype(id),
                                  args=[],
                                  ntype='node',
                                  time=1)




    def handle_array(self, expr):
        fid = self.getText(expr.IDENTIFIER())

        id = self.getText(expr)
        idims = self.get_dims(expr.index_expression_list())
        dimtext = self.getText(expr.index_expression_list())

        if self.flow_declaration:
            dtype = self.dtype
            instr_op = 'edge'

        else:
            dtype = self.get_dtype(fid)
            instr_op = id

        if self.assign or self.flow_declaration:
            self.add_local(fid, check_exists=False)

            self.dfg.add_node(fid,
                              op=fid,
                              dtype=dtype,
                              fid=fid,
                              ntype='ileaf',
                              time=1)
        else:
            self.add_local(fid, check_exists=True)


        self.dfg.add_node(id,
                      op=instr_op,
                      dims=idims,
                      dtype=dtype,
                      fid=fid,
                      ntype='node',
                      time=self.get_time(idims) + 1)

        self.dfg.add_edge(fid, id, label=fid)
        self.dfg.add_edge(dimtext, id, label=dimtext)


    def handle_group(self, expr):

        fid = expr.IDENTIFIER().getText()
        expr_arg = self.getText(expr.expression())
        id = self.getText(expr)
        idims = self.get_dims(expr.index_expression_list())

        self.dfg.add_node(fid,
                          op=fid,
                          dtype=self.get_dtype(fid),
                          ntype='ileaf',
                          time=1)
        self.dfg.add_node(id,
                          op=id,
                          dims=idims,
                          dtype=self.get_dtype(id),
                          fid=fid,
                          ntype='node',
                          time=self.get_time(idims + [expr_arg])+1)

        idx_list = expr.index_expression_list().getText()
        self.dfg.add_edge(fid, id, label=fid)
        self.dfg.add_edge(idx_list, id, label=idx_list)
        self.dfg.add_edge(expr_arg, id, label=expr_arg)

    # Exit a parse tree produced by CMLangv2Parser#expression.
    def exitExpression(self, ctx:CMLangv2Parser.ExpressionContext):

        if ctx.array_expression():
            self.handle_array(ctx.array_expression())
        elif ctx.group_expression():
            self.handle_group(ctx.group_expression())
        elif ctx.function_expression():
            self.handle_function(ctx.function_expression())
        elif ctx.expression():
            id = self.getText(ctx)
            self.add_local(id)
            if len(ctx.expression()) > 1:
                e1 = self.getText(ctx.expression()[0])
                e2 = self.getText(ctx.expression()[1])
                parents = [e1, e2]
                self.dfg.add_edge(e1, id, label=e1)
                self.dfg.add_edge(e2, id, label=e2)
                self.expop = self.getText(ctx.getChild(1))
            else:
                self.expop = self.getText(ctx.getChild(0))
                e1 = self.getText(ctx.expression()[0])
                parents = [e1]
                self.dfg.add_edge(e1, id, label=e1)
            # TODO: Do type inference for type evaluation

            self.dfg.add_node(id, op=self.expop,
                              id=self.local_variables[id],
                              dtype=self.get_dtype(id),
                              dims=[],
                              ntype='node',
                              time=self.get_time(parents)+1)

            del self.expop
        elif ctx.IDENTIFIER():
            id = ctx.getText()
            self.add_local(id, check_exists=True)
        elif ctx.number():
            id = ctx.getText()
            self.dfg.add_node(id, op=id,
                              id=None,
                              dtype=self.dtype,
                              dims=[],
                              ntype='ileaf',
                              time=1)

        self.dtype = None

    def exitAssignment_expression(self, ctx:CMLangv2Parser.Assignment_expressionContext):
        #TODO: Change to point to same ID and check for flow
        id = self.getText(ctx.prefix_expression())

        self.add_local(id)

        if ctx.expression():
            expr_text = self.getText(ctx.expression())
            attributes = self.dfg.nodes[expr_text]
            print(expr_text)
            self.dfg.add_node(id, **attributes)

            if self.fid in self.outputs.keys() or self.fid in self.states.keys():
                self.dfg.nodes[id]['op'] = 'write'
                print(self.dfg.nodes[id]['time'])
            else:
                self.dfg.nodes[id]['op'] = 'assign'
            del self.fid
            self.dfg.add_edge(expr_text, id, label=expr_text)



    # Enter a parse tree produced by CMLangv2Parser#declaration_statement.
    def enterDeclaration_statement(self, ctx:CMLangv2Parser.Declaration_statementContext):
        if ctx.INDEX():
            self.dtype = self.getText(ctx.INDEX())
        else:
            self.dtype = self.getText(ctx.dtype_specifier())

    # Exit a parse tree produced by CMLangv2Parser#declaration_statement.
    def exitDeclaration_statement(self, ctx:CMLangv2Parser.Declaration_statementContext):
        self.dtype = None

    # Exit a parse tree produced by CMLangv2Parser#predicate_expression.
    def exitPredicate_expression(self, ctx:CMLangv2Parser.Predicate_expressionContext):
        boolid= self.getText(ctx.expression()[0])
        tid = self.getText(ctx.expression()[1])
        fid = self.getText(ctx.expression()[2])

        for n in self.dfg.predecessors(tid):
            self.dfg.nodes[n]['predicate'] = 't'
            self.dfg.nodes[n]['predicate_dep'] = boolid

        for n in self.dfg.predecessors(fid):
            self.dfg.nodes[n]['predicate'] = 'f'
            self.dfg.nodes[n]['predicate_dep'] = boolid

        node = self.getText(ctx)
        self.add_local(node)

        self.dfg.add_node(node,
                          op='predicate',
                          true=tid,
                          false=fid,
                          boolid=boolid,
                          dtype=self.get_dtype(tid),
                          ntype='node',
                          time=self.get_time([boolid, tid, fid])+1)
        self.dfg.add_edge(boolid, node, label=boolid)
        self.dfg.add_edge(tid, node, label=tid)
        self.dfg.add_edge(fid, node, label=fid)



    # Enter a parse tree produced by CMLangv2Parser#integer.
    def enterInteger(self, ctx:CMLangv2Parser.IntegerContext):
        self.dtype='int'

    # Exit a parse tree produced by CMLangv2Parser#number.
    def exitNumber(self, ctx:CMLangv2Parser.NumberContext):
        if ctx.FLOAT_NUMBER():
            self.dtype='float'
        elif ctx.IMAG_NUMBER():
            self.dtype='imag'



def parse_file(fname,draw=False, print_code=True, commented=True):
    input_file = FileStream(fname)
    lexer = CMLangv2Lexer(input_file)
    stream = CommonTokenStream(lexer)
    parser = CMLangv2Parser(stream)
    tree = parser.cmlang()

    compiler = CMLangCompiler(draw=draw)
    walker = ParseTreeWalker()
    walker.walk(compiler, tree)
    # graph = HDFG(fname, compiler, tree, print_code=print_code, commented=commented)

if __name__ == '__main__':

    parse_file('../benchmarks/kmeans/kmeans_paper.cm', draw=True)