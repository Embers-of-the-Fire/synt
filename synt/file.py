from __future__ import annotations


__all__ = [
    "File",
]


from typing import TYPE_CHECKING

from synt.stmt.block import Block


if TYPE_CHECKING:
    from synt.stmt.stmt import Statement


class File:
    r"""Abstract file containing arbitrary python code.

    Examples:
        ```python
        file = File(
            id_("print").expr().call(litstr("Hello, World!")).stmt(),
            id_("x").expr().assign(litint(42)),
            if_(id_("x").expr().eq(litint(42))).block(
                id_("print").expr().call(litstr("x is 42")).stmt()
            )
        )
        assert file.into_str() == '''print('Hello, World!')
        x = 42
        if x == 42:
            print('x is 42')'''
        ```
    """

    body: Block
    """Code lines in the file."""

    def __init__(self, *statements: Statement):
        """Initialize a file.

        Args:
            statements: Statements to include in the file.
        """
        self.body = Block(*statements)

    def into_str(self, indent_atom: str = "    ", indent_width: int = 0) -> str:
        """Convert the file into a string.

        Args:
            indent_width: number of `indent_atom`s per indentation level.
            indent_atom: string to use for indentation. E.g. `\\t`, whitespace, etc.
        """
        return self.body.indented(indent_width, indent_atom)
