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
        raise NotImplementedError("{} does not compile!".format(self.name))

    def execute_good_code(self,output):
        raise NotImplementedError("{} does not execute!".format(self.name))


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
                arr_size = "s{}".format(Tracker().get_var_num())
                track = "s{}".format(Tracker().get_var_num())
                compare = "s{}".format(Tracker().get_var_num())
                temp = "s{}".format(Tracker().get_var_num())
                label_num = Tracker().get_while_num()
                start_label = "start_print_label_{}".format(label_num)
                end_label = "end_print_label_{}".format(label_num)
                output.append("ar_get_size {} {}".format(
                    var.get_value(),arr_size))
                output.append("val_copy 0 {}".format(track))
                output.append("{}:".format(start_label))
                output.append("test_equ {} {} {}".format(
                    arr_size,track,compare))
                output.append("jump_if_n0 {} {}".format(
                    compare,end_label)) 
                output.append("ar_get_idx {} {} {}".format(
                    var.get_value(),track,temp))
                if var.element_type.get_type() == 'char':
                    output.append("out_char {}".format(temp))
                elif var.element_type.get_type() == 'val':
                    output.append("out_val {}".format(temp))
                output.append("add 1 {} {}".format(track,track))
                output.append("jump {}".format(start_label))
                output.append("{}:".format(end_label))
        output.append("out_char '\\n'")
        output.append("#End PrintNode")

    def execute_good_code(self,output):
        outstr = "" 
        for child in self.children:
            var = child.execute_good_code(output)
            value = var.get_value()
                #TODO implement print array
            if var.get_type() == 'array':
                for elem in value:
                    if elem == "\\t":
                        elem = "\t"
                    elif elem == "\\n":
                        elem = "\n"
                    elif elem == "\\\\":
                        elem = "\\"
                    elif elem == "\\'":
                        elem = "'"
                    outstr = outstr + str(elem)
            else:
                if value == "\\t":
                    value = "\t"
                elif value == "\\n":
                    value = "\n"
                elif value == "\\\\":
                    value = "\\"
                elif value == "\\'":
                    value = "'"
                outstr = outstr + str(value)
        outstr = outstr + "\n"
        output.append(outstr) 
        

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

    def execute_good_code(self,output):
        tracker = Tracker()
        temp_var = ValVariable("s{}".format(tracker.get_var_num()))
        fdata = float(self.data)
        idata = int(self.data)
        if fdata == idata:
            temp_var.set_value(idata)
        else:
            temp_var.set_value(fdata)

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

    def execute_good_code(self,output):
        tracker = Tracker()
        temp_var = CharVariable("s{}".format(tracker.get_var_num()))
        value = self.data
        value = list(value)
        value.pop(0)
        value.pop()
        value = "".join(value)
        temp_var.set_value(value)

        return temp_var

