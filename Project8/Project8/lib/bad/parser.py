# Parser for bad code for optimization
import ply.yacc as yacc
from .baddata import *
from .commands import *

class VariableEntry():
    def __init__(self,variable):
        self._variable = variable
        self._reads = []
        self._writes = []

    @property
    def variable(self):
        return self._variable

    def __hash__(self):
        return hash(self._variable.value)

    @property
    def reads(self):
        return self._reads

    @property
    def writes(self):
        return self._writes

VARIABLES = {}

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
    p[0] = CommandFactory.make_command(p[1],p[2])

def p_tag_line(p):
    """
    tag_line : TAG ':' eol
    """
    p[0] = CommandFactory.make_command("target",[p[1]])

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
    data = BadData(p[1],BadDataTypes.Scalar) 
    if data not in VARIABLES:
        VARIABLES[data] = VariableEntry(data)
    p[0] = data

def p_array_variable(p):
    """
    value : ARRAY_VARIABLE
    """
    data = BadData(p[1],BadDataTypes.Array) 
    if data not in VARIABLES:
        VARIABLES[data] = VariableEntry(data)
    p[0] = data

def p_tag(p):
    """
    value : TAG
    """
    p[0] = BadData(p[1],BadDataTypes.Tag)

def p_val_literal(p):
    """
    value : VAL_LITERAL 
    """
    p[0] = BadData(p[1],BadDataTypes.Literal)

def p_char_literal(p):
    """
    value : CHAR_LITERAL 
    """
    p[0] = BadData(p[1],BadDataTypes.Literal)

def p_error(p):
    raise Exception("Parsing Error Occured! Result: {}".format(p))
