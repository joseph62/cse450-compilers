#Name: Sean Joseph

from .variable import *

class Table:
    """
    A Table will have a dictionary of key value pairs
    of name and variable object.
    """
    
    def __init__(self):
        self._variables = {}

    def __str__(self):
        return str(self._variables)

    __repr__ = __str__

    def __contains__(self,name):
        return name in self._variables

    def declare_variable(self,var):
        self._variables[var.name] = var

    def deref_variable(self,name):
        return self._variables[name]

    def set_variable(self,name,value):
        self._variables[name].value = value
        
    def get_variables(self):
        return self._variables.values()

class SymbolTable:
    def __init__(self):
        self._tables = [Table()]
        self._scope = 0

    def __str__(self):
        output = str(self._tables)
        return output
    
    __repr__ = __str__

    def declare_variable(self,var):
        if var.name in self._tables[-1]:
            raise NameError("Variable {} is already declared in scope {}!"
                    .format(var.name,self._scope))
        var.scope = self._scope
        self._tables[-1].declare_variable(var)

    def deref_variable(self,name):
        for table in reversed(self._tables):
            if name in table:
                return table.deref_variable(name) 
        raise NameError("Variable {} used before declaration!".format(name))

    def set_variable(self,name,value):
        for table in reversed(self._tables):
            if name in table:
                table.set_variable(name,value)
                return
        raise NameError("Variable {} used before declaration!".format(name))

    def add_scope(self):
        self._tables.append(Table())
        self._scope += 1

    def remove_scope(self):
        self._tables.pop()
        self._scope -= 1

    def is_global_scope(self):
        return self._scope == 0

    def get_all_variables(self):
        result = []
        for table in self._tables:
            result += table.get_variables()
        return result

