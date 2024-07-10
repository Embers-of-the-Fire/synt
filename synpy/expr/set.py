from __future__ import annotations


__all__ = [
    "SetDisplay",
    "SetVerbatim",
    "SetComprehension",
    "set_",
    "set_comp",
]


from abc import ABCMeta

import synpy.expr.comprehension as comp_expr
import synpy.expr.expr as expr

from synpy.errors.expr import ExpressionTypeException


class SetDisplay(expr.Expression, metaclass=ABCMeta):
    """Literal set expression.

    References:
        [Set display](https://docs.python.org/3/reference/expressions.html#set-displays).
    """

    precedence = expr.ExprPrecedence.Atom
    expr_type = expr.ExprType.Set


class SetVerbatim(SetDisplay):
    """Verbatim set expression."""

    items: list[expr.Expression]
    """Set items."""

    def __init__(self, *items: expr.IntoExpression):
        """Initialize a new verbatim set expression.

        Args:
            items: Set items.
        """
        self.items = [x.into_expression() for x in items]

    def into_code(self) -> str:
        item_text = ", ".join(x.into_code() for x in self.items)
        return f"{{{item_text}}}"


set_ = SetVerbatim
"""Alias [`SetVerbatim`][synpy.expr.set.SetVerbatim].

Notes:
    `set` is a built-in type in Python, so it's renamed to `set_` with a suffix.
"""


class SetComprehension(SetDisplay):
    """Set comprehension expression.

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
        """Initialize a new set comprehension expression.

        Args:
            comprehension: Internal comprehension expression.

        Raises:
            ExpressionTypeException: Invalid set comprehension result type,
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
        return f"{{{self.comprehension.into_code()}}}"


set_comp = SetComprehension
"""Alias [`SetComprehension`][synpy.expr.set.SetComprehension]."""
