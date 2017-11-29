# TypeChecker

class TypeEnforcer:
    @staticmethod
    def error_if_is(variable,typecode):
        if variable.type.type == typecode:
            raise TypeError("{} is of the wrong type!".format(variable))
        return True

    @staticmethod
    def error_if_is_not(variable,typecode):
        if variable.type.type != typecode:
            raise TypeError("{} is of the wrong type!".format(variable))
        return True

    @staticmethod
    def error_if_not_equal(first,second):
        if not first.type == second.type:
            raise TypeError("{} and {} must have matching types!".format(first,second))
        return True

    @staticmethod
    def is_type(variable,typecode):
        return variable.type.type == typecode

    @staticmethod
    def error_if_not_has_method(variable,method):
        if method not in variable.type.methods:
            raise TypeError("{} does not have method {}!".format(variable,method))
        return True
