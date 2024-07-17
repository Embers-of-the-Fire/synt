from __future__ import annotations

import pytest
import synt

from synt.expr.binary_op import BinaryOpType
from synt.expr.expr import ExprPrecedence
from synt.expr.unary_op import UnaryOpType
from synt.prelude import *


def test_expr_type():
    assert BinaryOpType.Add.to_precedence() == ExprPrecedence.Additive

    for i in range(23):
        op = BinaryOpType(i)
        assert op.to_precedence() is not None
        assert op.into_code() is not None
    for i in range(8):
        op = UnaryOpType(i)
        assert op.to_precedence() is not None
        assert op.into_code() is not None

    with pytest.raises(ValueError) as err:
        op = BinaryOpType(100)
        op.to_precedence()
    assert "100" in str(err.value)

    with pytest.raises(ValueError) as err:
        op = BinaryOpType(100)
        op.into_code()
    assert "100" in str(err.value)

    with pytest.raises(ValueError) as err:
        op = UnaryOpType(100)
        op.to_precedence()
    assert "100" in str(err.value)

    with pytest.raises(ValueError) as err:
        op = UnaryOpType(100)
        op.into_code()
    assert "100" in str(err.value)


def test_expr_binop():
    e = litint(1).add(id_("foo"))
    assert e.into_code() == "1 + foo"
    e = litint(1).sub(id_("foo"))
    assert e.into_code() == "1 - foo"
    e = litint(1).mul(id_("foo"))
    assert e.into_code() == "1 * foo"
    e = litint(1).div(id_("foo"))
    assert e.into_code() == "1 / foo"
    e = litint(1).floor_div(id_("foo"))
    assert e.into_code() == "1 // foo"
    e = litint(1).mod(id_("foo"))
    assert e.into_code() == "1 % foo"
    e = litint(1).pow(id_("foo"))
    assert e.into_code() == "1 ** foo"
    e = litint(1).at(id_("foo"))
    assert e.into_code() == "1 @ foo"
    e = litint(1).lshift(id_("foo"))
    assert e.into_code() == "1 << foo"
    e = litint(1).rshift(id_("foo"))
    assert e.into_code() == "1 >> foo"
    e = litint(1).lt(id_("foo"))
    assert e.into_code() == "1 < foo"
    e = litint(1).le(id_("foo"))
    assert e.into_code() == "1 <= foo"
    e = litint(1).gt(id_("foo"))
    assert e.into_code() == "1 > foo"
    e = litint(1).ge(id_("foo"))
    assert e.into_code() == "1 >= foo"
    e = litint(1).eq(id_("foo"))
    assert e.into_code() == "1 == foo"
    e = litint(1).ne(id_("foo"))
    assert e.into_code() == "1 != foo"
    e = litint(1).in_(id_("foo"))  # builtin check, no alias
    assert e.into_code() == "1 in foo"
    e = litint(1).not_in(id_("foo"))  # builtin check, no alias
    assert e.into_code() == "1 not in foo"
    e = litint(1).is_(id_("foo"))  # builtin check, no alias
    assert e.into_code() == "1 is foo"
    e = litint(1).is_not(id_("foo"))  # builtin check, no alias
    assert e.into_code() == "1 is not foo"
    e = litint(1).bool_and(id_("foo"))  # builtin operation, no alias
    assert e.into_code() == "1 and foo"
    e = litint(1).bool_or(id_("foo"))  # builtin operation, no alias
    assert e.into_code() == "1 or foo"
    e = litint(1).bit_and(id_("foo"))  # alias ... & ...
    assert e.into_code() == "1 & foo"
    e = litint(1).bit_or(id_("foo"))  # alias ... | ...
    assert e.into_code() == "1 | foo"
    e = litint(1).bit_xor(id_("foo"))  # alias ... ^ ...
    assert e.into_code() == "1 ^ foo"


def test_expr_unary_op():
    await_expr = await_(litint(10))
    assert await_expr.into_code() == "await 10"
    positive_expr = positive(litint(10))
    assert positive_expr.into_code() == "+ 10"
    not_expr = not_(id_("foo"))
    assert not_expr.into_code() == "not foo"
    not_expr = invert(id_("foo"))
    assert not_expr.into_code() == "~ foo"
    unpacked_expr = unpack(list_(litint(1), litint(2), litint(3)))
    assert unpacked_expr.into_code() == "* [1, 2, 3]"
    unpacked_expr = unpack_kv(dict_(kv(litint(1), litstr("a"))))
    assert unpacked_expr.into_code() == "** {1: 'a'}"
    yield_expr = yield_(litint(10))
    assert yield_expr.into_code() == "yield 10"
    yield_expr = yield_from(list_(litint(10), litint(42)))
    assert yield_expr.into_code() == "yield from [10, 42]"


def test_expr_named():
    named_expr = id_("a").expr().named(litint(1))
    assert named_expr.into_code() == "a := 1"
    named_as_expr = (litint(1) + litint(2)).named_as(id_("a")).is_(TRUE)
    assert named_as_expr.into_code() == "(a := 1 + 2) is True"


def test_expr_attr():
    attr_expr = id_("a").expr().attr("b").expr().call(litint(1), litint(2))
    assert attr_expr.into_code() == "a.b(1, 2)"


