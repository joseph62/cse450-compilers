# Name: Sean Joseph
# This is where all of the abstract syntax tree node classes will be defined.

class Node:
    """
    AST Node base class
    """
    def __init__(self,children=None,data=None):
        self.children = children
        self.data = data

    def generate_bad_code(output):
        raise NotImplementedError()

class ValLiteralNode(Node):
    """
    ValLiteralNode will be bad code that generates Bad code
    for a Val Literal Usage
    """
    def __init__(self,data):
        super().__init__(data=data)

    #TODO: The walls are closing in! Look at the in class examples
    # to divine what needs doing, dunce.
    def generate_bad_code(output,tracker):
        output += "\n#ValLiteral in use!\nval_copy {} {}".format(
                self.data.get_value(),self.data.get_name()
                )
