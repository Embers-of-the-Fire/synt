from __future__ import annotations


__all__ = [
    "NamedExpr",
]

from typing import TYPE_CHECKING

import synt.expr.expr as expr


if TYPE_CHECKING:
    from synt.tokens.ident import Identifier


class NamedExpr(expr.Expression):
    r"""Inline assignment expression, aka `:=`.

    References:
        [expr.ExprPrecedence.NamedExpr][synt.expr.expr.ExprPrecedence.NamedExpr].
    """

    receiver: Identifier
    """The identifier to be assigned."""
    value: expr.Expression
    """The value to be assigned to the receiver."""
    precedence = expr.ExprPrecedence.NamedExpr
    expr_type = expr.ExprType.NamedExpr

    def __init__(self, receiver: Identifier, value: expr.IntoExpression):
        """Initialize a named expr expression.

        Args:
            receiver: The identifier to be assigned.
            value: The value to be assigned to the receiver.
        """
        self.receiver = receiver
        self.value = value.into_expression()

        if self.value.precedence > self.precedence:
            self.value = self.value.wrapped()

    def into_code(self) -> str:
        return f"{self.receiver.into_code()} := {self.value.into_code()}"