def test_expr_call():
    call_expr = id_("a").expr().call(litint(1), litint(2)).call(kw=litint(3))
    assert call_expr.into_code() == "a(1, 2)(kw=3)"
    call_expr = id_("a").expr().call((id_("b"), litint(42)))
    assert call_expr.into_code() == "a(b=42)"


def test_expr_closure():
    closure = (
        lambda_(id_("x"), id_("y"))  # initial a closure builder
        .join(id_("z"))  # append new argument
        .return_(
            id_("x").expr() + id_("y") + id_("z")
        )  # set the expression to be returned
    )
    assert closure.into_code() == "lambda x, y, z: x + y + z"


def test_expr_comp():
    comp_expr = list_comp(
        id_("x")
        .expr()
        .for_(id_("x"))
        .in_(id_("range").expr().call(litint(5)))
        .if_((id_("x").expr() % litint(2)) == litint(0))
    )
    assert comp_expr.into_code() == "[x for x in range(5) if x % 2 == 0]"
    comp_expr = list_comp(
        id_("x")
        .expr()
        .async_for(id_("x"))
        .in_(id_("range").expr().call(litint(5)))
        .if_((id_("x").expr() % litint(2)) == litint(0))
    )
    assert comp_expr.into_code() == "[x async for x in range(5) if x % 2 == 0]"


def test_expr_cond():
    cond_expr = id_("a").expr().if_(id_("b").expr() > litint(0)).else_(litstr("foo"))
    assert cond_expr.into_code() == "a if b > 0 else 'foo'"


def test_expr_subscript():
    subscript_expr = (
        id_("a").expr().subscribe(id_("b").expr(), slice_(litint(2), litint(3)))
    )
    assert subscript_expr.into_code() == "a[b, 2:3]"
    subscript_expr = id_("a").expr()[id_("b").expr(), slice_(litint(2), litint(3))]
    assert subscript_expr.into_code() == "a[b, 2:3]"
    subscript_expr = id_("a").expr()[id_("b").expr()]
    assert subscript_expr.into_code() == "a[b]"


def test_expr_dict():
    d = dict_(kv(litstr("a"), id_("b")))
    assert d.into_code() == "{'a': b}"

    d = dict_comp(
        kv(id_("a"), litint(1)).for_(id_("a")).in_(id_("range").expr().call(litint(5)))
    )
    assert d.into_code() == "{a: 1 for a in range(5)}"


def test_expr_fstring():
    node = fnode(id_("sin").expr().call(litint(1)), ".2")
    assert node.into_code() == "{sin(1):.2}"
    string = fstring("sin(1) = ", fnode(id_("sin").expr().call(litint(1))))
    assert string.into_code() == 'f"sin(1) = {sin(1)}"'
    for i in ["", "!a", "!r", "!s"]:
        w = synt.expr.fstring.FormatConversionType.from_str(i)
        assert w is not None
        assert w.into_str() == i
    with pytest.raises(ValueError) as err_info:
        w = synt.expr.fstring.FormatConversionType.from_str("foo")
    assert "foo" in str(err_info.value)
    with pytest.raises(ValueError) as err_info:
        w = synt.expr.fstring.FormatConversionType(0).into_str()
    assert "0" in str(err_info.value)


def test_empty():
    assert NULL.into_code() == ""


def test_expr_list():
    l = list_(litstr("a"), id_("b"))
    assert l.into_code() == "['a', b]"
    l = list_comp(
        id_("x").expr().for_(id_("x")).in_(id_("range").expr().call(litint(5)))
    )
    assert l.into_code() == "[x for x in range(5)]"


def test_expr_set():
    s = set_(litint(1), id_("b"))
    assert s.into_code() == "{1, b}"
    s = set_comp(
        id_("x").expr().for_(id_("x")).in_(id_("range").expr().call(litint(5)))
    )
    assert s.into_code() == "{x for x in range(5)}"


def test_expr_slice():
    sl = slice_(litint(5), litint(10))
    assert sl.into_code() == "5:10"
    sl = slice_(litint(5), litint(10), id_("a"))
    assert sl.into_code() == "5:10:a"


def test_expr_tuple():
    t = tup(litstr("abc"))
    assert t.into_code() == "('abc',)"


def test_expr_wrapped():
    wp = wrapped(litint(1) + litint(2)) * litint(3)
    assert wp.into_code() == "(1 + 2) * 3"
    non_wp = (litint(1) + litint(2)) * litint(3)
    assert non_wp.into_code() == "(1 + 2) * 3"


def test_expr_alias():
    al = id_("a").as_(id_("b"))
    assert al.into_code() == "a as b"

    p = path(id_("foo"), id_("bar")).as_(id_("baz"))
    assert p.into_code() == "foo.bar as baz"


def test_expr_modpath():
    p = path(id_("foo"))
    assert p.into_code() == "foo"
    p = path(id_("foo"), id_("bar"))
    assert p.into_code() == "foo.bar"
    p = path(id_("foo"), id_("bar"), depth=3)
    assert p.into_code() == "...foo.bar"
    p = path(id_("foo"), id_("bar")).dep(4)
    assert p.into_code() == "....foo.bar"

    r = relpath(id_("abc"))
    assert r.into_code() == ".abc"

    r = parentpath(id_("abc"))
    assert r.into_code() == "..abc"
