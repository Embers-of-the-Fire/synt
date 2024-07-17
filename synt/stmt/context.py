from __future__ import annotations


__all__ = [
    "WithItem",
    "With",
    "WithBuilder",
    "with_item",
    "with_",
]


from typing import TYPE_CHECKING
from typing import Self

from synt.code import IntoCode
from synt.stmt.block import Block
from synt.stmt.stmt import Statement


if TYPE_CHECKING:
    from synt.expr.expr import Expression
    from synt.expr.expr import IntoExpression


class WithItem(IntoCode):
    """An item of the `with` statement.

    References:
        [`withitem`](https://docs.python.org/3/library/ast.html#ast.withitem).
    """

    context: Expression
    """The context expression."""
    asname: Expression | None
    """The alias for the context expression.
    
    Notes:
        ```python
        with a as b:
            ...
        ```
        Consider the above example, the context returned by `a` is assigned to `b`.
        Hence, `b`, the syntax node, must be an assignable object, that is,
        a `tuple`, `list`, or a single `Identifier`.
    """

    def __init__(self, context: IntoExpression):
        """Initialize a new `with` item.

        Args:
            context: The context expression.
        """
        self.context = context.into_expression()
        self.asname = None

    def as_(self, asname: IntoExpression) -> Self:
        """Set the alias.

        Args:
            asname: The alias for the context expression.
        """
        self.asname = asname.into_expression()
        return self

    def into_code(self) -> str:
        asname_text = (
            f" as {self.asname.into_code()}" if self.asname is not None else ""
        )
        return f"{self.context.into_code()}{asname_text}"


with_item = WithItem
"""Alias [`WithItem`][synt.stmt.context.with_item]."""


class With(Statement):
    """The `with` statement.

    Examples:
        ```python
        with_stmt = with_(id_("a"), (id_("b"), id_("b2")), with_item(id_("c")).as_(id_("c2"))).block(
                        PASS
                    )
        assert with_stmt.into_code() == "with a, b as b2, c as c2:\n    pass"
        ```

    References:
        [`With`](https://docs.python.org/3/library/ast.html#ast.With).
    """

    items: list[WithItem]
    """`with` items."""
    body: Block
    """Statement block."""

    def __init__(self, items: list[WithItem], body: Block):
        """Initialize a `with` statement.

        **DO NOT USE THIS IN YOUR CODE!**

        Args:
            items: `with` items.
            body: Statement block.

        Raises:
            ValueError: If `items` is empty.
        """
        if len(items) == 0:
            raise ValueError("At least one `with` item is required.")
        self.items = items
        self.body = body

    def indented(self, indent_width: int, indent_atom: str) -> str:
        return (
            f"{indent_atom * indent_width}with {', '.join(x.into_code() for x in self.items)}:\n"
            f"{self.body.indented(indent_width + 1, indent_atom)}"
        )


class WithBuilder:
    """The builder for [`With`][synt.stmt.context.With]."""

    items: list[WithItem]
    """`with` items."""

    def __init__(
        self, *items: WithItem | IntoExpression | tuple[IntoExpression, IntoExpression]
    ):
        """Initialize a `with` statement.

        The `items`'s item could be either `WithItem` object, an expression-like or a tuple:
        - `WithItem`: Save as-is.
        - Expression-like: Convert into a `WithItem` without any alias.
        - `tuple[IntoExpression, IntoExpression]`: The first element is the context, and the second is the alias.

        Args:
            items: `with` items.

        Raises:
            ValueError: If `items` is empty.
        """
        if len(items) == 0:
            raise ValueError("At least one `with` item is required.")
        self.items = []
        for item in items:
            if isinstance(item, tuple):
                self.items.append(
                    WithItem(item[0].into_expression()).as_(item[1].into_expression())
                )
            elif isinstance(item, WithItem):
                self.items.append(item)
            else:
                self.items.append(WithItem(item.into_expression()))

    def block(self, *statements: Statement) -> With:
        """Set the code block.

        Args:
            statements: block statements.
        """
        return With(self.items, Block(*statements))


with_ = WithBuilder
"""Alias [`WithBuilder`][synt.stmt.context.WithBuilder]."""
