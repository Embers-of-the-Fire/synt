from __future__ import annotations


__all__ = [
    "Attribute",
]


import synt.expr.expr as expr


class Attribute(expr.Expression):
    r"""The operation to get a value's attribute.

    References:
        [Attribute](https://docs.python.org/3/library/ast.html#ast.Attribute).
    """

    target: expr.Expression
    """The target of the operation."""
    attribute_name: str
    """The attribute's name."""

    precedence = expr.ExprPrecedence.Call
    expr_type = expr.ExprType.Attribute

    def __init__(self, target: expr.IntoExpression, attr: str):
        """Initialize an attribute expression.

        Args:
            target: The target of the operation.
            attr: The attribute's name.
        """
        self.target = target.into_expression()
        self.attribute_name = attr

        if self.target.precedence > self.precedence:
            self.target = self.target.wrapped()

    def into_code(self) -> str:
        return f"{self.target.into_code()}.{self.attribute_name}"
