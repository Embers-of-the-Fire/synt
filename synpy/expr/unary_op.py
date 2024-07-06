from __future__ import annotations


__all__ = [
    "UnaryOpType",
    "UnaryOp",
    "awaited",
    "await_",
    "unpack",
    "starred",
    "unpack_seq",
    "unpack_dict",
    "unpack_kv",
    "double_starred",
    "positive",
    "negative",
    "neg",
    "not_",
    "bool_not",
    "invert",
    "bit_not",
    "yield_",
    "yield_from",
]


from enum import IntEnum
from typing import TYPE_CHECKING

import synpy.expr.expr as expr


if TYPE_CHECKING:
    from synpy.expr.expr import ExprPrecedence


class UnaryOpType(IntEnum):
    """Unary operator type.

    References:
        [`expr.ExprPrecedence`][synpy.expr.expr.ExprPrecedence]
    """

    Await = 0
    """Await expression operator `await`.
    
    Notes:
        `await` is a Python hard keyword, but synpy treats it as a unary operator.
    """

    Yield = 1

    YieldFrom = 2

    Starred = 3
    """Tuple/list extractor operator `*`."""

    DoubleStarred = 4
    """Dict/mapping extractor operator `**`."""

    Positive = 5
    """Positive operator `+`."""

    Neg = 6
    """Negative operator `-`."""

    BitNot = 7
    """Bitwise NOT operator `~`."""

    BoolNot = 8
    """Boolean NOT operator `not`."""

    def to_precedence(self) -> expr.ExprPrecedence:
        """Get the operator's backend expression's precedence."""
        match self:
            case (
                UnaryOpType.Starred
                | UnaryOpType.DoubleStarred
                | UnaryOpType.Yield
                | UnaryOpType.YieldFrom
            ):
                return expr.ExprPrecedence.Atom
            case UnaryOpType.Await:
                return expr.ExprPrecedence.Await
            case UnaryOpType.Positive | UnaryOpType.Neg | UnaryOpType.BitNot:
                return expr.ExprPrecedence.Unary
            case UnaryOpType.BoolNot:
                return expr.ExprPrecedence.BoolNot
            case _:
                raise ValueError(
                    f"Unexpected unary operator type: {self} [{self.value}]"
                )

    def into_code(self) -> str:
        """Converts the operator into a string representation.

        Raises:
            ValueError: If the operator is not recognized.
        """
        match self:
            case UnaryOpType.Starred:
                return "*"
            case UnaryOpType.DoubleStarred:
                return "**"
            case UnaryOpType.Yield:
                return "yield"
            case UnaryOpType.YieldFrom:
                return "yield from"
            case UnaryOpType.Await:
                return "await"
            case UnaryOpType.Positive:
                return "+"
            case UnaryOpType.Neg:
                return "-"
            case UnaryOpType.BitNot:
                return "~"
            case UnaryOpType.BoolNot:
                return "not"


class UnaryOp(expr.Expression):
    """Unary operation."""

    expression: expr.Expression
    """Internal expression."""
    op_type: UnaryOpType
    """Operator type."""
    expr_type = expr.ExprType.UnaryOp

    def __init__(self, op: UnaryOpType, e: expr.IntoExpression):
        """Initialize a unary operation.

        Args:
            op: Unary operator type.
            e: Internal expression.
        """
        self.expression = e.into_expression()
        self.op_type = op

        if self.expression.precedence > self.precedence:
            self.expression = self.expression.wrapped()

    def into_code(self) -> str:
        return f"{self.op_type.into_code()} {self.expression.into_code()}"

    @property
    def precedence(self) -> ExprPrecedence:
        """expr.Expression precedence.

        References:
            [Unary.to_precedence][synpy.expr.unary_op.UnaryOpType.to_precedence].
        """
        return self.op_type.to_precedence()


def await_(e: expr.IntoExpression) -> UnaryOp:
    """Create an `await` expression."""
    return UnaryOp(UnaryOpType.Await, e)


awaited = await_
"""Alias [`await_`][synpy.expr.unary_op.await_]."""


def unpack(e: expr.IntoExpression) -> UnaryOp:
    """Sequence unpacking operation."""
    return UnaryOp(UnaryOpType.Starred, e)


starred = unpack_seq = unpack
"""Alias [`unpack`][synpy.expr.unary_op.unpack]."""


def unpack_kv(e: expr.IntoExpression) -> UnaryOp:
    """K-V pair unpacking operation."""
    return UnaryOp(UnaryOpType.Starred, e)


double_starred = unpack_dict = unpack_kv
"""Alias [`unpack_kv`][synpy.expr.unary_op.unpack_kv]."""


def positive(e: expr.IntoExpression) -> UnaryOp:
    """Positive operation."""
    return UnaryOp(UnaryOpType.Positive, e)


def negative(e: expr.IntoExpression) -> UnaryOp:
    """Negative operation."""
    return UnaryOp(UnaryOpType.Positive, e)


neg = negative
"""Alias [`negative`][synpy.expr.unary_op.negative]."""


def not_(e: expr.IntoExpression) -> UnaryOp:
    """Boolean NOT operation."""
    return UnaryOp(UnaryOpType.BoolNot, e)


bool_not = not_
"""Alias [`not_`][synpy.expr.unary_op.not_]."""


def invert(e: expr.Expression) -> UnaryOp:
    """Bitwise NOT operation."""
    return UnaryOp(UnaryOpType.BitNot, e)


bit_not = invert
"""Alias [`invert`][synpy.expr.unary_op.invert]."""


def yield_(e: expr.Expression) -> UnaryOp:
    """Yield operation."""
    return UnaryOp(UnaryOpType.Yield, e)


def yield_from(e: expr.Expression) -> UnaryOp:
    """Yield from operation."""
    return UnaryOp(UnaryOpType.YieldFrom, e)
