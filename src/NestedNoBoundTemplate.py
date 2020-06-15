import numpy as np
import z3
import fractions as Frac
import math
import signal
import time
from FindMultiphaseUtil import *

'''
nested ranking function <f_1, f_2, ..., f_k>; this is a template used to find functions f_1, ..., f_k
Let f_i = a^T_i U_i(x) for every  1 <= i <= k such that for a list positive numbers {C_1, C_2, ..., C_n} and a number delta

a^T_1 ( U_1(x) - U_1(x')) >= C_1
a^T_2 ( U_2(x) - U_2(x')) + a^T_1 U_1(x)  >= C_2
...
a^T_k ( U_k(x) - U_k(x')) + a^T_{k-1} U_{k-1}(x)  >= C_k

@author Xuechao Sun, Yong Li, Xie Li

'''
class TimeOutException(Exception):
	pass
def z3_verify_fail():
	raise Exception('RUNTIME')
	return False,None
def set_timeout(num, callback):
	def wrape(func):
		def handle(signum, frame): 
			raise TimeOutException

		def toDo(*args, **kwargs):
			try:
				signal.signal(signal.SIGINT, handle)  
				signal.alarm(num)  
				#print('start alarm signal.')
				r = func(*args, **kwargs)
				#print('close alarm signal.')
				signal.alarm(0)  
				return r
			except TimeOutException as e:
			 	callback()

		return toDo

	return wrape

class NestedNoBoundTemplate:

	def __init__(self, list_of_Ux, list_of_C, l):  # list_of_Ux: k U_x, list_of_C: C_i
		self.K = len(list_of_Ux)
		self.list_of_Ux = list_of_Ux
		self.list_of_C = list_of_C
		# Ux is a polynomial and dimension is the number of monomials
		self.dimension = [x.get_dimension() for x in list_of_Ux]  # calculate dimension  of each U_x
		self.list_of_Gx = []
		self.__generate_gx_list_no_bound()
		self.num_of_pos_data = 0
		self.num_of_neg_data = 1
		self.coefficients = None
		self.sample_points_list = []
		self.last_coef_array = l
		self.print_coef = []

	def get_zero_vec(self):
		return np.zeros(np.sum(self.dimension))

	'''
	G_1(x) = (0, 0, ..., U_1(x) - U_1(x'))^T
	G_2(x) = (0, ..., 0, U_2(x) - U_2(x'), U_1(x))^T
	...
	G_k(x) = (U_k(x) - U_k(x'), U_{k-1}(x), 0, ..., 0)^T
	#G_{k+1}(x) = (U_k(x), 0, ..., 0)^T
	
	a^T = (a^T_k, a^T_{k-1}, ..., a^T_2, a^T_1)^T
	'''

	def __generate_gx_list_no_bound(self):  # Generate G_x by U_x, G_x is a lambda expression
		'''
		(0, 0, ..., 0, U_1(x') - U_1(x))^T
		there are K-1 0-vector in the front
		'''
		self.list_of_Gx.append(  # x is the list of variables, x_ is primed x.
			lambda x, x_: np.concatenate(
				(
					np.zeros(int(np.sum(self.dimension[1:]))).astype(int),
					np.array(self.list_of_Ux[0].get_value(x)) - np.array(self.list_of_Ux[0].get_value(x_))
				)
			)
		)
		'''
		i and i-1
		(0, 0, ..., 0, U_i(x) - U_i(x'))^T, U_{i-1}(x), 0, ..., 0)^T
		i-2 consecutive 0 vector in the end
		'''
		for index in range(self.K - 1):
			'''
			there are index - 1 0-vector in the end
			'''
			#pre_zeros = 0 if index == 0 else int(np.sum(self.dimension[0:index]))
			'''
			i, i + 1 -> -U_{i-1}(x) and U_{i}(x')-U_{i}(x) 
			>= i + 2, 0-vector
			'''
			#aft_zeros = 0 if index + 2 == self.K else int(np.sum(self.dimension[(index + 2):self.K]))
			#print(index, pre_zeros, aft_zeros)
			self.list_of_Gx.append(
				lambda x, x_,index = index: np.concatenate(
					(
						np.zeros(0 if index + 2 == self.K else int(np.sum(self.dimension[(index + 2):self.K]))).astype(int),
						np.array(self.list_of_Ux[index + 1].get_value(x)) -
						np.array(self.list_of_Ux[index + 1].get_value(x_)),
						np.array(self.list_of_Ux[index].get_value(x)),
						np.zeros(0 if index == 0 else int(np.sum(self.dimension[0:index]))).astype(int)
					)
				)
			)
		# x = [z3.Real('xr_%s' % i)  for i in range(4)]
		# for i in range(len(self.list_of_Gx)):
		# 	print(self.list_of_Gx[i](x,x))
		
	def get_example(self, x, x_):  # Generate training set by Gx
		num_of_Gx = len(self.list_of_Gx)
		for index in range(num_of_Gx):
			print("INDEX: ", index, num_of_Gx)
			g_x = self.list_of_Gx[index](x, x_)
			# print('sample = ', g_x)
			# self.num_of_neg_data += 1INDEX
			# yield (- g_x, -1)
			# if list of Gx only has two components
			# it means that K = 1
