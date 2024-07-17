from __future__ import annotations


__all__ = [
    "Assignment",
    "assign",
]


from typing import TYPE_CHECKING
from typing import Self

from synt.stmt.stmt import Statement
from synt.type_check import is_tuple


if TYPE_CHECKING:
    from synt.expr.expr import Expression
    from synt.expr.expr import IntoExpression


class Assignment(Statement):
    r"""Assignment statement.

    Examples:
        ```python
        ass = tup(id_("a"), id_("b")).assign(tup(litint(1), litstr("foo")))
        assert ass.into_code() == "a, b = (1, 'foo')" # automatically unpack
        ass = id_("a").expr().ty(id_("str")).assign(litstr("foo"))
        assert ass.into_code() == "a: str = 'foo'" # explicitly typing
        ass = id_("a").expr().ty(id_("str"))
        assert ass.into_code() == "a: str" # only typing
        ```

    References:
        [`Assign`](https://docs.python.org/3/library/ast.html#ast.Assign)<br/>
        [`AnnAssign`](https://docs.python.org/3/library/ast.html#ast.AnnAssign)<br/>
        [`AugAssign`](https://docs.python.org/3/library/ast.html#ast.AugAssign).
    """

    target: Expression
    """Target of the assignment."""
    target_ty: Expression | None
    """The type of the target."""
    value: Expression | None
    """The value to be assigned."""

    def __init__(self, target: IntoExpression):
        """Initialize a new assignment statement.

        Args:
            target: The variable to be assigned to.
        """
        self.target = target.into_expression()
        self.target_ty = None
        self.value = None

    def type(self, ty: IntoExpression) -> Self:
        """Set the target's type.

        Args:
            ty: The type of the target variable.
        """
        self.target_ty = ty.into_expression()
        return self

    def assign(self, v: IntoExpression) -> Self:
        """Set the target's value.

        Args:
            v: The value of the assignment.
        """
        self.value = v.into_expression()
        return self

    def indented(self, indent_width: int, indent_atom: str) -> str:
        if is_tuple(self.target):  # implicit tuple, like `a, b = foo`.
            target = self.target.into_code_implicit()
        else:
            target = self.target.into_code()
        tty = f": {self.target_ty.into_code()}" if self.target_ty is not None else ""
        ass = f" = {self.value.into_code()}" if self.value is not None else ""
        return f"{indent_atom * indent_width}{target}{tty}{ass}"


assign = Assignment
"""Alias [`Assignment`][synt.stmt.assign.Assignment]."""
