# SynPy

<i>Write Python with Python.&emsp;<small>Inspired by [jennifer](https://github.com/dave/jennifer).</small></i>

![Python-3.12](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge)
![GitHub top language](https://img.shields.io/github/languages/top/Embers-of-the-Fire/syn-py?style=for-the-badge&color=yellow)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/Embers-of-the-Fire/syn-py/CI.yaml?style=for-the-badge)
![Codecov](https://img.shields.io/codecov/c/github/Embers-of-the-Fire/syn-py?style=for-the-badge)
![PyPI - Downloads](https://img.shields.io/pypi/dm/syn-py?style=for-the-badge)
![PyPI - License](https://img.shields.io/pypi/l/syn-py?style=for-the-badge)
![PyPI - Version](https://img.shields.io/pypi/v/syn-py?style=for-the-badge)

SynPy is a library for developers to write elegant machine-generated Python code.

[Documentation][github-page-doc]

---

## Installation

To install SynPy, use your preferred package manager and add `syn-py` to your dependencies, e.g. by pip:

```bash
pip install syn-py
```

Then, import SynPy:

```python
import synpy                    # directly import SynPy, or
from synpy.prelude import *     # import pre-organized utilities from `prelude`.
```

## Overview

SynPy creates a Python-based DSL for writing actual Python code.

Different from text-based template systems like Jinja,
SynPy allows you to construct Python code generator as-is:

```python
from synpy.prelude import *

expression = id_("foo") \
    .expr() \
    .attr("bar") \
    .call(buzz=id_("buzz"))

assert expression.into_code() == "foo.bar(buzz=buzz)"
```

## Usage

SynPy keeps most of Python's standard operations as-is.
Currently, SynPy only supports generating expressions,
and statement generating is on the to-do list.

Typically, special syntax in Python can be used with alias methods with the same name.
For example, the following example shows how to create a generator comprehension:

```python
from synpy.prelude import *

comp = fstring("Item: ", fnode(id_("x"))) \
    .for_(id_("x")) \
    .in_(id_("it"))

# note: Comprehension expressions are a bit different
#       because it accepts any amount of `for`s and `if`s.
#       Thus we must add a `.expr()` to force it to be an expression.
assert comp.expr().into_code() == r'(f"Item: {x}" for x in it)'
```

For full api documentation, see the [Documentation][github-page-doc] page.

[github-page-doc]: https://embers-of-the-fire.github.io/syn-py/
