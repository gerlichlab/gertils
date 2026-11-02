"""Tests for reading ZARR data"""

import numpy as np
import pytest
import zarr

from gertils.zarr_tools import ZarrParseException, read_zarr


def _data():
    return np.random.default_rng(0).integers(0, 1000, size=(2, 3, 4), dtype=np.uint16)


@pytest.mark.parametrize("zarr_format", [2, 3])
@pytest.mark.parametrize("subfolder", ["", "0"])
def test_read_zarr_returns_the_stored_array(tmp_path, subfolder, zarr_format):
    data = _data()
    root = tmp_path / "img.zarr"
    zarr.create_array(str(root / subfolder), data=data, zarr_format=zarr_format)
    result = read_zarr(root)
    assert isinstance(result, np.ndarray)
    assert result.dtype == data.dtype
    np.testing.assert_array_equal(result, data)


@pytest.mark.parametrize("zarr_format", [2, 3])
def test_read_zarr_returns_the_array_of_a_group(tmp_path, zarr_format):
    # An OME-Zarr store: a group, with the array at "0". In format 3, the group's
    # metadata is in a zarr.json, as an array's is.
    data = _data()
    root = tmp_path / "img.zarr"
    group = zarr.open_group(str(root), mode="w", zarr_format=zarr_format)
    group.create_array("0", data=data)
    np.testing.assert_array_equal(read_zarr(root), data)


def test_read_zarr_rejects_a_folder_without_array(tmp_path):
    with pytest.raises(ZarrParseException, match="Failed to find an array's"):
        read_zarr(tmp_path)


def test_read_zarr_rejects_a_group_without_array(tmp_path):
    root = tmp_path / "img.zarr"
    zarr.open_group(str(root), mode="w", zarr_format=3)
    with pytest.raises(ZarrParseException, match="Failed to find an array's"):
        read_zarr(root)
