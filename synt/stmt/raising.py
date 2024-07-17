from __future__ import annotations


__all__ = [
    "Raise",
    "raise_",
]


from typing import TYPE_CHECKING
from typing import Self

from synt.stmt.stmt import Statement


if TYPE_CHECKING:
    from synt.expr.expr import Expression
    from synt.expr.expr import IntoExpression


class Raise(Statement):
    r"""The `raise` statement.

    Examples:
        ```python
        r = raise_()
        assert r.into_code() == "raise"
        r = raise_(litint(42))
        assert r.into_code() == "raise 42"
        r = raise_(litint(42)).from_(litstr("Custom exception"))
        assert r.into_code() == "raise 42 from 'Custom exception'"
        ```

    References:
        [`Raise`](https://docs.python.org/3/library/ast.html#ast.Raise).
    """

    exception: Expression | None
    """The exception to raise."""
    cause: Expression | None
    """The origin of the raised exception."""

    def __init__(self, exception: IntoExpression | None = None):
        """Initialize a new `raise` statement.

        Args:
            exception: The exception to raise.
        """
        if exception:
            self.exception = exception.into_expression()
        else:
            self.exception = None
        self.cause = None

    def from_(self, cause: IntoExpression) -> Self:
        """Set the cause of the raised exception.

        Args:
            cause: The origin of the raised exception.

        Raises:
            ValueError: If `exception` is `None`.
        """
        if self.exception is None:
            raise ValueError("Cannot set cause without setting exception.")
        self.cause = cause.into_expression()
        return self

    def indented(self, indent_width: int, indent_atom: str) -> str:
        cause = f" from {self.cause.into_code()}" if self.cause is not None else ""
        exc = f" {self.exception.into_code()}" if self.exception is not None else ""
        return f"{indent_width * indent_atom}raise{exc}{cause}"


raise_ = Raise
"""Alias [`Raise`][synt.stmt.raising.Raise]."""
