from __future__ import annotations


__all__ = [
    "FormatString",
    "FormatConversionType",
    "FormatNode",
    "fstring",
    "fnode",
]


from enum import IntEnum

import synt.code as code
import synt.expr.expr as expr


class FormatString(expr.Expression):
    r"""Format string, aka f-string.

    Examples:
        ```python
        string = fstring("sin(1) = ", fnode(id_("sin").expr().call(litint(1))))
        assert string.into_code() == 'f"sin(1) = {sin(1)}"'
        ```

    References:
        [expr.ExprType.FormatString][synt.expr.expr.ExprType.FormatString].
    """

    nodes: list[FormatNode | str]
    """Formatting nodes."""

    precedence = expr.ExprPrecedence.Atom
    expr_type = expr.ExprType.FormatString

    def __init__(self, *nodes: FormatNode | str):
        """Initialize a new format string expression.

        Args:
            nodes: Formatting nodes.
        """
        self.nodes = list(nodes)

    def into_code(self) -> str:
        string = ""
        for item in self.nodes:
            if isinstance(item, str):
                string += item
            else:
                string += item.into_code()
        return f'f"{string}"'


fstring = FormatString
"""Alias [`FormatString`][synt.expr.fstring.FormatString]."""


class FormatConversionType(IntEnum):
    r"""Format conversion type.

    References:
        [`FormattedValue`](https://docs.python.org/3/library/ast.html#ast.FormattedValue).
    """

    No = -1
    """No formatting."""
    Ascii = 97
    """Ascii representation, aka `!a`."""
    Repr = 114
    """`__repr__` representation, aka `!r`."""
    Str = 115
    """`__str__` representation, aka `!s`."""

    @staticmethod
    def from_str(s: str) -> FormatConversionType:
        """Parse a conversion string.

        | text          | result                       |
        | ------------- | ---------------------------- |
        | `""`, `"!"`   | `FormatConversionType.No`    |
        | `"a"`, `"!a"` | `FormatConversionType.Ascii` |
        | `"r"`, `"!r"` | `FormatConversionType.Repr`  |
        | `"s"`, `"!s"` | `FormatConversionType.Str`   |

        Args:
            s: Conversion string.

        Raises:
            ValueError: If the conversion string is invalid (valid forms are the texts listed above).
        """
        s = s.removeprefix("!")
        match s:
            case "":
                return FormatConversionType.No
            case "a":
                return FormatConversionType.Ascii
            case "r":
                return FormatConversionType.Repr
            case "s":
                return FormatConversionType.Str
            case r:
                raise ValueError(f"Invalid conversion string: {r}")

    def into_str(self) -> str:
        """Converts the conversion type into a string.

        Raises
            ValueError: If the conversion type is not recognized.
        """
        match self:
            case FormatConversionType.No:
                return ""
            case FormatConversionType.Ascii:
                return "!a"
            case FormatConversionType.Repr:
                return "!r"
            case FormatConversionType.Str:
                return "!s"
            case _ as conversion_type:
                raise ValueError(f"Unrecognized conversion type: {conversion_type}")


class FormatNode(code.IntoCode):
    r"""Format node used in [`FormatString`][synt.expr.fstring.FormatString].

    Examples:
        ```python
        node = fnode(id_("sin").expr().call(litint(1)), ".2")
        assert node.into_code() == "{sin(1):.2}"
        ```
    """

    value: expr.Expression
    """expr.Expression to be joint with other nodes."""
    format_spec: str | None
    """The formatting of the value.
    
    Notes:
        Different from Python's behavior, Synt directly use `str` as the type of `format_spec`,
        instead of wrapping it in a `JointStr(Constant(string))`.
    """
    conversion: FormatConversionType
    """The conversion of the expression, e.g. `__str__`, `__repr__`, ..."""

    def __init__(
        self,
        value: expr.IntoExpression,
        format_spec: str | None = None,
        conversion: FormatConversionType | str = FormatConversionType.No,
    ):
        """Initialize a format node.

        Args:
            value: expr.Expression to be joint with other nodes.
            format_spec: The formatting of the value.
            conversion: The conversion of the expression.
        """
        self.value = value.into_expression()
        self.format_spec = format_spec
        self.conversion = (
            FormatConversionType.from_str(conversion)
            if isinstance(conversion, str)
            else conversion
        )

    def into_code(self) -> str:
        fmt_spec = f":{self.format_spec}" if self.format_spec else ""
        return f"{{{self.value.into_code()}{self.conversion.into_str()}{fmt_spec}}}"


fnode = FormatNode
"""Alias [`FormatNode`][synt.expr.fstring.FormatNode]."""
