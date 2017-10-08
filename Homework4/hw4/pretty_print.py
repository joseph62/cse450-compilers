class Node:
    def __init__(self, children=None, data=None):
        self.children = children
        self.data = data
        self.name = "Node"

    def output_structure(self,prefix):
        output =  "{}{}:".format(prefix,self.name)
        if self.children is not None:
            for child in self.children:
                output += "\n" + child.output_structure(prefix + ".")
        return output

class OtherNode(Node):
    def __init__(self):
        self.name = "OtherNode"

    def output_structure(self,prefix):
        output = "{}{}:".format(prefix,self.name)
        return output

class BinaryNode(Node):
    def __init__(self, children):
        super().__init__(children=children)
        self.name = "BinaryNode"


    def output_structure(self,prefix):
        output = "{}{}:".format(prefix,self.name)
        for child in self.children:
            output += "\n" + child.output_structure(prefix + ".")
        return output


class DataNode(Node):
    def __init__(self, data):
        super().__init__(data=data)
        self.name = "DataNode"

    def output_structure(self,prefix):
        output = "{}{} data = {}:".format(prefix,self.name,self.data)
        return output


class ManyNode(Node):
    def __init__(self, children):
        super().__init__(children=children)
        self.name = "ManyNode"

    def output_structure(self,prefix):
        output = "{}{}:".format(prefix,self.name)
        for child in self.children:
            output += "\n" + child.output_structure(prefix + ".")
        return output

def node_to_string(node):
    return node.output_structure("")

if __name__ == '__main__':
    node = Node([])
    print(node_to_string(node))
