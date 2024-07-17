from __future__ import annotations


__all__ = [
    "DecoratorGroup",
    "dec",
]


from typing import TYPE_CHECKING
from typing import Self

from synt.stmt.cls import ClassDefBuilder
from synt.stmt.fn import FunctionDefBuilder


if TYPE_CHECKING:
    from synt.expr.expr import Expression
    from synt.expr.expr import IntoExpression
    from synt.tokens.ident import Identifier


class DecoratorGroup:
    r"""A group of decorators."""

    decorators: list[Expression]
    """Decorators."""

    def __init__(self, decorator: IntoExpression):
        """Initialize a decorator and create a new group.

        Args:
            decorator: The decorator to add.
        """
        self.decorators = [decorator.into_expression()]

    def dec(self, decorator: IntoExpression) -> Self:
        """Append a new decorator.

        Args:
            decorator: The decorator to add.
        """
        self.decorators.append(decorator.into_expression())
        return self

    def class_(self, name: Identifier) -> ClassDefBuilder:
        """Initialize a class with the decorators.

        Args:
            name: The name of the class.
        """
        cls = ClassDefBuilder()
        cls.decorators = self.decorators
        return cls.class_(name)

    def def_(self, name: Identifier) -> FunctionDefBuilder:
        """Initialize a function with the decorators.

        Args:
            name: The name of the function.
        """
        fn = FunctionDefBuilder()
        fn.decorators = self.decorators
        return fn.def_(name)

    def async_def(self, name: Identifier) -> FunctionDefBuilder:
        """Initialize an async function with the decorators.

        Args:
            name: The name of the function.
        """
        return self.def_(name).async_()


dec = DecoratorGroup
"""Alias [`DecoratorGroup`][synt.stmt.decorator.DecoratorGroup]."""
