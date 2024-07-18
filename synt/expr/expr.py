from __future__ import annotations


__all__ = [
    "IntoExpression",
    "Expression",
    "ExprType",
    "ExprPrecedence",
]

from abc import ABCMeta
from abc import abstractmethod
from enum import IntEnum
from typing import TYPE_CHECKING

import synt.code as code


if TYPE_CHECKING:
    from synt.expr.alias import Alias
    from synt.stmt.stmt import Statement
    from synt.tokens.ident import Identifier


# add in-lib imports to the bottom of the file


class ExprPrecedence(IntEnum):
    r"""Python's expression precedence.

    Sort sequence: smaller = prior

    References:
        [Operator precedence](https://docs.python.org/3/reference/expressions.html#operator-precedence)
    """

    Atom = 0
    """Atom expression: Binding or parenthesized expression, list display, dictionary display, set display,
    and other bound operations.

    Examples:
        ```python
        (expressions...)  # tuple / bind
        [expressions...]  # list
        {key: value...}   # dict
        {expressions...}  # set
        **kwargs          # bound operations (unpacking)
        x for x in y      # bound expressions (generator comprehension)
        yield from tasks  # bound expressions (yield / yield from)
        ```
    """

    Call = 1
    """call.Call-like: subscription, slicing, call, attribute reference.

    Examples:
        ```python
        x[index]       # subscribe
        x[index:index] # slice
        x(args, ...)   # call
        x.attr         # attribute
        ```
    """

    Await = 2
    """Await expression.

    Examples:
        ```python
        await x
        ```
    """

    Exponential = 3
    """Exponential operation: exponentiation.

    **Exception:**
    The power operator `**` binds less tightly than an arithmetic or bitwise unary operator on its right,
    that is, `2 ** -1` is `0.5`.

    Examples:
        ```python
        x ** y
        ```
    """

    Unary = 4
    """Unary operator: positive, negative, bitwise NOT.

    Examples:
        ```python
        +x  # positive
        -x  # negative
        ~x  # bitwise NOT
        ```
    """

    Multiplicative = 5
    """Multiplicative operation: multiplication, matrix multiplication, division, floor division, remainder.

    Notes:
        The `%` operator is also used for string formatting; the same precedence applies.

    Examples:
        ```python
        x * y   # multiplication
        x @ y   # matrix multiplication
        x / y   # division
        x // y  # floor division
        x % y   # remainder
        ```
    """

    Additive = 6
    """Additive operation: addition and subtraction.

    Examples:
        ```python
        x + y  # addition
        x - y  # subtraction
        ```
    """

    Shift = 7
    """Shift operation.

    Examples:
        ```python
        x << y  # left shift
        x >> y  # right shift
        ```
    """

    BitAnd = 8
    """Bitwise AND.

    Examples:
        ```python
        x & y  # bitwise AND
        ```
    """

    BitXor = 9
    """Bitwise XOR.

    Examples:
        ```python
        x ^ y  # bitwise XOR
        ```
    """

    BitOr = 10
    """Bitwise OR.

    Examples:
        ```python
        x | y  # bitwise OR
        ```
    """

    Comparative = 11
    """Boolean operations: comparisons, including membership tests and identity tests.

    Examples:
        ```python
        x in y          # membership tests
        x not in y
        x is y          # identity tests
        x is not y
        x < y           # comparisons
        x <= y
        x > y
        x >= y
        x != y
        x == y
        ```
    """

    BoolNot = 12
    """Boolean NOT.

    Examples:
        ```python
        not x  # boolean NOT
        ```
    """

    BoolAnd = 13
    """Boolean AND.

    Examples:
        ```python
        x and y  # boolean AND
        ```
    """

    BoolOr = 14
    """Boolean OR.

    Examples:
        ```python
        x or y  # boolean OR
        ```
    """

    Conditional = 15
    """Conditional expression: `if` - `else` expression.

    Examples:
        ```python
        x if condition else y
        ```
    """

    Lambda = 16
    """Lambda expression.

    Examples:
        ```python
        lambda x, y: x + y
        ```
    """

    NamedExpr = 17
    """Inline assignment expression.

    Examples:
        ```python
        x := y
        ```
    """