class StringLiteralNode(Node):
    """
    StringLiteralNode for easy array definitions
    """
    def __init__(self,data):
        super().__init__(name='StringLiteralNode',data=data)

    def generate_bad_code(self,output):
        tracker = Tracker()
        temp_var = ArrayVariable(
            "a{}".format(tracker.get_var_num()),CharVariable("")
        )
        temp_var.set_value(temp_var.get_name())
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
        output.append("ar_set_size {} {}".format(temp_var.get_value(),arr_size))
        temp = "s{}".format(Tracker().get_var_num())
        for index,character in enumerate(result):
            output.append("val_copy '{}' {}".format(character,temp))
            output.append("ar_set_idx {} {} {}".format(
                temp_var.get_value(),index,temp))
        output.append("# Ending {}".format(self.name))

        return temp_var
        
    def execute_good_code(self,output):
        tracker = Tracker()
        temp_var = ArrayVariable(
            "a{}".format(tracker.get_var_num()),CharVariable("element")
        )
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
        temp_var.set_value(result)

        return temp_var
        
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
            raise TypeError("Arithmetic operator {} invalid!".format(
                self._operator
                ))

    def execute_good_operator(self,left,right):
        if self._operator == '+':
            return left.get_value() + right.get_value()
        elif self._operator == '-':
            return left.get_value() - right.get_value()
        elif self._operator == '/':
            value = left.get_value() / right.get_value()
            ivalue = int(value)
            fvalue = float(value)
            if ivalue == fvalue:
                return ivalue
            return fvalue
        elif self._operator == '*':
            return left.get_value() * right.get_value()
        else:
            raise TypeError("Arithmetic operator {} invalid!".format(
                self._operator
                ))

    def generate_bad_code(self,output):
        tracker = Tracker()
        output.append("#Start {}".format(self.name))
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
        output.append("{} {} {} {}".format(
            self.get_bad_operator(),child1.get_value(),
            child2.get_value(),result_var.get_value()))
        output.append("#End {}".format(self.name))
        return result_var

    def execute_good_code(self,output):
        tracker = Tracker()
        child1 = self.children[0].execute_good_code(output)
        child2 = self.children[1].execute_good_code(output)
        if child1.get_type() != 'val' or child2.get_type() != 'val':
            raise TypeError(
                "Error: cannot use type {} in addition expressions!".format(
                    child1.get_type())) 
        result_var = ValVariable("s{}".format(tracker.get_var_num()))
        result_var.set_value(self.execute_good_operator(child1,child2))
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

    def execute_good_code(self,output):
        tracker = Tracker()
        child = self.children[0].execute_good_code(output)
        if child.get_type() != 'val':
            raise TypeError(
                "Error: cannot use type {} in addition expressions!".format(
                    child.get_type())) 
        result_var = ValVariable("s{}".format(tracker.get_var_num()))
        value = child.get_value()
        result_var.set_value(0 if value == 0 else 1)
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

    def execute_good_code(self,output):
        tracker = Tracker()
        child = self.children[0].execute_good_code(output)
        if child.get_type() != 'val':
            raise TypeError(
                "Error: cannot use type {} in addition expressions!".format(
                    child.get_type())) 
        result_var = ValVariable("s{}".format(tracker.get_var_num()))
        value = child.get_value()
        result_var.set_value( - value )
        return result_var

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

    def execute_good_operator(self,left,right):
        value = False
        if self._operator == '<':
            value = left.get_value() < right.get_value()
        elif self._operator == '>':
            value = left.get_value() > right.get_value()
        elif self._operator == '>=':
            value = left.get_value() >= right.get_value()
        elif self._operator == '<=':
            value = left.get_value() <= right.get_value()
        elif self._operator == '==':
            value = left.get_value() == right.get_value()
        elif self._operator == '!=':
            value = left.get_value() != right.get_value()
        else:
            raise SyntaxError("Comparison operator {} invalid!".format(
                self._operator
                ))
        value = int(value)
        return value

    def generate_bad_code(self,output):
        tracker = Tracker()
        output.append("#Start {}".format(self.name))
        child1 = self.children[0].generate_bad_code(output)
        child2 = self.children[1].generate_bad_code(output)

        if not child1.same_type(child2):
            raise TypeError("Error: Cannot compare a {} and a {}!".format(
                child1.get_type(),child2.get_type()))

        result_var = ValVariable("s{}".format(tracker.get_var_num()))
        result_var.set_value(result_var.get_name())
        output.append("{} {} {} {}".format(
            self.get_bad_operator(),child1.get_value(),
            child2.get_value(),result_var.get_value()))

        output.append("#End {}".format(self.name))
        return result_var

    def execute_good_code(self,output):
        tracker = Tracker()
        child1 = self.children[0].execute_good_code(output)
        child2 = self.children[1].execute_good_code(output)
        if not child1.same_type(child2):
            raise TypeError("Error: Cannot compare a {} and a {}!".format(
                child1.get_type(),child2.get_type()))
        result_var = ValVariable("s{}".format(tracker.get_var_num()))
        result_var.set_value(self.execute_good_operator(child1,child2))
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

    def execute_good_code(self,output):
        tracker = Tracker() 
        child1 = self.children[0].execute_good_code(output)
        if child1.get_type() != 'val':
            raise TypeError(
                    "Cannot use type {} in boolean operation!".format(
                        child1.get_type())) 
        result_var = ValVariable("s{}".format(tracker.get_var_num()))
        result_var.set_value(child1.get_value()) 
        if result_var.get_value() == 0:
            return result_var 
        child2 = self.children[1].generate_bad_code(output)
        if child2.get_type() != 'val':
            raise TypeError(
                    "Cannot use type {} in boolean operation!".format(
                        child1.get_type())) 
        result_var.set_value(child2.get_value())
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


    def execute_good_code(self,output):
        tracker = Tracker() 
        child1 = self.children[0].execute_good_code(output)
        if child1.get_type() != 'val':
            raise TypeError(
                    "Cannot use type {} in boolean operation!".format(
                        child1.get_type())) 
        result_var = ValVariable("s{}".format(tracker.get_var_num()))
        result_var.set_value(child1.get_value()) 
        if result_var.get_value() != 0:
            return result_var 
        child2 = self.children[1].generate_bad_code(output)
        if child2.get_type() != 'val':
            raise TypeError(
                    "Cannot use type {} in boolean operation!".format(
                        child1.get_type())) 
        result_var.set_value(child2.get_value())
        return result_var


