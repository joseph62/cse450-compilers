#Name: Sean Joseph
# Token class definitions

special_words = {
        'val' : 'TYPE',
        'char' : 'TYPE',
        'string' : 'ALIAS_TYPE',
        'array' : 'META_TYPE',
        'print' : 'COMMAND_PRINT',
        'random' : 'COMMAND_RANDOM',
        'break' : 'COMMAND_BREAK',
        'return' : 'COMMAND_RETURN',
        'if' : 'COMMAND_IF',
        'else' : 'COMMAND_ELSE',
        'while' : 'COMMAND_WHILE',
        'define' : 'FUNCTION_DEFINE',
}

tokens = ["ID","VAL_LITERAL","CHAR_LITERAL","STRING_LITERAL",
        "ASSIGN_ADD","ASSIGN_SUB","ASSIGN_MULT",
        "ASSIGN_DIV","COMP_EQU","COMP_NEQU","COMP_LESS",
        "COMP_LTE","COMP_GTR","COMP_GTE","BOOL_AND","BOOL_OR",
        "WHITESPACE","COMMENT"] + list(set(special_words.values()))

literals = "+-*/()={}[].;!,"

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
    r"('\\[\'tn]'|'\\\\'|'.')"
    return t

def t_STRING_LITERAL(t):
    r'"(\\\"|[^"])*"'
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
    raise SyntaxError("Bad token: {}".format(t))
