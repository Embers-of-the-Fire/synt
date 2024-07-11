from __future__ import annotations

from synpy.expr.binary_op import BinaryOpType
from synpy.expr.expr import ExprPrecedence
from synpy.expr.unary_op import UnaryOpType
from synpy.prelude import *


def test_expr_type():
    assert BinaryOpType.Add.to_precedence() == ExprPrecedence.Additive

    for i in range(23):
        op = BinaryOpType(i)
        assert op.to_precedence() is not None
        assert op.into_code() is not None
    for i in range(8):
        op = UnaryOpType(i)
        assert op.to_precedence() is not None
        assert op.into_code() is not None


def test_expr_closure():
    closure = (
        lambda_(id_("x"), id_("y"))  # initial a closure builder
        .join(id_("z"))  # append new argument
        .return_(
            id_("x").expr() + id_("y") + id_("z")
        )  # set the expression to be returned
    )
    assert closure.into_code() == "lambda x, y, z: x + y + z"


def test_expr_dict():
    d = dict_(kv(litstr("a"), id_("b")))
    assert d.into_code() == "{'a': b}"

    d = dict_comp(
        kv(id_("a"), litint(1)).for_(id_("a")).in_(id_("range").expr().call(litint(5)))
    )
    assert d.into_code() == "{a: 1 for a in range(5)}"


def test_fstring():
    node = fnode(id_("sin").expr().call(litint(1)), ".2")
    assert node.into_code() == "{sin(1):.2}"
    string = fstring("sin(1) = ", fnode(id_("sin").expr().call(litint(1))))
    assert string.into_code() == 'f"sin(1) = {sin(1)}"'
