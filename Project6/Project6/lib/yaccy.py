#Name: Sean Joseph
#This is where my production rules are housed!
from .tracker import Tracker
from .variable import *
from .symbols import SymbolTable
from .node import *

precedence = (
            ('right','=' ,'ASSIGN_ADD' ,'ASSIGN_SUB' ,
                'ASSIGN_MULT' ,'ASSIGN_DIV'),
            ('left','BOOL_OR'),
            ('left','BOOL_AND'),
            ('nonassoc','COMP_EQU','COMP_NEQU','COMP_LESS',
                'COMP_LTE','COMP_GTR','COMP_GTE'),
            ('left','+', '-'),
            ('left','*','/'),
            ('nonassoc','UNARY_MINUS'),
            ('nonassoc','UNARY_NOT'),
            ('nonassoc','LONE_IF'),
            ('nonassoc','COMMAND_ELSE'),
            ('left','.'),
            )

# YACC RULEZ 
def p_program(p):
    """
    program : statements
    """
    p[0] = p[1]

def p_zero_statements(p):
    """
    statements :
    """
    p[0] = BlockNode([])

def p_statements(p):
    """
    statements : statements statement 
    """
    if p[2] is not None:
        p[1].children.append(p[2])
    p[0] = p[1]

def p_block_baby(p):
    """
    statement : scopeupbro '{' statements '}' 
    """
    symbols = Tracker().get_symbols()
    symbols.remove_scope()
    Tracker().set_symbols(symbols)
    p[0] = p[3]

def p_break_statement(p):
    """
    statement : COMMAND_BREAK ';'
    """
    p[0] = BreakNode()


def p_scope_up_bro(p):
    """
    scopeupbro :
    """
    symbols = Tracker().get_symbols()
    symbols.add_scope()
    Tracker().set_symbols(symbols) 

def p_empty_statement(p):
    """
    statement : ';'
    """
    p[0] = NoOpNode()

def p_statement(p):
    """
    statement : expression ';'
    """
    p[0] = p[1]

def p_declaration_statement(p):
    """
    statement : declaration ';'
            | print_statement ';'
    """
    p[0] = p[1]

def p_print_statement(p):
    """
    print_statement : COMMAND_PRINT '(' non_empty_comma_sep_expr ')'
    """
    p[0] = p[3]


def p_comma_sep_expression_1(p):
    """
    non_empty_comma_sep_expr : expression
    """
    p[0] = PrintNode([p[1]])


def p_comma_sep_expression_many(p):
    """
    non_empty_comma_sep_expr : expression ',' non_empty_comma_sep_expr
    """
    p[3].children.insert(0,p[1])
    p[0] = p[3]

def p_declaration(p):
    """
    declaration : simple_declaration
                | assign_declaration
    """
    if isinstance(p[1],Node):
        p[0] = p[1]

def p_simple_declaration(p):
    """
    simple_declaration : type ID
    """
    var_name = p[2]
    symbols = Tracker().get_symbols()
    variable = p[1]
    variable.set_name(var_name)
    variable.set_value(variable.get_variable_template().format(Tracker().get_var_num()))
    symbols.declare_variable(variable)
    Tracker().set_symbols(symbols) 
    p[0] = variable

def p_assign_declaration(p):
    """
    assign_declaration : simple_declaration '=' expression
    """
    p[0] = AssignmentNode(p[1],p[3])

def p_if_statement(p):
    """
    statement : COMMAND_IF '(' expression ')' statement %prec LONE_IF
    """
    p[0] = IfNode(p[3],p[5])

def p_if_else_statement(p):
    """
    statement : COMMAND_IF '(' expression ')' statement COMMAND_ELSE statement
    """
    p[0] = IfElseNode(p[3],p[5],p[7])

def p_while_statement(p):
    """
    statement : COMMAND_WHILE '(' expression ')' statement
    """
    p[0] = WhileNode(p[3],p[5]) 

def p_var_usage(p):
    """
    var_usage : ID
    """
    symbols = Tracker().get_symbols()
    variable = symbols.deref_variable(p[1])
    p[0] = UsageNode(variable)

def p_array_element_usage(p):
    """
    var_usage : ID '[' expression ']'
    """
    symbols = Tracker().get_symbols()
    var = symbols.deref_variable(p[1])
    if var.get_type() != 'array':
        raise TypeError("Cannot index non array type variable {}".format(var.get_name()))
    p[0] = ArrayIndexNode(var,p[3])

def p_assignment(p):
    """
    expression : var_usage '=' expression
    """
    p[0] = ExpressionAssignmentNode(p[1],p[3])

