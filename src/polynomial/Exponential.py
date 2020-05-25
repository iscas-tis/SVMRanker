
from polynomial.Item import Item

class Exponential(Item):

    def __init__(self, base_of_each_var):
        super(Exponential, self).__init__(base_of_each_var)

    def get_value(self, value_of_each_var):  # Get the real value under the case of 'value_of_each_var'.
        result = 1
        for index in range(self.num_of_vars):
            if self.arg_of_each_var[index] != 0:
                result *= self.arg_of_each_var[index] ** value_of_each_var[index]
        return result

    def __str__(self):
        result = ''
        first = True
        for index in range(self.num_of_vars):
            if self.arg_of_each_var[index] != 0:
                pred = '' if first else ' * '
                result += pred + '(' + self.arg_of_each_var[index].__str__() + ' ** ' + ' x[' + index.__str__() + '])'
                first = False
        if len(result) == 0:
            return '1'
        else:
            return result
