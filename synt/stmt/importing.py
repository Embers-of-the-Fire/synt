from __future__ import annotations


__all__ = [
    "ImportType",
    "Import",
    "import_",
    "from_",
]


from typing import TYPE_CHECKING
from typing import Literal

from synt.stmt.stmt import Statement


if TYPE_CHECKING:
    from synt.expr.alias import Alias
    from synt.expr.modpath import ModPath
    from synt.tokens.ident import Identifier


type ImportType = Literal["*"] | Identifier | ModPath | Alias
"""Any possible import identifier."""


class Import(Statement):
    r"""The `import` statement.

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


class ImportFrom(Statement):
    r"""The `from ... import` statement.

    Examples:
        ```python
        fi = from_(id_("io")).import_(id_("path"))
        assert fi.into_code() == "from io import path"
        fi = from_(id_("io")).import_(id_("path").as_(id_("p")))
        assert fi.into_code() == "from io import path as p"
        fi = from_(id_("io")).import_(path(id_("path")), id_("os").as_(id_("p")))
        assert fi.into_code() == "from io import path, os as p"
        fi = from_(id_("io")).import_("*")
        assert fi.into_code() == "from io import *"
        ```

    References:
        [`ImportFrom`](https://docs.python.org/3/library/ast.html#ast.ImportFrom).
    """

    module: ModPath
    """The module to import from."""
    names: list[ImportType]
    """Identifiers that are imported."""

    def __init__(self, module: ModPath, *names: ImportType):
        """Initialize a new `from ... import` statement.

        Args:
            module: The module to import from.
            names: Identifiers that are imported.

        Raises:
            ValueError: If no import names are provided.
        """
        if len(names) == 0:
            raise ValueError("At least one import name is required.")

        self.names = list(names)
        self.module = module

    def indented(self, indent_width: int, indent_atom: str) -> str:
        names: list[str] = []
        for name in self.names:
            if isinstance(name, str):
                names.append(name)
            else:
                names.append(name.into_code())

        return f"{indent_atom * indent_width}from {self.module.into_code()} import {', '.join(names)}"


class ImportFromBuilder:
    r"""The builder for [`ImportFrom`][synt.stmt.importing.ImportFrom]."""

    module: ModPath
    """The module to import from."""

    def __init__(self, module: ModPath | Identifier):
        """Initialize a new `from ... import` statement builder.

        Args:
            module: The module to import from.
        """
        from synt.expr.modpath import ModPath
        from synt.tokens.ident import Identifier

        if isinstance(module, Identifier):
            self.module = ModPath(module)
        else:
            self.module = module

    def import_(self, *names: ImportType) -> ImportFrom:
        """Import target objects from the module.

        Args:
            names: Items that are imported.

        Raises:
            ValueError: If no import names are provided.
        """
        return ImportFrom(self.module, *names)


from_ = ImportFromBuilder
"""Alias [`ImportFromBuilder`][synt.stmt.importing.ImportFromBuilder]."""
