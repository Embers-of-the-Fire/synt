from __future__ import annotations


__all__ = [
    "FunctionDef",
    "FnArg",
    "arg",
    "vararg",
    "kwarg",
    "FunctionDefBuilder",
    "def_",
    "async_def",
]

from typing import TYPE_CHECKING
from typing import Self

from synt.code import IntoCode
from synt.stmt.block import Block
from synt.stmt.stmt import Statement
from synt.ty.type_param import TypeVar


if TYPE_CHECKING:
    from synt.expr.expr import Expression
    from synt.expr.expr import IntoExpression
    from synt.tokens.ident import Identifier
    from synt.ty.type_param import TypeParam


class FnArg(IntoCode):
    r"""Function argument.

    Examples:
        ```python
        a = arg(id_("foo")).ty(id_("int")).default(litint(1))
        assert a.into_code() == "foo: int = 1"
        ```

    References:
        [`arg`](https://docs.python.org/3/library/ast.html#ast.arg).
    """

    name: Identifier
    """Argument name."""
    annotation: Expression | None
    """Argument annotation."""
    default_expr: Expression | None
    """Argument default expression."""
    is_vararg: bool
    """Whether the argument is a variable argument, or `*args`."""
    is_kwarg: bool
    """Whether the argument is a keyword argument, or `**kwargs`."""

    def __init__(
        self,
        name: Identifier,
        annotation: IntoExpression | None = None,
        default: IntoExpression | None = None,
        is_vararg: bool = False,
        is_kwarg: bool = False,
    ):
        """Initialize a new argument.

        Args:
            name: Argument keyword.
            annotation: Argument annotation.
            default: Default value for the argument.
            is_vararg: Whether the argument is a variable argument, or `*args`.
            is_kwarg: Whether the argument is a keyword argument, or `**kwargs`.
        """
        self.name = name
        self.annotation = (
            annotation.into_expression() if annotation is not None else None
        )
        self.default_expr = default.into_expression() if default is not None else None
        self.is_vararg = is_vararg
        self.is_kwarg = is_kwarg

    def vararg(self) -> Self:
        """Set the argument as a variable argument."""
        self.is_vararg = True
        return self

    def kwarg(self) -> Self:
        """Set the argument as a keyword argument."""
        self.is_kwarg = True
        return self

    def annotate(self, annotation: IntoExpression) -> Self:
        """Add annotation for the argument.

        Args:
            annotation: Argument annotation.
        """
        self.annotation = annotation.into_expression()
        return self

    def ty(self, annotation: IntoExpression) -> Self:
        """Alias [`annotate`][synt.stmt.fn.FnArg.annotate]."""
        return self.annotate(annotation)

    def default(self, default: IntoExpression) -> Self:
        """Set the default value of the argument.

        Args:
            default: Default value for the argument.
        """
        self.default_expr = default.into_expression()
        return self

    def into_code(self) -> str:
        if self.is_vararg:
            name = f"*{self.name.into_code()}"
        elif self.is_kwarg:
            name = f"**{self.name.into_code()}"
        else:
            name = self.name.into_code()
        ret = name
        if self.annotation is not None:
            ret += f": {self.annotation.into_code()}"
        if self.default_expr is not None:
            ret += f" = {self.default_expr.into_code()}"
        return ret


arg = FnArg
"""Alias [`FnArg`][synt.stmt.fn.FnArg]."""


def vararg(i: Identifier) -> FnArg:
    r"""Initialize a variable argument.

    This is equivalent to `FnArg(...).vararg()`.

    Examples:
        ```python
        va = vararg(id_("foo")).ty(id_("int"))
        assert va.into_code() == "*foo: int"
        ```
    """
    return FnArg(i).vararg()


def kwarg(i: Identifier) -> FnArg:
    r"""Initialize a keyword argument.

    This is equivalent to `FnArg(...).kwarg()`.

    Examples:
        ```python
        va = kwarg(id_("foo")).ty(id_("tuple").expr()[id_("str"), id_("int")])
        assert va.into_code() == "**foo: tuple[str, int]"
        ```
    """
    return FnArg(i).kwarg()


class FunctionDef(Statement):
    r"""Function definition.

    Examples:
        With dsl-like aliases:
        ```python
        func = (
            dec(id_("foo"))
            .async_def(id_("bar"))[id_("T")](
                id_("a"),
                arg(id_("b")).ty(id_("int")),
                kw=NONE
            ).returns(id_("float")).block(
                return_(ELLIPSIS)
            )
        )
        assert func.into_code() == "@foo\nasync def bar[T](a, b: int, kw = None) -> float:\n    return ..."
        # @foo
        # async def bar[T](a, b: int, kw = None) -> float:
        #     return ...
        ```

        With raw ast:
        ```python
        func = (
            dec(id_("foo"))
            .async_def(id_("bar"))
            .type_param(id_("T"))
            .arg(
                id_("a"),
                arg(id_("b")).ty(id_("int")),
                kw=NONE
            )
            .returns(id_("float"))
            .block(
                return_(ELLIPSIS)
            )
        )
        assert func.into_code() == "@foo\nasync def bar[T](a, b: int, kw = None) -> float:\n    return ..."
        # @foo
        # async def bar[T](a, b: int, kw = None) -> float:
        #     return ...
        ```

    References:
        [`FunctionDef`](https://docs.python.org/3/library/ast.html#ast.FunctionDef)<br/>
        [`AsyncFunctionDef`](https://docs.python.org/3/library/ast.html#ast.AsyncFunctionDef)
    """

    is_async: bool
    """Whether this function is asynchronous."""
    decorators: list[Expression]
    """Decorators."""
    name: Identifier
    """Function name."""
    type_params: list[TypeParam]
    """Type parameters."""
    args: list[FnArg]
    """Function arguments."""
    returns: Expression | None
    """Return types of the function."""
    body: Block
    """Function body."""

    def __init__(
        self,
        decorators: list[Expression],
        is_async: bool,
        type_params: list[TypeParam],
        args: list[FnArg],
        returns: Expression | None,
        name: Identifier,
        body: Block,
    ):
        """Initialize a function definition.

        **DO NOT USE THIS IN YOUR CODE!**
        """
        self.is_async = is_async
        self.decorators = decorators
        self.type_params = type_params
        self.args = args
        self.returns = returns
        self.name = name
        self.body = body

    def indented(self, indent_width: int, indent_atom: str) -> str:
        indent = indent_width * indent_atom
        decorators = "".join(f"{indent}@{t.into_code()}\n" for t in self.decorators)
        type_param = (
            ""
            if not self.type_params
            else f"[{', '.join(x.into_code() for x in self.type_params)}]"
        )
        args = ", ".join(a.into_code() for a in self.args)
        returns = f" -> {self.returns.into_code()}" if self.returns else ""
        body = self.body.indented(indent_width + 1, indent_atom)
        async_ = "async " if self.is_async else ""
        return f"{decorators}{indent}{async_}def {self.name.into_code()}{type_param}({args}){returns}:\n{body}"


