from __future__ import annotations

from synt.prelude import *


def test_demo_single_file():
    file = File(
        from_(id_("__future__")).import_(id_("annotations")),
        id_("print").expr().call(litstr("Hello world!")).stmt(),
        id_("prime_numbers")
        .expr()
        .assign(list_())
        .type(id_("list").expr()[id_("int")]),
        for_(id_("i"))
        .in_(id_("range").expr().call(litint(2), litint(100)))
        .block(
            for_(id_("j"))
            .in_(id_("range").expr().call(litint(2), id_("i")))
            .block(
                if_(id_("i").expr() % id_("j") == litint(0))
                .block(BREAK)
                .else_(id_("prime_numbers").expr().attr("append").call(id_("i")).stmt())
            )
        ),
        assert_(litint(13).in_(id_("prime_numbers"))),
    )

    print(file.into_str())


def test_demo_orm():
    def orm_codegen(table: str, args: list[tuple[str, str]]) -> str:
        cls_name = "".join(x.title() for x in table.split("_"))
        rows = [id_(n).expr().ty(id_(t)) for n, t in args]
        file = File(
            class_(id_(cls_name))(id_("Orm")).block(
                id_("orm_table_name").expr().assign(litstr(table)),
                *rows,
            )
        )
        return file.into_str()

    text = orm_codegen("person", [("id", "int"), ("name", "str"), ("position", "str")])
    print(text)
