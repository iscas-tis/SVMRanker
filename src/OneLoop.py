from z3 import *

L = [
lambda x :(True and (((4 * x[0]) + x[1]) >= 1)),
lambda x :[((4 * x[1]) - (2 * x[0])), (4 * x[0]), x[0], ],
3,
0,
lambda x :[( ( 4* x[1])- ( 2* x[0])), ( 4* x[0]), x[0], ],
lambda x :(And( True, ( ( ( 4* x[0])+ x[1])>= 1))),
False,
]
T = [
[1, 0, 0, 0], 
[0, 1, 0, 0], 
[0, 0, 1, 0]]
