grammar CMLang;

/* scanner tokens */
INPUT : 'input';
OUTPUT : 'output';
STATE: 'state';
FLOW: 'flow';
PARAMETER: 'parameter';

SPRING : 'spring';
RESERVOIR: 'reservoir';
COMPONENT: 'component';


FOR: 'for';
WHILE: 'while';

INDEX : 'index';
NOT : '!';
NOTEQ : '!=';
ADD : '+';
SUB : '-';
DIV : '/';
LT : '<';
LEQ : '<=';
EQUAL : '==';
GT : '>';
GEQ : '>=';
MUL : '*';
POW : '^';
// Built-in functions
FILE_READ : 'fread';
FILE_WRITE : 'fwrite';
FLOAT_FUNC : 'float';
BINARY_FUNC : 'bin';
INT_FUNC : 'int';
MAX : 'max';
ARGMAX : 'argmax';
MIN : 'min';
ARGMIN : 'argmin';
E : 'e';
PI : 'pi';
SUM : 'sum';
NORM : 'norm';
GAUSSIAN : 'gaussian';
SIGMOID : 'sigmoid';
CEILING : 'ceiling';
SIG_SYM : 'sigmoid_symmetric';
LOG : 'log';
LOG2 : 'log2';
RANDOM : 'random';
SEMI : ';';
COLON: ':';
LEFT_BRACK : '[';
RIGHT_BRACK : ']';
RIGHT_CURLY : '}';
LEFT_CURLY : '{';
LEFT_PAREN : '(';
RIGHT_PAREN : ')';
COMMA : ',';
ASSIGN : '=';


/* var name */
ID
    : (LOWER | UPPER) (LOWER | UPPER | DIGIT | '_')* ('\'')?
    ;

fragment LOWER: 'a'..'z';
fragment UPPER: 'A'..'Z';
fragment DIGIT
 : '0'..'9'
 ;
fragment NON_ZERO_DIGIT
 : '1'..'9'
 ;
 fragment OCT_DIGIT
 : '0'..'7'
 ;
 fragment HEX_DIGIT
 : DIGIT
 | 'a'..'f'
 | 'A'..'F'
 ;
 fragment BIN_DIGIT
 : '0'
 | '1'
 ;
 fragment POINT_FLOAT
 : INT_PART? FRACTION
 | INT_PART '.'
 ;
 fragment INT_PART
 : DIGIT+
 ;