class ExprType(IntEnum):
    r"""Expression type in Synt."""

    Atom = -1
    """Any expression type.
    
    This type is Reserved for internal use."""
    Unknown = -2
    """Unknown expression type.
    
    This type is Reserved for internal use."""

    Identifier = 0
    """[`IdentifierExpr`][synt.tokens.ident.IdentifierExpr]"""
    Wrapped = 1
    """[`Wrapped`][synt.expr.wrapped.Wrapped]."""
    KeyValuePair = 1
    """[`KVPair`][synt.tokens.kv_pair.KVPair]."""
    UnaryOp = 2
    """[`unary_op.UnaryOp`][synt.expr.unary_op.UnaryOp]."""
    BinaryOp = 3
    """[`binary_op.BinaryOp`][synt.expr.binary_op.BinaryOp]."""
    List = 4
    """[`ListDisplay`][synt.expr.list.ListDisplay]."""
    Dict = 5
    """[`DictDisplay`][synt.expr.dict.DictDisplay]."""
    Set = 6
    """[`SetDisplay`][synt.expr.set.SetDisplay]."""
    Tuple = 7
    """[`Tuple`][synt.expr.tuple.Tuple]."""
    Closure = 8
    """[`Closure`][synt.expr.closure.Closure]."""
    Condition = 9
    """[`Condition`][synt.expr.condition.Condition]."""
    NamedExpr = 10
    """[`NamedExpr`][synt.expr.named_expr.NamedExpr]."""
    Comprehension = 11
    """[`Comprehension`][synt.expr.comprehension.Comprehension]."""
    FormatString = 12
    """[`FormatString`][synt.expr.fstring.FormatString]"""
    Subscript = 13
    """[`subscript.Subscript`][synt.expr.subscript.Subscript]"""
    Attribute = 14
    """[`attribute.Attribute`][synt.expr.attribute.Attribute]"""
    Call = 15
    """[`call.Call`][synt.expr.call.Call]"""
    Literal = 16
    """[`tokens.lit.Literal`][synt.tokens.lit.Literal]"""
    Empty = 17
    """[`Empty`][synt.expr.empty.Empty]"""


class IntoExpression(code.IntoCode, metaclass=ABCMeta):
    r"""Abstract class for those that can be converted into an
    [`Expression`][synt.expr.expr.Expression]."""

    @abstractmethod
    def into_expression(self) -> Expression:
        """Convert the object into an expression."""

    def expr(self) -> Expression:
        """Convert the object into an expression.

        This is a convenience method that calls `into_expression()` and returns the result.
        """
        return self.into_expression()

    def into_code(self) -> str:
        """Convert the object into a code string.

        This is a convenience method that calls `into_expression()` and calls `into_code` on the result.
        """
        return self.into_expression().into_code()


