from __future__ import annotations

from synt.prelude import *


def test_file():
    file = File(
        id_("print").expr().call(litstr("Hello, World!")).stmt(),
        id_("x").expr().assign(litint(42)),
        if_(id_("x").expr().eq(litint(42))).block(
            id_("print").expr().call(litstr("x is 42")).stmt()
        ),
    )
    assert (
        file.into_str()
        == """print('Hello, World!')
x = 42
if x == 42:
    print('x is 42')"""
    )
