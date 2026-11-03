"""Tools for working with ZARR"""

import logging
from pathlib import Path
from typing import Any

import numpy as np
import numpy.typing as npt
import zarr

from .types import PixelArray

logger: logging.Logger = logging.getLogger(__name__)


def read_zarr(root: Path) -> PixelArray:
    """Read data from ZARR rooted at given path.

    Parameters
    ----------
    root : Path
        Path at which datastore is rooted: an array, or a group with the array
        at '0', in zarr format 2 or 3.

    Returns
    -------
    NDArray[uint8 or uint16] or Array
        Array of pixel (or similar) data.

    Raises
    ------
    ZarrParseException
        If neither the root nor '0' holds an array, or zarr can't read the
        metadata.

    """
    logger.debug("Reading ZARR: %s", root)
    for folder in (root, root / "0"):
        pixels = _read_array(folder)
        if pixels is not None:
            return pixels
    raise ZarrParseException(
        path=root,
        msg="Failed to find an array's .zarray or zarr.json to indicate data folder",
    )


def _read_array(folder: Path) -> npt.NDArray[Any] | None:
    """Read the array in the folder, or give None if the folder holds a group or nothing."""
    try:
        # zarr tells what the folder holds from its metadata, in either format. The stores
        # zarr accepts include fsspec's, and fsspec ships no type information, so pyright
        # can't know the whole signature.
        node = zarr.open(str(folder), mode="r")  # pyright: ignore[reportUnknownMemberType]
    except FileNotFoundError:
        # Also zarr's NodeNotFoundError, for a folder without zarr metadata.
        return None
    except (ValueError, KeyError, TypeError, AttributeError) as error:
        # zarr doesn't validate metadata before it uses it, so damaged metadata, such as a
        # zarr.json cut off by a killed job, can raise any of these.
        raise ZarrParseException(
            path=folder, msg=f"Failed to read zarr metadata: {error!r}"
        ) from error
    return np.asarray(node) if isinstance(node, zarr.Array) else None


class ZarrParseException(Exception):
    """Exception for when something goes wrong parsing ZARR"""

    def __init__(self, *, path: Path, msg: str) -> None:  # noqa: D107
        super().__init__(f"Parsing {path} failed with message: {msg}")
        self.path = path
