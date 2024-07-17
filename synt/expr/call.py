from __future__ import annotations


__all__ = [
    "Call",
    "Keyword",
]

from typing import TYPE_CHECKING

import synt.code as code
import synt.expr.expr as expr


if TYPE_CHECKING:
    from synt.tokens.ident import Identifier


class Call(expr.Expression):
    r"""Calling a value.

    References:
        [Call](https://docs.python.org/3/library/ast.html#ast.Call).
    """

    target: expr.Expression
    """Call target."""
    args: list[expr.Expression]
    """Positional arguments of the call."""
    keywords: list[Keyword]
    """Keyword arguments of the call."""

    precedence = expr.ExprPrecedence.Call
    expr_type = expr.ExprType.Call

    def __init__(
        self,
        target: expr.IntoExpression,
        args: list[expr.IntoExpression],
        keywords: list[Keyword],
    ):
        """Initialize a new `Call`.

        Args:
            target: Call target.
            args: Positional arguments of the call.
            keywords: Keyword arguments of the call.
        """
        self.target = target.into_expression()
        if self.target.precedence > self.precedence:
            self.target = self.target.wrapped()

        self.args = [arg.into_expression() for arg in args]
        self.keywords = keywords

    def into_code(self) -> str:
        arg_text = ""
        if self.args:
            args_text = ", ".join(arg.into_code() for arg in self.args)
            if self.keywords:
                kwargs_text = ", ".join(kw.into_code() for kw in self.keywords)
                arg_text = f"{args_text}, {kwargs_text}"
            else:
                arg_text = args_text
        elif self.keywords:
            arg_text = ", ".join(kw.into_code() for kw in self.keywords)

        return f"{self.target.into_code()}({arg_text})"


class Keyword(code.IntoCode):
    r"""Keyword arguments of a object call.

    References:
        [`Call`][synt.expr.call.Call]
        [`Keyword`(PythonAst)](https://docs.python.org/3/library/ast.html#ast.keyword)
    """

    key: Identifier
    """Keyword."""
    value: expr.Expression
    """Value for the argument."""

    def __init__(self, key: Identifier, value: expr.IntoExpression):
        """Initialize a new keyword argument.

        Args:
            key: Keyword.
            value: Value for the argument.
        """
        self.key = key
        self.value = value.into_expression()

    def into_code(self) -> str:
        return f"{self.key.into_code()}={self.value.into_code()}"
