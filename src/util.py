'''
some functions for convenience
@author xuechao
'''
import os
import numpy as np
import random
import datetime
from sklearn.svm import LinearSVC
from z3 import *
import signal
import time


from polynomial.Polynomial import Polynomial
from polynomial.Monomial import Monomial
from polynomial.Exponential import Exponential
from NestedRankingFunction import NestedRankingFunction
from NestedTemplate import NestedTemplate



def get_time_interval(s,e):
	return float((e-s).total_seconds())*1000
def get_time(t):
    return t.strftime("%Y-%m-%d-%H-%M-%S")

'''
    the matrix for the polynomial
    p(x) = b0 * (x_0^{p00} * x_1^{p01} .....) + b1 * (x_0^p10 * x_1^p11.....)+.....
    as follows.  
            [
                [p00,p01,p02,...,b0],
                [p10,p11,p12,...,b1],
                .......
                [.....]
            ]
              row: every monomial in p(x)
              column: the power of each variables, and the coefficient of this monomial(last value).
'''

def has_fraction(list_of_items):
    for item in list_of_items:
        if 0 < item < 1:
            return True
    return False

def make_dict_order(num_of_vars, dimension, mat_of_vars):
    polys = {}
    order = []
    for i in range(dimension):
        # initialize a monomial with an array of powers
        # input the i-th monomial
        mon_ = None
        coefs = mat_of_vars[i][:num_of_vars]
        # if not has_fraction(coefs):
        #     mon_ = Monomial(coefs)
        # else:
        #     mon_ = Exponential(coefs)
        mon_ = Monomial(coefs)
        order.append(mon_)
        # print(mon_)
        # get the coefficient of the monomial
        polys[mon_] = mat_of_vars[i][-1]
    # print(polys)
    return polys,order

def parse_template(templatePath,numOfVar,ListOfDimension, indexOfTemplate):
	arrays = np.loadtxt(os.path.join(templatePath,"template"+str(indexOfTemplate)),delimiter=',')
	arrays = arrays.reshape(-1,numOfVar+1)
	print(len(arrays),ListOfDimension)
	if(len(arrays) != np.sum(ListOfDimension)):
		raise Exception('Wrong template format')
	start = 0
	# print(arrays)
	polynomial_result = []
	for d in ListOfDimension:
		polys,order = make_dict_order(numOfVar, d,  arrays[start:start+d])
		# print(polys,order)
		polynomial_result.append(
			Polynomial(
				polys, order
				)
			)
		start += d
	return polynomial_result





def get_condition(L,x):
    try :
        result = L[0](x)
    except Exception as e:
        return False 
    return result  # e.g. x[0]**2 + x[1]**2 <= 1 # 3 >= x[0] >= 1


def get_statement(L, x):
    try :
        result = L[1](x)
    except Exception as e:
        return None
    return result # e.g. [x[0]-x[1]**2+1, x[1]+x[0]**2-1] # [5*x[0]-x[0]**2]


def is_type_real(L): 
    return len(L) <= 6 + L[3]

def sample_points(L, m, h, n, rf,base_point):
	# for result, x, y in sample_points_same_interval(L, m, h, n, rf,base_point):
	# 	yield(result, x, y)

	for result, x, y in sample_points_bisection(L,n,rf):
		print(x,y)
		yield(result, x, y)

def sample_points_bisection(L,n,rf):
	rt = is_type_real(L)
	if rt:
		cond = L[-1]
	else:
		cond = L[-2]
	for i in range(1):
		x = [z3.Real('xr_%s' % i) if rt else z3.Int('xi_%s' % i) for i in range(n)]
		s = z3.Solver()
		s.push()
		s.add(simplify(cond(x)))  # condition
		result = s.check()
		m = None
		if result == z3.sat:
			model = [eval(s.model()[v].__str__()) for v in x]
			s_p = np.array([(x if x is not None else 0) for x in model ])
			s.pop()
			condition = True
			if isinstance(cond(x),list):
				for i in cond(x):
					condition = And(condition, i)
			else:
				condition = cond(x)
			s.add(simplify(Not(condition)))
			result = s.check()
			# print(result)
			if result == z3.sat:
				model = [eval(s.model()[v].__str__()) for v in x]
				u_p = np.array([(x if x is not None else 0) for x in model])
				for i in range(20):
					# print(s_p,u_p)
					if np.all(s_p == u_p):
						s_p_ = get_statement(L,s_p)
						if s_p_ is None:
							break
						for x,y in rf.get_example(s_p,s_p_):
							yield('UNKNOWN',x,y)
					m = (s_p+u_p)/2
					# print(m)
					if get_condition(L,m):
						s_p = m
					else:
						u_p = m
				# print(m)
			else:
				yield('INFINATE',None,None)
		else:
			yield('FINATE',None,None)
		m_ = get_statement(L,m)
		if m_ is None:
			continue
		for x,y in rf.get_example(m,m_):
			yield('UNKNOWN', x,y)

