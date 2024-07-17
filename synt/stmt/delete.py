from __future__ import annotations


__all__ = [
    "Delete",
    "del_",
]


from typing import TYPE_CHECKING

from synt.stmt.stmt import Statement


if TYPE_CHECKING:
    from synt.expr.expr import Expression
    from synt.expr.expr import IntoExpression


class Delete(Statement):
    r"""The `del` statement.

    Examples:
        ```python
        d = del_(id_("foo").expr().attr("bar"))
        assert d.into_code() == "del foo.bar"
        ```

    References:
        [`Delete`](https://docs.python.org/3/library/ast.html#ast.Delete).
    """

    target: Expression
    """The expression to be deleted."""

    def __init__(self, target: IntoExpression):
        """Initialize the delete statement.

        Args:
            target: The expression to be deleted.
        """
        self.target = target.into_expression()

    def indented(self, indent_width: int, indent_atom: str) -> str:
        return f"{indent_atom * indent_width}del {self.target.into_code()}"


del_ = Delete
"""Alias [`Delete`][synt.stmt.delete.Delete]."""
