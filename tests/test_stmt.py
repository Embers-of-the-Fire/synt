from __future__ import annotations

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


def test_del():
    d = del_(id_("foo").expr().attr("bar"))
    assert d.into_code() == "del foo.bar"


def test_assign():
    ass = tup(id_("a"), id_("b")).assign(tup(litint(1), litstr("foo")))
    assert ass.into_code() == "a, b = (1, 'foo')"  # automatically unpack
    ass = id_("a").expr().ty(id_("str")).assign(litstr("foo"))
    assert ass.into_code() == "a: str = 'foo'"  # explicitly typing
    ass = id_("a").expr().ty(id_("str"))
    assert ass.into_code() == "a: str"  # only typing


def test_assert():
    assert_stmt = assert_(TRUE, litstr("Condition is true"))
    assert assert_stmt.into_code() == "assert True, 'Condition is true'"


def test_raise():
    r = raise_()
    assert r.into_code() == "raise"
    r = raise_(litint(42))
    assert r.into_code() == "raise 42"
    r = raise_(litint(42)).from_(litstr("Custom exception"))
    assert r.into_code() == "raise 42 from 'Custom exception'"


def test_import():
    im = import_(id_("path"))
    assert im.into_code() == "import path"
    im = import_(id_("asyncio").as_(id_("aio")))
    assert im.into_code() == "import asyncio as aio"
    im = import_(path(id_("io"), id_("path")))
    assert im.into_code() == "import io.path"

    fi = from_(id_("io")).import_(id_("path"))
    assert fi.into_code() == "from io import path"
    fi = from_(id_("io")).import_(id_("path").as_(id_("p")))
    assert fi.into_code() == "from io import path as p"
    fi = from_(id_("io")).import_(path(id_("path")), id_("os").as_(id_("p")))
    assert fi.into_code() == "from io import path, os as p"
    fi = from_(id_("io")).import_("*")
    assert fi.into_code() == "from io import *"


def test_if():
    if_stmt = if_(id_("foo").expr().eq(litstr("bar"))).block(return_(TRUE))
    assert if_stmt.into_code() == "if foo == 'bar':\n    return True"
    # if foo == 'bar'
    #     return True

    if_stmt = (
        if_(id_("foo").expr().eq(litstr("bar")))
        .block(return_(TRUE))
        .elif_(id_("foo").expr().is_not(NONE))
        .block(return_(FALSE))
    )
    assert (
        if_stmt.into_code()
        == """if foo == 'bar':
    return True
elif foo is not None:
    return False"""
    )
    # if foo == 'bar':
    #     return True
    # elif foo is not None:
    #     return False

    if_stmt = (
        if_(id_("foo").expr().eq(litstr("bar")))
        .block(return_(TRUE))
        .elif_(id_("foo").expr().is_not(NONE))
        .block(return_(FALSE))
        .else_(raise_(id_("ValueError").expr().call(litstr("Unexpected value"))))
    )
    assert (
        if_stmt.into_code()
        == """if foo == 'bar':
    return True
elif foo is not None:
    return False
else:
    raise ValueError('Unexpected value')"""
    )
    # if foo == 'bar':
    #     return True
    # elif foo is not None:
    #     return False
    # else:
    #     raise ValueError('Unexpected value')


def test_loop():
    for_loop = (
        for_(id_("i"))
        .in_(id_("range").expr().call(litint(5)))
        .block(if_(id_("i").expr().gt(litint(2))).block(BREAK).else_(CONTINUE))
        .else_(PASS)
    )
    assert (
        for_loop.into_code()
        == """for i in range(5):
    if i > 2:
        break
    else:
        continue
else:
    pass"""
    )
    # for i in range(5):
    #     if i > 2:
    #         break
    #     else:
    #         continue
    # else:
    #     pass


def test_try():
    try_block = (
        try_(PASS)
        .except_(id_("ValueError"))
        .block(PASS)
        .except_(id_("Exception"))
        .as_(id_("e"))
        .block(return_())
        .except_()
        .block(raise_())
        .else_(PASS)
        .finally_(PASS)
    )
    assert (
        try_block.into_code()
        == """try:
    pass
except ValueError:
    pass
except Exception as e:
    return
except:
    raise
else:
    pass
finally:
    pass"""
    )
    # try:
    #     pass
    # except ValueError:
    #     pass
    # except Exception as e:
    #     return
    # except:
    #     raise
    # finally:
    #     pass

    try_block = try_(PASS).except_star(id_("Exception")).block(PASS)
    assert try_block.into_code() == "try:\n    pass\nexcept* Exception:\n    pass"
    # try:
    #     pass
    # except* Exception:
    #     pass


def test_with():
    with_stmt = with_(
        id_("a"), (id_("b"), id_("b2")), with_item(id_("c")).as_(id_("c2"))
    ).block(PASS)
    assert with_stmt.into_code() == "with a, b as b2, c as c2:\n    pass"


def test_ns():
    global_stmt = global_(id_("foo"))
    assert global_stmt.into_code() == "global foo"

    nonlocal_stmt = nonlocal_(id_("foo"))
    assert nonlocal_stmt.into_code() == "nonlocal foo"


def test_expr():
    stmt = id_("print").expr().call(litstr("Hello world!")).stmt()
    assert stmt.into_code() == "print('Hello world!')"


def test_match():
    match_stmt = (
        match_(id_("a"))
        .case_(id_("b"))
        .block(PASS)
        .case_(id_("Point").expr().call(id_("x"), id_("y")))
        .block(PASS)
        .case_(list_(id_("x")).as_(id_("y")))
        .block(PASS)
        .case_(UNDERSCORE)
        .block(PASS)
    )
    assert (
        match_stmt.into_code()
        == """match a:
    case b:
        pass
    case Point(x, y):
        pass
    case [x] as y:
        pass
    case _:
        pass"""
    )
    # match a:
    #     case b:
    #         pass
    #     case Point(x, y):
    #         pass
    #     case [x] as y:
    #         pass
    #     case _:
    #         pass
