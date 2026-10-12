"""Tests for package-level properties"""

import pytest

import gertils
from gertils import environments as envs_module

COLLECTIONS_PUBLIC_MEMBERS = ["count_repeats", "listify", "uniquify"]
PATHTOOLS_PUBLIC_MEMBERS = [
    "ExtantFile",
    "ExtantFolder",
    "NonExtantPath",
    "PathWrapperException",
]


@pytest.mark.parametrize(
    ("member_name", "expected_presence"),
    [(name, True) for name in PATHTOOLS_PUBLIC_MEMBERS]
    + [
        (name, True)
        for name in [
            "RegionalPixelStatistics",
            "compute_pixel_statistics",
            "compute_pixel_statistics_for_channel",
        ]
    ]
    + [(name, False) for name in envs_module.__all__ + COLLECTIONS_PUBLIC_MEMBERS],
)
def test_import_visibility(member_name, expected_presence):
    observed_presence = member_name in dir(gertils)
    assert observed_presence == expected_presence


def test_package_level_names_are_declared_public():
    assert sorted(gertils.__all__) == sorted(
        [
            *PATHTOOLS_PUBLIC_MEMBERS,
            "find_multiple_paths_by_fov",
            "find_single_path_by_fov",
            "get_fov_sort_key",
            "RegionalPixelStatistics",
            "compute_pixel_statistics",
            "compute_pixel_statistics_for_channel",
        ]
    )
    assert all(hasattr(gertils, name) for name in gertils.__all__)
