'''
@author Xie Li
'''
import numpy as np
from z3 import *
import os

'''-----------------functions for conjunct to get new L-----------------'''
def coefDotExpr(x, coef, last_coef_list, NumOfVars):
    result = 0
    for i in range(NumOfVars):
        result += coef[i]*x[i]
    result += coef[-1]
    return result

def coefDotExprZ3Constraint(x, coef, last_coef_list, NumOfVars, divideConstant):
    result = RealVal(0)
    for i in range(NumOfVars):
        CoefTemp = RealVal(coef[i])
        lastCoefTemp = RealVal(last_coef_list[i])
        result = Sum(result, Product(CoefTemp, x[i], lastCoefTemp))
    result = Sum(result, Product(RealVal(coef[-1]), RealVal(last_coef_list[-1])))
    #print("-----DOT RESULT: ", result)
    #print(type(result))
    return result < divideConstant

def coefDotExprZ3Arithmetic(x, coef, last_coef_list, NumOfVars):
    result = RealVal(0)
    for i in range(NumOfVars):
        CoefTemp = RealVal(coef[i])
        lastCoefTemp = RealVal(last_coef_list[i])
        result = Sum(result, Product(CoefTemp, x[i], lastCoefTemp))
    result = Sum(result, Product(RealVal(coef[-1]), RealVal(last_coef_list[-1])))
    #print(result)
    #print(type(result))
    return result


def ConjunctRankConstraintL(L_old, rf, print_all, strategy="MINUS"):
    # conjunct the ranking function constrain f <= 0 with the loop guard in L_old
    # to obtain a new loop L_new

    L_new = []
    # find new loop guard
    old_loopGuard = L_old[0]
    NumOfVars = L_old[2]
    coef = rf.coefficients
    addedExp = lambda x: coefDotExpr(x, coef, rf.last_coef_array, NumOfVars)
    if strategy == "ZERO":
        divideConstant = 0
    elif strategy == "MINUS":
        divideConstant = -1
    elif strategy == "POS":
        divideConstant = 1
    elif strategy == "MINI":
        divideConstant = -1
        minPoint = [0 for i in range(NumOfVars)]
        for point in rf.sample_points_list:
            if addedExp(point) < divideConstant:
                divideConstant = addedExp(point)
                minPoint = point
    else:
        divideConstant = -1
    if print_all:
        print("---------DIVIDING CONSTANT:", divideConstant)
    # ATTENTION NOT ROBUST HERE TODO
    rf.coefficients[-1] += -divideConstant/rf.last_coef_array[-1]
    appendConstraint = lambda x : addedExp(x) < divideConstant
    newLoopGuard = lambda x: old_loopGuard(x) and appendConstraint(x)
    #L_new[0]
    L_new.append(newLoopGuard)

    #L_new[1]
    # find new update of the variables
    old_update = L_old[1]
    # the latter part will not happen for the loop guard is updated TODO: check
    new_update = lambda x: old_update(x) if appendConstraint(x) else [x[i] for i in range(len(x))]
    L_new.append(new_update)
    
    #L_new[2]
    # num of var
    L_new.append(L_old[2])
    #L_new[3]
    # num of phases
    L_new.append(L_old[3])
    #L_new[4]
    # template
    L_new.append(L_old[4])



    
    #L_new[5]
    # z3 update
    L_new.append(lambda x: [If(coefDotExprZ3Constraint(x, coef, rf.last_coef_array, NumOfVars, divideConstant), L_old[5](x)[i], x[i]) for i in range(NumOfVars)])
   
    #L_new.append(L_old[5])
    #L_new[6]
    # z3 loop guard
    L_new.append(lambda x: And(coefDotExprZ3Constraint(x, coef, rf.last_coef_array, NumOfVars, divideConstant), L_old[6](x)))
    return L_new
'''-------------------------functions for generating templates lib---------------------------'''
def changeTemplate(L, template):
    L[4] = template

def genListOfVectors(numOfVar, maxPower=1):
    listOfUxVectors = []
    for i in range(numOfVar):
        UxTemplate = []
        for j in range(numOfVar):
            UxTemplate.append(0)
        UxTemplate.append(1)
        UxTemplate[i] = 1
        listOfUxVectors.append(UxTemplate)
    UxTemplate = []
    for j in range(numOfVar):
        UxTemplate.append(0)
    UxTemplate.append(1)
    listOfUxVectors.append(UxTemplate)
    UxTemplate = []
    for k in range(numOfVar+1):
        UxTemplate.append(0)
    listOfUxVectors.append(UxTemplate)
    return listOfUxVectors

def generateTemplateLibSingleFull(numOfVar, maxPower=1):
    # numOfvar represents the maximum diemension of a function
    # maxPower represents the maximum power of a variable, default 1 meaning linear functions
    # for linear template the function will finally generate a list of templates of num 2^varnum
    listOfUxVectors = genListOfVectors(numOfVar, maxPower)
    listOfTemplates = []
    for varId in range(numOfVar):
        item = []
        for itemId in range(numOfVar):
            if itemId == varId:
                item.append(listOfUxVectors[itemId])
            else:
                item.append(listOfUxVectors[-1])
        item.append(listOfUxVectors[-2])
        listOfTemplates.append(item)
    item = []
    for itemId in range(numOfVar + 1):
        item.append(listOfUxVectors[itemId])
    listOfTemplates.append(item)
    return listOfTemplates

def generateTemplateLibFull(numOfVar, maxPower=1):
    listOfUxVectors = genListOfVectors(numOfVar, maxPower)
    listOfTemplates = []
    item = []
    for itemId in range(numOfVar + 1):
        item.append(listOfUxVectors[itemId])
    listOfTemplates.append(item)
    return listOfTemplates


def generateTemplatesStrategy(strategy, numOfVar, maxPower=1):
    if strategy == "FULL":
        return generateTemplateLibFull(numOfVar, maxPower)
    elif strategy == "SINGLEFULL":
        return generateTemplateLibSingleFull(numOfVar, maxPower)
    else:
        return []

def isUselessRankingFunction(rf):
    for c in rf.coefficients:
        if(c != 0):
            return False
    return True

'''--------------------Attributes for testing-------------------'''

TemplatesListTest = generateTemplateLibSingleFull(3)
TemplatesListExp = [
    [[1,0,1],
     [0,1,-4],
     [0,0,1]],
    [[1,0,1],
     [0,1,-2],
     [0,0,1]],
    [[1,0,1],
     [0,1,-1],
     [0,0,1]]
]
TemplatesNondet = generateTemplateLibSingleFull(4)

'''--------------------Print methods-------------------------'''
def printSummary(multidepth, ret, listOfRFs):
    if(ret != "TERMINATE"):
        depth = 0
    else:
        depth = multidepth
    print("--------------------LEARNING MULTIPHASE SUMMARY-------------------")
    print("MULTIPHASE DEPTH: ", depth)
    print("LEARNING RESULT: ", ret)
    print("-----------RANKING FUNCTIONS----------")
    if depth != 0:
        for rf in listOfRFs:
            print(str(rf))
