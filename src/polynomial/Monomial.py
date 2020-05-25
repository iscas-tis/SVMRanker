'''
two fields:
1. number of variables
2. power of each variable

for example, the monomial x^2 y z over [x, y, z, w] can be represented as follows:
  num_of_vars = 4
  power_of_vars = [2, 1, 1, 0]

currently only support natural powers
'''

from polynomial.Item import Item


class Monomial(Item):

    def __init__(self, power_of_vars):
        super(Monomial, self).__init__(power_of_vars)

    '''
    plugin in the values of the variables
    '''
    def get_value(self, value_of_each_var):  # Get the real value under the case of 'value_of_each_var'.
        result = 1
        for index in range(self.num_of_vars):
            if self.arg_of_each_var[index] != 0:
                # print('getValue', value_of_each_var[index], self.arg_of_each_var[index])
                if self.arg_of_each_var[index] == 1:
                    result *= value_of_each_var[index]
                else:
                    # result *= pow(value_of_each_var[index], int(self.arg_of_each_var[index]))
                    if value_of_each_var[index] ==0:
                        result = 0
                    else:
                        if int(self.arg_of_each_var[index]) < 0:
                            #print(value_of_each_var,self.arg_of_each_var)
                            result *= 1/pow(value_of_each_var[index], -int(self.arg_of_each_var[index]))
                        else:
                            result *= pow(value_of_each_var[index], int(self.arg_of_each_var[index]))
                    #print(result)
        # print(result)
        return result
    #
    # def __eq__(self, other):
    # 	if self.num_of_vars != other.num_of_vars:  # the number of variable should be equal
    # 		return False
    # 	for index in range(self.num_of_vars):
    # 		if self.power_of_vars[index] != other.power_of_vars[index]:  # power of every variable should be equal
    # 			return False
    # 	return True
    #
    # def __hash__(self):
    # 	return hash(str(self.power_of_vars))

    def __str__(self):
        result = ''
        first = True
        for index in range(self.num_of_vars):
            if self.arg_of_each_var[index] != 0:
                pred = '' if first else ' * '
                result += pred + ' x[' + index.__str__() + ']^' + self.arg_of_each_var[index].__str__()
                first = False
        if len(result) == 0:
            return '1'
        else:
            return result
#
# def __repr__(self):
# 	return self.__str__()
#
# def __le__(self, other):
# 	for index in range(self.num_of_vars):
# 		if self.power_of_vars[index] >= other.power_of_vars[index]:
# 			return False
# 	return True
#
# def __gt__(self, other):
# 	for index in range(self.num_of_vars):
# 		if self.power_of_vars[index] <= other.power_of_vars[index]:
# 			return False
# 	return True
#
# def __ge__(self, other):
# 	for index in range(self.num_of_vars):
# 		if self.power_of_vars[index] < other.power_of_vars[index]:
# 			return False
# 	return True
