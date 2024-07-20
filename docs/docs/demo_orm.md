# Demo of an ORM Code Generator

> This article will demonstrate how to use Synt to write a simple orm codegen.

## Aim

With the code we should be able to generate a utility like this:

```python
from __future__ import annotations


def orm_codegen(
        table: str,
        args: list[tuple[str, str]], # name, type
) -> str:
    ...
```

And this is an example result:

```python
class Person(Orm):
    orm_table_name = "person"
    id: int
    name: str
    position: str
```

## Generating the code

### Write the content

```python
from __future__ import annotations

from synt.prelude import *  # import prelude objects


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
```

### Test the output (Optional)

```python
text = orm_codegen("person", [("id", "int"), ("name", "str"), ("position", "str")])
print(text)
```

Expected output:

```python
class Person(Orm):
    orm_table_name = 'person'
    id: int
    name: str
    position: str
```

### Save the output to a file

```python
with open('/path/to/output.py', 'w+', encoding='utf-8') as f:
    f.write(file.into_str())
```
