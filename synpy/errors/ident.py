from __future__ import annotations


__all__ = [
    "InvalidIdentifierException",
]


class InvalidIdentifierException(Exception):
    __raw: str

    def __init__(self, raw: str):
        self.__raw = raw
