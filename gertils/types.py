"""Data types commonly used around this package"""

from dataclasses import dataclass
from pathlib import Path
from typing import Union

import dask.array as da
import numpy as np
import numpy.typing as npt
from numpydoc_decorator import doc  # type: ignore[import]

CsvRow = list[str]
LayerParams = dict
PathLike = Union[str, Path]
PathOrPaths = Union[PathLike, list[PathLike]]
PixelValue = Union[np.uint8, np.uint16]
PixelArray = Union[npt.NDArray[PixelValue], da.Array]


@doc(
    summary="Wrap an int as a 1-based field of view (FOV).",
    parameters=dict(get="The value to wrap"),
    raises=dict(
        TypeError="If the given value to wrap isn't an integer",
        ValueError="If the given value to wrap isn't positive",
    ),
)
@dataclass(frozen=True, order=True)
class FieldOfViewFrom1:  # noqa: D101
    get: int

    def __post_init__(self) -> None:
        if not isinstance(self.get, int):
            raise TypeError(
                f"Non-integer as 1-based FOV! {self.get} (type" f" {type(self.get).__name__})"
            )
        if self.get < 1:
            raise ValueError(f"1-based FOV view must be positive int; got {self.get}")


@doc(summary="An imaging channel", parameters=dict(get="Wrapped value"))
@dataclass(frozen=True, order=True)
class ImagingChannel:  # noqa: D101
    get: int

    def __post_init__(self) -> None:
        if not isinstance(self.get, int):
            raise TypeError(f"Imaging channel must be integer, not {type(self.get).__name__}")
        if self.get < 0:
            raise ValueError(f"Imaging channel must be nonnegative; got {self.get}")


@doc(
    summary="Wrap an int as a 1-based nucleus number.",
    parameters=dict(get="The value to wrap"),
    raises=dict(
        TypeError="If the given value to wrap isn't an integer",
        ValueError="If the given value to wrap isn't positive",
    ),
)
@dataclass(frozen=True, order=True)
class NucleusNumber:  # noqa: D101
    get: int

    def __post_init__(self) -> None:
        if not isinstance(self.get, int):
            raise TypeError(
                f"Non-integer as nucleus number! {self.get} (type" f" {type(self.get).__name__})"
            )
        if self.get < 1:
            raise ValueError(f"Nucleus number must be positive int; got {self.get}")


@doc(
    summary="Wrap an int as a 0-based timepoint.",
    parameters=dict(get="The value to wrap"),
    raises=dict(
        TypeError="If the given value to wrap isn't an integer",
        ValueError="If the given value to wrap is negative",
    ),
)
@dataclass(frozen=True, order=True)
class TimepointFrom0:  # noqa: D101
    get: int

    def __post_init__(self) -> None:
        if not isinstance(self.get, int):
            raise TypeError(
                f"Non-integer as timepoint! {self.get} (type {type(self.get).__name__})"
            )
        if self.get < 0:
            raise ValueError(f"Timepoint must be nonnegative int; got {self.get}")


@doc(
    summary="Wrap an int as a 0-based trace ID.",
    parameters=dict(get="The value to wrap"),
    raises=dict(
        TypeError="If the given value to wrap isn't an integer",
        ValueError="If the given value to wrap is negative",
    ),
)
@dataclass(frozen=True, order=True)
class TraceIdFrom0:  # noqa: D101
    get: int

    def __post_init__(self) -> None:
        if not isinstance(self.get, int):
            raise TypeError(f"Non-integer as trace ID! {self.get} (type {type(self.get).__name__})")
        if self.get < 0:
            raise ValueError(f"Trace ID must be nonnegative int; got {self.get}")