def p_method_expression(p):
    """
    expression : expression '.' ID '(' ')'
    """
    var = p[1]
    p[0] = SizeMethodNode(var)

def p_resize_method_expression(p):
    """
    expression : expression '.' ID '(' expression ')'
    """
    var = p[1]
    child = p[5]
    p[0] = ResizeMethodNode(var,child)


def p_add_assign(p):
    """
    expression : var_usage ASSIGN_ADD expression
    """
    p[0] = ExpressionAssignmentNode(p[1],AdditionNode(p[1],p[3]))


def p_sub_assign(p):
    """
    expression : var_usage ASSIGN_SUB expression
    """
    p[0] = ExpressionAssignmentNode(p[1],SubtractionNode(p[1],p[3]))


def p_mult_assign(p):
    """
    expression : var_usage ASSIGN_MULT expression
    """
    p[0] = ExpressionAssignmentNode(p[1],MultiplicationNode(p[1],p[3]))


def p_div_assign(p):
    """
    expression : var_usage ASSIGN_DIV expression
    """
    p[0] = ExpressionAssignmentNode(p[1],DivisionNode(p[1],p[3]))


def p_var_usage_value(p):
    """
    expression : var_usage
    """
    p[0] = p[1]

def p_random_call(p):
    """
    expression : COMMAND_RANDOM '(' expression ')'
    """
    p[0] = RandomNode(p[3])

def p_type(p):
    """
    type : TYPE
    """
    p[0] = Variable("",p[1])

def p_alias_type(p):
    """
    type : ALIAS_TYPE
    """
    alias = p[1]
    var = None
    if alias == "string":
        var = ArrayVariable("",CharVariable(""))
    p[0] = var

def p_meta_type(p):
    """
    type : META_TYPE '(' TYPE ')'
    """
    sub_var = Variable("",p[3])
    p[0] = ArrayVariable("",sub_var)

def p_boolean_and(p):
    """
    expression : expression BOOL_AND expression
    """
    p[0] = BooleanAndNode(p[1],p[3])

def p_boolean_or(p):
    """
    expression : expression BOOL_OR expression
    """
    p[0] = BooleanOrNode(p[1],p[3])


def p_val_literal_expression(p):
    """
    expression : VAL_LITERAL
    """
    p[0] = ValLiteralNode(p[1])

def p_char_literal_expression(p):
    """
    expression : CHAR_LITERAL
    """
    p[0] = CharLiteralNode(p[1])

def p_string_literal_expression(p):
    """
    expression : STRING_LITERAL
    """
    p[0] = StringLiteralNode(p[1])


def p_arithmetic_expression_sub(p):
    """
    expression : expression '-' expression
    """
    p[0] = SubtractionNode(p[1],p[3])

def p_arithmetic_expression_mult(p):
    """
    expression : expression '*' expression
    """
    p[0] = MultiplicationNode(p[1],p[3])


def p_arithmetic_expression_div(p):
    """
    expression : expression '/' expression
    """
    p[0] = DivisionNode(p[1],p[3])


def p_arithmetic_expression_add(p):
    """
    expression : expression '+' expression
    """
    p[0] = AdditionNode(p[1],p[3])

def p_boolean_expression_equality(p):
    """
    expression : expression COMP_EQU expression
    """
    p[0] = EqualityNode(p[1],p[3])

def p_boolean_expression_inequality(p):
    """
    expression : expression COMP_NEQU expression
    """
    p[0] = InequalityNode(p[1],p[3])

def p_arithmetic_expression_negation(p):
    """
    expression : '-' expression %prec UNARY_MINUS
    """
    p[0] = NegateNode(p[2])

def p_boolean_expression_negation(p):
    """
    expression : '!' expression %prec UNARY_NOT
    """
    p[0] = NotNode(p[2])

def p_boolean_expression_less_than(p):
    """
    expression : expression COMP_LESS expression
    """
    p[0] = LessNode(p[1],p[3])

def p_boolean_expression_greater_than(p):
    """
    expression : expression COMP_GTR expression
    """
    p[0] = GreaterNode(p[1],p[3])

def p_boolean_expression_less_than_equal(p):
    """
    expression : expression COMP_LTE expression
    """
    p[0] = LessEqualNode(p[1],p[3])

def p_boolean_expression_greater_than_equal(p):
    """
    expression : expression COMP_GTE expression
    """
    p[0] = GreaterEqualNode(p[1],p[3])

def p_paren_expression(p):
    """
    expression : '(' expression ')'
    """
    p[0] = p[2]

def p_error(p):
    raise SyntaxError(p)

