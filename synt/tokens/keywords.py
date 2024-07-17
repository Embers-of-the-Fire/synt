from __future__ import annotations


__all__ = [
    "hard_keywords",
    "soft_keywords",
    "is_hard_keyword",
    "is_soft_keyword",
]


import keyword


hard_keywords = keyword.kwlist
"""All Python's hard keywords, in string format.

Alias for std library's [`keyword.kwlist`](https://docs.python.org/3/library/keyword.html#keyword.kwlist)."""


def is_hard_keyword(i: str) -> bool:
    r"""Check if a string is a hard keyword.

    See [`hard_keywords`][synt.tokens.keywords.hard_keywords] for more information.

    Args:
        i: The string to check.
    """
    return keyword.iskeyword(i)


soft_keywords = keyword.softkwlist
"""All Python's soft keywords, in string format.

Alias for std library's [`keyword.softkwlist`](https://docs.python.org/3/library/keyword.html#keyword.softkwlist)."""


def is_soft_keyword(i: str) -> bool:
    r"""Check if a string is a soft keyword.

    See [`soft_keywords`][synt.tokens.keywords.soft_keywords] for more information.

    Args:
        i: The string to check.
    """
    return keyword.issoftkeyword(i)
