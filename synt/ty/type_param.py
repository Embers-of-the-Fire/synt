from __future__ import annotations


__all__ = [
    "TypeVar",
    "TypeVarTuple",
    "TypeParamSpec",
    "tvar",
    "ttup",
    "tspec",
    "TypeParam",
]

from typing import TYPE_CHECKING

from synt.code import IntoCode


if TYPE_CHECKING:
    from synt.expr.expr import Expression
    from synt.expr.expr import IntoExpression
    from synt.tokens.ident import Identifier


class TypeVar(IntoCode):
    r"""`TypeVar` in type parameters.

    Examples:
        ```python
        ty_var = tvar(id_("T"), id_("int"))
        assert ty_var.into_code() == "T: int"
        ```

    References:
        [Type parameters](https://docs.python.org/3/library/ast.html#ast-type-params).
    """

    name: Identifier
    """The name of the type variable."""
    bound: Expression | None
    """The bound of the type variable."""

    def __init__(self, name: Identifier, bound: IntoExpression | None = None):
        """Initialize a type variable.

        Args:
            name: The name of the type variable.
            bound: The bound of the type variable.
        """
        self.name = name
        if bound is not None:
            self.bound = bound.into_expression()
        else:
            self.bound = None

    def into_code(self) -> str:
        bound = f": {self.bound.into_code()}" if self.bound is not None else ""
        return f"{self.name.into_code()}{bound}"


tvar = TypeVar
"""Alias [`TypeVar`][synt.ty.type_param.TypeVar]."""


class TypeVarTuple(IntoCode):
    r"""Type variable tuple.

    Examples:
        ```python
        ty_var = ttup(id_("T"))
        assert ty_var.into_code() == "*T"
        ```

    References:
        [Type variable tuple](https://docs.python.org/3/library/ast.html#ast.TypeVarTuple).
    """

    name: Identifier
    """The name of the type variable tuple."""

    def __init__(self, name: Identifier):
        """Initialize a type variable tuple.

        Args:
            name: The name of the type variable tuple.
        """
        self.name = name

    def into_code(self) -> str:
        return f"*{self.name.into_code()}"


ttup = TypeVarTuple
"""Alias [`TypeVarTuple`][synt.ty.type_param.TypeVarTuple]."""


class TypeParamSpec(IntoCode):
    r"""Type parameter spec.

    Examples:
        ```python
        ty_var = tspec(id_("P"))
        assert ty_var.into_code() == "**P"
        ```

    References:
        [Type param spec](https://docs.python.org/3/library/ast.html#ast.ParamSpec).
    """

    name: Identifier
    """The name of the type variable tuple."""

    def __init__(self, name: Identifier):
        """Initialize a type parameter spec.

        Args:
            name: The name of the type parameter spec.
        """
        self.name = name

    def into_code(self) -> str:
        return f"**{self.name.into_code()}"


tspec = TypeParamSpec
"""Alias [`TypeParamSpec`][synt.ty.type_param.TypeParamSpec]."""


type TypeParam = TypeVar | TypeVarTuple | TypeParamSpec
"""Any type parameter."""
