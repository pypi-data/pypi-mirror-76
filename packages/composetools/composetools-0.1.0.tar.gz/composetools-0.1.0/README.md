# composetools

Utility functions for Pythonic function composition.
BYO `compose()` implementation.

## Install

```
pip install composetools
```

## Examples

```python
from funcy import compose, rcompose

from composetools import unique, flat, sort


# Get unique items from nested iterables.
compose(sort, flat, unique)([[1, 2, 3], [4, 3, 2]])  # [1, 2, 3, 4]


# Get lines of a file.
from pathlib import Path
get_lines = rcompose(
    Path,
    Path.expanduser,
    Path.resolve,
    Path.read_text,
    str.splitlines,
)
get_lines("~/.gitconfig")
```

## Functions

* `tap` - Call a function but don't return the result, eg. `tap(lambda x: print(x))(4) == 4`
* `each` - Curried version of `map`.
* `keep` - Curried version of `filter`.
* `drop` - Curried version of `itertools.filterfalse`.
* `sort` - Curried version of `sorted`.
* `flat` - Flatten an arbitrarily nested iterable.
* `unique` - Yield unique items of an iterable.

## Develop

```
$ git clone https://github.com/SeparateRecords/python-composetools
$ poetry install
$ poetry run tests
```

## Licence

ISC
