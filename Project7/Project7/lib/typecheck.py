# TypeChecker

class TypeEnforcer:
    @staticmethod
    def error_if_is(variable,typecode):
        if variable.data.type.type == typecode:
            raise TypeError("{} is of the wrong type!".format(variable))
        return True

    @staticmethod
    def error_if_is_not(variable,typecode):
        if variable.data.type.type != typecode:
            raise TypeError("{} is of the wrong type!".format(variable))
        return True

    @staticmethod
    def error_if_not_equal(first,second):
        if not first.data.type == second.data.type:
            raise TypeError("{} and {} must have matching types!".format(first,second))
        return True

    @staticmethod
    def is_type(variable,typecode):
        return variable.data.type.type == typecode

    @staticmethod
    def error_if_not_has_method(variable,method):
        if method not in variable.data.type.methods:
            raise TypeError("{} does not have method {}!".format(variable,method))
        return True
