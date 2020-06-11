'''
@author Xie Li
'''
from LearnRanker import *
from Loops import L_test, L_hand, L_hand2, L_incremental, L_branch, L_jump, L_nondet
from FindMultiphaseUtil import *
from LearnMultiRanker import *
from BoogieParser import *
import os
import ast
import codegen
from z3 import *
'''
ret, rf = LearnRankerNoBoundLoopBody(L_nondet ,(), ())
print(rf.coefficients)
L_new = ConjunctRankConstraintL(L_test, rf)
ret, rf = LearnRankerNoBoundLoopBody(L_new, (), ())
print(rf.coefficients)
L_new = ConjunctRankConstraintL(L_test, rf) 
ret, rf = LearnRankerBoundedLoopBody(L_new, (), ())
'''
#train_multi_ranking_function_incremental(L_nondet, (), (), 4)
#generateTemplateLib(2)

#result, rf_list = train_multi_ranking_function_backtracking_loopbody(L_incremental, (), (), [], TemplatesListExp, 0, 1, 5)
#result, rf_list = train_multi_ranking_function_backtracking(L_nondet, (), (), generateTemplateLibSingleFull(L_nondet[2]), 3, "MINI")
#printSummary(len(rf_list), result, rf_list)
parseBoogieProgram("../ProgramTest/0.bpl")
#fillOneLoop()