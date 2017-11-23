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
