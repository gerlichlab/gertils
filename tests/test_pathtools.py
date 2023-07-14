"""Tests for core utilities for working with paths"""

from pathlib import Path
from typing import *

import pytest

from gertils import pathtools

__author__ = "Vince Reuter"
__email__ = "vincent.reuter@imba.oeaw.ac.at"


PATH_PREPARATIONS = {
    pathtools.ExtantFile: (lambda p: p.write_text("", encoding="utf-8")),
    pathtools.ExtantFolder: (lambda p: p.mkdir()),
    pathtools.NonExtantPath: (lambda p: p),
}


class MyWrapper(pathtools.PathWrapper):
    """Dummy subtype of the path wrapper, just to prove properties for invalid subtype"""


@pytest.mark.parametrize("wrapper", [pathtools.PathWrapper, MyWrapper])
def test_path_wrapper_cannot_be_instantiated(wrapper):
    with pytest.raises(TypeError) as error_context:
        wrapper(Path.cwd())
    assert str(error_context.value) == get_exp_anc_err_msg(wrapper)


@pytest.mark.parametrize(["wrap_type", "prepare_path"], PATH_PREPARATIONS.items())
def test_path_wrapper_subtypes_provide_path_attribute_access(
    tmp_path,
    wrap_type,
    prepare_path,
):
    path = tmp_path / "my-awesome-path"
    prepare_path(path)
    assert wrap_type(path).path == path


@pytest.mark.parametrize(["wrap_type", "prepare_path"], PATH_PREPARATIONS.items())
def test_path_wrapper_subtypes_rountrip_through_string(
    tmp_path, prepare_path, wrap_type
):
    path = tmp_path / "my-awesome-path"
    prepare_path(path)
    wrapper = wrap_type(path)
    assert wrap_type.from_string(wrapper.to_string()) == wrapper


@pytest.mark.parametrize(
    ["from_tmp_path", "wrap_type", "message_prefix"],
    [
        (lambda p: p, pathtools.ExtantFile, "Not an extant file"),
        (
            lambda p: p / "bogus_subfolder",
            pathtools.ExtantFolder,
            "Not an extant folder",
        ),
        (lambda p: p, pathtools.NonExtantPath, "Path already exists"),
    ],
)
def test_path_wrapper_subtypes_invalidation(
    tmp_path, from_tmp_path, wrap_type, message_prefix
):
    path = from_tmp_path(tmp_path)
    with pytest.raises(TypeError) as error_context:
        wrap_type(path)
    assert str(error_context.value) == f"{message_prefix}: {path}"


def get_exp_anc_err_msg(wrapper: Type) -> str:
    return f"Can't instantiate abstract class {wrapper.__name__} with abstract method _invalidate"
