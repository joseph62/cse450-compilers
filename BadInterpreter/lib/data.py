# Data and Variable classes

class Type:
    """
    Type represents a type for data,variables, and expressions
    """
    def __init__(self,_type):
        """
        _type : the string representation of type
        """
        self._type = _type

    def __str__(self):
        return str(self._type)

    __repr = __str__

    def __eq__(self,other):
        return (isinstance(other,Type) and
                self._type == other._type
                )

class CharType(Type):
    def __init__(self):
        super().__init__("char")


class ValType(Type):
    def __init__(self):
        super().__init__("val")

class ArrayType(Type):
    def __init__(self,elementtype):
        super().__init__("array")
        self._elementtype = elementtype

    def __str__(self):
        return "{}[{}]".format(self._type,
                self._elementtype)

    __repr = __str__

    def __eq__(self,other):
        return (isinstance(other,Type) and
                self._type == other._type and
                self._elementtype == other._elementtype
                )

class Data:
    def __init__(self,value,_type):
        self._value = value
        self._type = _type

    def __str__(self):
        return "({}){}".format(self._type,self._value)

    __repr__ = __str__

    def sametype(self,other):
        return self._type == other._type

class Variable:
    def __init__(self,name,data):
        self._name = name
        self._data = data

    def __str__(self):
        return "{}: {}".format(self._name,self._data)

    __repr__ = __str__
