#! /usr/bin/env python3

import sys
import ply.lex as lex
import ply.yacc as yacc
from data import *

literals = ':'

tokens = [
        "COMMAND",
        "TAG",
        "SCALAR_VARIABLE",
        "ARRAY_VARIABLE",
        "VAL_LITERAL",
        "CHAR_LITERAL",
        "COMMENT",
        "NEWLINE",
        ]

commands = [
        "val_copy",
        "add",
        "sub",
        "mult",
        "div",
        "test_less",
        "test_gtr",
        "test_equ",
        "test_nequ",
        "test_gte",
        "test_lte",
        "jump",
        "jump_if_0",
        "jump_if_n0",
        "random",
        "out_val",
        "out_char",
        "nop",
        "push",
        "pop",
        "ar_get_idx",
        "ar_set_idx",
        "ar_get_size",
        "ar_set_size",
        "ar_copy",
        "ar_push",
        "ar_pop",
        ]

def t_NEWLINE(t):
    r"[\n]"
    return t

def t_WHITESPACE(t):
    r"[ \t]+"

def t_COMMENT(t):
    r"\#.*"

def t_SCALAR_VARIABLE(t):
    r"s[0-9]+"
    return t

def t_ARRAY_VARIABLE(t):
    r"a[0-9]+"
    return t

def t_VAL_LITERAL(t):
    r"(\.[0-9]+|[0-9]+(\.[0-9]+)?)"
    return t

def t_CHAR_LITERAL(t):
    r"'(\\'|\\\\|\\n|\\t|[^'\\])'"
    return t
    

def t_TAG(t):
    r"[a-zA-Z0-9_]+"
    if t.value in commands:
        t.type = "COMMAND"
    return t

def t_error(t):
    raise Exception("Bad token found! Token: {}".format(t))


def p_program(p):
    """
    program : lines
    """
    p[0] = p[1]

def p_lines(p):
    """
    lines : lines line
    """
    p[1].append(p[2])
    p[0] = p[1]

def p_no_lines(p):
    """
    lines : 
    """
    p[0] = []

def p_END_OF_LINE(p):
    """
    eol : NEWLINE
    """
    p[0] = []

def p_line(p):
    """
    line : command_line
        | tag_line
        | empty_line
    """
    p[0] = p[1]

def p_empty_line(p):
    """
    empty_line : eol
    """
    p[0] = ()

def p_command_line(p):
    """
    command_line : COMMAND values eol
    """
    p[0] = (p[1],p[2])

def p_tag_line(p):
    """
    tag_line : TAG ':' eol
    """
    p[0] = ("target",[p[1]])

def p_VALUES(p):
    """
    values : values value
    """
    p[1].append(p[2])
    p[0] = p[1]

def p_EMPTY_VALUES(p):
    """
    values : 
    """
    p[0] = []

def p_VALUE(p):
    """
    value : SCALAR_VARIABLE 
    """
    p[0] = p[1]

def p_tag(p):
    """
    value : TAG
    """
    p[0] = p[1]

def p_array_variable(p):
    """
    value : ARRAY_VARIABLE
    """
    p[0] = ArrayData(p[1])

def p_val_literal(p):
    """
    value : VAL_LITERAL 
    """
    p[0] = ValData(p[1])

def p_char_literal(p):
    """
    value : CHAR_LITERAL 
    """
    p[0] = CharData(p[1])

def p_error(p):
    raise Exception("Parsing Error Occured! Result: {}".format(p))

def run_lexer(_input):
    lexer = lex.lex()

    lexer.input(_input)

    while True:
        token = lexer.token()
        if not token:
            break
        print("{}: {}".format(token.type,token.value))

def run_parser(_input):
    lexer = lex.lex()
    parser = yacc.yacc()
    result = parser.parse(_input)
    return result

def interpret_bad_code(_input):
    instructions = run_parser(_input)
    return instructions

if __name__ == '__main__':
    _input = sys.stdin.read()

    output = interpret_bad_code(_input)
    print(output)
