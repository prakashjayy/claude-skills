# Advanced Patterns

Reference for the more distinctive patterns in this pragmatic Python style.

---

## `@patch` — Adding Methods Post-Definition

Adds methods to existing classes without subclassing. The type annotation on `self` determines the target class.

```python
from fastcore.basics import patch

@patch
def shuffle(self: L, seed=None):
    "Return a shuffled copy of `L`"
    items = copy(self.items)
    if seed is not None: random.seed(seed)
    random.shuffle(items)
    return type(self)(items)

@patch(as_prop=True)
def sorted(self: L):
    "Return sorted copy of `L`"
    return type(self)(sorted(self.items))
```

Use `@patch` when:
- You want to extend a class you don't own
- You want to keep method definitions close to where they're used
- You're organizing methods by feature rather than class

---

## `store_attr()` — Auto-Store Init Params

Uses frame introspection to store all local variables in `__init__` as `self.*`.

```python
class Optimizer:
    def __init__(self, params, lr=1e-3, mom=0.9, wd=0.01, eps=1e-8):
        store_attr()
        # Equivalent to:
        # self.params = params; self.lr = lr; self.mom = mom; ...

# Exclude some params:
class Model:
    def __init__(self, layers, device='cpu', _debug=False):
        store_attr(but='_debug')   # skips _debug

# Store only named params:
class Config:
    def __init__(self, lr, wd, epochs):
        store_attr('lr,wd')        # only stores lr and wd
```

---

## `@delegates` — Transparent Kwargs

Replaces `**kwargs` in the function signature with the actual params from the delegated function. Enables accurate IDE autocomplete and `help()` output.

```python
from fastcore.meta import delegates

def fit(model, epochs, lr, wd=0.01, callbacks=None):
    "Fit `model` for `epochs`"
    ...

@delegates(fit)
def fine_tune(model, epochs, base_lr=1e-3, **kwargs):
    "Fine-tune with discriminative learning rates"
    fit(model, epochs//4, base_lr/100, **kwargs)
    fit(model, epochs, base_lr, **kwargs)
```

Now `help(fine_tune)` shows `wd` and `callbacks` params from `fit`.

---

## `bind` and `Self` — Lambda Alternatives

**`bind`** — like `partial` but supports positional argument placeholders:
```python
from fastcore.basics import bind, arg0, arg1

f = bind(operator.add, arg0, 10)
f(5)    # → 15, arg0 is a placeholder for first positional arg

# Useful in map:
list(map(bind(str.replace, arg0, 'a', 'b'), ['cat', 'bat']))
# → ['cbt', 'bbt']
```

**`Self`** — lazy method caller, avoids `lambda`:
```python
from fastcore.basics import Self

items = L(['hello world', 'foo bar'])
items.map(Self.split())         # → [['hello', 'world'], ['foo', 'bar']]
items.map(Self.upper())         # → ['HELLO WORLD', 'FOO BAR']
# vs: items.map(lambda x: x.split())
```

---

## `L` Collection — Fluent List Operations

An enhanced list with boolean indexing, masking, and fluent method chaining:

```python
items = L([1, 2, 3, 4, 5])
items.filter(lambda x: x > 2)      # → L([3, 4, 5])
items.map(lambda x: x * 2)         # → L([2, 4, 6, 8, 10])
items.unique()                      # → L([1, 2, 3, 4, 5])
items[[0, 2, 4]]                    # → L([1, 3, 5])  — list indexing
items[L([True, False, True, False, True])]  # boolean mask
```

Prefer `L` over plain `list` when:
- You need chainable operations
- You need boolean/list indexing
- You're building pipelines

---

## `partialler` — Partial with Docstring Preservation

```python
from fastcore.basics import partialler

def format_num(x, decimals=2, prefix=''):
    "Format number `x` with `decimals` decimal places and `prefix`"
    return f"{prefix}{x:.{decimals}f}"

fmt_dollar = partialler(format_num, decimals=2, prefix='$')
fmt_dollar.__doc__  # → "Format number `x` with `decimals` decimal places and `prefix`"
```

