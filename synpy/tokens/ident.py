from __future__ import annotations


__all__ = [
    "Identifier",
    "IdentifierExpr",
    "id_",
]


import synpy.code as code
import synpy.expr.expr as expr

from synpy.errors.ident import InvalidIdentifierException


class Identifier(expr.IntoExpression, code.IntoCode):
    """Represents a valid Python identifier.

    For more information, see the [Identifier and Keywords][ident-and-keywords-python-docs]
    section of the Python's standard documentation.

    [ident-and-keywords-python-docs]: https://docs.python.org/3.12/reference/lexical_analysis.html#identifiers
    """

    raw: str
    """Raw identifier text."""

    def __init__(self, raw: str):
        """Initialize a new identifier.

        The raw content will be checked immediately when initializing the object.

        Args:
            raw: Raw identifier text.

        Raises:
            InvalidIdentifierException: If the raw identifier text is not a valid identifier.

        Examples:
            ```python
            id_foo = synpy.tokens.ident.Identifier('foo')
            id_foo_alias = id_('foo') # with alias
            try:
                id_fail = id_('foo bar') # invalid identifier lit will fail
            except synpy.errors.ident.InvalidIdentifierException:
                pass
            ```
        """
        if not raw.isidentifier():
            raise InvalidIdentifierException(raw)
        self.raw = raw

    def into_expression(self) -> IdentifierExpr:
        return IdentifierExpr(self)

    def expr(self) -> IdentifierExpr:
        """Initialize a new expression with `self`.

        Alias for [`into_expression`][synpy.tokens.ident.Identifier.into_expression].

        Examples:
            ```python
            id_foo = id_('foo')
            id_foo_expr = id_foo.expr()
            assert isinstance(id_foo_expr, synpy.expr.expr.Expression)
            ```
        """
        return IdentifierExpr(self)

    def into_code(self) -> str:
        return self.raw


id_ = Identifier
"""Alias [`Identifier`][synpy.tokens.ident.Identifier].

Notes:
    `id` is a built-in function in Python, so it's renamed to `id_` with a suffix.
"""


class IdentifierExpr(expr.Expression):
    """An identifier as a Python expression.

    See [`Identifier`][synpy.tokens.ident.Identifier] for more information.
    """

    precedence = expr.ExprPrecedence.Atom
    expr_type = expr.ExprType.Identifier

    ident: Identifier
    """Inner identifier."""

    def __init__(self, raw: Identifier):
        """Initialize a new identifier.

        Use [`Identifier`][synpy.tokens.ident.Identifier.expr] instead and converts it into an expression.

        Args:
            raw: Identifier to be used as an expression.
        """
        self.ident = raw

    @staticmethod
    def from_str(s: str) -> IdentifierExpr:
        """Parse an identifier from a string.

        The raw content will be checked immediately when initializing the object.

        Args:
            s: Raw identifier text.

        Raises:
            InvalidIdentifierException: If the raw identifier text is not a valid identifier.
        """
        return IdentifierExpr(Identifier(s))

    def into_code(self) -> str:
        return self.ident.raw
