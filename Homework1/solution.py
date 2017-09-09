#Name: Sean Joseph

import re
import ply.lex as lex
from sys import stdin

# Question 1
def chemical_check(input_string):
    expression = re.compile(
            r"^[a-zA-Z]+[a-zA-Z0-9]*$"
            )

    return expression.match(input_string) is not None


# Question 2

tokens = ('NOUN','VERB','PUNCTUATION','UNKNOWN','WHITESPACE')

def t_PUNCTUATION(t):
    r'!'
    return t

def t_NOUN(t):
    r'(cat|ferret|dog|human|MSU|Daenerys|Ghost|Josh|you)'
    return t

def t_VERB(t):
    r'(is|chases|loves)'
    return t

def t_UNKNOWN(t):
    r'[a-zA-Z0-9]+'
    return t

def t_WHITESPACE(t):
    r'[ \n\t]'
    return None

lexer = lex.lex()
input_str = stdin.read()
lexer.input(input_str)

while True:
    tok = lexer.token()
    if not tok:
        break # all done
    print("{} ({})".format(tok.type,tok.value))
            
