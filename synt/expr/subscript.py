from __future__ import annotations


__all__ = [
    "Subscript",
    "Slice",
    "slice_",
]

import synt.code as code
import synt.expr.expr as expr


class Subscript(expr.Expression):
    r"""Subscript operation.

    References:
        [Subscription](https://docs.python.org/3/reference/expressions.html#grammar-token-python-grammar-subscription).
    """

    target: expr.Expression
    """Target of the operation."""
    slices: list[Slice | expr.Expression]
    """Slices to index the target."""

    expr_type = expr.ExprType.Subscript
    precedence = expr.ExprPrecedence.Call

    def __init__(
        self, target: expr.IntoExpression, slices: list[Slice | expr.IntoExpression]
    ):
        """Initialize a `Subscript` operation.

        Args:
            target: Target of the operation.
            slices: Slices to index the target.
        """
        self.target = target.into_expression()
        if (
            self.target.precedence > self.precedence
        ):  # special rule here, attr call doesn't need a wrap
            self.target = self.target.wrapped()
        self.slices = [
            s if isinstance(s, Slice) else s.into_expression() for s in slices
        ]

    def into_code(self) -> str:
        slice_text = ", ".join(x.into_code() for x in self.slices)
        return f"{self.target.into_code()}[{slice_text}]"


class Slice(code.IntoCode):
    r"""Slice constructor.

    ```python
    foo[
        5     # lower
        :10   # upper
        :2    # step (optional)
    ]
    ```

    Examples:
        ```python
        sl = slice_(litint(5), litint(10))
        assert sl.into_code() == "5:10"
        sl = slice_(litint(5), litint(10), id_("a"))
        assert sl.into_code() == "5:10:a"
        ```

    References:
        [Slice](https://docs.python.org/3/library/ast.html#ast.Slice).
    """

    lower: expr.Expression
    """Lower bound of the slice."""
    upper: expr.Expression
    """Upper bound of the slice."""
    step: expr.Expression | None
    """Step of the slice."""

    def __init__(
        self,
        lower: expr.IntoExpression,
        upper: expr.IntoExpression,
        step: expr.IntoExpression | None = None,
    ):
        """Initialize the slice.

        Args:
            lower: Lower bound of the slice.
            upper: Upper bound of the slice.
            step: Step of the slice.
        """
        self.lower = lower.into_expression()
        self.upper = upper.into_expression()
        self.step = step.into_expression() if step else None

    def into_code(self) -> str:
        if self.step:
            return f"{self.lower.into_code()}:{self.upper.into_code()}:{self.step.into_code()}"
        else:
            return f"{self.lower.into_code()}:{self.upper.into_code()}"


slice_ = Slice
"""Alias [`Slice`][synt.expr.subscript.Slice].

Notes:
    `slice` is a built-in type in Python, so it's renamed to `slice_` with a suffix.
"""
