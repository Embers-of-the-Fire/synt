from __future__ import annotations


__all__ = [
    "BinaryOpType",
    "BinaryOp",
]


from enum import IntEnum
from typing import TYPE_CHECKING

import synt.expr.expr as expr


if TYPE_CHECKING:
    from synt.expr.expr import ExprPrecedence


class BinaryOpType(IntEnum):
    r"""Binary operator type.

    **Exception:**
    Although [`NamedExpr`][synt.expr.expr.ExprPrecedence.NamedExpr]
    takes the form of a binary operator, it is not a binary operator (at least not in `synt`).

    References:
        [`expr.ExprPrecedence`][synt.expr.expr.ExprPrecedence]
    """

    Add = 0
    """Addition operator `+`."""
    Sub = 1
    """Subtraction operator `-`."""
    Mul = 2
    """Multiplication operator `*`."""
    Div = 3
    """Division operator `/`."""
    FloorDiv = 4
    """Floor division operator `//`."""
    Mod = 5
    """Modulus(remainder) operator `%`."""
    Pow = 6
    """Exponent(power) operator `**`."""
    At = 7
    """At(matrix multiplication) operator `@`."""
    LShift = 8
    """Left shift operator `<<`."""
    RShift = 9
    """Right shift operator `>>`."""
    In = 10
    """Membership test operator `in`."""
    NotIn = 11
    """Negative membership test operator group `not in`."""
    Is = 12
    """Identity test operator `is`."""
    IsNot = 13
    """Negative identity test operator group `is not`."""
    Less = 14
    """'Less than' operator `<`."""
    LessEqual = 15
    """'Less than or Equal' operator `<=`."""
    Greater = 16
    """'Greater than' operator `>`."""
    GreaterEqual = 17
    """'Greater than or Equal' operator `>=`."""
    Equal = 18
    """'Equal' operator `==`."""
    NotEqual = 19
    """Negative 'Equal' operator `!=`."""
    BitAnd = 20
    """Bitwise AND operator `&`."""
    BitOr = 21
    """Bitwise OR operator `|`."""
    BitXor = 22
    """Bitwise XOR operator `^`."""
    BoolAnd = 23
    """Boolean AND operator `and`."""
    BoolOr = 24
    """Boolean OR operator `or`."""

    def to_precedence(self) -> expr.ExprPrecedence:
        """Get the operator's backend expression's precedence."""
        match self:
            case BinaryOpType.Add | BinaryOpType.Sub:
                return expr.ExprPrecedence.Additive
            case (
                BinaryOpType.Mul
                | BinaryOpType.Div
                | BinaryOpType.FloorDiv
                | BinaryOpType.Mod
                | BinaryOpType.At
            ):
                return expr.ExprPrecedence.Multiplicative
            case BinaryOpType.Pow:
                return expr.ExprPrecedence.Exponential
            case BinaryOpType.LShift | BinaryOpType.RShift:
                return expr.ExprPrecedence.Shift
            case (
                BinaryOpType.In
                | BinaryOpType.NotIn
                | BinaryOpType.Is
                | BinaryOpType.IsNot
                | BinaryOpType.Less
                | BinaryOpType.LessEqual
                | BinaryOpType.Greater
                | BinaryOpType.GreaterEqual
                | BinaryOpType.Equal
                | BinaryOpType.NotEqual
            ):
                return expr.ExprPrecedence.Comparative
            case BinaryOpType.BitAnd:
                return expr.ExprPrecedence.BitAnd
            case BinaryOpType.BitOr:
                return expr.ExprPrecedence.BitOr
            case BinaryOpType.BitXor:
                return expr.ExprPrecedence.BitXor
            case BinaryOpType.BoolAnd:
                return expr.ExprPrecedence.BoolAnd
            case BinaryOpType.BoolOr:
                return expr.ExprPrecedence.BoolOr
            case _:
                raise ValueError(
                    f"Unrecognized binary operator type: {self} [{self.value}]"
                )

    def into_code(self) -> str:
        """
        Raises:
            ValueError: If the provided operator type is not recognized.
        """
        match self:
            case BinaryOpType.Add:
                return "+"
            case BinaryOpType.Sub:
                return "-"
            case BinaryOpType.Mul:
                return "*"
            case BinaryOpType.Div:
                return "/"
            case BinaryOpType.FloorDiv:
                return "//"
            case BinaryOpType.Mod:
                return "%"
            case BinaryOpType.Pow:
                return "**"
            case BinaryOpType.At:
                return "@"
            case BinaryOpType.LShift:
                return "<<"
            case BinaryOpType.RShift:
                return ">>"
            case BinaryOpType.In:
                return "in"
            case BinaryOpType.NotIn:
                return "not in"
            case BinaryOpType.Is:
                return "is"
            case BinaryOpType.IsNot:
                return "is not"
            case BinaryOpType.Less:
                return "<"
            case BinaryOpType.LessEqual:
                return "<="
            case BinaryOpType.Greater:
                return ">"
            case BinaryOpType.GreaterEqual:
                return ">="
            case BinaryOpType.Equal:
                return "=="
            case BinaryOpType.NotEqual:
                return "!="
            case BinaryOpType.BitAnd:
                return "&"
            case BinaryOpType.BitOr:
                return "|"
            case BinaryOpType.BitXor:
                return "^"
            case BinaryOpType.BoolAnd:
                return "and"
            case BinaryOpType.BoolOr:
                return "or"
            case _:
                raise ValueError(f"Unrecognized binary operator type: {self}")


class BinaryOp(expr.Expression):
    r"""Binary operation."""

    left: expr.Expression
    """Left operand expression."""
    right: expr.Expression
    """Right operand expression."""
    op_type: BinaryOpType
    """Operator type."""

    expr_type = expr.ExprType.BinaryOp

    def __init__(
        self, op: BinaryOpType, left: expr.IntoExpression, right: expr.IntoExpression
    ):
        """Initialize a binary operation.

        Args:
            op: Binary operator type.
            left: Left operand.
            right: Right operand.
        """
        self.left = left.into_expression()
        self.right = right.into_expression()
        self.op_type = op

        if self.left.precedence > self.precedence:
            self.left = self.left.wrapped()
        if self.right.precedence > self.precedence:
            self.right = self.right.wrapped()

    def into_code(self) -> str:
        return f"{self.left.into_code()} {self.op_type.into_code()} {self.right.into_code()}"

    @property
    def precedence(self) -> ExprPrecedence:
        """expr.Expression precedence.

        References:
            [BinaryOpType.to_precedence][synt.expr.binary_op.BinaryOpType.to_precedence].
        """
        return self.op_type.to_precedence()
