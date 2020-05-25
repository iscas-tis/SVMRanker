
import numpy as np
from polynomial.Monomial import Monomial

'''
A polynomial is the sum of several monomials.

two fields: 
dimension : the number of monomials in this polynomial  [removed]
poly_map: a map from a monomial to its coefficient
monomials: a sorted list of monomials
'''


class Polynomial:
	'''
	def hhe2(self, ListOfMonomial, ListOfValue):  # ListOfValue is the coefficient of corresponding monomial
		self.Dimension = len(ListOfMonomial)
		self.Monomials = []
		self.poly_map = {}  # store the relation between coefficient and monomial
		for index in range(self.Dimension):
			self.poly_map[ListOfMonomial[index]] = ListOfValue[index]
			self.Monomials.append(ListOfMonomial[index])
		self.Monomials.sort()
	'''
	'''
	constructed from a map from a monomial to a coefficient
	'''
	def __init__(self, dict_of_monos, order_of_monos):
		self.poly_map  = dict_of_monos  # store the relation between coefficient and monomial
		self.monomials = order_of_monos
		# for key in dict_of_monos:
		# 	self.monomials.append(key)
		# self.monomials.sort()
	
	'''
	def hh1(self, NumOfVriable, Dimension, MatrixOfVariable):  # Use the matrix to initialize the poly_map
		self.Dimension = Dimension
		self.poly_map = {}  # store the relation between coefficient and monomial
		self.monomials = []
		for i in range(self.Dimension):
			# initialize a monomial with an array of powers
			# input the i-th monomial
			mon_ = Monomial(MatrixOfVariable[i][:NumOfVriable])
			# get the coefficient of the monomial
			self.poly_map[mon_] = MatrixOfVariable[i][-1]
			self.monomials.append(mon_)
		self.monomials.sort()
	'''
		
	def get_value(self, value_of_vars):  # Get the matrix of the value
		return [key.get_value(value_of_vars) * int(self.poly_map[key]) for key in self.monomials]

	def get_dimension(self):
		return len(self.monomials)
	
	def set_coefficients(self, vec):
		result = {}
		for index in range(self.get_dimension()):
			mono = self.monomials[index]
			result[mono] = vec[index]
		# print(result)
		# print(poly_map(result))
		return Polynomial(result,self.monomials)
	
	'''
	should check whether the monomials are the same first for the following two methods
	currently they should be consistent
	'''
	
	def __sub__(self, other):  # reload the '-' operation
		result = {}
		monos1 = set(self.poly_map.keys())
		monos2 = set(other.poly_map.keys())
		monos = monos1.union(monos2)
		for key in monos:
			if key in monos1 and key in monos2:
				result[key] = self.poly_map[key] - other.poly_map[key]
			elif key in monos1:
				result[key] = self.poly_map[key]
			else :
				result[key] = 0 - other.poly_map[key]
		return Polynomial(result,self.monomials)
	
	def __add__(self, other):  # reload '+' operation
		result = {}
		monos1 = set(self.poly_map.keys())
		monos2 = set(other.poly_map.keys())
		monos = monos1.union(monos2)
		for key in monos:
			if key in monos1 and key in monos2:
				result[key] = self.poly_map[key] + other.poly_map[key]
			elif key in monos1:
				result[key] = self.poly_map[key]
			else:
				result[key] = other.poly_map[key]
		return Polynomial(result,self.monomials)	
	
	def __str__(self):
		result = ''
		first = True
		for key in self.monomials:
			# check whether coefficient is negative
			if self.poly_map[key] == 0:
				continue
			negative = self.poly_map[key] < 0
			# get the string of the coefficient
			coef = ' - ' if negative else ''
			coef = coef + abs(self.poly_map[key]).__str__()
			result += ('' if (first or negative) else ' + ') + coef + ' * ' + key.__str__()
			first = False
		return result

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