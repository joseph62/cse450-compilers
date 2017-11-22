# Types for good language data

from enum import Enum

class TypeEnum(Enum):
    """
    Enumeration for different types of data
    """
    Char = 1
    Val = 2
    Array = 3

class Type:
    """
    Type represents a type for data,variables, and expressions
    """
    def __init__(self,_type):
        """
        _type : instance of TypeEnum
        """
        if not isinstance(_type,TypeEnum):
            raise TypeError("Type must be of TypeEnum")
        self._type = _type

    def __str__(self):
        return str(self._type)

    __repr = __str__

    def __eq__(self,other):
        return (isinstance(other,Type) and
                self._type == other._type
                )

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self,_type):
        self._type = _type

class MetaType(Type):
    """
    Meta type represents a type that is made up of other types
    """
    def __init__(self,_type,_subtype):
        """
        _type : TypeEnum
        _subtype : TypeEnum
        """
        super().__init__(_type)
        if not isinstance(_subtype,TypeEnum):
            raise TypeError("Subtype must be of TypeEnum")
        self._subtype = _subtype

    def __str__(self):
        return "{}({})".format(self.type,self.subtype)

    __repr = __str__

    def __eq__(self,other):
        return (
                isinstance(other,Type) 
                and self.type == other.type
                and self.subtype == other.subtype
                )

    @property
    def subtype(self):
        return self._subtype

    @subtype.setter
    def subtype(self,_subtype):
        self._subtype = _subtype


