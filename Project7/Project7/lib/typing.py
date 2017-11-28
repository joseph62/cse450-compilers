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
    def __init__(self,_type,template="s{}",methods=()):
        """
        _type : instance of TypeEnum
        template : Intermediate variable type - string
        """
        if not isinstance(_type,TypeEnum):
            raise TypeError("Type must be of TypeEnum")
        self._type = _type
        self._template = template
        self._methods = methods

    def __str__(self):
        return str(self._type)

    __repr = __str__

    def __eq__(self,other):
        return (isinstance(other,Type) and
                self._type == other._type
                )

    @property
    def methods(self):
        return self._methods

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self,template):
        self._template = template

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
        _subtype : Type
        """
        super().__init__(_type,methods=("resize","size"))
        if not isinstance(_subtype,Type):
            raise TypeError("Subtype must be of Type")
        self._subtype = _subtype
        self.template = "a{}"

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


class TypeFactory:

    type_mapping = {
            "array" : TypeEnum.Array,
            "val" : TypeEnum.Val,
            "char" : TypeEnum.Char,
            }

    @staticmethod
    def make(_type_string):
        if _type_string not in TypeFactory.type_mapping:
            raise ValueError("Type string {} is not valid!".format(_type_string)) 
        enum = TypeFactory.type_mapping[_type_string]
        return Type(enum)

    @staticmethod
    def makemeta(_type_string,_subtype):
        if _type_string not in TypeFactory.type_mapping:
            raise ValueError("Type string {} is not valid!".format(_type_string))
        enum = TypeFactory.type_mapping[_type_string]
        return MetaType(enum,_subtype)



