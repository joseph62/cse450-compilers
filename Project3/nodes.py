# Name: Sean Joseph
# This is where all of the abstract syntax tree node classes will be defined.

from tracker import Tracker

# Init the singleton tracker
tracker = Tracker()

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

