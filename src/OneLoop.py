from z3 import *

L = [
lambda x :(True and (x[0] > 0)),
lambda x :[(x[0] + 1), ],
1,
0,
lambda x :[( x[0]+ 1), ],
lambda x :(And( True, ( x[0]> 0))),
False,
]
