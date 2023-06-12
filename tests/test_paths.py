"""Tests for path utilities"""

from pathlib import Path
from string import ascii_letters as alphachars

import pytest
from hypothesis import given
from hypothesis import strategies as st

from gertils.paths import (
    EXPERIMENT_NUMBER_CHARACTER_COUNT,
    GROUPS_HOME,
    IllegalExperimentNumberException,
    _get_experiment_index,
    get_experiment_path,
)

__author__ = "Vince Reuter"
__email__ = "vincent.reuter@imba.oeaw.ac.at"


MAX_INT_REPRESENTABLE = int(pow(10, EXPERIMENT_NUMBER_CHARACTER_COUNT)) - 1

negative_integer = st.integers(max_value=-1)


def excessive_integer(inclusive_lower_bound: int = MAX_INT_REPRESENTABLE + 1):
    """Strategy for generating experiment number in excess of representable"""
    return st.integers(min_value=inclusive_lower_bound)


@given(experiment=st.one_of(negative_integer, excessive_integer()))
@pytest.mark.parametrize("groups_home", [None, Path("/test"), "/dummy"])
@pytest.mark.parametrize("must_exist", [False, True])
def test_get_experiment_path__out_of_bounds_value_is_always_exceptional(
    experiment, groups_home, must_exist
):
    with pytest.raises(IllegalExperimentNumberException) as err_ctx:
        get_experiment_path(
            exp=experiment, groups_home=groups_home, must_exist=must_exist
        )
    exp_msg_prefix = (
        "Negative experiment number"
        if experiment < 0
        else (
            f"Impossible to represent given experiment number "
            f"with {EXPERIMENT_NUMBER_CHARACTER_COUNT} characters"
        )
    )
    assert err_ctx.value.number == experiment
    assert f"{exp_msg_prefix}: {experiment}" == str(err_ctx.value)


@given(
    experiment=st.integers(min_value=0, max_value=MAX_INT_REPRESENTABLE),
    groups_home=st.one_of(st.text(min_size=1, alphabet=alphachars), st.none()),
)
@pytest.mark.parametrize("must_exist", [False, True])
def test_get_experiment_path__existence_check_flag_matters(
    experiment, groups_home, must_exist
):
    kwargs = {"exp": experiment, "must_exist": must_exist}
    if groups_home:
        kwargs["groups_home"] = groups_home
        exp_groups_home = Path(groups_home)
    else:
        exp_groups_home = GROUPS_HOME
    idx_str = str(_get_experiment_index(experiment)).zfill(
        EXPERIMENT_NUMBER_CHARACTER_COUNT
    )
    expected_path = (
        exp_groups_home / "gerlich" / "experiments" / f"Experiments_{idx_str}" / idx_str
    )
    if must_exist:
        with pytest.raises(IllegalExperimentNumberException) as err_ctx:
            get_experiment_path(**kwargs)
        assert err_ctx.value.number == experiment
        assert (
            str(err_ctx.value)
            == f"Folder path ({expected_path}) isn't a directory for experiment: {experiment}"
        )
    else:
        observed_path = get_experiment_path(**kwargs)
        assert observed_path == expected_path