class UsageNode(Node):
    """
    UsageNode
    """
    def __init__(self,data):
        super().__init__(name='UsageNode',data=data)
    def generate_bad_code(self,output):
        return self.data

    execute_good_code = generate_bad_code

class ArrayIndexNode(Node):
    """
    ArrayIndexNode
    """
    def __init__(self,data,child):
        super().__init__(name='ArrayIndexNode',data=data,children=[child])

    def generate_bad_code(self,output):
        temp_var_value = "s{}".format(Tracker().get_var_num())
        output.append("#Start {}".format(self.name))
        index = self.children[0].generate_bad_code(output)
        if index.get_type() != "val":
            raise TypeError("Cannot index array with type {}".format(
                index.get_type()))
        var = ArrayElementVariable(temp_var_value,self.data.element_type.get_type(),
                self.data.get_value(),index)
        var.set_value(var.get_name())
        output.append("ar_get_idx {} {} {}".format(
            self.data.get_value(),index.get_value(),var.get_value()))
        output.append("#End {}".format(self.name))
        return var

    def execute_good_code(self,output):
        temp_var_value = "s{}".format(Tracker().get_var_num())
        index = self.children[0].execute_good_code(output)

        if index.get_type() != "val":
            raise TypeError("Cannot index array with type {}".format(
                index.get_type()))
        var = ArrayElementVariable(
                temp_var_value,
                self.data.element_type.get_type(),
                self.data.get_value(),index)

        var.set_value(self.data.get_value()[index.get_value()])
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
        if not child.same_type(self.data):
            raise TypeError("Error cannot assign type {} to type {}".format(
                child.get_type(),self.data.get_type()))
        if child.get_type() == 'array':
            output.append("ar_copy {} {}".format(
                child.get_value(),self.data.get_value()))
        else:
            output.append("val_copy {} {}".format(
                child.get_value(),self.data.get_value()))
        output.append("#End Assignment")
        return self.data

    def execute_good_code(self,output):
        tracker = Tracker()
        child = self.children[0].execute_good_code(output)
        if not child.same_type(self.data):
            raise TypeError("Error cannot assign type {} to type {}".format(
                child.get_type(),self.data.get_type()))
        if child.get_type() == 'array':
            self.data.set_value(child.get_value().copy())
        else:
            self.data.set_value(child.get_value())
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
        if 'size' not in var.get_methods():
            raise TypeError("SizeMethod {} cannot be invoked on a {}".format(
                method,var.get_type()))
        result = ValVariable("s{}".format(Tracker().get_var_num()))
        result.set_value(result.get_name())
        output.append("ar_get_size {} {}".format(
            var.get_value(),result.get_value()))
        output.append("#End SizeMethod")
        return result

    def execute_good_code(self,output):
        var = self.data.execute_good_code(output)
        if 'size' not in var.get_methods():
            raise TypeError("SizeMethod {} cannot be invoked on a {}".format(
                method,var.get_type()))
        result = ValVariable("s{}".format(Tracker().get_var_num()))
        result.set_value(len(var.get_value()))
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
        if 'resize' not in var.get_methods():
            raise TypeError("ResizeMethod {} cannot be invoked on a {}".format(
                method,var.get_type()))
        child = self.children[0].generate_bad_code(output)
        if child.get_type() != 'val':
            raise TypeError("Resize must have expression of type val for an argument")

        output.append("ar_set_size {} {}".format(
            var.get_value(),child.get_value()))
        output.append("#End ReresizeMethod")
        return var

    def execute_good_code(self,output):
        var = self.data.execute_good_code(output) 
        if 'resize' not in var.get_methods():
            raise TypeError("SizeMethod {} cannot be invoked on a {}".format(
                method,var.get_type())) 
        expr = self.children[0].execute_good_code(output)
        if expr.get_type() != 'val':
            raise TypeError("Resize must have expression of type val for an argument") 
        expr = expr.get_value()
        value = var.get_value()
        if isinstance(value,str):
            value = []
        if expr < len(value):
            value = value[:expr]
        elif expr > len(value):
            diff = expr - len(value)
            while diff > 0:
                value.append(0)
                diff -= 1
        var.set_value(value)
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
        if not child1.same_type(child2):
            raise TypeError("Error cannot assign type {} to type {}".format(
                child1.get_type(),child2.get_type()))
        if child1.is_reference():
            output.append("ar_set_idx {} {} {}".format(
                child1.array_name,child1.index.get_value(),child2.get_value()
            ))
        else:
            output.append("val_copy {} {}".format(
                child2.get_value(),child1.get_value()))
        
        output.append("#End Expression Assignment")
        return child1

    def execute_good_code(self,output):
        tracker = Tracker()
        child1 = self.children[0].execute_good_code(output)
        child2 = self.children[1].execute_good_code(output)
        if not child1.same_type(child2):
            raise TypeError("Error cannot assign type {} to type {}".format(
                child1.get_type(),child2.get_type()))
        if child1.is_reference():
            array = child1.array_name
            newvalue = child2.get_value()
            index = child1.index.get_value()
            array[index] = newvalue
            return child2
        else:
            child1.set_value(child2.get_value())
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

    def execute_good_code(self,output):
        for child in self.children:
            child.execute_good_code(output)


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

    def execute_good_code(self,output):
        expression = self.children[0].execute_good_code(output)
        if expression.get_type() != 'val':
            raise TypeError(
                    "Unable to use type {} in if statement!".format(
                        expression.get_type()))
        block = self.children[1] 
        if expression.get_value() != 0:
            block.execute_good_code(output) 
        return None

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

    def execute_good_code(self,output):
        expression = self.children[0].execute_good_code(output)
        if expression.get_type() != 'val':
            raise TypeError(
                    "Unable to use type {} in if statement!".format(
                        expression.get_type()))
        block1 = self.children[1] 
        block2 = self.children[2] 
        if expression.get_value() != 0:
            block1.execute_good_code(output) 
        else:
            block2.execute_good_code(output)
        return None



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

    def execute_good_code(self,output):
        expression = self.children[0]
        block = self.children[1] 

        try:
            expr = expression.execute_good_code(output)
            if expr.get_type() != 'val':
                raise TypeError(
                        "Unable to use type {} in if statement!".format(
                            expression.get_type()))
            while expr.get_value() != 0:
                block.execute_good_code(output)
                expr = expression.execute_good_code(output)
        except Exception:
            pass

class NoOpNode(Node):
    """
    I do nothing!
    """
    def __init__(self):
        super().__init__(name="NoOpNode")

    def generate_bad_code(self,output):
        output.append("# LOL, I don't do anything! I'm a {}.".format(self.name))

    def execute_good_code(self,output):
        pass

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

    def execute_good_code(self,output):
        raise Exception()
