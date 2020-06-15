from z3 import *

L = [
lambda x :(True and (x[1] < x[0])),
lambda x :[x[0], (x[1] + 1), (x[2] + 1), ],
3,
0,
lambda x :[x[0], ( x[1]+ 1), ( x[2]+ 1), ],
lambda x :(And( True, ( x[1]< x[0]))),
False,
]
T = [
[1, 0, 0, 0], 
[0, 1, 0, 0], 
[0, 0, 1, 0]]
