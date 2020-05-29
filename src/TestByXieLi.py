'''
@author Xie Li
'''
from LearnRanker import *
from Loops import L_test
from FindMultiphaseUtil import *
from LearnMultiRanker import *
import os
from z3 import *
'''
ret, rf = LearnRankerNoBoundLoopBody(L_test, (), ())
print(rf.coefficients)
L_new = ConjunctRankConstraintL(L_test, rf)
ret, rf = LearnRankerNoBoundLoopBody(L_test, (), ())
print(rf.coefficients)
L_new = ConjunctRankConstraintL(L_test, rf) 
ret, rf = LearnRankerBoundedLoopBody(L_test, (), ())
'''
LearnMultiRanker(L_test, (), ())