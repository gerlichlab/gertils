"""Tools for working with ZARR"""

import json
import logging
from pathlib import Path

import numpy as np
import zarr
from numpydoc_decorator import doc

from .types import PixelArray


@doc(
    summary="Read data from ZARR rooted at given path.",
    parameters=dict(
        root="Path at which datastore is rooted: an array, or a group with the array at '0', in zarr format 2 or 3"
    ),
    returns="Array of pixel (or similar) data",
)
def read_zarr(root: Path) -> PixelArray:
    logging.debug("Reading ZARR: %s", root)
    if _holds_array(root):
        data_root = root
    elif _holds_array(root / "0"):
        data_root = root / "0"
    else:
        raise ZarrParseException(
            path=root,
            msg="Failed to find an array's .zarray or zarr.json to indicate data folder",
        )
    # The check above found an array, so open it as one; reading is all this function does.
    # The stores zarr accepts include fsspec's, which isn't installed, so pyright can't
    # know the whole signature.
    return np.asarray(zarr.open_array(str(data_root), mode="r"))  # pyright: ignore[reportUnknownMemberType]


def _holds_array(folder: Path) -> bool:
    """Whether the folder has an array's metadata: .zarray in format 2, zarr.json in format 3."""
    if (folder / ".zarray").is_file():
        return True
    metadata_path = folder / "zarr.json"
    if not metadata_path.is_file():
        return False
    # In format 3, a group has a zarr.json too, so the node type tells the two apart.
    metadata: dict[str, object] = json.loads(metadata_path.read_text())
    return metadata.get("node_type") == "array"


class ZarrParseException(Exception):
    """Exception for when something goes wrong parsing ZARR"""

    def __init__(self, *, path: Path, msg: str) -> None:  # noqa: D107
        super().__init__(f"Parsing {path} failed with message: {msg}")
        self.path = path
