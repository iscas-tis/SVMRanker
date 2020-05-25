import sys
import os, os.path
from io import open
import glob, time

from lark import Lark
# from lark.indenter import Indenter

# __path__ = os.path.dirname(__file__)

#class BoogieIndenter(Indenter):
    # NL_type = '_NEWLINE'
    # OPEN_PAREN_types = ['LPAR', 'LSQB', 'LBRACE']
    # CLOSE_PAREN_types = ['RPAR', 'RSQB', 'RBRACE']
    # INDENT_type = '_INDENT'
    # DEDENT_type = '_DEDENT'
    # tab_len = 8


boogie_parser = Lark(open('bb.lark'), parser="lalr", start='boogie_program')



file = '/home/liyong/git/loopranker/examples/3phase.bpl'
tree = boogie_parser.parse( open(file).read())
print("All grammars parsed successfully: ", tree)