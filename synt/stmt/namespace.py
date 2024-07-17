from __future__ import annotations


__all__ = [
    "Global",
    "global_",
    "Nonlocal",
    "nonlocal_",
]


from typing import TYPE_CHECKING

from synt.stmt.stmt import Statement


if TYPE_CHECKING:
    from synt.tokens.ident import Identifier


class Global(Statement):
    """The `global` statement.

    Examples:
        ```python
        global_stmt = global_(id_('foo'))
        assert global_stmt.into_code() == 'global foo'
        ```

    References:
        [`Global`](https://docs.python.org/3/library/ast.html#ast.Global).
    """

    names: list[Identifier]
    """Global variable names."""

    def __init__(self, *names: Identifier):
        """Initialize a new `global` statement.

        Args:
            names: Global variable names.

        Raises:
            ValueError: If the `names` list is empty.
        """
        if len(names) == 0:
            raise ValueError("At least one global variable name is required.")
        self.names = list(names)

    def indented(self, indent_width: int, indent_atom: str) -> str:
        return f"{indent_atom * indent_width}global {', '.join(name.into_code() for name in self.names)}"


global_ = Global
"""Alias [`Global`][synt.stmt.namespace.Global]."""


class Nonlocal(Statement):
    """The `nonlocal` statement.

    Examples:
        ```python
        nonlocal_stmt = nonlocal_(id_('foo'))
        assert nonlocal_stmt.into_code() == 'nonlocal foo'
        ```

    References:
        [`Nonlocal`](https://docs.python.org/3/library/ast.html#ast.Nonlocal).
    """

    names: list[Identifier]
    """Nonlocal variable names."""

    def __init__(self, *names: Identifier):
        """Initialize a new `nonlocal` statement.

        Args:
            names: Nonlocal variable names.

        Raises:
            ValueError: If the `names` list is empty.
        """
        if len(names) == 0:
            raise ValueError("At least one nonlocal variable name is required.")
        self.names = list(names)

    def indented(self, indent_width: int, indent_atom: str) -> str:
        return f"{indent_atom * indent_width}nonlocal {', '.join(name.into_code() for name in self.names)}"


nonlocal_ = Nonlocal
"""Alias [`Nonlocal`][synt.stmt.namespace.Nonlocal]."""
