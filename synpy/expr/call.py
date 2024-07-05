from __future__ import annotations


__all__ = [
    "Call",
    "Keyword",
]


import synpy.code as code
import synpy.expr.expr as expr


class Call(expr.Expression):
    """Calling a value.

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
        if self.target.precedence >= self.precedence:
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
    """Keyword arguments of a object call.

    References:
        [`Call`][synpy.expr.call.Call]
        [`Keyword`(PythonAst)](https://docs.python.org/3/library/ast.html#ast.keyword)
    """

    key: str
    """Keyword."""
    value: expr.Expression
    """Value for the argument."""

    def __init__(self, key: str, value: expr.IntoExpression):
        """Initialize a new keyword argument.

        Args:
            key: Keyword.
            value: Value for the argument.
        """
        self.key = key
        self.value = value.into_expression()

    def into_code(self) -> str:
        return f"{self.key}={self.value.into_code()}"
