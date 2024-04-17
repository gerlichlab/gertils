"""Types and tools for working with environment specifications"""

import string
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

from .collection_extras import count_repeats, uniquify

__all__ = [
    "CondaEnvironmentSpecification",
    "IllegalEnvironmentOperationException",
    "PipEnvironmentSpecification",
    "RepeatedEnvironmentElementException",
    "combine_pip_environments",
    "conda2pip",
    "read_pip_env_file",
    "write_env_file",
]


@dataclass
class CondaEnvironmentSpecification:
    """Specification of an environment to be managed by conda"""

    python_spec: str
    channels: list[str]
    conda_dependencies: list[str]
    pip_dependencies: list[str]
    name: Optional[str]

    def __post_init__(self) -> None:
        if self.pip_dependencies and "pip" not in self.conda_dependencies:
            self.conda_dependencies += "pip"
        repeats = {
            sn: reps
            for sn, reps in [
                (name, count_repeats(data))
                for name, data in [
                    ("channels", self.channels),
                    ("conda", self.conda_dependencies),
                    ("pip", self.pip_dependencies),
                ]
            ]
            if reps
        }
        if repeats:
            raise RepeatedEnvironmentElementException(
                f"Repeated elements by section for conda environment: {repeats}"
            )
        python_likes = [d for d in self.conda_dependencies if _is_python_like_dependency(d)]
        if python_likes:
            raise RepeatedEnvironmentElementException(
                "Python(s) specified among other conda environment dependencies; "
                f"specify directly in environment as python_spec: {', '.join(python_likes)}"
            )


def _is_python_like_dependency(dep: str) -> bool:
    return [c for c in list(dep.split("=")[0]) if c in string.ascii_lowercase] == [
        "p",
        "y",
        "t",
        "h",
        "o",
        "n",
    ]


@dataclass
class PipEnvironmentSpecification:
    """Specification of an environment to be managed by pip"""

    dependencies: list[str]
    name: Optional[str]

    def __post_init__(self) -> None:
        reps = count_repeats(self.dependencies)
        if reps:
            raise RepeatedEnvironmentElementException(
                f"Repeated dependencies for pip environment: {reps}"
            )


class IllegalEnvironmentOperationException(Exception):
    """Exception for an attempted environment operation that's impermissible"""


class RepeatedEnvironmentElementException(Exception):
    """Exception for when there are one or more environment elements with repetition"""


def combine_pip_environments(
    *environments: PipEnvironmentSpecification,
) -> PipEnvironmentSpecification:
    """Combine multiple pip environment specifications."""
    names = {e.name for e in environments if e.name}
    if len(names) > 1:
        raise IllegalEnvironmentOperationException(
            f"Cannot combine pip environments with different names: {', '.join(names)}"
        )
    try:
        name = next(iter(names))
    except StopIteration:
        name = None
    deps = list(uniquify(dep for env in environments for dep in env.dependencies))
    return PipEnvironmentSpecification(name=name, dependencies=deps)


def conda2pip(env: CondaEnvironmentSpecification) -> PipEnvironmentSpecification:
    """Convert a conda environment to a pip one."""
    if env.conda_dependencies:
        raise IllegalEnvironmentOperationException(
            "Cannot convert a conda environment with non-pip dependencies to a pip environment"
        )
    return PipEnvironmentSpecification(dependencies=env.pip_dependencies, name=env.name)


def read_pip_env_file(path: Path) -> PipEnvironmentSpecification:
    """Parse a pip requirements.txt style file."""
    with path.open() as envfile:
        lines = [line for line in envfile if line.strip()]
    return PipEnvironmentSpecification(name=None, dependencies=[line.strip() for line in lines])


def write_env_file(
    env: Union[CondaEnvironmentSpecification, PipEnvironmentSpecification], path: Path
) -> Path:
    """Write an environment specification to a file."""
    if isinstance(env, PipEnvironmentSpecification):
        lines = env.dependencies
    elif isinstance(env, CondaEnvironmentSpecification):
        lines = []
        if env.name:
            lines += f"name: {env.name}"
        if env.channels:
            lines += "channels:"
            lines.extend([f"    - {c}" for c in env.channels])
        if env.conda_dependencies:
            lines += "dependencies:"
            lines.extend([f"    - {d}" for d in env.conda_dependencies])
        if env.pip_dependencies:
            lines += "    - pip:"
            lines.extend([f"        - {d}" for d in env.pip_dependencies])
    else:
        raise TypeError(
            f"Environment to write to file is not a supported type: {type(env).__name__}"
        )
    with path.open(mode="w") as envfile:
        for line in lines:
            envfile.write(line + "\n")
    return path
