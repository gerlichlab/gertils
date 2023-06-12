"""Extra tools for working with collections"""

from collections import OrderedDict
from typing import *

__author__ = "Vince Reuter"

__all__ = ["count_repeats", "listify", "uniquify"]

# Very core abstractions related to collections are apt to use very generic
# names deliberately to underscore the generality of the logic, so disable
# the invalid name warnings that often result, for all code in this module.
# pylint: disable=invalid-name


AnyT = TypeVar("AnyT")
HashT = TypeVar("HashT", bound=Hashable)


def count_repeats(xs: Iterable[HashT]) -> List[Tuple[HashT, int]]:
    """Count the instance of repeated elements and their number"""
    return [(x, n) for x, n in Counter(xs).items() if n > 1]


def listify(maybe_items: Optional[Iterable[AnyT]]) -> List[AnyT]:
    """Convert an optional iterable into a list, or wrap a string as a singleton list."""
    if maybe_items is None:
        return []
    if isinstance(maybe_items, str):
        return [maybe_items]
    return list(maybe_items)


def uniquify(xs: Iterable[HashT]) -> Iterable[HashT]:
    """Collapse repeats to single values while preserving order of the given items."""
    seen: MutableMapping[HashT, None] = OrderedDict()
    for x in xs:
        if x in seen:
            continue
        seen[x] = None
    return seen.keys()
