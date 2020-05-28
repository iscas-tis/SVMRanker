'''
@author Xie Li
'''
from LearnRanker import *
from Loops import L_test
from FindMultiphaseUtil import *
rf = LearnRankerNoBoundLoopBody(L_test, (), ())
print(rf.coefficients)
L_new = ConjunctRankConstraintL(L_test, rf)
rf = LearnRankerNoBoundLoopBody(L_new, (), ())