class Expression(IntoExpression, code.IntoCode, metaclass=ABCMeta):
    r"""Base class for any expression in Python."""

    @property
    @abstractmethod
    def precedence(self) -> ExprPrecedence:
        """The expression's precedence."""

    @property
    @abstractmethod
    def expr_type(self) -> ExprType:
        """The expression's type."""

    @abstractmethod
    def into_code(self) -> str:
        """Convert the expression into Python code.

        **No Formatting!**
        """

    def into_expression(self) -> Expression:
        """An `Expression` can always be converted into an `Expression`."""
        return self

    def ensure_identifier(self) -> Identifier:
        """Ensure that the expression is an identifier and returns it.

        Raises:
            ValueError: If the expression is not an identifier.
        """
        if type_check.is_ident(self):
            return self.ident
        else:
            raise ValueError("Expression is not an identifier")

    # alias for binary operation

    # bin op > plain method

    def add(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Add operation.

        Examples:
            ```python
            e = litint(1).add(id_("foo")) # alias ... + ...
            assert e.into_code() == "1 + foo"
            ```
        """
        return binary_op.BinaryOp(binary_op.BinaryOpType.Add, self, other)

    def sub(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Subtract operation.

        Examples:
            ```python
            e = litint(1).sub(id_("foo")) # alias ... - ...
            assert e.into_code() == "1 - foo"
            ```
        """
        return binary_op.BinaryOp(binary_op.BinaryOpType.Sub, self, other)

    def mul(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Multiply operation.

        Examples:
            ```python
            e = litint(1).mul(id_("foo")) # alias ... * ...
            assert e.into_code() == "1 * foo"
            ```
        """
        return binary_op.BinaryOp(binary_op.BinaryOpType.Mul, self, other)

    def div(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Divide operation.

        Examples:
            ```python
            e = litint(1).div(id_("foo")) # alias ... / ...
            assert e.into_code() == "1 / foo"
            ```
        """
        return binary_op.BinaryOp(binary_op.BinaryOpType.Div, self, other)

    def truediv(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Alias [`div`][synt.expr.expr.Expression.div]."""
        return self.div(other)

    def floor_div(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Floor divide operation.

        Examples:
            ```python
            e = litint(1).floor_div(id_("foo")) # alias ... // ...
            assert e.into_code() == "1 // foo"
            ```
        """
        return binary_op.BinaryOp(binary_op.BinaryOpType.FloorDiv, self, other)

    def mod(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Modulus operation.

        Examples:
            ```python
            e = litint(1).mod(id_("foo")) # alias ... % ...
            assert e.into_code() == "1 % foo"
            ```
        """
        return binary_op.BinaryOp(binary_op.BinaryOpType.Mod, self, other)

    def pow(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Exponentiation operation.

        Examples:
            ```python
            e = litint(1).pow(id_("foo")) # alias ... ** ...
            assert e.into_code() == "1 ** foo"
            ```
        """
        return binary_op.BinaryOp(binary_op.BinaryOpType.Pow, self, other)

    def at(self, other: IntoExpression) -> binary_op.BinaryOp:
        """At(matrix multiplication) operation.

        Examples:
            ```python
            e = litint(1).at(id_("foo")) # alias ... @ ...
            assert e.into_code() == "1 @ foo"
            ```
        """
        return binary_op.BinaryOp(binary_op.BinaryOpType.At, self, other)

    def matmul(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Alias [`at`][synt.expr.expr.Expression.matmul]."""
        return self.at(other)

    def lshift(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Left shift operation.

        Examples:
            ```python
            e = litint(1).lshift(id_("foo")) # alias ... << ...
            assert e.into_code() == "1 << foo"
            ```
        """
        return binary_op.BinaryOp(binary_op.BinaryOpType.LShift, self, other)

    def rshift(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Right shift operation.

        Examples:
            ```python
            e = litint(1).rshift(id_("foo")) # alias ... >> ...
            assert e.into_code() == "1 >> foo"
            ```
        """
        return binary_op.BinaryOp(binary_op.BinaryOpType.RShift, self, other)

    def lt(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Less than operation.

        Examples:
            ```python
            e = litint(1).lt(id_("foo")) # alias ... < ...
            assert e.into_code() == "1 < foo"
            ```
        """
        return binary_op.BinaryOp(binary_op.BinaryOpType.Less, self, other)

    def le(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Less than or equal to operation.

        Examples:
            ```python
            e = litint(1).le(id_("foo")) # alias ... <= ...
            assert e.into_code() == "1 <= foo"
            ```
        """
        return binary_op.BinaryOp(binary_op.BinaryOpType.LessEqual, self, other)

    def gt(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Greater than operation.

        Examples:
            ```python
            e = litint(1).gt(id_("foo")) # alias ... > ...
            assert e.into_code() == "1 > foo"
            ```
        """
        return binary_op.BinaryOp(binary_op.BinaryOpType.Greater, self, other)

    def ge(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Greater than or equal to operation.

        Examples:
            ```python
            e = litint(1).ge(id_("foo")) # alias ... >= ...
            assert e.into_code() == "1 >= foo"
            ```
        """
        return binary_op.BinaryOp(binary_op.BinaryOpType.GreaterEqual, self, other)

    def eq(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Equal to operation.

        Examples:
            ```python
            e = litint(1).eq(id_("foo")) # alias ... == ...
            assert e.into_code() == "1 == foo"
            ```
        """
        return binary_op.BinaryOp(binary_op.BinaryOpType.Equal, self, other)

    def ne(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Not equal to operation.

        Examples:
            ```python
            e = litint(1).ne(id_("foo")) # alias ... != ...
            assert e.into_code() == "1 != foo"
            ```
        """
        return binary_op.BinaryOp(binary_op.BinaryOpType.NotEqual, self, other)

    def in_(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Membership test operation.

        Examples:
            ```python
            e = litint(1).in_(id_("foo")) # builtin check, no alias
            assert e.into_code() == "1 in foo"
            ```
        """
        return binary_op.BinaryOp(binary_op.BinaryOpType.In, self, other)

    def not_in(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Negative membership test operation.

        Examples:
            ```python
            e = litint(1).not_in(id_("foo")) # builtin check, no alias
            assert e.into_code() == "1 not in foo"
            ```
        """
        return binary_op.BinaryOp(binary_op.BinaryOpType.NotIn, self, other)

    def is_(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Identity test operation.

        Examples:
            ```python
            e = litint(1).is_(id_("foo")) # builtin check, no alias
            assert e.into_code() == "1 is foo"
            ```
        """
        return binary_op.BinaryOp(binary_op.BinaryOpType.Is, self, other)

    def is_not(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Negative identity test operation.

        Examples:
            ```python
            e = litint(1).is_not(id_("foo")) # builtin check, no alias
            assert e.into_code() == "1 is not foo"
            ```
        """
        return binary_op.BinaryOp(binary_op.BinaryOpType.IsNot, self, other)

    def bool_and(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Boolean AND operation.

        Examples:
            ```python
            e = litint(1).bool_and(id_("foo")) # builtin operation, no alias
            assert e.into_code() == "1 and foo"
            ```
        """
        return binary_op.BinaryOp(binary_op.BinaryOpType.BoolAnd, self, other)

    def bool_or(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Boolean OR operation.

        Examples:
            ```python
            e = litint(1).bool_or(id_("foo")) # builtin operation, no alias
            assert e.into_code() == "1 or foo"
            ```
        """
        return binary_op.BinaryOp(binary_op.BinaryOpType.BoolOr, self, other)

    def bit_and(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Bitwise AND operation.

        Examples:
            ```python
            e = litint(1).bit_and(id_("foo")) # alias ... & ...
            assert e.into_code() == "1 & foo"
            ```
        """
        return binary_op.BinaryOp(binary_op.BinaryOpType.BitAnd, self, other)

    def bit_or(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Bitwise OR operation.

        Examples:
            ```python
            e = litint(1).bit_or(id_("foo")) # alias ... | ...
            assert e.into_code() == "1 | foo"
            ```
        """
        return binary_op.BinaryOp(binary_op.BinaryOpType.BitOr, self, other)

    def bit_xor(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Bitwise XOR operation.

        Examples:
            ```python
            e = litint(1).bit_xor(id_("foo")) # alias ... ^ ...
            assert e.into_code() == "1 ^ foo"
            ```
        """
        return binary_op.BinaryOp(binary_op.BinaryOpType.BitXor, self, other)

    # bin op > magic method

    def __lt__(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Alias [`lt`][synt.expr.expr.Expression.lt]."""
        return self.lt(other)

    def __le__(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Alias [`le`][synt.expr.expr.Expression.le]."""
        return self.le(other)

    def __gt__(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Alias [`gt`][synt.expr.expr.Expression.gt]."""
        return self.gt(other)

    def __ge__(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Alias [`ge`][synt.expr.expr.Expression.ge]."""
        return self.ge(other)

    def __eq__(self, other: IntoExpression) -> binary_op.BinaryOp:  # type:ignore[override]
        """Alias [`eq`][synt.expr.expr.Expression.eq]."""
        return self.eq(other)

    def __ne__(self, other: IntoExpression) -> binary_op.BinaryOp:  # type:ignore[override]
        """Alias [`ne`][synt.expr.expr.Expression.ne]."""
        return self.ne(other)

    def __lshift__(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Alias [`lshift`][synt.expr.expr.Expression.lshift]."""
        return self.lshift(other)

    def __rshift__(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Alias [`rshift`][synt.expr.expr.Expression.rshift]."""
        return self.rshift(other)

    def __and__(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Alias [`bit_and`][synt.expr.expr.Expression.bit_and]."""
        return self.bit_and(other)

    def __or__(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Alias [`bit_or`][synt.expr.expr.Expression.bit_or]."""
        return self.bit_or(other)

    def __xor__(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Alias [`bit_xor`][synt.expr.expr.Expression.bit_xor]."""
        return self.bit_xor(other)

    def __add__(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Alias [`add`][synt.expr.expr.Expression.add]."""
        return self.add(other)

    def __sub__(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Alias [`sub`][synt.expr.expr.Expression.sub]."""
        return self.sub(other)

    def __mul__(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Alias [`mul`][synt.expr.expr.Expression.mul]."""
        return self.mul(other)

    def __truediv__(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Alias [`div`][synt.expr.expr.Expression.div]."""
        return self.div(other)

    def __floordiv__(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Alias [`floor_div`][synt.expr.expr.Expression.floor_div]."""
        return self.floor_div(other)

    def __mod__(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Alias [`mod`][synt.expr.expr.Expression.mod]."""
        return self.mod(other)

    def __matmul__(self, other: IntoExpression) -> binary_op.BinaryOp:
        """Alias [`at`][synt.expr.expr.Expression.at]."""
        return self.at(other)

    # alias for unary operation

    # unary op > plain method

    def positive(self) -> unary_op.UnaryOp:
        """Positive operation, alias [`positive` function][synt.expr.unary_op.positive]."""
        return unary_op.UnaryOp(unary_op.UnaryOpType.Positive, self)

    def negative(self) -> unary_op.UnaryOp:
        """Negative operation, alias [`negative` function][synt.expr.unary_op.negative]."""
        return unary_op.UnaryOp(unary_op.UnaryOpType.Neg, self)

    def neg(self) -> unary_op.UnaryOp:
        """Alias [`negative`][synt.expr.expr.Expression.negative]."""
        return unary_op.UnaryOp(unary_op.UnaryOpType.Neg, self)

    def not_(self) -> unary_op.UnaryOp:
        """Boolean NOT operation, alias [`not_` function][synt.expr.unary_op.not_]."""
        return unary_op.UnaryOp(unary_op.UnaryOpType.BoolNot, self)

    def bool_not(self) -> unary_op.UnaryOp:
        """Alias [`not_`][synt.expr.expr.Expression.not_]."""
        return self.not_()

    def invert(self) -> unary_op.UnaryOp:
        """Bitwise NOT operation, alias [`invert` function][synt.expr.unary_op.invert]."""
        return unary_op.UnaryOp(unary_op.UnaryOpType.BitNot, self)

    def bit_not(self) -> unary_op.UnaryOp:
        """Alias [`invert`][synt.expr.expr.Expression.invert]."""
        return self.invert()

    def await_(self) -> unary_op.UnaryOp:
        """Await operation, alias [`await_` function][synt.expr.unary_op.await_]."""
        return unary_op.UnaryOp(unary_op.UnaryOpType.Await, self)

    def awaited(self) -> unary_op.UnaryOp:
        """Alias [`await_`][synt.expr.expr.Expression.await_]"""
        return self.await_()

    def unpack(self) -> unary_op.UnaryOp:
        """Sequence unpacking operation, Alias [`unpack` function][synt.expr.unary_op.unpack]."""
        return unary_op.UnaryOp(unary_op.UnaryOpType.Starred, self)

    def starred(self) -> unary_op.UnaryOp:
        """Alias [`unpack`][synt.expr.expr.Expression.unpack]."""
        return self.unpack()

    def unpack_seq(self) -> unary_op.UnaryOp:
        """Alias [`unpack`][synt.expr.expr.Expression.unpack]."""
        return self.unpack()

    def unpack_kv(self) -> unary_op.UnaryOp:
        """K-V pair unpacking operation, Alias [`unpack_kv` function][synt.expr.unary_op.unpack_kv]."""
        return unary_op.UnaryOp(unary_op.UnaryOpType.DoubleStarred, self)

    def double_starred(self) -> unary_op.UnaryOp:
        """Alias [`unpack_kv`][synt.expr.expr.Expression.unpack_kv]."""
        return self.unpack_kv()

    def unpack_dict(self) -> unary_op.UnaryOp:
        """Alias [`unpack_kv`][synt.expr.expr.Expression.unpack_kv]."""
        return self.unpack_kv()

    def yield_(self) -> unary_op.UnaryOp:
        """Yield operation, alias [`yield_` function][synt.expr.unary_op.yield_]."""
        return unary_op.UnaryOp(unary_op.UnaryOpType.Yield, self)

    def yield_from(self) -> unary_op.UnaryOp:
        """Yield from operation, alias [`yield_from` function][synt.expr.unary_op.yield_from]."""
        return unary_op.UnaryOp(unary_op.UnaryOpType.YieldFrom, self)

    # unary op > magic method

    def __neg__(self) -> unary_op.UnaryOp:
        """Alias [`neg`][synt.expr.expr.Expression.neg]."""
        return self.neg()

    def __not__(self) -> unary_op.UnaryOp:
        """Alias [`not_`][synt.expr.expr.Expression.not_]."""
        return self.not_()

    def __invert__(self) -> unary_op.UnaryOp:
        """Alias [`invert`][synt.expr.expr.Expression.invert]."""
        return self.invert()

    # alias for named value

    def named(self, expr: IntoExpression) -> named_expr.NamedExpr:
        """Assign the expression to `self`.

        Args:
            expr: The expression to assign.

        Raises:
            ValueError: If `self` is not an identifier.

        Examples:
            ```python
            named_expr = id_('a').expr().named(litint(1))
            assert named_expr.into_code() == "a := 1"
            ```
        """
        return named_expr.NamedExpr(self.ensure_identifier(), expr)

    def named_as(self, target: Identifier) -> named_expr.NamedExpr:
        """Assign self to the target.

        Args:
            target: The target identifier.

        Examples:
            ```python
            named_as_expr = (litint(1) + litint(2)).named_as(id_('a')).is_(TRUE)
            assert named_as_expr.into_code() == "(a := 1 + 2) is True"
            ```
        """
        return named_expr.NamedExpr(target, self)

    # alias for attribute

    def attr(self, attr: str) -> attribute.Attribute:
        """attribute.Attribute getting operation.

        Args:
            attr: The attribute name.

        Examples:
            ```python
            attr_expr = id_('a').expr().attr('b').expr().call(litint(1), litint(2))
            assert attr_expr.into_code() == "a.b(1, 2)"
            ```
        """
        return attribute.Attribute(self, attr)

    # alias for call

    def call(
        self,
        *args: IntoExpression | tuple[Identifier, IntoExpression],
        **kwargs: IntoExpression,
    ) -> call.Call:
        """Calling a function or object.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Raises:
            ValueError: If any argument is not [`IntoExpression`][synt.expr.expr.IntoExpression].

        Examples:
            ```python
            call_expr = id_('a').expr().call(litint(1), litint(2)).call(kw=litint(3))
            assert call_expr.into_code() == "a(1, 2)(kw=3)"
            ```
            With dynamic keyword arguments:
            ```python
            call_expr = id_('a').expr().call(kwarg(id_('b'), litint(42)))
            assert call_expr.into_code() == "a(b=42)"
            ```
        """
        from synt.tokens.ident import Identifier

        kwarg: list[call.Keyword] = []
        arg: list[IntoExpression] = []
        for a in args:
            if isinstance(a, tuple):
                kwarg.append(call.Keyword(a[0], a[1]))
                continue
            if type_check.is_into_expr(a):
                arg.append(a)
                continue
            raise ValueError(f"Invalid argument: {a}")

        for k, v in kwargs.items():
            kwarg.append(call.Keyword(Identifier(k), v))

        return call.Call(self, arg, kwarg)

    # alias for comprehension

    def for_(self, *target: Identifier) -> comprehension.ComprehensionNodeBuilder:
        """Initialize a new comprehension.

        Args:
            target: The target of the iteration.

        Examples:
            ```python
            # `comp_expr` here only implements `IntoExpression` and `IntoCode`
            # because it's still a non-finished builder
            comp_expr = list_comp(id_('x').expr()
                .for_(id_('x')).in_(id_('range').expr().call(litint(5)))
                .if_((id_('x').expr() % litint(2)) == litint(0)))
            assert comp_expr.into_code() == "[x for x in range(5) if x % 2 == 0]"
            ```
        """
        return comprehension.ComprehensionBuilder.init(self, list(target), False)

    def async_for(self, *target: Identifier) -> comprehension.ComprehensionNodeBuilder:
        """Initialize a new async comprehension.

        Args:
            target: The iterator expression of the comprehension.

        Examples:
            ```python
            # `comp_expr` here only implements `IntoExpression` and `IntoCode`
            # because it's still a non-finished builder
            comp_expr = list_comp(id_('x').expr()
                .async_for(id_('x')).in_(id_('range').expr().call(litint(5)))
                .if_((id_('x').expr() % litint(2)) == litint(0)))
            assert comp_expr.into_code() == "[x async for x in range(5) if x % 2 == 0]"
            ```
        """
        return comprehension.ComprehensionBuilder.init(self, list(target), True)

    # alias for condition

    def if_(self, cond: IntoExpression) -> condition.ConditionBuilder:
        """Initialize a new condition expression.

        Args:
            cond: The condition expression.

        Examples:
            ```python
            cond_expr = id_('a').expr().if_(id_('b').expr() > litint(0)).else_(litstr('foo'))
            assert cond_expr.into_code() == "a if b > 0 else 'foo'"
            ```
        """
        return condition.ConditionBuilder(cond, self)

    # alias for subscript

    # subscript > plain method

    def subscribe(
        self, *slices: subscript.Slice | IntoExpression
    ) -> subscript.Subscript:
        """Subscribe to the expression.

        Args:
            slices: The slice expressions.

        Examples:
            ```python
            subscript_expr = id_('a').expr().subscribe(id_('b').expr(), slice_(litint(2), litint(3)))
            # also alias: ...[...]
            assert subscript_expr.into_code() == "a[b, 2:3]"
            ```
        """
        return subscript.Subscript(self, list(slices))

    # subscript > magic method

    def __getitem__(
        self,
        items: tuple[subscript.Slice | IntoExpression, ...]
        | subscript.Slice
        | IntoExpression,
    ) -> subscript.Subscript:
        """Alias [`subscribe`][synt.expr.expr.Expression.subscribe]."""
        if isinstance(items, tuple):
            return self.subscribe(*items)
        else:
            return self.subscribe(items)

    # wrap

    def wrap(self) -> expr_wrapped.Wrapped:
        """Wrap `self` in a pair of parentheses, alias [`Wrapped`][synt.expr.wrapped.Wrapped]."""
        return expr_wrapped.Wrapped(self)

    def wrapped(self) -> expr_wrapped.Wrapped:
        """Alias [`wrap`][synt.expr.expr.Expression.wrap]."""
        return self.wrap()

    def par(self) -> expr_wrapped.Wrapped:
        """Alias [`wrap`][synt.expr.expr.Expression.wrap]."""
        return self.wrap()

    def atom(self) -> expr_wrapped.Wrapped:
        """Alias [`wrap`][synt.expr.expr.Expression.wrap]."""
        return self.wrap()

    # statement constructors

    # assignment

    def assign(self, value: IntoExpression) -> stmt_assign.Assignment:
        """Create a new assignment statement, take `self` as the target.

        Args:
            value: The value to assign.
        """
        return stmt_assign.Assignment(self).assign(value)

    def assign_to(self, target: IntoExpression) -> stmt_assign.Assignment:
        """Create a new assignment statement, take `self` as the value.

        Args:
            target: The value to be assigned.
        """
        return stmt_assign.Assignment(target.into_expression()).assign(self)

    def type(self, ty: IntoExpression) -> stmt_assign.Assignment:
        """Create a new typed assignment statement, take `self` as the target.

        Args:
            ty: The type of the target.
        """
        return stmt_assign.Assignment(self).type(ty)

    def ty(self, ty: IntoExpression) -> stmt_assign.Assignment:
        """Alias [`type`][synt.expr.expr.Expression.type]."""
        return self.type(ty)

    def stmt(self) -> Statement:
        """Convert the expression into a statement."""
        from synt.stmt.expression import stmt

        return stmt(self)

    def as_(self, target: Identifier) -> Alias:
        """Convert the expression into an alias.

        Args:
            target: The target identifier.
        """
        from synt.expr.alias import Alias

        return Alias(self, target)


# add import here to avoid circular imports

import synt.expr.attribute as attribute
import synt.expr.binary_op as binary_op
import synt.expr.call as call
import synt.expr.comprehension as comprehension
import synt.expr.condition as condition
import synt.expr.named_expr as named_expr
import synt.expr.subscript as subscript
import synt.expr.type_check as type_check
import synt.expr.unary_op as unary_op
import synt.expr.wrapped as expr_wrapped
import synt.stmt.assign as stmt_assign
