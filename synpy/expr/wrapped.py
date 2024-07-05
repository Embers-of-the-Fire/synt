from __future__ import annotations


__all__ = [
    "Wrapped",
    "wrap",
    "wrapped",
    "par",
]


import synpy.expr.expr as expr


class Wrapped(expr.Expression):
    """A wrapped expression, aka `( expr )`, which is always an atomic expression."""

    inner: expr.Expression
    """Inner expression."""

    precedence = expr.ExprPrecedence.Atom
    expr_type = expr.ExprType.Wrapped

    def __init__(self, inner: expr.IntoExpression):
        """Initialize a wrapped expression.

        Args:
            inner: Inner expression.
        """
        self.inner = inner.into_expression()

    def into_code(self) -> str:
        return f"({self.inner.into_code()})"


wrapped = wrap = par = Wrapped
"""Alias [`Wrapped`][synpy.expr.wrapped.Wrapped]."""
