#Name: Sean Joseph
#Abstract Syntax Tree

from tracker import Tracker

class Node:
    """
    AST Node base class
    """
    def __init__(self,name='Node',children=None,data=None):
        self.children = children
        self.data = data
        self.name = name

    def generate_tree(self,prefix):
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

