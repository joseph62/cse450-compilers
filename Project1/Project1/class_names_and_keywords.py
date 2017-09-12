# A file that contains the definitions of the token
# class names and keywords.

special_words = {
        'val' : 'TYPE',
        'char' : 'TYPE',
        'string' : 'TYPE',
        'print' : 'COMMAND_PRINT',
        'random' : 'COMMAND_RANDOM',
}

tokens = ("TYPE","COMMAND_PRINT","COMMAND_RANDOM",
        "ID","VAL_LITERAL","CHAR_LITERAL","STRING_LITERAL",
        "ASCII_CHAR","ASSIGN_ADD","ASSIGN_SUB","ASSIGN_MULT",
        "ASSIGN_DIV","COMP_EQU","COMP_NEQU","COMP_LESS",
        "COMP_LTE","COMP_GTR","COMP_GTE","BOOL_AND","BOOL_OR",
        "WHITESPACE","COMMENT","UNKNOWN")

