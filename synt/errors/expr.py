from __future__ import annotations


__all__ = [
    "ExpressionTypeException",
]


from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from synt.expr.expr import ExprType


class ExpressionTypeException(Exception):
    __expected: ExprType
    __actual: ExprType

    def __init__(self, expected: ExprType, actual: ExprType):
        self.__expected = expected
        self.__actual = actual

    @property
    def expected(self) -> ExprType:
        """Expected expression type."""
        return self.__expected

    @property
    def actual(self) -> ExprType:
        """Actually found expression type."""
        return self.__actual
