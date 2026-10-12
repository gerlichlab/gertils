"""Tests for reading ZARR data"""

import numpy as np
import pytest
import zarr

from gertils.zarr_tools import ZarrParseException, read_zarr


@pytest.mark.parametrize("subfolder", ["", "0"])
def test_read_zarr_returns_the_stored_array(tmp_path, subfolder):
    data = np.random.default_rng(0).integers(0, 1000, size=(2, 3, 4), dtype=np.uint16)
    root = tmp_path / "img.zarr"
    zarr.save_array(str(root / subfolder), data)
    result = read_zarr(root)
    assert isinstance(result, np.ndarray)
    assert result.dtype == data.dtype
    np.testing.assert_array_equal(result, data)


def test_read_zarr_rejects_a_folder_without_array(tmp_path):
    with pytest.raises(ZarrParseException, match="Failed to find .zarray"):
        read_zarr(tmp_path)
