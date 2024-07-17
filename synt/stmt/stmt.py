from __future__ import annotations


__all__ = [
    "IntoStatement",
    "Statement",
]

from abc import ABCMeta
from abc import abstractmethod

from synt.code import IntoCode


class IntoStatement(metaclass=ABCMeta):
    r"""Any type that can be converted into a statement."""

    @abstractmethod
    def into_statement(self) -> Statement:
        """Convert the object into a statement."""


class Statement(IntoCode, IntoStatement, metaclass=ABCMeta):
    r"""A base class for any Python statement."""

    def into_statement(self) -> Statement:
        """A statement can always be converted into a statement."""
        return self

    @abstractmethod
    def indented(self, indent_width: int, indent_atom: str) -> str:
        """Return the code block with appropriate indentation.

        Args:
            indent_width: number of `indent_atom`s per indentation level.
            indent_atom: string to use for indentation. E.g. `\\t`, whitespace, etc.

        Returns:
            indented code block.
        """

    def into_code(self) -> str:
        """Convert the object into a code string."""
        return self.indented(0, "    ")
