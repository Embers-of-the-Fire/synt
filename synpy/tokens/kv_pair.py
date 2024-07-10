from __future__ import annotations


__all__ = [
    "KVPair",
    "pair",
    "kv",
]


from synpy.expr.expr import Expression
from synpy.expr.expr import ExprPrecedence
from synpy.expr.expr import ExprType
from synpy.expr.expr import IntoExpression


class KVPair(Expression):
    """A key-value pair, aka `a: b`.

    This is mainly used in slicing (`x[i:j]`) and dict initializing (`{a: b}`)."""

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
        """
        self.key = key.into_expression()
        self.value = value.into_expression()

    def into_code(self) -> str:
        return f"{self.key.into_code()}: {self.value.into_code()}"


pair = kv = KVPair
"""Alias for [`KVPair`][synpy.tokens.kv_pair.KVPair]."""
