# Name: Sean Joseph
# SymbolTable class handles scopes and variable declares.

from variable import ValVariable,CharVariable

class Table:
    """
    A Table will have a dictionary of key value pairs
    of name and variable object.
    """
    
    def __init__(self):
        self._variables = {}

    def __contains__(self,name):
        return name in self._variables

    def define_variable(self,var):
        self._variables[var.get_name()] = var

    def deref_variable(self,name):
        return self._variables[name]


class SymbolTable:
    def __init__(self):
        self._tables = [Table()]
        self._scope = 0

    def define_variable(self,var):
        if var.get_name() in self._tables[-1]:
            raise NameError("Variable {} is already defined in scope {}!"
                    .format(var.get_name(),self._scope))
        var.set_scope(self._scope)
        self._tables[-1].define_variable(var)

    def deref_variable(self,name):
        for table in reversed(self._tables):
            if name in table:
                return table.deref_variable(name) 
        raise NameError("Variable {} used before declaration!".format(name))

    def add_scope(self):
        self._tables.append(Table())
        self._scope += 1

    def remove_scope(self):
        self._tables.pop()
        self._scope -= 1

if __name__ == '__main__':

    table = SymbolTable()

    init_variable = ValueVariable('x')
    init_variable.set_value('s1')

    table.define_variable(init_variable)
    variable = table.deref_variable('x')
    print("{} -> {}".format(variable.get_name(),variable.get_value()))

    table.add_scope()

    init_variable = ValueVariable('x')
    init_variable.set_value('s2')
    table.define_variable(init_variable)

    variable = table.deref_variable('x')
    print("{} -> {}".format(variable.get_name(),variable.get_value()))

    table.remove_scope()

    variable = table.deref_variable('x')
    print("{} -> {}".format(variable.get_name(),variable.get_value()))



