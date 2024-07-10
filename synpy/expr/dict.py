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
    from synpy.tokens.kv_pair import KVPair


class DictDisplay(expr.Expression, metaclass=ABCMeta):
    """Literal dict expression.

    References:
        [Dictionary display](https://docs.python.org/3/reference/expressions.html#dictionary-displays).
    """

    precedence = expr.ExprPrecedence.Atom
    expr_type = expr.ExprType.Dict


class DictVerbatim(DictDisplay):
    """Verbatim dict expression.

    Examples:
        ```python
        d = dict_(kv(litstr("a"), id_("b")))
        assert d.into_code() == "{'a': b}"
        ```
    """

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

    Note that you can also directly insert a comprehension expression into a normal dictionary,
    but that will become a generator comprehension and returns a pair of extra parenthesis.

    Examples:
        ```python
        d = dict_comp(kv(id_("a"), litint(1)).for_(id_("a")).in_(id("range").call(litint(5)))
        assert d.into_code() == "{a: 1 for a in range(5)}"
        ```

    References:
        [`comprehension`](https://docs.python.org/3/reference/
        expressions.html#grammar-tokens-python-grammar-comprehension).
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
                typically not a [`KVPair`][synpy.tokens.kv_pair.KVPair].
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
