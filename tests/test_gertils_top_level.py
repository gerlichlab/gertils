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
    + [(name, False) for name in envs_module.__all__ + COLLECTIONS_PUBLIC_MEMBERS],
)
def test_import_visibility(member_name, expected_presence):
    observed_presence = member_name in dir(gertils)
    assert observed_presence == expected_presence
