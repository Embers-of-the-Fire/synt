from __future__ import annotations


import synt
from synt.prelude import *


def test_ty_param():
    ty_var = tvar(id_("T"), id_("int"))
    assert ty_var.into_code() == "T: int"

    ty_var = ttup(id_("T"))
    assert ty_var.into_code() == "*T"

    ty_var = tspec(id_("P"))
    assert ty_var.into_code() == "**P"
