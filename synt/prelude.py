"""## Synt Prelude

This module contains multiple utilities that is often used when working with Synt.

It's suggested to import everything from this module instead of writing several separate import statements.
"""

from __future__ import annotations


__all__ = [
    "lambda_",
    "dict_",
    "dict_comp",
    "EMPTY",
    "NULL",
    "empty",
    "expr",
    "null",
    "Expression",
    "IntoExpression",
    "fnode",
    "fstring",
    "list_",
    "list_comp",
    "path",
    "relpath",
    "parentpath",
    "set_",
    "set_comp",
    "slice_",
    "tup",
    "tuple_",
    "await_",
    "awaited",
    "bit_not",
    "bool_not",
    "double_starred",
    "invert",
    "neg",
    "negative",
    "not_",
    "positive",
    "starred",
    "unpack",
    "unpack_dict",
    "unpack_kv",
    "unpack_seq",
    "yield_",
    "yield_from",
    "par",
    "wrap",
    "wrapped",
    "assert_",
    "Block",
    "class_",
    "dec",
    "arg",
    "async_def",
    "def_",
    "kwarg",
    "vararg",
    "BREAK",
    "CONTINUE",
    "PASS",
    "raise_",
    "ret",
    "return_",
    "IntoStatement",
    "Statement",
    "if_",
    "id_",
    "kv",
    "pair",
    "ELLIPSIS",
    "FALSE",
    "NONE",
    "TRUE",
    "UNDERSCORE",
    "litbool",
    "litfloat",
    "litint",
    "litstr",
    "tspec",
    "ttup",
    "tvar",
    "del_",
    "import_",
    "from_",
    "for_",
    "while_",
    "try_",
    "with_item",
    "with_",
    "global_",
    "nonlocal_",
    "match_",
    "File",
]

from synt.expr.closure import lambda_
from synt.expr.dict import dict_
from synt.expr.dict import dict_comp
from synt.expr.empty import EMPTY
from synt.expr.empty import NULL
from synt.expr.empty import empty
from synt.expr.empty import expr
from synt.expr.empty import null
from synt.expr.expr import Expression
from synt.expr.expr import IntoExpression
from synt.expr.fstring import fnode
from synt.expr.fstring import fstring
from synt.expr.list import list_
from synt.expr.list import list_comp
from synt.expr.modpath import parentpath
from synt.expr.modpath import path
from synt.expr.modpath import relpath
from synt.expr.set import set_
from synt.expr.set import set_comp
from synt.expr.subscript import slice_
from synt.expr.tuple import tup
from synt.expr.tuple import tuple_
from synt.expr.unary_op import await_
from synt.expr.unary_op import awaited
from synt.expr.unary_op import bit_not
from synt.expr.unary_op import bool_not
from synt.expr.unary_op import double_starred
from synt.expr.unary_op import invert
from synt.expr.unary_op import neg
from synt.expr.unary_op import negative
from synt.expr.unary_op import not_
from synt.expr.unary_op import positive
from synt.expr.unary_op import starred
from synt.expr.unary_op import unpack
from synt.expr.unary_op import unpack_dict
from synt.expr.unary_op import unpack_kv
from synt.expr.unary_op import unpack_seq
from synt.expr.unary_op import yield_
from synt.expr.unary_op import yield_from
from synt.expr.wrapped import par
from synt.expr.wrapped import wrap
from synt.expr.wrapped import wrapped
from synt.file import File
from synt.stmt.assertion import assert_
from synt.stmt.block import Block
from synt.stmt.branch import if_
from synt.stmt.cls import class_
from synt.stmt.context import with_
from synt.stmt.context import with_item
from synt.stmt.decorator import dec
from synt.stmt.delete import del_
from synt.stmt.fn import arg
from synt.stmt.fn import async_def
from synt.stmt.fn import def_
from synt.stmt.fn import kwarg
from synt.stmt.fn import vararg
from synt.stmt.importing import from_
from synt.stmt.importing import import_
from synt.stmt.keyword import BREAK
from synt.stmt.keyword import CONTINUE
from synt.stmt.keyword import PASS
from synt.stmt.loop import for_
from synt.stmt.loop import while_
from synt.stmt.match_case import match_
from synt.stmt.namespace import global_
from synt.stmt.namespace import nonlocal_
from synt.stmt.raising import raise_
from synt.stmt.returns import ret
from synt.stmt.returns import return_
from synt.stmt.stmt import IntoStatement
from synt.stmt.stmt import Statement
from synt.stmt.try_catch import try_
from synt.tokens.ident import id_
from synt.tokens.kv_pair import kv
from synt.tokens.kv_pair import pair
from synt.tokens.lit import ELLIPSIS
from synt.tokens.lit import FALSE
from synt.tokens.lit import NONE
from synt.tokens.lit import TRUE
from synt.tokens.lit import UNDERSCORE
from synt.tokens.lit import litbool
from synt.tokens.lit import litfloat
from synt.tokens.lit import litint
from synt.tokens.lit import litstr
from synt.ty.type_param import tspec
from synt.ty.type_param import ttup
from synt.ty.type_param import tvar
