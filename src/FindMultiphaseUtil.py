import numpy as np
from z3 import *
import os


def ConjunctRankConstraintL(L_old, rf):
    # conjunct the ranking function constrain f <= 0 with the loop guard in L_old
    # to obtain a new loop L_new

    L_new = []
    # find new loop guard
    old_loopGuard = L_old[0]
    NumOfVars = L_old[2]
    coef = rf.coefficients
    addedExp = [lambda x: 0]
    for i in range(NumOfVars + 1):
        addedExp.append(lambda x: addedExp[0](x) + coef[i-1]*x[i-1])
    appendConstraint = lambda x : addedExp[NumOfVars+1](x) <= 0
    newLoopGuard = lambda x: old_loopGuard(x) and appendConstraint(x)
    #L_new[0]
    L_new.append(newLoopGuard)

    #L_new[1]
    # find new update of the variables
    old_update = L_old[1]
    # the latter part will not happen for the loop guard is updated TODO: check
    new_update = lambda x: old_update(x) if appendConstraint(x) else [x[0], x[1]]
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
    L_new.append(lambda x: [If(appendConstraint(x), update, [x[i-1] for i in range(NumOfVars)]) for update in L_old[5](x)])
    #L_new[6]
    # z3 loop guard
    L_new.append(lambda x: And(appendConstraint(x), L_old[6]))
    return L_new

    

