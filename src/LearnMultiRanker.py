'''
@author Xie Li
'''
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
        listOfUxDimension.append(L_test[2]+1)
    print("listOfDimension",listOfUxDimension)
    listOfUx = parse_template_handcraft(L_test[4], L_test[2], listOfUxDimension)
    rf = NestedNoBoundTemplate(
        listOfUx,
        [0.001] *len(listOfUx)
    )
    #ret, new_x, new_y = train_ranking_function(L_test, rf, x, y)
    ret, new_x, new_y = train_ranking_function(L_test, rf, x, y)
    if ret == 'FINITE':
        no_bound_return = 'CORRECT'
    elif ret == 'INFINITE':
        no_bound_return = 'INFINITE'
    else:
        no_bound_return = 'FALSE'
    return no_bound_return, rf

def LearnRankerBoundedLoopBody(L_test, x, y):
    ret = 'UNKNOWN'
    print("L[2]:",L_test[2])
    print("L[3]:",L_test[3])
    print("L[4]:",L_test[4])
    listOfUxDimension = []
    for i in range(L_test[3]):
        listOfUxDimension.append(L_test[2]+1)
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
    if ret== 'FINITE':
        print(rf)
        # print('#num_pos = ', rf.get_num_of_pos(), ' #num_neg = ', rf.get_num_of_neg())
    return 'UNKNOWN',new_x,new_y
'''
def train_multi_ranking_function(L, x, y, upperLoopBound=3):
    ret = 'UNKNOWN'
    print("----------------START LOOP LEARNING-------------------")
    
    for phaseNum in range(upperLoopBound):
        rankingFunctionRecordingList = []
        L_current = L
        # used for implication 
        old_coef_array = []
        print("----------------START LEARNING MULTI-------------------")
        for i in range(phaseNum+1):
            if(i < phaseNum):
                print("---------------------LEARN RANKING PART----------------------")
                print("---------LoopNum ", i)
                print("---------LoopBound ", phaseNum)
                # if the phase does not reach the bound, should find ranking no bound
                ret, rf = LearnRankerNoBoundLoopBody(L_current, x, y)
                rankingFunctionRecordingList.append(rf)
                L_current = ConjunctRankConstraintL(L_current, rf)
                old_coef_array.append(rf.coefficients)
            else:
                # the phase reach the bound, should find ranking function here
                print("---------------------LEARN RANKING FUNCTION----------------------")
                print("---------LoopNum ", i)
                print("---------LoopBound ", phaseNum)
                ret, rf = LearnRankerBoundedLoopBody(L_current, x, y)
                if ret == 'FINITE':
                    rankingFunctionRecordingList.append(rf)
                    printSummary(phaseNum + 1, ret, rankingFunctionRecordingList)
                    return 'FINITE'
                elif ret == 'INFINITE':
                    printSummary(phaseNum + 1, ret, rankingFunctionRecordingList)
                    return 'INFANITE'
            i += 1
        print("---------------- LEARNING OVER-------------------")
        print("---------RESULT:", ret, rf)
    printSummary(phaseNum + 1, 'UNKNOWN', rankingFunctionRecordingList)
    return 'UNKNOWN'
'''

def train_multi_ranking_function_incremental(L, x, y, depthBound=2):
    
    print("-------------------START INCREMENTAL LEARNING--------------------")
    i = 0
    ret = 'UNKNOWN'
    L_current = L
    rf_list = []
    while i < depthBound and ret == 'UNKNOWN':
        print("-------------INCREASE TIMES:", i)
        print("--------LEARN BOUNDED")
        ret, rf = LearnRankerBoundedLoopBody(L_current, x, y)
        if(ret == 'FINITE' or ret == 'INFINITE'):
            rf_list.append(rf)
            printSummary(i+1, ret, rf_list)
            return rf_list
        else:
            print("--------LEARN UNBOUNDED")
            # TODO: add loop here for the change of unbound template
            ret, rf = LearnRankerNoBoundLoopBody(L_current, x, y)
            if(isUselessRankingFunction(rf)):
                ret = 'UNKNOWN'
                printSummary(i+1, ret, rf_list)
                return rf_list
            else:
                rf_list.append(rf)
            ret = 'UNKNOWN'
        L_current = ConjunctRankConstraintL(L_current, rf)
        #changeTemplate(L_current, [[1,0,1],[0,1,1],[0,0,1]])
        i += 1
    printSummary(i+1, ret, rf_list)
    return rf_list


def train_multi_ranking_function_backtracking_loopbody(L, x, y, rf_list, templates, templateNum, currentDepth, depthBound):

    print("-------------------START BACKTRACK LEARNING--------------------")
    result = 'UNKNOWN'
    if currentDepth < depthBound:
        for num in range(len(templates)):
            changeTemplate(L, templates[num])
            result, rf = LearnRankerBoundedLoopBody(L, (), ())
            print("-----RESULT:", result, "-------")
            if(result != 'UNKNOWN'):
                rf_list.append(rf)
                return result, rf_list
                
        while templateNum < len(templates):
            print('--------------------- Depth: ', currentDepth, "templateNum:", templateNum, " Learn unbound ---------------------" )
            changeTemplate(L, templates[templateNum])
            ret, rf = LearnRankerNoBoundLoopBody(L, (), ())
            if ret == 'CORRECT':
                rf_list.append(rf)
                L_new = ConjunctRankConstraintL(L, rf)
                result, rf_list = train_multi_ranking_function_backtracking_loopbody(L_new, x, y, rf_list, templates, 0, currentDepth + 1, depthBound)
                print("-----RESULT:", result, "-------")
                if result == 'UNKNOWN':
                    rf_list.pop()
                    templateNum += 1
                else:
                    return result, rf_list
            elif ret == 'INFINITE':
                rf_list.append(rf)
                return 'INFINITE', rf_list
            elif ret == 'FALSE':
                templateNum += 1
        return 'UNKNOWN', rf_list
    elif currentDepth == depthBound:
        while templateNum < len(templates) and result == 'UNKNOWN':
            print('--------------------- Depth: ', currentDepth, "templateNum:", templateNum, " Learn bounded ---------------------" )
            changeTemplate(L, templates[templateNum])
            result, rf = LearnRankerBoundedLoopBody(L, (), ())

            print("-----RESULT:", result, "-------")
            if result != 'UNKNOWN':
                rf_list.append(rf)
                return result, rf_list
            templateNum += 1
        return 'UNKNOWN', rf_list
        # backtracking 
    else:
        # not reachable 
        return 'UNKNOWN', rf_list



def train_multi_ranking_function_backtracking(L, x, y, templates, depthBound):
    i = 1
    result = 'UNKNOWN'
    
    while i <= depthBound and result == 'UNKNOWN':
        rf_list = []
        ret, rf_list = train_multi_ranking_function_backtracking_loopbody(L, x, y, rf_list, templates, 0, 1, i)
        i+=1
    return ret, rf_list



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
    if ret== 'FINITE':
        #print(rf)
        # print('#num_pos = ', rf.get_num_of_pos(), ' #num_neg = ', rf.get_num_of_neg())
        return ret