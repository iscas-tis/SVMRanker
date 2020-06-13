from z3 import *

L = [
lambda x :(True and (x[0] <= 0)),
lambda x :[x[0], (x[1] + x[0]), ],
2,
0,
lambda x :[x[0], ( x[1]+ x[0]), ],
lambda x :(And( True, ( x[0]<= 0))),
False,
]
