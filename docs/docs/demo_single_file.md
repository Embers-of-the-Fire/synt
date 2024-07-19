# Demo with a Single File

> This article will demonstrate how to use Synt to write a simple file generator with static content.

## Aim

With the code we should be able to generate a file like the following:

```python
from __future__ import annotations

print('Hello world!')

prime_numbers: list[int] = []
for i in range(2, 100):
    for j in range(2, i):
        if i % j == 0:
            break
    else:
        prime_numbers.append(i)

assert 13 in prime_numbers
```

## Generating the file

### Write the content

```python
from synt.prelude import *  # import prelude objects

file = File(
    from_(id_("__future__")).import_(id_("annotations")),
    id_("print").expr().call(litstr("Hello world!")).stmt(),
    id_("prime_numbers").expr().assign(list_()).type(id_("list").expr()[id_("int")]),
    for_(id_("i")).in_(id_("range").expr().call(litint(2), litint(100))).block(
        for_(id_("j")).in_(id_("range").expr().call(litint(2), id_("i"))).block(
            if_(id_("i").expr() % id_("j") == litint(0)).block(
                BREAK
            ).else_(
                id_("prime_numbers").expr().attr("append").call(id_("i")).stmt()
            )
        )
    ),
    assert_(litint(13).in_(id_("prime_numbers")))
)
```

### Test the output (Optional)

```python
text = file.into_str()
print(text)
```

Expected output:

```python
from __future__ import annotations
print('Hello world!')
prime_numbers: list[int] = []
for i in range(2, 100):
    for j in range(2, i):
        if i % j == 0:
            break
        else:
            prime_numbers.append(i)
assert 13 in prime_numbers
```

> **Note**:
> 
> You may find that there's no blank line between the code.
> Designed as a massive code generator, Synt (currently) doesn't support explicit space lines.

### Save the output to a file

```python
with open('/path/to/output.py', 'w+', encoding='utf-8') as f:
    f.write(file.into_str())
```
