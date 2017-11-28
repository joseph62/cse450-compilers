#Name: Sean Joseph
#Abstract Syntax Tree

from .tracker import Tracker
from .variable import *
from .typecheck import TypeEnforcer
from .typing import *
from .variable import *
from .data import *
from .mode import CompilerMode

class Node:
    """
    AST Node base class
    """
    def __init__(self,name='Node',children=None,data=None):
        self.children = children
        self.data = data
        self.name = name

    def do_a_thing(self,operation):
        terminate = operation(self)
        if self.children is not None and not terminate:
            for child in self.children:
                child.do_a_thing(operation)

    def generate_tree(self,prefix=''):
        print("{}{}".format(prefix,self.name))
        if self.children is not None:
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
            if var.data.type.type == TypeEnum.Char:
                output.append("out_char {}".format(var.data.value))
            elif var.data.type.type == TypeEnum.Val:
                output.append("out_val {}".format(var.data.value))
                #TODO implement print array
            elif var.data.type.type == TypeEnum.Array:
                output.append("# Printing an array...")
                arr_size = "s{}".format(Tracker().varnum)
                track = "s{}".format(Tracker().varnum)
                compare = "s{}".format(Tracker().varnum)
                temp = "s{}".format(Tracker().varnum)
                label_num = Tracker().whilenum
                start_label = "start_print_label_{}".format(label_num)
                end_label = "end_print_label_{}".format(label_num) 
                output.append("ar_get_size {} {}".format(var.data.value,arr_size))
                output.append("val_copy 0 {}".format(track))
                output.append("{}:".format(start_label))
                output.append("test_equ {} {} {}".format(arr_size,track,compare))
                output.append("jump_if_n0 {} {}".format(compare,end_label)) 
                output.append("ar_get_idx {} {} {}".format(var.data.value,track,temp))
                if var.data.type.subtype.type == TypeEnum.Char:
                    output.append("out_char {}".format(temp))
                elif var.data.type.subtype.type == TypeEnum.Val:
                    output.append("out_val {}".format(temp))
                output.append("add 1 {} {}".format(track,track))
                output.append("jump {}".format(start_label))
                output.append("{}:".format(end_label))
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
        var = VariableFactory.maketempscalar("val",tracker.varnum)
        output.append("val_copy {} {}".format(self.data, var.data.value))
        return var

class CharLiteralNode(Node):
    """
    CharLiteralNode will be bad code that generates Bad code
    for a Char Literal Usage
    """
    def __init__(self,data):
        super().__init__(name='CharLiteralNode',data=data)

    #TODO: The walls are closing in! Look at the inclass examples
    # to divine what needs doing, dunce.
    def generate_bad_code(self,output):
        tracker = Tracker()
        var = VariableFactory.maketempscalar("char",tracker.varnum)
        output.append("val_copy {} {}".format(self.data, var.data.value))
        return var

class StringLiteralNode(Node):
    """
    StringLiteralNode for easy array definitions
    """
    def __init__(self,data):
        super().__init__(name='StringLiteralNode',data=data)

    def generate_bad_code(self,output):
        tracker = Tracker()
        var = VariableFactory.maketempmeta("array","char",tracker.varnum)

        characters = list(self.data)
        characters.pop(0)
        characters.pop()
        result = []
        while len(characters)>0:
            character = characters.pop(0)
            if character == "\\":
                escape = characters.pop(0)
                if escape == "\"":
                    result.append("\"")
                else:
                    result.append(character + escape)
            elif character == "'":
                result.append("\\'")
            else:
                result.append(character)

        arr_size = len(result)
        output.append("# Starting {}".format(self.name))
        output.append("ar_set_size {} {}".format(var.data.value,arr_size))
        temp = var.data.type.subtype.template.format(tracker.varnum)
        for index,character in enumerate(result):
            output.append("val_copy '{}' {}".format(character,temp))
            output.append("ar_set_idx {} {} {}".format(
                var.data.value,index,temp))
        output.append("# Ending {}".format(self.name)) 
        return var
        
