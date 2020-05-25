'''
This is a prototype tool for proving the termination of lopp programs
@author:  
    Xuechao Sun (sunxc@ios.ac.cn)
    Yong Li (liyong@ios.ac.cn)
'''


import numpy as np
from sklearn.svm import LinearSVC
from Loops import L
import datetime
import z3
import sys
import os
import random

from polynomial.Polynomial import Polynomial
from polynomial.Monomial import Monomial
from polynomial.Exponential import Exponential
from NestedRankingFunction import NestedRankingFunction
from NestedTemplate import NestedTemplate

from util import *

Log=""


def main():
    # U_1 = Polynomial(2,2,np.array([  [0,0,1],
    # 				[0,1,1]]))
    # U_2 = Polynomial(2,2,np.array([  [0,0,1],
    # 				[1,0,1]]))
    # rf = NestedRankingFunction([U_1,U_2],[0,0],0.1)
    # no = 19
    # train_ranking_function(rf,n=L[no][-2])
    # old_num_solved = []
    # L = sys.argv[1]
    # log_path = sys.argv[1]
    num_start = int(sys.argv[1])
    num_end = int(sys.argv[2])
    # if not os.path.exists(log_path):
    #     os.makedirs(log_path)
    # log_file = os.path.join(log_path,"LogFile_"+str(get_time(time.time()))+"_nonLinear.log")
    new_num_solved = []
    finate_num = 0
    infinate_num = 0
    unknow_num = 0
    # f = open(log_file,'w')
    # f.write("")
    # f.close()
    for no in range(num_start,num_end):  # list(range(1, 6)) + list(range(18, 20)):
        s_t = datetime.datetime.now()
        if no not in L.keys():
            continue
        print('Example >>>>',no)
        list_dic = [make_dict_order(L[no][2], len(x), np.array(x)) for x in L[no][4:4 + L[no][3]]]
        print(list_dic)
        rf = NestedTemplate( #NestedRankingFunction(

            # list of U(x)
            [
                Polynomial(list_dic[i][0],list_dic[i][1]) for i in range(len(list_dic))
            ]
            # list of C
            , [0.001] * L[no][3]
            # Delta
            , 0)
        # number of variables   
        # global Log
        # Log = ""
        ret = False
        try:
            ret = train_ranking_function(L[no],rf)
        except Exception as e:
            print("ERROR:\n" + str(e)+"\n")
            # Log += "\n" + str(e)+"\n"
        # f = open(log_file,'a')
        # f.write(Log)
        # f.close()
        if ret== 'FINATE':
            finate_num +=1
        #     print('#num_pos = ', rf.get_num_of_pos(), ' #num_neg = ', rf.get_num_of_neg())
        elif ret == 'INFINATE':
            infinate_num +=1
        elif ret == 'UNKNOWN':
            unknow_num +=1
        #new_num_solved.append(ret != 'UNKNOWN')
        e_t = datetime.datetime.now()
        print('Time Total used --->: ',get_time_interval(s_t,e_t))

    print(finate_num, infinate_num,unknow_num, finate_num+ infinate_num,finate_num+infinate_num+unknow_num )

#    for i in range(len(old_num_solved)):
#        if old_num_solved[i] and not new_num_solved[i]:
#            print(i)


if __name__ == '__main__':
    main()
