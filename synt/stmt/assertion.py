from __future__ import annotations


__all__ = [
    "Assert",
    "assert_",
]


from typing import TYPE_CHECKING

from synt.stmt.stmt import Statement


if TYPE_CHECKING:
    from synt.expr.expr import Expression
    from synt.expr.expr import IntoExpression


class Assert(Statement):
    r"""The `assert` statement.

    Examples:
        ```python
        assert_stmt = assert_(TRUE, litstr("Condition is true"))
        assert assert_stmt.into_code() == "assert True, 'Condition is true'"
        ```

    References:
        [`Assert`](https://docs.python.org/3/library/ast.html#ast.Assert).
    """

    test: Expression
    """The expression to assert."""
    msg: Expression | None
    """The assert message."""

    def __init__(self, test: IntoExpression, msg: IntoExpression | None = None):
        """Initialize the assertion.

        Args:
            test: The expression to assert.
            msg: The assert message.
        """
        self.test = test.into_expression()
        if msg:
            self.msg = msg.into_expression()
        else:
            self.msg = None

    def indented(self, indent_width: int, indent_atom: str) -> str:
        msg = f", {self.msg.into_code()}" if self.msg else ""
        return f"{indent_width * indent_atom}assert {self.test.into_code()}{msg}"


assert_ = Assert
"""Alias [`Assert`][synt.stmt.assertion.Assert]."""
