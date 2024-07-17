from __future__ import annotations

from typing import TYPE_CHECKING

from synt.stmt.stmt import Statement


if TYPE_CHECKING:
    from synt.expr.expr import Expression
    from synt.expr.expr import IntoExpression


class Return(Statement):
    r"""The `return` statement.

    Examples:
        ```python
        return_stmt = return_(litint(42))
        assert return_stmt.into_code() == "return 42"
        return_stmt = ret()
        assert return_stmt.into_code() == "return"
        ```

    References:
        [`Returns`](https://docs.python.org/3/library/ast.html#ast.Return).
    """

    expression: Expression | None
    """The value to return from the function."""

    def __init__(self, expression: IntoExpression | None = None):
        """Initialize the return statement.

        Args:
            expression: The value to return from the function.
        """
        if expression:
            self.expression = expression.into_expression()
        else:
            self.expression = None

    def indented(self, indent_width: int, indent_atom: str) -> str:
        if self.expression:
            return f"{indent_atom * indent_width}return {self.expression.into_code()}"
        else:
            return f"{indent_atom * indent_width}return"


return_ = ret = Return
"""Alias [`Return`][synt.stmt.returns.Return]."""
