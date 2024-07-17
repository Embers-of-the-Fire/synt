from __future__ import annotations


__all__ = [
    "is_tuple",
]


from typing import TYPE_CHECKING
from typing import TypeGuard

from synt.expr.expr import Expression
from synt.expr.expr import ExprType


if TYPE_CHECKING:
    import synt.expr.tuple


def is_tuple(exp: Expression) -> TypeGuard[synt.expr.tuple.Tuple]:
    r"""Check if the given expression is a tuple."""
    return exp.expr_type == ExprType.Tuple
