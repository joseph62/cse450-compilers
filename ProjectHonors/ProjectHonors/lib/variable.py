#Name: Sean Joseph
#Variable class

class Variable:
    """
    The Variable class will hold information about a variable.
    This will include it's name, type, value, and scope.

    _name - The name of the variable
    _data_type - The type of variable
    _scope - The scope the variable is in
    _value - The value of the variable declared
    """
    def __init__(self,name,data_type,value=None,scope=None):
        """
        Variable assignment.
        Nothing exciting.
        Value can be set at a later time
        """
        self._name = name
        self._data_type = data_type
        self._scope = scope
        self._value = value
        self._methods = {} #Methods for this variable

    def __str__(self):
        return "{} {} = {} ;scope:{}".format(
                self._data_type,self._name,self._value,self._scope)

    __repr__ = __str__

    def get_name(self):
        return self._name

    def defined(self):
        return self.value is not None

    def get_type(self):
        return self._data_type

    def set_value(self,value):
        self._value = value

    def set_scope(self,scope):
        self._scope = scope

    def set_name(self,name):
        self._name = name

    def get_scope(self):
        return self._scope

    def get_value(self):
        return self._value

    def get_variable_template(self):
        return "s{}"
    
    def is_reference(self):
        return False

    def set_methods(self,methods):
        self._methods = methods

    def get_methods(self):
        return self._methods

    def same_type(self,other):
        """
        other: Variable
        rtype: boolean
        returns true if other is the same type as self.
        """
        return self.get_type() == other.get_type()

class ValVariable(Variable):
    """
    A variable of type value will contain a floating point number.
    """
    def __init__(self,name):
        super().__init__(name,'val')

class CharVariable(Variable):
    """
    A variable of type character will contain a character.
    """
    def __init__(self,name):
        super().__init__(name,'char')

class ArrayElementVariable(Variable):
    """
    A variable that is really just an element of an array
    """
    def __init__(self,name,element_type,array_name,index):
        super().__init__(name,element_type)
        self.array_name = array_name
        self.index = index

    def is_reference(self):
        return True

    def __str__(self):
        return "{} {} = {} ; in {} scope:{}".format(
                self._data_type,self._name,self._value,
                self.array_name,self._scope)

    __repr__ = __str__




class ArrayVariable(Variable):
    def __init__(self,name,element_type):
        super().__init__(name,"array")
        self.element_type  = element_type
        self.set_methods({'size' : 'val' ,'resize' : None})

    def __str__(self):
        return "{}({}) {} = {} ;scope:{}".format(
                self._data_type,self.element_type.get_type(),
                self._name,self._value,self._scope)

    __repr__ = __str__


    def get_element_type(self):
        return self.element_type

    def get_variable_template(self):
        return "a{}"

    def same_type(self,other):
        result = super().same_type(other) 
        result = result and self.element_type.same_type(other.element_type) 
        return result

