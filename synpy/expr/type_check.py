from __future__ import annotations


__all__ = [
    "is_ident",
    "is_into_expr",
    "is_unary_op",
    "is_seq_unpack",
    "is_kv_unpack",
]


from typing import TYPE_CHECKING
from typing import Any
from typing import TypeGuard

import synpy.expr.expr as expr
import synpy.expr.unary_op as unary_op


if TYPE_CHECKING:
    from synpy.tokens.ident import IdentifierExpr


def is_into_expr(e: Any) -> TypeGuard[expr.IntoExpression]:
    """Whether the expression is an instance of `IntoExpression`."""
    return isinstance(e, expr.IntoExpression)


def is_ident(e: expr.Expression) -> TypeGuard[IdentifierExpr]:
    """Whether the expression is an identifier."""
    return e.expr_type == expr.ExprType.Identifier


def is_unary_op(e: expr.Expression) -> TypeGuard[unary_op.UnaryOp]:
    """Whether the expression is an unary operation."""
    return e.expr_type == expr.ExprType.UnaryOp


def is_seq_unpack(e: expr.Expression) -> bool:
    """Whether the expression is a sequence unpacking."""
    if is_unary_op(e):
        return e.op_type == unary_op.UnaryOpType.Starred
    return False


def is_kv_unpack(e: expr.Expression) -> bool:
    """Whether the expression is a kv-pair unpacking."""
    if is_unary_op(e):
        return e.op_type == unary_op.UnaryOpType.DoubleStarred
    return False
