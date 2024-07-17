from __future__ import annotations


__all__ = [
    "ForLoop",
    "ForLoopBuilder",
    "for_",
    "WhileLoop",
    "WhileLoopBuilder",
    "while_",
]


from typing import TYPE_CHECKING
from typing import Self

from synt.stmt.block import Block
from synt.stmt.stmt import Statement
from synt.type_check import is_tuple


if TYPE_CHECKING:
    from synt.expr.expr import Expression
    from synt.expr.expr import IntoExpression


class ForLoop(Statement):
    r"""The `for` loop.

    Examples:
        ```python
        for_loop = for_(id_("i")).in_(id_("range").expr().call(litint(5))).block(
                       if_(id_("i").expr().gt(litint(2))).block(
                           BREAK
                       ).else_(
                           CONTINUE
                       )
                   ).else_(
                       PASS
                   )
        assert for_loop.into_code() == '''for i in range(5):
            if i > 2:
                break
            else:
                continue
        else:
            pass'''
        # for i in range(5):
        #     if i > 2:
        #         break
        #     else:
        #         continue
        # else:
        #     pass
        ```

    References:
        [`For`](https://docs.python.org/3/library/ast.html#ast.For).
    """

    target: Expression
    """Target item for the iteration.
    
    Notes:
        Tuples will be automatically unwrapped.
    """
    iter: Expression
    """The expression to iterate over."""
    body: Block
    """The body of the loop."""
    orelse: Block | None
    """The body of the fallback block, aka `for ... else`."""

    def __init__(self, target: IntoExpression, it: IntoExpression, body: Block):
        """Initialize the loop.

        **DO NOT USE THIS IN YOUR CODE!**

        Args:
            target: Target item for the iteration.
            it: The expression to iterate over.
            body: The body of the loop.
        """
        self.target = target.into_expression()
        self.iter = it.into_expression()
        self.body = body
        self.orelse = None

    def else_(self, *statements: Statement) -> Self:
        """Set the fallback `else` block.

        Args:
            statements: The body of the fallback block.
        """
        self.orelse = Block(*statements)
        return self

    def indented(self, indent_width: int, indent_atom: str) -> str:
        indent = indent_atom * indent_width
        if self.orelse is not None:
            else_text = f"\n{indent}else:\n{self.orelse.indented(indent_width + 1, indent_atom)}"
        else:
            else_text = ""
        if is_tuple(self.target):
            target_text = self.target.into_code_implicit()
        else:
            target_text = self.target.into_code()
        return (
            f"{indent}for {target_text} in {self.iter.into_code()}:\n"
            f"{self.body.indented(indent_width + 1, indent_atom)}"
            f"{else_text}"
        )


class ForLoopBuilder:
    r"""Builder for `for` loop.

    References:
        [`ForLoop`][synt.stmt.loop.ForLoop].
    """

    target: Expression
    """Target item for the iteration."""
    iter: Expression | None
    """The expression to iterate over."""

    def __init__(self, target: IntoExpression):
        """Initialize a new `for` loop builder.

        Args:
            target: Target item for the iteration.
        """
        self.target = target.into_expression()
        self.iter = None

    def in_(self, it: IntoExpression) -> Self:
        """Set the iterator of the loop.

        Args:
            it: The expression to iterate over.
        """
        self.iter = it.into_expression()
        return self

    def block(self, *statements: Statement) -> ForLoop:
        """Set the block of the loop.

        Args:
            *statements: Statements to include in the loop body.

        Raises:
            ValueError: If the required fields (`[iter,]`) are not set.
        """
        err_fields = []
        if self.iter is None:
            err_fields.append("iter")

        if err_fields:
            raise ValueError(
                f"Missing required field(s): {', '.join(f'`{t}`' for t in err_fields)}"
            )

        return ForLoop(self.target, self.iter, Block(*statements))  # type:ignore[arg-type]


for_ = ForLoopBuilder
"""Alias [`ForLoopBuilder`][synt.stmt.loop.ForLoopBuilder]."""


class WhileLoop:
    r"""The `while` loop.

    References:
        [`While`](https://docs.python.org/3/library/ast.html#ast.While).
    """

    test: Expression
    """The condition."""
    orelse: Block | None
    """The body of the fallback block, aka `while ... else`."""

    def __init__(self, test: IntoExpression, body: Block):
        """Initialize a new `while` loop.

        **DO NOT USE THIS IN YOUR CODE!**

        Args:
            test: The condition.
            body: The body of the loop.
        """
        self.test = test.into_expression()
        self.orelse = None
        self.body = body

    def else_(self, *statements: Statement) -> Self:
        """Set the fallback `else` block.

        Args:
            statements: The body of the fallback block.
        """
        self.orelse = Block(*statements)
        return self

    def indented(self, indent_width: int, indent_atom: str) -> str:
        indent = indent_atom * indent_width
        if self.orelse is not None:
            else_text = f"\n{indent}else:\n{self.orelse.indented(indent_width + 1, indent_atom)}"
        else:
            else_text = ""
        return (
            f"{indent}while {self.test.into_code()}:\n"
            f"{self.body.indented(indent_width + 1, indent_atom)}"
            f"{else_text}"
        )


class WhileLoopBuilder:
    r"""Builder for `while` loop.

    Examples:
        ```python
        while_loop = while_(id_("i").expr().lt(litint(5))).block(
                         id_("i").assign(id_("i").expr() + litint(1))
                     ).else_(
                         PASS
                     )
        assert while_loop.into_code() == '''while i < 5:
            i = i + 1
        else:
            pass'''
        # while i < 5:
        #     i = i + 1
        # else:
        #     pass
        ```

    References:
        [`WhileLoop`][synt.stmt.loop.WhileLoop].
    """

    test: Expression
    """The condition."""

    def __init__(self, test: IntoExpression):
        """Initialize a new `while` loop builder.

        Args:
            test: The condition.
        """
        self.test = test.into_expression()

    def block(self, *statements: Statement) -> WhileLoop:
        """Set the block of the loop.

        Args:
            *statements: Statements to include in the loop body.
        """
        return WhileLoop(self.test, Block(*statements))


while_ = WhileLoopBuilder
"""Alias [`WhileLoopBuilder`][synt.stmt.loop.WhileLoopBuilder]."""
