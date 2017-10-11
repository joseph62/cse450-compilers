#! /usr/bin/env python3
import sys
import ply.lex as lex
import ply.yacc as yacc

class Variable:
    """
    The Variable class will hold information about a variable.
    This will include it's name, type, value, and scope.

    _name - The name of the variable
    _data_type - The type of variable
    _scope - The scope the variable is in
    _value - The value of the variable declared
    """
    def __init__(self,name,data_type,value=None,scope=None):
        """
        Variable assignment.
        Nothing exciting.
        Value can be set at a later time
        """
        self._name = name
        self._data_type = data_type
        self._scope = scope
        self._value = value

    def get_name(self):
        return self._name

    def defined(self):
        return self.value is not None

    def get_type(self):
        return self._data_type

    def set_value(self,value):
        self._value = value

    def set_scope(self,scope):
        self._scope = scope

    def get_scope(self):
        return self._scope

    def get_value(self):
        return self._value

    def same_type(self,other):
        """
        other: Variable
        rtype: boolean
        returns true if other is the same type as self.
        """
        return self.get_type() == other.get_type()

class ValVariable(Variable):
    """
    A variable of type value will contain a floating point number.
    """
    def __init__(self,name):
        super().__init__(name,'val')

class CharVariable(Variable):
    """
    A variable of type character will contain a character.
    """
    def __init__(self,name):
        super().__init__(name,'char')

class Table:
    """
    A Table will have a dictionary of key value pairs
    of name and variable object.
    """
    
    def __init__(self):
        self._variables = {}

    def __contains__(self,name):
        return name in self._variables

    def declare_variable(self,var):
        self._variables[var.get_name()] = var

    def deref_variable(self,name):
        return self._variables[name]

    def set_variable(self,name,value):
        self._variables[name].value = value


class SymbolTable:
    def __init__(self):
        self._tables = [Table()]
        self._scope = 0

    def declare_variable(self,var):
        if var.get_name() in self._tables[-1]:
            raise NameError("Variable {} is already declared in scope {}!"
                    .format(var.get_name(),self._scope))
        var.set_scope(self._scope)
        self._tables[-1].declare_variable(var)

    def deref_variable(self,name):
        for table in reversed(self._tables):
            if name in table:
                return table.deref_variable(name) 
        raise NameError("Variable {} used before declaration!".format(name))

    def set_variable(self,name,value):
        for table in reversed(self._tables):
            if name in table:
                table.set_variable(name,value)
                return
        raise NameError("Variable {} used before declaration!".format(name))

    def add_scope(self):
        self._tables.append(Table())
        self._scope += 1

    def remove_scope(self):
        self._tables.pop()
        self._scope -= 1


class Tracker:
    """
    The Tracker class is a singleton that keeps track of the
    global symbol table and counters for vars, ifs, and whiles.
    """

    class _Tracker:
        def __init__(self):
            self.var_counter = 0
            self.if_counter = 0
            self.while_counter = 0
            self.symbols = SymbolTable()

    instance = None

    def __init__(self):
        if not Tracker.instance:
            Tracker.instance = Tracker._Tracker()

    def reset(self):
        Tracker.instance = None

    def get_var_num(self):
        unique_number = Tracker.instance.var_counter 
        Tracker.instance.var_counter += 1 
        return unique_number

    def get_while_num(self):
        unique_number = Tracker.instance.while_counter 
        Tracker.instance.while_counter += 1 
        return unique_number

    def get_if_num(self):
        unique_number = Tracker.instance.if_counter 
        Tracker.instance.if_counter += 1 
        return unique_number

    def get_symbols(self):
        return Tracker.instance.symbols

    def set_symbols(self,symbols):
        Tracker.instance.symbols = symbols

class Node:
    """
    AST Node base class
    """
    def __init__(self,name='Node',children=None,data=None):
        self.children = children
        self.data = data
        self.name = name

    def generate_tree(self,prefix):
        print("{}{}".format(self.name,prefix))
        for child in self.children:
            child.generate_tree("."+prefix)

    def generate_bad_code(self,output):
        raise NotImplementedError()

