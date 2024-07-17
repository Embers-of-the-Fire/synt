from __future__ import annotations


__all__ = [
    "Comprehension",
    "ComprehensionNode",
    "GeneratorComprehension",
    "ComprehensionBuilder",
    "ComprehensionNodeBuilder",
]

from typing import TYPE_CHECKING
from typing import Self

import synt.code as code
import synt.expr.expr as expr
import synt.tokens.ident as ident


if TYPE_CHECKING:
    from synt.tokens.ident import Identifier


class Comprehension(expr.IntoExpression, code.IntoCode):
    r"""A Comprehension expression.

    **Attribute explanation:**
    ```python
    [
        a           # elt, aka "extract, load, transform"
                    # 👇 generator node #1
        for b       # target
        in c        # iter
        if          # `if`s
            d == e  # an `if`

        for f in g  # 👈 generator node #2
    ]
    ```

    **Note:**
    `Comprehension` is not a subclass of [`expr.Expression`][synt.expr.expr.Expression].
    However, it implements [`expr.IntoExpression`][synt.expr.expr.IntoExpression],
    and will be internally converted into [`GeneratorComprehension`][synt.expr.comprehension.GeneratorComprehension].

    References:
        [`comprehension`](https://docs.python.org/3/reference/
        expressions.html#grammar-tokens-python-grammar-comprehension).
    """

    elt: expr.Expression
    """The expression to evaluate when iterating over the
    [`iterator`][synt.expr.comprehension.ComprehensionNode.iterator].
    
    **Note:** aka "extract, load, transform"."""
    comprehensions: list[ComprehensionNode]
    """Generator nodes."""

    precedence = expr.ExprPrecedence.Atom

    def __init__(
        self,
        elt: expr.IntoExpression,
        comprehensions: list[ComprehensionNode],
    ):
        """Initialize a new comprehension expression.

        Args:
            elt: The expression to evaluate.
            comprehensions: The generator nodes.
        """
        self.elt = elt.into_expression()
        self.comprehensions = comprehensions

    def into_expression(self) -> GeneratorComprehension:
        return GeneratorComprehension(self)

    def into_code(self) -> str:
        comp_text = " ".join(x.into_code() for x in self.comprehensions)
        return f"{self.elt.into_code()} {comp_text}"


class ComprehensionNode(code.IntoCode):
    target: list[Identifier]
    """Comprehension `for`-loop target identifiers."""
    iterator: expr.Expression
    """The iterator to iterate over."""
    ifs: list[expr.Expression]
    """A list of `if` expressions to filter comprehension result."""
    is_async: bool
    """Whether the iterator is asynchronous."""

    precedence = expr.ExprPrecedence.Atom

    def __init__(
        self,
        target: list[Identifier],
        iterator: expr.IntoExpression,
        ifs: list[expr.IntoExpression],
        is_async: bool,
    ):
        """Initialize a new comprehension expression.

        Args:
            target: The target identifiers.
            iterator: The iterator to iterate over.
            ifs: A list of `if` expressions.
            is_async: Whether the iterator is asynchronous.
        """
        self.target = target
        self.iterator = iterator.into_expression()
        self.ifs = [x.into_expression() for x in ifs]
        self.is_async = is_async

    def into_code(self) -> str:
        target_text = ", ".join(t.into_code() for t in self.target)
        if self.ifs:
            if_text = " " + " ".join(f"if {i.into_code()}" for i in self.ifs)
        else:
            if_text = ""
        for_text = "async for" if self.is_async else "for"
        return f"{for_text} {target_text} in {self.iterator.into_code()}{if_text}"


class GeneratorComprehension(expr.Expression):
    r"""A generator comprehension expression.

    **Note:**
    `GeneratorComprehension` is a subclass of [`expr.Expression`][synt.expr.expr.Expression],
    working as a wrapper for [`Comprehension`][synt.expr.comprehension.Comprehension].
    """

    comprehension: Comprehension
    """The inner comprehension expression."""

    precedence = expr.ExprPrecedence.Atom
    expr_type = expr.ExprType.Comprehension

    def __init__(self, comprehension: Comprehension):
        """Initialize a generator comprehension expression.

        Args:
            comprehension: The inner comprehension expression to wrap.
        """
        self.comprehension = comprehension

    def into_code(self) -> str:
        return f"({self.comprehension.into_code()})"


