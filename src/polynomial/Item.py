'''
Item is a monomial or
'''


class Item:

    def __init__(self, arg_of_each_var):
        self.num_of_vars = len(arg_of_each_var)
        self.arg_of_each_var = arg_of_each_var

    def get_value(self, value_of_each_var):  # Get the real value under the case of 'ValueOfEachVariable'.
        pass

    def __eq__(self, other):
        if self.__class__.__name__ != other.__class__.__name__:
            return False
        if self.num_of_vars != other.num_of_vars:  # the number of variable should be equal
            return False
        for index in range(self.num_of_vars):
            if self.arg_of_each_var[index] != other.arg_of_each_var[index]:  # power of every variable should be equal
                return False
        return True

    def __hash__(self):
        return hash(str(self.arg_of_each_var))

    def __str__(self):
        pass

    def __repr__(self):
        return self.__str__()

    def __le__(self, other):
        for index in range(self.num_of_vars):
            if self.arg_of_each_var[index] >= other.arg_of_each_var[index]:
                return False
        return True

    def __gt__(self, other):
        for index in range(self.num_of_vars):
            if self.arg_of_each_var[index] <= other.arg_of_each_var[index]:
                return False
        return True

    def __ge__(self, other):
        for index in range(self.num_of_vars):
            if self.arg_of_each_var[index] < other.arg_of_each_var[index]:
                return False
        return True
