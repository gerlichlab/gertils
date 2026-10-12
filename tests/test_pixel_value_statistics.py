"""Tests for statistics over pixel values"""

import dask.array as da
import numpy as np
import pytest

from gertils.geometry import ImagePoint3D
from gertils.pixel_value_statistics import RegionalPixelStatistics, compute_pixel_statistics
from gertils.types import ImagingChannel


def stack_of_indexed_planes(num_planes):
    """Build a z-stack in which every pixel of plane i has the value i."""
    return np.stack([np.full((4, 4), i, dtype=np.uint16) for i in range(num_planes)])


@pytest.mark.parametrize(
    ("num_planes", "central_z", "expected_planes"),
    [
        (10, 5, [4, 5, 6]),
        (10, 9, [8, 9]),
        (10, 0, [0, 1]),
        (10, 0.3, [0, 1]),
        (3, 0, [0, 1]),
        (2, 0, [0, 1]),
    ],
)
def test_z_window_is_truncated_at_the_edges_of_the_stack(num_planes, central_z, expected_planes):
    stats = RegionalPixelStatistics.from_image(
        stack_of_indexed_planes(num_planes), central_z=central_z
    )
    assert (stats.center_min, stats.center_max, stats.center_mean) == (
        min(expected_planes),
        max(expected_planes),
        np.mean(expected_planes),
    )


def test_z_window_below_plane_0_is_rejected_when_full_padding_is_required():
    with pytest.raises(ValueError, match=r"\[-1, 2\) slice for image of 10 z-slices"):
        RegionalPixelStatistics.from_image(
            stack_of_indexed_planes(10), central_z=0, require_full_padding=True
        )


def test_compute_pixel_statistics_for_point_in_bottom_plane():
    img = stack_of_indexed_planes(10)[np.newaxis]
    (record,) = compute_pixel_statistics(
        img,
        ImagePoint3D(x=2.0, y=2.0, z=0.3),
        channels=[ImagingChannel(0)],
        diameter=2,
        channel_column="channel",
    )
    assert (record["center_min"], record["center_max"]) == (0, 1)


def test_compute_pixel_statistics_gives_the_same_records_for_dask_and_numpy_input():
    img = np.random.default_rng(0).integers(0, 1000, size=(2, 6, 40, 40), dtype=np.uint16)
    kwargs = {
        "pt": ImagePoint3D(x=17.3, y=22.8, z=3.0),
        "channels": [ImagingChannel(0), ImagingChannel(1)],
        "diameter": 8,
        "channel_column": "channel",
    }
    from_numpy = compute_pixel_statistics(img, **kwargs)
    from_dask = compute_pixel_statistics(da.from_array(img, chunks=(1, 2, 20, 20)), **kwargs)
    assert not any(isinstance(value, da.Array) for record in from_dask for value in record.values())
    assert from_dask == from_numpy