fragment FRACTION
 : '.' DIGIT+
 ;
 fragment EXPONENT
 : ('e'|'E') ('+'|'-')? DIGIT+
 ;
 fragment EXPONENT_FLOAT
 : ( INT_PART | POINT_FLOAT ) EXPONENT
 ;
 fragment SHORT_STRING
 : '\'' ( STRING_ESCAPE_SEQ | ~[\\\r\n\f'] )* '\''
 | '"' ( STRING_ESCAPE_SEQ | ~[\\\r\n\f"] )* '"'
 ;
fragment LONG_STRING
 : '\'\'\'' LONG_STRING_ITEM*? '\'\'\''
 | '"""' LONG_STRING_ITEM*? '"""'
 ;
 fragment LONG_STRING_ITEM
 : LONG_STRING_CHAR
 | STRING_ESCAPE_SEQ
 ;
fragment LONG_STRING_CHAR
 : ~'\\'
 ;
 fragment STRING_ESCAPE_SEQ
 : '\\' .
 | '\\'
 ;
WHITESPACE
    : (' ' | '\t' | '\n' | '\r')+ -> skip
    ;

COMMENT
    : '//' .+? ('\n' | EOF) -> skip
    ;
STRING
    :(SHORT_STRING | LONG_STRING)
    ;
DECIMAL_INTEGER
 : NON_ZERO_DIGIT DIGIT*
 | '0'+
 ;
 OCT_INTEGER
 : '0' ('o'|'O') OCT_DIGIT+
 ;
 HEX_INTEGER
 : '0' ('x'|'X') HEX_DIGIT+
 ;
BIN_INTEGER
 : '0' ('b'|'B') BIN_DIGIT+
 ;
 FLOAT_NUMBER
 : POINT_FLOAT
 | EXPONENT_FLOAT
 ;
 IMAG_NUMBER
 : ( FLOAT_NUMBER | INT_PART ) ('i'|'I')
 ;

number
 : integer
 | FLOAT_NUMBER
 | IMAG_NUMBER
 ;

integer
 : DECIMAL_INTEGER
 | OCT_INTEGER
 | HEX_INTEGER
 | BIN_INTEGER
 ;
 val_type
    : 'float'
    | 'int'
    | 'complex'
    | 'string'
    | 'bool'
    | 'complex'
    ;

/* LL(1) parser rules */
program 
    : component_list EOF
    ;

component_list
    : component_definition+
    ;

component_definition
    : component_type ID component_parameters component_body
    ;

component_parameters
    : LEFT_PAREN (arg_list)? RIGHT_PAREN
    ;

arg_list
   : arg (',' arg)*
   ;

default_param_value
    : STRING
    | number
    ;

flow_def_index
    : ID
    ;
arg
   : arg_type val_type ID parameter_arg_def
   | arg_type val_type ID (LEFT_BRACK (flow_def_index) RIGHT_BRACK)+
   ;

parameter_arg_def
    : '=' default_param_value
    | // epsilon
    ;

arg_type
    : INPUT
    | OUTPUT
    | STATE
    | PARAMETER
    ;

component_type
    : COMPONENT
    | RESERVOIR
    | SPRING
    ;


component_body
    : LEFT_CURLY statement_list RIGHT_CURLY
    ;

statement_list
    : statement+
    ;


statement
    : primitive
    | component_inst
    | cond_loop
    ;
primitive
    : data_decl SEMI
    | var ASSIGN (expr | predicate) SEMI
    | file_operation SEMI
    ;

data_decl 
    : flow_declaration_list
    | index_declaration_list
    ;
flow_declaration_list
    : flow_declaration
    | flow_declaration COMMA flow_declaration
    ;
index_declaration_list
    : index_declaration
    | index_declaration COMMA flow_declaration
    ;

flow_declaration
    : FLOW val_type var_list_flow
    ;
index_declaration
    :  index var_list_index
    ;
power
    : POW
    ;

index
    : INDEX
    ;

flow
    : ID LEFT_BRACK (flow_index) RIGHT_BRACK id_tail
    ;
var_list_flow
    : flow var_list_flow_tail
    ;
var_list_flow_tail
    : COMMA var_list_flow
    | // epsilon
    ;

var_list
    : var var_list_tail
    ;

var 
    : var_id
    ;

var_id 
    : ID id_tail
    ;

id_tail 
    : LEFT_BRACK (flow_index) RIGHT_BRACK id_tail
	| // epsilon
    ;
flow_index
    : expr
    ;

var_list_tail
    : COMMA var_list
    | // epsilon
    ;

var_list_index
    : ID LEFT_BRACK expr COLON expr RIGHT_BRACK
    ;

component_inst
    : ID LEFT_PAREN comp_param_list? RIGHT_PAREN SEMI
    ;

call_param_id
    : ID
    | number
    | STRING
    ;
comp_param_id
    : ID
    | number
    | STRING
    ;
comp_param_list
    : comp_param_id comp_param_list_tail
    ;

comp_param_list_tail
    : COMMA comp_param_list
    | //epsilon
    ;
call_param_list
    : call_param_id call_param_list_tail
    ;

call_param_list_tail
    : COMMA call_param_list
    | //epsilon
    ;

file_function
    : FILE_READ
    | FILE_WRITE
    ;
file_operation
    : file_function LEFT_PAREN call_param_list? RIGHT_PAREN
    ;

function
    : PI
	| SUM
    | NORM
	| GAUSSIAN
	| SIGMOID
	| SIG_SYM
	| LOG
	| LOG2
	| CEILING
	| E
	| FLOAT_FUNC
	| BINARY_FUNC
	| INT_FUNC
	| RANDOM
	| MAX
	| ARGMAX
	| ARGMIN
    ;

predicate
    : expr '?' expr COLON expr
    ;

logic
    : GEQ
    | GT
    | EQUAL
    | LT
    | LEQ
    ;
add_sub
    : ADD
    | SUB
    ;
mul_div
    : MUL
    | DIV
    ;


expr
   : logical_expr ((logic) logical_expr)*
   ;
logical_expr
    : add_sub_expr ((add_sub) add_sub_expr)*
    ;
add_sub_expr
   : factor ((mul_div) factor)*
   ;

factor
   : signed_value ((power) signed_value)*
   ;

signed_value
   : add_sub signed_value
   | atom
   ;

atom
    :	number //numbers
    |	var  //variables
    |   file_operation
    |   function function_args
    |	LEFT_PAREN expr RIGHT_PAREN
    ;

function_args
    : (LEFT_BRACK ID RIGHT_BRACK)+ LEFT_PAREN expr RIGHT_PAREN
    | LEFT_PAREN expr RIGHT_PAREN
    | LEFT_PAREN RIGHT_PAREN
    ;



cond_loop
    : WHILE LEFT_PAREN index_expression RIGHT_PAREN component_body
    | FOR LEFT_PAREN index_expression? SEMI index_expression? SEMI index_expression? RIGHT_PAREN component_body
    ;

index_expression
    : var ASSIGN expr
    | expr
    | ID ASSIGN number
    ;