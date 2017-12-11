# Optimizing functions

import ply.lex as lex
import ply.yacc as yacc
from .bad.lexer import *
from .bad.parser import *

def get_blocks(lines):
    blocks = [[]]
    for line in lines:
        if line == ():
            continue
        if line.instruction.startswith("jump"):
            # Jump statement ends a block
            blocks[-1].append(line)
            blocks.append([])
        elif line.instruction == "target":
            # A tag starts the block
            blocks.append([line]) 
        else:
            # Add lines in they are comments or instructions
            blocks[-1].append(line)

    return [ block for block in blocks if len(block) > 0 ]

def parse_bad_code(input_):
    global VARIABLES
    VARIABLES = {}
    lexer = lex.lex()
    parser = yacc.yacc()
    program = parser.parse(input_, lexer=lexer)
    return program

def get_usage_data(blocks):
    global VARIABLES
    for block_num,block in enumerate(blocks):
        for line_num,line in enumerate(block):
            for variable in VARIABLES.keys():
                if variable in line.reads:
                    VARIABLES[variable].reads.append((block_num,line_num))
                if variable in line.writes:
                    VARIABLES[variable].writes.append((block_num,line_num))

    print(VARIABLES)


def optimize_bad(input_):
    program = parse_bad_code(input_)
    blocks = get_blocks(program)
    usage_data = get_usage_data(blocks)
    return input_

def optimize_ugly(lines):
    return lines
