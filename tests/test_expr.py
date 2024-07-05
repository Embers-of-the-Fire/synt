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


def test_expr_constructor():
    text = tup(id_("a"), id_("b")).for_(id_("a")).in_(id_("it")).expr().into_code()
    assert text == "((a, b) for a in it)"
    text = (id_("a").expr().awaited() + id_("b")).into_code()
    assert text == "await a + b"
    text = fstring("abc", fnode(id_("sin").expr().call(id_("a")), ".3")).into_code()
    assert text == '"abc{sin(a):.3}"'
    text = id_("a").expr().attr("b")[id_("slice")] == (
        -id_("sin").expr().call(angle=id_("theta"))
    ).if_(id_("j").expr() >= id_("k")).else_(id_("t"))
    text = text.into_code()
    assert text == "a.b[slice] == (- sin(angle=theta) if j >= k else t)"
    text = (
        (
            id_("a").expr().attr("b")[id_("slice")]
            == (-id_("sin").expr().call(angle=id_("theta")))
        )
        .if_(id_("j").expr() >= id_("k"))
        .else_(id_("t"))
    )
    text = text.into_code()
    assert text == "a.b[slice] == - sin(angle=theta) if j >= k else t"
