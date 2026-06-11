---
name: pragmatic-py
description: Write Python code in a pragmatic, minimal-boilerplate style — short functions, concise backtick docstrings, selective type hints, custom test helpers, store_attr/patch patterns, and functional-first idioms. Use when user says "pragmatic-py", "pragmatic style", "clean python style", or wants code following this minimal, functional-first Python philosophy.
---

# Pragmatic Python Style

Quick reference for writing Python code in a concise, boilerplate-free, functional-first style.

## Core Philosophy

- **Minimal boilerplate** — use introspection and decorators to eliminate repetition
- **Self-documenting names** — brief docstrings instead of lengthy comments
- **Functional first** — prefer composition, `map`, comprehensions over imperative loops
- **Short functions** — almost everything fits under 20 lines; one-liners are fine when clear
- **Strategic types** — annotate only where it adds clarity; return types more than params

---

## Functions

**One-liners are fine:**
```python
def ifnone(a, b):
    "`b` if `a` is None else `a`"
    return b if a is None else a

def maybe_attr(o, attr):
    "`getattr(o,attr,o)`"
    return getattr(o, attr, o)
```

**Flexible args with `*args, **kwargs`:**
```python
def map_ex(iterable, f, *args, gen=False, **kwargs):
    "Like `map`, but supports `str` and indexing"
    g = bind(f, *args, **kwargs) if callable(f) else f.format if isinstance(f, str) else f.__getitem__
    res = map(g, iterable)
    return res if gen else list(res)
```

**Sentinel defaults instead of mutable defaults:**
```python
_none = object()

def get_first(items, default=_none):
    for o in items: return o
    if default is _none: raise ValueError("empty")
    return default
```

**Internal helpers use underscore prefix:**
```python
def _mk_op(op, g): ...    # private
def mk_op(op): ...        # public
```

---

## Docstrings

**Always a single backtick-wrapped line.** No numpy/google style. Conversational, short.

```python
def chunked(it, chunk_sz=None, drop_last=False, n_chunks=None):
    "Return batches from iterator `it` of size `chunk_sz` (or return `n_chunks` total)"
    ...
```

- Use backticks around param names: `` `a` ``, `` `b` ``
- One sentence max
- Explain WHAT, never HOW
- No `Args:`, `Returns:`, `Raises:` sections

---

## Types

Use types selectively — not everywhere:

```python
def ver2tuple(v: str) -> tuple:        # return type worth annotating
    ...

def listify(o=None, *rest, use_list=False, match=None):  # no types — clear enough
    ...
```

- Annotate return types more often than params
- Use `None` default freely; check with `ifnone()` or `is None`
- For Union: `Union[int, str]` or `int|str` (3.10+)

---

## Classes

**`store_attr()` eliminates `__init__` boilerplate:**
```python
class Param:
    def __init__(self, help="", type=None, opt=True, action=None, default=None):
        store_attr()   # stores all params as self.help, self.type, etc.
```

**`@patch` adds methods after class definition:**
```python
@patch
def unique(self: L, sort=False, bidir=False, start=None):
    "Unique items, in stable order"
    return L(uniqueify(self, sort=sort, bidir=bidir, start=start))
```

**`@delegates` expands `**kwargs` signature:**
```python
@delegates(fit)
def fine_tune(self, epochs, lr=None, **kwargs):
    "Fine-tune for `epochs` starting from `lr`"
    ...
```

**Mixins over deep inheritance:**
```python
class MyClass(GetAttr, CollBase):
    _default = 'items'    # GetAttr delegates to self.items
```

---

## Module Structure

```python
# Top of every module — comprehensive __all__
__all__ = ['ifnone', 'maybe_attr', 'listify', 'L', 'patch', 'store_attr']

from .imports import *
import builtins, types, typing
from functools import wraps, partial
from copy import copy
```

- `__all__` at the top, always — defines the public API
- Relative imports from own package with `.`
- Layer modules: `imports` → `basics` → `foundation` → `meta`

---

## Idioms

**Creative tuple-indexing instead of if/else:**
```python
# Instead of: if f(o): ts.append(o) else: fs.append(o)
(fs, ts)[f(o)].append(o)
```

**Comprehensions and `map` over loops:**
```python
def filter_dict(d, func):
    "Filter a `dict` using `func`, applied to keys and values"
    return {k: v for k, v in d.items() if func(k, v)}
```

**`partialler` preserves docstrings:**
```python
def partialler(f, *args, order=None, **kwargs):
    "Like `partial` but copies docstring"
    fnew = partial(f, *args, **kwargs)
    fnew.__doc__ = f.__doc__
    return fnew
```

**Context managers for temporary state:**
```python
@contextmanager
def modified_env(**env_vars):
    "Temporarily modify environment variables"
    old = {k: os.environ.get(k) for k in env_vars}
    for k, v in env_vars.items(): os.environ[k] = v
    try: yield
    finally:
        for k, v in old.items():
            if v is None: os.environ.pop(k, None)
            else: os.environ[k] = v
```

---

## Testing

Use custom test helpers, not raw pytest assertions:

```python
def test_eq(a, b):
    "`test` that `a==b`"
    assert a == b, f"Expected {b!r} but got {a!r}"

def test_ne(a, b):
    "`test` that `a!=b`"
    assert a != b, f"Expected {a!r} != {b!r}"
```

- Test file: `tests/test_<module>.py`
- Test function naming: `test_<behavior>`, not `test_<function_name>`
- Use `ExceptionExpected` context manager for expected failures
- Test observable behavior, not implementation details

---

## What NOT to do

- No multi-line or section-style docstrings (`Args:`, `Returns:`, `Raises:`)
- No over-engineered abstractions for single-use code
- No comments explaining HOW — rename instead
- No deep class hierarchies — prefer mixins and composition
- No bare `except:` except in tiny utilities where truly all exceptions are fine
- No type annotations on every parameter — only when genuinely clarifying

---

See [PATTERNS.md](PATTERNS.md) for advanced patterns: `@patch`, `bind`, `Self`, metaclasses, signature manipulation.
