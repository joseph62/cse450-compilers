#! /usr/bin/env python3
import sys
import ply.lex as lex
import ply.yacc as yacc

from tracker import Tracker
from node import *
from variable import *
from symbols import SymbolTable
from lexy import *
from yaccy import *

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

if __name__ == "__main__":
    source = sys.stdin.read()
    output = generate_bad_code_from_string(source)
    print(output)
