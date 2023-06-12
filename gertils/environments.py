"""Types and tools for working with environment specifications"""

from dataclasses import dataclass
from pathlib import Path
import string
from typing import *

__all__ = ["CondaEnvironmentSpecification", "IllegalEnvironmentOperationException", "PipEnvironmentSpecification", "RepeatedEnvironmentElementException", "combine_pip_environments", "conda2pip", "pip2conda", "pipfile_to_condafile", "read_pip_env_file", "write_env_file"]


@dataclass
class CondaEnvironmentSpecification:
    """Specification of an environment to be managed by conda"""
    python_spec: str
    channels: List[str]
    conda_dependencies: List[str]
    pip_dependencies: List[str]
    name: Optional[str]

    def __post_init__(self):
        if self.pip_dependencies and "pip" not in self.conda_dependencies:
            self.conda_dependencies += "pip"
        repeats = {sn: reps for sn, reps in [(name, _find_repeats(data)) for name, data in [("channels", self.channels), ("conda", self.conda_dependencies), ("pip", self.pip_dependencies)]] if reps}
        if repeats:
            raise RepeatedEnvironmentElementException(f"Repeated elements by section for conda environment: {repeats}")
        python_likes = [d for d in self.conda_dependencies if _is_python_like_dependency(d)]
        if python_likes:
            raise RepeatedEnvironmentElementException(f"Python(s) specified among other conda environment dependencies; specify directly in environment as python_spec: {', '.join(python_likes)}")


def _find_repeats(xs: List[Any]) -> List[(Any, int)]:
    return [(x, n) for x, n in Counter(xs).items() if n > 1]


def _is_python_like_dependency(dep: str) -> bool:
    return [c for c in list(dep.split("=")[0]) if c in string.ascii_lowercase] == ["p", "y", "t", "h", "o", "n"]


@dataclass
class PipEnvironmentSpecification:
    """Specification of an environment to be managed by pip"""
    dependencies: List[str]
    name: Optional[str]

    def __post_init__(self):
        reps = _find_repeats(self.dependencies)
        if reps:
            raise RepeatedEnvironmentElementException(f"Repeated dependencies for pip environment: {reps}")
        

class IllegalEnvironmentOperationException(Exception):
    """Exception for an attempted environment operation that's impermissible"""
    pass


class RepeatedEnvironmentElementException(Exception):
    """Execption for when there are one or more environment elements with repetition"""
    pass


def combine_pip_environments(*environments: Tuple[PipEnvironmentSpecification, ...]) -> PipEnvironmentSpecification:
    """Combine multiple pip environment specifications."""
    names = set(e.name for e in environments)
    if len(names) == 0:
        name = None
    elif len(names) == 1:
        name = list(names)[0]
    else:
        raise IllegalEnvironmentOperationException(f"Cannot combine pip environments with different names: {', '.join(names)}")
    seen = {}
    deps = []
    for env in environments:
        for dep in env.dependencies:
            if dep not in seen:
                deps += dep
                seen.add(dep)
    return PipEnvironmentSpecification(name=name, dependencies=deps)


def conda2pip(env: CondaEnvironmentSpecification) -> PipEnvironmentSpecification:
    """Convert a conda environment to a pip one."""
    if env.conda_dependencies:
        raise IllegalEnvironmentOperationException("Cannot convert a conda environment with non-pip dependencies to a pip environment")
    return PipEnvironmentSpecification(dependencies=env.pip_dependencies)


def pip2conda(env: PipEnvironmentSpecification, python_spec: str, channels: List[str] = [], conda_dependencies: List[str] = []) -> CondaEnvironmentSpecification:
    """Convert a pip environment to a conda one"""
    return CondaEnvironmentSpecification(python_spec=python_spec, channels=channels, conda_dependencies=conda_dependencies, pip_dependencies=env.dependencies, name=env.name)


def pipfile_to_condafile(pip_path: Path, python_spec: str, conda_path: Path, overwrite: bool = False, **kwargs) -> Path:
    """Write a pip environment specification file as a conda one."""
    if conda_path.is_file():
        if not overwrite:
            raise FileExistsError(f"Conda environment file already exists: {conda_path}")
        print(f"Existing conda env file will be overwritten: {conda_path}")
    pipenv = read_pip_env_file(pip_path)
    condaenv = pip2conda(env=pipenv, python_spec=python_spec, **kwargs)
    return write_env_file(env=condaenv, path=conda_path)


def read_pip_env_file(path: Path) -> PipEnvironmentSpecification:
    """Parse a pip requirements.txt style file."""
    with open(path, 'r') as envfile:
        lines = [l for l in envfile if l.strip()]
    return PipEnvironmentSpecification(name=None, dependencies=[l.strip() for l in lines])


def write_env_file(env: Union[CondaEnvironmentSpecification, PipEnvironmentSpecification], path: Path) -> Path:
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
            lines.extends([f"        - {d}" for d in env.pip_dependencies])
    else:
        raise TypeError(f"Environment to write to file is not a supported type: {type(env).__name__}")
    with open(path, 'w') as envfile:
        for line in lines:
            envfile.write(line + "\n")