class ComprehensionBuilder(expr.IntoExpression):
    r"""Builder for [`Comprehension`][synt.expr.comprehension.Comprehension]."""

    __elt: expr.Expression
    __comprehensions: list[ComprehensionNode]
    __curr_node: ComprehensionNodeBuilder | None

    def __init__(
        self,
        elt: expr.IntoExpression,
        target: list[ident.Identifier],
        is_async: bool = False,
    ):
        """Initialize a generator comprehension expression.

        Args:
            elt: The expression to evaluate.
            target: The target of the iteration.
            is_async: Whether the comprehension is asynchronous.
        """
        self.__elt = elt.into_expression()
        self.__comprehensions = []
        self.__curr_node = ComprehensionNodeBuilder(self, is_async).target(*target)

    @staticmethod
    def init(
        elt: expr.IntoExpression, target: list[ident.Identifier], is_async: bool = False
    ) -> ComprehensionNodeBuilder:
        """Initialize a generator comprehension expression and return the first node builder.

        Args:
            elt: The expression to evaluate.
            target: The target of the iteration.
            is_async: Whether the comprehension is asynchronous.
        """
        return ComprehensionBuilder(elt, target, is_async).curr_node()  # type:ignore[return-value]

    def curr_node(self) -> ComprehensionNodeBuilder | None:
        """Returns the current node builder."""
        return self.__curr_node

    def __finish_node_builder(self) -> None:
        if self.__curr_node:
            res = self.__curr_node.build()
            self.__comprehensions.append(res)
            self.__curr_node = None

    def for_(self, iterator: expr.IntoExpression) -> ComprehensionNodeBuilder:
        """Create a new comprehension node.

        This will finish the previous [`ComprehensionNodeBuilder`][synt.expr.comprehension.ComprehensionNodeBuilder]
        and start a new one.
        """
        self.__finish_node_builder()
        return ComprehensionNodeBuilder(self).iterator(iterator)

    def async_for(self, iterator: expr.IntoExpression) -> ComprehensionNodeBuilder:
        """Create a new async comprehension node.

        This will finish the previous [`ComprehensionNodeBuilder`][synt.expr.comprehension.ComprehensionNodeBuilder]
        and start a new one.
        """
        self.__finish_node_builder()
        return ComprehensionNodeBuilder(self, True).iterator(iterator)

    def build(self) -> Comprehension:
        """Build the comprehension expression.

        Raises:
            ValueError: If any required fields are missing.
        """
        self.__finish_node_builder()
        return Comprehension(self.__elt, self.__comprehensions)

    def into_expression(self) -> GeneratorComprehension:
        return self.build().into_expression()


class ComprehensionNodeBuilder(expr.IntoExpression):
    r"""Builder for [`ComprehensionNode`][synt.expr.comprehension.ComprehensionNode]."""

    __target: list[Identifier] | None
    __iterator: expr.Expression | None
    __ifs: list[expr.IntoExpression]
    __is_async: bool = False

    def __init__(self, root: ComprehensionBuilder, is_async: bool = False):
        """Initialize an empty builder.

        Args:
            root: The root builder.
            is_async: Whether the comprehension is asynchronous.
        """
        self.root = root
        self.__is_async = is_async
        self.__target = None
        self.__iterator = None
        self.__ifs = []

    def target(self, *target: Identifier) -> Self:
        """Set the target of the comprehension generator.

        Args:
            target: The target identifiers.
        """
        self.__target = list(target)
        return self

    def in_(self, iterator: expr.IntoExpression) -> Self:
        """Alias [`iterator`][synt.expr.comprehension.ComprehensionNodeBuilder.iterator]."""
        return self.iterator(iterator)

    def iterator(self, iterator: expr.IntoExpression) -> Self:
        """Set the iterator of the comprehension generator.

        Args:
            iterator: The iterator to iterate over.
        """
        self.__iterator = iterator.into_expression()
        return self

    def if_(self, if_expr: expr.IntoExpression) -> Self:
        """Add an `if` expression to filter comprehension result.

        Args:
            if_expr: The `if` expression.
        """
        self.__ifs.append(if_expr.into_expression())
        return self

    def async_(self) -> Self:
        """Set the comprehension as asynchronous."""
        self.__is_async = True
        return self

    def sync(self) -> Self:
        """Set the comprehension as synchronous."""
        self.__is_async = False
        return self

    def build(self) -> ComprehensionNode:
        """Build the comprehension node.

        Raises:
            ValueError: If any required fields are missing.
        """
        err_fields = []
        if self.__iterator is None:
            err_fields.append("iterator")
        if not self.__target:
            err_fields.append("target")

        if err_fields:
            raise ValueError(
                f"Missing required fields: {', '.join(f'`{t}`' for t in err_fields)}"
            )
        return ComprehensionNode(
            self.__target,  # type:ignore[arg-type]
            self.__iterator,  # type:ignore[arg-type]
            self.__ifs,
            self.__is_async,
        )

    def for_(self, iterator: expr.IntoExpression) -> ComprehensionNodeBuilder:
        """Create a new comprehension node.

        This will call root's [`for_`][synt.expr.comprehension.ComprehensionBuilder.for_].
        """
        return self.root.for_(iterator)

    def async_for(self, iterator: expr.IntoExpression) -> ComprehensionNodeBuilder:
        """Create a new async comprehension node.

        This will call root's [`async_for`][synt.expr.comprehension.ComprehensionBuilder.async_for].
        """
        return self.root.async_for(iterator)

    def build_comp(self) -> Comprehension:
        """Build the comprehension expression.

        Raises:
            ValueError: If any required fields are missing.
        """
        return self.root.build()

    def into_expression(self) -> GeneratorComprehension:
        return self.build_comp().into_expression()
