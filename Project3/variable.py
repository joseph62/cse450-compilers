# Name: Sean Joseph
# Variable models information for a variable in the Good language

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

    def get_scope(self):
        return self._scope

    def get_value(self):
        return self._value

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

if __name__ == '__main__':
    val_var1 = ValVariable('x')
    char_var1 = CharVariable('y')
    if not val_var1.same_type(char_var1):
        print("A value is not the same as a character!")
    else:
        print("Something has gone horribly wrong!")

    val_var2 = ValVariable('z')
    char_var2 = CharVariable('kekistan')

    if val_var1.same_type(val_var2):
        print("A value is the same type as a value!")
    else:
        print("Everday we stray further from God's light")

    if char_var1.same_type(char_var2):
        print("A char is the same type as a char!")
    else:
        print("The Empire did nothing wrong.")
