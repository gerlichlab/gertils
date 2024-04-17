"""Tests for FOV sort key determination"""

import pytest

from gertils.pathtools import get_fov_sort_key
from gertils.types import FieldOfViewFrom1


@pytest.mark.parametrize(
    ("folder", "extension", "expected"),
    [
        ("P0001.zarr", ".zarr", FieldOfViewFrom1(1)),
        ("P0001.zarr", "zarr", None),
        ("P0002.zarr", ".zarr", FieldOfViewFrom1(2)),
        ("P0001.zarr", ".csv", None),
    ],
)
def test_simple_zarr_folder_sort_keys(tmp_path, folder, extension, expected):
    arg = tmp_path / folder
    arg.mkdir()
    assert arg.is_dir()
    assert get_fov_sort_key(arg, extension=extension) == expected
