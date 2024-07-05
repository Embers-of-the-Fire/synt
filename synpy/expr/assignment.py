from __future__ import annotations


__all__ = [
    "Assignment",
]

from typing import TYPE_CHECKING

import synpy.expr.expr as expr


if TYPE_CHECKING:
    from synpy.token.ident import Identifier


class Assignment(expr.Expression):
    """Inline assignment expression, aka `:=`.

    References:
        [expr.ExprPrecedence.Assignment][synpy.expr.expr.ExprPrecedence.Assignment].
    """

    receiver: Identifier
    """The identifier to be assigned."""
    value: expr.Expression
    """The value to be assigned to the receiver."""
    precedence = expr.ExprPrecedence.Assignment
    expr_type = expr.ExprType.Assignment

    def __init__(self, receiver: Identifier, value: expr.IntoExpression):
        """Initialize an assignment expression.

        Args:
            receiver: The identifier to be assigned.
            value: The value to be assigned to the receiver.
        """
        self.receiver = receiver
        self.value = value.into_expression()

        if self.value.precedence >= self.precedence:
            self.value = self.value.wrapped()

    def into_code(self) -> str:
        return f"{self.receiver.into_code()} := {self.value.into_code()}"
