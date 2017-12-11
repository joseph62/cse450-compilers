# Data arguments for bad lang

from enum import Enum

class BadDataTypes(Enum):
    Scalar = 0
    Array = 1
    Literal = 2
    Tag = 3

class BadData:
    def __init__(self,value,_type):
        self._value = value
        if not isinstance(_type,BadDataTypes):
            raise Exception("Bad Data Type must be of type BadDataTypes!")
        self._type = _type

    def __str__(self):
        return "{} {}".format(self._type,self._value)

    __repr__ = __str__

    def __hash__(self):
        return hash(self._value)

    @property
    def value(self):
        return self._value

    @property
    def type(self):
        return self._type

