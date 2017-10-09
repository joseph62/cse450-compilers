# Name: Sean Joseph
# Tracker will be a singleton that holds counters for variables,
# if tags, while tags, and anything else that needs a global counter.

from symboltable import SymbolTable

# I didn't know how to implement a singleton so I referenced a 
# python design pattern cook book. Python 3 Patterns, Recipes and Idioms <-

class Tracker:
    """
    The Tracker class is a singleton that keeps track of the
    global symbol table and counters for vars, ifs, and whiles.
    """

    class _Tracker:
        def __init__(self):
            self.var_counter = 0
            self.if_counter = 0
            self.while_counter = 0
            self.symbols = SymbolTable()

    instance = None

    def __init__(self):
        if not Tracker.instance:
            Tracker.instance = Tracker._Tracker()

    def get_var_num(self):
        unique_number = Tracker.instance.var_counter 
        Tracker.instance.var_counter += 1 
        return unique_number

    def get_while_num(self):
        unique_number = Tracker.instance.while_counter 
        Tracker.instance.while_counter += 1 
        return unique_number

    def get_if_num(self):
        unique_number = Tracker.instance.if_counter 
        Tracker.instance.if_counter += 1 
        return unique_number

    def get_symbols(self):
        return Tracker.instance.symbols

    def set_symbols(self,symbols):
        Tracker.instance.symbols = symbols


