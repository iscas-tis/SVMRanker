'''
Program variables
'''

from z3 import *


class ProgramVar:

    def __init__(self, name, type):
        self.name = name
        self.type = type

    def get_smt_var(self):
        if self.type == 'real':
            return z3.Real(self.name)
        elif self.type == 'int':
            return z3.Int(self.name)
        else:
            return None

