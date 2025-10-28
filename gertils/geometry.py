"""Geometric types and tools"""

from dataclasses import dataclass
from typing import Union

import numpy as np
from numpydoc_decorator import doc  # type: ignore[import]

ZCoordinate = Union[int, float, np.float64]  # int to accommodate notion of "z-slice"


@doc(
    summary="Bundle x and y position to create point in 2D space.",
    parameters=dict(
        x="Position in x",
        y="Position in y",
    ),
)
@dataclass(kw_only=True, frozen=True)
class ImagePoint2D:  # noqa: D101
    x: float
    y: float

    def __post_init__(self) -> None:
        if not all(isinstance(c, float) for c in [self.x, self.y]):
            raise TypeError(f"At least one coordinate isn't floating-point! {self}")
        if any(c < 0 for c in [self.x, self.y]):
            raise ValueError(f"At least one coordinate is negative! {self}")


@doc(
    summary="Bundle x and y position to create point in 2D space.",
    parameters=dict(
        x="Position in x",
        y="Position in y",
        z="Position in z",
    ),
    see_also=dict(
        ImagePoint2D="Simpler, non-z implementation of an image point",
    ),
)
@dataclass(kw_only=True, frozen=True)
class ImagePoint3D(ImagePoint2D):  # noqa: D101
    z: ZCoordinate

    def __post_init__(self) -> None:
        super().__post_init__()
        if not isinstance(self.z, int | float | np.float64):
            raise TypeError(f"Bad z ({type(self.z).__name__}: {self.z}")
        if self.z < 0:
            raise ValueError(f"z-coordinate is negative! {self}")