class FunctionDefBuilder:
    r"""Function definition builder.

    References:
        [`FunctionDef`][synt.stmt.fn.FunctionDef]
    """

    is_async: bool
    """Whether this function is asynchronous."""
    decorators: list[Expression]
    """Decorators."""
    name: Identifier | None
    """Function name."""
    type_params: list[TypeParam]
    """Type parameters."""
    args: list[FnArg]
    """Function arguments."""
    returns_ty: Expression | None
    """Return types of the function."""

    def __init__(self) -> None:
        """Initialize an empty builder."""
        self.is_async = False
        self.decorators = []
        self.type_params = []
        self.args = []
        self.returns_ty = None
        self.name = None

    def async_(self) -> Self:
        """Set this function as asynchronous."""
        self.is_async = True
        return self

    def decorator(self, decorator: IntoExpression) -> Self:
        """Append a decorator.

        Args:
            decorator: Decorator to append.
        """
        self.decorators.append(decorator.into_expression())
        return self

    def dec(self, decorator: IntoExpression) -> Self:
        """Alias [synt.stmt.fn.FunctionDefBuilder.decorator]."""
        return self.decorator(decorator)

    def def_(self, name: Identifier) -> Self:
        """Initialize a function.

        Args:
            name: Function name.
        """
        self.name = name
        return self

    def async_def(self, name: Identifier) -> Self:
        """Initialize an async function.

        This is equivalent to `self.async_().def_(name)`.

        Args:
            name: Function name.
        """
        return self.async_().def_(name)

    def type_param(self, *args: TypeParam | Identifier) -> Self:
        """Add generic type parameters.

        Args:
            *args: Type parameters to add.
        """
        from synt.tokens.ident import Identifier

        self.type_params = [
            TypeVar(x) if isinstance(x, Identifier) else x for x in args
        ]
        return self

    def ty(self, *args: TypeParam | Identifier) -> Self:
        """Alias [`type_param`][synt.stmt.fn.FunctionDefBuilder.type_param]."""
        return self.type_param(*args)

    def __getitem__(
        self, items: tuple[TypeParam | Identifier, ...] | TypeParam | Identifier
    ) -> Self:
        """Alias [`type_param`][synt.stmt.fn.FunctionDefBuilder.type_param]."""
        if isinstance(items, tuple):
            return self.type_param(*items)
        else:
            return self.type_param(items)

    def arg(self, *args: FnArg | Identifier, **kwargs: IntoExpression) -> Self:
        """Add arguments for the function.

        Args:
            *args: Arguments to add.
            **kwargs: Keyword arguments to add with their default values.
        """
        from synt.tokens.ident import Identifier

        self.args = []
        for a in args:
            if isinstance(a, Identifier):
                self.args.append(FnArg(a))
            else:
                self.args.append(a)
        for k, v in kwargs.items():
            self.args.append(FnArg(Identifier(k), default=v.into_expression()))
        return self

    def __call__(self, *args: FnArg | Identifier, **kwargs: IntoExpression) -> Self:
        """Alias [`arg`][synt.stmt.fn.FunctionDefBuilder.arg]."""
        return self.arg(*args, **kwargs)

    def returns(self, returns: IntoExpression) -> Self:
        """Set the return type of the function.

        Args:
            returns: Return type of the function.
        """
        self.returns_ty = returns.into_expression()
        return self

    def block(self, *statements: Statement) -> FunctionDef:
        """Set the block of the function, and build it.

        Args:
            *statements: Statements to include in the function body.

        Raises:
            ValueError: If the required fields (`[name,]`) are not set.
        """
        err_fields = []
        if self.name is None:
            err_fields.append("name")

        if err_fields:
            raise ValueError(
                f"Missing required fields: {', '.join(f'`{t}`' for t in err_fields)}"
            )

        return FunctionDef(
            decorators=self.decorators,
            is_async=self.is_async,
            type_params=self.type_params,
            args=self.args,
            returns=self.returns_ty,
            name=self.name,  # type:ignore[arg-type]
            body=Block(*statements),
        )


def def_(name: Identifier) -> FunctionDefBuilder:
    r"""Initialize a function definition.

    Args:
        name: Function name.
    """
    return FunctionDefBuilder().def_(name)


def async_def(name: Identifier) -> FunctionDefBuilder:
    r"""Initialize an async function definition.

    Args:
        name: Function name.
    """
    return FunctionDefBuilder().async_def(name)
