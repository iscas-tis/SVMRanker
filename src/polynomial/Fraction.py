'''
Polynomial divided by Polynomial
'''


class Fraction:

    def __init__(self, N, D):
        self.numerator = N
        self.denominator = D

    def get_numerator(self):
        return self.numerator

    def get_denominator(self):
        return self.denominator

    def get_value(self, value_of_each_var):
        # print(self.numerator.GetValue(value_of_each_var))
        # print(self.denominator.GetValue(value_of_each_var))
        return sum(self.numerator.get_value(value_of_each_var)) / sum(self.denominator.get_value(value_of_each_var))

    def __eq__(self, other):
        if self.__class__.__name__ != other.__class__.__name:
            return False
        return self.numerator.__eq__(other.numerator) and self.denominator.__eq__(other.denominator)

    def __hash__(self):
        return hash(str(self.numerator) + str(self.denominator))

    def __str__(self):
        return '(' + self.numerator.__str__() + ') / (' + self.denominator.__str__() + ')'

    def __repr__(self):
        return self.__str__()

    def __le__(self, other):
        lft_str = self.__str__()
        rgt_str = other.__str__()
        return lft_str.__le__(rgt_str)

    def __gt__(self, other):
        lft_str = self.__str__()
        rgt_str = other.__str__()
        return lft_str.__gt__(rgt_str)

    def __ge__(self, other):
        lft_str = self.__str__()
        rgt_str = other.__str__()
        return lft_str.__ge__(rgt_str)


