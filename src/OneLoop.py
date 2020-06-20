from z3 import *

L = [
lambda x :(((True and (True and (x[0] > 0)) ) if (x[0] > 0) else (True and (True and (not(x[0] > 0))) ) ) and (True and (x[0] != 0)) ),
lambda x :[((1 - x[0]) if (x[0] > 0) else (-1 - x[0]) ), ],
1,
0,
lambda x :[If(( x[0]> 0), ( 1- x[0]), ( -1- x[0]) ), ],
lambda x :And(If(( x[0]> 0), And(True, (And( True, ( x[0]> 0))) ), And(True, (And( True, (Not(x[0] > 0)))) ) ), (And( True, ( x[0]!= 0))) ),
False,
]
