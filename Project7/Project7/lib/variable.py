# Variable class

from .typing import *
from .data import *

class Variable:
    def __init__(self,name,data):
        """
        name : string
        data : Data
        """
        if not isinstance(data,Data):
            raise TypeError("data must be of type Data!")
        self._name = name
        self._data = data
        self._scope = -1

    def __str__(self):
        return "{}: {}".format(self._name,self._data)

    __repr__ = __str__

    @property
    def is_reference(self):
        return False

    @property
    def type(self):
        return self._data.type

    @property
    def value(self):
        return self._data.value

    @property
    def data(self):
        return self._data

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,name):
        self._name = name

    @property
    def scope(self):
        return self._scope

    @scope.setter
    def scope(self,scope):
        self._scope = scope

class RefVariable(Variable):
    def __init__(self,name,data,source,position):
        super().__init__(name,data)
        self._source = source
        self._position = position

    def __str__(self):
        return "{} Reference of {} at position {}".format(
                super().__str__(),
                self._source,
                self._position
                )
    @property
    def is_reference(self):
        return True

    @property
    def source(self):
        return self._source
    @property
    def position(self):
        return self._position


class VariableFactory:

    @staticmethod
    def maketempscalar(_type_string,substitute):
        """
        Makes a temporary scalar variable that has the same
        name as it's value.
        _type_string : a type string
        substitute : a substitute for data value and name
        """
        _type = TypeFactory.make(_type_string)
        value = _type.template.format(substitute)
        data = Data(value,_type)
        var = Variable(data.value,data)
        return var

    @staticmethod
    def maketempmeta(_type_string,_subtype_string,substitute):
        subtype = TypeFactory.make(_subtype_string)
        _type = TypeFactory.makemeta(_type_string,subtype)
        value = _type.template.format(substitute)
        data = Data(value,_type)
        var = Variable(data.value,data)
        return var
