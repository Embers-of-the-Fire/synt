from __future__ import annotations


__all__ = [
    "Closure",
    "ClosureBuilder",
    "lambda_",
]


from typing import TYPE_CHECKING
from typing import Self

import synpy.code as code
import synpy.expr.expr as expr


if TYPE_CHECKING:
    from synpy.tokens.ident import Identifier


class Closure(expr.Expression, code.IntoCode):
    """Python's closure expression, aka `lambda`.

    Notes:
        In Python, a lambda expression can have a single expression as its body.
        SynPy won't try to create a separate function containing multiple statements,
        you must do it yourself.

    References:
        [expr.ExprPrecedence.Lambda][synpy.expr.expr.ExprPrecedence.Lambda].
    """

    args: list[Identifier]
    """Argument list."""
    body: expr.Expression
    """expr.Expression body."""

    precedence = expr.ExprPrecedence.Lambda
    expr_type = expr.ExprType.Closure

    def __init__(self, args: list[Identifier], body: expr.IntoExpression):
        """Initialize a closure expression.

        Args:
            args: Argument list.
            body: expr.Expression body.
        """
        self.args = args
        self.body = body.into_expression()
        if self.body.precedence > self.precedence:
            self.body = self.body.wrapped()

    def into_code(self) -> str:
        return f"lambda {', '.join(arg.into_code() for arg in self.args)}: {self.body.into_code()}"


class ClosureBuilder:
    """Builder for [`Closure`][synpy.expr.closure.Closure]."""

    __args: list[Identifier]

    def __init__(self, *args: Identifier):
        """Initialize a closure.

        Args:
            *args: Initial closure argument list.
        """
        self.__args = list(args)

    def join(self, *args: Identifier) -> Self:
        """Append new arguments to the closure.

        Args:
            *args: New closure arguments.
        """
        self.__args.extend(args)
        return self

    def ret(self, expr: expr.IntoExpression) -> Closure:
        """Set the expression to be returned by the closure.

        Args:
            expr: expr.Expression to be returned.
        """
        return Closure(self.__args, expr)

    def return_(self, expr: expr.IntoExpression) -> Closure:
        """Alias [`ret`][synpy.expr.closure.ClosureBuilder.ret]."""
        return self.ret(expr)


lambda_ = ClosureBuilder
"""Alias [`ClosureBuilder`][synpy.expr.closure.ClosureBuilder]."""
