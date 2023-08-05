"""A Pythonic way to apply multiple functions to an object."""

__version__ = "0.5.0"
__all__ = (
    "apply",
    "tap",
    "keep",
    "each",
    "sort",
    "unique",
    "remove",
    "flatten",
)


def apply(*fns):
    """Get a function that applies each function of `fns` to an object."""
    def do_apply(x):
        for fn in fns:
            x = fn(x)
        return x
    return do_apply


def tap(fn):
    """Get a function that takes `x`, execute `fn(x)`, return `x`."""
    def tapper(x):
        fn(x)
        return x
    return tapper


def keep(check):
    """Yield items of the iterable where `check(item)` succeeds."""
    def keeper(it):
        return (x for x in it if check(x))
    return keeper


def remove(check):
    """Yield items of the iterable where `check(item)` fails."""
    def remover(it):
        return (x for x in it if not check(x))
    return remover


def each(fn):
    """Yield the result of applying `fn` to each item of an iterable."""
    def mapper(it):
        return (fn(x) for x in it)
    return mapper


def sort(it=None, *, key=None, reverse=False):
    """Get a sorted list of the input iterable."""
    def sorter(iterable):
        return sorted(iterable, key=key, reverse=reverse)

    if it is None:
        return sorter

    return sorter(it)


def flatten(it=None, *, depth=1, scalar=(str, bytes)):
    """Flatten a sequence of regular or irregular depth.

    `scalar` types are treated as single, even if iterable.
    """
    from collections.abc import Sequence

    def flattener(sequence):
        if depth <= 0:
            yield from sequence
            return

        for item in sequence:
            if isinstance(item, Sequence) and not isinstance(item, scalar):
                yield from flatten(item, depth=depth-1, scalar=scalar)
            else:
                yield item

    if it is None:
        return flattener

    return flattener(it)


def unique(it=None, *, key=None):
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

    if it is None:
        return inner

    return inner(it)
