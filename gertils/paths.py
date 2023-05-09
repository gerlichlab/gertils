"""General utilities for working with paths"""

from pathlib import Path
from typing import *

__author__ = "Vince Reuter"
__email__ = "vincent.reuter@imba.oeaw.ac.at"

__all__ = ["IllegalExperimentNumberException", "get_experiment_path"]


GROUPS_HOME = Path("/groups")
EXPERIMENT_NUMBER_CHARACTER_COUNT = 6

OptPath = Optional[Union[str, Path]]


class IllegalExperimentNumberException(Exception):
    """Error type for when an experiment number is illegal."""

    def __init__(self, exp_num: int, message: str):
        super(IllegalExperimentNumberException, self).__init__(message)
        self._exp_num = exp_num

    @property
    def number(self) -> int:
        """Return the experiment number underlying this exception"""
        return self._exp_num


def get_experiment_path(
    exp: int, groups_home: OptPath = None, must_exist: bool = True
) -> Path:
    """Get the filepath to the folder associated with given experiment."""
    if exp < 0:
        raise IllegalExperimentNumberException(
            exp_num=exp, message=f"Negative experiment number: {exp}"
        )
    if len(str(exp)) > EXPERIMENT_NUMBER_CHARACTER_COUNT:
        raise IllegalExperimentNumberException(
            exp_num=exp,
            message=f"Impossible to represent given experiment number with {EXPERIMENT_NUMBER_CHARACTER_COUNT} characters: {exp}",
        )
    idx = _get_experiment_index(exp)
    idx_str = str(idx).zfill(EXPERIMENT_NUMBER_CHARACTER_COUNT)
    branch = f"Experiments_{idx_str}"
    path = _experiments_folder_path(groups_home=groups_home) / branch / idx_str
    if must_exist and not path.is_dir():
        msg = f"Folder path ({path}) isn't a directory for experiment: {exp}"
        raise IllegalExperimentNumberException(exp_num=exp, message=msg)
    return path


def _experiments_folder_path(groups_home: OptPath = None) -> Path:
    """Get the path for the group's shared storage experiments folder."""
    return _group_home_path(groups_home=groups_home) / "experiments"


def _get_experiment_index(exp: int) -> int:
    return 100 * (exp // 100)


def _group_home_path(groups_home: OptPath = None) -> Path:
    """Get the path to the group's shared storage home folder."""
    if isinstance(groups_home, str):
        groups_home = Path(groups_home)
    elif not groups_home:
        groups_home = GROUPS_HOME
    return groups_home / "gerlich"
