from __future__ import annotations

import synpy.token.keyword


def test_namespace():
    assert synpy.token.keyword.is_hard_keyword("False")
    assert synpy.token.keyword.is_soft_keyword("type")
