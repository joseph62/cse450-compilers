# Config class to pass around switches and arguments

class Config:
    """
    Config objects should be passed around to
    control functionality of the compiler
    """
    def __init__(self):
        """
        Initialize the Config object with 
        some default values
        """
        self.debug = False
        self.verbose = False
        self.input_filename = ''
        self.output_lexing_information = False
        self.output_filename = 'a.ugly'

