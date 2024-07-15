from __future__ import annotations


__all__ = [
    "IntoCode",
]


from abc import ABCMeta
from abc import abstractmethod


class IntoCode(metaclass=ABCMeta):
    @abstractmethod
    def into_code(self) -> str:
        """Converts the object into a string of Python code."""
