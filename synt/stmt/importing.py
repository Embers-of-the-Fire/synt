from __future__ import annotations


__all__ = [
    "ImportType",
    "Import",
    "import_",
]


from typing import TYPE_CHECKING
from typing import Literal

from synt.expr.alias import Alias
from synt.stmt.stmt import Statement


if TYPE_CHECKING:
    from synt.expr.modpath import ModPath
    from synt.tokens.ident import Identifier


type ImportType = Literal["*"] | Identifier | ModPath | Alias
"""Any possible import identifier."""


class Import(Statement):
    """The `import` statement.

    Examples:
        ```python
        im = import_(id_("path"))
        assert im.into_code() == "import path"
        im = import_(id_("asyncio").as_(id_("aio")))
        assert im.into_code() == "import asyncio as aio"
        im = import_(path(id_("io"), id_("path")))
        assert im.into_code() == "import io.path"
        ```

    References:
        [`Import`](https://docs.python.org/3/library/ast.html#ast.Import).
    """

    names: list[ImportType]
    """Identifiers that are imported."""

    def __init__(self, *names: ImportType):
        """Initialize a new `import` statement.

        Args:
            names: Identifiers that are imported.

        Raises:
            ValueError: If no import names are provided.
        """
        if len(names) == 0:
            raise ValueError("At least one import name is required.")

        self.names = list(names)

    def indented(self, indent_width: int, indent_atom: str) -> str:
        names: list[str] = []
        for name in self.names:
            if isinstance(name, str):
                names.append(name)
            else:
                names.append(name.into_code())

        return f"{indent_atom * indent_width}import {', '.join(names)}"


import_ = Import
"""Alias [`Import`][synt.stmt.importing.Import]."""
