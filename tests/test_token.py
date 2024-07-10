from __future__ import annotations

import pytest

from synpy.prelude import *
import synpy


def test_kwd():
    assert synpy.tokens.keywords.is_hard_keyword("False")
    assert synpy.tokens.keywords.is_soft_keyword("type")


def test_ident():
    id_foo = synpy.tokens.ident.Identifier("foo")
    id_foo_alias = id_("foo")  # with alias

    with pytest.raises(InvalidIdentifierException) as err_info:
        id_fail = id_("foo bar")  # invalid identifier lit will fail
    print(repr(err_info.value))

    id_foo = id_("foo")
    id_foo_expr = id_foo.expr()
    assert isinstance(id_foo_expr, synpy.expr.expr.Expression)


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
