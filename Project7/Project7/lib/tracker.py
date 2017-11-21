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

    def get_bool_num(self):
        unique_number = Tracker.instance.bool_counter 
        Tracker.instance.bool_counter += 1 
        return unique_number 

    def get_var_num(self):
        unique_number = Tracker.instance.var_counter 
        Tracker.instance.var_counter += 1 
        return unique_number

    # Arrays share the same var pool as non meta
    # variables. 
    # I wanted a separate function, but not to
    # duplicate code.
    get_array_num = get_var_num

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
