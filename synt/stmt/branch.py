from __future__ import annotations


__all__ = [
    "Branch",
    "BranchBuilder",
    "if_",
]

from typing import TYPE_CHECKING
from typing import Self

from synt.stmt.block import Block
from synt.stmt.stmt import Statement


if TYPE_CHECKING:
    from synt.expr.expr import Expression
    from synt.expr.expr import IntoExpression


class Branch(Statement):
    r"""The branch statement, aka `if ... elif ... else`.

    Examples:
        ```python
        if_stmt = if_(id_("foo").expr().eq(litstr("bar"))).block(
                      return_(TRUE)
                  )
        assert if_stmt.into_code() == "if foo == 'bar':\n    return True"
        # if foo == 'bar'
        #     return True

        if_stmt = if_(id_("foo").expr().eq(litstr("bar"))).block(
                      return_(TRUE)
                  ).elif_(id_("foo").expr().is_not(NONE)).block(
                      return_(FALSE)
                  )
        assert if_stmt.into_code() == '''if foo == 'bar':
            return True
        elif foo is not None:
            return False'''
        # if foo == 'bar':
        #     return True
        # elif foo is not None:
        #     return False

        if_stmt = if_(id_("foo").expr().eq(litstr("bar"))).block(
                      return_(TRUE)
                  ).elif_(id_("foo").expr().is_not(NONE)).block(
                      return_(FALSE)
                  ).else_(
                      raise_(id_("ValueError").expr().call(litstr("Unexpected value")))
                  )
        assert if_stmt.into_code() == '''if foo == 'bar':
            return True
        elif foo is not None:
            return False
        else:
            raise ValueError('Unexpected value')'''
        # if foo == 'bar':
        #     return True
        # elif foo is not None:
        #     return False
        # else:
        #     raise ValueError('Unexpected value')
        ```

    References:
        [`If`](https://docs.python.org/3/library/ast.html#ast.ImportFrom).
    """

    tests: list[tuple[Expression, Block]]
    """Branches of the statement, including `if` and `elif`."""
    fallback: Block | None
    """Fallback branch, aka `else`."""

    def __init__(self) -> None:
        """Initialize a new empty branch statement.

        **DO NOT USE THIS IN YOUR CODE!**
        """
        self.tests = []
        self.fallback = None

    def elif_(self, test: IntoExpression) -> BranchBuilder:
        """Create a new branch.

        Args:
            test: Expression to test.
        """
        return BranchBuilder(self, test)

    def else_(self, *statements: Statement) -> Self:
        """Add a fallback branch.

        Args:
            statements: List of statements.
        """
        self.fallback = Block(*statements)
        return self

    def indented(self, indent_width: int, indent_atom: str) -> str:
        if len(self.tests) == 0:
            raise ValueError("Empty branches, at least one test should be added.")
        indent = indent_atom * indent_width
        if_item = self.tests[0]
        if_text = f"{indent}if {if_item[0].into_code()}:\n{if_item[1].indented(indent_width + 1, indent_atom)}"
        if len(self.tests) > 1:
            elif_item = self.tests[1:]
            elif_text = "\n" + "\n".join(
                f"{indent}elif {x[0].into_code()}:\n{x[1].indented(indent_width + 1, indent_atom)}"
                for x in elif_item
            )
        else:
            elif_text = ""
        if self.fallback is not None:
            else_text = f"\n{indent}else:\n{self.fallback.indented(indent_width + 1, indent_atom)}"
        else:
            else_text = ""
        return if_text + elif_text + else_text


class BranchBuilder:
    r"""A single branch builder for the branch statement."""

    parent: Branch
    """Parent node."""
    test: Expression
    """The expression to test."""

    def __init__(self, parent: Branch, test: IntoExpression):
        """Initialize a branch builder.

        Args:
            parent: The parent node.
            test: The expression to test.
        """
        self.parent = parent
        self.test = test.into_expression()

    def block(self, *statements: Statement) -> Branch:
        """Append a block to the branch.

        Args:
            statements: Statements to include in the block.
        """
        block = Block(*statements)
        self.parent.tests.append((self.test, block))
        return self.parent


def if_(test: IntoExpression) -> BranchBuilder:
    r"""Initialize a new branch statement.

    Args:
        test: The expression to test.

    References:
        [`Branch`][synt.stmt.branch.Branch].
    """
    return Branch().elif_(test)
