from __future__ import annotations


import synt
from synt.prelude import *


def test_fn():
    a = arg(id_("foo")).ty(id_("int")).default(litint(1))
    assert a.into_code() == "foo: int = 1"

    va = vararg(id_("foo")).ty(id_("int"))
    assert va.into_code() == "*foo: int"

    va = kwarg(id_("foo")).ty(id_("tuple").expr()[id_("str"), id_("int")])
    assert va.into_code() == "**foo: tuple[str, int]"

    func = (
        dec(id_("foo"))
        .async_def(id_("bar"))[id_("T")](
            id_("a"), arg(id_("b")).ty(id_("int")), kw=NONE
        )
        .returns(id_("float"))
        .block(return_(ELLIPSIS))
    )
    assert (
        func.into_code()
        == "@foo\nasync def bar[T](a, b: int, kw = None) -> float:\n    return ..."
    )
    # @foo
    # async def bar[T](a, b: int, kw = None) -> float:
    #     return ...

    func = (
        dec(id_("foo"))
        .async_def(id_("bar"))
        .type_param(id_("T"))
        .arg(id_("a"), arg(id_("b")).ty(id_("int")), kw=NONE)
        .returns(id_("float"))
        .block(return_(ELLIPSIS))
    )
    assert (
        func.into_code()
        == "@foo\nasync def bar[T](a, b: int, kw = None) -> float:\n    return ..."
    )
    # @foo
    # async def bar[T](a, b: int, kw = None) -> float:
    #     return ...


def test_cls():
    cls = (
        dec(id_("foo"))
        .class_(id_("Bar"))[id_("T")](metaclass=id_("ABCMeta"))
        .block(
            dec(id_("abstractmethod"))
            .def_(id_("baz"))(id_("self"), arg(id_("a"), id_("T")))
            .returns(id_("str"))
            .block(return_(fstring("Bar(", fnode(id_("a")), ").baz")))
        )
    )
    assert (
        cls.into_code()
        == '''@foo
class Bar[T](metaclass=ABCMeta):
    @abstractmethod
    def baz(self, a: T) -> str:
        return f"Bar({a}).baz"'''
    )


def test_return():
    return_stmt = return_(litint(42))
    assert return_stmt.into_code() == "return 42"
    return_stmt = ret()
    assert return_stmt.into_code() == "return"


def test_keywords():
    assert PASS.into_code() == "pass"
    assert BREAK.into_code() == "break"
    assert CONTINUE.into_code() == "continue"
