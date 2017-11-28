# Function object

from .variable import *
from .typing import *
from .node import Node
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

    @property
    def name(self):
        return self._name

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
