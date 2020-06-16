'''
@author Xie Li
'''
import numpy as np
import time
import sys
import os
from Util import *
from FindMultiphaseUtil import *
from LearnRanker import *

def LearnRankerNoBoundLoopBody(L_test, sample_strategy, print_level, x, y):
    ret = 'UNKNOWN'
    if print_level > 1:
        print("L:",L_test[2])
        print(L_test[3])
        print(L_test[4])
    listOfUxDimension = []
    for i in range(L_test[3]):
        listOfUxDimension.append(L_test[2]+1)
    if print_level > 1:
        print("listOfDimension",listOfUxDimension)
    
    listOfUx, last_coef_array = parse_template_handcraft(L_test[4], L_test[2], listOfUxDimension)
    if print_level > 1:
        print("Last coef array:", last_coef_array)
    rf = NestedNoBoundTemplate(
        listOfUx,
        [0.001] *len(listOfUx),
        last_coef_array
    )
    #ret, new_x, new_y = train_ranking_function(L_test, rf, x, y)
    ret, new_x, new_y = train_ranking_function_strategic(L_test, rf, sample_strategy, print_level, x, y)
    if ret == 'TERMINATE':
        no_bound_return = 'CORRECT'
    elif ret == 'NONTERM':
        no_bound_return = 'NONTERM'
    else:
        no_bound_return = 'FALSE'
    return no_bound_return, rf

def LearnRankerBoundedLoopBody(L_test, sample_strategy, print_level, x, y):
    ret = 'UNKNOWN'
    if print_level > 1:
        print("L[2]:",L_test[2])
        print("L[3]:",L_test[3])
        print("L[4]:",L_test[4])
    listOfUxDimension = []
    for i in range(L_test[3]):
        listOfUxDimension.append(L_test[2]+1)
    if print_level > 1:
        print("listOfDimension",listOfUxDimension)
    listOfUx, last_coef_array = parse_template_handcraft(L_test[4], L_test[2], listOfUxDimension)
    rf = NestedTemplate(
        listOfUx,
        [0.001] *len(listOfUx),
        0,
        last_coef_array
    )
    ret, new_x, new_y = train_ranking_function_strategic(L_test, rf, sample_strategy, print_level, x, y)
    return ret, rf

def train_multi_ranking_function_backtracking_loopbody(L, x, y, rf_list, templates, templateNum, currentDepth, depthBound, sample_strategy, cutting_strategy, print_level):

    if print_level > 0:
        print("-------------------START BACKTRACK LEARNING--------------------")
    result = 'UNKNOWN'
    if currentDepth < depthBound:
        for num in range(len(templates)):
            if print_level > 0:
                print('--------------------- Depth: ', currentDepth, "templateNum:", num, " Learn bounded ---------------------" )
            changeTemplate(L, templates[num])
            result, rf = LearnRankerBoundedLoopBody(L, sample_strategy, print_level, (), ())
            if print_level > 0:
                print("-----RESULT:", result, "-------")
            if(result != 'UNKNOWN'):
                rf_list.append(rf)
                return result, rf_list
                
        while templateNum < len(templates):
            if print_level > 0:
                print('--------------------- Depth: ', currentDepth, "templateNum:", templateNum, " Learn unbound ---------------------" )
            changeTemplate(L, templates[templateNum])
            ret, rf = LearnRankerNoBoundLoopBody(L, sample_strategy, print_level, (), ())
            if ret == 'CORRECT':
                L_new = ConjunctRankConstraintL(L, rf, print_level, cutting_strategy)
                rf_list.append(rf)
                result, rf_list = train_multi_ranking_function_backtracking_loopbody(L_new, x, y, rf_list, templates, 0, currentDepth + 1, depthBound, sample_strategy, cutting_strategy, print_level)
                if print_level > 0:
                    print("-----RESULT:", result, "-------")
                if result == 'UNKNOWN':
                    rf_list.pop()
                    templateNum += 1
                else:
                    return result, rf_list
            elif ret == 'NONTERM':
                rf_list.append(rf)
                rf_list = []
                return 'NONTERM', rf_list
            elif ret == 'FALSE':
                templateNum += 1
        return 'UNKNOWN', rf_list
    elif currentDepth == depthBound:
        while templateNum < len(templates) and result == 'UNKNOWN':
            if print_level > 0:
                print('--------------------- Depth: ', currentDepth, "templateNum:", templateNum, " Learn bounded ---------------------" )
            changeTemplate(L, templates[templateNum])
            result, rf = LearnRankerBoundedLoopBody(L, sample_strategy, print_level, (), ())
            if print_level > 0:
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

def train_multi_ranking_function_backtracking(L, x, y, templates, depthBound, sample_strategy, cutting_strategy, print_level):
    i = 1
    result = 'UNKNOWN'
    
    while i <= depthBound and result == 'UNKNOWN':
        rf_list = []
        ret, rf_list = train_multi_ranking_function_backtracking_loopbody(L, x, y, rf_list, templates, 0, 1, i, sample_strategy, cutting_strategy, print_level)
        i+=1
    return ret, rf_list

def LearnMultiRanker(L, db, sample_strategy, cuttingStrategy, template_strategy, print_level, nestedPhase, x, y):
    L_loop = L
    L_loop[3] = nestedPhase
    #TemplateVector = T
    templateStrategy = template_strategy
    if L[2] < 10:
        templateStrategy = template_strategy
    else:
        templateStrategy = "FULL"
    templatesLib = generateTemplatesStrategy(templateStrategy, L[2])
    L_loop.insert(4, templatesLib[0])

    #print(L_loop)
    result, rf_list = train_multi_ranking_function_backtracking(L, x, y, templatesLib, db, sample_strategy, cuttingStrategy, print_level)
    return result, rf_list
