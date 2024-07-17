from __future__ import annotations


__all__ = [
    "Tuple",
    "tup",
    "tuple_",
]


import synt.expr.expr as expr


class Tuple(expr.Expression):
    r"""Tuple expression.

    Examples:
        ```python
        t = tup(litstr("abc"))
        assert t.into_code() == "('abc',)"
        ```
    """

    items: list[expr.Expression]
    """Tuple items."""

    precedence = expr.ExprPrecedence.Atom
    expr_type = expr.ExprType.Tuple

    def __init__(self, *items: expr.IntoExpression):
        """Initialize a tuple expression.

        Args:
            items: Tuple items.
        """
        self.items = [i.into_expression() for i in items]

    def into_code(self) -> str:
        return f"({self.into_code_implicit()})"

    def into_code_implicit(self) -> str:
        """Convert the tuple into a string representation implicitly, omitting the parentheses."""
        item_text = ", ".join(x.into_code() for x in self.items)
        if len(self.items) == 1:
            item_text += ","
        return item_text


tuple_ = tup = Tuple
"""Alias [`Tuple`][synt.expr.tuple.Tuple]."""
