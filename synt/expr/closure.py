from __future__ import annotations


__all__ = [
    "Closure",
    "ClosureBuilder",
    "lambda_",
]


from typing import TYPE_CHECKING
from typing import Self

import synt.code as code
import synt.expr.expr as expr


if TYPE_CHECKING:
    from synt.tokens.ident import Identifier


class Closure(expr.Expression, code.IntoCode):
    r"""Python's closure expression, aka `lambda`.

    Notes:
        In Python, a lambda expression can have a single expression as its body.
        Synt won't try to create a separate function containing multiple statements,
        you must do it yourself.

    References:
        [expr.ExprPrecedence.Lambda][synt.expr.expr.ExprPrecedence.Lambda].
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
    r"""Builder for [`Closure`][synt.expr.closure.Closure].

    Examples:
        ```python
        closure = (
            lambda_(id_("x"), id_("y")) # initial a closure builder
            .join(id_("z")) # append new argument, optional
            .return_(id_("x").expr() + id_("y") + id_("z")) # set the expression to be returned and build the closure
        )
        assert closure.into_code() == "lambda x, y, z: x + y + z"
        ```
    """

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

    def ret(self, e: expr.IntoExpression) -> Closure:
        """Set the expression to be returned by the closure.

        Args:
            e: expr.Expression to be returned.
        """
        return Closure(self.__args, e)

    def return_(self, e: expr.IntoExpression) -> Closure:
        """Alias [`ret`][synt.expr.closure.ClosureBuilder.ret]."""
        return self.ret(e)


lambda_ = ClosureBuilder
"""Alias [`ClosureBuilder`][synt.expr.closure.ClosureBuilder]."""
