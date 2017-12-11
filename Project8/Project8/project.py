#! /usr/bin/env python3
import sys
import ply.lex as lex
import ply.yacc as yacc

from .lib.tracker import Tracker
from .lib.yaccy import *
from .lib.lexy import *
from .lib.ugly import *
from .lib.optimize import optimize_bad, optimize_ugly

def generate_ugly_code_from_string(input_,optimize_mode=False):
    output = generate_bad_code_from_string(input_)
    lines = output.split("\n")
    output = compile_ugly_lines(lines)
    if optimize_mode:
        output = optimize_ugly(output)
    return "\n".join(output) + "\n"

# LEX RULEZ
def generate_bad_code_from_string(input_,optimize_mode=False):
    Tracker().reset()
    tracker = Tracker()
    lexer = lex.lex()
    parser = yacc.yacc()
    program = parser.parse(input_, lexer=lexer)
    output = []
    function_block = []
    for function in tracker.functions.get_all_variables():
        function_block.append("{}:".format(function.label))
        tracker.in_function = True
        tracker.active_function = function
        for node in function.nodes:
            node.generate_bad_code(function_block)
    tracker.in_function = False
    program.generate_bad_code(output)
    output.append("jump program_end")
    output.append("# Function Definitions")
    output += function_block
    output.append("program_end:")

    output = "\n".join(output) + "\n"
 

    if optimize_mode:
        output = optimize_bad(output)

    return output

def generate_tree_from_string(input_):
    Tracker().reset()
    Tracker()

    lexer = lex.lex()
    parser = yacc.yacc()
    program = parser.parse(input_, lexer=lexer)
    program.generate_tree()
