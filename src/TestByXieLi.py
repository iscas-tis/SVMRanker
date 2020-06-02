'''
@author Xie Li
'''
from LearnRanker import *
from Loops import L_test, L_hand, L_hand2, L_incremental, L_branch, L_jump
from FindMultiphaseUtil import *
from LearnMultiRanker import *
import os
from z3 import *

#ret, rf = LearnRankerNoBoundLoopBody(L_branch ,(), ())
#print(rf.coefficients)
#L_new = ConjunctRankConstraintL(L_test, rf)
#ret, rf = LearnRankerNoBoundLoopBody(L_test, (), ())
#print(rf.coefficients)
#L_new = ConjunctRankConstraintL(L_test, rf) 
#ret, rf = LearnRankerBoundedLoopBody(L_new, (), ())

#train_multi_ranking_function_incremental(L_jump, (), (), 4)
#generateTemplateLib(3)

#result, rf_list = train_multi_ranking_function_backtracking_loopbody(L_branch, (), (), [], TemplatesListTest, 0, 1, 4)
result, rf_list = train_multi_ranking_function_backtracking(L_jump, (), (), TemplatesListTest, 3)
printSummary(len(rf_list), result, rf_list)