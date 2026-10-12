"""Tests for FOV sort key determination"""

import pytest

from gertils.pathtools import find_multiple_paths_by_fov, find_single_path_by_fov, get_fov_sort_key
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


@pytest.mark.parametrize(
    ("filename", "extension", "expected"),
    [
        ("P0012.nd2", ".nd2", FieldOfViewFrom1(12)),
        ("P0002.nd2", ".nd2", FieldOfViewFrom1(2)),
        ("P0022.nd2", ".nd2", FieldOfViewFrom1(22)),
        ("P0013.nd2", ".nd2", FieldOfViewFrom1(13)),
        ("P0015.h5", ".h5", FieldOfViewFrom1(15)),
    ],
)
def test_extension_with_digits_leaves_fov_digits_intact(filename, extension, expected):
    assert get_fov_sort_key(filename, extension=extension) == expected


def test_only_one_leading_p_is_removed():
    assert get_fov_sort_key("PP0001.zarr", extension=".zarr") is None


def test_double_zarr_extension_is_parsed_with_deprecation_warning():
    with pytest.warns(DeprecationWarning, match="Stripping second '.zarr' extension"):
        assert get_fov_sort_key("P0003.zarr.zarr", extension=".zarr") == FieldOfViewFrom1(3)


def test_find_multiple_paths_by_fov_keeps_fovs_apart_for_extension_with_digits(tmp_path):
    for name in ["P0001.nd2", "P0012.nd2"]:
        (tmp_path / name).touch()
    assert find_multiple_paths_by_fov(tmp_path, extensions=[".nd2"]) == {
        FieldOfViewFrom1(1): [tmp_path / "P0001.nd2"],
        FieldOfViewFrom1(12): [tmp_path / "P0012.nd2"],
    }


def test_find_single_path_by_fov_keeps_fovs_apart_for_extension_with_digits(tmp_path):
    for name in ["P0001.nd2", "P0002.nd2", "P0012.nd2"]:
        (tmp_path / name).touch()
    assert find_single_path_by_fov(tmp_path, extension=".nd2") == {
        FieldOfViewFrom1(1): tmp_path / "P0001.nd2",
        FieldOfViewFrom1(2): tmp_path / "P0002.nd2",
        FieldOfViewFrom1(12): tmp_path / "P0012.nd2",
    }
