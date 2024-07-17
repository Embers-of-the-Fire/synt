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

import synt.expr.expr as expr


if TYPE_CHECKING:
    from synt.expr.expr import ExprPrecedence


class UnaryOpType(IntEnum):
    r"""Unary operator type.

    References:
        [`expr.ExprPrecedence`][synt.expr.expr.ExprPrecedence]
    """

    Await = 0
    """Await expression operator `await`.
    
    Notes:
        `await` is a Python hard keyword, but synt treats it as a unary operator.
    """

    Yield = 1
    """Yield expression operator `yield`.
    
    Notes:
        `yield` is a Python hard keyword, but synt treats it as a unary operator.
    """

    YieldFrom = 2
    """Yield-from expression operator `yield from`.
    
    Notes:
        `yield from` is a Python hard keyword group, but synt treats it as a single unary operator.
    """

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
    r"""Unary operation."""

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
            [Unary.to_precedence][synt.expr.unary_op.UnaryOpType.to_precedence].
        """
        return self.op_type.to_precedence()


def await_(e: expr.IntoExpression) -> UnaryOp:
    r"""Create an `await` expression.

    Examples:
        ```python
        await_expr = await_(litint(10))
        assert await_expr.into_code() == "await 10"
        ```
    """
    return UnaryOp(UnaryOpType.Await, e)


awaited = await_
"""Alias [`await_`][synt.expr.unary_op.await_]."""


def unpack(e: expr.IntoExpression) -> UnaryOp:
    r"""Sequence unpacking operation.

    Examples:
        ```python
        unpacked_expr = unpack(list_(litint(1), litint(2), litint(3)))
        assert unpacked_expr.into_code() == "* [1, 2, 3]"
        ```
    """
    return UnaryOp(UnaryOpType.Starred, e)


starred = unpack_seq = unpack
"""Alias [`unpack`][synt.expr.unary_op.unpack]."""


def unpack_kv(e: expr.IntoExpression) -> UnaryOp:
    r"""K-V pair unpacking operation.

    Examples:
        ```python
        unpacked_expr = unpack_kv(dict_(kv(litint(1), litstr('a'))))
        assert unpacked_expr.into_code() == "** {1: 'a'}"
        ```
    """
    return UnaryOp(UnaryOpType.DoubleStarred, e)


double_starred = unpack_dict = unpack_kv
"""Alias [`unpack_kv`][synt.expr.unary_op.unpack_kv]."""


def positive(e: expr.IntoExpression) -> UnaryOp:
    r"""Positive operation.

    Examples:
        ```python
        positive_expr = positive(litint(10))
        assert positive_expr.into_code() == "+ 10"
        ```
    """
    return UnaryOp(UnaryOpType.Positive, e)


def negative(e: expr.IntoExpression) -> UnaryOp:
    r"""Negative operation.

    Examples:
        ```python
        positive_expr = negative(litint(10))
        assert positive_expr.into_code() == "- 10"
        ```
    """
    return UnaryOp(UnaryOpType.Positive, e)


neg = negative
"""Alias [`negative`][synt.expr.unary_op.negative]."""


def not_(e: expr.IntoExpression) -> UnaryOp:
    r"""Boolean NOT operation.

    Examples:
        ```python
        not_expr = not_(id_("foo"))
        assert not_expr.into_code() == "not foo"
        ```
    """
    return UnaryOp(UnaryOpType.BoolNot, e)


bool_not = not_
"""Alias [`not_`][synt.expr.unary_op.not_]."""


def invert(e: expr.IntoExpression) -> UnaryOp:
    r"""Bitwise NOT operation.

    Examples:
        ```python
        not_expr = invert(id_("foo"))
        assert not_expr.into_code() == "~ foo"
        ```
    """
    return UnaryOp(UnaryOpType.BitNot, e)


bit_not = invert
"""Alias [`invert`][synt.expr.unary_op.invert]."""


def yield_(e: expr.Expression) -> UnaryOp:
    r"""Yield operation.

    Examples:
        ```python
        yield_expr = yield_(litint(10))
        assert yield_expr.into_code() == "yield 10"
        ```
    """
    return UnaryOp(UnaryOpType.Yield, e)


def yield_from(e: expr.Expression) -> UnaryOp:
    r"""Yield from operation.

    Examples:
        ```python
        yield_expr = yield_from(list_(litint(10), litint(42)))
        assert yield_expr.into_code() == "yield from [10, 42]"
        ```
    """
    return UnaryOp(UnaryOpType.YieldFrom, e)
