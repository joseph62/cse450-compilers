# Function object

from .variable import *
from .typing import *
from .node import (
        Node,
        ReturnNode,
        UsageNode,
        ValLiteralNode,
        StringLiteralNode,
        CharLiteralNode,
        ResizeMethodNode
        )
from .tracker import Tracker

class Function():
    def __init__(self,name,_type,arguments,node):
        self._name = name
        if not isinstance(_type,Type):
            raise ValueError("_type argument must be of type Type!")
        if not isinstance(arguments,list):
            raise ValueError("arguments argument must be of type list!")
        if not isinstance(node,Node):
            raise ValueError("node argument must be of type Node!")
        tracker = Tracker()
        self._name = name
        self._label = "function_{}_{}".format(name,tracker.varnum)
        self._type = _type
        self._nodes = [node]
        self._arguments = arguments
        var_name = self._type.template.format(tracker.varnum)
        self._return_var = Variable(var_name,Data(var_name,self._type))
        self._return_label = VariableFactory.maketempscalar("val",tracker.varnum)
        self.add_default_return()
        #self._variables_to_save = [self._return_label] + self._arguments
        self._variables_to_save = [self._return_label] + self._arguments

    def add_default_return(self):
        tracker = Tracker()
        temp = None
        node = None
        if self._type.type == TypeEnum.Val:
            temp = VariableFactory.maketempscalar("val",tracker.varnum)
            node = ValLiteralNode("0")
        elif self._type.type == TypeEnum.Char:
            temp = VariableFactory.maketempscalar("char",tracker.varnum)
            node = CharLiteralNode("'0'")
        elif self._type.type == TypeEnum.Array:
            if self._type.subtype.type == TypeEnum.Val:
                temp = VariableFactory.maketempmeta("array","val",tracker.varnum)
                self._nodes.append(ResizeMethodNode(temp,ValLiteralNode("0")))
                node = UsageNode(temp)
            elif self._type.subtype.type == TypeEnum.Char:
                temp = VariableFactory.maketempmeta("array","char",tracker.varnum)
                node = StringLiteralNode("\"\"")
        self._nodes.append(ReturnNode(node))

    @property
    def name(self):
        return self._name

    @property
    def variables_to_save(self):
        return self._variables_to_save

    @property
    def label(self):
        return self._label

    @property
    def type(self):
        return self._type

    @property
    def nodes(self):
        return self._nodes

    @property
    def return_var(self):
        return self._return_var

    @property
    def return_label(self):
        return self._return_label

    @property
    def arguments(self):
        return self._arguments

