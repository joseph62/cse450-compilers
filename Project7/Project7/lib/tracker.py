#Name: Sean Joseph
#Singleton tracker for global values

from .symbols import SymbolTable

class Tracker:
    """
    The Tracker class is a singleton that keeps track of the
    global symbol table and counters for vars, ifs, and whiles.
    """

    class _Tracker:
        def __init__(self):
            self.var_counter = 1
            self.if_counter = 1
            self.while_counter = 1
            self.bool_counter = 1
            self.symbols = SymbolTable()

    instance = None

    def __init__(self):
        if not Tracker.instance:
            Tracker.instance = Tracker._Tracker()

    def reset(self):
        Tracker.instance = None

    @property
    def boolnum(self):
        unique_number = Tracker.instance.var_counter 
        Tracker.instance.var_counter += 1 
        return unique_number

    @property
    def varnum(self):
        unique_number = Tracker.instance.var_counter 
        Tracker.instance.var_counter += 1 
        return unique_number

    @property
    def arraynum(self):
        return self.varnum

    @property
    def whilenum(self):
        unique_number = Tracker.instance.while_counter 
        Tracker.instance.while_counter += 1 
        return unique_number

    @property
    def ifnum(self):
        unique_number = Tracker.instance.if_counter 
        Tracker.instance.if_counter += 1 
        return unique_number

    @property
    def symbols(self):
        return Tracker.instance.symbols

    @symbols.setter
    def symbols(self,symbols):
        Tracker.instance.symbols = symbols
