'''
Created on Jan 22, 2019

@author: liyong
'''


import numpy as np
from polynomial.Monomial import Monomial
from polynomial.Polynomial import Polynomial
from polynomial.Fraction import Fraction


'''
set all ranking function as one template
 1 + X + 
'''


def get_polynomial_template(num_of_vars, max_power):

    if max_power == 0:
        return None

    mono1 = np.zeros(num_of_vars)
    # np.append(1, mono1)
    poly_dict = {}
    m0 = Monomial(list(mono1))
    poly_dict[m0] = 1

    for var in range(num_of_vars):
        mono2 = np.zeros(num_of_vars)
        mono2[var] = 1
        # np.append(1, mono2)
        m1 = Monomial(list(mono2))
        poly_dict[m1] = 1

    if max_power == 1:
        return Polynomial(poly_dict)

    '''
    for var1 in range(num_of_vars):
        for var2 in range(var1, num_of_vars):
            # 0 - var1
            mono = np.zeros(num_of_vars)
            mono[var1] += 1
            mono[var2] += 1
            # np.append(1, mono)
            mat.append(list(mono) + [1])
            print(mono, ",", var1, ",", var2)
    if max_power == 2:
        return mat
    '''
    # >= 2-dimensional
    for var1 in range(num_of_vars):
        for d in range(2, (max_power + 1)):
            mono = np.zeros(num_of_vars)
            mono[var1] = d
            md = Monomial(list(mono))
            poly_dict[md] = 1

    return Polynomial(poly_dict)


def get_fraction_template(num_of_vars, var1, var2):
    # only allow simple fractions like x/y

    mono = np.zeros(num_of_vars)
    mono[var1] = 1
    mvar1 = Monomial(list(mono))
    num = Polynomial({mvar1 : 1})
    mono = np.zeros(num_of_vars)
    mono[var2] = 1
    mvar2 = Monomial(list(mono))
    den = Polynomial({mvar2 : 1})
    frac = Fraction(num, den)

    return Polynomial({frac : 1})