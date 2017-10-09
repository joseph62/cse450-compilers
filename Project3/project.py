#! /usr/bin/env python3
import sys
import ply.lex as lex
import ply.yacc as yacc
from tracker import Tracker
from variable import CharVariable, ValVariable
from nodes import *

special_words = {
        'val' : 'TYPE',
        'char' : 'TYPE',
        'string' : 'TYPE',
        'print' : 'COMMAND_PRINT',
        'random' : 'COMMAND_RANDOM',
}

tokens = ["TYPE","COMMAND_PRINT","COMMAND_RANDOM",
        "ID","VAL_LITERAL","CHAR_LITERAL","STRING_LITERAL",
        "ASSIGN_ADD","ASSIGN_SUB","ASSIGN_MULT",
        "ASSIGN_DIV","COMP_EQU","COMP_NEQU","COMP_LESS",
        "COMP_LTE","COMP_GTR","COMP_GTE","BOOL_AND","BOOL_OR",
        "WHITESPACE","COMMENT","UNKNOWN"] + list(set(special_words.values()))

literals = "+-*/()={}[].;!,"

Tracker()

precedence = (
            ('nonassoc','UNARY_MINUS'),
            ('left','+', '-', '*', '/'),
            ('nonassoc','COMP_EQU' ,'COMP_NEQU' ,'COMP_LESS' ,
                'COMP_LTE' ,'COMP_GTR' ,'COMP_GTE'),
            ('left','BOOL_OR','BOOL_AND'),
            ('right','=' ,'ASSIGN_ADD' ,'ASSIGN_SUB' ,
                'ASSIGN_MULT' ,'ASSIGN_DIV'),
            )


def t_SEVEN(t):
    r'7'
    return t


def t_WHITESPACE(t):
    r'\n'
    pass


def t_error(t):
    print("Unknown token on line {}: {}".format(t.lexer.lineno, t.value[0]))
    raise SyntaxError(t)
    exit(1)


precedence = (('left', '+'),)


def p_program(p):
    """
    program : SEVEN
            | SEVEN '+' SEVEN
    """
    p[0] = Node()


def p_error(p):
    raise SyntaxError(p)


def generate_bad_code_from_string(input_):
    lexer = lex.lex()
    parser = yacc.yacc()
    program = parser.parse(input_, lexer=lexer)

    output = []
    program.generate_bad_code(output)
    return "\n".join(output) + "\n"


if __name__ == "__main__":
    source = sys.stdin.read()
    result = generate_bad_code_from_string(source)
    print(result)
