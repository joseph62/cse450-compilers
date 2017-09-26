#! /usr/bin/env python3

import sys
import ply.lex as lex
import ply.yacc as yacc
import re

special_words = {
        'val' : 'TYPE',
        'char' : 'TYPE',
        'string' : 'TYPE',
        'print' : 'COMMAND_PRINT',
        'random' : 'COMMAND_RANDOM',
}

tokens = ("TYPE","COMMAND_PRINT","COMMAND_RANDOM",
        "ID","VAL_LITERAL","CHAR_LITERAL","STRING_LITERAL",
        "ASSIGN_ADD","ASSIGN_SUB","ASSIGN_MULT",
        "ASSIGN_DIV","COMP_EQU","COMP_NEQU","COMP_LESS",
        "COMP_LTE","COMP_GTR","COMP_GTE","BOOL_AND","BOOL_OR",
        "WHITESPACE","COMMENT","UNKNOWN")

literals = "+-*/()={}[].;!,"

SYMBOLS = {}

precedence = (('left', '*', '/', '+', '-','COMP_LESS','COMP_GTR',
    'COMP_LTE','COMP_GTE','COMP_EQU','COMP_NEQU','BOOL_AND','BOOL_OR'),

                ('usage','assignment'),
                )

# LEXER RULES
def t_newline(t):
    r'\n'
    t.lexer.lineno += 1
    t.type = 'WHITESPACE'

def t_WHITESPACE(t):
    r'[ \t]+'
    return None

def t_ID(t):
    r'[a-zA-Z_]+[a-zA-Z0-9\-_]*'
    t.type = special_words.get(t.value,'ID')
    return t

def t_VAL_LITERAL(t):
    r'([0-9]*\.[0-9]+|[0-9]+)'
    string_with_a_period = "^[0-9]*\.[0-9]*$"
    regex = re.compile(string_with_a_period)
    if regex.match(t.value):
        # VAL_LITERAL is a float
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

def t_CHAR_LITERAL(t):
    r'\'.\''
    return t

def t_STRING_LITERAL(t):
    r'".*"'
    return t

def t_COMMENT(t):
    r'\#.*'
    return None

def t_ASSIGN_ADD(t):
    r'\+='
    return t

def t_ASSIGN_SUB(t):
    r'\-='
    return t

def t_ASSIGN_MULT(t):
    r'\*='
    return t

def t_ASSIGN_DIV(t):
    r'/='
    return t

def t_COMP_EQU(t):
    r'=='
    return t

def t_COMP_LTE(t):
    r'<='
    return t

def t_COMP_GTE(t):
    r'>='
    return t

def t_COMP_NEQU(t):
    r'!='
    return t

def t_COMP_LESS(t):
    r'<'
    return t

def t_COMP_GTR(t):
    r'>'
    return t

def t_BOOL_AND(t):
    r'&&'
    return t

def t_BOOL_OR(t):
    r'\|\|'
    return t

# Example implementation from the ply
# documentation
def t_error(t):
    print("Unknown token on line {}: {}".format(t.lexer.lineno,t.value))
    sys.exit(1)
# END OF TOKEN DEFINITIONS


# START OF YACC RULES
def p_program(p):
    """
    program : statements
    """
    global SYMBOLS
    SYMBOLS = {}
    print("I'm a program!")

def p_zero_statements(p):
    """
    statements :
    """
    print("Started parsing!")

def p_statements(p):
    """
    statements : statements statement 
    """
    pass

def p_declarative_statements(p):
    """
    statement : declaration ';'
    """
    pass

def p_var_usage_assign_declare_expressions(p):
    """
    expression : assignment
            | usage
    """
    p[0] = p[1]

def p_command_expression(p):
    """
    expression : function
    """
    print("Function call found")
    p[0] = p[1]

def p_print_command(p):
    """
    function : COMMAND_PRINT '(' nonempty_list ')'
    """
    print("Print command found")
    p[0] = None

def p_random_command(p):
    """
    function : COMMAND_RANDOM '(' expression ')'
    """
    print("Random command found")
    p[0] = 1337

def p_list(p):
    """
    list : empty_list
    | nonempty_list
    """
    print("List found")
    p[0] = p[1]

def p_nonempty_list(p):
    """
    nonempty_list : expression ',' list
    """
    print("Nonempty list found")
    if p[3] is not None:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_single_element_list(p):
    """
    nonempty_list : expression
    """
    p[0] = [p[1]]

def p_empty_list(p):
    """
    empty_list : 
    """
    print("End of list")
    p[0] = None

def p_var_declaration(p):
    """
    declaration : TYPE ID
    """
    global SYMBOLS
    print("Variable Declaration")
    if p[2] in SYMBOLS:
        raise NameError(p)
    SYMBOLS[p[2]] = 0
    p[0] = p[2]

