#! /usr/bin/env python
from pycparser import c_parser
from pycparser.c_ast import Node, Decl, TypeDecl, FuncDecl, IdentifierType,\
        FuncDef, ArrayDecl, Constant, FuncCall, ArrayRef, ID, UnaryOp,\
        BinaryOp,\
        If, Compound, Label, Assignment, Return, For, While
from argparse import ArgumentParser
from copy import deepcopy, copy
from CastMatch import *
import sys
import re

tabsp=2


def translate_FunDecl(c_ast):
    args = []
    if c_ast.args is not None:
        for a in c_ast.args.params:
            args.append(translate_Decl(a))

    subst = unify(c_ast.type, TypeDecl(Var("declname"),
                                       [],
                                       IdentifierType(Var("ret_type"))))

    name = subst.lookup("declname")
    ret_type = subst.lookup("ret_type")
    return (name, args, ret_type)


def translate_typ(c_ast):
    if isinstance(c_ast, FuncDecl):
        return translate_FunDecl(c_ast)
    elif isinstance(c_ast, TypeDecl):
        pat = TypeDecl(Var("declname"), [], IdentifierType(Var("names")))
        t = unify(pat, c_ast)
        return t.lookup("names")
    elif isinstance(c_ast, ArrayDecl):
        pat = ArrayDecl(Var("element_type"), Var("dim", True), [])
        t = unify(pat, c_ast)
        elem_typ = translate_typ(t.lookup("element_type"))
        return (elem_typ, t.lookup("dim", None))
    else:
        NYI(c_ast)


def translate_exp(c_ast):
    if isinstance(c_ast, Constant):
        return str(c_ast.value)
    elif isinstance(c_ast, FuncCall):
        args = []
        if c_ast.args is not None:
            for arg in c_ast.args.exprs:
                args.append(translate_exp(arg))
        return "{}({})".format(c_ast.name.name, ",".join(args))
    elif isinstance(c_ast, ArrayRef):
        arr = translate_exp(c_ast.name)
        subs = translate_exp(c_ast.subscript)
        return "{}[{}]".format(arr, subs)
    elif isinstance(c_ast, ID):
        return c_ast.name
    elif isinstance(c_ast, UnaryOp):
        inner = translate_exp(c_ast.expr)
        op = {
            "!": "!"
        }[c_ast.op]

        return "{}({})".format(op, inner)
    elif isinstance(c_ast, BinaryOp):
        left = translate_exp(c_ast.left)
        right = translate_exp(c_ast.right)
        op = {
            "+": "+",
            "-": "-",
            "*": "*",
            "%": "mod",
            "/": "div",
            "<": "<",
            ">": ">",
            ">=": ">=",
            "<=": "<=",
            "==": "==",
            "!=": "!=",
            "||": "||",
            "&&": "&&",
        }[c_ast.op]
        return "({}{}{})".format(left, op, right)
    else:
        NYI(c_ast)


def translate_Decl(c_ast):
    pat = Decl(Var("name"), [], [], [], Var("type"), Var("init", True), None)
    subst = unify(pat, c_ast)
    if subst is None:
        pat.show()
        c_ast.show()
    name = subst.lookup("name")
    raw_typ = subst.lookup("type")
    raw_init = subst.lookup("init")

    typ = translate_typ(raw_typ)
    if raw_init is not None:
        init = translate_exp(raw_init)
    else:
        init = None

    return (name, typ, init)


class Ctx:
  def __init__(self, indent, renames, trivial_inv):
    self._indent = indent
    self._renames = renames
    self._trivial_inv = trivial_inv

  def indent(self):
    c = Ctx(self._indent + tabsp, self._renames, self._trivial_inv)
    return c


