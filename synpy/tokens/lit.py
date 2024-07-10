from __future__ import annotations


__all__ = [
    "Literal",
    "litfloat",
    "litint",
    "litstr",
]


from typing import Any

from synpy.expr.expr import Expression
from synpy.expr.expr import ExprPrecedence
from synpy.expr.expr import ExprType


class Literal(Expression):
    """Literal Python expression."""

    lit: str
    """Source code of the literal."""

    precedence = ExprPrecedence.Atom
    expr_type = ExprType.Literal

    def __init__(self, src: str):
        """Initialize a Literal value.

        **DO NOT USE THIS IN YOUR CODE!** Use other entry points instead.

        Args:
            src: Source code of the literal.
        """
        self.lit = src

    @staticmethod
    def str_(s: str) -> Literal:
        """Initialize a literal string.

        Notes:
            `str` is a built-in type, so this function is suffixed with a `_`.

        Args:
            s: Original string.

        Examples:
            ```python
            a = litstr("abc")
            assert a.into_code() == "'abc'"
            ```
        """
        return Literal._repr(s)

    @staticmethod
    def int_(s: int) -> Literal:
        """Initialize a literal integer.

        Notes:
            `int` is a built-in type, so this function is suffixed with a `_`.

        Args:
            s: Original integer.

        Examples:
            ```python
            a = litint(1)
            assert a.into_code() == "1"
            ```
        """
        return Literal._repr(s)

    @staticmethod
    def float_(s: float) -> Literal:
        """Initialize a literal float.

        Args:
            s: Original float.

        Notes:
            `float` is a built-in type, so this function is suffixed with a `_`.

        Examples:
            ```python
            a = litfloat(0.24)
            assert a.into_code() == "0.24"
            ```
        """
        return Literal._repr(s)

    @staticmethod
    def _repr(mr: Any) -> Literal:
        """Initialize a literal value with the `__repr__` method of the given value.

        Args:
            mr: Value to be represented.

        Raises:
            AttributeError: `__repr__` is not found for the given value.
        """
        return Literal(repr(mr))

    @staticmethod
    def _str(s: Any) -> Literal:
        """Initialize a literal value with the `__str__` method of the given value.

        Args:
            s: Value to be represented.

        Raises:
            AttributeError: `__str__` is not found for the given value.
        """
        return Literal(str(s))

    def into_code(self) -> str:
        return self.lit


litstr = Literal.str_
"""Alias for [`str_`][synpy.tokens.lit.Literal.str_]."""
litint = Literal.int_
"""Alias for [`int_`][synpy.tokens.lit.Literal.int_]."""
litfloat = Literal.float_
"""Alias for [`float_`][synpy.tokens.lit.Literal.float_]."""
