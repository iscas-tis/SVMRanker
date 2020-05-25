'''
This is a prototype tool for proving the termination of lopp programs
@author:  
    Xuechao Sun (sunxc@ios.ac.cn)
    Yong Li (liyong@ios.ac.cn)
'''


import numpy as np
from sklearn.svm import LinearSVC
from Loops import L
import time
import z3
import sys
import os
import random

from polynomial.Polynomial import Polynomial
from polynomial.Monomial import Monomial
from polynomial.Exponential import Exponential
from NestedRankingFunction import NestedRankingFunction
from NestedTemplate import NestedTemplate

Log=""

def get_time(t):
    return time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime(t))

def get_condition(x, no):
    return L[no][0](x)  # e.g. x[0]**2 + x[1]**2 <= 1 # 3 >= x[0] >= 1


def get_statement(x, no):
    return L[no][1](x)  # e.g. [x[0]-x[1]**2+1, x[1]+x[0]**2-1] # [5*x[0]-x[0]**2]


def is_type_real(no):
    return len(L[no]) <= 6 + L[no][3]


def sample_points(no, m, h, n, rf,base_point):
    print('sample_points ', no, m, h, n,base_point)
    for p in get_xpoints(no, m, h, n,base_point):  # Generate all candidate n-D points
        if get_condition(p, no):  # must satisfy the guard condition
            p_ = get_statement(p, no)
            for x, y in rf.get_example(p, p_):  # by ranking function to generate dataset for SVM
                yield (x, y)
                #print(x,y)
    #print(rf.get_zero_vec())
    yield (rf.get_zero_vec(), -1)
    print("sample example down!!")


def get_xpoints(no, m, h, n,base_point):
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
        # 	append all possible value in [-m,m] by h step to generate 2m/h {n}-D points in n dimension iteration
        for p in get_xpoints(no, m, h, n - 1,base_point):
            for x in np.arange(-m+base_point[n-1], m + h+base_point[n-1], h):
                yield p + [x]


def train_ranking_function(rf, no, m=4, h=0.5, n=2):
    m = max((100 ** (1/n))*h/2,h )
    global Log
    Log = ""
    rt = is_type_real(no)
    # integer
    if not rt:
        h = 1
        m = int(max((100 ** (1/n))/2,0))
        
    Log +=  "*****************************************************\n"
    Log +=  str(no)+":\n"
    st = time.time()
    Log += str(get_time(st)) + "   >>>>   " + "Start sampling point\n"
    # print(*sample_points(no, m, h, n, rf))
    x, y = zip(*sample_points(no, m, h, n, rf,[0]*n))
    s_t = time.time()
    Log += str(get_time(s_t))+"   >>>>   " + "End sampling point\n"
    #print(x, y)
    # print 'start train_ranking_function...'
    count = 0
    last_coef =[]
    while True:
        Log +="       ########################################         \n"
        Log += "iteration "+str(count)+" for No."+str(no)+ " with "+str(len(y)) + " examples"+"\n"
        ct = time.time()
        Log += str(get_time(ct))+ "   >>>>   " + "Start train ranking function\n"
        if len(y) >1:
            SVM = LinearSVC (fit_intercept=False)
            SVM.fit (x, y)
            print(SVM.coef_[0])
            coef = [round (j, 7) for j in SVM.coef_[0]]
        else:
            coef = [round (random.random(), 7) for j in range(np.sum(rf.dimension))]
        if(np.all(coef == last_coef)):
            Log += "the coefficient is convergent\n"
            break
        last_coef = coef
        et = time.time ()
        Log += str(get_time(et))+"   >>>>   " + "End train ranking function\n"
        np.set_printoptions (suppress=True)
        # print 'train_ranking_function done...'
        Log += "\ncoefficient are \n"
        Log += " "+str(coef) + "\n\n"
        print (coef, len (y))
        ht = time.time ()
        Log += str(get_time(ht))+"   >>>>   " + "Start verify ranking function\n"
        rf.set_coefficients (coef)
        print('ranking function: ', rf)
        ret = None
        if rt:
            ret = rf.z3_verify (n, coef, L[no][-1], L[no][-2])
            # print('check_result = ', ret)
            print(ret)
            if not ret[0]:
                Is_inf,inf_model = rf.check_infinite_loop (n, L[no][-1], L[no][-2])
        else:
            ret = rf.z3_verify(n, coef, L[no][-2], L[no][-3], False)
            if not ret[0]:
                Is_inf,inf_model =rf.check_infinite_loop (n, L[no][-2], L[no][-3])
        if Is_inf:
            Log += "it is not terminated, an infinate loop with initial condition:\n"
            Log += inf_model+'\n'
            return "INFINATE"
        # check(n, coef)
        h_t = time.time()
        Log += "ranking function : " + str(rf)+"\n"
        Log += str(get_time(h_t))+"   >>>>   " + "End verify ranking function\n"
        Log += "\nTotal time used:\n"
        Log += 'sampling = %.3fs, train_ranking_functioning = %.3fs, verifying = %.3fs\n\n' % (
                        s_t - st, et - ct, h_t - ht)
        print ('sampling = %.3fs, train_ranking_functioning = %.3fs, verifying = %.3fs' % (
        s_t - st, et - ct, h_t - ht))
        if ret[0]:
            Log += "Found Ranking Fcuntion\n"
            return "FINATE"
        elif ret[1] is not None:
            # add more points
            Log += "Not Found Ranking Fcuntion\n"
            p = [(x if x is not None else 0) for x in ret[1] ]#ret[1]
            Log += "Conterexample is \n"
            Log += str(p)+"\n"
            print('model = ', p)
            # p_ = get_statement(p, no)
            # print(p, p_)
            # tp = rf.get_example(p, p_)
            # print(tp)
            # print(*tp)
            # new_x,new_y = zip(*rf.get_example(p, p_))
            # print(x,y)
            # for new_x,new_y  in rf.get_example(p, p_):
            for new_x,new_y  in sample_points(no, m, h, n, rf,p):
                x = x+(np.array(new_x),)
                y = y+(new_y,)
        count += 1
        if count >= 200:
           break
    Log += "Failed to prove it is terminated\n"
    return "UNKNOWN"






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