#			if num_of_Gx == 2:
#				if index == 0:
#					self.num_of_neg_data += 1
#					yield (- g_x, -1)
#				else:
#					self.num_of_pos_data += 1
#					yield (g_x, 1)
#			else:
		

			if num_of_Gx > 1:
				if index %2 == 0:
					# print('positive')
					self.num_of_pos_data += 1
					yield (g_x, 1)
				else:
					# print('negtive')
					self.num_of_neg_data += 1
					yield(-g_x,-1)
			else:
				self.num_of_neg_data += 1
				self.num_of_pos_data += 1
				yield(g_x, 1)
				yield(-g_x, -1)
			
	def get_num_of_pos(self):
		return self.num_of_pos_data

	def get_num_of_neg(self):
		return self.num_of_neg_data

	def set_coefficients(self, coef):
		self.coefficients = coef

	def check_infinite_loop(self, n, cond, prime,tr=True):
		#print("check infinite loop")
		#x = [z3.Real('xr_%s' % i) for i in range(n)]
		x = [z3.Real('xr_%s' % i) if tr else z3.Int('xi_%s' % i) for i in range(n)]
		#print(x)
		# xp = [z3.Real('xrp_%s' % i) for i in range(n)]
		x_ = prime(x)
		#print(x_)
		a = cond(x)
		s = z3.Solver()
		s.add(cond(x))  # condition
		s.push()
		for i in range(n):
			s.add(x[i] == x_[i])
		#s.add(x = x_)
		s.push()
		#print('constraint system: ', s)
		result = s.check()
		if result == z3.sat:
			#print('found one infinite loop: ')
			m = s.model()
			model = [str(v)+"="+m[v].__str__() for v in x]
			for var in x:
				print(var, ' = ', m[var])
			return True, str(model)
		else:
			return False,''

	def int_coef_dot(self, coef_vec, gx, up_bound):
		den_upbound = z3.z3num.Numeral(up_bound).denominator()
		den_coef = max([z3.z3num.Numeral(v).denominator() for v in coef_vec])
		multiplied = max(den_upbound, den_coef)
		ceilings = [int(multiplied * v) for v in coef_vec]
		return sum(i[0] * i[1] for i in zip(ceilings, gx))

	def get_max_denominator(self, coef_vec, up_bound):
		den_upbound = z3.z3num.Numeral(up_bound).denominator()
		den_coef = max ([z3.z3num.Numeral(v).denominator() for v in coef_vec])
		multiplied = max(den_upbound, den_coef)
		return multiplied.as_long()
	
	@set_timeout(4, z3_verify_fail)
	def z3_verify(self, n, coef, cond, prime, tr=True):  # Check if every condition satisfied.
		x = [z3.Real('xr_%s' % i) if tr else z3.Int('xi_%s' % i) for i in range(n)]
		x_ = prime(x)
		s = z3.Solver()
		s.add(cond(x))  # condition
		s.push()
		valid = None
		model = None
		sum_dot = None
		#left_up_bound = None
		right_up_bound = None
		for index in range(self.K):
			# check whether it will be less than C_{index}
			if tr:
				sum_dot = np.dot(coef, self.list_of_Gx[index](x, x_))
				right_up_bound = self.list_of_C[index]
			else:
				multiplied = self.get_max_denominator(coef, self.list_of_C[index])
				ceilings = [int(multiplied * v) for v in coef]
				sum_dot = sum(i[0] * i[1] for i in zip(ceilings, self.list_of_Gx[index](x, x_)))
				right_up_bound = int(multiplied * self.list_of_C[index])
			s.add(sum_dot < right_up_bound)
			#print('-----constraint system CS: ', s)
			result = s.check()
			valid = result == z3.unsat
			#print(valid,result)
			if result == z3.sat:
				model = s.model()
				model = [eval(model[v].__str__()) for v in x]
				#print(s.model())		
			# elif result == z3.unsat:
			# 	print('case %d OK ' % index)
			# else:
			# 	print('unknown')
			s.pop()
			s.push()
			if not valid:
				break
		if valid:
			print('valid no bound ranking function')
			return True, model
		else:
			return False, model

	'''@set_timeout(4, z3_verify_fail)
	def z3_verify_heuristic_implication(self, n, coef, cond, prime, old_coef_array, tr=True):
		x = [z3.Real('xr_%s' % i) if tr else z3.Int('xi_%s' % i) for i in range(n)]
		x_ = prime(x)
		s = z3.Solver()
		s.add(cond(x))  # condition
		list_of_old_expr = []
		new_expr = coefDotExprZ3Arithmetic(x, coef, n, tr)
		for old_coef in old_coef_array:
			list_of_old_expr.append(coefDotExprZ3Arithmetic(x, old_coef, n, tr))
		heuristic_constraint = heuristicImplicationConstraint(list_of_old_expr, new_expr, tr)
		s.add(heuristic_constraint)
		s.push()
		valid = None
		model = None
		sum_dot = None
		#left_up_bound = None
		right_up_bound = None
		for index in range(self.K):
			# check whether it will be less than C_{index}
			if tr:
				sum_dot = np.dot(coef, self.list_of_Gx[index](x, x_))
				right_up_bound = self.list_of_C[index]
			else:
				multiplied = self.get_max_denominator(coef, self.list_of_C[index])
				ceilings = [int(multiplied * v) for v in coef]
				sum_dot = sum(i[0] * i[1] for i in zip(ceilings, self.list_of_Gx[index](x, x_)))
				right_up_bound = int(multiplied * self.list_of_C[index])
			s.add(sum_dot < right_up_bound)
			#print('constraint system: ', s)
			result = s.check()
			valid = result == z3.unsat
			#print(valid,result)
			if result == z3.sat:
				model = s.model()
				model = [eval(model[v].__str__()) for v in x]
				print(s.model())		
			# elif result == z3.unsat:
			# 	print('case %d OK ' % index)
			# else:
			# 	print('unknown')
			s.pop()
			s.push()
			if not valid:
				break
		if valid:
			print('valid no bound ranking function')
			return True, model
		else:
			return False, model'''
	
	def __str__(self):
		result = ''
		first = True
		#print(self.coefficients)
		for index in range(self.K):
			# remove all coefficients we used
			num_of_coef_used = sum(self.dimension[index:])
			print_coef = self.coefficients[(num_of_coef_used - self.dimension[index]): num_of_coef_used] * self.last_coef_array[(num_of_coef_used - self.dimension[index]): num_of_coef_used]
			#print('coeff = ', print_coef)
			#print('coeff = ', self.coefficients)
			#print("last coef = ", self.last_coef_array)
			#print("print coef:", print_coef)
			# polynomial
			#print(self.list_of_Ux[index])
			polys = self.list_of_Ux[index]
			rkf = polys.set_coefficients(print_coef)
			result += ('' if first else '; ') + rkf.__str__()
			first = False
		from VarStrMap import Map
		for t in Map:
			result = result.replace(t[0], t[1])	
		return result