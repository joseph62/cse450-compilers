#! /usr/bin/env python3
import sys
import ply.lex as lex
import ply.yacc as yacc

from .lib.tracker import Tracker
from .lib.yaccy import *
from .lib.lexy import *
from .lib.ugly import *

def generate_ugly_code_from_string(input_):
    output = generate_bad_code_from_string(input_)
    lines = output.split("\n")
    output = compile_ugly_lines(lines)
    return "\n".join(output) + "\n"

# LEX RULEZ
def generate_bad_code_from_string(input_):
    Tracker().reset()
    tracker = Tracker()
    lexer = lex.lex()
    parser = yacc.yacc()
    program = parser.parse(input_, lexer=lexer)
    output = []
    program.generate_bad_code(output)
    output.append("jump program_end")
    output.append("# Function Definitions")
    for function in tracker.functions.get_all_variables():
        output.append("{}:".format(function.label))
        tracker.active_function = function
        for node in function.nodes:
            node.generate_bad_code(output)
    output.append("program_end:")
    return "\n".join(output) + "\n"

def generate_tree_from_string(input_):
    Tracker().reset()
    Tracker()

    lexer = lex.lex()
    parser = yacc.yacc()
    program = parser.parse(input_, lexer=lexer)
    program.generate_tree()
