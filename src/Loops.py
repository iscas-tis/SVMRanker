# -*- coding: <encoding name> -*-
"""
adpated from Yuan Yue's SVM_loops.py

L:
guards
update
number of variables
k
next k paramaters is the U_i(x) for 1<= i <=k
      each matrix of U_i(x) = b0 * (x_0^p00 * x_1^p01.....)+b1 * (x_0^p10 * x_1^p11.....)+.....
          [
            [p00,p01,p02,...,b0],
            [p10,p11,p12,...,b1],
            .......
            [.....]
          ]
          row: every monomial in U_i(x)
          column: the power of each variables, and the coefficient of this monomial(last value).

check--guard

real or integer
"""

import math
from z3 import *
from Templates import *

L = {1: [lambda x: x[0] ** 2 + x[1] ** 2 <= 1,
         lambda x: [x[0] - x[1] ** 2 + 1, x[1] + x[0] ** 2 - 1],
         2,
         1,
         [[0, 0, 1],
          [0, 1, 1],
          [1, 0, 1]],
          #prime condition
         lambda x :[x[0] - x[1] ** 2 + 1, x[1] + x[0] ** 2 - 1],
         lambda x: x[0] ** 2 + x[1] ** 2 <= 1],
     2: [lambda x: x[1] ** 2 + 10 <= x[0] + 6 * x[1] and x[0] ** 2 + 6 <= 4 * x[0] + x[1],
         lambda x: [x[0] + x[1], x[1] - 1],
         2,
         1,
         [[0, 0, 1],
          [0, 1, 1],
          [1, 0, 1]],
          #prime condition
         lambda x :[x[0] + x[1], x[1] - 1],
         lambda x: [x[1] ** 2 + 10 <= x[0] + 6 * x[1], x[0] ** 2 + 6 <= 4 * x[0] + x[1]]],
     3: [lambda x: x[0] - x[1] >= 1 and x[0] + x[1] >= 1 and x[0] <= 10,
         lambda x: [x[1], x[1] - 1],
         2,
         1,
         [[0, 0, 1],
          [0, 2, 1],
          [1, 0, 1]],
          #prime condition
         lambda x :[x[1], x[1] - 1],
         lambda x: [x[0] - x[1] >= 1, x[0] + x[1] >= 1, x[0] <= 10]],
     4: [lambda x: 3 >= x[0] >= 1 - x[1] and x[1] ** 2 <= 1,
         lambda x: [5 * x[0] - x[0] ** 2, x[1] ** 2 + x[1]],
         2,
         1,
         [[0, 0, 1],
          [0, 1, 1],
          [1, 0, 1]],
          #prime condition
         lambda x :[5 * x[0] - x[0] ** 2, x[1] ** 2 + x[1]],
         lambda x: [3 >= x[0], x[0] + x[1] >= 1, x[1] ** 2 <= 1]],
     5: [lambda x: x[0] >= 0 and x[1] - 2 * x[0] >= 1,
         lambda x: [-x[0] ** 2 - 4 * x[1] ** 2 + 1, -x[0] * x[1] - 1],
         2,
         1,
         [[0, 0, 1],
          [0, 1, 1],
          [1, 0, 1]],
          #prime condition
         lambda x :[-x[0] ** 2 - 4 * x[1] ** 2 + 1, -x[0] * x[1] - 1],
         lambda x: [x[0] >= 0, x[1] - 2 * x[0] >= 1]],
     6: [lambda x: x[0] + x[1] >= x[2] ** 4 - x[2] ** 2 + 1 and x[0] ** 2 >= x[2],
         lambda x: [x[0] + x[1], -x[2] - 1, x[2] ** 2 - 2 * x[2]],
         3,
          1,
         [[0, 0, 0, 1],
          [0, 0, 1, 1],
          [0, 1, 0, 1],
          [1, 0, 0, 1]],
          #prime condition
         lambda x :[x[0] + x[1], -x[2] - 1, x[2] ** 2 - 2 * x[2]],
         lambda x: [x[0] + x[1] >= x[2] ** 2 - x[2] + 1, x[0] ** 2 >= x[2]]],
    # x' = x - (2y - 1)^2 + 4, y' = y - 2
    7: [lambda x: x[0] >= x[1],
         lambda x: [x[0] - 4 * x[1] ** 2 + 4 * x[1] + 3, x[1] - 2],
         2,
         1,
         [[0, 0, 1],
          [1, 0, 1],
          [0, 1, 1],
          [0, 2, 1]],
          #prime condition
         lambda x :[x[0] - 4 * x[1] ** 2 + 4 * x[1] + 3, x[1] - 2],
         lambda x: [x[0] >= x[1]]],  # polynomial x[1]**2
     # y^2 >= x^2 - x + 1
     8: [lambda x: x[1] ** 2 >= x[0] ** 2 - x[0] + 1,
         lambda x: [x[0] ** 2 + x[1] + 1, -x[1] + 1],
         2,
         1,
         [[0, 0, 1],
          [0, 2, 1],
          [0, 1, 1],
          [1, 0, 1],
          [2, 0, 1]],
          #prime condition
         lambda x :[x[0] ** 2 + x[1] + 1, -x[1] + 1],
         lambda x: [x[1] >= x[0] ** 2 - x[0] + 1]],  # polynomial x[1]**2
     9: [lambda x: x[0] >= 0,
         lambda x: [x[0] + x[1], x[1] - 1],
         2,
         1,
         [[0, 0, 1],
          [0, 1, 1],
          [0, 2, 1],
          [1, 0, 1]],
          #prime condition
         lambda x :[x[0] + x[1], x[1] - 1],
         lambda x: [x[0] >= 0]],  # polynomial x[1]**2
     10: [lambda x: x[1] ** 2 - x[1] <= x[0],
         lambda x: [x[0] + x[1] - 5, -x[1]],
         2,
         1,
         [[0, 0, 1],
          [0, 1, 1],
          [0, 2, 1],
          [1, 0, 1]],
          #prime condition
         lambda x :[x[0] + x[1] - 5, -x[1]],
         lambda x: [x[1] ** 2 - x[1] <= x[0]]],  # polynomial x[0], x[1], x[2], x[2]**2, x[2]*x[1], x[1]**2
     11: [lambda x: x[0] * x[1] ** 2 >= x[1] ** 4 + 1 and x[1] <= -1,
          lambda x: [x[0] + x[1] - 1 / x[1], x[1] - 1],
          2,
          1,
         [[0, 0, 1],
          [0, 1, 1],
          [1, 2, 1],
          [1, 0, 1],
          [2, 0, 1],
          [0, 2, 1]],
          #prime condition
          lambda x :[x[0] + x[1] - 1 / x[1], x[1] - 1],
          lambda x: [x[0] * x[1] ** 2 >= x[1] ** 4 + 1, x[1] <= -1]],
     12: [lambda x: 1 <= x[0] and x[1] ** 2 + 2 * x[0] <= 3 * x[1],
          lambda x: [1 + 1 / x[0] ** 2, -x[1] * x[0] - 3 * x[1] + x[1] ** 2 + 1],
          2,
          1,
         [[0, 0, 1],
          [0, 1, 1],
          [1, 0, 1]],
          #prime condition
          lambda x :[1 + 1 / x[0] ** 2, -x[1] * x[0] - 3 * x[1] + x[1] ** 2 + 1],
          lambda x: [1 <= x[0], x[1] ** 2 + 2 * x[0] <= 3 * x[1]]],
     13: [lambda x: x[0] >= 0 and 1 + 8 * x[0] ** 3 <= x[1] ** 3 + x[1] - 4 * x[1] ** 2,
          lambda x: [-x[0] ** 2 - 4 * x[1] ** 2 + x[1], -x[1] * x[0] - 1 / (x[1] + 1)],
          2,
          1,
         [[0, 0, 1],
          [0, 1, 1],
          [1, 0, 1]],
          #prime condition
          lambda x :[-x[0] ** 2 - 4 * x[1] ** 2 + x[1], -x[1] * x[0] - 1 / (x[1] + 1)],
          lambda x: [x[0] >= 0, 1 + 8 * x[0] ** 3 <= x[1] ** 3 + x[1] - 4 * x[1] ** 2]],
     14: [lambda x: x[0] >= 0 and x[0] + x[1] >= 0,
          lambda x: [x[0] + x[1] + (x[2] - 1) / (1 + x[2] ** 2), -x[2] * (x[2] + 1) / (1 + x[2] ** 2), x[2] ** 2],
          3,
          1,
         [[0, 0, 0, 1],
          [0, 0, 1, 1],
          [0, 1, 0, 1],
          [1, 0, 0, 1]],
          #prime condition
          lambda x :[x[0] + x[1] + (x[2] - 1) / (1 + x[2] ** 2), -x[2] * (x[2] + 1) / (1 + x[2] ** 2), x[2] ** 2],
          lambda x: [x[0] >= 0, x[0] + x[1] >= 0]],
     15: [lambda x: 5 * x[0] ** 2 + 4 * x[2] ** 2 <= 40 * x[1] and x[1] + x[2] <= -1,
          lambda x: [x[0] + x[1], x[0] + x[2], x[2] - x[2] ** 2 - 1 / x[2] ** 2],
          3,
          1,
         [[0, 0, 0, 1],
          [0, 0, 1, 1],
          [0, 1, 0, 1],
          [1, 0, 0, 1]],
          #prime condition
          lambda x :[x[0] + x[1], x[0] + x[2], x[2] - x[2] ** 2 - 1 / x[2] ** 2],
          lambda x: [5 * x[0] ** 2 + 4 * x[2] ** 2 <= 40 * x[1], x[1] + x[2] <= -1]],
      # TODO
     # 16: [lambda x: 4 * x[0] ** 2 + x[1] ** 2 + 16 <= 16 * x[0] + 6 * x[1] and x[0] + 4 * x[1] >= 4 + (1 + x[1] ** 2)**0.5,
     #      lambda x: [x[0] ** 2 - x[1] ** 2, x[0] + x[1] + (x[0] ** 2 + 1)**0.5],
     #      2,
     #      1,
     #     [[0, 0, 1],
     #      [0, 1, 1],
     #      [1, 0, 1]],
     #      #prime condition
     #      lambda x :[x[0] ** 2 - x[1] ** 2, x[0] + x[1] + (x[0] ** 2 + 1)**0.5],
     #      lambda x: [4 * x[0] ** 2 + x[1] ** 2 + 16 <= 16 * x[0] + 6 * x[1], x[0] + 4 * x[1] >= 4 + (1 + x[1] ** 2) ** 0.5]],
     17: [lambda x: x[1] + 1 <= x[0] and x[1] >= 0,
          lambda x: [1 / x[0] ** 2, x[1] ** 2 + (x[0] - x[1])**0.5],
          2,
          1,
         [[0, 0, 1],
          [0, 1, 1],
          [1, 0, 1]],
          #prime condition
          lambda x :[1 / x[0] ** 2, x[1] ** 2 + (x[0] - x[1])**0.5],
          lambda x: [x[1] + 1 <= x[0], x[1] >= 0]],
     18: [lambda x: 0 <= x[0] and x[1] - 2 * x[0] >= x[2] and x[2] >= 1,
          lambda x: [-x[0] ** 2 - 4 * x[1] ** 2 + x[2] ** 2, -x[0] * x[1] - x[2] ** 2, x[2] ** 2],
          3,
          1,
         [[0, 0, 0, 1],
          [0, 0, 1, 1],
          [0, 1, 0, 1],
          [1, 0, 0, 1]],
          #prime condition
          lambda x :[-x[0] ** 2 - 4 * x[1] ** 2 + x[2] ** 2, -x[0] * x[1] - x[2] ** 2, x[2] ** 2],
          lambda x: [0 <= x[0], x[1] - 2 * x[0] >= x[2], x[2] >= 1]
        ],
     # x = [y, z]
     # loop (y >= 0) { y' = y - z,  z' = z + 1 }
     # 19: [lambda x:  x[0] >= 0,
     #      lambda x: [x[0] - x[1], x[1] + 1],
     #      # number of variables
     #      2,
     #      # number of ranking symbols
     #      2,
     #      # following are k ranking functions
     #      # U_0(x) = 1 * x[0]^0 * x[1]^0 + 1 * x[0]^0 * x[1]^1
     #      # U_0(x) = 1 + z
     #      [
     #       [0, 0, 1],
     #       [0, 1, 1]
     #      ],
     #      # U_1(x) = 1 * x[0]^0 * x[1]^0 + 1 * x[0]^1 * x[1]^0
     #      # U_1(x) = 1 + y
     #      [
     #       [0, 0, 1],
     #       [1, 0, 1]
     #      ],
     #      #prime condition
     #      lambda x :[x[0] - x[1], x[1] + 1],
     #      # 
     #      lambda x: [x[0] >= 0]
     #    ],
        # same as 37
    # 20: [ lambda x : [x[0] >= 1, x[1] >= 1, x[0] >= x[1]],
    #       lambda x : [2 * x[0], 3 * x[1]],
    #       2,
    #       2,
    #       [
    #           [0, 0, 1],
    #           [1/2, 0, 1],
    #           [0, 1/3, 1]
    #       ],
    #       [
    #           [0, 0, 1],
    #           [1/2, 0, 1],
    #           [0, 1/3, 1]
    #       ],
    #       #prime condition
    #       lambda x :[2 * x[0], 3 * x[1]],
    #       #
    #       lambda x: [x[0] >= 1, x[1] >= 1, x[0] >= x[1]]
    #      ],
         #Example 1  ,10
      #X=[n,f,N]
      #loop(f<=N){ n' = n+1;f'=n*f+f;}
     # infinite loop when y = 0, z = 0
      21:[  lambda x :x[1]<=x[2] and x[0]>=1 and x[1] >=1,
            lambda x : [x[0]+1, x[1]*x[0] +x[1], x[2]],
            #number of variables
            3,
            #number of ranking symbles
            1,
            #U_1(x) = 1 * x[0]^0 * x[1]^0 * x[2]^0 + 1 * x[0]^1 * x[1]^0 * x[2]^0 + 1 * x[0]^0 * x[1]^1 * x[2]^0 + 1 * x[0]^0 * x[1]^0 * x[2]^1
            [
              [0,0,0,1],
              [0,0,1,1],
              [0,1,0,1],
              [1,0,0,1],
            ],
            #prime condition
            lambda x :[x[0]+1 , x[1]*x[0] + x[1] ,x[2]],
            #loop condition for Z3
            lambda x : [x[1]<=x[2], x[0]>=1, x[1]>=1]
      ],
      #Example 2
      #X=[x,y]
      #loop(x<y | x>y){ x' = x-1;y'=y+1;}
     # infinite loop : x = -1, y = 1
      # 22:[  lambda x : x[0]<x[1] or x[1]<x[0],
      #       lambda x : [x[0]-1, x[1]+1],
      #       #number of variables
      #       2,
      #       #number of ranking symbles
      #       2,
      #       #U_1(x) = 1 * x[0]^0 * x[1]^0 + 1 * x[0]^1 * x[1]^0 + 1 * x[0]^0 * x[1]^1
      #       [
      #         [0,0,1],
      #         [0,1,1],
      #         [1,0,1]
      #       ],
      #       [
      #         [0,0,1],
      #         [0,1,1],
      #         [1,0,1]
      #       ],
      #       #prime condition
      #       lambda x :[x[0]-1, x[1]+1],
      #       #loop condition for Z3
      #       lambda x : [Or(x[0] < x[1], x[1]<x[0])]
      # ],
      #Example 3
      #X=[x,y,k]
      #loop(x<y & x>y){ k' = k-1; x'=x-1; y' = y+1;}
     # infinite loop with x = -1, y = 1
      # 23:[lambda x : x[2] < x[1] or x[1] < x[2],
      #       lambda x : [x[0]-1, x[1]+1, x[2]-1],
      #       #number of variables
      #       3,
      #       #number of ranking symbles
      #       2,
      #       #U_1(x) = 1 * x[0]^0 * x[1]^0 * x[2]^0 + 1 * x[0]^1 * x[1]^0 * x[2]^0 + 1 * x[0]^0 * x[1]^1 * x[2]^0 + 1 * x[0]^0 * x[1]^0 * x[2]^1
      #       [
      #         [0,0,0,1],
      #         [0,0,1,1],
      #         [0,1,0,1],
      #         [1,0,0,1]
      #       ],
      #       [
      #         [0,0,0,1],
      #         [0,0,1,1],
      #         [0,1,0,1],
      #         [1,0,0,1]
      #       ],
      #       #prime condition
      #       lambda x :[x[0]-1, x[1]+1, x[2]-1],
      #       #loop condition for Z3
      #       lambda x : [Or(x[2] < x[1], x[1] < x[2])]
      # ],
      #Example 5
      #X=[x,y]
      #loop(x>=1 & y>=1){ x' = x-y;}
      24:[lambda x:x[0]>=1 and x[1]>=1 ,
            lambda x : [x[0]-x[1] , x[1] ],
            #number of variables
            2,
            #number of ranking symbles
            1,
            #U_1(x) = 1 * x[0]^0 * x[1]^0 + 1 * x[0]^1 * x[1]^0 + 1 * x[0]^0 * x[1]^1
            [
              [0,0,1],
              [3,0,1]
            ],
            #prime condition
            lambda x :[x[0]-x[1] , x[1]],
            #loop condition for Z3
            lambda x : [x[0]>=1, x[1]>=1]
      ],
        #Example 7
        #X =[q,y,r]
        #loop(y-r <= 0) { r'= r-y; q' = q+1; }
       # infinite loop : r = 1, y = 0
      # 25 : [lambda x: x[1] - x[2] <= 0,
      #       lambda x: [x[0] + 1, x[1], x[2] - x[1]],
      #       # number of variables
      #       3,
      #       #number of ranking symbles
      #       3,
      #       #U_1(x) = 1 * x[0]^0 * x[1]^0 * x[2]^0 + 1 * x[0]^1 * x[1]^0 * x[2]^0 + 1 * x[0]^0 * x[1]^1 * x[2]^0 + 1 * x[0]^0 * x[1]^0 * x[2]^1
      #       [
      #         [0,0,0,1],
      #         [0,0,1,1],
      #         [0,1,0,1],
      #         [1,0,0,1]
      #       ],
      #       [
      #         [0,0,0,1],
      #         [0,0,1,1],
      #         [0,1,0,1],
      #         [1,0,0,1]
      #       ],
      #       [
      #         [0,0,0,1],
      #         [0,0,1,1],
      #         [0,1,0,1],
      #         [1,0,0,1]
      #       ],
      #       #prime condition
      #       lambda x :[x[0]+1,x[1],x[2]-x[1]],
      #       #loop condition for Z3
      #       lambda x : [x[1]-x[2]<=0]
      # ],
      #Example 8
      #X=[x,y,k]
      #loop(x<y || x>y){k' = k-1;x'=x-1;y'=y+1}
      # infinite loop: k = -1,
      # 26:[lambda x: x[0]<x[1] or x[0]>x[1],
      #       lambda x:[x[0]-1, x[1]+1, x[2]-1],
      #       #number of variables
      #       3,
      #       #number of ranking symbles
      #       3,
      #       #U_1(x) = 1 * x[0]^0 * x[1]^0 * x[2]^0 + 1 * x[0]^1 * x[1]^0 * x[2]^0 + 1 * x[0]^0 * x[1]^1 * x[2]^0 + 1 * x[0]^0 * x[1]^0 * x[2]^1
      #       [
      #         [0,0,0,1],
      #         [0,0,1,1],
      #         [0,1,0,1],
      #         [1,0,0,1]
      #       ],
      #       [
      #         [0,0,0,1],
      #         [0,0,1,1],
      #         [0,1,0,1],
      #         [1,0,0,1]
      #       ],
      #       [
      #         [0,0,0,1],
      #         [0,0,1,1],
      #         [0,1,0,1],
      #         [1,0,0,1]
      #       ],
      #       #prime condition
      #       lambda x :[x[0]-1,x[1]+1,x[2]-1],
      #       #loop condition for Z3
      #       lambda x : [Or(x[0]<x[1],x[0]>x[1])]
      # ],
      #Example 9
      #X=[i,j,n]
      #loop(i<0||i>0){if j>0 :j' = j-1; else : j' = n; i' = i-1;}
      27:[lambda x: [x[0] < 0 or x[0] > 0,x[1]>=0,x[0]>=0,x[2]>=x[0],x[2]>=x[1],x[2] ==10],
            lambda x : [x[0] if x[1]>0 else x[0] - 1, x[1]-1 if x[1]>0 else x[2], x[2]],
            #number of variables
            3,
          1,
          # U_1(x) = 1 * x[0]^0 * x[1]^0 * x[2]^0 + 1 * x[0]^1 * x[1]^0 * x[2]^0 + 1 * x[0]^0 * x[1]^1 * x[2]^0 + 1 * x[0]^0 * x[1]^0 * x[2]^1
          [
              [0, 0, 2, 1],
              [1, 0, 1, 1],
              [0, 1, 1, 1],
              [0, 0, 1, 1],
              [2, 0, 0, 1],
              [1, 1, 0, 1],
              [1, 0, 0, 1],
              [0, 2, 0, 1],
              [0, 1, 0, 1],
              [0, 0, 0, 1],
          ], 
            #prime condition
            lambda x :[If(x[1]>0,x[0],x[0]-1),If(x[1]>0,x[1]-1,x[2]),x[2]],
            #loop condition for Z3
            lambda x : [Or(x[0]<0,x[0]>0),x[1]>=0,x[0]>=0,x[2]>=x[0],x[2]>=x[1],x[2] ==10 ],
            False
      ],
      #Example 11
      #X=[x,y,i]
      #loop(x<y){if i>=0 :x' = x+i+1; else : y' = y+i;}
      # linear
      # 28:[lambda x:x[0]<x[1],
      #       lambda x : [x[0]+x[2]+1 if x[2]>=0 else x[0] , x[1] if x[2]>=0 else x[1]+x[2],x[2]],
      #       #number of variables
      #       3,
      #       #number of ranking symbles
      #     1,
      #     # U_1(x) = 1 * x[0]^0 * x[1]^0 * x[2]^0 + 1 * x[0]^1 * x[1]^0 * x[2]^0 + 1 * x[0]^0 * x[1]^1 * x[2]^0 + 1 * x[0]^0 * x[1]^0 * x[2]^1
      #     [
      #         [0, 1, 0, 1],
      #         [1, 0, 0, 1]
      #     ],
      #       #prime condition
      #       lambda x :[If(x[2]>=0,x[0]+x[2]+1,x[0]),If(x[2]>=0,x[1],x[1]+x[2]),x[2]],
      #       #loop condition for Z3
      #       lambda x : [x[0]<x[1]]
      # ],
      #Example 15
      #X=[a,x]
      #loop(a>=0 & a<1 &0.1 <= x & x<=1){x' = a*x*(1-x)}
      29:[lambda x:x[0]>=0 and x[0]<1 and 0.1 <=x[1] and x[1]<=1,
            lambda x : [x[0],x[0]*x[1]*(1-x[1])],
            #number of variables
            2,
            #number of ranking symbles
            1,
            #U_1(x) = 1 * x[0]^0 * x[1]^0  + 1 * x[0]^1 * x[1]^0 + 1 * x[0]^0 * x[1]^1
            [
              [0,0,1],
              [0,1,1],
            ],
            #prime condition
            lambda x :[x[0],x[0]*x[1]*(1-x[1])],
            #loop condition for Z3
            lambda x : [x[0]>=0,x[0]<1,0.1 <=x[1],x[1]<=1]
      ],

     # Examples from ranking templates
     # Example 2.5
# cannot be solved by lassoranker
# void f(int q, int y)
# {
#    while(q > 0) {
#        if (y > 0) {
#            q = q - y - 1;
#        }else {
#           q = q + y -1;
#        }
#    }
# }
     # (q > 0) : q = q - y - 1 if y > 0 else q = q + y -1
     30 : [
            lambda x : [x[0] > 0],
            lambda x : [x[0] - x[1] - 1 if x[1] > 0 else x[0] + x[1] - 1, x[1]],
            2,
            1,
            [
              [0,0,1],
              [3,0,1],
              [0,2,1]
            ],
            #prime condition
            lambda x :[If(x[1] > 0, x[0] - x[1] - 1, x[0] + x[1] - 1), x[1]],
            #loop condition for Z3
            lambda x : [x[0] > 0],
            False
        ],
     # Example 4.6
# cannot be solved by lassoranker
# void f(int q, int y)
# {
#    while(q > 0) {
#        if (y > 0) {
#            y = 0;
#        }else {
#            y = y - 1;
#           q = q -1;
#        }
#    }
# }
     # (q > 0) :  if y > 0 else q = q + y -1
     # f1 = y, f2 = q + 1
     #lnear
     # 31 : [
     #        lambda x : [x[0] > 0],
     #        lambda x : [x[0] if x[1] > 0 else x[0] - 1, 0 if x[1] > 0 else x[1] - 1],
     #        2,
     #        1,
     #     [
     #         [0, 0, 1],
     #         [1, 0, 1]
     #     ],
     #     # prime condition
     #     lambda x: [If(x[1] > 0, x[0], x[0] - 1), If(x[1] > 0, 0, x[1] - 1)],
     #     # loop condition for Z3
     #     lambda x: [x[0] > 0]
     # ],

# Example 4.12
#    void f(float q, float
# a, float
# b)
# {
# while (q > 0)
#    {
#        q = q + a - 1;
#    a = 0.6 * a - 0.8 * b;
#    b = 0.8 * a + 0.6 * b;
#    }
#    }
# f1 (q, a, b) = 2q + a - 2b,
# f2 (q, a, b) = 4q + 5a,
# and f 3 (q, a, b) = 5q.
#linear
     # 32 : [
     #     lambda x : [x[0] > 0],
     #     lambda x : [x[0] + x[1] - 1, 3/5 * x[1] - 4/5 * x[2], 4/5 * x[1] + 3/5 * x[2]],
     #     3,
     #     3,
     #      [
     #          [0, 0, 1, -2],
     #          [0, 1, 0, 1],
     #          [1, 0, 0, 2]
     #      ],
     #      [
     #          [0, 1, 0, 5],
     #          [1, 0, 0, 4]
     #      ],
     #      [
     #          [1, 0, 0, 5]
     #      ],
     #     # updates
     #     lambda x : [x[0] + x[1] - 1, 3/5 * x[1] - 4/5 * x[2], 4/5 * x[1] + 3/5 * x[2]],
     #     lambda x : [x[0] > 0]

     # ],
     #Linear
     # 33 : [
     #     lambda x : [x[0] > 0],
     #     lambda x : [x[0] + x[1], x[1] + x[2], x[2] - 1],
     #     3,
     #     3,
     #        [
     #          [0, 0, 0, 1],
     #          [0, 0, 1, 1],
     #          [0, 1, 0, 1],
     #          [1, 0, 0, 1]
     #      ],
     #      [
     #          [0, 0, 0, 1],
     #          [0, 0, 1, 1],
     #          [0, 1, 0, 1],
     #          [1, 0, 0, 1]
     #      ],
     #      [
     #          [0, 0, 0, 1],
     #          [0, 0, 1, 1],
     #          [0, 1, 0, 1],
     #          [1, 0, 0, 1]
     #      ],
     #     lambda x: [x[0] + x[1], x[1] + x[2], x[2] - 1],
     #     lambda x: [x[0] > 0],
     # ],
#linear
     # 34 : [
     #     lambda x : [x[0] > 0, x[0] != 0],
     #     lambda x : [x[0] - 2],
     #     1,
     #     1,
     #     [
     #         [0, 1],
     #         [1, 1]
     #     ],
     #     lambda x: [x[0] - 2],
     #     lambda x : [x[0] > 0, Not(x[0] == 0)]
     # ],

    # integer terminate, real non-terminating
     35 : [
         lambda x : x[0] != 0,
         lambda x : [-x[0] + 1 if x[0] > 0 else -x[0] - 1],
         1,
         1,
         [
             [0, 1],
             # [1, 1],
             [2, 1]
         ],
         lambda x : [If(x[0] > 0, -x[0] + 1, -x[0] - 1)],
         lambda x : [Not(x[0] == 0)],
         False
     ],

     # can not solve
     # integer terminate, real non-terminating
     # 36: [
     #     lambda x: x[0] != 0,
     #     lambda x: [-x[0] - 2 if x[0] > 0 else -x[0] - 3],
     #     1,
     #     2,
     #     [
     #         [0, 1],
     #         [1, 1],
     #         [2, 1]
     #     ],
     #     [
     #         [0, 1],
     #         [1, 1],
     #         [2, 1]
     #     ],
     #     lambda x: [If(x[0] > 0, -x[0] - 2, -x[0] - 3)],
     #     lambda x: [x[0] != 0],
     #     False
     # ],
     #####
     # while(x0 >=1 and x1>=x0){x1 = 2*x1; x0 = 3 * x0;}
     #  r(x,y) = x/y
     37:[
     lambda x: x[0] >=1 and x[1] >= x[0],
     lambda x: [3*x[0], 2*x[1]],
     2,
     1,
     [
     [-1,1,1],
     ],
     lambda x: [3*x[0], 2*x[1]],
     lambda x: [And(x[0] >=1 , x[1] >= x[0])],
     ],
     #Ex8. {x>=0,y>=0,x1=-x-3*y+2,y1=-4*x^2+y-1}  
     38:[
     lambda x: x[0] >=0 and x[1]>=0,
     lambda x: [-x[0]-3*x[1]+2, -4*x[0]**2+x[1]-1],
     2,
     1,
     [
     [3,0,1],
     [0,1,1]
     ],
     lambda x: [-x[0]-3*x[1]+2, -4*x[0]**2+x[1]-1],
     lambda x: And(x[0] >=0 , x[1]>=0),
     ],
     #TODO
     #Ex7. {x>=0, y>=0, x1=-x^3-4*y-3*x+1, y1=-x-y} 
     # 39:[
     # lambda x: x[0]>=0 and x[1]>=0,
     # lambda x: [-x[0]**3-4*x[1]-3*x[0]+1, -x[0]-x[1]],
     # 2,
     # lambda x: [-x[0]**3-4*x[1]-3*x[0]+1, -x[0]-x[1]],
     # lambda x: And(x[0]>=0 , x[1]>=0),
     # ],

     }


 