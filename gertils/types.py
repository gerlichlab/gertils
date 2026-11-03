"""Data types commonly used around this package"""

from dataclasses import dataclass
from pathlib import Path
from typing import Union

import numpy as np
import numpy.typing as npt
from dask.array.core import Array as DaskArray

CsvRow = list[str]
LayerParams = dict
PathLike = Union[str, Path]
PathOrPaths = Union[PathLike, list[PathLike]]
PixelValue = Union[np.uint8, np.uint16]
PixelArray = Union[npt.NDArray[PixelValue], DaskArray]


def _is_int(value: object) -> bool:
    """Check at runtime, since callers may pass any type despite the annotations."""
    return isinstance(value, int)


@dataclass(frozen=True, order=True)
class FieldOfViewFrom1:
    """Wrap an int as a 1-based field of view (FOV).

    Parameters
    ----------
    get : int
        The value to wrap.

    Raises
    ------
    TypeError
        If the given value to wrap isn't an integer.
    ValueError
        If the given value to wrap isn't positive.

    """

    get: int

    def __post_init__(self) -> None:
        if not _is_int(self.get):
            raise TypeError(
                f"Non-integer as 1-based FOV! {self.get} (type"
                f" {type(self.get).__name__})"
            )
        if self.get < 1:
            raise ValueError(f"1-based FOV view must be positive int; got {self.get}")


@dataclass(frozen=True, order=True)
class ImagingChannel:
    """An imaging channel.

    Parameters
    ----------
    get : int
        Wrapped value.

    """

    get: int

    def __post_init__(self) -> None:
        if not _is_int(self.get):
            raise TypeError(
                f"Imaging channel must be integer, not {type(self.get).__name__}"
            )
        if self.get < 0:
            raise ValueError(f"Imaging channel must be nonnegative; got {self.get}")


@dataclass(frozen=True, order=True)
class NucleusNumber:
    """Wrap an int as a 1-based nucleus number.

    Parameters
    ----------
    get : int
        The value to wrap.

    Raises
    ------
    TypeError
        If the given value to wrap isn't an integer.
    ValueError
        If the given value to wrap isn't positive.

    """

    get: int

    def __post_init__(self) -> None:
        if not _is_int(self.get):
            raise TypeError(
                f"Non-integer as nucleus number! {self.get} (type"
                f" {type(self.get).__name__})"
            )
        if self.get < 1:
            raise ValueError(f"Nucleus number must be positive int; got {self.get}")


@dataclass(frozen=True, order=True)
class TimepointFrom0:
    """Wrap an int as a 0-based timepoint.

    Parameters
    ----------
    get : int
        The value to wrap.

    Raises
    ------
    TypeError
        If the given value to wrap isn't an integer.
    ValueError
        If the given value to wrap is negative.

    """

    get: int

    def __post_init__(self) -> None:
        if not _is_int(self.get):
            raise TypeError(
                f"Non-integer as timepoint! {self.get} (type {type(self.get).__name__})"
            )
        if self.get < 0:
            raise ValueError(f"Timepoint must be nonnegative int; got {self.get}")


@dataclass(frozen=True, order=True)
class TraceIdFrom0:
    """Wrap an int as a 0-based trace ID.

    Parameters
    ----------
    get : int
        The value to wrap.

    Raises
    ------
    TypeError
        If the given value to wrap isn't an integer.
    ValueError
        If the given value to wrap is negative.

    """

    get: int

    def __post_init__(self) -> None:
        if not _is_int(self.get):
            raise TypeError(
                f"Non-integer as trace ID! {self.get} (type {type(self.get).__name__})"
            )
        if self.get < 0:
            raise ValueError(f"Trace ID must be nonnegative int; got {self.get}")
