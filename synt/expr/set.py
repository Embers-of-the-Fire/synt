from __future__ import annotations


__all__ = [
    "SetDisplay",
    "SetVerbatim",
    "SetComprehension",
    "set_",
    "set_comp",
]


from abc import ABCMeta

import synt.expr.comprehension as comp_expr
import synt.expr.expr as expr


class SetDisplay(expr.Expression, metaclass=ABCMeta):
    r"""Literal set expression.

    References:
        [Set display](https://docs.python.org/3/reference/expressions.html#set-displays).
    """

    precedence = expr.ExprPrecedence.Atom
    expr_type = expr.ExprType.Set


class SetVerbatim(SetDisplay):
    r"""Verbatim set expression.

    Examples:
        ```python
        s = set_(litint(1), id_("b"))
        assert s.into_code() == "{1, b}"
        ```
    """

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
"""Alias [`SetVerbatim`][synt.expr.set.SetVerbatim].

Notes:
    `set` is a built-in type in Python, so it's renamed to `set_` with a suffix.
"""


class SetComprehension(SetDisplay):
    r"""Set comprehension expression.

    Examples:
        ```python
        s = set_comp(id_("x").expr().for_(id_("x")).in_(id_("range").expr().call(litint(5))))
        assert s.into_code() == "{x for x in range(5)}"
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
        """Initialize a new set comprehension expression.

        Args:
            comprehension: Internal comprehension expression.

        Raises:
            ExpressionTypeException: Invalid set comprehension result type,
                typically a [`KVPair`][synt.tokens.kv_pair.KVPair].
        """
        if isinstance(comprehension, comp_expr.Comprehension):
            comp = comprehension
        elif isinstance(comprehension, comp_expr.ComprehensionBuilder):
            comp = comprehension.build()
        elif isinstance(comprehension, comp_expr.ComprehensionNodeBuilder):
            comp = comprehension.build_comp()
        else:
            raise ValueError(
                "Expect expression of type `Comprehension`, found `Unknown`."
            )

        if comp.elt.expr_type == expr.ExprType.KeyValuePair:
            raise ValueError("Expect expression of type `Atom`, found `KeyValuePair`.")
        self.comprehension = comp

    def into_code(self) -> str:
        return f"{{{self.comprehension.into_code()}}}"


set_comp = SetComprehension
"""Alias [`SetComprehension`][synt.expr.set.SetComprehension]."""
