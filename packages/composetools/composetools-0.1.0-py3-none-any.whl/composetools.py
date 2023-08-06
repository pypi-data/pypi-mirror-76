"""Utility functions for common tasks when composing functions."""

__version__ = "0.1.0"
__all__ = (
    "tap",
    "keep",
    "each",
    "sort",
    "drop",
    "flat",
    "unique",
)


def tap(fn):
    """Get a function that takes `x`, executes `fn(x)`, and returns `x`."""
    def tapper(x):
        fn(x)
        return x
    return tapper


def keep(check):
    """Yield items of the iterable where `check(item)` succeeds."""
    def keeper(it):
        return (x for x in it if check(x))
    return keeper


def drop(check):
    """Yield items of the iterable where `check(item)` fails."""
    def remover(it):
        return (x for x in it if not check(x))
    return remover


def each(fn):
    """Yield the result of applying `fn` to each item of an iterable."""
    def mapper(it):
        return (fn(x) for x in it)
    return mapper


def sort(_=None, /, *, key=None, reverse=False):
    """Get a sorted list of the input iterable."""
    def sorter(iterable):
        return sorted(iterable, key=key, reverse=reverse)

    if _ is None:
        return sorter

    return sorter(_)


def flat(_=None, /, *, depth=1, scalar=(str, bytes, set, dict)):
    """Flatten a sequence of regular or irregular depth.

    `scalar` types are treated as single, even if iterable.
    """
    from collections.abc import Iterable

    def flattener(iterable):
        if depth <= 0:
            yield from iterable
            return

        for item in iterable:
            if isinstance(item, Iterable) and not isinstance(item, scalar):
                yield from flat(item, depth=depth-1, scalar=scalar)
            else:
                yield item

    if _ is None:
        return flattener

    return flattener(_)


def unique(_=None, /, *, key=None):
    """Yield all unique items of an iterable."""
    from collections.abc import Hashable

    def inner(iterable):
        hashables = set()
        unhashables = []

        for item in iterable:
            value = item if not key else key(item)

            if isinstance(value, Hashable):
                if value in hashables:
                    continue
                hashables.add(value)
            else:
                if value in unhashables:
                    continue
                unhashables.append(value)

            yield item

    if _ is None:
        return inner

    return inner(_)
