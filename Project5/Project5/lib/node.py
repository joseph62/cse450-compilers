#Name: Sean Joseph
#Abstract Syntax Tree

from .tracker import Tracker
from .variable import *

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
            if var.get_type() == 'char':
                output.append("out_char {}".format(var.get_value()))
            elif var.get_type() == 'val':
                output.append("out_val {}".format(var.get_value()))
                #TODO implement print array
            elif var.get_type() == 'array':
                if var.element_type() == 'char':
                    pass
                elif var.element_type() == 'var':
                    pass
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
        temp_var = ValVariable("s{}".format(tracker.get_var_num()))
        temp_var.set_value(temp_var.get_name())
        output.append("val_copy {} {}".format(self.data, temp_var.get_value()))
        return temp_var

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
        temp_var = CharVariable("s{}".format(tracker.get_var_num()))
        temp_var.set_value(temp_var.get_name())
        output.append("val_copy {} {}".format(self.data, temp_var.get_value()))
        return temp_var

class StringLiteralNode(Node):
    """
    StringLiteralNode for easy array definitions
    """
    def __init__(self,data):
        super().__init__(name='StringLiteralNode',data=data)

    def generate_bad_code(self,output):
        tracker = Tracker()
        temp_var = ArrayVariable("a{}".format(tracker.get_var_num()),"char")
        temp_var.set_value(temp_var.get_name())
        characters = list(self.data)

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
        output.append("ar_set_size {} {}".format(temp_var.get_value(),arr_size))

        for index,character in enumerate(result):
            output.append("ar_set_idx {} {} '{}'".format(
                temp_var.get_value(),index,character))

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
        if child1.get_type() == 'char' or child2.get_type() == 'char':
            raise TypeError(
                "Error: cannot use type {} in addition expressions!".format(
                    child1.get_type()))
        if not child1.same_type(child2):
            raise TypeError("Error: Cannot add a {} and a {}!".format(
                child1.get_type(),child2.get_type()))
        result_var = ValVariable("s{}".format(tracker.get_var_num()))
        result_var.set_value(result_var.get_name())
        output.append("add {} {} {}".format(
            child1.get_value(),child2.get_value(),result_var.get_value()))
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

        if child1.get_type() == 'char' or child2.get_type() == 'char':
            raise TypeError(
                "Error: cannot use type {} in addition expressions!".format(
                    child1.get_type()))
        if not child1.same_type(child2):
            raise TypeError("Error: Cannot subtract a {} and a {}!".format(
                child1.get_type(),child2.get_type()))

        result_var = ValVariable("s{}".format(tracker.get_var_num()))
        result_var.set_value(result_var.get_name())
        output.append("sub {} {} {}".format(
            child1.get_value(),child2.get_value(),result_var.get_value()))
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

        if child1.get_type() == 'char' or child2.get_type() == 'char':
            raise TypeError(
                "Error: cannot use type {} in addition expressions!".format(
                    child1.get_type()))
        if not child1.same_type(child2):
            raise TypeError("Error: Cannot divide a {} and a {}!".format(
                child1.get_type(),child2.get_type()))

        result_var = ValVariable("s{}".format(tracker.get_var_num()))
        result_var.set_value(result_var.get_name())
        output.append("div {} {} {}".format(
            child1.get_value(),child2.get_value(),result_var.get_value()))

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

        if child1.get_type() == 'char' or child2.get_type() == 'char':
            raise TypeError(
                "Error: cannot use type {} in addition expressions!".format(
                    child1.get_type()))
        if not child1.same_type(child2):
            raise TypeError("Error: Cannot multiply a {} and a {}!".format(
                child1.get_type(),child2.get_type()))

        result_var = ValVariable("s{}".format(tracker.get_var_num()))
        result_var.set_value(result_var.get_name())
        output.append("mult {} {} {}".format(
            child1.get_value(),child2.get_value(),result_var.get_value()))

        output.append("#End MultiplicationNode")
        return result_var

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
        if child.get_type() == 'char':
            raise TypeError("Error: unable to negate type {}!".format(
                child.get_type()))

        result_var = ValVariable("s{}".format(tracker.get_var_num()))
        result_var.set_value(result_var.get_name())
        output.append("test_equ 0 {} {}".format(
            child.get_value(),result_var.get_value()))
        output.append("#End NotNode")
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
        if child.get_type() == 'char':
            raise TypeError("Error: unable to negate type {}!".format(
                child.get_type()))

        result_var = ValVariable("s{}".format(tracker.get_var_num()))
        result_var.set_value(result_var.get_name())
        output.append("sub 0 {} {}".format(
            child.get_value(),result_var.get_value()))
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

        if not child1.same_type(child2):
            raise TypeError("Error: Cannot compare a {} and a {}!".format(
                child1.get_type(),child2.get_type()))

        result_var = ValVariable("s{}".format(tracker.get_var_num()))
        result_var.set_value(result_var.get_name())
        output.append("test_nequ {} {} {}".format(
            child1.get_value(),child2.get_value(),result_var.get_value()))

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

        if not child1.same_type(child2):
            raise TypeError("Error: Cannot compare a {} and a {}!".format(
                child1.get_type(),child2.get_type()))

        result_var = ValVariable("s{}".format(tracker.get_var_num()))
        result_var.set_value(result_var.get_name())
        output.append("test_gtr {} {} {}".format(
            child1.get_value(),child2.get_value(),result_var.get_value()))

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

        if not child1.same_type(child2):
            raise TypeError("Error: Cannot compare a {} and a {}!".format(
                child1.get_type(),child2.get_type()))

        result_var = ValVariable("s{}".format(tracker.get_var_num()))
        result_var.set_value(result_var.get_name())
        output.append("test_gte {} {} {}".format(
            child1.get_value(),child2.get_value(),result_var.get_value()))

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

        if not child1.same_type(child2):
            raise TypeError("Error: Cannot compare a {} and a {}!".format(
                child1.get_type(),child2.get_type()))

        result_var = ValVariable("s{}".format(tracker.get_var_num()))
        result_var.set_value(result_var.get_name())
        output.append("test_lte {} {} {}".format(
            child1.get_value(),child2.get_value(),result_var.get_value()))

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

        if not child1.same_type(child2):
            raise TypeError("Error: Cannot compare a {} and a {}!".format(
                child1.get_type(),child2.get_type()))

        result_var = ValVariable("s{}".format(tracker.get_var_num()))
        result_var.set_value(result_var.get_name())
        output.append("test_less {} {} {}".format(
            child1.get_value(),child2.get_value(),result_var.get_value()))

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

        if not child1.same_type(child2):
            raise TypeError("Error: Cannot compare a {} and a {}!".format(
                child1.get_type(),child2.get_type()))

        result_var = ValVariable("s{}".format(tracker.get_var_num()))
        result_var.set_value(result_var.get_name())
        output.append("test_equ {} {} {}".format(
            child1.get_value(),child2.get_value(),result_var.get_value()))

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
        if child.get_type() != 'val':
            raise TypeError(
                "Cannot use type {} as an argument to random!".format(
                child.get_type()))
        result_var = ValVariable("s{}".format(tracker.get_var_num()))
        result_var.set_value(result_var.get_name())
        output.append("random {} {}".format(
            child.get_value(),result_var.get_value()))
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
        jump_man = "{}_{}".format(self.name,tracker.get_bool_num())
        child1 = self.children[0].generate_bad_code(output)

        if child1.get_type() != 'val':
            raise TypeError(
                    "Cannot use type {} in boolean operation!".format(
                        child1.get_type()))

        result_var = ValVariable("s{}".format(tracker.get_var_num()))
        result_var.set_value(result_var.get_name())
        output.append("test_nequ 0 {} {}".format(
            child1.get_value(),result_var.get_value()))
        output.append("jump_if_0 {} {}".format(
            result_var.get_value(),jump_man))

        child2 = self.children[1].generate_bad_code(output)
        if child1.get_type() != 'val':
            raise TypeError(
                    "Cannot use type {} in boolean operation!".format(
                        child1.get_type()))

        output.append("test_nequ 0 {} {}".format(
            child2.get_value(),result_var.get_value()))
        output.append("{}: # Jump Tag {}".format(jump_man,self.name))
        output.append("#End BooleanAndNode")
        return result_var

