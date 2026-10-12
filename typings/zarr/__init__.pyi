# Type information for the part of zarr that gertils and its tests use; zarr 2 ships none.
# Extend it when gertils starts using more of zarr.

from typing import Literal

from numpy.typing import ArrayLike

class Array: ...

def open_array(store: str, mode: Literal["r", "r+", "a", "w", "w-"] = "a") -> Array: ...
def save_array(store: str, arr: ArrayLike) -> None: ...
