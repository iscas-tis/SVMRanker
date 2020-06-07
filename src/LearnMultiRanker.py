'''
@author Xie Li
'''
import numpy as np
from OneLoop import L, T
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
    
    listOfUx, last_coef_array = parse_template_handcraft(L_test[4], L_test[2], listOfUxDimension)
    print("Last coef array:", last_coef_array)
    rf = NestedNoBoundTemplate(
        listOfUx,
        [0.001] *len(listOfUx),
        last_coef_array
    )
    #ret, new_x, new_y = train_ranking_function(L_test, rf, x, y)
    ret, new_x, new_y = train_ranking_function_strategic(L_test, rf, x, y)
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
    print("UX DIMENSION: ", L_test[3])
    for i in range(L_test[3]):
        listOfUxDimension.append(L_test[2]+1)
    print("listOfDimension",listOfUxDimension)
    listOfUx, last_coef_array = parse_template_handcraft(L_test[4], L_test[2], listOfUxDimension)
    rf = NestedTemplate(
        listOfUx,
        [0.001] *len(listOfUx),
        0,
        last_coef_array
    )
    ret, new_x, new_y = train_ranking_function_strategic(L_test, rf, x, y)
    return ret, rf

def train_multi_ranking_function_incremental(L, x, y, depthBound=2, strategic="MINUS"):
    
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
        L_current = ConjunctRankConstraintL(L_current, rf, strategic)
        #changeTemplate(L_current, [[1,0,1],[0,1,1],[0,0,1]])
        i += 1
    printSummary(i+1, ret, rf_list)
    return rf_list


def train_multi_ranking_function_backtracking_loopbody(L, x, y, rf_list, templates, templateNum, currentDepth, depthBound, strategic="MINUS"):

    print("-------------------START BACKTRACK LEARNING--------------------")
    result = 'UNKNOWN'
    if currentDepth < depthBound:
        for num in range(len(templates)):
            print('--------------------- Depth: ', currentDepth, "templateNum:", num, " Learn bounded ---------------------" )
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
                L_new = ConjunctRankConstraintL(L, rf, strategic)
                rf_list.append(rf)
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



def train_multi_ranking_function_backtracking(L, x, y, templates, depthBound, strategic="MINUS"):
    i = 1
    result = 'UNKNOWN'
    
    while i <= depthBound and result == 'UNKNOWN':
        rf_list = []
        ret, rf_list = train_multi_ranking_function_backtracking_loopbody(L, x, y, rf_list, templates, 0, 1, i, strategic)
        i+=1
    return ret, rf_list





'''
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
'''