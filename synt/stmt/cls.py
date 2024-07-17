from __future__ import annotations


__all__ = [
    "ClassDef",
    "ClassDefBuilder",
    "class_",
]


from typing import TYPE_CHECKING
from typing import Self

from synt.stmt.block import Block
from synt.stmt.stmt import Statement
from synt.ty.type_param import TypeVar


if TYPE_CHECKING:
    from synt.expr.expr import Expression
    from synt.expr.expr import IntoExpression
    from synt.tokens.ident import Identifier
    from synt.ty.type_param import TypeParam


class ClassDef(Statement):
    r"""Class definition.

        Examples:
            ```python
            cls = (
                dec(id_("foo"))
                .class_(id_("Bar"))[id_("T")](metaclass=id_("ABCMeta"))
                .block(
                    dec(id_("abstractmethod"))
                    .def_(id_("baz"))(id_("self"), arg(id_("a"), id_("T"))).returns(id_("str"))
                    .block(
                        return_(fstring("Bar(", fnode(id_("a")), ").baz"))
                    )
                )
            )
            assert cls.into_code() == '''@foo
    class Bar[T](metaclass=ABCMeta):
        @abstractmethod
        def baz(self, a: T) -> str:
            return f"Bar({a}).baz"'''

            # @foo
            # class Bar[T](metaclass=ABCMeta):
            #     @abstractmethod
            #     def baz(self, a: T) -> str:
            #         return f"Bar({a}).baz"
            ```

        References:
            [`ClassDef`](https://docs.python.org/3/library/ast.html#ast.ClassDef).
    """

    decorators: list[Expression]
    """Decorators."""
    name: Identifier
    """Class name."""
    type_params: list[TypeParam]
    """Type parameters."""
    cargs: list[Expression]
    """Class arguments.
    
    E.g., base classes.
    """
    ckwargs: list[tuple[Identifier, Expression]]
    """Class keyword arguments.
    
    E.g., meta classes.
    """
    body: Block
    """Function body."""

    def __init__(
        self,
        decorators: list[Expression],
        type_params: list[TypeParam],
        name: Identifier,
        cargs: list[Expression],
        ckwargs: list[tuple[Identifier, Expression]],
        body: Block,
    ):
        """Initialize a function definition.

        **DO NOT USE THIS IN YOUR CODE!**
        """
        self.decorators = decorators
        self.type_params = type_params
        self.cargs = cargs
        self.ckwargs = ckwargs
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
        args_l: list[str] = []
        args_l.extend(x.into_code() for x in self.cargs)
        args_l.extend(f"{x[0].into_code()}={x[1].into_code()}" for x in self.ckwargs)
        args = f"({', '.join(args_l)})" if args_l else ""
        body = self.body.indented(indent_width + 1, indent_atom)
        return f"{decorators}{indent}class {self.name.into_code()}{type_param}{args}:\n{body}"


class ClassDefBuilder:
    r"""Class definition builder.

    References:
        [`ClassDef`][synt.stmt.cls.ClassDef].
    """

    decorators: list[Expression]
    """Decorators."""
    name: Identifier | None
    """Class name."""
    type_params: list[TypeParam]
    """Type parameters."""
    cargs: list[Expression]
    """Class arguments.
    
    E.g., base classes.
    """
    ckwargs: list[tuple[Identifier, Expression]]
    """Class keyword arguments.
    
    E.g., meta classes.
    """

    def __init__(self) -> None:
        """Initialize an empty builder."""
        self.decorators = []
        self.name = None
        self.type_params = []
        self.cargs = []
        self.ckwargs = []

    def decorator(self, decorator: IntoExpression) -> Self:
        """Append a decorator.

        Args:
            decorator: Decorator to append.
        """
        self.decorators.append(decorator.into_expression())
        return self

    def dec(self, decorator: IntoExpression) -> Self:
        """Alias [`decorator`][synt.stmt.cls.ClassDefBuilder.decorator]."""
        return self.decorator(decorator)

    def class_(self, name: Identifier) -> Self:
        """Initialize a class.

        Args:
            name: Class name.
        """
        self.name = name
        return self

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
        """Alias [`type_param`][synt.stmt.cls.ClassDefBuilder.type_param]."""
        return self.type_param(*args)

    def __getitem__(
        self, items: tuple[TypeParam | Identifier, ...] | TypeParam | Identifier
    ) -> Self:
        """Alias [`type_param`][synt.stmt.cls.ClassDefBuilder.type_param]."""
        if isinstance(items, tuple):
            return self.type_param(*items)
        else:
            return self.type_param(items)

    def arg(
        self,
        *args: IntoExpression | tuple[Identifier, IntoExpression],
        **kwargs: IntoExpression,
    ) -> Self:
        """Add arguments for the class.

        Args:
            *args: Arguments to add.
            **kwargs: Keyword arguments to add with their default values.
        """
        from synt.tokens.ident import Identifier

        self.cargs = []
        self.ckwargs = []
        for a in args:
            if isinstance(a, tuple):
                self.ckwargs.append((a[0], a[1].into_expression()))
            else:
                self.cargs.append(a.into_expression())
        for k, v in kwargs.items():
            self.ckwargs.append((Identifier(k), v.into_expression()))
        return self

    def __call__(
        self,
        *args: IntoExpression | tuple[Identifier, IntoExpression],
        **kwargs: IntoExpression,
    ) -> Self:
        """Alias [`arg`][synt.stmt.cls.ClassDefBuilder.arg]."""
        return self.arg(*args, **kwargs)

    def block(self, *statements: Statement) -> ClassDef:
        """Set the block of the class, and build it.

        Args:
            *statements: Statements to include in the class body.

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

        return ClassDef(
            decorators=self.decorators,
            type_params=self.type_params,
            cargs=self.cargs,
            ckwargs=self.ckwargs,
            name=self.name,  # type:ignore[arg-type]
            body=Block(*statements),
        )


def class_(name: Identifier) -> ClassDefBuilder:
    r"""Initialize a class without decorators.

    Args:
        name: Class name.
    """
    return ClassDefBuilder().class_(name)
