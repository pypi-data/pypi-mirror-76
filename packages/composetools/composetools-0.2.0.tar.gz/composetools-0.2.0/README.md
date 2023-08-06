# composetools

**A library of utility functions** for Pythonic function composition.<br>
Most utilities are focused on transforming and dealing with iterables.

## Install

```console
pip install composetools
```

## Functions

* `compose`

   Compose functions such that `compose(f, g)(x)` is equivalent to `g(f(x))`

* `pipe`

   Compose functions such that `pipe(f, g)(x)` is equivalent to `f(g(x))`

### Utilities

* `unique` - Yield unique items of an iterable.
* `each` - Curried `map`.
* `keep` - Curried `filter`.
* `drop` - Curried `itertools.filterfalse`.
* `sort` - Curried `sorted`.
* `flat` - Flatten an arbitrarily nested iterable to a desired depth.
* `also` - Call a function and return its *input*, eg. `also(print)(4)`
will print 4 and return 4.

## Develop

```console
$ gh repo clone SeparateRecords/python-composetools
$ poetry install
$ poetry run python -m pytest tests.py
```

## Licence

ISC
