from __future__ import annotations


__all__ = [
    "MatchCase",
    "MatchCaseBuilder",
    "Match",
    "match_",
]


from typing import TYPE_CHECKING
from typing import Self

from synt.stmt.block import Block
from synt.stmt.stmt import Statement


if TYPE_CHECKING:
    from synt.expr.expr import Expression
    from synt.expr.expr import IntoExpression


class MatchCase(Statement):
    r"""A `case` statement.

    References:
        [`matchcase`](https://docs.python.org/3/library/ast.html#ast.match_case).
    """

    pattern: Expression
    """Match pattern."""
    guard: Expression | None
    """Pattern guard."""
    body: Block
    """Case body."""

    def __init__(
        self, pattern: IntoExpression, guard: IntoExpression | None, body: Block
    ):
        """Initialize a `case` statement.

        **DO NOT USE THIS IN YOUR CODE!**

        Args:
            pattern: Match pattern.
            guard: Pattern guard.
            body: Case body.
        """
        self.pattern = pattern.into_expression()
        self.guard = guard.into_expression() if guard is not None else None
        self.body = body

    def indented(self, indent_width: int, indent_atom: str) -> str:
        guard = f" if {self.guard.into_code()}" if self.guard is not None else ""
        return (
            f"{indent_atom * indent_width}case {self.pattern.into_code()}{guard}:\n"
            f"{self.body.indented(indent_width + 1, indent_atom)}"
        )


class MatchCaseBuilder:
    """Builder for [`MatchCase`][synt.stmt.match_case.MatchCase]."""

    pattern: Expression
    """Match pattern."""
    guard: Expression | None
    """Pattern guard."""
    parent: Match
    """Parent node."""

    def __init__(self, pattern: IntoExpression, parent: Match):
        """Initialize a new builder.

        Args:
            pattern: Match pattern.
        """
        self.pattern = pattern.into_expression()
        self.guard = None
        self.parent = parent

    def if_(self, guard: IntoExpression) -> Self:
        """Set the guard.

        Args:
            guard: Pattern guard.
        """
        self.guard = guard.into_expression()
        return self

    def block(self, *statements: Statement) -> Match:
        """Set the body statements.

        Args:
            *statements: Body statements.
        """
        case = MatchCase(self.pattern, self.guard, Block(*statements))
        self.parent.cases.append(case)
        return self.parent


class Match(Statement):
    r"""The `match` statement.

    Examples:
        ```python
        match_stmt = (
            match_(id_("a"))
            .case_(id_("b")).block(PASS)
            .case_(id_("Point").expr().call(id_("x"), id_("y"))).block(PASS)
            .case_(list_(id_("x")).as_(id_("y"))).block(PASS)
            .case_(UNDERSCORE).block(PASS)
        )
        assert match_stmt.into_code() == '''match a:
            case b:
                pass
            case Point(x, y):
                pass
            case [x] as y:
                pass
            case _:
                pass'''
        # match a:
        #     case b:
        #         pass
        #     case Point(x, y):
        #         pass
        #     case [x] as y:
        #         pass
        #     case _:
        #         pass
        ```

    Notes:
        Python views `[x]`, `(x)`, etc, as different `case` nodes,
        but Synt views them as the same.
        Synt accepts any form of expression as case patterns,
        and you must check yourself.

    References:
        [`Match`](https://docs.python.org/3/library/ast.html#ast.Match).
    """

    subject: Expression
    """Match subject."""
    cases: list[MatchCase]
    """Match cases."""

    def __init__(self, subject: IntoExpression):
        """Initialize a new `match` statement.

        Args:
            subject: Match subject.
        """
        self.subject = subject.into_expression()
        self.cases = []

    def case_(self, pattern: IntoExpression) -> MatchCaseBuilder:
        """Append a new case.

        Args:
            pattern: Match pattern.
        """
        return MatchCaseBuilder(pattern, self)

    def indented(self, indent_width: int, indent_atom: str) -> str:
        if len(self.cases) == 0:
            cases = f"{indent_atom * (indent_width + 1)}pass"
        else:
            cases = "\n".join(
                x.indented(indent_width + 1, indent_atom) for x in self.cases
            )
        return (
            f"{indent_atom * indent_width}match {self.subject.into_code()}:\n"
            f"{cases}"
        )


match_ = Match
"""Alias [`Match`][synt.stmt.match_case.Match]."""
