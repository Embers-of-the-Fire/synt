from __future__ import annotations

import pytest

from synpy.prelude import *


def test_kwd():
    assert synpy.tokens.keywords.is_hard_keyword("False")
    assert synpy.tokens.keywords.is_soft_keyword("type")


def test_ident():
    id_foo = synpy.tokens.ident.Identifier("foo")
    id_foo_alias = id_("foo")  # with alias

    with pytest.raises(InvalidIdentifierException) as err_info:
        id_fail = id_("foo bar")  # invalid identifier lit will fail
    print(repr(err_info.value))
