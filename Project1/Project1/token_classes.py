# A file that defines all of the token 
# class functions

# example implementation from the ply documentation
def t_newline(t):
    r'\n'
    t.lexer.lineno += 1
    t.type = 'WHITESPACE'

def t_WHITESPACE(t):
    r'[ \t]+'
    return None

def t_ID(t):
    r'[a-zA-Z_]+[a-zA-Z0-9\-_]*'
    t.type = special_words.get(t.value,'ID')
    return t

def t_VAL_LITERAL(t):
    r'([0-9]*\.[0-9]+|[0-9]+)'
    return t

def t_CHAR_LITERAL(t):
    r'\'.\''
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

def t_ASCII_CHAR(t):
    r'[\+\-\*/\(\)=,\{\}\[\]\.;]'
    return t

def t_UNKNOWN(t):
    r'.'
    print("Unknown token on line {}: {}".format(t.lexer.lineno,t.value))
    sys.exit(0)
    return t

