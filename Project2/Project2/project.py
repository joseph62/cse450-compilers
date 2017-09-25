#! /usr/bin/env python3

import sys
import ply.lex as lex
import ply.yacc as yacc

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

literals = ["+","-","*","/","(",")","=",",","{","}","[","]",".",";"]

#precedence = (('left', '+'),)

# LEXER RULES
def t_newline(t):
    r'\n'
    #t.lexer.lineno += 1
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

def t_UNKNOWN(t):
    r'.'
    #print("Unknown token on line {}: {}".format(t.lexer.lineno,t.value))
    sys.exit(0)
    return t

# Example implementation from the ply
# documentation
def t_error(t):
    print("Bad character: {}".format(t.value))
    sys.exit(1)
# END OF TOKEN DEFINITIONS


# START OF YACC RULES
def p_program(p):
    """
    program : statements
    """
    print("Valid Program")

def p_empty_statements(p):
    """
    statements : 
    """
    print("Beginning...")

def p_statements(p):
    """
    statements : statements statement
    """
    p[0] = p[2]
    print("statements that make for statements")

def p_statement(p):
    """
    statement : expression ';'
    """
    print("Single statement")
    p[0] = p[1]

def p_empty_expression(p):
    """
    expression : 
    """
    print("Empty expression found!")
    p[0] = None

def p_expression_literal(p):
    """
    expression : VAL_LITERAL
    """
    print("Literal found: {}".format(p[1]))
    p[0] = p[1]

def p_maths_expression_add(p):
    """
    expression : expression '+' expression
    """
    p[0] = p[1] + p[3]

def p_maths_expression_subtract(p):
    """
    expression : expression '-' expression
    """
    p[0] = p[1] - p[3]


def p_maths_expression_multiply(p):
    """
    expression : expression '*' expression
    """
    p[0] = p[1] * p[3]

def p_maths_expression_divide(p):
    """
    expression : expression '/' expression
    """
    p[0] = p[1] / p[3]

def p_error(p):
    raise SyntaxError(p)

# END OF YACC RULES

def parse_string(input_):
    lex.lex()
    parser = yacc.yacc()
    parser.parse(input_)
    return True

if __name__ == "__main__":
    source = sys.stdin.read()
    source = """
    ;
    ;
    ;;
    4;5;5;
    """
    parse_string(source)
    print("Parse Successful!")
