#! /usr/bin/env python3
import sys
import ply.lex as lex
import ply.yacc as yacc

reserved = {
    'val': 'TYPE',
    'char': 'TYPE',
    'string': 'TYPE',
    'print': 'COMMAND_PRINT',
    'random': 'COMMAND_RANDOM'
}

tokens = [
    'ID',
    'VAL_LITERAL',
    'CHAR_LITERAL',
    'STRING_LITERAL',
    'ASSIGN_ADD',
    'ASSIGN_SUB',
    'ASSIGN_MULT',
    'ASSIGN_DIV',
    'COMP_EQU',
    'COMP_NEQU',
    'COMP_LESS',
    'COMP_LTE',
    'COMP_GTR',
    'COMP_GTE',
    'BOOL_AND',
    'BOOL_OR',
    ] + list(set(reserved.values()))


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_VAL_LITERAL(t):
    r'((\d+)(\.\d+)?)|(\.\d+)'
    return t


def t_CHAR_LITERAL(t):
    r"'.'"
    return t


def t_STRING_LITERAL(t):
    r'"[^\n"]*"'
    return t


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


def t_COMP_NEQU(t):
    r'!='
    return t


def t_COMP_LTE(t):
    r'<='
    return t


def t_COMP_GTE(t):
    r'>='
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


literals = '+-*/()=,{}[].;'


def t_WHITESPACE(t):
    r'[ \t]'
    pass


def t_COMMENT(t):
    r'\#[^\n]*'
    pass


def t_error(t):
    raise SyntaxError("Unknown token on line {}: {}".format(t.lexer.lineno, t.value[0]))


DECLARED_VARIABLES = {}

def p_program(p):
    """
    program : statements
    """
    pass


def p_statements_empty(p):
    """
    statements :
    """
    pass


def p_statements_nonempty(p):
    """
    statements : statement statements
    """
    pass


def p_statement_rules(p):
    """
    statement : expression ';'
              | print_statement ';'
              | declaration ';'
    """
    pass


def p_print_statement(p):
    """
    print_statement : COMMAND_PRINT '(' non_empty_comma_sep_expr ')'
    """
    pass


def p_comma_sep_expression_1(p):
    """
    non_empty_comma_sep_expr : expression
    """
    pass


def p_comma_sep_expression_many(p):
    """
    non_empty_comma_sep_expr : expression ',' non_empty_comma_sep_expr
    """
    pass


def p_assignment(p):
    """
    expression : var_usage '=' expression
    """
    pass


def p_binary_math(p):
    """
    expression : expression '+' expression
               | expression '-' expression
               | expression '*' expression
               | expression '/' expression
    """
    pass


def p_unary_minus(p):
    """
    expression : '-' expression
    """
    pass


def p_compound_math(p):
    """
    expression : var_usage ASSIGN_ADD expression
               | var_usage ASSIGN_SUB expression
               | var_usage ASSIGN_DIV expression
               | var_usage ASSIGN_MULT expression
    """
    pass


def p_comparisons(p):
    """
    expression : expression COMP_EQU expression
               | expression COMP_NEQU expression
               | expression COMP_LTE expression
               | expression COMP_LESS expression
               | expression COMP_GTR expression
               | expression COMP_GTE expression
    """
    pass


def p_boolean_operators(p):
    """
    expression : expression BOOL_AND expression
               | expression BOOL_OR expression
    """
    pass


def p_simple_declaration(p):
    """
    simple_declaration : type ID
    """
    var_name = p[2]
    if var_name in DECLARED_VARIABLES:
        raise NameError("{} redeclared!".format(var_name))
    DECLARED_VARIABLES[p[2]] = None


def p_assign_declaration(p):
    """
    assign_declaration : simple_declaration '=' expression
    """
    pass


def p_declaration(p):
    """
    declaration : simple_declaration
                | assign_declaration
    """
    pass


def p_var_usage(p):
    """
    var_usage : ID
    """
    var_name = p[1]
    if var_name not in DECLARED_VARIABLES:
        raise NameError("{} not declared!".format(var_name))


def p_value(p):
    """
    expression : VAL_LITERAL
               | CHAR_LITERAL
               | STRING_LITERAL
               | var_usage
    """
    pass


def p_parentheses(p):
    """
    expression : '(' expression ')'
    """
    pass


def p_type(p):
    """
    type : TYPE
    """
    pass


def p_random(p):
    """
    expression : COMMAND_RANDOM '(' expression ')'
    """
    pass


def p_error(p):
    line = 0 if p is None else p.lineno
    raise SyntaxError("ERROR(line {}): syntax error {}".format(line, p))


def lex_stdin():
    data = sys.stdin.read()
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        if tok.type in literals:
            print("ASCII_CHAR: {}".format(tok.value))
        else:
            print("{0.type}: {0.value}".format(tok))
    print("Line Count: {}".format(lexer.lineno - 1))


def reset():
    global DECLARED_VARIABLES
    DECLARED_VARIABLES = {}


def parse_string(input_):
    reset()

    lexer = lex.lex()
    parser = yacc.yacc()
    parser.parse(input_, lexer=lexer)

    return True


if __name__ == "__main__":
    source = sys.stdin.read()
    parse_string(source)
