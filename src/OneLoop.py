from z3 import *

L = [
lambda x :(True and (x[1] >= x[2])),
lambda x :[x[0], (x[1] - x[3]), x[2], (x[3] + 2), ],
4,
0,
lambda x :[x[0], ( x[1]- x[3]), x[2], ( x[3]+ 2), ],
lambda x :(And( True, ( x[1]>= x[2]))),
False,
]
T = [
[1, 0, 0, 0, 0], 
[0, 1, 0, 0, 0], 
[0, 0, 1, 0, 0], 
[0, 0, 0, 1, 0]]
