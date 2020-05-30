import numpy as np
from OneLoop import L
import time
import sys
import os
from util import *
from FindMultiphaseUtil import *
from LearnRanker import *

def LearnRankerNoBoundLoopBody(L_test, x, y):
    ret = 'UNKNOWN'
    print("L:",L_test[2])
    print(L_test[3])
    print(L_test[4])
    listOfUxDimension = []
    for i in range(L_test[3]):
        listOfUxDimension.append(L_test[2] + 1)
    #print("listOfDimension",listOfUxDimension)
    listOfUx = parse_template_handcraft(L_test[4], L_test[2], listOfUxDimension)
    rf = NestedNoBoundTemplate(
        listOfUx,
        [0.001] *len(listOfUx)
    )
    #ret, new_x, new_y = train_ranking_function(L_test, rf, x, y)
    ret, new_x, new_y = train_ranking_function(L_test, rf, x, y)
    return ret, rf

def LearnRankerBoundedLoopBody(L_test, x, y):
    ret = 'UNKNOWN'
    print("L[2]:",L_test[2])
    print("L[3]:",L_test[3])
    print("L[4]:",L_test[4])
    listOfUxDimension = []
    for i in range(L_test[3]):
        listOfUxDimension.append(L_test[2] + 1)
    print("listOfDimension",listOfUxDimension)
    listOfUx = parse_template_handcraft(L_test[4], L_test[2], listOfUxDimension)
    rf = NestedTemplate(
        listOfUx,
        [0.001] *len(listOfUx),
        0
    )
    ret, new_x, new_y = train_ranking_function(L_test, rf, x, y)
    return ret, rf


def LearnRankerNoBound(templateFilePath, indexOfTemplate, x, y, L_test):
    infoFile = open(os.path.join(templateFilePath,'Info'+str(indexOfTemplate)),'r')
    info = []
    for line in infoFile.readlines():
        line = line.strip()
        if line== '':
            continue
        info.append(line)
    listOfUxDimension= [int(x) for x in info]
    
    listOfUx = parse_template(templateFilePath,L_test[2],listOfUxDimension, indexOfTemplate)
    rf = NestedNoBoundTemplate( #NestedNoBoundRankingFunction(
        # list of U(x)
        listOfUx
        # list of C
        , [0.001] *len(listOfUx)
        )
    # number of variables   

    ret = 'UNKNOWN'
    # oldtime=datetime.datetime.now()
    try:
        ret,new_x,new_y = train_ranking_function(L, rf, x, y)
    except Exception as e:
        # print("ERROR:\n" + str(e)+"\n")
        print( "\n" + str(e)+"\n")
        new_x,new_y  = x,y
    #newtime=datetime.datetime.now()
    #f = open(os.path.join(logPath,'AnalysisTimeForTraining.log'),'a')
    #f.write('Time For %s Is ---> %f ms\n' %(templateFilePath,float((newtime-oldtime).total_seconds())*1000 ))

    #f.close()
    if ret== 'FINATE':
        print(rf)
        # print('#num_pos = ', rf.get_num_of_pos(), ' #num_neg = ', rf.get_num_of_neg())
    return ret,new_x,new_y

def train_multi_ranking_function(L, x, y, upperLoopBound=3):
    ret = 'UNKNOWN'
    print("----------------START MAIN LOOP-------------------")
    
    for phaseNum in range(upperLoopBound):
        L_current = L
        old_coef_array = []
        print("----------------START LEARNING MULTI-------------------")
        for i in range(phaseNum+1):
            if(i < phaseNum):
                print("---------------------LEARN RANKING PART----------------------")
                print("---------LoopNum ", i)
                print("---------LoopBound ", phaseNum)
                # if the phase does not reach the bound, should find ranking no bound
                ret, rf = LearnRankerNoBoundLoopBody(L_current, x, y)
                L_current = ConjunctRankConstraintL(L_current, rf)
                old_coef_array.append(rf.coefficients)
            else:
                # the phase reach the bound, should find ranking function here
                print("---------------------LEARN RANKING FUNCTION----------------------")
                print("---------LoopNum ", i)
                print("---------LoopBound ", phaseNum)
                ret, rf = LearnRankerBoundedLoopBody(L_current, x, y)
                if ret == 'FINATE':
                    return 'FINATE'
                elif ret == 'INFINATE':
                    return 'INFANITE'
            i += 1
        print("---------------- LEARNING OVER-------------------")
        print("---------RESULT:", ret, rf)
    print(rf)
    return 'UNKNOWN'


def LearnMultiRanker(templateFilePath, indexOfTemplate, x, y):
    infoFile = open(os.path.join(templateFilePath,'Info'+str(indexOfTemplate)),'r')
    info = []
    for line in infoFile.readlines():
        line = line.strip()
        if line== '':
            continue
        info.append(line)
    listOfUxDimension= [int(x) for x in info]
    
    listOfUx = parse_template_multi(templateFilePath,L[2],listOfUxDimension, indexOfTemplate)
    
    # number of variables   

    ret = 'UNKNOWN'
   # oldtime=datetime.datetime.now()
    try:
        ret,new_x,new_y = train_ranking_function(L, rf, x, y)
    except Exception as e:
        # print("ERROR:\n" + str(e)+"\n")
        print( "\n" + str(e)+"\n")
        new_x,new_y  = x,y
    #newtime=datetime.datetime.now()
    #f = open(os.path.join(logPath,'AnalysisTimeForTraining.log'),'a')
    #f.write('Time For %s Is ---> %f ms\n' %(templateFilePath,float((newtime-oldtime).total_seconds())*1000 ))

    #f.close()
    if ret== 'FINATE':
        #print(rf)
        # print('#num_pos = ', rf.get_num_of_pos(), ' #num_neg = ', rf.get_num_of_neg())
        return ret