class PrintNode(Node):
    """
    PrintNode
    """
    def __init__(self,children):
        super().__init__(name="PrintNode",children=children)
    def generate_bad_code(self,output):
        output.append("#Start PrintNode")
        for child in self.children:
            var = child.generate_bad_code(output)
            output.append("out_val {}".format(var))
        output.append("out_char '\\n'")
        output.append("#End PrintNode")

class ValLiteralNode(Node):
    """
    ValLiteralNode will be bad code that generates Bad code
    for a Val Literal Usage
    """
    def __init__(self,data):
        super().__init__(name='ValLiteralNode',data=data)

    #TODO: The walls are closing in! Look at the inclass examples
    # to divine what needs doing, dunce.
    def generate_bad_code(self,output):
        tracker = Tracker()
        temp_var = "s{}".format(tracker.get_var_num())
        output.append("val_copy {} {}".format(self.data, temp_var))
        return temp_var

class AdditionNode(Node):
    """
    AdditionNode
    """
    def __init__(self,child1,child2):
        super().__init__(name='AdditionNode',children=[child1,child2])

    def generate_bad_code(self,output):
        tracker = Tracker()
        output.append("#Start AdditionNode")
        child1 = self.children[0].generate_bad_code(output)
        child2 = self.children[1].generate_bad_code(output)
        result_var = "s{}".format(tracker.get_var_num())
        output.append("add {} {} {}".format(child1,child2,result_var))
        output.append("#End AdditionNode")
        return result_var


class SubtractionNode(Node):
    """
    SubtractionNode
    """
    def __init__(self,child1,child2):
        super().__init__(name='SubtractionNode',children=[child1,child2])

    def generate_bad_code(self,output):
        tracker = Tracker()
        output.append("#Start SubtractionNode")
        child1 = self.children[0].generate_bad_code(output)
        child2 = self.children[1].generate_bad_code(output)
        result_var = "s{}".format(tracker.get_var_num())
        output.append("sub {} {} {}".format(child1,child2,result_var))
        output.append("#End SubtractionNode")
        return result_var


class DivisionNode(Node):
    """
    DivisionNode
    """
    def __init__(self,child1,child2):
        super().__init__(name='DivisionNode',children=[child1,child2])

    def generate_bad_code(self,output):
        tracker = Tracker()
        output.append("#Start DivisionNode")
        child1 = self.children[0].generate_bad_code(output)
        child2 = self.children[1].generate_bad_code(output)
        result_var = "s{}".format(tracker.get_var_num())
        output.append("div {} {} {}".format(child1,child2,result_var))
        output.append("#End DivisionNode")
        return result_var

class MultiplicationNode(Node):
    """
    MultiplicationNode
    """
    def __init__(self,child1,child2):
        super().__init__(name='MultiplicationNode',children=[child1,child2])

    def generate_bad_code(self,output):
        tracker = Tracker()
        output.append("#Start MultiplicationNode")
        child1 = self.children[0].generate_bad_code(output)
        child2 = self.children[1].generate_bad_code(output)
        result_var = "s{}".format(tracker.get_var_num())
        output.append("mult {} {} {}".format(child1,child2,result_var))
        output.append("#End MultiplicationNode")
        return result_var

class NegateNode(Node):
    """
    NegateNode
    """
    def __init__(self,child):
        super().__init__(name='NegateNode',children=[child])

    def generate_bad_code(self,output):
        tracker = Tracker()
        output.append("#Start NegateNode")
        child = self.children[0].generate_bad_code(output)
        result_var = "s{}".format(tracker.get_var_num())
        output.append("sub 0 {} {}".format(child,result_var))
        output.append("#End NegateNode")
        return result_var

class InequalityNode(Node):
    """
    InequalityNode
    """
    def __init__(self,child1,child2):
        super().__init__(name='InequalityNode',children=[child1,child2])

    def generate_bad_code(self,output):
        tracker = Tracker()
        output.append("#Start InequalityNode")
        child1 = self.children[0].generate_bad_code(output)
        child2 = self.children[1].generate_bad_code(output)
        result_var = "s{}".format(tracker.get_var_num())
        output.append("test_nequ {} {} {}".format(child1,child2,result_var))
        output.append("#End InequalityNode")
        return result_var

