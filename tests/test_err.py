from synpy.expr.expr import ExprType

from synpy.prelude import *


def test_err():
    err = ExpressionTypeException(ExprType.Atom, ExprType.Identifier)
    assert err.actual == ExprType.Identifier
    assert err.expected == ExprType.Atom
