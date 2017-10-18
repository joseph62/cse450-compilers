#! /usr/bin/env python3
import sys
import ply.lex as lex
import ply.yacc as yacc

from .lib.tracker import Tracker
from .lib.yaccy import *
from .lib.lexy import *

# LEX RULEZ
def generate_bad_code_from_string(input_):
    Tracker()
    try:
        lexer = lex.lex()
        parser = yacc.yacc()
        program = parser.parse(input_, lexer=lexer)
        output = []
        program.generate_bad_code(output)
    except:
        Tracker().reset()
        raise
    Tracker().reset()
    return "\n".join(output) + "\n"

def generate_tree_from_string(input_):
    Tracker().reset()
    Tracker()

    lexer = lex.lex()
    parser = yacc.yacc()
    program = parser.parse(input_, lexer=lexer)
    program.generate_tree()

if __name__ == "__main__":
    source = sys.stdin.read()
    output = generate_bad_code_from_string(source)
    print(output)
