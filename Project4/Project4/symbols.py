#Name: Sean Joseph

from variable import *

class Table:
    """
    A Table will have a dictionary of key value pairs
    of name and variable object.
    """
    
    def __init__(self):
        self._variables = {}

    def __contains__(self,name):
        return name in self._variables

    def declare_variable(self,var):
        self._variables[var.get_name()] = var

    def deref_variable(self,name):
        return self._variables[name]

    def set_variable(self,name,value):
        self._variables[name].value = value

class SymbolTable:
    def __init__(self):
        self._tables = [Table()]
        self._scope = 0

    def declare_variable(self,var):
        if var.get_name() in self._tables[-1]:
            raise NameError("Variable {} is already declared in scope {}!"
                    .format(var.get_name(),self._scope))
        var.set_scope(self._scope)
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

