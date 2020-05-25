import numpy as np
import z3

'''
nested ranking function <f_1, f_2, ..., f_k>; this is a template more expressive than traditional ranking function.
Let f_i = a^T_i U_i(x) for every  1 <= i <= k such that for a list positive numbers {C_1, C_2, ..., C_n} and a number delta

a^T_1 (- U_1(x) + U_1(x')) <= 0 - C_1
a^T_2 (- U_2(x) + U_2(x')) - a^T_1 U_1(x)  <= 0 - C_2
...
a^T_k (- U_k(x) + U_k(x')) - a^T_{k-1} U_{k-1}(x)  <= 0 - C_k
a^T_k U_k(x) >= delta

'''


class NestedRankingFunction:
	
	def __init__(self, list_of_Ux, list_of_C, delta):  # list_of_Ux: k U_x, list_of_C: C_i
		self.K = len(list_of_Ux)
		self.list_of_Ux = list_of_Ux
		self.list_of_C = list_of_C
		self.delta = delta
		# Ux is a polynomial and dimension is the number of monomials
		self.dimension = [x.get_dimension() for x in list_of_Ux]  # calculate dimension  of each U_x
		self.list_of_Gx = []
		self.__generate_gx_list()
		self.num_of_pos_data = 0
		self.num_of_neg_data = 0

	def get_zero_vec(self):
		return np.zeros(np.sum(self.dimension))

	'''
	G_1(x) = 0 -(0, 0, ..., U_1(x) - U_1(x'))^T
	G_2(x) = 0 -(0, ..., 0, U_2(x) - U_2(x'), U_1(x))^T
	...
	G_k(x) = 0 - (U_k(x) - U_k(x'), U_{k-1}(x), 0, ..., 0)^T
	G_{k+1}(x) = (U_k(x), 0, ..., 0)^T
	
	a^T = (a^T_k, a^T_{k-1}, ..., a^T_2, a^T_1)^T
	'''

	def __generate_gx_list(self):  # Generate G_x by U_x, G_x is a lambda expression
		'''
		(0, 0, ..., 0, U_1(x') - U_1(x))^T
		there are K-1 0-vector in the front
		'''
		self.list_of_Gx.append(# x is the list of variables, x_ is primed x.
				lambda x, x_:  np.concatenate(
					(np.zeros(int(np.sum(self.dimension[1:]))),
								np.array(self.list_of_Ux[0].get_value(x_)) - np.array(self.list_of_Ux[0].get_value(x))
					)
				)
			)
		'''
		i and i-1
		(0, 0, ..., 0, U_i(x') - U_i(x))^T, 0-U_{i-1}(x), 0, ..., 0)^T
		i-2 consecutive 0 vector in the end
		'''
		for index in range(self.K - 1):
			'''
			there are index - 1 0-vector in the end
			'''
			pre_zeros = 0 if index == 0 else int(np.sum(self.dimension[0:index]))
			'''
			i, i + 1 -> -U_{i-1}(x) and U_{i}(x')-U_{i}(x) 
			>= i + 2, 0-vector
			'''
			aft_zeros = 0 if index + 2 == self.K else int(np.sum(self.dimension[(index + 2):self.K]))
			self.list_of_Gx.append(
				lambda x, x_: np.concatenate(
						(	
						np.zeros(pre_zeros),
						np.array(self.list_of_Ux[index + 1].get_value(x_)) - np.array(self.list_of_Ux[index + 1].get_value(x)),
						-np.array(self.list_of_Ux[index].get_value(x)),
						np.zeros(aft_zeros)
						)
					)
				)
		'''
		(U_k(x), 0, ..., 0)^T
		k-1 consecutive 0 vector in the end
		'''
		self.list_of_Gx.append(
				lambda x, x_: np.concatenate((np.array(self.list_of_Ux[self.K - 1].get_value(x)),
								np.zeros(int(np.sum(self.dimension[0:-1])))
							))
			)

	def get_example(self, x, x_):  # Generate training set by Gx
		for index in range(len(self.list_of_Gx)):
			g_x = self.list_of_Gx[index](x, x_)
			if index == self.K:
				self.num_of_pos_data += 1
				yield(g_x, 1)
			else:
				self.num_of_neg_data += 1
				yield(g_x, -1)

	def get_num_of_pos(self):
		return self.num_of_pos_data

	def get_num_of_neg(self):
		return self.num_of_neg_data

	def set_coefficients(self, coef):
		self.coefficients = coef

	def check_infinite_loop(self, n, cond, prime):
		x = [z3.Real('xr_%s' % i) for i in range(n)]
		# xp = [z3.Real('xrp_%s' % i) for i in range(n)]
		x_ = prime(x)
		s = z3.Solver()
		s.add(cond(x))  # condition
		s.push()
		s.add(x == x_)
		s.push()
		result = s.check()
		if result == z3.sat:
			print('found one infinite loop: ')
			m = s.model()
			for var in x:
				print(var, ' = ', m[var])


	def z3_verify(self, n, coef, cond, prime, tr = True):  # Check if every condition satisfied.
		x = [z3.Real('xr_%s' % i) if tr else z3.Int('xi_%s' % i) for i in range(n)]
		x_ = prime(x)
		s = z3.Solver()
		s.add(cond(x))  # condition
		s.push()
		valid = None
		model = None
		for index in range(self.K):
			# should also add 0 - C_{index}
			s.add(np.dot(coef, self.list_of_Gx[index](x, x_)) > - self.list_of_C[index])
			print('constraint system: ', s)
			result = s.check()
			valid = result == z3.unsat
			if result == z3.sat:
				model = s.model()
				print(s.model())
			elif result == z3.unsat:
				print('case %d OK ' % index)
			else:
				print('unknown')
			s.pop()
			s.push()
			if not valid:
				break
		if valid:
			s.add(np.dot(coef, self.list_of_Gx[self.K](x, x_)) < self.delta)
			result = s.check()
			if result == z3.sat:
				model = s.model()
				print(s.model())
			elif result == z3.unsat:
				print('valid ranking function')
				return True, model
			else:
				print('unknown')
				return False, model
		else:
			print('unknown')
			return False, model
	
	def __str__(self):
		result = ''
		first = True
		for index in range(self.K):
			# remove all coefficients we used
			num_of_coef_used = sum(self.dimension[index:])
			coef = self.coefficients[(num_of_coef_used - self.dimension[index]) : num_of_coef_used ]
			# print('coeff = ', coef)
			# polynomial
			# print(self.list_of_Ux[index])
			polys = self.list_of_Ux[index]
			rkf = polys.set_coefficients(coef)
			result += ('' if first else '; ') + rkf.__str__()
			first = False 
		return result
