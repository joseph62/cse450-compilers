# Variable class

class Variable:
    def __init__(self,name,data):
        """
        name : string
        data : Data
        """
        if not isinstance(data,Data):
            raise TypeError("data must be of type Data!")
        self._name = name
        self._data = data

    def __str__(self):
        return "{}: {}".format(self._name,self._data)

    __repr__ = __str__

    @property
    def data(self):
        return self._data

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,name):
        self._name = name
