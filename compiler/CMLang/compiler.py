#!/usr/bin/env python3
from antlr4 import *

# import json
import os
from antlr4.tree.Trees import Trees
from CMLang.CMLangLexer import CMLangLexer
from CMLang.CMLangParser import CMLangParser
from CMLang.CMLangVisitor import CMLangVisitor
from CMLang.CMLangListener import CMLangListener
from CMLang.HDFG import HDFG, Component, Node
import pprint
import networkx as nx


class CMLangCompiler(CMLangListener):

    def __init__(self):
        self.symbols = []
        self.symbol_id = 0
        self.scope = ''
        self.component_def = {}
        self.component_inst = {}
        self.variables = {}
        self.primitives = []
        self.flows = {}
        self.iterators = {}
        self.args = {}

        self.fdeclaration = False
        self.ideclaration = False
        self.primitive = False
        self.assignee = False

    def evaluateNumber(self, number):
        if number.integer():
            return ('int', int(number.integer().getText()))
        elif number.FLOAT_NUMBER():
            return ('float', float(number.FLOAT_NUMBER().getText()))
        else:
            return ('imag', complex(number.getText()))
        # Enter a parse tree produced by CMLangParser#number.


    def add_symbol(self, name, ttype):
        self.symbols.append((self.symbol_id, name, ttype))
        self.symbol_id += 1

    def add_component_def(self):


        self.component_def[self.scope] = {'id' : self.component_definition_id,
                                    'component_type' : self.component_type,
                                    'args': self.args,
                                    'vars' : self.vars,
                                    'primitives' : self.primitives,
                                    'instances' : self.instances}

        del self.component_definition_id
        del self.scope
        del self.args
        del self.vars
        del self.primitives
        del self.instances


    def add_arg(self):
        self.args[self.argname] = {'id' : self.arg_id,
                                    'type': self.atype,
                                    'edge_type' : self.edge_type,
                                    'position' : self.position,
                                    'dimensions' : self.dimensions,
                                    'default' : self.default_value}
        print(self.args[self.argname])

        del self.arg_id
        del self.argname
        del self.atype
        del self.edge_type
        del self.default_value

    ## TODO: Need to figure out info to go in here
    def add_var(self):

        if self.var_name not in self.vars.keys():
            self.vars[self.var_name] = {'id' : self.symbol_id,
                                      'type': self.type}
            self.add_symbol(self.var_name, 'variable')
            del self.var_name


    def add_component_instance(self):
        i = 1
        name = self.instance_name + '$' + str(i)
        while name in self.component_inst.keys():
            i = i+1
            name = self.instance_name + '$' + str(i)

        self.instances.append(name)
        self.component_inst[name] = {'id' : self.symbol_id,
                                    'component_definition': self.instance_name,
                                    'parent' : self.scope,
                                    'args' : self.instargs}
        self.add_symbol(name, 'component_instance')

    def add_flow(self):
        name = self.scope + ':' + self.flow_name
        ## Assert no redeclaration
        self.flows[name] = {
            'id' : self.symbol_id - 1,
            'local_name' : self.flow_name,
            'scope' : self.scope,
            'dimensions' : self.dimensions
        }
        del self.flow_name

    def add_iter(self):

        ## Assert no redeclaration
        ## evluate bounds
        name = self.scope + ':' + self.iter_name
        self.iterators[name] = {
            'id': self.symbol_id - 1,
            'local_name': self.iter_name,
            'low' : self.low,
            'high' : self.high,
            'scope': self.scope
        }

        del self.low
        del self.high



    def enterComponent_definition(self, ctx:CMLangParser.Component_definitionContext):
        self.scope = ctx.ID().getText()
        self.component_definition_id = self.symbol_id
        self.add_symbol(self.scope, 'component_definition')
        self.component_type = ctx.component_type().getText()
        self.position = 0
        self.args = {}
        self.vars = {}
        self.primitives = []
        self.instances = []
        self.dag = nx.DiGraph()

    def exitComponent_definition(self, ctx:CMLangParser.Component_definitionContext):
        self.add_component_def()

    def enterArg(self, ctx:CMLangParser.ArgContext):
        self.var_name = ctx.ID().getText()
        self.atype = ctx.val_type().getText()
        self.type = ctx.val_type().getText()
        self.edge_type = ctx.arg_type().getText()
        self.arg_id = self.symbol_id
        self.argname = self.var_name
        self.default_value = None
        self.add_var()
        self.dimensions = []
        del self.type


    def exitArg(self, ctx:CMLangParser.ArgContext):

        self.add_arg()
        del self.dimensions
        self.position += 1

    def enterDefault_param_value(self, ctx:CMLangParser.Default_param_valueContext):
        # TODO: Get actual value instead
        self.default_value = ctx.STRING().getText() if ctx.STRING() else ctx.number().getText()



    def enterFlow_def_index(self, ctx:CMLangParser.Flow_def_indexContext):
        self.var_name = ctx.ID().getText()
        self.dimensions.append(self.var_name)
        self.type = 'int'
        self.add_var()
        del self.type


    def enterComponent_inst(self, ctx:CMLangParser.Component_instContext):
        self.instance_name = ctx.ID().getText()
        self.instargs = []

    def enterComp_param_id(self, ctx:CMLangParser.Call_param_idContext):
        if ctx.ID():
            self.instargs.append((ctx.ID().getText(), 'var'))
        elif ctx.number():
            # TODO: Evaluate value
            self.instargs.append((ctx.number().getText(), 'number'))
        else:
            self.instargs.append((ctx.STRING().getText(), 'string'))

    def exitComponent_inst(self, ctx:CMLangParser.Component_instContext):
        self.add_component_instance()



    def enterFlow_declaration(self, ctx:CMLangParser.Flow_declarationContext):
        self.type = ctx.val_type().getText()
        self.fdeclaration = True

    def exitFlow_declaration(self, ctx:CMLangParser.Flow_declarationContext):
        self.fdeclaration = False
        del self.type

    def enterIndex_declaration(self, ctx:CMLangParser.Flow_declarationContext):
        self.type = 'iterator'
        self.ideclaration = True

    def exitIndex_declaration(self, ctx:CMLangParser.Flow_declarationContext):
        self.ideclaration = False
        del self.type

    def enterVar_list_index(self, ctx:CMLangParser.Var_list_indexContext):
        self.low = ctx.expr()[0]
        self.high = ctx.expr()[1]

    def enterFlow_index(self, ctx:CMLangParser.Flow_indexContext):
        ##TODO: Evaluate

        if self.fdeclaration:
            self.dimensions.append(ctx.expr())

    def enterFlow(self, ctx:CMLangParser.FlowContext):
        self.dimensions = []
        self.flow_name = ctx.ID().getText()
        self.var_name = self.flow_name
        self.add_var()
        self.add_symbol(self.flow_name, 'flow')

    def exitFlow(self, ctx:CMLangParser.FlowContext):
        self.add_flow()
        del self.dimensions


    def exitVar_list_index(self, ctx:CMLangParser.Var_list_indexContext):
        self.iter_name = ctx.ID().getText()
        self.var_name = self.iter_name
        self.add_var()
        self.add_symbol(self.iter_name, 'iterator')
        self.add_iter()

    def exitStatement(self, ctx:CMLangParser.StatementContext):
        if ctx.component_inst():
            self.primitives.append(('comp', ctx.component_inst()))
        elif ctx.cond_loop():
            self.primitives.append(('loop', ctx.cond_loop()))

    def enterPrimitive(self, ctx:CMLangParser.PrimitiveContext):

        if ctx.expr():
            self.primitives.append(('assign', ctx.var(), ctx.expr()))
        elif ctx.predicate():
            self.primitives.append(('predicate', ctx.var(), ctx.predicate()))
        elif ctx.file_operation():
            self.primitives.append(('file', ctx.file_operation()))
        elif ctx.data_decl():
            self.primitives.append(('decl', ctx.data_decl()))

def parse_file(fname, print_code=True, commented=True):
    input_file = FileStream(fname)
    lexer = CMLangLexer(input_file)
    stream = CommonTokenStream(lexer)
    parser = CMLangParser(stream)
    tree = parser.program()

    compiler = CMLangCompiler()
    walker = ParseTreeWalker()
    walker.walk(compiler, tree)
    graph = HDFG(fname, compiler, tree, print_code=print_code, commented=commented)

if __name__ == '__main__':
    parse_file()


