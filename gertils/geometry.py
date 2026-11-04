"""Geometric types and tools"""

from dataclasses import dataclass
from typing import Union, cast

import numpy as np

ZCoordinate = Union[int, float, np.float64]  # int to accommodate notion of "z-slice"


@dataclass(kw_only=True, frozen=True)
class ImagePoint2D:
    """Bundle x and y position to create point in 2D space.

    Parameters
    ----------
    x : float
        Position in x.
    y : float
        Position in y.

    """

    x: float
    y: float

    def __post_init__(self) -> None:
        if not all(isinstance(c, float) for c in [self.x, self.y]):
            raise TypeError(f"At least one coordinate isn't floating-point! {self}")
        if any(c < 0 for c in [self.x, self.y]):
            raise ValueError(f"At least one coordinate is negative! {self}")


@dataclass(kw_only=True, frozen=True)
class ImagePoint3D(ImagePoint2D):
    """Bundle x, y and z position to create point in 3D space.

    Parameters
    ----------
    x : float
        Position in x.
    y : float
        Position in y.
    z : int or float or float64
        Position in z.

    See Also
    --------
    ImagePoint2D : Simpler, non-z implementation of an image point.

    """

    z: ZCoordinate

    def __post_init__(self) -> None:
        super().__post_init__()
        # Checked at runtime, since callers may pass any type despite the annotation.
        # np.float64 is a subclass of float. A bool is an int to Python, but True
        # would otherwise place the point at z = 1.
        if isinstance(self.z, bool) or not isinstance(
            cast("object", self.z), int | float
        ):
            raise TypeError(f"Bad z ({type(self.z).__name__}): {self.z}")
        if self.z < 0:
            raise ValueError(f"z-coordinate is negative! {self}")
