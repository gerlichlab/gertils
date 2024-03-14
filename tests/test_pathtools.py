# mypy: disable-error-code=no-any-return

"""Tests for core utilities for working with paths"""

from dataclasses import FrozenInstanceError, dataclass
from pathlib import Path
from typing import *

import pytest

from gertils import pathtools

__author__ = "Vince Reuter"
__email__ = "vincent.reuter@imba.oeaw.ac.at"


# How to prepare a valid input for each path wrapper type, using the pytest temp path fixture.
PATH_PREPARATIONS = {
    pathtools.ExtantFile: (lambda p: p.write_text("", encoding="utf-8")),
    pathtools.ExtantFolder: (lambda p: p.mkdir()),
    pathtools.NonExtantPath: (lambda p: p),
}


@dataclass
class InvalidationParameterisation:
    """A parameterisation of an invalidation workflow and assertion for each path wrapper type"""

    from_tmp_path: Callable[[Path], Path]
    wrap_type: Type
    exp_err_msg_prefix: str


# An invalidation scheme for each of the path wrapper types
INVALIDATION_PARAMETERISATIONS = [
    InvalidationParameterisation(
        lambda p: p, pathtools.ExtantFile, "Not an extant file"
    ),
    InvalidationParameterisation(
        lambda p: p / "bogus_subfolder", pathtools.ExtantFolder, "Not an extant folder"
    ),
    InvalidationParameterisation(
        lambda p: p, pathtools.NonExtantPath, "Path already exists"
    ),
]


class MyWrapper(pathtools.PathWrapper):
    """Dummy subtype of the path wrapper, just to prove properties for invalid subtype"""


@pytest.mark.parametrize("wrapper", [pathtools.PathWrapper, MyWrapper])
def test_path_wrapper_cannot_be_instantiated(wrapper):
    with pytest.raises(TypeError) as error_context:
        wrapper(Path.cwd())
    obs_err_msg = str(error_context.value)
    # The error message should mention impossibility of instantiating an abstract class.
    assert obs_err_msg.startswith(
        f"Can't instantiate abstract class {wrapper.__name__}"
    )
    # The error message should mention the abstract method.
    assert "_invalidate" in obs_err_msg


@pytest.mark.parametrize(
    "parameterisation", INVALIDATION_PARAMETERISATIONS, ids=lambda p: p.wrap_type
)
def test_path_wrapper_subtypes_invalidation(tmp_path, parameterisation):
    path = parameterisation.from_tmp_path(tmp_path)
    with pytest.raises(pathtools.PathWrapperException) as error_context:
        parameterisation.wrap_type(path)
    assert str(error_context.value) == f"{parameterisation.exp_err_msg_prefix}: {path}"


@pytest.mark.parametrize(
    "parameterisation", INVALIDATION_PARAMETERISATIONS, ids=lambda p: p.wrap_type
)
def test_path_wrapper_immutability(tmp_path, parameterisation):
    prepare_path = PATH_PREPARATIONS[
        parameterisation.wrap_type
    ]  # Use the legitimate preparation here.
    good_path = tmp_path / "my-awesome-path"
    prepare_path(good_path)
    wrapper = parameterisation.wrap_type(good_path)
    with pytest.raises(FrozenInstanceError) as error_context:
        wrapper.path = wrapper.path
    assert str(error_context.value) == "cannot assign to field 'path'"


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
def test_path_wrapper_subtypes_roundtrip_through_string(
    tmp_path, prepare_path, wrap_type
):
    path = tmp_path / "my-awesome-path"
    prepare_path(path)
    wrapper = wrap_type(path)
    assert wrap_type.from_string(wrapper.to_string()) == wrapper


def get_exp_anc_err_msg(wrapper: Type) -> str:
    return f"Can't instantiate abstract class {wrapper.__name__} with abstract method _invalidate"
