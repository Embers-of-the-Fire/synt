# Synt

<i>Write Python with Python.&emsp;<small>Inspired by [jennifer](https://github.com/dave/jennifer).</small></i>

![Python-3.12](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge)
![GitHub top language](https://img.shields.io/github/languages/top/Embers-of-the-Fire/synt?style=for-the-badge&color=yellow)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/Embers-of-the-Fire/synt/CI.yaml?style=for-the-badge)
![Codecov](https://img.shields.io/codecov/c/github/Embers-of-the-Fire/synt?style=for-the-badge)
![PyPI - Downloads](https://img.shields.io/pypi/dm/synt?style=for-the-badge)
![PyPI - License](https://img.shields.io/pypi/l/synt?style=for-the-badge)
![PyPI - Version](https://img.shields.io/pypi/v/synt?style=for-the-badge)

Synt is a library for developers to write elegant machine-generated Python code.

[Documentation][github-page-doc]

---

## Installation

To install Synt, use your preferred package manager and add `synt` to your dependencies, e.g. by pip:

```bash
pip install synt
```

Then, import Synt:

```python
import synt                    # directly import Synt, or
from synt.prelude import *     # import pre-organized utilities from `prelude`.
```

## Overview

Synt creates a Python-based DSL for writing actual Python code.

Different from text-based template systems like Jinja,
Synt allows you to construct Python code generator as-is:

```python
from synt.prelude import *

expression = id_("foo") \
    .expr() \
    .attr("bar") \
    .call(buzz=id_("buzz"))

assert expression.into_code() == "foo.bar(buzz=buzz)"
```

## Usage

Synt keeps most of Python's standard operations as-is.
Currently, Synt only supports generating expressions,
and statement generating is on the to-do list.

Typically, special syntax in Python can be used with alias methods with the same name.
For example, the following example shows how to create a generator comprehension:

```python
from synt.prelude import *

comp = fstring("Item: ", fnode(id_("x"))) \
    .for_(id_("x")) \
    .in_(id_("it"))

# note: Comprehension expressions are a bit different
#       because it accepts any amount of `for`s and `if`s.
#       Thus we must add a `.expr()` to force it to be an expression.
assert comp.expr().into_code() == r'(f"Item: {x}" for x in it)'
```

For full api documentation, see the [Documentation][github-page-doc] page.

[github-page-doc]: https://embers-of-the-fire.github.io/synt/