def translate_stmt(c_ast, ctx):
    istr = " "*ctx._indent
    if isinstance(c_ast, Compound):
        stmts = [translate_stmt(x, ctx) for x in c_ast.block_items]
        stmts = [x for x in stmts if len(x.strip()) > 0]
        return "\n".join(stmts)
    elif isinstance(c_ast, Decl):
        t = translate_Decl(c_ast)
        if t[2] is not None:
            return istr + "{} := {};".format(t[0], t[2])
        else:
            return istr + ""
    elif isinstance(c_ast, If):
        cond = translate_exp(c_ast.cond)
        iftrue = translate_stmt(c_ast.iftrue, ctx.indent())
        if c_ast.iffalse is None:
            return istr + "if ({})\n" .format(cond) +\
                   istr + "{\n" + \
                              iftrue + \
                   istr + "}\n"
        else:
            iffalse = translate_stmt(c_ast.iffalse, ctx.indent())
            return istr + "if ({})\n" .format(cond) + \
                   istr + "{\n" + \
                              iftrue + \
                   istr + "} else {\n" +\
                              iffalse + \
                   istr + "}\n"
    elif isinstance(c_ast, Label):
        inner = translate_stmt(c_ast.stmt, ctx)
        return istr + "{}: {}".format(c_ast.name, inner)
    elif isinstance(c_ast, FuncCall):
        if c_ast.name.name in renames:
            c_ast.name.name = renames[c_ast.name.name]
        return istr + translate_exp(c_ast) + ";"
    elif isinstance(c_ast, Assignment):
        lhs = translate_exp(c_ast.lvalue)
        rhs = translate_exp(c_ast.rvalue)
        if c_ast.op == "=":
            return istr + "{} := {};".format(lhs, rhs)
        else:
            NYI(c_ast)
    elif isinstance(c_ast, Return):
        e = translate_exp(c_ast.expr)
        return ""
    elif isinstance(c_ast, For):
        init = translate_stmt(c_ast.init, ctx)
        cond = translate_exp(c_ast.cond)
        nxt = translate_stmt(c_ast.__next__, ctx.indent())
        body = translate_stmt(c_ast.stmt, ctx.indent())
        inv_str = ""
        return "{}\n".format(init) +\
               istr + "while ({})\n{}".format(cond, inv_str) + \
               istr + "{\n" + \
                        body + "\n" +\
                        nxt + "\n" +\
               istr + "}"
    elif isinstance(c_ast, While):
        cond = translate_exp(c_ast.cond)
        body = translate_stmt(c_ast.stmt, ctx)
        inv_str = ""
        return istr + "while ({})\n{}".format(cond, inv_str) + \
               istr + "{\n" +\
               body +\
               istr + "}\n"
    elif isinstance(c_ast, UnaryOp):
        inner = translate_exp(c_ast.expr)
        if c_ast.op == "p++":
            return istr + "{} := {} + 1;".format(inner, inner)
        if c_ast.op == "p--":
            return istr + "{} := {} - 1;".format(inner, inner)
        else:
            NYI(c_ast)
    else:
        NYI(c_ast)


def format_typ(typ):
    if typ == ["int"]:
        return "int"
    elif isinstance(typ, tuple):
        return "[int]{}".format(format_typ(typ[0]))
    else:
        NYI(typ)


def translate_FuncDef(c_ast, ctx):
    decl = translate_Decl(c_ast.decl)
    decls = []
    if c_ast.param_decls is not None:
        NYI(c_ast.param_decls)
    stmts = [x for (_, x) in c_ast.body.children()]

    # Step 0: Build header:
    name = decl[0]
    if decl[1][2] != ['void']:
        ret_t = format_typ(decl[1][2])
    else:
        ret_t = None

    param_list = ", ".join("{}: {}".format(name, format_typ(typ))
                           for (name, typ, init) in decl[1][1])
    header = "procedure {}({})".format(name, param_list)

    # Step 1. Accumulate all definitions
    for stmt in stmts:
        if not isinstance(stmt, Decl):
            continue

        t = translate_Decl(stmt)
        decls.append(t)

    dec_str = ";\n".join("{}var {}: {}".format(" "*tabsp, name,
        format_typ(typ)) for (name, typ, init) in decls)

    # Step 2. Walk over each statement and translate:
    body = translate_stmt(c_ast.body, ctx.indent())

    if len(dec_str.strip()) > 0:
        dec_str += ";\n"
    proc = header + "\n{\n" + dec_str + body + "\n}"
    return proc


if __name__ == "__main__":
    p = ArgumentParser(description="convert a C file to Boogie.")
    p.add_argument('input', type=str, help='Input C file')
    p.add_argument('output', type=str, help='Output Boogie file')
    p.add_argument('--skip-methods', type=str, nargs="+",
                   help='Methods names which to omit', default=[])
    p.add_argument('--assert-method', type=str,
            help='Name of the C method equivalent to assert', required=True)
    p.add_argument('--assume-method', type=str,
            help='Name of the C method equivalent to assume', required=True)
    p.add_argument('--add-trivial-invariants', action="store_true",
            default=False,
            help='If specified add "invariant true;" to each while loop')

    args = p.parse_args()

    cparser = c_parser.CParser()
    if args.input == 'stdin':
        src = sys.stdin.read()
    else:
        src = open(args.input).read()

    src = re.sub(re.compile('__attribute__ *\(\(.*\)\)([^)])'), "\\1", src)
    ast = cparser.parse(src)

    renames = {
        args.assert_method: "assert",
        args.assume_method: "assume",
    }

    ctx = Ctx(0, renames, args.add_trivial_invariants)

    boogie_text = ""
    for x in ast.ext:
        if isinstance(x, FuncDef) and x.decl.name not in args.skip_methods:
            t = translate_FuncDef(x, ctx)
            boogie_text += t

    if args.output == "stdout":
      sys.stdout.write(boogie_text)
    else:
      with open(args.output, "w") as f:
        f.write(boogie_text)
