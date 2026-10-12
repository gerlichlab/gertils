# Type information for the part of zarr that gertils and its tests use; zarr 2 ships none.
# Extend it when gertils starts using more of zarr.

from collections.abc import MutableMapping
from typing import Literal

from numpy.typing import ArrayLike

class Array: ...

def array(
    data: ArrayLike,
    *,
    chunks: tuple[int, ...] | None = None,
    store: MutableMapping[str, bytes] | None = None,
) -> Array: ...
def open_array(
    store: str | MutableMapping[str, bytes], mode: Literal["r", "r+", "a", "w", "w-"] = "a"
) -> Array: ...
def save_array(store: str, arr: ArrayLike) -> None: ...
