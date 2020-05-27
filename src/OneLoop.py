from z3 import *

L = {1: [lambda x : x[0] > 0 or x[1] > 0, 
         lambda x : [x[0], x[1] - 1,
         2,
         2,
         [[0, 0, 1],
          [0, 1, 1],
          [1, 0, 1]]
         ],
         lambda x : [x[0], x[1] - 1],
         lambda x : x[0] > 0 or x[1] > 0]
         }