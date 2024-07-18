from __future__ import annotations


__all__ = [
    "Alias",
]

from synt.expr.expr import Expression
from synt.expr.expr import ExprPrecedence
from synt.expr.expr import ExprType
from synt.expr.modpath import ModPath


class Alias(Expression):
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

    names: ModPath | Expression
    """The names of the alias item."""
    asname: Identifier
    """The alias name."""

    expr_type = ExprType.Atom
    precedence = ExprPrecedence.Atom

    def __init__(self, names: Identifier | ModPath | Expression, asname: Identifier):
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