def p_var_assign(p):
    """
    assignment : ID '=' expression
    """
    global SYMBOLS
    print("variable {} is now {}".format(p[1],p[3]))
    if p[1] not in SYMBOLS:
        raise NameError(p)
    SYMBOLS[p[1]] = p[3]
    p[0] = SYMBOLS[p[1]]


def p_var_declare_assign_combo(p):
    """
    declaration : TYPE ID '=' expression
    """
    global SYMBOLS
    if p[2] in SYMBOLS:
        raise NameError(p)
    SYMBOLS[p[2]] = p[4]
    print("new variable {} declared with value {}".format(p[2],p[4]))
    p[0] = SYMBOLS[p[2]]

def p_var_add_assign_operation(p):
    """
    assignment : ID ASSIGN_ADD expression
    """
    if p[1] not in SYMBOLS:
        raise NameError(p)
    SYMBOLS[p[1]] += p[3]
    p[0] = SYMBOLS[p[1]]

def p_var_subtract_assign_operation(p):
    """
    assignment : ID ASSIGN_SUB expression
    """
    if p[1] not in SYMBOLS:
        raise NameError(p)
    SYMBOLS[p[1]] -= p[3]
    p[0] = SYMBOLS[p[1]]

def p_var_mulitply_assign_operation(p):
    """
    assignment : ID ASSIGN_MULT expression
    """
    if p[1] not in SYMBOLS:
        raise NameError(p)
    SYMBOLS[p[1]] *= p[3]
    p[0] = SYMBOLS[p[1]]


def p_var_divide_assign_operation(p):
    """
    assignment : ID ASSIGN_DIV expression
    """
    if p[1] not in SYMBOLS:
        raise NameError(p)
    SYMBOLS[p[1]] /= p[3]
    p[0] = SYMBOLS[p[1]]

def p_statement(p):
    """
    statement : expression ';'
    """
    print("My statement's result: {}".format(p[1]))

def p_var_dereference_expression(p):
    """
    usage : ID
    """
    global SYMBOLS
    if p[1] not in SYMBOLS:
        raise NameError(p)
    print("Variable Dereferenced! {} is {}".format(p[1],SYMBOLS[p[1]]))
    p[0] = SYMBOLS[p[1]]

def p_negation_expression(p):
    """
    expression : negate expression
    """
    p[0] = -p[2]

def p_left_expression(p):
    """
    negate : '-'
    """
    pass

def p_val_literal_expression(p):
    """
    expression : VAL_LITERAL
    """
    print("val literal found!")
    p[0] = p[1]

def p_parens_expression(p):
    """
    expression : '(' expression ')'
    """
    p[0] = p[2]

def p_arithmetic_expression_add(p):
    """
    expression : expression '+' expression
    """
    p[0] = p[1] + p[3]

def p_arithmetic_expression_subtraction(p):
    """
    expression : expression '-' expression
    """
    p[0] = p[1] - p[3]


def p_arithmetic_expression_multiply(p):
    """
    expression : expression '*' expression
    """
    p[0] = p[1] * p[3]


def p_arithmetic_expression_division(p):
    """
    expression : expression '/' expression
    """
    p[0] = p[1] / p[3]

def p_boolean_expression_equality(p):
    """
    expression : expression COMP_EQU expression
    """
    p[0] = p[1] == p[3]

def p_boolean_expression_inequality(p):
    """
    expression : expression COMP_NEQU expression
    """
    p[0] = p[1] != p[3]

def p_boolean_expression_negation(p):
    """
    expression : '!' expression
    """
    p[0] = not p[2]

def p_boolean_expression_less_than(p):
    """
    expression : expression COMP_LESS expression
    """
    p[0] = p[1] < p[3]

def p_boolean_expression_greater_than(p):
    """
    expression : expression COMP_GTR expression
    """
    p[0] = p[1] > p[3]

def p_boolean_expression_less_than_equal(p):
    """
    expression : expression COMP_LTE expression
    """
    p[0] = p[1] <= p[3]

def p_boolean_expression_greater_than_equal(p):
    """
    expression : expression COMP_GTE expression
    """
    p[0] = p[1] >= p[3]

def p_boolean_expression_and(p):
    """
    expression : expression BOOL_AND expression
    """
    p[0] = p[1] and p[3]

def p_boolean_expression_or(p):
    """
    expression : expression BOOL_OR expression
    """
    p[0] = p[1] or p[3]

def p_error(p):
    print("Syntax Error!")
    raise SyntaxError(p)

# END OF YACC RULES

def parse_string(input_):
    lex.lex()
    parser = yacc.yacc()
    parser.parse(input_)
    return True

if __name__ == "__main__":
    source = sys.stdin.read()
    parse_string(source)

    '''
    lexer = lex.lex()
    lexer.input(source)
    while True:
        token = lexer.token()
        if not token:
            break
        print("{}: {}".format(token.type,token.value))

    print("Line Count: {}".format(lexer.lineno - 1))
    '''
    print("Parse Successful!")
