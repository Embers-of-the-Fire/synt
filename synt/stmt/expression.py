from __future__ import annotations

from typing import TYPE_CHECKING

from synt.stmt.stmt import Statement


if TYPE_CHECKING:
    from synt.expr.expr import Expression
    from synt.expr.expr import IntoExpression


class ExprStatement(Statement):
    """A statement that only contains a single expression.

    Examples:
        ```python
        stmt = id_("print").expr().call(litstr("Hello world!")).stmt()
        assert stmt.into_code() == "print('Hello world!')"
        ```
    """

    expr: Expression
    """Inner expression."""

    def __init__(self, expr: IntoExpression):
        """Initialize a nwe statement.

        Args:
            expr: Inner expression.
        """
        self.expr = expr.into_expression()

    def indented(self, indent_width: int, indent_atom: str) -> str:
        return f"{indent_atom * indent_width}{self.expr.into_code()}"


stmt = ExprStatement
"""Alias [`ExprStatement`][synt.stmt.expression.ExprStatement]."""