def make_dict(num_of_vars, dimension, mat_of_vars):
    polys = {}
    for i in range(dimension):
        # initialize a monomial with an array of powers
        # input the i-th monomial
        mon_ = None
        coefs = mat_of_vars[i][:num_of_vars]
        if not has_fraction(coefs):
            mon_ = Monomial(coefs)
        else:
            mon_ = Exponential(coefs)
        # print(mon_)
        # get the coefficient of the monomial
        polys[mon_] = mat_of_vars[i][-1]
    # print(polys)
    return polys





def main():
    # U_1 = Polynomial(2,2,np.array([  [0,0,1],
    # 				[0,1,1]]))
    # U_2 = Polynomial(2,2,np.array([  [0,0,1],
    # 				[1,0,1]]))
    # rf = NestedRankingFunction([U_1,U_2],[0,0],0.1)
    # no = 19
    # train_ranking_function(rf,n=L[no][-2])
    # old_num_solved = []
    L = sys.argv[1]
    log_path = sys.argv[2]
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    log_file = os.path.join(log_path,"LogFile_"+str(get_time(time.time()))+".log")
    new_num_solved = []
    f = open(log_file,'w')
    f.write("")
    f.close()
    for no in range(17,18):  # list(range(1, 6)) + list(range(18, 20)):
        if no not in L.keys():
            continue
        print(no)
        print('NestedTemplate')
        rf = NestedTemplate( #NestedRankingFunction(

            # list of U(x)
            [
                Polynomial(make_dict(L[no][2], len(x), np.array(x))) for x in L[no][4:4 + L[no][3]]
            ]
            # list of C
            , [0.001] * L[no][3]
            # Delta
            , 0)
        # number of variables   
        global Log
        Log = ""
        ret = False
        try:
            ret = train_ranking_function(rf, no, n=L[no][2])
        except Exception as e:
            print("ERROR:\n" + str(e)+"\n")
            Log += "\n" + str(e)+"\n"
        f = open(log_file,'a')
        f.write(Log)
        f.close()
        if ret== 'FINATE':
            print(rf)
            print('#num_pos = ', rf.get_num_of_pos(), ' #num_neg = ', rf.get_num_of_neg())
        new_num_solved.append(ret != 'UNKNOWN')

    print('total solved number = ', sum([1 if v else 0 for v in new_num_solved]))

#    for i in range(len(old_num_solved)):
#        if old_num_solved[i] and not new_num_solved[i]:
#            print(i)


if __name__ == '__main__':
    main()