class ArithmeticNode(Node):
    """
    ArithmeticNode : +-/*
    """
    def __init__(self,operator,child1,child2):
        self._operator = operator
        super().__init__(name='ArithmeticNode',children=[child1,child2])

    def get_bad_operator(self):
        if self._operator == '+':
            return 'add'
        elif self._operator == '-':
            return 'sub'
        elif self._operator == '/':
            return 'div'
        elif self._operator == '*':
            return 'mult'
        else:
            raise TypeError(
                    "Arithmetic operator {} invalid!".format(
                        self._operator
                        )
                )

    def generate_bad_code(self,output):
        tracker = Tracker()
        output.append("#Start {}".format(self.name))
        child1 = self.children[0].generate_bad_code(output)
        child2 = self.children[1].generate_bad_code(output)
        TypeEnforcer.error_if_is_not(child1,TypeEnum.Val)
        TypeEnforcer.error_if_is_not(child2,TypeEnum.Val)
        var = VariableFactory.maketempscalar("val",tracker.varnum)
        output.append(
                        "{} {} {} {}".format(
                    self.get_bad_operator(),
                    child1.data.value,
                    child2.data.value,
                    var.data.value
                    )
                )
        output.append("#End {}".format(self.name))
        return var

class NotNode(Node):
    """
    NotNode
    """
    def __init__(self,child):
        super().__init__(name='NotNode',children=[child])

    def generate_bad_code(self,output):
        tracker = Tracker()
        output.append("#Start NotNode")
        child = self.children[0].generate_bad_code(output)
        TypeEnforcer.error_if_is_not(child,TypeEnum.Val)
        var = VariableFactory.maketempscalar("val",tracker.varnum)
        output.append("test_equ 0 {} {}".format(child.data.value,var.data.value))
        output.append("#End NotNode")
        return var

class ComparisonNode(Node):
    """
    ComparisonNode : +-/*
    """
    def __init__(self,operator,child1,child2):
        self._operator = operator
        super().__init__(name='ComparisonNode',children=[child1,child2])

    def get_bad_operator(self):
        if self._operator == '<':
            return 'test_less'
        elif self._operator == '>':
            return 'test_gtr'
        elif self._operator == '>=':
            return 'test_gte'
        elif self._operator == '<=':
            return 'test_lte'
        elif self._operator == '==':
            return 'test_equ'
        elif self._operator == '!=':
            return 'test_nequ'
        else:
            raise SyntaxError("Comparison operator {} invalid!".format(
                self._operator
                ))

    def generate_bad_code(self,output):
        tracker = Tracker()
        output.append("#Start {}".format(self.name))
        child1 = self.children[0].generate_bad_code(output)
        child2 = self.children[1].generate_bad_code(output)
        TypeEnforcer.error_if_not_equal(child1,child2)
        var = VariableFactory.maketempscalar("val",tracker.varnum)
        output.append("{} {} {} {}".format(
                    self.get_bad_operator(),
                    child1.data.value,
                    child2.data.value,
                    var.data.value
                    )
                )

        output.append("#End {}".format(self.name))
        return var

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
        TypeEnforcer.error_if_is_not(child,TypeEnum.Val)
        var = VariableFactory.maketempscalar("val",tracker.varnum)
        output.append("random {} {}".format(child.data.value,var.data.value))
        output.append("#End RandomNode")
        return var

class BooleanAndNode(Node):
    """
    BooleanAndNode
    """
    def __init__(self,child1,child2):
        super().__init__(name='BooleanAndNode',children=[child1,child2])
    def generate_bad_code(self,output):
        tracker = Tracker()
        output.append("#Start BooleanAndNode")
        jump_man = "{}_{}".format(self.name,tracker.boolnum)
        child1 = self.children[0].generate_bad_code(output)
        TypeEnforcer.error_if_is_not(child1,TypeEnum.Val)
        var = VariableFactory.maketempscalar("val",tracker.varnum)
        output.append("test_nequ 0 {} {}".format(child1.data.value,var.data.value))
        output.append("jump_if_0 {} {}".format(var.data.value,jump_man)) 
        child2 = self.children[1].generate_bad_code(output)
        TypeEnforcer.error_if_is_not(child2,TypeEnum.Val)
        output.append("test_nequ 0 {} {}".format(child2.data.value,var.data.value))
        output.append("{}: # Jump Tag {}".format(jump_man,self.name))
        output.append("#End BooleanAndNode")
        return var