def sample_points_same_interval(L, m, h, n, rf,base_point):
   # print('sample_points ',  m, h, n,base_point)
        for p in get_xpoints( m, h, n,base_point):  # Generate all candidate n-D points
            #print(p)
            condition = get_condition(L,p)
            if condition:  # must satisfy the guard condition
                p_ = get_statement(L,p)
                if p_ is None:
                    continue
                for x, y in rf.get_example(p, p_):  # by ranking function to generate dataset for SVM
                    yield ('UNKNOWN',x, y)
        #print(rf.get_zero_vec())
        base_point_ = get_statement(L,base_point)
        if base_point_ is None:
            return 
        for x,y in rf.get_example(base_point,base_point_):
            yield('UNKNOWN',x,y)

    # yield (rf.get_zero_vec(), -1)
    # print("sample example down!!")


def get_xpoints( m, h, n,base_point):
    """
    :param m: width
    :param h: distance
    :param n: dimension
    :return: points
    """
    if n == 1:
        for p in np.arange(-m+base_point[n-1], m + h+base_point[n-1], h):  # for 1 dimension iteration,just generate 2m/h 1-D points with only one value
            yield [p]
    elif n > 1:
        # for every {n-1}-D point in n-1 dimension iteration,
        #   append all possible value in [-m,m] by h step to generate 2m/h {n}-D points in n dimension iteration
        for p in get_xpoints(m, h, n - 1,base_point):
            for x in np.arange(-m+base_point[n-1], m + h+base_point[n-1], h):
                yield p + [x]

def signal_handler(signum, frame):
	raise Exception("time out")

