// Generated from /Users/seankinzer/ACTLab/cmlang/cmlang.code/compiler/CMLangv2/CMLangv2.g4 by ANTLR 4.7
import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link CMLangv2Parser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
public interface CMLangv2Visitor<T> extends ParseTreeVisitor<T> {
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#cmlang}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCmlang(CMLangv2Parser.CmlangContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#component_list}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitComponent_list(CMLangv2Parser.Component_listContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#component_definition}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitComponent_definition(CMLangv2Parser.Component_definitionContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#flow_list}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFlow_list(CMLangv2Parser.Flow_listContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#flow}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFlow(CMLangv2Parser.FlowContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#flow_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFlow_expression(CMLangv2Parser.Flow_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#flow_declaration_list}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFlow_declaration_list(CMLangv2Parser.Flow_declaration_listContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#index_declaration_list}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitIndex_declaration_list(CMLangv2Parser.Index_declaration_listContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#index_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitIndex_declaration(CMLangv2Parser.Index_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#prefix_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPrefix_expression(CMLangv2Parser.Prefix_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#array_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArray_expression(CMLangv2Parser.Array_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#group_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGroup_expression(CMLangv2Parser.Group_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#function_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFunction_expression(CMLangv2Parser.Function_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#nested_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNested_expression(CMLangv2Parser.Nested_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#index_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitIndex_expression(CMLangv2Parser.Index_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#index_expression_list}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitIndex_expression_list(CMLangv2Parser.Index_expression_listContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#expression_list}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitExpression_list(CMLangv2Parser.Expression_listContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitExpression(CMLangv2Parser.ExpressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#unary_op}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnary_op(CMLangv2Parser.Unary_opContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#multiplicative_op}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMultiplicative_op(CMLangv2Parser.Multiplicative_opContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#additive_op}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAdditive_op(CMLangv2Parser.Additive_opContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#relational_op}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRelational_op(CMLangv2Parser.Relational_opContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#assignment_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAssignment_expression(CMLangv2Parser.Assignment_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitStatement(CMLangv2Parser.StatementContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#statement_list}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitStatement_list(CMLangv2Parser.Statement_listContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#expression_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitExpression_statement(CMLangv2Parser.Expression_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#declaration_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDeclaration_statement(CMLangv2Parser.Declaration_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#assignment_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAssignment_statement(CMLangv2Parser.Assignment_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#predicate_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPredicate_expression(CMLangv2Parser.Predicate_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#iteration_statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitIteration_statement(CMLangv2Parser.Iteration_statementContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#func_ident_list}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFunc_ident_list(CMLangv2Parser.Func_ident_listContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#component_type}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitComponent_type(CMLangv2Parser.Component_typeContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#flow_type}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFlow_type(CMLangv2Parser.Flow_typeContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#dtype_specifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDtype_specifier(CMLangv2Parser.Dtype_specifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#integer}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInteger(CMLangv2Parser.IntegerContext ctx);
	/**
	 * Visit a parse tree produced by {@link CMLangv2Parser#number}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNumber(CMLangv2Parser.NumberContext ctx);
}