class GreaterNode(Node):
    """
    GreaterNode
    """
    def __init__(self,child1,child2):
        super().__init__(name='GreaterNode',children=[child1,child2])

    def generate_bad_code(self,output):
        tracker = Tracker()
        output.append("#Start GreaterNode")
        child1 = self.children[0].generate_bad_code(output)
        child2 = self.children[1].generate_bad_code(output)
        result_var = "s{}".format(tracker.get_var_num())
        output.append("test_gtr {} {} {}".format(child1,child2,result_var))
        output.append("#End GreaterNode")
        return result_var


class GreaterEqualNode(Node):
    """
    GreaterEqualNode
    """
    def __init__(self,child1,child2):
        super().__init__(name='GreaterEqualNode',children=[child1,child2])

    def generate_bad_code(self,output):
        tracker = Tracker()
        output.append("#Start GreaterEqualNode")
        child1 = self.children[0].generate_bad_code(output)
        child2 = self.children[1].generate_bad_code(output)
        result_var = "s{}".format(tracker.get_var_num())
        output.append("test_gte {} {} {}".format(child1,child2,result_var))
        output.append("#End GreaterEqualNode")
        return result_var


class LessEqualNode(Node):
    """
    LessEqualNode
    """
    def __init__(self,child1,child2):
        super().__init__(name='LessEqualNode',children=[child1,child2])

    def generate_bad_code(self,output):
        tracker = Tracker()
        output.append("#Start LessEqualNode")
        child1 = self.children[0].generate_bad_code(output)
        child2 = self.children[1].generate_bad_code(output)
        result_var = "s{}".format(tracker.get_var_num())
        output.append("test_lte {} {} {}".format(child1,child2,result_var))
        output.append("#End LessEqualNode")
        return result_var


class LessNode(Node):
    """
    LessNode
    """
    def __init__(self,child1,child2):
        super().__init__(name='LessNode',children=[child1,child2])

    def generate_bad_code(self,output):
        tracker = Tracker()
        output.append("#Start LessNode")
        child1 = self.children[0].generate_bad_code(output)
        child2 = self.children[1].generate_bad_code(output)
        result_var = "s{}".format(tracker.get_var_num())
        output.append("test_less {} {} {}".format(child1,child2,result_var))
        output.append("#End LessNode")
        return result_var


class EqualityNode(Node):
    """
    EqualityNode
    """
    def __init__(self,child1,child2):
        super().__init__(name='EqualityNode',children=[child1,child2])

    def generate_bad_code(self,output):
        tracker = Tracker()
        output.append("#Start EqualityNode")
        child1 = self.children[0].generate_bad_code(output)
        child2 = self.children[1].generate_bad_code(output)
        result_var = "s{}".format(tracker.get_var_num())
        output.append("test_equ {} {} {}".format(child1,child2,result_var))
        output.append("#End EqualityNode")
        return result_var

class RandomNode(Node):
    """
    RandomNode
    """
    def __init__(self,child):
        super().__init__(name='RandomNode',children=[child])
    def generate_bad_code(self,output):
        tracker = Tracker()
        output.append("#Start RandomNode")
        child = self.children[0].generate_bad_code(output)
        result_var = "s{}".format(tracker.get_var_num())
        output.append("random {} {}".format(child,result_var))
        output.append("#End RandomNode")
        return result_var

class BooleanAndNode(Node):
    """
    BooleanAndNode
    """
    def __init__(self,child1,child2):
        super().__init__(name='BooleanAndNode',children=[child1,child2])
    def generate_bad_code(self,output):
        tracker = Tracker()
        output.append("#Start BooleanAndNode")
        child1 = self.children[0].generate_bad_code(output)
        child2 = self.children[1].generate_bad_code(output)
        result_var_1 = "s{}".format(tracker.get_var_num())
        result_var_2 = "s{}".format(tracker.get_var_num())
        result_var_3 = "s{}".format(tracker.get_var_num())
        result_var_final = "s{}".format(tracker.get_var_num())

        output.append("test_nequ 0 {} {}".format(child1,result_var_1))
        output.append("test_nequ 0 {} {}".format(child2,result_var_2))
        output.append("add {} {} {}".format(result_var_1,result_var_2,result_var_3))
        output.append("test_equ 2 {} {}".format(result_var_3,result_var_final))
        output.append("#End BooleanAndNode")
        return result_var_final

