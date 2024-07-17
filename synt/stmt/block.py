from __future__ import annotations


__all__ = [
    "Block",
]

from synt.stmt.stmt import Statement


class Block(Statement):
    r"""A Python code block."""

    body: list[Statement]
    """Code lines in the block."""

    def __init__(self, *args: Statement):
        """Initialize a new code block.

        Args:
            args: code lines.
        """
        self.body = list(args)

    def indented(self, indent_width: int, indent_atom: str) -> str:
        return "\n".join(
            f"{line.indented(indent_width, indent_atom)}" for line in self.body
        )
