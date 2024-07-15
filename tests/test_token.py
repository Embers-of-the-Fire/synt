from __future__ import annotations

import pytest
import synt

from synt.prelude import *


def test_kwd():
    assert synt.tokens.keywords.is_hard_keyword("False")
    assert synt.tokens.keywords.is_soft_keyword("type")


def test_ident():
    id_foo = synt.tokens.ident.Identifier("foo")
    id_foo_alias = id_("foo")  # with alias

    with pytest.raises(InvalidIdentifierException) as err_info:
        id_fail = id_("foo bar")  # invalid identifier lit will fail
    print(repr(err_info.value))

    id_foo = id_("foo")
    id_foo_expr = id_foo.expr()
    assert isinstance(id_foo_expr, synt.expr.expr.Expression)


def test_kv_pair():
    kv_pair = kv(id_("a"), id_("b"))
    assert kv_pair.into_code() == "a: b"


def test_lit():
    a = litstr("abc")
    assert a.into_code() == "'abc'"
    a = litint(1)
    assert a.into_code() == "1"
    a = litfloat(0.24)
    assert a.into_code() == "0.24"
    assert litbool(True).into_code() == TRUE.into_code()
    assert litbool(False).into_code() == FALSE.into_code()
    assert synt.tokens.lit.Literal._str("foo").into_code() == "foo"
