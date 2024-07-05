from __future__ import annotations


__all__ = [
    "Empty",
    "null",
    "expr",
]


import synpy.expr.expr as syn_expr


class Empty(syn_expr.Expression):
    """Empty expression.

    References:
        [expr.ExprType.Empty][synpy.expr.expr.ExprType.Empty].
    """

    precedence = syn_expr.ExprPrecedence.Atom
    expr_type = syn_expr.ExprType.Identifier

    def __init__(self) -> None:
        pass

    def into_code(self) -> str:
        return ""


empty = expr = null = Empty
"""Alias [`Empty`][synpy.expr.empty.Empty]."""
