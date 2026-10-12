"""Tests for the geometric types"""

import numpy as np
import pytest

from gertils.geometry import ImagePoint2D, ImagePoint3D


@pytest.mark.parametrize(("x", "y"), [(-1.0, 0.0), (0.0, -1.0), (-0.5, -0.5)])
def test_negative_x_or_y_is_rejected(x, y):
    with pytest.raises(ValueError, match="At least one coordinate is negative"):
        ImagePoint2D(x=x, y=y)
    with pytest.raises(ValueError, match="At least one coordinate is negative"):
        ImagePoint3D(x=x, y=y, z=0.0)


@pytest.mark.parametrize("z", [-1, -0.5, np.float64(-2.0)])
def test_negative_z_is_rejected(z):
    with pytest.raises(ValueError, match="z-coordinate is negative"):
        ImagePoint3D(x=1.0, y=1.0, z=z)


@pytest.mark.parametrize("coordinate", [1, "1.0", None])
def test_x_and_y_must_be_floating_point(coordinate):
    with pytest.raises(TypeError, match="isn't floating-point"):
        ImagePoint2D(x=coordinate, y=1.0)
    with pytest.raises(TypeError, match="isn't floating-point"):
        ImagePoint3D(x=1.0, y=coordinate, z=0.0)


@pytest.mark.parametrize("z", ["1.0", None])
def test_z_must_be_a_number(z):
    with pytest.raises(TypeError, match="Bad z"):
        ImagePoint3D(x=1.0, y=1.0, z=z)


@pytest.mark.parametrize("z", [0, 2, 0.0, 2.5, np.float64(2.5)])
def test_valid_coordinates_are_accepted(z):
    point = ImagePoint3D(x=0.0, y=np.float64(1.5), z=z)
    assert (point.x, point.y, point.z) == (0.0, 1.5, z)
