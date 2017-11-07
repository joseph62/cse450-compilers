# Data and Variable classes

class Data:
    def __init__(self,value,_type):
        self._value = value
        self._type = _type

    def __str__(self):
        return "({}){}".format(self._type,self.value)

    __repr__ = __str__

    def sametype(self,other):
        return self._type == other._type

class CharData(Data):
    def __init__(self,value):
        super().__init__(value,"char")

class ValData(Data):
    def __init__(self,value):
        super().__init__(value,"val")

class ArrayData(Data):
    def __init__(self,value,elementdata):
        super().__init__(value,"array")
        self._elementdata = elementdata

    def __str__(self):
        return "({}[{}]){}".format(self._type,
                    self._elementdata._type,
                    self.value)

    __repr__ = __str__

    def sametype(self,other):
        # Recurse until we hit something that does
        # or doesn't match
        return (super().sametype(other) and 
                self.elementdata.sametype(other.elementdata))

class Variable:
    def __init__(self,name,data):
        self._name = name
        self._data = data

    def __str__(self):
        return "{}: {}".format(self._name,self._data)

    __repr__ = __str__
