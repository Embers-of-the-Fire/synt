from __future__ import annotations


__all__ = [
    "Empty",
    "null",
    "expr",
    "empty",
    "EMPTY",
    "NULL",
]


import synt.expr.expr as syn_expr


class Empty(syn_expr.Expression):
    r"""Empty expression.

    References:
        [expr.ExprType.Empty][synt.expr.expr.ExprType.Empty].
    """

    precedence = syn_expr.ExprPrecedence.Atom
    expr_type = syn_expr.ExprType.Identifier

    def __init__(self) -> None:
        pass

    def into_code(self) -> str:
        return ""


empty = expr = null = Empty
"""Alias [`Empty`][synt.expr.empty.Empty]."""

EMPTY = NULL = Empty()
"""An instance of [`Empty`][synt.expr.empty.Empty]."""