class BooleanOrNode(Node):
    """
    BooleanOrNode
    """
    def __init__(self,child1,child2):
        super().__init__(name='BooleanOrNode',children=[child1,child2])
    def generate_bad_code(self,output):
        tracker = Tracker()
        output.append("#Start BooleanOrNode")
        child1 = self.children[0].generate_bad_code(output)
        child2 = self.children[1].generate_bad_code(output)
        result_var_1 = "s{}".format(tracker.get_var_num())
        result_var_2 = "s{}".format(tracker.get_var_num())
        result_var_3 = "s{}".format(tracker.get_var_num())
        result_var_final = "s{}".format(tracker.get_var_num())

        output.append("test_nequ 0 {} {}".format(child1,result_var_1))
        output.append("test_nequ 0 {} {}".format(child2,result_var_2))
        output.append("add {} {} {}".format(result_var_1,result_var_2,result_var_3))
        output.append("test_nequ 0 {} {}".format(result_var_3,result_var_final))
        output.append("#End BooleanOrNode")
        return result_var_final


class UsageNode(Node):
    """
    UsageNode
    """
    def __init__(self,data):
        super().__init__(name='UsageNode',data=data)
    def generate_bad_code(self,output):
        tracker = Tracker()
        result_var = tracker.get_symbols().deref_variable(self.data).get_value()
        return result_var

class AssignmentNode(Node):
    """
    AssignmentNode
    """
    def __init__(self,data,child):
        super().__init__(name='AssignmentNode',data=data,children=[child])
    def generate_bad_code(self,output):
        tracker = Tracker()
        output.append("#Start Assignment")
        child = self.children[0].generate_bad_code(output)
        output.append("val_copy {} {}".format(child,self.data))
        output.append("#End Assignment")
        return self.data

class ExpressionAssignmentNode(Node):
    """
    AssignmentNode
    """
    def __init__(self,child1,child2):
        super().__init__(name='AssignmentNode',children=[child1,child2])
    def generate_bad_code(self,output):
        tracker = Tracker()
        output.append("#Start Expression Assignment")
        child1 = self.children[0].generate_bad_code(output)
        child2 = self.children[1].generate_bad_code(output)
        output.append("val_copy {} {}".format(child2,child1))
        output.append("#End Expression Assignment")
        return child1

class BlockNode(Node):
    """
    A block node is simply a node with children.
    call the generate code function on the children.
    """
    def __init__(self,children):
        super().__init__(name='BlockNode',children=children)

    def generate_bad_code(self,output):
        output.append("#{} beginning".format(self.name))
        for child in self.children:
            child.generate_bad_code(output)
        output.append("#{} ending".format(self.name))


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
        "WHITESPACE","COMMENT"] + list(set(special_words.values()))

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
    r'(\'.\'|\'\\t\'|\'\\\'\'|\'\\n\'|\'\#\')'
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
    raise SyntaxError(t)

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

# YACC RULEZ

def p_program(p):
    """
    program : statements
    """
    p[0] = p[1]

def p_zero_statements(p):
    """
    statements :
    """
    p[0] = BlockNode([])

def p_statements(p):
    """
    statements : statements statement 
    """
    if p[2] is not None:
        p[1].children.append(p[2])
    p[0] = p[1]

def p_statement(p):
    """
    statement : expression ';'
    """
    p[0] = p[1]

def p_declaration_statement(p):
    """
    statement : declaration ';'
            | print_statement ';'
    """
    p[0] = p[1]

def p_print_statement(p):
    """
    print_statement : COMMAND_PRINT '(' non_empty_comma_sep_expr ')'
    """
    p[0] = p[3]


def p_comma_sep_expression_1(p):
    """
    non_empty_comma_sep_expr : expression
    """
    p[0] = PrintNode([p[1]])


def p_comma_sep_expression_many(p):
    """
    non_empty_comma_sep_expr : expression ',' non_empty_comma_sep_expr
    """
    p[3].children.insert(0,p[1])
    p[0] = p[3]

def p_declaration(p):
    """
    declaration : simple_declaration
                | assign_declaration
    """
    p[0] = p[1]

def p_simple_declaration(p):
    """
    simple_declaration : type ID
    """
    var_name = p[2]
    symbols = Tracker().get_symbols()
    variable = ValVariable(var_name)
    variable.set_value("s{}".format(Tracker().get_var_num()))
    symbols.declare_variable(variable)
    Tracker().set_symbols(symbols) 
    p[0] = variable.get_value()

