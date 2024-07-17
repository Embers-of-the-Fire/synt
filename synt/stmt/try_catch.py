from __future__ import annotations


__all__ = [
    "ExceptionHandler",
    "ExceptionHandlerBuilder",
    "Try",
    "try_",
]


from typing import TYPE_CHECKING
from typing import Self

from synt.stmt.block import Block
from synt.stmt.stmt import Statement


if TYPE_CHECKING:
    from synt.expr.expr import Expression
    from synt.expr.expr import IntoExpression
    from synt.tokens.ident import Identifier


class ExceptionHandler(Statement):
    r"""Exception handler.

    References:
        [`ExceptionHandler`](https://docs.python.org/3/library/ast.html#ast.ExceptHandler).
    """

    is_group: bool
    """Whether the exception handler is a group handler."""
    type: Expression | None
    """The type of exception to catch."""
    asname: Identifier | None
    """The alias name."""
    body: Block
    """The handler body."""

    def __init__(
        self,
        ty: IntoExpression | None,
        is_group: bool,
        asname: Identifier | None,
        body: Block,
    ):
        """Initialize a new exception handler.

        **DO NOT USE THIS IN YOUR CODE!**

        Args:
            ty: The type of exception to catch.
            is_group: Whether the exception handler is a group handler, aka `except*`.
            asname: The alias name.
            body: The handler body.
        """
        if ty is not None:
            self.type = ty.into_expression()
        else:
            self.type = None
        self.is_group = is_group
        self.asname = asname
        self.body = body

    def indented(self, indent_width: int, indent_atom: str) -> str:
        indent = indent_width * indent_atom
        except_kwd = "except*" if self.is_group else "except"
        type_text = f" {self.type.into_code()}" if self.type is not None else ""
        as_text = f" as {self.asname.into_code()}" if self.asname is not None else ""
        return (
            f"{indent}{except_kwd}{type_text}{as_text}:\n"
            f"{self.body.indented(indent_width + 1, indent_atom)}"
        )


class ExceptionHandlerBuilder:
    r"""The builder for exception handlers.

    References:
        [`ExceptionHandler`][synt.stmt.try_catch.ExceptionHandler].
    """

    is_group: bool
    """Whether the exception handler is a group handler, aka `except*`."""
    type: Expression | None
    """The type of exception to catch."""
    asname: Identifier | None
    """The alias name."""
    parent: Try
    """Parent node."""

    def __init__(self, ty: IntoExpression | None, is_group: bool, parent: Try):
        """Initialize a new exception handler builder.

        Args:
            ty: The type of exception to catch.
            is_group: Whether the exception handler is a group handler, aka `except*`.
            parent: Parent node.
        """
        if ty is not None:
            self.type = ty.into_expression()
        else:
            self.type = None
        self.asname = None
        self.is_group = is_group
        self.parent = parent

    def as_(self, asname: Identifier) -> Self:
        """Set the alias.

        Args:
            asname: The alias name.
        """
        self.asname = asname
        return self

    def block(self, *statements: Statement) -> Try:
        """Set the block of the statement.

        Args:
            statements: The block of the statement.
        """
        handler = ExceptionHandler(
            self.type, self.is_group, self.asname, Block(*statements)
        )
        self.parent.handlers.append(handler)
        return self.parent


class Try(Statement):
    r"""The `try` statement.

    Notes:
        Python views `except` and `except*` as separate statement types,
        but Synt does view them as the same kind and a pair of different variations.

        That means if you write `except` and `except*` statements together in a single `Try`,
        Synt won't complain about it, but the Python parser will reject it.

    Examples:
        ```python
        try_block = try_(
                        PASS
                    ).except_(id_("ValueError")).block(
                        PASS
                    ).except_(id_("Exception")).as_(id_("e")).block(
                        return_()
                    ).except_().block(
                        raise_()
                    ).else_(
                        PASS
                    ).finally_(
                        PASS
                    )
        assert try_block.into_code() == '''try:
            pass
        except ValueError:
            pass
        except Exception as e:
            return
        except:
            raise
        else:
            pass
        finally:
            pass'''
        # try:
        #     pass
        # except ValueError:
        #     pass
        # except Exception as e:
        #     return
        # except:
        #     raise
        # finally:
        #     pass

        try_block = try_(
                        PASS
                    ).except_star(id_("Exception")).block(
                        PASS
                    )
        assert try_block.into_code() == "try:\n    pass\nexcept* Exception:\n    pass"
        # try:
        #     pass
        # except* Exception:
        #     pass
        ```

    References:
        [`Try`](https://docs.python.org/3/library/ast.html#ast.Try)<br/>
        [`TryStar`](https://docs.python.org/3/library/ast.html#ast.TryStar)
    """

    try_block: Block
    """The block to catch exceptions."""
    handlers: list[ExceptionHandler]
    """Exception handlers"""
    orelse: Block | None
    """Fallback handler, aka `else`."""
    final: Block | None
    """Final workaround body, aka `finally`."""

    def __init__(
        self,
        try_block: Block,
        handlers: list[ExceptionHandler],
        orelse: Block | None,
        final: Block | None,
    ):
        """Initialize a new `try` statement.

        **DO NOT USE THIS IN YOUR CODE!**

        Args:
            try_block: The block to catch exceptions.
            handlers: Exception handlers.
            orelse: Fallback handler, aka `else`.
            final: Final workaround body, aka `finally`.
        """
        self.try_block = try_block
        self.handlers = handlers
        self.orelse = orelse
        self.final = final

    def except_(self, ty: IntoExpression | None = None) -> ExceptionHandlerBuilder:
        """Append a new exception handler.

        Args:
            ty: The type of exception to catch.
        """
        return ExceptionHandlerBuilder(ty, False, self)

    def except_star(self, ty: IntoExpression | None) -> ExceptionHandlerBuilder:
        """Append a new group exception handler.

        Args:
            ty: The type of exception to catch.
        """
        return ExceptionHandlerBuilder(ty, True, self)

    def else_(self, *statements: Statement) -> Self:
        """Set the fallback handler.

        Args:
            statements: The statements in the fallback handler.
        """
        self.orelse = Block(*statements)
        return self

    def finally_(self, *statements: Statement) -> Self:
        """Set the final workaround body.

        Args:
            statements: The statements in the final workaround body.
        """
        self.final = Block(*statements)
        return self

    def indented(self, indent_width: int, indent_atom: str) -> str:
        indent = indent_atom * indent_width
        if len(self.handlers) > 0:
            handlers_text = "\n" + "\n".join(
                x.indented(indent_width, indent_atom) for x in self.handlers
            )
        else:
            handlers_text = ""
        if self.orelse is not None:
            orelse_text = f"\n{indent}else:\n{self.orelse.indented(indent_width + 1, indent_atom)}"
        else:
            orelse_text = ""
        if self.final is not None:
            final_text = f"\n{indent}finally:\n{self.final.indented(indent_width + 1, indent_atom)}"
        else:
            final_text = ""
        return (
            f"{indent}try:\n{self.try_block.indented(indent_width + 1, indent_atom)}"
            f"{handlers_text}{orelse_text}{final_text}"
        )


def try_(*statement: Statement) -> Try:
    r"""Initialize a `try` statement.

    Args:
        statement: The statements in the `try` block.
    """
    return Try(Block(*statement), [], None, None)
