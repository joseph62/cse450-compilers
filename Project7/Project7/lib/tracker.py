#Name: Sean Joseph
#Singleton tracker for global values

from .symbols import SymbolTable


class Tracker:
    """
    The Tracker class is a singleton that keeps track of the
    global symbol table and counters for vars, ifs, functions, and whiles.
    """

    class _Tracker:
        def __init__(self):
            self.var_counter = 1
            self.if_counter = 1
            self.while_counter = 1
            self.bool_counter = 1
            self.function_counter = 1
            self.symbols = SymbolTable()
            self.break_tag_stack = []
            self._active_function = None
            self.functions = SymbolTable()

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
    def functionnum(self):
        unique_number = Tracker.instance.function_counter 
        Tracker.instance.function_counter += 1 
        return unique_number

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
    def functions(self):
        return Tracker.instance.functions

    @functions.setter
    def functions(self,functions):
        Tracker.instance.functions = functions


    @property
    def symbols(self):
        return Tracker.instance.symbols

    @symbols.setter
    def symbols(self,symbols):
        Tracker.instance.symbols = symbols

    @property
    def break_tag(self):
        if len(Tracker.instance.break_tag_stack) == 0:
            raise Exception("Break tag stack empty!")
        return Tracker.instance.break_tag_stack[-1]


    @property
    def break_tags(self):
        return Tracker.instance.break_tag_stack

    @property
    def mode(self):
        if len(Tracker.instance._mode_stack) == 0:
            raise Exception("Mode stack empty!")
        return Tracker.instance._mode_stack[-1]

    @property
    def modes(self):
        return Tracker.instance._mode_stack

    @property
    def active_function(self):
        active_function = Tracker.instance._active_function
        if active_function is None:
            raise Exception("There is no active function!")
        return active_function

    @active_function.setter
    def active_function(self,function):
        #if not isinstance(function,Function):
        #    raise Exception("Active function must be of type Function!")
        Tracker.instance._active_function = function

