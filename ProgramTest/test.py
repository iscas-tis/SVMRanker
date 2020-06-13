from z3 import *

L = [
lambda x :(True and (x[0] > (x[1] + x[2]))),
lambda x :[x[0], (x[1] + 1), (x[2] + 1), (x[3] + 1), ],
4,
0,
lambda x :[x[0], ( x[1]+ 1), ( x[2]+ 1), ( x[3]+ 1), ],
lambda x :(And( True, ( x[0]> ( x[1]+ x[2])))),
False,
]
T = [
[1, 0, 0, 0, 0], 
[0, 1, 0, 0, 0], 
[0, 0, 1, 0, 0], 
[0, 0, 0, 1, 0]]
