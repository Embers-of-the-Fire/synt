from __future__ import annotations


__all__ = [
    "Wrapped",
    "wrap",
    "wrapped",
    "par",
]


import synt.expr.expr as expr


class Wrapped(expr.Expression):
    r"""A wrapped expression, aka `( expr )`, which is always an atomic expression.

    Examples:
        ```python
        wp = wrapped(litint(1) + litint(2)) * litint(3)
        assert wp.into_code() == "(1 + 2) * 3"
        ```

    Notes:
        Most plain expressions have their own expression precedence, and will be wrapped
        automatically by Synt.
        However, for those atomic expressions, some of them does have different parser precedence
        which is hard to represent beforehand. Thus, you must explicitly wrap them manually.
    """

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
"""Alias [`Wrapped`][synt.expr.wrapped.Wrapped]."""
