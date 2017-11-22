# Data and Variable classes

from .typing import Type,MetaType

class Data:
    """
    value : any data
    _type : Type
    """
    def __init__(self,value,_type):
        self._value = value
        if not isinstance(_type,Type):
            raise TypeError("Data must have a Type for the type property!")
        self._type = _type

    def __str__(self):
        return "{} -> {}".format(self._value,self._type)

    __repr__ = __str__

    def sametype(self,other):
        return self._type == other._type

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self,value):
        self._value = value
