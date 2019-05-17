// Generated from /Users/seankinzer/ACTLab/cmlang/cmlang.code/compiler/CMLangv2/CMLangv2.g4 by ANTLR 4.7
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link CMLangv2Parser}.
 */
public interface CMLangv2Listener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#cmlang}.
	 * @param ctx the parse tree
	 */
	void enterCmlang(CMLangv2Parser.CmlangContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#cmlang}.
	 * @param ctx the parse tree
	 */
	void exitCmlang(CMLangv2Parser.CmlangContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#component_list}.
	 * @param ctx the parse tree
	 */
	void enterComponent_list(CMLangv2Parser.Component_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#component_list}.
	 * @param ctx the parse tree
	 */
	void exitComponent_list(CMLangv2Parser.Component_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#component_definition}.
	 * @param ctx the parse tree
	 */
	void enterComponent_definition(CMLangv2Parser.Component_definitionContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#component_definition}.
	 * @param ctx the parse tree
	 */
	void exitComponent_definition(CMLangv2Parser.Component_definitionContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#flow_list}.
	 * @param ctx the parse tree
	 */
	void enterFlow_list(CMLangv2Parser.Flow_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#flow_list}.
	 * @param ctx the parse tree
	 */
	void exitFlow_list(CMLangv2Parser.Flow_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#flow}.
	 * @param ctx the parse tree
	 */
	void enterFlow(CMLangv2Parser.FlowContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#flow}.
	 * @param ctx the parse tree
	 */
	void exitFlow(CMLangv2Parser.FlowContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#flow_expression}.
	 * @param ctx the parse tree
	 */
	void enterFlow_expression(CMLangv2Parser.Flow_expressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#flow_expression}.
	 * @param ctx the parse tree
	 */
	void exitFlow_expression(CMLangv2Parser.Flow_expressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#flow_declaration_list}.
	 * @param ctx the parse tree
	 */
	void enterFlow_declaration_list(CMLangv2Parser.Flow_declaration_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#flow_declaration_list}.
	 * @param ctx the parse tree
	 */
	void exitFlow_declaration_list(CMLangv2Parser.Flow_declaration_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#index_declaration_list}.
	 * @param ctx the parse tree
	 */
	void enterIndex_declaration_list(CMLangv2Parser.Index_declaration_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#index_declaration_list}.
	 * @param ctx the parse tree
	 */
	void exitIndex_declaration_list(CMLangv2Parser.Index_declaration_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#index_declaration}.
	 * @param ctx the parse tree
	 */
	void enterIndex_declaration(CMLangv2Parser.Index_declarationContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#index_declaration}.
	 * @param ctx the parse tree
	 */
	void exitIndex_declaration(CMLangv2Parser.Index_declarationContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#prefix_expression}.
	 * @param ctx the parse tree
	 */
	void enterPrefix_expression(CMLangv2Parser.Prefix_expressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#prefix_expression}.
	 * @param ctx the parse tree
	 */
	void exitPrefix_expression(CMLangv2Parser.Prefix_expressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#array_expression}.
	 * @param ctx the parse tree
	 */
	void enterArray_expression(CMLangv2Parser.Array_expressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#array_expression}.
	 * @param ctx the parse tree
	 */
	void exitArray_expression(CMLangv2Parser.Array_expressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#group_expression}.
	 * @param ctx the parse tree
	 */
	void enterGroup_expression(CMLangv2Parser.Group_expressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#group_expression}.
	 * @param ctx the parse tree
	 */
	void exitGroup_expression(CMLangv2Parser.Group_expressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#function_expression}.
	 * @param ctx the parse tree
	 */
	void enterFunction_expression(CMLangv2Parser.Function_expressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#function_expression}.
	 * @param ctx the parse tree
	 */
	void exitFunction_expression(CMLangv2Parser.Function_expressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#nested_expression}.
	 * @param ctx the parse tree
	 */
	void enterNested_expression(CMLangv2Parser.Nested_expressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#nested_expression}.
	 * @param ctx the parse tree
	 */
	void exitNested_expression(CMLangv2Parser.Nested_expressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#index_expression}.
	 * @param ctx the parse tree
	 */
	void enterIndex_expression(CMLangv2Parser.Index_expressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#index_expression}.
	 * @param ctx the parse tree
	 */
	void exitIndex_expression(CMLangv2Parser.Index_expressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#index_expression_list}.
	 * @param ctx the parse tree
	 */
	void enterIndex_expression_list(CMLangv2Parser.Index_expression_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#index_expression_list}.
	 * @param ctx the parse tree
	 */
	void exitIndex_expression_list(CMLangv2Parser.Index_expression_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#expression_list}.
	 * @param ctx the parse tree
	 */
	void enterExpression_list(CMLangv2Parser.Expression_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#expression_list}.
	 * @param ctx the parse tree
	 */
	void exitExpression_list(CMLangv2Parser.Expression_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#expression}.
	 * @param ctx the parse tree
	 */
	void enterExpression(CMLangv2Parser.ExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#expression}.
	 * @param ctx the parse tree
	 */
	void exitExpression(CMLangv2Parser.ExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#unary_op}.
	 * @param ctx the parse tree
	 */
	void enterUnary_op(CMLangv2Parser.Unary_opContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#unary_op}.
	 * @param ctx the parse tree
	 */
	void exitUnary_op(CMLangv2Parser.Unary_opContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#multiplicative_op}.
	 * @param ctx the parse tree
	 */
	void enterMultiplicative_op(CMLangv2Parser.Multiplicative_opContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#multiplicative_op}.
	 * @param ctx the parse tree
	 */
	void exitMultiplicative_op(CMLangv2Parser.Multiplicative_opContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#additive_op}.
	 * @param ctx the parse tree
	 */
	void enterAdditive_op(CMLangv2Parser.Additive_opContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#additive_op}.
	 * @param ctx the parse tree
	 */
	void exitAdditive_op(CMLangv2Parser.Additive_opContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#relational_op}.
	 * @param ctx the parse tree
	 */
	void enterRelational_op(CMLangv2Parser.Relational_opContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#relational_op}.
	 * @param ctx the parse tree
	 */
	void exitRelational_op(CMLangv2Parser.Relational_opContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#assignment_expression}.
	 * @param ctx the parse tree
	 */
	void enterAssignment_expression(CMLangv2Parser.Assignment_expressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#assignment_expression}.
	 * @param ctx the parse tree
	 */
	void exitAssignment_expression(CMLangv2Parser.Assignment_expressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#statement}.
	 * @param ctx the parse tree
	 */
	void enterStatement(CMLangv2Parser.StatementContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#statement}.
	 * @param ctx the parse tree
	 */
	void exitStatement(CMLangv2Parser.StatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#statement_list}.
	 * @param ctx the parse tree
	 */
	void enterStatement_list(CMLangv2Parser.Statement_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#statement_list}.
	 * @param ctx the parse tree
	 */
	void exitStatement_list(CMLangv2Parser.Statement_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#expression_statement}.
	 * @param ctx the parse tree
	 */
	void enterExpression_statement(CMLangv2Parser.Expression_statementContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#expression_statement}.
	 * @param ctx the parse tree
	 */
	void exitExpression_statement(CMLangv2Parser.Expression_statementContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#declaration_statement}.
	 * @param ctx the parse tree
	 */
	void enterDeclaration_statement(CMLangv2Parser.Declaration_statementContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#declaration_statement}.
	 * @param ctx the parse tree
	 */
	void exitDeclaration_statement(CMLangv2Parser.Declaration_statementContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssignment_statement(CMLangv2Parser.Assignment_statementContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssignment_statement(CMLangv2Parser.Assignment_statementContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#predicate_expression}.
	 * @param ctx the parse tree
	 */
	void enterPredicate_expression(CMLangv2Parser.Predicate_expressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#predicate_expression}.
	 * @param ctx the parse tree
	 */
	void exitPredicate_expression(CMLangv2Parser.Predicate_expressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#iteration_statement}.
	 * @param ctx the parse tree
	 */
	void enterIteration_statement(CMLangv2Parser.Iteration_statementContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#iteration_statement}.
	 * @param ctx the parse tree
	 */
	void exitIteration_statement(CMLangv2Parser.Iteration_statementContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#func_ident_list}.
	 * @param ctx the parse tree
	 */
	void enterFunc_ident_list(CMLangv2Parser.Func_ident_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#func_ident_list}.
	 * @param ctx the parse tree
	 */
	void exitFunc_ident_list(CMLangv2Parser.Func_ident_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#component_type}.
	 * @param ctx the parse tree
	 */
	void enterComponent_type(CMLangv2Parser.Component_typeContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#component_type}.
	 * @param ctx the parse tree
	 */
	void exitComponent_type(CMLangv2Parser.Component_typeContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#flow_type}.
	 * @param ctx the parse tree
	 */
	void enterFlow_type(CMLangv2Parser.Flow_typeContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#flow_type}.
	 * @param ctx the parse tree
	 */
	void exitFlow_type(CMLangv2Parser.Flow_typeContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#dtype_specifier}.
	 * @param ctx the parse tree
	 */
	void enterDtype_specifier(CMLangv2Parser.Dtype_specifierContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#dtype_specifier}.
	 * @param ctx the parse tree
	 */
	void exitDtype_specifier(CMLangv2Parser.Dtype_specifierContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#integer}.
	 * @param ctx the parse tree
	 */
	void enterInteger(CMLangv2Parser.IntegerContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#integer}.
	 * @param ctx the parse tree
	 */
	void exitInteger(CMLangv2Parser.IntegerContext ctx);
	/**
	 * Enter a parse tree produced by {@link CMLangv2Parser#number}.
	 * @param ctx the parse tree
	 */
	void enterNumber(CMLangv2Parser.NumberContext ctx);
	/**
	 * Exit a parse tree produced by {@link CMLangv2Parser#number}.
	 * @param ctx the parse tree
	 */
	void exitNumber(CMLangv2Parser.NumberContext ctx);
}