class BooleanOrNode(Node):
    """
    BooleanOrNode
    """
    def __init__(self,child1,child2):
        super().__init__(name='BooleanOrNode',children=[child1,child2])
    def generate_bad_code(self,output):
        tracker = Tracker()
        output.append("#Start BooleanOrNode")
        jump_man = "{}_{}".format(self.name,tracker.boolnum)
        var = VariableFactory.maketempscalar("val",tracker.varnum)
        child1 = self.children[0].generate_bad_code(output)
        TypeEnforcer.error_if_is_not(child1,TypeEnum.Val)
        output.append("test_nequ 0 {} {}".format(child1.data.value,var.data.value))
        output.append("jump_if_n0 {} {}".format(var.data.value,jump_man))
        child2 = self.children[1].generate_bad_code(output)
        TypeEnforcer.error_if_is_not(child2,TypeEnum.Val)
        output.append("test_nequ 0 {} {}".format(child2.data.value,var.data.value))
        output.append("{}: # Jump Tag {}".format(jump_man,self.name))
        output.append("#End BooleanOrNode")
        return var

class UsageNode(Node):
    """
    UsageNode
    """
    def __init__(self,data):
        super().__init__(name='UsageNode',data=data)
    def generate_bad_code(self,output):
        output.append("#{} for {}".format(self.name,self.data))
        return self.data

class ArrayIndexNode(Node):
    """
    ArrayIndexNode
    """
    def __init__(self,data,child):
        super().__init__(name='ArrayIndexNode',data=data,children=[child])
    def generate_bad_code(self,output):
        temp_var_value = "s{}".format(Tracker().varnum)
        output.append("#Start {}".format(self.name))
        position = self.children[0].generate_bad_code(output)
        TypeEnforcer.error_if_is_not(position,TypeEnum.Val)
        # This code is a common pattern. Try refactoring into another function
        _type = self.data.data.type.subtype
        data = Data(temp_var_value,_type)
        var = RefVariable(data.value,data,self.data,position)
        output.append(
                    "ar_get_idx {} {} {}".format(
                    var.source.data.value,
                    var.position.data.value,
                    var.data.value
                    )
            )
        output.append("#End {}".format(self.name))
        return var

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
        TypeEnforcer.error_if_not_equal(child,self.data)
        if TypeEnforcer.is_type(child,TypeEnum.Array):
            output.append("ar_copy {} {}".format(child.data.value,self.data.data.value))
        else:
            output.append("val_copy {} {}".format(child.data.value,self.data.data.value))
        output.append("#End Assignment")
        return self.data

class SizeMethodNode(Node):
    """
    SizeMethodNode
    """
    def __init__(self,data):
        super().__init__(name='SizeMethodNode',data=data)

    def generate_bad_code(self,output):
        output.append("#Start SizeMethod")
        var = self.data.generate_bad_code(output)
        TypeEnforcer.error_if_not_has_method(var,'size')
        result = VariableFactory.maketempscalar("val",Tracker().varnum)
        output.append("ar_get_size {} {}".format(var.data.value,result.data.value))
        output.append("#End SizeMethod")
        return result

class ResizeMethodNode(Node):
    """
    ResizeMethodNode
    """
    def __init__(self,data,expression):
        super().__init__(name='ResizeMethodNode',data=data,children=[expression])

    def generate_bad_code(self,output):
        output.append("#Start ResizeMethod")
        var = self.data.generate_bad_code(output)
        TypeEnforcer.error_if_not_has_method(var,'resize')
        child = self.children[0].generate_bad_code(output)
        TypeEnforcer.error_if_is_not(child,TypeEnum.Val)
        output.append("ar_set_size {} {}".format(
            var.data.value,child.data.value))
        output.append("#End ResizeMethod")
        return var

class ExpressionAssignmentNode(Node):
    """
    ExpressionAssignmentNode
    """
    def __init__(self,child1,child2):
        super().__init__(name='ExpressionAssignmentNode',children=[child1,child2])
    def generate_bad_code(self,output):
        tracker = Tracker()
        output.append("#Start Expression Assignment")
        child1 = self.children[0].generate_bad_code(output)
        child2 = self.children[1].generate_bad_code(output)
        TypeEnforcer.error_if_not_equal(child1,child2)
        if child1.is_reference:
            output.append(
                    "ar_set_idx {} {} {}".format(
                    child1.source.data.value,
                    child1.position.data.value,
                    child2.data.value
                    )
                )
        elif TypeEnforcer.is_type(child2,TypeEnum.Array):
            output.append("ar_copy {} {}".format(child2.data.value,child1.data.value)) 
        else:
            output.append("val_copy {} {}".format(child2.data.value,child1.data.value)) 
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

