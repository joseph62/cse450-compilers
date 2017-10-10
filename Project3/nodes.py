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
    def generate_bad_code(output):
        tracker = Tracker()
        temp_var = "s{}".format(tracker.get_var_num())
        output.append("val_copy {} {}".format(self.data, temp_var))

class BlockNode(Node):
    """
    A block node is simply a node with children.
    call the generate code function on the children.
    """
    def __init__(self,children):
        super().__init__(name='BlockNode',children=children)

    def generate_bad_code(output):
        output.append("#{} beginning".format(self.name))
        for child in self.children:
            child.generate_bad_code(output)
        output.append("#{} ending".format(self.name))

