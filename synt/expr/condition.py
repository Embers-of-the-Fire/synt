from __future__ import annotations


__all__ = [
    "Condition",
    "ConditionBuilder",
]


from typing import Self

import synt.expr.expr as expr


class Condition(expr.Expression):
    r"""Conditional expression, aka `if - else`.

    References:
        [expr.ExprPrecedence.Conditional][synt.expr.expr.ExprPrecedence.Conditional].
    """

    condition: expr.Expression
    """Condition expression."""
    true_expr: expr.Expression
    """expr.Expression to evaluate and return if the condition is true."""
    false_expr: expr.Expression
    """expr.Expression to evaluate and return if the condition is false."""
    precedence = expr.ExprPrecedence.Conditional
    expr_type = expr.ExprType.Condition

    def __init__(
        self,
        condition: expr.IntoExpression,
        true_expr: expr.IntoExpression,
        false_expr: expr.IntoExpression,
    ):
        """Initialize a new conditional expression.

        Args:
            condition: Condition expression.
            true_expr: expr.Expression to evaluate and return if the condition is true.
            false_expr: expr.Expression to evaluate and return if the condition is false.
        """
        self.condition = condition.into_expression()
        if self.condition.precedence > self.precedence:
            self.condition = self.condition.wrapped()
        self.true_expr = true_expr.into_expression()
        if self.true_expr.precedence > self.precedence:
            self.true_expr = self.true_expr.wrapped()
        self.false_expr = false_expr.into_expression()
        if self.false_expr.precedence > self.precedence:
            self.false_expr = self.false_expr.wrapped()

    def into_code(self) -> str:
        return f"{self.true_expr.into_code()} if {self.condition.into_code()} else {self.false_expr.into_code()}"


class ConditionBuilder:
    r"""Builder for [`Condition`][synt.expr.condition.Condition]."""

    __condition: expr.Expression
    __true_expr: expr.Expression
    __false_expr: expr.Expression | None

    def __init__(self, condition: expr.IntoExpression, true_expr: expr.IntoExpression):
        """Initialize an empty condition builder.

        Args:
            condition: Condition expression.
            true_expr: expr.Expression to evaluate if the condition is true.
        """
        self.__condition = condition.into_expression()
        self.__true_expr = true_expr.into_expression()
        self.__false_expr = None

    def false_expr(self, e: expr.IntoExpression) -> Self:
        """Set the expression to evaluate if the condition is false.

        Args:
            e: expr.Expression to evaluate.
        """
        self.__false_expr = e.into_expression()
        return self

    def build(self) -> Condition:
        """Build the condition.

        Raises:
            ValueError: If any of the required field is empty.
        """
        err_fields = []
        if self.__false_expr is None:
            err_fields.append("false_expr")

        if err_fields:
            raise ValueError(
                f"Missing required field(s): {', '.join(f'`{t}`' for t in err_fields)}"
            )
        return Condition(self.__condition, self.__true_expr, self.__false_expr)  # type:ignore[arg-type]

    def else_(self, other: expr.IntoExpression) -> Condition:
        """Set the `false_expr` and build the builder.

        Args:
            other: expr.Expression to evaluate if the condition is false.

        Raises:
            ValueError: If any of the required field is empty.
        """
        self.false_expr(other)
        return self.build()