class IfNode(Node):
    """
    A node to compile an if statement.
    """
    def __init__(self,expression,block):
        super().__init__(name="IfNode",children=[expression,block])

    def generate_bad_code(self,output):
        output.append("#Start {}".format(self.name))
        jump_man = "if_statement_{}".format(Tracker().ifnum)
        expression = self.children[0].generate_bad_code(output)
        var = VariableFactory("val",Tracker().varnum)
        TypeEnforcer.error_if_is_not(expression,TypeEnum.Val)
        output.append("test_nequ 0 {} {}".format(expression.data.value,var.data.value))
        output.append("jump_if_0 {} {}".format(var.data.value,jump_man))
        block = self.children[1].generate_bad_code(output)
        output.append("{}: # Jump If".format(jump_man))
        output.append("#End {}".format(self.name))

class IfElseNode(Node):
    """
    A node to compile an if statement.
    """
    def __init__(self,expression,block_if,block_else):
        super().__init__(name="IfNode",children=[expression,block_if,block_else])

    def generate_bad_code(self,output):
        output.append("#Start {}".format(self.name))
        jump_num = Tracker().ifnum
        jump_end_if = "if_statement_{}".format(jump_num)
        jump_else = "else_statment_{}".format(jump_num)
        expression = self.children[0].generate_bad_code(output)
        var = VariableFactory("val",Tracker().varnum)
        TypeEnforcer.error_if_is_not(expression,TypeEnum.Val)
        output.append("test_nequ 0 {} {}".format(expression.data.value,var.data.value))
        output.append("jump_if_0 {} {}".format(var.data.value,jump_else))
        block_if = self.children[1].generate_bad_code(output)
        output.append("jump {}".format(jump_end_if))
        output.append("{}: # Jump Else".format(jump_else))
        block_else = self.children[2].generate_bad_code(output)
        output.append("{}: # Jump If".format(jump_end_if))
        output.append("#End {}".format(self.name))


class WhileNode(Node):
    """
    A node to compile an while statement.
    """
    def __init__(self,expression,block):
        super().__init__(name="WhileNode",children=[expression,block])

    def generate_bad_code(self,output):
        output.append("#Start {}".format(self.name))
        while_num = Tracker().whilenum
        jump_start = "while_statement_start_{}".format(while_num)
        jump_end = "while_statement_end_{}".format(while_num)
        tracker = Tracker()
        tracker.break_tags.append(jump_end)
        output.append("{}: # While start".format(jump_start))
        expression = self.children[0].generate_bad_code(output)
        var = VariableFactory.maketempscalar("val",Tracker().varnum)
        TypeEnforcer.error_if_is_not(expression,TypeEnum.Val)
        output.append("test_nequ 0 {} {}".format(expression.data.value,var.data.value))
        output.append("jump_if_0 {} {}".format(var.data.value,jump_end))
        block = self.children[1].generate_bad_code(output)
        output.append("jump {}".format(jump_start))
        output.append("{}: # While End".format(jump_end))
        output.append("#End {}".format(self.name))
        tracker.break_tags.pop()

class NoOpNode(Node):
    """
    I do nothing!
    """
    def __init__(self):
        super().__init__(name="NoOpNode")

    def generate_bad_code(self,output):
        output.append("# LOL, I don't do anything! I'm a {}.".format(self.name))

class ReturnNode(Node):
    """
    ReturnNode
    """
    def __init__(self,retexpression):
        super().__init__(name="ReturnNode",children=[retexpression])

    def generate_bad_code(self,output):
        tracker = Tracker()
        function = tracker.active_function
        retexpression = self.children[0].generate_bad_code(output)
        if not function.type == retexpression.data.type:
            raise TypeError("Return statement needs type {} not type {}!".format(function.type,retexpression.data.type))
        if retexpression.data.type.type == TypeEnum.Array:
            output.append("ar_copy {} {}".format(retexpression.data.value,function.return_var.data.value))
        else:
            output.append("val_copy {} {}".format(retexpression.data.value,function.return_var.data.value))
        output.append("jump {} # Return!".format(function.return_label.data.value))


class BreakNode(Node):
    """
    BreakNode
    """
    def __init__(self):
        super().__init__(name="BreakNode")
        self.tag = None
    def set_tag(self,tag):
        self.tag = tag
    def generate_bad_code(self,output):
        tracker = Tracker()
        output.append("jump {} # Break".format(tracker.break_tag))
