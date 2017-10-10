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

tokens = ["ID","VAL_LITERAL","CHAR_LITERAL","STRING_LITERAL",
        "ASSIGN_ADD","ASSIGN_SUB","ASSIGN_MULT",
        "ASSIGN_DIV","COMP_EQU","COMP_NEQU","COMP_LESS",
        "COMP_LTE","COMP_GTR","COMP_GTE","BOOL_AND","BOOL_OR",
        "WHITESPACE","COMMENT","UNARY_MINUS"] + list(set(special_words.values()))

literals = "+-*/()={}[].;!,"
Tracker()

# LEX RULEZ
def t_newline(t):
    r'\n'
    t.lexer.lineno += 1
    t.type = 'WHITESPACE'

def t_WHITESPACE(t):
    r'[ \t]+'
    return None

def t_VAL_LITERAL(t):
    r'([0-9]*\.[0-9]+|[0-9]+)'
    t.value = float(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9\-_]*'
    t.type = special_words.get(t.value,'ID')
    return t

def t_CHAR_LITERAL(t):
    r'(\'.\'|\'\t\'|\'\\\'\'|\'\n\'|\'\#\')'
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

def t_error(t):
    print("Unknown token on line {}: {}".format(t.lexer.lineno, t.value[0]))
    raise SyntaxError(t)
'''
precedence = (
            ('right','=' ,'ASSIGN_ADD' ,'ASSIGN_SUB' ,
                'ASSIGN_MULT' ,'ASSIGN_DIV'),
            ('left','BOOL_OR'),
            ('left','BOOL_AND'),
            ('nonassoc','COMP_EQU','COMP_NEQU','COMP_LESS',
                'COMP_LTE','COMP_GTR','COMP_GTE'),
            ('left','+', '-'),
            ('left','*','/'),
            ('nonassoc','UNARY_MINUS'),
            )
'''

# YACC RULEZ

def p_program(p):
    """
    program : statements
    """
    print("Statements Final: {}".format(p[1]))
    p[0] = p[1]

def p_zero_statements(p):
    """
    statements :
    """
    print("Started Block Node")
    p[0] = BlockNode([])

def p_statements(p):
    """
    statements : statements statement 
    """
    print("Adding statement to block node")
    if p[2] is not None:
        p[1].children.append(p[2])
    p[0] = p[1]

def p_statement(p):
    """
    statement : expression ';'
    """
    print("Statement: {}".format(p[1]))
    p[0] = p[1]

def p_declaration_statement(p):
    """
    statement : declaration ';'
    """
    pass

def p_declaration(p):
    """
    declaration : type ID
    """
    var_name = p[2]
    symbols = Tracker().get_symbols()
    symbols.declare_variable(ValVariable(var_name))
    Tracker().set_symbols(symbols) 

def p_type(p):
    """
    type : TYPE
    """
    p[0] = p[1]

def p_val_literal_expression(p):
    """
    expression : VAL_LITERAL
    """
    p[0] = ValLiteralNode(p[1])

def p_arithmetic_expression_sub(p):
    """
    expression : expression '-' expression
    """
    p[0] = SubtractionNode(p[1],p[3])

def p_arithmetic_expression_mult(p):
    """
    expression : expression '*' expression
    """
    p[0] = MultiplicationNode(p[1],p[3])


def p_arithmetic_expression_div(p):
    """
    expression : expression '/' expression
    """
    p[0] = DivisionNode(p[1],p[3])


def p_arithmetic_expression_add(p):
    """
    expression : expression '+' expression
    """
    p[0] = AdditionNode(p[1],p[3])

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
