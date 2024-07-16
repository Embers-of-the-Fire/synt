from __future__ import annotations


__all__ = [
    "Alias",
]


from typing import TYPE_CHECKING

from synt.code import IntoCode


if TYPE_CHECKING:
    from synt.tokens.ident import Identifier


class Alias(IntoCode):
    """Import alias.

    Examples:
        ```python
        al = id_("a").as_("b")
        assert al.into_code() == "a as b"
        ```

    References:
        [`alias`](https://docs.python.org/3/library/ast.html#ast.alias).
    """

    name: Identifier
    """The name of the alias item."""
    asname: Identifier
    """The alias name."""

    def __init__(self, name: Identifier, asname: Identifier):
        """Initialize a new alias.

        Args:
            name: The name of the alias item.
            asname: The alias name.
        """
        self.name = name
        self.asname = asname

    def into_code(self) -> str:
        return f"{self.name.into_code()} as {self.asname.into_code()}"
