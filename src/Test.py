'''
Created on Jan 20, 2019

@author: liyong
'''
import numpy as np
from sklearn.svm import LinearSVC
from Loops import L
import time
from z3 import *
import math
from polynomial.Polynomial import Polynomial
from polynomial.Monomial import Monomial
from polynomial.Fraction import Fraction


from Templates import *
from LoopRanker import *
from polynomial.Exponential import Exponential
from NestedRankingFunction import NestedRankingFunction

from program.LoopProgram import LoopProgram

from program.Filter import Filter
import fractions as Frac


import polynomial.Item
import  math

# x, y
m1 = Monomial([1, 0])
m2 = Monomial([1, 1])
m3 = Monomial([0, 1])
dct1 = {}

dct1[m1] = 2
dct1[m2] = 3

p1 = Polynomial(dct1)
dct2 = {}
dct2[m1] = 2
dct2[m2] = 3
dct2[m3] = 1
p2 = Polynomial(dct2)

print(p1)
print(p2)
print(p1 - p2)

print(p2 - p1)

print(p1 + p2)

func = get_polynomial_template(2, 2)
print('template(2, 2) = ', func)

print('template(2, 5) = ', get_polynomial_template(2, 5))

xx = Exponential([2, 1/2])

print(xx)

print(xx.get_value([2, 4]))

fr = Fraction(p1, p2)

print(fr)

m4 = Monomial([0, 0])
dict3 = {}
dict3[m1] = 1
dict3[m4] = 1
pp = Polynomial(dict3)
dict4 = {}
dict4[m3] = 1
dict4[m4] = 1
ppp = Polynomial(dict4)

rf = NestedRankingFunction(
            # list of U(x)
            [
                pp, ppp
            ]
            # list of C
            , [0.001] * 2
            # Delta
            , 0)
rf.set_coefficients([0, 1, 1, 1])
print(rf.z3_verify(2, [0, 1, 1, 1], L[31][-1], L[31][-2]))
print(rf)


### 31

prog = LoopProgram()
prog.add_var('a', 'real')
prog.add_var('b', 'real')
prog.add_loop_condition(lambda x : [x[1] >= 1, x[0] >= x[1]])
prog.add_loop_statement(lambda x : [2 * x[0], 3 * x[1]])
prog.add_loop_smt_condition(lambda x : [x[1] >= 1, x[0] >= x[1]])
prog.add_loop_smt_statement(lambda x : [2 * x[0], 3 * x[1]])

print(prog)

f = Filter({"eq": 4})
print(f(4))

f = Filter(
    {"∨": [
        {"∧": [
            {"≥": 1},
            {"≤": 2},
        ]},
        {"∧": [
            {"≥": 4},
            {"≤": 6},
        ]},
    ]})
print(f(5))

fdict1 = {}
fdict1[m1] = 1

fp1 = Polynomial(fdict1)
fdict2 = {}
fdict2[m3] = 1
fp2 = Polynomial(fdict2)

fr = Fraction(fp1, fp2)
print('frac = ', fr)
fdict3 = {}
fdict3[fr] = 1
frpp = Polynomial(fdict3)
rf = NestedRankingFunction(
            # list of U(x)
            [
                get_fraction_template(2, 0, 1)
            ]
            # list of C
            , [0.001] * 2
            # Delta
            , 0)
rf.set_coefficients([1])
print(rf)
print(rf.z3_verify(2, [1], L[20][-1], L[20][-2]))

print(get_fraction_template(2, 0, 1))


def coef_dot(coef, gx):
    fracs = [Frac.Fraction(v) for v in coef]
    num = [ v.numerator for v in fracs]
    den = [ v.denominator for v in fracs]
    return sum (i[0] * i[1]/ i[2] for i in zip (num, gx, den))

cc = [1.29, 0.9, 0.36]

gx = lambda x : [ 1, x[0], x[0]**2]
x = [z3.Int('x')]

s = z3.Solver()

s.add(coef_dot(cc, gx(x)) <= 3)
result = s.check ()
if result == z3.unsat:
    print(result)
else:
    print(s.model())




