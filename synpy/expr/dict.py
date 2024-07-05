from __future__ import annotations


__all__ = [
    "DictDisplay",
    "DictVerbatim",
    "DictComprehension",
    "dict_",
    "dict_comp",
]


from abc import ABCMeta
from typing import TYPE_CHECKING

import synpy.expr.comprehension as comp_expr
import synpy.expr.expr as expr

from synpy.errors.expr import ExpressionTypeException


if TYPE_CHECKING:
    from synpy.token.kv_pair import KVPair


class DictDisplay(expr.Expression, metaclass=ABCMeta):
    """Literal dict expression.

    References:
        [Dictionary display](https://docs.python.org/3/reference/expressions.html#dictionary-displays).
    """

    precedence = expr.ExprPrecedence.Atom
    expr_type = expr.ExprType.Dict


class DictVerbatim(DictDisplay):
    """Verbatim dict expression."""

    items: list[KVPair]
    """Dict items."""

    def __init__(self, *items: KVPair):
        """Initialize a new verbatim dict expression.

        Args:
            items: dictionary items.
        """
        self.items = list(items)

    def into_code(self) -> str:
        item_text = ", ".join(x.into_code() for x in self.items)
        return f"{{{item_text}}}"


dict_ = DictVerbatim
"""Alias [`DictVerbatim`][synpy.expr.dict.DictVerbatim].

Notes:
    `dict` is a built-in type in Python, so it's renamed to `dict_` with a suffix.
"""


class DictComprehension(DictDisplay):
    """Dict comprehension expression.

    References:
        [`comprehension`](https://docs.python.org/3/reference/
        expressions.html#grammar-token-python-grammar-comprehension).
    """

    comprehension: comp_expr.Comprehension
    """Internal comprehension expression."""

    def __init__(
        self,
        comprehension: comp_expr.Comprehension
        | comp_expr.ComprehensionBuilder
        | comp_expr.ComprehensionNodeBuilder,
    ):
        """Initialize a new dict comprehension expression.

        Args:
            comprehension: Internal comprehension expression.

        Raises:
            ExpressionTypeException: Invalid dict comprehension result type,
                typically not a [`KVPair`][synpy.token.kv_pair.KVPair].
        """
        if isinstance(comprehension, comp_expr.Comprehension):
            comp = comprehension
        elif isinstance(comprehension, comp_expr.ComprehensionBuilder):
            comp = comprehension.build()
        elif isinstance(comprehension, comp_expr.ComprehensionNodeBuilder):
            comp = comprehension.build_comp()
        else:
            raise ExpressionTypeException(
                expr.ExprType.Comprehension, expr.ExprType.Unknown
            )

        if comp.elt.expr_type != expr.ExprType.KeyValuePair:
            raise ExpressionTypeException(
                expr.ExprType.KeyValuePair, expr.ExprType.Atom
            )
        self.comprehension = comp

    def into_code(self) -> str:
        return f"{{{self.comprehension.into_code()}}}"


dict_comp = DictComprehension
"""Alias [`DictComprehension`][synpy.expr.dict.DictComprehension]."""
