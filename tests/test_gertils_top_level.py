"""Tests for package-level properties"""

import pytest

import gertils
from gertils import environments as envs_module
from gertils import group_paths as group_paths_module

__author__ = "Vince Reuter"


COLLECTIONS_PUBLIC_MEMBERS = ["count_repeats", "listify", "uniquify"]
EXCEPTIONS_PUBLIC_MEMBERS = [
    "GerlichToolsException",
    "IllegalExperimentNumberException",
    "TensorflowNotFoundException",
]
PATHTOOLS_PUBLIC_MEMBERS = [
    "ExtantFile",
    "ExtantFolder",
    "NonExtantPath",
    "PathWrapperException",
]


@pytest.mark.parametrize(
    ["member_name", "expected_presence"],
    [
        (name, True)
        for name in COLLECTIONS_PUBLIC_MEMBERS
        + EXCEPTIONS_PUBLIC_MEMBERS
        + PATHTOOLS_PUBLIC_MEMBERS
    ]
    + [(name, False) for name in envs_module.__all__ + group_paths_module.__all__],
)
def test_import_visibility(member_name, expected_presence):
    observed_presence = member_name in dir(gertils)
    assert observed_presence == expected_presence