def train_ranking_function(L, rf, x, y,  m=4, h=0.5, n=2):
	n=L[2]
	m = max((100 ** (1/n))*h/2,h )
	rt = is_type_real(L)
	# integer
	if not rt:
		h = 1
		m = int(max((100 ** (1/n))/2,0))
        
	print("*****************************************************\n")
	if rt:
		Is_inf,inf_model = rf.check_infinite_loop (n, L[-1], L[-2])
	else:
		Is_inf,inf_model =rf.check_infinite_loop (n, L[-2], L[-3],False)
	if Is_inf:
		print(  "it is not terminating, an infinate loop with initial condition:\n")
		print(  inf_model+'\n')
		return "INFINATE",None,None
	st = datetime.datetime.now()
	# print(str(get_time(st)) + "   >>>>   " + "Start sampling point\n")
	# print(*sample_points(no, m, h, n, rf))
	result=[]
	try:
		#result,x, y = zip(*sample_points(L, m, h, n, rf,[0]*n)) 
		for new_result,new_x,new_y in sample_points(L, m, h, n, rf,[0]*n):
			x = x+(np.array(new_x),)
			y = y+(new_y,)
			result.append(new_result)
		# result,x, y = zip(*sample_points_bisection(L, n, rf))
		#print(x,y)
	except Exception as e:
		print(e)
		#x,y = (),()
		result = ['UNKNOWN']
	s_t = datetime.datetime.now()
	#print(result)
	if result[0] != 'UNKNOWN':
		return result[0],x,y
	print( str(get_time(s_t))+"   >>>>   " + "End sampling point\n")
	print( 'sampling time = %.3f ms,\n\n' % ( get_time_interval(st, s_t)))
	#print(x, y)
	# print 'start train_ranking_function...'
	count = 0
	last_coef =[]
	same_coef_count = 0
	list_of_accu = [0,1,4]
	acc = 4 if rt else 1
	while True:
		print( "       ########################################         \n")
		print(  "iteration "+str(count)+ " with "+str(len(y)) + " examples"+"\n")
		ct = datetime.datetime.now()
		print(  str(get_time(ct))+ "   >>>>   " + "Start train ranking function\n")
		try:
			SVM=LinearSVC (fit_intercept=False)
			SVM.fit(x, y)
			# print(SVM.coef_[0])
			coef = [round (j, acc) for j in SVM.coef_[0]]
			if(np.all(coef == last_coef)):
				same_coef_count+=1
				if same_coef_count == 5 :
					list_of_accu.remove(acc)
					print(same_coef_count)
					length = len(list_of_accu)
					if length ==0:
						print( "the coefficient is convergent\n")
						break
					acc = random.choice(list_of_accu)
					same_coef_count = 0
			else:
				same_coef_count=0
			last_coef = coef
			print('training done')
		except Exception as e:
			coef = [round (random.random(), acc) for j in range(np.sum(rf.dimension))]
			last_coef =coef
			print(e)
			raise e
			print('problem in training, choose random value')
        	
		et = datetime.datetime.now()
		print(  str(get_time(et))+"   >>>>   " + "End train ranking function\n")
		print( 'train_ranking_functioning time = %.3f ms\n\n' % ( get_time_interval(ct, et)))
		np.set_printoptions (suppress=True)
		# print 'train_ranking_function done...'
		#print(  "\ncoefficient are \n")
		#print( " "+str(coef) + "\n\n")
		#print (coef, len (y))
		ht = datetime.datetime.now()
		print(  str(get_time(ht))+"   >>>>   " + "Start verify ranking function\n")
		rf.set_coefficients (coef)
		# print('ranking function: ', rf)
		ret = None
		Is_inf = False

		#signal.signal(signal.SIGALRM, signal_handler)
		#signal.alarm(1)     
		#try:
		if rt:
			ret = rf.z3_verify (n, coef, L[-1], L[-2])
			# print('check_result = ', ret)
			# print(ret)
			# if not ret[0]:
			# 	Is_inf,inf_model = rf.check_infinite_loop (n, L[-1], L[-2])
		else:
			ret = rf.z3_verify(n, coef, L[-2], L[-3], False)
		# except Exception as e:
		# 	print(e)
		# 	ret = False, None
		# 	# if not ret[0]:
		# 	# 	Is_inf,inf_model =rf.check_infinite_loop (n, L[-2], L[-3],False)
		# signal.alarm(0)
		# if Is_inf:
		# 	print(  "it is not terminated, an infinate loop with initial condition:\n")
		# 	print(  inf_model+'\n')
		# 	return "INFINATE"
		# check(n, coef)
		h_t = datetime.datetime.now()
		print(  "ranking function : " + str(rf)+"\n")
		print(  str(get_time(h_t))+"   >>>>   " + "End verify ranking function\n")
		#print( "\nTotal time used:\n")
		print( 'verifying time = %.3f ms\n\n' % (get_time_interval(ht, h_t)))
		# print ('sampling = %.3fs, train_ranking_functioning = %.3fs, verifying = %.3fs' % (
		# s_t - st, et - ct, h_t - ht))
		if ret[0]:
			print(  "Found Ranking Fcuntion: "+str(rf)+"\n")
			return "FINATE",None,None
		elif ret[1] is None:
			return 'UNKNOWN',x,y
		elif ret[1] is not None:
			# add more points
			print( "Not Found Ranking Fcuntion\n")
			p = [(x if x is not None else 0) for x in ret[1] ]#ret[1]
			print(  "Conterexample is \n")
			print(  str(p)+"\n")
			# print('model = ', p)
			p_ = get_statement(L, p)
			# print(p, p_)
			# tp = rf.get_example(p, p_)
			# print(tp)
			# print(*tp)
			# new_x,new_y = zip(*rf.get_example(p, p_))
			# print(x,y)
			st = datetime.datetime.now()
			for new_x,new_y  in rf.get_example(p, p_):
			# for new_x,new_y  in sample_points(L, m, h, n, rf,p):
			    x = x+(np.array(new_x),)
			    y = y+(new_y,)
			s_t = datetime.datetime.now()
			print( 'sampling time = %.3f ms\n\n' % (get_time_interval(st, s_t)))
		count += 1
		if count >= 200:
		   break
	print(  "Failed to prove it is terminating\n")
	return "UNKNOWN",x,y

