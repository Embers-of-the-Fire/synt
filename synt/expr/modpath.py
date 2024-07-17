from __future__ import annotations


__all__ = [
    "ModPath",
    "path",
    "relpath",
    "parentpath",
]


from typing import TYPE_CHECKING
from typing import Self

from synt.code import IntoCode


if TYPE_CHECKING:
    from synt.expr.alias import Alias
    from synt.tokens.ident import Identifier


class ModPath(IntoCode):
    r"""Module path.

    Examples:
        ```python
        p = path(id_('foo'))
        assert p.into_code() == "foo"
        p = path(id_('foo'), id_('bar'))
        assert p.into_code() == "foo.bar"
        p = path(id_('foo'), id_('bar'), depth=3)
        assert p.into_code() == "...foo.bar"
        p = path(id_('foo'), id_('bar')).dep(4)
        assert p.into_code() == "....foo.bar"
        ```
    """

    names: list[Identifier]
    """Names of the path."""
    depth: int
    """Relative depth of the path."""

    def __init__(self, *names: Identifier, depth: int = 0):
        """Initialize a new module path.

        Args:
            names: Names of the path.
            depth: Relative depth of the path.
        """
        self.names = list(names)
        self.depth = depth

    def dep(self, depth: int) -> Self:
        """Set the depth of the path.

        Args:
            depth: New depth of the path.
        """
        self.depth = depth
        return self

    def into_code(self) -> str:
        return "." * self.depth + ".".join(name.into_code() for name in self.names)

    def as_(self, asname: Identifier) -> Alias:
        """Alias the import path.

        Args:
            asname: Name of the alias.
        """
        from synt.expr.alias import Alias

        return Alias(self, asname)


path = ModPath
"""Alias [`ModPath`][synt.expr.modpath.ModPath]."""


def relpath(*names: Identifier) -> ModPath:
    r"""Initialize a path relatively (`depth = 1`).

    Args:
        names: Names of the path.

    Examples:
        ```python
        r = relpath(id_("abc"))
        assert r.into_code() == ".abc"
        ```
    """
    return ModPath(*names, depth=1)


def parentpath(*names: Identifier) -> ModPath:
    r"""Initialize a path from its parent (`depth = 2`).

    Args:
        names: Names of the path.

    Examples:
        ```python
        r = parentpath(id_("abc"))
        assert r.into_code() == "..abc"
        ```
    """
    return ModPath(*names, depth=2)