class BooleanOrNode(Node):
    """
    BooleanOrNode
    """
    def __init__(self,child1,child2):
        super().__init__(name='BooleanOrNode',children=[child1,child2])
    def generate_bad_code(self,output):
        tracker = Tracker()
        output.append("#Start BooleanOrNode")
        jump_man = "{}_{}".format(self.name,tracker.get_bool_num())
        child1 = self.children[0].generate_bad_code(output)

        if child1.get_type() != 'val':
            raise TypeError(
                    "Cannot use type {} in boolean operation!".format(
                        child1.get_type()))

        result_var = ValVariable("s{}".format(tracker.get_var_num()))
        result_var.set_value(result_var.get_name())
        output.append("test_nequ 0 {} {}".format(
            child1.get_value(),result_var.get_value()))
        output.append("jump_if_n0 {} {}".format(
            result_var.get_value(),jump_man))

        child2 = self.children[1].generate_bad_code(output)
        if child1.get_type() != 'val':
            raise TypeError(
                    "Cannot use type {} in boolean operation!".format(
                        child1.get_type()))

        output.append("test_nequ 0 {} {}".format(
            child2.get_value(),result_var.get_value()))
        output.append("{}: # Jump Tag {}".format(jump_man,self.name))
        output.append("#End BooleanOrNode")
        return result_var


