#Name: Sean Joseph
#This is where my production rules are housed!
from .tracker import Tracker
from .variable import *
from .symbols import SymbolTable
from .node import *
from .function import Function

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
    symbols = Tracker().symbols
    symbols.remove_scope()
    Tracker().symbols = symbols
    p[0] = p[3]

def p_return_statement(p):
    """
    retstatement : COMMAND_RETURN expression ';'
    """
    p[0] = ReturnNode(p[2])

def p_return_statement_as_statement(p):
    """
    statement : retstatement
    """
    p[0] = p[1]

def p_break_statement(p):
    """
    statement : COMMAND_BREAK ';'
    """
    p[0] = BreakNode()

def p_funcdef_statement(p):
    """
    statement : funcdef
    """
    p[0] = p[1]

def p_function_definition(p):
    """
    funcdef : in_function FUNCTION_DEFINE type ID  scopeupbro '(' parameters ')' statement
    """
    #class Function(name,_type,label,return_var,return_label,argument_vars):
    tracker = Tracker()
    funcname = p[4]
    functype = p[3]
    parameters = p[7]
    node = p[9]
    function = Function(funcname,functype,parameters,node)
    tracker.functions.declare_variable(function)
    tracker.symbols.remove_scope()
    tracker.in_function = False
    p[0] = None

def p_in_function(p):
    """
    in_function : 
    """
    tracker = Tracker()
    if tracker.in_function:
        raise Exception("Cannot define a function in a function!")
    tracker.in_function = True

def p_function_call(p):
    """
    expression : ID '(' arguments ')'
    """
    p[0] = FunctionCallNode(p[1],p[3])

def p_arguments_list(p):
    """
    arguments : argument ',' arguments
    """
    arguments = p[3]
    arguments.insert(0,p[1])
    p[0] = arguments

def p_empty_arguments(p):
    """
    arguments : 
    """
    p[0] = []

def p_single_argument(p):
    """
    arguments : argument
    """
    p[0] = [p[1]]

def p_argument(p):
    """
    argument : expression
    """
    p[0] = p[1]

def p_parameter_list(p):
    """
    parameters : parameter ',' parameters
    """
    parameters = p[3]
    parameters.insert(0,p[1])
    p[0] = parameters

def p_parameter(p):
    """
    parameter : simple_declaration
    """
    p[0] = p[1]

def p_empty_parameter_list(p):
    """
    parameters : 
    """
    p[0] = []

def p_one_parameter_list(p):
    """
    parameters : parameter
    """
    p[0] = [p[1]]

def p_scope_up_bro(p):
    """
    scopeupbro :
    """
    symbols = Tracker().symbols
    symbols.add_scope()
    Tracker().symbols = symbols

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
    symbols = Tracker().symbols
    name = p[2]
    _type = p[1]
    value = _type.template.format(Tracker().varnum)
    data = Data(value,_type)
    variable = Variable(name,data)
    symbols.declare_variable(variable)
    Tracker().symbols = symbols
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
    symbols = Tracker().symbols
    variable = symbols.deref_variable(p[1])
    p[0] = UsageNode(variable)

def p_array_element_usage(p):
    """
    var_usage : ID '[' expression ']'
    """
    symbols = Tracker().symbols
    var = symbols.deref_variable(p[1])
    TypeEnforcer.error_if_is_not(var,TypeEnum.Array)
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
    p[0] = ExpressionAssignmentNode(p[1],ArithmeticNode('+',p[1],p[3])) 

def p_sub_assign(p):
    """
    expression : var_usage ASSIGN_SUB expression
    """
    p[0] = ExpressionAssignmentNode(p[1],ArithmeticNode('-',p[1],p[3])) 

def p_mult_assign(p):
    """
    expression : var_usage ASSIGN_MULT expression
    """
    p[0] = ExpressionAssignmentNode(p[1],ArithmeticNode('*',p[1],p[3])) 

def p_div_assign(p):
    """
    expression : var_usage ASSIGN_DIV expression
    """
    p[0] = ExpressionAssignmentNode(p[1],ArithmeticNode('/',p[1],p[3])) 

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
    p[0] = TypeFactory.make(p[1])

def p_alias_type(p):
    """
    type : ALIAS_TYPE
    """
    alias = p[1]
    aliastype = None
    if alias == "string":
        subtype = TypeFactory.make("char")
        aliastype = TypeFactory.makemeta("array",subtype)
    else:
        raise ValueError("Alias type {} not configured!".format(alias))
    p[0] = aliastype

def p_meta_type(p):
    """
    type : META_TYPE '(' TYPE ')'
    """
    subtype = TypeFactory.make(p[3])
    p[0] = TypeFactory.makemeta(p[1],subtype)

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

def p_arithmetic_expression(p):
    """
    expression : expression '-' expression
                | expression '/' expression
                | expression '+' expression
                | expression '*' expression
    """
    p[0] = ArithmeticNode(p[2],p[1],p[3])

def p_boolean_expression_equality(p):
    """
    expression : expression COMP_EQU expression
                | expression COMP_NEQU expression
                | expression COMP_LESS expression
                | expression COMP_GTR expression
                | expression COMP_LTE expression
                | expression COMP_GTE expression
    """
    p[0] = ComparisonNode(p[2],p[1],p[3])

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

def p_paren_expression(p):
    """
    expression : '(' expression ')'
    """
    p[0] = p[2]

def p_error(p):
    raise SyntaxError(p)

