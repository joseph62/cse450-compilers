# Bad lexer for optimization

import ply.lex as lex

literals = ':'

tokens = [
        "COMMAND",
        "TAG",
        "SCALAR_VARIABLE",
        "ARRAY_VARIABLE",
        "VAL_LITERAL",
        "CHAR_LITERAL",
        "COMMENT",
        "NEWLINE",
        ]

commands = [
        "val_copy",
        "add",
        "sub",
        "mult",
        "div",
        "test_less",
        "test_gtr",
        "test_equ",
        "test_nequ",
        "test_gte",
        "test_lte",
        "jump",
        "jump_if_0",
        "jump_if_n0",
        "random",
        "out_val",
        "out_char",
        "nop",
        "push",
        "pop",
        "ar_get_idx",
        "ar_set_idx",
        "ar_get_size",
        "ar_set_size",
        "ar_copy",
        "ar_push",
        "ar_pop",
        ]

def t_NEWLINE(t):
    r"[\n]"
    return t

def t_WHITESPACE(t):
    r"[ \t]+"
    pass

def t_COMMENT(t):
    r"\#.*"
    pass

def t_SCALAR_VARIABLE(t):
    r"s[0-9]+"
    return t

def t_ARRAY_VARIABLE(t):
    r"a[0-9]+"
    return t

def t_VAL_LITERAL(t):
    r"(\.[0-9]+|[0-9]+(\.[0-9]+)?)"
    return t

def t_CHAR_LITERAL(t):
    r"'(\\'|\\\\|\\n|\\t|[^'\\])'"
    return t
    

def t_TAG(t):
    r"[a-zA-Z0-9_]+"
    if t.value in commands:
        t.type = "COMMAND"
    return t

def t_error(t):
    raise Exception("Bad token found! Token: {}".format(t))

