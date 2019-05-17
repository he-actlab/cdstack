from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CMLangv2Parser import CMLangv2Parser
    from .CMLangv2Lexer import CMLangv2Lexer
    from .CMLangv2Listener import CMLangv2Listener
    from .HDFG import HDFG
else:
    from CMLangv2Parser import CMLangv2Parser
    from CMLangv2Lexer import CMLangv2Lexer
    from CMLangv2Listener import CMLangv2Listener
    from HDFG import HDFG
    import hdfg_pb2 as hdfg
import graphviz as gz
import pprint
import networkx as nx
# import matplotlib.pyplot as plt
import numpy as np
from collections import deque

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
    function_dtypes = { "pi": 'float',
                   "log" : 'float',
                   "log2" :  'float',
                   "float" : 'float',
                   "int" :  'int',
                   "bin" :  'int',
                   "random" : 'float',
                   "ceiling" :'float',
                   "floor" : 'float',
                   "e": 'float',
                   "fread" : 'str',
                   "fwrite" : 'str'}
    dtypes = {
        "float" : hdfg.DT_FLOAT,
        "int" : hdfg.DT_INT32,
        "str" : hdfg.DT_STRING,
        "bool" : hdfg.DT_BOOL,
        "complex" : hdfg.DT_COMPLEX64
    }

    def __init__(self, gname, draw=False):
        self.component_definition_id = 0
        self.graph = hdfg.Graph()
        self.graph.graph_name = gname
        self.def_nodes = {}
        self.draw = draw

    def add_component(self, key, component, inputs=None, outputs=None):

        if inputs:
            for k in inputs.keys():
                component.inputs[k].CopyFrom(inputs[k])
        if outputs:
            for k in outputs.keys():
                component.outputs[k].CopyFrom(outputs[k])
        if self.pred_val:
            component.is_predicated = True
            if self.pred_val == 't':
                component.predicate_val = True
            elif self.pred_val == 'f':
                component.predicate_val = False
            if not self.boolid:
                print("Error! Bool id not set with predicate val set")
            component.pred_id = self.boolid
        else:
            component.is_predicated = False
        id = hdfg.Attribute(i=self.local_component_ids)
        component.def_attributes['local_id'].CopyFrom(id)
        self.cdef.sub_component_ids.extend([key])
        self.local_component_ids += 1
        self.cdef.sub_components[key].CopyFrom(component)

    def add_edge(self, id,attr, check_var_exists=False):
        edge = hdfg.EdgeInfo(**attr)
        if id not in self.local_edges.keys():
            if check_var_exists:
                print("Use of undeclared variable {}!".format(id))
            self.local_edges[id] = edge
            self.graph.component_definitions[self.scope].sub_edges[id].CopyFrom(edge)
            self.uses[id] = 1
        else:
            self.graph.component_definitions[self.scope].sub_edges[id].MergeFrom(edge)

            edge = self.graph.component_definitions[self.scope].sub_edges[id]
            self.uses[id] += 1
        return edge


    def getText(self, context):
        if context.getText()[0] == '(' and context.getText()[-1] == ')':
            return context.getText()[1:-1]
        else:
            return context.getText()

    # TODO: Fill this out to correctly infer types
    def get_dtype(self, id, context):
        types = []
        for t in range(len(id)):
            if id[t] in self.local_edges.keys():
                types.append(self.local_edges[id[t]].type)
        if len(types) == 0:
            print("Error, value {} not declared with type and cannot be inferred from {}".format(context, id))
            return 0
        elif len(set(types)) <= 1:
            print("Error! Type mismatch in {}".format(context))
            return 0
        else:
            return types[0]


    def get_args(self, expr_list):
        args = []
        for arg in expr_list.expression():
            args.append(self.getText(arg))
        return args

    def handle_literal(self, literal):
        if literal.STRING_LITERAL():
            attr = hdfg.Attribute(s=literal.getText())
        elif literal.number():
            lit = literal.number()
            if lit.integer():
                attr = hdfg.Attribute(i=int(literal.getText()))
            elif lit.FLOAT_NUMBER():
                attr = hdfg.Attribute(f=float(literal.getText()))
            elif lit.IMAG_NUMBER():
                num = complex(literal.getText().replace(" ", "").replace("i", "j"))
                real = num.real
                imag = num.imag
                lv = hdfg.Attribute.ListValue(f=[real, imag])
                attr = hdfg.Attribute(list=lv)
        elif literal.complex_number():
            num = complex(literal.getText().replace(" ", "").replace("i", "j"))
            real = num.real
            imag = num.imag
            lv = hdfg.Attribute.ListValue(f=[real, imag])
            attr = hdfg.Attribute(list=lv)
        else:
            print("Unrecognized type!")
            exit(0)
        return attr

    def handle_function(self, expr):
        if expr.function_id().getText() not in self.functions.keys():

            arguments = self.get_args(expr.expression_list())
            fname = self.getText(expr.function_id())
            self.instances.append((fname, arguments))
            cdef = hdfg.ComponentDefinition(cname=fname,
                                            is_op=False,
                                            ordered_args=arguments,
                                            op_name='wait')
            print(expr.getText())
            self.add_component(expr.getText(), cdef)

        else:
            #TODO: Check assignment handling to make sure output edges are assigned
            id = expr.getText()
            fname = expr.function_id().getText()

            if expr.expression_list():
                arguments = self.get_args(expr.expression_list())

                inputs = {}
                for arg in range(len(arguments)):
                    inp_attr = {'local_name': arguments[arg],
                                'parent_cdef': self.scope,
                                'iposition': [arg],
                                'local_dst': [id]}
                    inputs[arguments[arg]] = self.add_edge(arguments[arg], inp_attr, check_var_exists=True)



            else:
                inputs = []
            dtype = self.dtypes[self.function_dtypes[fname]]

            ## TODO: Handle function output types
            out_attr = {'local_name': id,
                        'parent_cdef': self.scope,
                        'oposition': [0],
                        'local_src': [id],
                        'type' : dtype}
            outputs = {id :self.add_edge(id, out_attr)}
            cdef = hdfg.ComponentDefinition(cname=id,
                                            is_op=True,
                                            op_name=fname)
            self.add_component(id, cdef, inputs=inputs, outputs=outputs)


    def handle_array(self, expr):
        fid = self.getText(expr.IDENTIFIER())

        id = self.getText(expr)
        dimtext = self.dims.pop()
        if self.assigned_value:
            dtype = self.get_dtype([fid, self.assigned_value], id)
        else:
            dtype = self.get_dtype([fid], id)
        inputs = {}
        outputs = {}
        if self.assign:
            instr_op = 'offset_assign'
            assign_attr = {
                'local_name' : fid,
                'parent_cdef' : self.scope,
                'iposition' : [0],
                'type' : dtype,
                'local_dst': [id]
            }
            edge = self.add_edge(fid, assign_attr)
        else:
            instr_op = 'offset'
            assign_attr = {
                'local_name': fid,
                'parent_cdef': self.scope,
                'iposition': [0],
                'type': dtype,
                'local_dst': [id]
            }
            edge = self.add_edge(fid, assign_attr, check_var_exists=True)


        inputs[fid] = edge
        idx_attr = {'local_name' : dimtext,
                             'parent_cdef' : self.scope,
                             'iposition' : [1],
                             'type':self.dtypes['int'],
                             'is_index':True,
                             'local_dst' : [id]}
        idx_edge = self.add_edge(dimtext, idx_attr)

        inputs[dimtext] = idx_edge
        out_attr = {'local_name':id,
                       'parent_cdef' : self.scope,
                       'oposition':[0],
                       'type':dtype,
                       'local_src' : [id],
                       'local_var_id': fid}
        outputs[id] = self.add_edge(id, out_attr)

        cdef = hdfg.ComponentDefinition(cname=id,
                                        is_op=True,
                                        op_name=instr_op)
        self.add_component(id, cdef, inputs=inputs, outputs=outputs)

    def handle_group(self, expr):
        op = expr.IDENTIFIER().getText()
        expr_arg = self.getText(expr.expression())
        id = self.getText(expr)
        dimtext = self.dims.pop()
        in1_attr = {
            'local_name': dimtext,
            'parent_cdef': self.scope,
            'iposition': [1],
            'type': self.dtypes['int'],
            'local_dst': [id],
            'is_index' : True
        }
        in0_attr = {
            'local_name' : expr_arg,
            'parent_cdef' : self.scope,
            'iposition' : [0],
            'type' : self.get_dtype([expr_arg], id),
            'local_dst' : [id]
        }
        inputs = {expr_arg : self.add_edge(expr_arg, in0_attr),
                  dimtext : self.add_edge(dimtext, in1_attr)}
        out_attr = {
            'local_name' : id,
            'parent_cdef' : self.scope,
            'oposition' : [0],
            'type' : self.get_dtype([expr_arg], id),
            'local_src' : [id]
        }
        outputs = {id: self.add_edge(id, out_attr)}

        cdef = hdfg.ComponentDefinition(cname=id,
                                        is_op=True,
                                        op_name=op)
        self.add_component(id, cdef, inputs=inputs, outputs=outputs)


    def handle_flow_declaration(self, arr):
        fid = self.getText(arr.IDENTIFIER())
        cname = arr.getText()

        inputs = {}
        dims = []
        for dim in self.fdims.pop():
            name = self.getText(dim.expression())
            dims.append(name)
            inp_attr = {'local_name' : name,
                                 'parent_cdef' : self.scope,
                                 'iposition' : [len(inputs)],
                                 'type':self.dtypes['int'],
                                 'is_static':True,
                                 'local_dst' : [cname]}
            edge = self.add_edge(name, inp_attr)
            inputs[name] = edge
        out_attr = {'local_name':fid,
                               'parent_cdef' : self.scope,
                               'oposition': [0],
                               'type':self.dtypes[self.dtype],
                               'dims':dims,
                               'local_src' : [cname]}
        outputs = {}
        outputs[fid] = self.add_edge(fid, out_attr)
        cdef = hdfg.ComponentDefinition(cname=cname,
                                        is_op=True,
                                        op_name='edge')

        self.add_component(cname, cdef, inputs=inputs, outputs=outputs)

    # Enter a parse tree produced by CMLangv2Parser#component_definition.
    def enterComponent_definition(self, ctx:CMLangv2Parser.Component_definitionContext):

        self.scope = ctx.IDENTIFIER().getText()
        self.cdef = hdfg.ComponentDefinition(cname=self.scope, is_op=False)
        self.component_type = ctx.component_type().getText()
        self.inputs = {}
        self.outputs = {}
        self.states = {}
        self.parameters = {}
        self.instances = []
        self.indices = {}
        self.flows = []
        self.dfg = nx.DiGraph()
        self.local_edges = {}
        self.local_component_ids = 0
        self.uses = {}
        self.times = {}
        self.assign=False
        self.pred_id = None
        self.pred_val = None
        self.boolid = None
        self.tid = None
        self.fid = None
        self.is_flow_decl=False
        self.assigned_value=None

        self.dims = deque()


    # Exit a parse tree produced by CMLangv2Parser#component_definition.
    def exitComponent_definition(self, ctx:CMLangv2Parser.Component_definitionContext):

        self.graph.component_definitions[self.scope].CopyFrom(self.cdef)

        self.component_definition_id += 1

        del self.scope
        del self.inputs

        del self.states
        del self.outputs
        del self.parameters
        del self.instances
        del self.dfg
        del self.flows
        del self.indices
        del self.local_edges
        del self.assign
        del self.assigned_value

    # Enter a parse tree produced by CMLangv2Parser#flow.
    def enterFlow(self, ctx:CMLangv2Parser.FlowContext):
        self.ftype = ctx.flow_type().getText()
        self.dtype = ctx.dtype_specifier().getText()
        self.default = None
        self.fdims = []


    # Exit a parse tree produced by CMLangv2Parser#flow.
    def exitFlow(self, ctx:CMLangv2Parser.FlowContext):
        if self.ftype == 'input':
            attr = {'local_name' :self.fid,
                          'parent_cdef' :self.scope,
                          'type': self.dtypes[self.dtype],
                          'is_queue' :True,
                          'dims' : self.fdims,
                          'iposition' : [len(self.flows)]
            }
            edge = hdfg.EdgeInfo(**attr)
            self.inputs[self.fid] = edge

        elif self.ftype == 'state':
            attr = {'local_name' :self.fid,
                          'parent_cdef' :self.scope,
                          'type': self.dtypes[self.dtype],
                          'is_state' : True,
                          'dims' : self.fdims,
                          'iposition' : [len(self.flows)]
            }
            edge = hdfg.EdgeInfo(**attr)
            self.states[self.fid] = edge

        elif self.ftype == 'output':
            attr = {'local_name' :self.fid,
                          'parent_cdef' :self.scope,
                          'type': self.dtypes[self.dtype],
                          'is_queue' :True,
                          'dims' : self.fdims,
                          'iposition' : [len(self.flows)]
            }

            edge = hdfg.EdgeInfo(**attr)
            self.outputs[self.fid] = edge

        elif self.ftype == 'param':
            attr = {'local_name' :self.fid,
                          'parent_cdef' :self.scope,
                          'type': self.dtypes[self.dtype],
                          'is_static' :True,
                          'dims' : self.fdims,
                          'default' :self.default,
                          'iposition' : [len(self.flows)]
            }
            edge = hdfg.EdgeInfo(**attr)
            self.parameters[self.fid] = edge

        else:
            print('Invalid flow type: {}'.format(self.ftype))
            exit(0)
        self.add_edge(self.fid, attr)
        self.flows.append(self.fid)
        del edge
        del self.ftype
        del self.fdims


    # Enter a parse tree produced by CMLangv2Parser#flow_expression.
    def enterFlow_expression(self, ctx:CMLangv2Parser.Flow_expressionContext):
        self.fid = ctx.IDENTIFIER().getText()

        # TODO: Evaluate literal and error when non-param has default
        if ctx.EQ():
            self.default = self.handle_literal(ctx.literal())


    def enterFlow_index(self, ctx: CMLangv2Parser.Flow_indexContext):
        id = ctx.IDENTIFIER().getText()
        attr = {'local_name' : id,
                'parent_cdef' : self.scope,
                'iposition': [len(self.fdims)],
                'type' : self.dtypes['int'],
                'is_static': True,
                'local_dst': [self.fid]}
        self.fdims.append(id)
        self.add_edge(id, attr)



    def enterFlow_declaration_list(self, ctx:CMLangv2Parser.Flow_declaration_listContext):
        self.is_flow_decl = True
        self.fdims = deque()

    def exitFlow_declaration_list(self, ctx:CMLangv2Parser.Flow_declaration_listContext):
        for arr in range(len(ctx.array_expression())):
            self.handle_flow_declaration(ctx.array_expression()[arr])
        self.is_flow_decl = False

        del self.fdims



    # Enter a parse tree produced by CMLangv2Parser#index_declaration.
    def enterIndex_declaration(self, ctx:CMLangv2Parser.Index_declarationContext):
        if ctx.IDENTIFIER().getText() in self.local_edges.keys():
            print("Redeclaration of index {}".format(ctx.IDENTIFIER().getText()))
        else:
            self.idx_id = ctx.IDENTIFIER().getText()


    # Exit a parse tree produced by CMLangv2Parser#index_declaration.
    #TODO: add node for index
    def exitIndex_declaration(self, ctx:CMLangv2Parser.Index_declarationContext):
        cname = ctx.getText()
        upper = ctx.expression()[1]
        lower = ctx.expression()[0]
        if upper.number():
            upper_attr = self.handle_literal(upper)
        else:
            upper_attr = hdfg.Attribute(s=upper.getText())
        if lower.number():
            lower_attr = self.handle_literal(lower)
        else:
            lower_attr = hdfg.Attribute(s=lower.getText())
        inp_attr_lower = {'local_name':lower.getText(),
                               'parent_cdef': self.scope,
                               'iposition' : [0],
                               'type' : self.dtypes['int'],
                               'local_dst':[cname]}
        inp_attr_upper = {'local_name' : upper.getText(),
                               'parent_cdef': self.scope,
                               'iposition' : [1],
                               'type' : self.dtypes['int'],
                               'local_dst' : [cname]}
        inputs = {lower.getText() : self.add_edge(lower.getText(), inp_attr_lower),
                  upper.getText() : self.add_edge(upper.getText(), inp_attr_upper)
                  }
        out_attr = {
            'local_name' : self.idx_id,
            'parent_cdef' : self.scope,
            'oposition' : [0],
            'is_index' : True,
            'local_src' : [cname],
            'lower' : lower_attr,
            'upper' : upper_attr
        }
        outputs = {}
        outputs[self.idx_id] = self.add_edge(self.idx_id, out_attr)
        cdef = hdfg.ComponentDefinition(cname=cname,
                                        is_op=True,
                                        op_name='edge')

        self.add_component(cname, cdef, inputs=inputs, outputs=outputs)
        del self.idx_id


    # Enter a parse tree produced by CMLangv2Parser#prefix_expression.
    def enterPrefix_expression(self, ctx:CMLangv2Parser.Prefix_expressionContext):
        self.assign=True


    # Exit a parse tree produced by CMLangv2Parser#prefix_expression.
    def exitPrefix_expression(self, ctx:CMLangv2Parser.Prefix_expressionContext):
        if ctx.array_expression():
            self.fid = ctx.array_expression().IDENTIFIER().getText()
            self.handle_array(ctx.array_expression())
        else:
            self.fid = ctx.IDENTIFIER().getText()

        self.assign=False


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
            if len(ctx.expression()) > 1:
                e1 = self.getText(ctx.expression()[0])
                e2 = self.getText(ctx.expression()[1])
                op1_attr = {
                    'local_name': e1,
                    'parent_cdef': self.scope,
                    'iposition': [0],
                    'local_dst': id
                }
                op2_attr = {
                    'local_name': e2,
                    'parent_cdef': self.scope,
                    'iposition': [1],
                    'local_dst': id
                }
                inputs = {e1 : self.add_edge(e1, op1_attr),
                          e2 : self.add_edge(e2, op2_attr)}
                parents = [e1, e2]
                self.expop = self.getText(ctx.getChild(1))
            else:

                self.expop = self.getText(ctx.getChild(0))
                e1 = self.getText(ctx.expression()[0])
                parents = [e1]
                op1_attr = {
                    'local_name': e1,
                    'parent_cdef': self.scope,
                    'iposition': [0],
                    'local_dst': id
                }
                inputs = {e1 :self.add_edge(e1, op1_attr)}
            out_attr  = {
                'local_name' : id,
                'parent_cdef' : self.scope,
                'oposition' : [0],
                'type' : self.get_dtype(parents, id),
                'local_src' : id
            }
            outputs = {id :self.add_edge(id, out_attr)}
            cdef = hdfg.ComponentDefinition(cname=id,
                                            is_op=True,
                                            op_name=self.expop)

            self.add_component(id, cdef, inputs=inputs, outputs=outputs)


            del self.expop
        elif ctx.IDENTIFIER():
            id = ctx.getText()
            id_attr = {'local_name' : id,
                       'parent_cdef' : self.scope}
            self.add_edge(id,id_attr, check_var_exists=True)
        elif ctx.number():
            if ctx.number().integer():
                attr = hdfg.Attribute(i=int(ctx.number().getText()))
                dtype = self.dtypes['int']
            elif ctx.number().FLOAT_NUMBER():
                attr = hdfg.Attribute(f=float(ctx.number().getText()))
                dtype = self.dtypes['float']
            else:
                num = complex(ctx.getText().replace(" ", "").replace("i", "j"))
                real = num.real
                imag = num.imag
                lv = hdfg.Attribute.ListValue(f=[real, imag])
                attr = hdfg.Attribute(list=lv)
                dtype = self.dtypes['complex']
            id = ctx.getText()
            in_attr = {
                'local_name' : id,
                'parent_cdef' : self.scope,
                'iposition' : [1],
                'type' : dtype,
                'default' : attr
            }
            _ = self.add_edge(id, in_attr)

        # self.dtype = None

    def enterAssignment_expression(self, ctx:CMLangv2Parser.Assignment_expressionContext):
        if ctx.expression():
            self.assigned_value = self.getText(ctx.expression())
        else:
            self.assigned_value = self.getText(ctx.predicate_expression().true_expression())

    def exitAssignment_expression(self, ctx:CMLangv2Parser.Assignment_expressionContext):
        #TODO: Change to point to same ID and check for flow
        id = self.getText(ctx.prefix_expression())
        ## TODO: Change destination of assignment node
        #TODO: check if last assignment to value before writing
        if ctx.expression():
            expr_text = self.getText(ctx.expression())

            edge = self.cdef.sub_edges[expr_text]
            new_edge = edge
            new_edge.local_name = id
            self.cdef.sub_edges[id].CopyFrom(edge)
            self.local_edges[id] = edge
            self.uses[id] = 1
            if self.fid in self.outputs.keys() or self.fid in self.states.keys():
                cdef = hdfg.ComponentDefinition(cname=expr_text,
                                                is_op=True,
                                                op_name='write')
                cdef.inputs[expr_text].CopyFrom(edge)
                cdef.outputs[id].CopyFrom(new_edge)
                self.add_component(expr_text, cdef)
            del self.fid
        self.assigned_value = None


    # Exit a parse tree produced by CMLangv2Parser#index_expression_list.
    def exitIndex_expression_list(self, ctx:CMLangv2Parser.Index_expression_listContext):
        if self.is_flow_decl:
            self.fdims.appendleft(ctx.index_expression())
        else:
            if len(ctx.index_expression()) > 1:
                dim1 = self.getText(ctx.index_expression()[0].expression())
                dim2 = self.getText(ctx.index_expression()[1].expression())
                dim_list = [dim1, dim2]
                result = '[' + dim1 + '][' + dim2 + ']'
                out_attr = {
                    'local_name' : result,
                    'parent_cdef' : self.scope,
                    'oposition' : [0],
                    'is_index' : True,
                    'type' : self.dtypes['int'],
                    'local_src' : [result],
                    'dims' : dim_list
                }
                dim1_attr = {'local_name' : dim1,
                    'parent_cdef' : self.scope,
                    'iposition' : [0],
                    'is_index' : True,
                    'type' : self.dtypes['int'],
                    'local_dst' : [result]
                             }
                dim2_attr = {'local_name' : dim2,
                    'parent_cdef' : self.scope,
                    'iposition' : [1],
                    'is_index' : True,
                    'type' : self.dtypes['int'],
                    'local_dst' : [result]
                             }
                o_edge = self.add_edge(result, out_attr)

                inputs = {dim1 : self.add_edge(dim1, dim1_attr),
                          dim2 : self.add_edge(dim2, dim2_attr)}
                outputs = {result: o_edge}
                cdef = hdfg.ComponentDefinition(cname=result,
                                                is_op=True,
                                                op_name='index')

                self.add_component(result, cdef, inputs=inputs, outputs=outputs)

                if len(ctx.index_expression()) > 2:
                    for idx in ctx.index_expression()[2:]:
                        dimn = self.getText(idx.expression())
                        dim_list.append(dimn)
                        prev = result
                        result += '[' + dimn + ']'
                        dimn_attr = {'local_name': dimn,
                                     'parent_cdef': self.scope,
                                     'iposition': [1],
                                     'is_index': True,
                                     'type': self.dtypes['int'],
                                     'local_dst': [result]
                                     }
                        dim_prev_attr = {'local_name': prev,
                                     'iposition': [0],
                                     'local_dst': [result]
                                     }
                        out_attr = {
                            'local_name': result,
                            'parent_cdef': self.scope,
                            'oposition': [0],
                            'is_index': True,
                            'type': self.dtypes['int'],
                            'local_src': [result],
                            'dims': dim_list
                        }
                        inputs = {dimn : self.add_edge(dimn, dimn_attr),
                                  prev : self.add_edge(prev, dim_prev_attr)}
                        outputs = {result : self.add_edge(result, out_attr)}

                        cdef = hdfg.ComponentDefinition(cname=result,
                                                        is_op=True,
                                                        op_name='index')

                        self.add_component(result, cdef, inputs=inputs, outputs=outputs)

                self.dims.append(result)
            else:
                self.dims.append(self.getText(ctx.index_expression()[0].expression()))




    # Enter a parse tree produced by CMLangv2Parser#declaration_statement.
    def enterDeclaration_statement(self, ctx:CMLangv2Parser.Declaration_statementContext):
        if ctx.INDEX():
            self.dtype = self.getText(ctx.INDEX())
        else:
            self.dtype = self.getText(ctx.dtype_specifier())

    # Exit a parse tree produced by CMLangv2Parser#declaration_statement.
    def exitDeclaration_statement(self, ctx:CMLangv2Parser.Declaration_statementContext):
        self.dtype = None

    def enterPredicate_expression(self, ctx:CMLangv2Parser.Predicate_expressionContext):
        self.boolid= self.getText(ctx.bool_expression())
        self.tid = self.getText(ctx.true_expression())
        self.fid = self.getText(ctx.false_expression())

    def enterTrue_expression(self, ctx:CMLangv2Parser.True_expressionContext):
        self.pred_id = self.tid
        self.pred_val = 't'
    def exitTrue_expression(self, ctx:CMLangv2Parser.True_expressionContext):
        self.pred_id = None
        self.pred_val = None
    def enterFalse_expression(self, ctx:CMLangv2Parser.True_expressionContext):
        self.pred_id = self.fid
        self.pred_val = 'f'


    def exitFalse_expression(self, ctx:CMLangv2Parser.True_expressionContext):
        self.pred_id = None
        self.pred_val = None

    # Exit a parse tree produced by CMLangv2Parser#predicate_expression.
    def exitPredicate_expression(self, ctx:CMLangv2Parser.Predicate_expressionContext):
        self.boolid = None
        self.tid = None
        self.fid = None

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

    compiler = CMLangCompiler(fname, draw=draw)
    walker = ParseTreeWalker()
    walker.walk(compiler, tree)

    graph = HDFG(compiler.graph)
    # graph = HDFG(fname, compiler, tree, print_code=print_code, commented=commented)

if __name__ == '__main__':

    parse_file('../test/examples/simple_example_v2.cm', draw=True)