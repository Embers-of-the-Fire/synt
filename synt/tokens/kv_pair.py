from __future__ import annotations


__all__ = [
    "KVPair",
    "pair",
    "kv",
]


from synt.expr.expr import Expression
from synt.expr.expr import ExprPrecedence
from synt.expr.expr import ExprType
from synt.expr.expr import IntoExpression


class KVPair(Expression):
    r"""A key-value pair, aka `a: b`.

    This is mainly used in dict initializing (`{a: b}`)."""

    key: Expression
    """Key expression."""
    value: Expression
    """Value expression."""
    precedence = ExprPrecedence.Atom
    expr_type = ExprType.KeyValuePair

    def __init__(self, key: IntoExpression, value: IntoExpression):
        """Initialize a key-value pair.

        Args:
            key: Key expression.
            value: Value expression.

        Examples:
            ```python
            kv_pair = kv(id_("a"), id_("b"))
            assert kv_pair.into_code() == "a: b"
            ```
        """
        self.key = key.into_expression()
        self.value = value.into_expression()

    def into_code(self) -> str:
        return f"{self.key.into_code()}: {self.value.into_code()}"


pair = kv = KVPair
"""Alias for [`KVPair`][synt.tokens.kv_pair.KVPair]."""
