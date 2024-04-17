"""Tools for working with ZARR"""

import logging
from pathlib import Path

import zarr  # type: ignore[import]
from numpydoc_decorator import doc  # type: ignore[import]

from .types import PixelArray


@doc(
    summary="Read data from ZARR rooted at given path.",
    parameters=dict(root="Path at which datastore is rooted"),
    returns="Array of pixel (or similar) data",
)
def read_zarr(root: Path) -> PixelArray:  # noqa: D103
    logging.debug("Reading ZARR: %s", root)
    if (root / ".zarray").is_file():
        data_root = root
    elif (root / "0" / ".zarray").is_file():
        data_root = root / "0"
    else:
        raise ZarrParseException(path=root, msg="Failed to find .zarray to indicate data folder")
    return zarr.open(data_root)[:]  # type: ignore[no-any-return]


class ZarrParseException(Exception):
    """Exception for when something goes wrong parsing ZARR"""

    def __init__(self, *, path: Path, msg: str) -> None:  # noqa: D107
        super().__init__(f"Parsing {path} failed with message: {msg}")
        self.path = path
