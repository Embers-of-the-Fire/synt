from __future__ import annotations


__all__ = [
    "Alias",
]

from synt.code import IntoCode
from synt.expr.modpath import ModPath


class Alias(IntoCode):
    r"""Import alias.

    Examples:
        ```python
        al = id_("a").as_("b")
        assert al.into_code() == "a as b"
        p = path(id_('foo'), id_('bar')).as_(id_("baz"))
        assert p.into_code() == "foo.bar as baz"
        ```

    References:
        [`alias`](https://docs.python.org/3/library/ast.html#ast.alias).
    """

    names: ModPath
    """The names of the alias item."""
    asname: Identifier
    """The alias name."""

    def __init__(self, names: Identifier | ModPath, asname: Identifier):
        """Initialize a new alias.

        Args:
            names: The names of the alias item.
            asname: The alias name.
        """
        if isinstance(names, Identifier):
            self.names = ModPath(names)
        else:
            self.names = names
        self.asname = asname

    def into_code(self) -> str:
        return f"{self.names.into_code()} as {self.asname.into_code()}"


from synt.tokens.ident import Identifier