class UsageNode(Node):
    """
    UsageNode
    """
    def __init__(self,data):
        super().__init__(name='UsageNode',data=data)
    def generate_bad_code(self,output):
        return self.data

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
        if not child.same_type(self.data):
            raise TypeError("Error cannot assign type {} to type {}".format(
                child.get_type(),self.data.get_type()))
        if child.get_type() == 'array':
            output.append("ar_copy {} {}".format(
                child.get_value(),self.data.get_type()))
        else:
            output.append("val_copy {} {}".format(
                child.get_value(),self.data.get_value()))
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
        output.append("val_copy {} {}".format(
            child2.get_value(),child1.get_value()))
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
        jump_man = "if_statement_{}".format(Tracker().get_if_num())
        expression = self.children[0].generate_bad_code(output)
        result_var = ValVariable("s{}".format(Tracker().get_var_num()))
        result_var.set_value(result_var.get_name())

        if expression.get_type() != 'val':
            raise TypeError(
                    "Unable to use type {} in if statement!".format(
                        expression.get_type()))

        output.append("test_nequ 0 {} {}".format(
            expression.get_value(),result_var.get_value()))
        output.append("jump_if_0 {} {}".format(result_var.get_value(),jump_man))
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
        jump_num = Tracker().get_if_num()
        jump_end_if = "if_statement_{}".format(jump_num)
        jump_else = "else_statment_{}".format(jump_num)
        expression = self.children[0].generate_bad_code(output)
        result_var = ValVariable("s{}".format(Tracker().get_var_num()))
        result_var.set_value(result_var.get_name())

        if expression.get_type() != 'val':
            raise TypeError(
                    "Unable to use type {} in if statement!".format(
                        expression.get_type()))

        output.append("test_nequ 0 {} {}".format(
            expression.get_value(),result_var.get_value()))
        output.append("jump_if_0 {} {}".format(result_var.get_value(),jump_else))
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

        while_num = Tracker().get_while_num()

        jump_start = "while_statement_start_{}".format(while_num)
        jump_end = "while_statement_end_{}".format(while_num)
        
        def operation(node):
            if isinstance(node,WhileNode):
                # return true to not iterate over children
                return True
            if isinstance(node,BreakNode):
                # set jump tag for break statements within while
                node.set_tag(jump_end)
            return False 
        self.children[1].do_a_thing(operation)

        output.append("{}: # While start".format(jump_start))
        expression = self.children[0].generate_bad_code(output)
        result_var = ValVariable("s{}".format(Tracker().get_var_num()))
        result_var.set_value(result_var.get_name())
        while expression.get_type() != 'val':
            raise TypeError(
                    "Unable to use type {} in while statement!".format(
                        expression.get_type()))
        output.append("test_nequ 0 {} {}".format(
            expression.get_value(),result_var.get_value()))
        output.append("jump_if_0 {} {}".format(result_var.get_value(),jump_end))
        block = self.children[1].generate_bad_code(output)
        output.append("jump {}".format(jump_start))
        output.append("{}: # While End".format(jump_end))
        output.append("#End {}".format(self.name))

class NoOpNode(Node):
    """
    I do nothing!
    """
    def __init__(self):
        super().__init__(name="NoOpNode")

    def generate_bad_code(self,output):
        output.append("# LOL, I don't do anything! I'm a {}.".format(self.name))

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
        if self.tag is None:
            raise SyntaxError("Cannot break like this!")
        output.append("jump {} # Break".format(self.tag))
