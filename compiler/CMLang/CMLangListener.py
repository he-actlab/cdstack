# Generated from /Users/seankinzer/ACTLab/cmlang/cmlang.code/compiler/CMLang/CMLang.g4 by ANTLR 4.7
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CMLangParser import CMLangParser
else:
    from CMLangParser import CMLangParser

# This class defines a complete listener for a parse tree produced by CMLangParser.
class CMLangListener(ParseTreeListener):

    # Enter a parse tree produced by CMLangParser#number.
    def enterNumber(self, ctx:CMLangParser.NumberContext):
        pass

    # Exit a parse tree produced by CMLangParser#number.
    def exitNumber(self, ctx:CMLangParser.NumberContext):
        pass


    # Enter a parse tree produced by CMLangParser#integer.
    def enterInteger(self, ctx:CMLangParser.IntegerContext):
        pass

    # Exit a parse tree produced by CMLangParser#integer.
    def exitInteger(self, ctx:CMLangParser.IntegerContext):
        pass


    # Enter a parse tree produced by CMLangParser#val_type.
    def enterVal_type(self, ctx:CMLangParser.Val_typeContext):
        pass

    # Exit a parse tree produced by CMLangParser#val_type.
    def exitVal_type(self, ctx:CMLangParser.Val_typeContext):
        pass


    # Enter a parse tree produced by CMLangParser#program.
    def enterProgram(self, ctx:CMLangParser.ProgramContext):
        pass

    # Exit a parse tree produced by CMLangParser#program.
    def exitProgram(self, ctx:CMLangParser.ProgramContext):
        pass


    # Enter a parse tree produced by CMLangParser#component_list.
    def enterComponent_list(self, ctx:CMLangParser.Component_listContext):
        pass

    # Exit a parse tree produced by CMLangParser#component_list.
    def exitComponent_list(self, ctx:CMLangParser.Component_listContext):
        pass


    # Enter a parse tree produced by CMLangParser#component_definition.
    def enterComponent_definition(self, ctx:CMLangParser.Component_definitionContext):
        pass

    # Exit a parse tree produced by CMLangParser#component_definition.
    def exitComponent_definition(self, ctx:CMLangParser.Component_definitionContext):
        pass


    # Enter a parse tree produced by CMLangParser#component_parameters.
    def enterComponent_parameters(self, ctx:CMLangParser.Component_parametersContext):
        pass

    # Exit a parse tree produced by CMLangParser#component_parameters.
    def exitComponent_parameters(self, ctx:CMLangParser.Component_parametersContext):
        pass


    # Enter a parse tree produced by CMLangParser#arg_list.
    def enterArg_list(self, ctx:CMLangParser.Arg_listContext):
        pass

    # Exit a parse tree produced by CMLangParser#arg_list.
    def exitArg_list(self, ctx:CMLangParser.Arg_listContext):
        pass


    # Enter a parse tree produced by CMLangParser#default_param_value.
    def enterDefault_param_value(self, ctx:CMLangParser.Default_param_valueContext):
        pass

    # Exit a parse tree produced by CMLangParser#default_param_value.
    def exitDefault_param_value(self, ctx:CMLangParser.Default_param_valueContext):
        pass


    # Enter a parse tree produced by CMLangParser#flow_def_index.
    def enterFlow_def_index(self, ctx:CMLangParser.Flow_def_indexContext):
        pass

    # Exit a parse tree produced by CMLangParser#flow_def_index.
    def exitFlow_def_index(self, ctx:CMLangParser.Flow_def_indexContext):
        pass


    # Enter a parse tree produced by CMLangParser#arg.
    def enterArg(self, ctx:CMLangParser.ArgContext):
        pass

    # Exit a parse tree produced by CMLangParser#arg.
    def exitArg(self, ctx:CMLangParser.ArgContext):
        pass


    # Enter a parse tree produced by CMLangParser#parameter_arg_def.
    def enterParameter_arg_def(self, ctx:CMLangParser.Parameter_arg_defContext):
        pass

    # Exit a parse tree produced by CMLangParser#parameter_arg_def.
    def exitParameter_arg_def(self, ctx:CMLangParser.Parameter_arg_defContext):
        pass


    # Enter a parse tree produced by CMLangParser#arg_type.
    def enterArg_type(self, ctx:CMLangParser.Arg_typeContext):
        pass

    # Exit a parse tree produced by CMLangParser#arg_type.
    def exitArg_type(self, ctx:CMLangParser.Arg_typeContext):
        pass


    # Enter a parse tree produced by CMLangParser#component_type.
    def enterComponent_type(self, ctx:CMLangParser.Component_typeContext):
        pass

    # Exit a parse tree produced by CMLangParser#component_type.
    def exitComponent_type(self, ctx:CMLangParser.Component_typeContext):
        pass


    # Enter a parse tree produced by CMLangParser#component_body.
    def enterComponent_body(self, ctx:CMLangParser.Component_bodyContext):
        pass

    # Exit a parse tree produced by CMLangParser#component_body.
    def exitComponent_body(self, ctx:CMLangParser.Component_bodyContext):
        pass


    # Enter a parse tree produced by CMLangParser#statement_list.
    def enterStatement_list(self, ctx:CMLangParser.Statement_listContext):
        pass

    # Exit a parse tree produced by CMLangParser#statement_list.
    def exitStatement_list(self, ctx:CMLangParser.Statement_listContext):
        pass


    # Enter a parse tree produced by CMLangParser#statement.
    def enterStatement(self, ctx:CMLangParser.StatementContext):
        pass

    # Exit a parse tree produced by CMLangParser#statement.
    def exitStatement(self, ctx:CMLangParser.StatementContext):
        pass


    # Enter a parse tree produced by CMLangParser#primitive.
    def enterPrimitive(self, ctx:CMLangParser.PrimitiveContext):
        pass

    # Exit a parse tree produced by CMLangParser#primitive.
    def exitPrimitive(self, ctx:CMLangParser.PrimitiveContext):
        pass


    # Enter a parse tree produced by CMLangParser#data_decl.
    def enterData_decl(self, ctx:CMLangParser.Data_declContext):
        pass

    # Exit a parse tree produced by CMLangParser#data_decl.
    def exitData_decl(self, ctx:CMLangParser.Data_declContext):
        pass


    # Enter a parse tree produced by CMLangParser#flow_declaration.
    def enterFlow_declaration(self, ctx:CMLangParser.Flow_declarationContext):
        pass

    # Exit a parse tree produced by CMLangParser#flow_declaration.
    def exitFlow_declaration(self, ctx:CMLangParser.Flow_declarationContext):
        pass


    # Enter a parse tree produced by CMLangParser#iterator_declaration.
    def enterIterator_declaration(self, ctx:CMLangParser.Iterator_declarationContext):
        pass

    # Exit a parse tree produced by CMLangParser#iterator_declaration.
    def exitIterator_declaration(self, ctx:CMLangParser.Iterator_declarationContext):
        pass


    # Enter a parse tree produced by CMLangParser#power.
    def enterPower(self, ctx:CMLangParser.PowerContext):
        pass

    # Exit a parse tree produced by CMLangParser#power.
    def exitPower(self, ctx:CMLangParser.PowerContext):
        pass


    # Enter a parse tree produced by CMLangParser#iterator.
    def enterIterator(self, ctx:CMLangParser.IteratorContext):
        pass

    # Exit a parse tree produced by CMLangParser#iterator.
    def exitIterator(self, ctx:CMLangParser.IteratorContext):
        pass


    # Enter a parse tree produced by CMLangParser#flow.
    def enterFlow(self, ctx:CMLangParser.FlowContext):
        pass

    # Exit a parse tree produced by CMLangParser#flow.
    def exitFlow(self, ctx:CMLangParser.FlowContext):
        pass


    # Enter a parse tree produced by CMLangParser#var_list_flow.
    def enterVar_list_flow(self, ctx:CMLangParser.Var_list_flowContext):
        pass

    # Exit a parse tree produced by CMLangParser#var_list_flow.
    def exitVar_list_flow(self, ctx:CMLangParser.Var_list_flowContext):
        pass


    # Enter a parse tree produced by CMLangParser#var_list_flow_tail.
    def enterVar_list_flow_tail(self, ctx:CMLangParser.Var_list_flow_tailContext):
        pass

    # Exit a parse tree produced by CMLangParser#var_list_flow_tail.
    def exitVar_list_flow_tail(self, ctx:CMLangParser.Var_list_flow_tailContext):
        pass


    # Enter a parse tree produced by CMLangParser#var_list.
    def enterVar_list(self, ctx:CMLangParser.Var_listContext):
        pass

    # Exit a parse tree produced by CMLangParser#var_list.
    def exitVar_list(self, ctx:CMLangParser.Var_listContext):
        pass


    # Enter a parse tree produced by CMLangParser#var.
    def enterVar(self, ctx:CMLangParser.VarContext):
        pass

    # Exit a parse tree produced by CMLangParser#var.
    def exitVar(self, ctx:CMLangParser.VarContext):
        pass


    # Enter a parse tree produced by CMLangParser#var_id.
    def enterVar_id(self, ctx:CMLangParser.Var_idContext):
        pass

    # Exit a parse tree produced by CMLangParser#var_id.
    def exitVar_id(self, ctx:CMLangParser.Var_idContext):
        pass


    # Enter a parse tree produced by CMLangParser#id_tail.
    def enterId_tail(self, ctx:CMLangParser.Id_tailContext):
        pass

    # Exit a parse tree produced by CMLangParser#id_tail.
    def exitId_tail(self, ctx:CMLangParser.Id_tailContext):
        pass


    # Enter a parse tree produced by CMLangParser#flow_index.
    def enterFlow_index(self, ctx:CMLangParser.Flow_indexContext):
        pass

    # Exit a parse tree produced by CMLangParser#flow_index.
    def exitFlow_index(self, ctx:CMLangParser.Flow_indexContext):
        pass


    # Enter a parse tree produced by CMLangParser#var_list_tail.
    def enterVar_list_tail(self, ctx:CMLangParser.Var_list_tailContext):
        pass

    # Exit a parse tree produced by CMLangParser#var_list_tail.
    def exitVar_list_tail(self, ctx:CMLangParser.Var_list_tailContext):
        pass


    # Enter a parse tree produced by CMLangParser#var_list_iterator.
    def enterVar_list_iterator(self, ctx:CMLangParser.Var_list_iteratorContext):
        pass

    # Exit a parse tree produced by CMLangParser#var_list_iterator.
    def exitVar_list_iterator(self, ctx:CMLangParser.Var_list_iteratorContext):
        pass


    # Enter a parse tree produced by CMLangParser#component_inst.
    def enterComponent_inst(self, ctx:CMLangParser.Component_instContext):
        pass

    # Exit a parse tree produced by CMLangParser#component_inst.
    def exitComponent_inst(self, ctx:CMLangParser.Component_instContext):
        pass


    # Enter a parse tree produced by CMLangParser#call_param_id.
    def enterCall_param_id(self, ctx:CMLangParser.Call_param_idContext):
        pass

    # Exit a parse tree produced by CMLangParser#call_param_id.
    def exitCall_param_id(self, ctx:CMLangParser.Call_param_idContext):
        pass


    # Enter a parse tree produced by CMLangParser#comp_param_id.
    def enterComp_param_id(self, ctx:CMLangParser.Comp_param_idContext):
        pass

    # Exit a parse tree produced by CMLangParser#comp_param_id.
    def exitComp_param_id(self, ctx:CMLangParser.Comp_param_idContext):
        pass


    # Enter a parse tree produced by CMLangParser#comp_param_list.
    def enterComp_param_list(self, ctx:CMLangParser.Comp_param_listContext):
        pass

    # Exit a parse tree produced by CMLangParser#comp_param_list.
    def exitComp_param_list(self, ctx:CMLangParser.Comp_param_listContext):
        pass


    # Enter a parse tree produced by CMLangParser#comp_param_list_tail.
    def enterComp_param_list_tail(self, ctx:CMLangParser.Comp_param_list_tailContext):
        pass

    # Exit a parse tree produced by CMLangParser#comp_param_list_tail.
    def exitComp_param_list_tail(self, ctx:CMLangParser.Comp_param_list_tailContext):
        pass


    # Enter a parse tree produced by CMLangParser#call_param_list.
    def enterCall_param_list(self, ctx:CMLangParser.Call_param_listContext):
        pass

    # Exit a parse tree produced by CMLangParser#call_param_list.
    def exitCall_param_list(self, ctx:CMLangParser.Call_param_listContext):
        pass


    # Enter a parse tree produced by CMLangParser#call_param_list_tail.
    def enterCall_param_list_tail(self, ctx:CMLangParser.Call_param_list_tailContext):
        pass

    # Exit a parse tree produced by CMLangParser#call_param_list_tail.
    def exitCall_param_list_tail(self, ctx:CMLangParser.Call_param_list_tailContext):
        pass


    # Enter a parse tree produced by CMLangParser#file_function.
    def enterFile_function(self, ctx:CMLangParser.File_functionContext):
        pass

    # Exit a parse tree produced by CMLangParser#file_function.
    def exitFile_function(self, ctx:CMLangParser.File_functionContext):
        pass


    # Enter a parse tree produced by CMLangParser#file_operation.
    def enterFile_operation(self, ctx:CMLangParser.File_operationContext):
        pass

    # Exit a parse tree produced by CMLangParser#file_operation.
    def exitFile_operation(self, ctx:CMLangParser.File_operationContext):
        pass


    # Enter a parse tree produced by CMLangParser#function.
    def enterFunction(self, ctx:CMLangParser.FunctionContext):
        pass

    # Exit a parse tree produced by CMLangParser#function.
    def exitFunction(self, ctx:CMLangParser.FunctionContext):
        pass


    # Enter a parse tree produced by CMLangParser#predicate.
    def enterPredicate(self, ctx:CMLangParser.PredicateContext):
        pass

    # Exit a parse tree produced by CMLangParser#predicate.
    def exitPredicate(self, ctx:CMLangParser.PredicateContext):
        pass


    # Enter a parse tree produced by CMLangParser#logic.
    def enterLogic(self, ctx:CMLangParser.LogicContext):
        pass

    # Exit a parse tree produced by CMLangParser#logic.
    def exitLogic(self, ctx:CMLangParser.LogicContext):
        pass


    # Enter a parse tree produced by CMLangParser#add_sub.
    def enterAdd_sub(self, ctx:CMLangParser.Add_subContext):
        pass

    # Exit a parse tree produced by CMLangParser#add_sub.
    def exitAdd_sub(self, ctx:CMLangParser.Add_subContext):
        pass


    # Enter a parse tree produced by CMLangParser#mul_div.
    def enterMul_div(self, ctx:CMLangParser.Mul_divContext):
        pass

    # Exit a parse tree produced by CMLangParser#mul_div.
    def exitMul_div(self, ctx:CMLangParser.Mul_divContext):
        pass


    # Enter a parse tree produced by CMLangParser#expr.
    def enterExpr(self, ctx:CMLangParser.ExprContext):
        pass

    # Exit a parse tree produced by CMLangParser#expr.
    def exitExpr(self, ctx:CMLangParser.ExprContext):
        pass


    # Enter a parse tree produced by CMLangParser#logical_expr.
    def enterLogical_expr(self, ctx:CMLangParser.Logical_exprContext):
        pass

    # Exit a parse tree produced by CMLangParser#logical_expr.
    def exitLogical_expr(self, ctx:CMLangParser.Logical_exprContext):
        pass


    # Enter a parse tree produced by CMLangParser#add_sub_expr.
    def enterAdd_sub_expr(self, ctx:CMLangParser.Add_sub_exprContext):
        pass

    # Exit a parse tree produced by CMLangParser#add_sub_expr.
    def exitAdd_sub_expr(self, ctx:CMLangParser.Add_sub_exprContext):
        pass


    # Enter a parse tree produced by CMLangParser#factor.
    def enterFactor(self, ctx:CMLangParser.FactorContext):
        pass

    # Exit a parse tree produced by CMLangParser#factor.
    def exitFactor(self, ctx:CMLangParser.FactorContext):
        pass


    # Enter a parse tree produced by CMLangParser#signed_value.
    def enterSigned_value(self, ctx:CMLangParser.Signed_valueContext):
        pass

    # Exit a parse tree produced by CMLangParser#signed_value.
    def exitSigned_value(self, ctx:CMLangParser.Signed_valueContext):
        pass


    # Enter a parse tree produced by CMLangParser#atom.
    def enterAtom(self, ctx:CMLangParser.AtomContext):
        pass

    # Exit a parse tree produced by CMLangParser#atom.
    def exitAtom(self, ctx:CMLangParser.AtomContext):
        pass


    # Enter a parse tree produced by CMLangParser#function_args.
    def enterFunction_args(self, ctx:CMLangParser.Function_argsContext):
        pass

    # Exit a parse tree produced by CMLangParser#function_args.
    def exitFunction_args(self, ctx:CMLangParser.Function_argsContext):
        pass


    # Enter a parse tree produced by CMLangParser#cond_loop.
    def enterCond_loop(self, ctx:CMLangParser.Cond_loopContext):
        pass

    # Exit a parse tree produced by CMLangParser#cond_loop.
    def exitCond_loop(self, ctx:CMLangParser.Cond_loopContext):
        pass


    # Enter a parse tree produced by CMLangParser#iter_expression.
    def enterIter_expression(self, ctx:CMLangParser.Iter_expressionContext):
        pass

    # Exit a parse tree produced by CMLangParser#iter_expression.
    def exitIter_expression(self, ctx:CMLangParser.Iter_expressionContext):
        pass


