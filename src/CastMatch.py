#! /usr/bin/env python
from pycparser import c_parser
from pycparser.c_ast import Node, Decl, TypeDecl, FuncDecl, IdentifierType,\
        FuncDef, ArrayDecl, Constant, FuncCall, ArrayRef, ID, UnaryOp,\
        BinaryOp,\
        If, Compound, Label, Assignment, Return, For, While
from argparse import ArgumentParser
from copy import deepcopy, copy
import sys
import re

class Var:
    def __init__(self, name, optional=False):
        self._name = name
        self._optional = optional

    def __hash__(self):
        return -1 * hash(self._name)

    def __eq__(self, other):
        if not isinstance(other, Var):
            return False
        return self._name == other._name

    def __repr__(self):
        return "Var({})".format(self._name)

    def is_optional(self):
        return self._optional

    def show(self, *args, **kwargs):
        return str(self)

    def instantiate(self, suffix):
        return Var(self._name + suffix, self._optional)

    def __iter__(self):
        return iter([])


class Substitution(dict):
    def lookup(self, arg, default=None):
        if isinstance(arg, Var):
            return self.get(arg, default)
        elif isinstance(arg, str):
            return self.get(Var(arg), default)
        else:
            raise Exception("Bad Arg: " + repr(arg))


def NYI(ast):
    print("Can't handle: ")
    ast.show()
    assert False


def substitute(ast, subst):
    if isinstance(ast, Var):
        if ast in subst:
            return subst[ast]

        return ast

    if isinstance(ast, Node):
        res = deepcopy(ast)

        for attr in ast.attr_names:
            setattr(res, attr, substitute(getattr(ast, attr), subst))

        for (idx, (name, child)) in enumerate(ast.children()):
            if child in subst:
                res.children()[idx] = (name, substitute(child, subst))

        return res

    return ast


def add_to_substitution(subst, a, b):
    assert isinstance(a, Var)
    subst[a] = b


def unify(ast1, ast2, subst=None):
    if subst is None:
        subst = Substitution()

    ast1 = substitute(ast1, subst)
    ast2 = substitute(ast2, subst)

    if isinstance(ast2, Var):
        t = ast1
        ast1 = ast2
        ast2 = t

    if isinstance(ast1, Var):
        if not ast1.is_optional() and ast2 is None:
            print("Required var {} not matched to anything".format(ast1))
            return None
        add_to_substitution(subst, ast1, ast2)
        return subst

    if (ast1.__class__ != ast2.__class__):
        return None

    for attr in set(ast1.attr_names).union(ast1.attr_names):
        attr1 = substitute(getattr(ast1, attr), subst)
        attr2 = substitute(getattr(ast2, attr), subst)

        if (isinstance(attr2, Var)):
            t = attr1
            attr1 = attr2
            attr2 = t

        if (isinstance(attr1, Var)):
            add_to_substitution(subst, attr1, attr2)
        else:
            if attr1 != attr2:
                print("Different attrs: ", attr1, attr2)
                return None

    def aggregate_children(children):
        res = {}
        arr_pat = re.compile('(^[^\[]*)\[([0-9]*)\]$')
        for (name, child) in children:
            m = arr_pat.match(name)
            if (m is not None):
                t = m.groups()[0] + "[*]"
                if t not in res:
                    res[t] = {}
                res[t][int(m.groups()[1])] = child
            else:
                res[name] = child
        return res

    def is_child_req(child):
        if isinstance(child, Var) and child.is_optional():
            return False

        if isinstance(child, dict) and len(child) == 1 and\
                isinstance(child[0], Var) and child[0].is_optional():
                    return False

        return True

    ast1_children = aggregate_children(ast1.children())
    ast2_children = aggregate_children(ast2.children())

    for name in set(ast1_children.keys()).union(list(ast2_children.keys())):
        child1 = ast1_children.get(name, None)
        child2 = ast2_children.get(name, None)

        if isinstance(child2, dict):
            t = child1
            child1 = child2
            child2 = t

        if isinstance(child1, dict) and isinstance(child2, dict):
            if set(child1.keys()) == set(child2.keys()):
                for idx in list(child1.keys()):
                    subst = unify(child1[idx], child2[idx], subst)
            elif (len(list(child1.keys()))) == 1 or (len(list(child2.keys()))) == 1:
                if len(list(child2.keys())) == 1:
                    t = child1
                    child1 = child2
                    child2 = t

                child1_subp = child1[list(child1.keys())[0]]
                for (idx, child) in list(child2.items()):
                    suffix = "[{}]".format(idx)
                    new_subst = unify(child1_subp, child, copy(subst))
                    new_keys = set(new_subst.keys()).difference(list(subst.keys()))
                    for new_k in new_keys:
                        subst[new_k.instantiate(suffix)] = new_subst[new_k]
            else:
                return None
        elif isinstance(child1, dict) and len(child1) == 1 and \
                child1[0].is_optional() and child2 is None:
            # Optional list var matched with None
            continue
        else:
            subst = unify(child1, child2, subst)

        if subst is None:
            return subst

    return subst
