from __future__ import annotations


__all__ = [
    "ListDisplay",
    "ListVerbatim",
    "ListComprehension",
    "list_",
    "list_comp",
]


from abc import ABCMeta

import synpy.expr.comprehension as comp_expr
import synpy.expr.expr as expr

from synpy.errors.expr import ExpressionTypeException


class ListDisplay(expr.Expression, metaclass=ABCMeta):
    """Literal list expression.

    References:
        [list display](https://docs.python.org/3/reference/expressions.html#list-displays).
    """

    precedence = expr.ExprPrecedence.Atom
    expr_type = expr.ExprType.List


class ListVerbatim(ListDisplay):
    """Verbatim list expression, aka `starred-list`.

    References:
        [`starred-list`](https://docs.python.org/3/reference/expressions.html#grammar-token-python-grammar-starred_list).
    """

    items: list[expr.Expression]
    """list items."""

    def __init__(self, *items: expr.IntoExpression):
        """Initialize a new verbatim list expression.

        Args:
            items: list items.
        """
        self.items = [x.into_expression() for x in items]

    def into_code(self) -> str:
        item_text = ", ".join(x.into_code() for x in self.items)
        return f"[{item_text}]"


list_ = ListVerbatim
"""Alias [`ListVerbatim`][synpy.expr.list.ListVerbatim].

Notes:
    `list` is a built-in type in Python, so it's renamed to `list_` with a suffix.
"""


class ListComprehension(ListDisplay):
    """list comprehension expression.

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
        """Initialize a new list comprehension expression.

        Args:
            comprehension: Internal comprehension expression.

        Raises:
            ExpressionTypeException: Invalid list comprehension result type,
                typically a [`KVPair`][synpy.tokens.kv_pair.KVPair].
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

        if comp.elt.expr_type == expr.ExprType.KeyValuePair:
            raise ExpressionTypeException(
                expr.ExprType.Atom, expr.ExprType.KeyValuePair
            )
        self.comprehension = comp

    def into_code(self) -> str:
        return f"[{self.comprehension.into_code()}]"


list_comp = ListComprehension
"""Alias [`ListComprehension`][synpy.expr.list.ListComprehension]."""
