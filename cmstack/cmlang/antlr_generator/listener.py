# Generated from /home/kinzers/projects/cmstack.code/cmstack/cmlang/antlr_generator/CMLang.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CMLangParser import CMLangParser
else:
    from CMLangParser import CMLangParser

# This class defines a complete listener for a parse tree produced by CMLangParser.
class CMLangListener(ParseTreeListener):

    # Enter a parse tree produced by CMLangParser#cmlang.
    def enterCmlang(self, ctx:CMLangParser.CmlangContext):
        pass

    # Exit a parse tree produced by CMLangParser#cmlang.
    def exitCmlang(self, ctx:CMLangParser.CmlangContext):
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


    # Enter a parse tree produced by CMLangParser#flow_list.
    def enterFlow_list(self, ctx:CMLangParser.Flow_listContext):
        pass

    # Exit a parse tree produced by CMLangParser#flow_list.
    def exitFlow_list(self, ctx:CMLangParser.Flow_listContext):
        pass


    # Enter a parse tree produced by CMLangParser#flow.
    def enterFlow(self, ctx:CMLangParser.FlowContext):
        pass

    # Exit a parse tree produced by CMLangParser#flow.
    def exitFlow(self, ctx:CMLangParser.FlowContext):
        pass


    # Enter a parse tree produced by CMLangParser#flow_expression.
    def enterFlow_expression(self, ctx:CMLangParser.Flow_expressionContext):
        pass

    # Exit a parse tree produced by CMLangParser#flow_expression.
    def exitFlow_expression(self, ctx:CMLangParser.Flow_expressionContext):
        pass


    # Enter a parse tree produced by CMLangParser#literal.
    def enterLiteral(self, ctx:CMLangParser.LiteralContext):
        pass

    # Exit a parse tree produced by CMLangParser#literal.
    def exitLiteral(self, ctx:CMLangParser.LiteralContext):
        pass


    # Enter a parse tree produced by CMLangParser#flow_index_list.
    def enterFlow_index_list(self, ctx:CMLangParser.Flow_index_listContext):
        pass

    # Exit a parse tree produced by CMLangParser#flow_index_list.
    def exitFlow_index_list(self, ctx:CMLangParser.Flow_index_listContext):
        pass


    # Enter a parse tree produced by CMLangParser#flow_index.
    def enterFlow_index(self, ctx:CMLangParser.Flow_indexContext):
        pass

    # Exit a parse tree produced by CMLangParser#flow_index.
    def exitFlow_index(self, ctx:CMLangParser.Flow_indexContext):
        pass


    # Enter a parse tree produced by CMLangParser#flow_declaration_list.
    def enterFlow_declaration_list(self, ctx:CMLangParser.Flow_declaration_listContext):
        pass

    # Exit a parse tree produced by CMLangParser#flow_declaration_list.
    def exitFlow_declaration_list(self, ctx:CMLangParser.Flow_declaration_listContext):
        pass


    # Enter a parse tree produced by CMLangParser#flow_declaration.
    def enterFlow_declaration(self, ctx:CMLangParser.Flow_declarationContext):
        pass

    # Exit a parse tree produced by CMLangParser#flow_declaration.
    def exitFlow_declaration(self, ctx:CMLangParser.Flow_declarationContext):
        pass


    # Enter a parse tree produced by CMLangParser#index_declaration_list.
    def enterIndex_declaration_list(self, ctx:CMLangParser.Index_declaration_listContext):
        pass

    # Exit a parse tree produced by CMLangParser#index_declaration_list.
    def exitIndex_declaration_list(self, ctx:CMLangParser.Index_declaration_listContext):
        pass


    # Enter a parse tree produced by CMLangParser#index_declaration.
    def enterIndex_declaration(self, ctx:CMLangParser.Index_declarationContext):
        pass

    # Exit a parse tree produced by CMLangParser#index_declaration.
    def exitIndex_declaration(self, ctx:CMLangParser.Index_declarationContext):
        pass


    # Enter a parse tree produced by CMLangParser#prefix_expression.
    def enterPrefix_expression(self, ctx:CMLangParser.Prefix_expressionContext):
        pass

    # Exit a parse tree produced by CMLangParser#prefix_expression.
    def exitPrefix_expression(self, ctx:CMLangParser.Prefix_expressionContext):
        pass


    # Enter a parse tree produced by CMLangParser#array_expression.
    def enterArray_expression(self, ctx:CMLangParser.Array_expressionContext):
        pass

    # Exit a parse tree produced by CMLangParser#array_expression.
    def exitArray_expression(self, ctx:CMLangParser.Array_expressionContext):
        pass


    # Enter a parse tree produced by CMLangParser#group_expression.
    def enterGroup_expression(self, ctx:CMLangParser.Group_expressionContext):
        pass

    # Exit a parse tree produced by CMLangParser#group_expression.
    def exitGroup_expression(self, ctx:CMLangParser.Group_expressionContext):
        pass


    # Enter a parse tree produced by CMLangParser#function_expression.
    def enterFunction_expression(self, ctx:CMLangParser.Function_expressionContext):
        pass

    # Exit a parse tree produced by CMLangParser#function_expression.
    def exitFunction_expression(self, ctx:CMLangParser.Function_expressionContext):
        pass


    # Enter a parse tree produced by CMLangParser#function_id.
    def enterFunction_id(self, ctx:CMLangParser.Function_idContext):
        pass

    # Exit a parse tree produced by CMLangParser#function_id.
    def exitFunction_id(self, ctx:CMLangParser.Function_idContext):
        pass


    # Enter a parse tree produced by CMLangParser#nested_expression.
    def enterNested_expression(self, ctx:CMLangParser.Nested_expressionContext):
        pass

    # Exit a parse tree produced by CMLangParser#nested_expression.
    def exitNested_expression(self, ctx:CMLangParser.Nested_expressionContext):
        pass


    # Enter a parse tree produced by CMLangParser#index_expression.
    def enterIndex_expression(self, ctx:CMLangParser.Index_expressionContext):
        pass

    # Exit a parse tree produced by CMLangParser#index_expression.
    def exitIndex_expression(self, ctx:CMLangParser.Index_expressionContext):
        pass


    # Enter a parse tree produced by CMLangParser#index_expression_list.
    def enterIndex_expression_list(self, ctx:CMLangParser.Index_expression_listContext):
        pass

    # Exit a parse tree produced by CMLangParser#index_expression_list.
    def exitIndex_expression_list(self, ctx:CMLangParser.Index_expression_listContext):
        pass


    # Enter a parse tree produced by CMLangParser#expression_list.
    def enterExpression_list(self, ctx:CMLangParser.Expression_listContext):
        pass

    # Exit a parse tree produced by CMLangParser#expression_list.
    def exitExpression_list(self, ctx:CMLangParser.Expression_listContext):
        pass


    # Enter a parse tree produced by CMLangParser#expression.
    def enterExpression(self, ctx:CMLangParser.ExpressionContext):
        pass

    # Exit a parse tree produced by CMLangParser#expression.
    def exitExpression(self, ctx:CMLangParser.ExpressionContext):
        pass


    # Enter a parse tree produced by CMLangParser#unary_op.
    def enterUnary_op(self, ctx:CMLangParser.Unary_opContext):
        pass

    # Exit a parse tree produced by CMLangParser#unary_op.
    def exitUnary_op(self, ctx:CMLangParser.Unary_opContext):
        pass


    # Enter a parse tree produced by CMLangParser#multiplicative_op.
    def enterMultiplicative_op(self, ctx:CMLangParser.Multiplicative_opContext):
        pass

    # Exit a parse tree produced by CMLangParser#multiplicative_op.
    def exitMultiplicative_op(self, ctx:CMLangParser.Multiplicative_opContext):
        pass


    # Enter a parse tree produced by CMLangParser#additive_op.
    def enterAdditive_op(self, ctx:CMLangParser.Additive_opContext):
        pass

    # Exit a parse tree produced by CMLangParser#additive_op.
    def exitAdditive_op(self, ctx:CMLangParser.Additive_opContext):
        pass


    # Enter a parse tree produced by CMLangParser#relational_op.
    def enterRelational_op(self, ctx:CMLangParser.Relational_opContext):
        pass

    # Exit a parse tree produced by CMLangParser#relational_op.
    def exitRelational_op(self, ctx:CMLangParser.Relational_opContext):
        pass


    # Enter a parse tree produced by CMLangParser#assignment_expression.
    def enterAssignment_expression(self, ctx:CMLangParser.Assignment_expressionContext):
        pass

    # Exit a parse tree produced by CMLangParser#assignment_expression.
    def exitAssignment_expression(self, ctx:CMLangParser.Assignment_expressionContext):
        pass


    # Enter a parse tree produced by CMLangParser#statement.
    def enterStatement(self, ctx:CMLangParser.StatementContext):
        pass

    # Exit a parse tree produced by CMLangParser#statement.
    def exitStatement(self, ctx:CMLangParser.StatementContext):
        pass


    # Enter a parse tree produced by CMLangParser#statement_list.
    def enterStatement_list(self, ctx:CMLangParser.Statement_listContext):
        pass

    # Exit a parse tree produced by CMLangParser#statement_list.
    def exitStatement_list(self, ctx:CMLangParser.Statement_listContext):
        pass


    # Enter a parse tree produced by CMLangParser#expression_statement.
    def enterExpression_statement(self, ctx:CMLangParser.Expression_statementContext):
        pass

    # Exit a parse tree produced by CMLangParser#expression_statement.
    def exitExpression_statement(self, ctx:CMLangParser.Expression_statementContext):
        pass


    # Enter a parse tree produced by CMLangParser#declaration_statement.
    def enterDeclaration_statement(self, ctx:CMLangParser.Declaration_statementContext):
        pass

    # Exit a parse tree produced by CMLangParser#declaration_statement.
    def exitDeclaration_statement(self, ctx:CMLangParser.Declaration_statementContext):
        pass


    # Enter a parse tree produced by CMLangParser#assignment_statement.
    def enterAssignment_statement(self, ctx:CMLangParser.Assignment_statementContext):
        pass

    # Exit a parse tree produced by CMLangParser#assignment_statement.
    def exitAssignment_statement(self, ctx:CMLangParser.Assignment_statementContext):
        pass


    # Enter a parse tree produced by CMLangParser#predicate_expression.
    def enterPredicate_expression(self, ctx:CMLangParser.Predicate_expressionContext):
        pass

    # Exit a parse tree produced by CMLangParser#predicate_expression.
    def exitPredicate_expression(self, ctx:CMLangParser.Predicate_expressionContext):
        pass


    # Enter a parse tree produced by CMLangParser#bool_expression.
    def enterBool_expression(self, ctx:CMLangParser.Bool_expressionContext):
        pass

    # Exit a parse tree produced by CMLangParser#bool_expression.
    def exitBool_expression(self, ctx:CMLangParser.Bool_expressionContext):
        pass


    # Enter a parse tree produced by CMLangParser#true_expression.
    def enterTrue_expression(self, ctx:CMLangParser.True_expressionContext):
        pass

    # Exit a parse tree produced by CMLangParser#true_expression.
    def exitTrue_expression(self, ctx:CMLangParser.True_expressionContext):
        pass


    # Enter a parse tree produced by CMLangParser#false_expression.
    def enterFalse_expression(self, ctx:CMLangParser.False_expressionContext):
        pass

    # Exit a parse tree produced by CMLangParser#false_expression.
    def exitFalse_expression(self, ctx:CMLangParser.False_expressionContext):
        pass


    # Enter a parse tree produced by CMLangParser#iteration_statement.
    def enterIteration_statement(self, ctx:CMLangParser.Iteration_statementContext):
        pass

    # Exit a parse tree produced by CMLangParser#iteration_statement.
    def exitIteration_statement(self, ctx:CMLangParser.Iteration_statementContext):
        pass


    # Enter a parse tree produced by CMLangParser#component_type.
    def enterComponent_type(self, ctx:CMLangParser.Component_typeContext):
        pass

    # Exit a parse tree produced by CMLangParser#component_type.
    def exitComponent_type(self, ctx:CMLangParser.Component_typeContext):
        pass


    # Enter a parse tree produced by CMLangParser#flow_type.
    def enterFlow_type(self, ctx:CMLangParser.Flow_typeContext):
        pass

    # Exit a parse tree produced by CMLangParser#flow_type.
    def exitFlow_type(self, ctx:CMLangParser.Flow_typeContext):
        pass


    # Enter a parse tree produced by CMLangParser#dtype_specifier.
    def enterDtype_specifier(self, ctx:CMLangParser.Dtype_specifierContext):
        pass

    # Exit a parse tree produced by CMLangParser#dtype_specifier.
    def exitDtype_specifier(self, ctx:CMLangParser.Dtype_specifierContext):
        pass


    # Enter a parse tree produced by CMLangParser#integer.
    def enterInteger(self, ctx:CMLangParser.IntegerContext):
        pass

    # Exit a parse tree produced by CMLangParser#integer.
    def exitInteger(self, ctx:CMLangParser.IntegerContext):
        pass


    # Enter a parse tree produced by CMLangParser#number.
    def enterNumber(self, ctx:CMLangParser.NumberContext):
        pass

    # Exit a parse tree produced by CMLangParser#number.
    def exitNumber(self, ctx:CMLangParser.NumberContext):
        pass


    # Enter a parse tree produced by CMLangParser#complex_number.
    def enterComplex_number(self, ctx:CMLangParser.Complex_numberContext):
        pass

    # Exit a parse tree produced by CMLangParser#complex_number.
    def exitComplex_number(self, ctx:CMLangParser.Complex_numberContext):
        pass


