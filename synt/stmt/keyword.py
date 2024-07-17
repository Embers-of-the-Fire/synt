from __future__ import annotations


__all__ = [
    "KeywordStatement",
    "PASS",
    "BREAK",
    "CONTINUE",
]


from synt.stmt.stmt import Statement


class KeywordStatement(Statement):
    r"""A statement that only contains a specific keyword.

    Examples:
        ```python
        assert PASS.into_code() == "pass"
        assert BREAK.into_code() == "break"
        assert CONTINUE.into_code() == "continue"
        ```
    """

    keyword: str

    def __init__(self, keyword: str):
        """Initialize a new keyword statement.

        Args:
            keyword: The keyword to be used in the statement.
        """
        self.keyword = keyword

    def indented(self, indent_width: int, indent_atom: str) -> str:
        return f"{indent_width * indent_atom}{self.keyword}"


PASS = KeywordStatement("pass")
BREAK = KeywordStatement("break")
CONTINUE = KeywordStatement("continue")
