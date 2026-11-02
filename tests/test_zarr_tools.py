"""Tests for reading ZARR data"""

import json

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


@pytest.mark.parametrize("zarr_format", [2, 3])
def test_read_zarr_rejects_a_group_without_array(tmp_path, zarr_format):
    root = tmp_path / "img.zarr"
    zarr.open_group(str(root), mode="w", zarr_format=zarr_format)
    with pytest.raises(ZarrParseException, match="Failed to find an array's"):
        read_zarr(root)


def test_read_zarr_takes_a_folder_for_what_its_zarr_json_says(tmp_path):
    # A format-3 group whose folder still has the .zarray of an array that was there
    # before. zarr takes the zarr.json over the .zarray, so the array is the one at "0".
    data = _data()
    root = tmp_path / "img.zarr"
    group = zarr.open_group(str(root), mode="w", zarr_format=3)
    group.create_array("0", data=data)
    old_array = tmp_path / "old.zarr"
    zarr.create_array(str(old_array), data=data + 1, zarr_format=2)
    (root / ".zarray").write_bytes((old_array / ".zarray").read_bytes())
    with pytest.warns(UserWarning, match="Both zarr.json"):
        result = read_zarr(root)
    np.testing.assert_array_equal(result, data)


@pytest.mark.parametrize(
    "rewrite",
    [
        # Non-ASCII text in UTF-8, as writers that don't escape it to ASCII store it.
        lambda raw: json.dumps(
            {**json.loads(raw), "attributes": {"label": "Á"}}, ensure_ascii=False
        ).encode("utf-8"),
        # A UTF-8 byte order mark, which JSON parsers skip.
        lambda raw: b"\xef\xbb\xbf" + raw,
    ],
    ids=["non-ascii-text", "byte-order-mark"],
)
def test_read_zarr_reads_metadata_that_zarr_reads(tmp_path, rewrite):
    data = _data()
    root = tmp_path / "img.zarr"
    zarr.create_array(str(root), data=data, zarr_format=3)
    metadata = root / "zarr.json"
    metadata.write_bytes(rewrite(metadata.read_bytes()))
    np.testing.assert_array_equal(read_zarr(root), data)


@pytest.mark.parametrize(
    ("metadata_file", "zarr_format"), [("zarr.json", 3), (".zarray", 2)]
)
@pytest.mark.parametrize(
    "content", [b"{not json", b"[]", b""], ids=["cut-off", "not-an-object", "empty"]
)
@pytest.mark.parametrize("subfolder", ["", "0"])
def test_read_zarr_rejects_damaged_metadata(
    tmp_path, metadata_file, zarr_format, content, subfolder
):
    root = tmp_path / "img.zarr"
    if subfolder:
        zarr.open_group(str(root), mode="w", zarr_format=zarr_format)
    folder = root / subfolder
    folder.mkdir(parents=True, exist_ok=True)
    (folder / metadata_file).write_bytes(content)
    with pytest.raises(ZarrParseException, match="Failed to read zarr metadata"):
        read_zarr(root)