Use `partialler` instead of `partial` whenever the resulting function will be inspected or documented.

---

## Operator Factory Pattern

Generating many similar functions from a loop:

```python
_ops = ['lt', 'gt', 'le', 'ge', 'eq', 'ne', 'add', 'sub', 'mul']

def _mk_op(op, g):
    def _inner(a, b=_dumobj):
        return (lambda o: getattr(operator, op)(o, a)) if b is _dumobj else getattr(operator, op)(a, b)
    _inner.__name__ = op
    _inner.__doc__ = f"Partial application of `operator.{op}`"
    g[op] = _inner

for op in _ops: _mk_op(op, globals())

# Now: lt(5) returns a function that tests if x < 5
# items.filter(gt(0))  # items greater than 0
```

---

## `GetAttr` — Attribute Delegation

Transparently delegates attribute access to a wrapped object:

```python
from fastcore.basics import GetAttr

class DataPipeline(GetAttr):
    _default = 'dataset'    # delegate unknown attrs to self.dataset

    def __init__(self, dataset, transforms=None):
        self.dataset = dataset
        self.transforms = transforms or []

pipe = DataPipeline(my_dataset)
pipe.items     # → my_dataset.items (delegated)
pipe.n_items   # → my_dataset.n_items (delegated)
```

---

## `compose` — Function Composition

```python
from fastcore.basics import compose

preprocess = compose(
    str.strip,
    str.lower,
    lambda s: s.replace('-', '_')
)

preprocess("  Hello-World  ")   # → "hello_world"
```

Use for building transformation pipelines without nesting lambdas.

---

## Custom Exception Helpers (Testing)

```python
@contextmanager
def ExceptionExpected(ex=Exception, regex=''):
    "Context manager that tests if an exception is raised"
    try: yield
    except ex as e:
        if regex: assert re.search(regex, str(e.args)), f"Pattern {regex!r} not in {e.args!r}"
        return
    assert False, f"Expected {ex.__name__} but none raised"

# Usage:
with ExceptionExpected(ValueError, regex='must be positive'):
    validate_input(-1)
```

---

## Metaclass Patterns (when you truly need them)

Use metaclasses only when you need to affect ALL instances of a class at class-creation time:

- **`FixSigMeta`**: Fixes `__signature__` when a class overrides `__new__` — makes `help()` show right params
- **`PrePostInitMeta`**: Adds `__pre_init__` and `__post_init__` hooks without touching `__init__`
- **`NewChkMeta`**: `MyClass(already_a_myclass)` returns the object unchanged instead of wrapping it
- **`BypassNewMeta`**: Smart casting — `MyClass(x)` casts `x` if possible, bypasses if already correct type

For anything else, use a decorator or `__init_subclass__`.

---

## Enum Extensions

```python
class StrEnum(str, enum.Enum):
    "An enum that behaves like a `str`"
    def __str__(self): return self.name

    @classmethod
    def imports(cls):
        "Import all enum values into caller's namespace"
        g = sys._getframe(1).f_locals
        for o in cls: g[o.name] = o

class Color(StrEnum):
    red = auto()
    green = auto()

Color.imports()   # imports red, green into local namespace
str(Color.red)    # → 'red'  (not 'Color.red')
```

---

## Repo Layout (Standard .py Files)

```
mypackage/
├── __init__.py          # re-exports from submodules
├── core.py              # fundamental utilities, no deps on other submodules  
├── data.py              # depends on core
├── model.py             # depends on core
└── train.py             # depends on data and model

tests/
├── test_core.py
├── test_data.py
└── test_model.py

pyproject.toml
README.md
```

- One layer of imports: `from .core import *` in `__init__.py`
- Keep `__all__` in every module
- Tests import from the package directly, not from files