def p_assign_declaration(p):
    """
    assign_declaration : simple_declaration '=' expression
    """
    p[0] = AssignmentNode(p[1],p[3])

def p_var_usage(p):
    """
    var_usage : ID
    """
    p[0] = UsageNode(p[1])

def p_assignment(p):
    """
    expression : var_usage '=' expression
    """
    p[0] = ExpressionAssignmentNode(p[1],p[3])

def p_add_assign(p):
    """
    expression : var_usage ASSIGN_ADD expression
    """
    p[0] = ExpressionAssignmentNode(p[1],AdditionNode(p[1],p[3]))


def p_sub_assign(p):
    """
    expression : var_usage ASSIGN_SUB expression
    """
    p[0] = ExpressionAssignmentNode(p[1],SubtractionNode(p[1],p[3]))


def p_mult_assign(p):
    """
    expression : var_usage ASSIGN_MULT expression
    """
    p[0] = ExpressionAssignmentNode(p[1],MultiplicationNode(p[1],p[3]))


def p_div_assign(p):
    """
    expression : var_usage ASSIGN_DIV expression
    """
    p[0] = ExpressionAssignmentNode(p[1],DivisionNode(p[1],p[3]))


def p_var_usage_value(p):
    """
    expression : var_usage
    """
    p[0] = p[1]

def p_random_call(p):
    """
    expression : COMMAND_RANDOM '(' expression ')'
    """
    p[0] = RandomNode(p[3])

def p_type(p):
    """
    type : TYPE
    """
    p[0] = p[1]

def p_boolean_and(p):
    """
    expression : expression BOOL_AND expression
    """
    p[0] = BooleanAndNode(p[1],p[3])

def p_boolean_or(p):
    """
    expression : expression BOOL_OR expression
    """
    p[0] = BooleanOrNode(p[1],p[3])


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

def p_boolean_expression_equality(p):
    """
    expression : expression COMP_EQU expression
    """
    p[0] = EqualityNode(p[1],p[3])

def p_boolean_expression_inequality(p):
    """
    expression : expression COMP_NEQU expression
    """
    p[0] = InequalityNode(p[1],p[3])

def p_boolean_expression_negation(p):
    """
    expression : '-' expression %prec UNARY_MINUS
    """
    p[0] = NegateNode(p[2])

def p_boolean_expression_less_than(p):
    """
    expression : expression COMP_LESS expression
    """
    p[0] = LessNode(p[1],p[3])

def p_boolean_expression_greater_than(p):
    """
    expression : expression COMP_GTR expression
    """
    p[0] = GreaterNode(p[1],p[3])

def p_boolean_expression_less_than_equal(p):
    """
    expression : expression COMP_LTE expression
    """
    p[0] = LessEqualNode(p[1],p[3])

def p_boolean_expression_greater_than_equal(p):
    """
    expression : expression COMP_GTE expression
    """
    p[0] = GreaterEqualNode(p[1],p[3])

def p_paren_expression(p):
    """
    expression : '(' expression ')'
    """
    p[0] = p[2]

def p_error(p):
    raise SyntaxError(p)

def generate_bad_code_from_string(input_):
    lexer = lex.lex()
    parser = yacc.yacc()
    try:
        program = parser.parse(input_, lexer=lexer)
        output = []
        program.generate_bad_code(output)
    except:
        Tracker().reset()
        raise
    return "\n".join(output) + "\n"

if __name__ == "__main__":
    source = 'a;'
    try:
        result = generate_bad_code_from_string(source)
    except NameError:
        print("1")
    source = 'val x; val x;'
    try:
        result = generate_bad_code_from_string(source)
    except NameError:
        print("2")
    source = 'print();'
    try:
        result = generate_bad_code_from_string(source)
    except SyntaxError:
        print("3")
    source = 'random();'
    try:
        result = generate_bad_code_from_string(source)
    except SyntaxError:
        print("4")
    source = 'val |;'
    try:
        result = generate_bad_code_from_string(source)
    except SyntaxError:
        print("5")
    source = 'val x = $;'
    try:
        result = generate_bad_code_from_string(source)
    except SyntaxError:
        print("6")
