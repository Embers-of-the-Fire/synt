from __future__ import annotations


__all__ = [
    "is_ident",
    "is_into_expr",
]


from typing import TYPE_CHECKING
from typing import Any
from typing import TypeGuard

import synt.expr.expr as expr


if TYPE_CHECKING:
    from synt.tokens.ident import IdentifierExpr


def is_into_expr(e: Any) -> TypeGuard[expr.IntoExpression]:
    r"""Whether the expression is an instance of `IntoExpression`."""
    return isinstance(e, expr.IntoExpression)


def is_ident(e: expr.Expression) -> TypeGuard[IdentifierExpr]:
    r"""Whether the expression is an identifier."""
    return e.expr_type == expr.ExprType.Identifier
