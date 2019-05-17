# Generated from /Users/seankinzer/ACTLab/cmlang/cmlang.code/compiler/CMLang/CMLang.g4 by ANTLR 4.7
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CMLangParser import CMLangParser
else:
    from CMLangParser import CMLangParser

# This class defines a complete generic visitor for a parse tree produced by CMLangParser.

class CMLangVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CMLangParser#number.
    def visitNumber(self, ctx:CMLangParser.NumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#integer.
    def visitInteger(self, ctx:CMLangParser.IntegerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#val_type.
    def visitVal_type(self, ctx:CMLangParser.Val_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#program.
    def visitProgram(self, ctx:CMLangParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#component_list.
    def visitComponent_list(self, ctx:CMLangParser.Component_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#component_definition.
    def visitComponent_definition(self, ctx:CMLangParser.Component_definitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#component_parameters.
    def visitComponent_parameters(self, ctx:CMLangParser.Component_parametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#arg_list.
    def visitArg_list(self, ctx:CMLangParser.Arg_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#default_param_value.
    def visitDefault_param_value(self, ctx:CMLangParser.Default_param_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#flow_def_index.
    def visitFlow_def_index(self, ctx:CMLangParser.Flow_def_indexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#arg.
    def visitArg(self, ctx:CMLangParser.ArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#parameter_arg_def.
    def visitParameter_arg_def(self, ctx:CMLangParser.Parameter_arg_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#arg_type.
    def visitArg_type(self, ctx:CMLangParser.Arg_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#component_type.
    def visitComponent_type(self, ctx:CMLangParser.Component_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#component_body.
    def visitComponent_body(self, ctx:CMLangParser.Component_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#statement_list.
    def visitStatement_list(self, ctx:CMLangParser.Statement_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#statement.
    def visitStatement(self, ctx:CMLangParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#primitive.
    def visitPrimitive(self, ctx:CMLangParser.PrimitiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#data_decl.
    def visitData_decl(self, ctx:CMLangParser.Data_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#flow_declaration.
    def visitFlow_declaration(self, ctx:CMLangParser.Flow_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#iterator_declaration.
    def visitIterator_declaration(self, ctx:CMLangParser.Iterator_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#power.
    def visitPower(self, ctx:CMLangParser.PowerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#iterator.
    def visitIterator(self, ctx:CMLangParser.IteratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#flow.
    def visitFlow(self, ctx:CMLangParser.FlowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#var_list_flow.
    def visitVar_list_flow(self, ctx:CMLangParser.Var_list_flowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#var_list_flow_tail.
    def visitVar_list_flow_tail(self, ctx:CMLangParser.Var_list_flow_tailContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#var_list.
    def visitVar_list(self, ctx:CMLangParser.Var_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#var.
    def visitVar(self, ctx:CMLangParser.VarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#var_id.
    def visitVar_id(self, ctx:CMLangParser.Var_idContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#id_tail.
    def visitId_tail(self, ctx:CMLangParser.Id_tailContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#flow_index.
    def visitFlow_index(self, ctx:CMLangParser.Flow_indexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#var_list_tail.
    def visitVar_list_tail(self, ctx:CMLangParser.Var_list_tailContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#var_list_iterator.
    def visitVar_list_iterator(self, ctx:CMLangParser.Var_list_iteratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#component_inst.
    def visitComponent_inst(self, ctx:CMLangParser.Component_instContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#call_param_id.
    def visitCall_param_id(self, ctx:CMLangParser.Call_param_idContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#comp_param_id.
    def visitComp_param_id(self, ctx:CMLangParser.Comp_param_idContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#comp_param_list.
    def visitComp_param_list(self, ctx:CMLangParser.Comp_param_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#comp_param_list_tail.
    def visitComp_param_list_tail(self, ctx:CMLangParser.Comp_param_list_tailContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#call_param_list.
    def visitCall_param_list(self, ctx:CMLangParser.Call_param_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#call_param_list_tail.
    def visitCall_param_list_tail(self, ctx:CMLangParser.Call_param_list_tailContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#file_function.
    def visitFile_function(self, ctx:CMLangParser.File_functionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#file_operation.
    def visitFile_operation(self, ctx:CMLangParser.File_operationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#function.
    def visitFunction(self, ctx:CMLangParser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#predicate.
    def visitPredicate(self, ctx:CMLangParser.PredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#logic.
    def visitLogic(self, ctx:CMLangParser.LogicContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#add_sub.
    def visitAdd_sub(self, ctx:CMLangParser.Add_subContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#mul_div.
    def visitMul_div(self, ctx:CMLangParser.Mul_divContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#expr.
    def visitExpr(self, ctx:CMLangParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#logical_expr.
    def visitLogical_expr(self, ctx:CMLangParser.Logical_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#add_sub_expr.
    def visitAdd_sub_expr(self, ctx:CMLangParser.Add_sub_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#factor.
    def visitFactor(self, ctx:CMLangParser.FactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#signed_value.
    def visitSigned_value(self, ctx:CMLangParser.Signed_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#atom.
    def visitAtom(self, ctx:CMLangParser.AtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#function_args.
    def visitFunction_args(self, ctx:CMLangParser.Function_argsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#cond_loop.
    def visitCond_loop(self, ctx:CMLangParser.Cond_loopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLangParser#iter_expression.
    def visitIter_expression(self, ctx:CMLangParser.Iter_expressionContext):
        return self.visitChildren(ctx)



del CMLangParser