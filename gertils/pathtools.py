"""Tools for working with paths"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import *
from typing import Any

__all__ = ["ExtantFile", "ExtantFolder", "NonExtantPath", "PathWrapperException"]
__author__ = "Vince Reuter"
__email__ = "vincent.reuter@imba.oeaw.ac.at"


PW = TypeVar("PW", bound="PathWrapper")


@dataclass
class PathWrapper(ABC):
    """A Wrapper around a path that does some sort of validation"""

    path: Path

    @abstractmethod
    def _invalidate(self) -> None:
        pass

    def __post_init__(self) -> None:
        if not isinstance(self.path, Path):
            raise TypeError(f"Not a path, but {type(self.path).__name__}: {self.path}")
        self._invalidate()

    def __setattr__(self, __name: str, __value: Any) -> None:  # type: ignore[misc]
        result = super().__setattr__(__name, __value)
        self.__post_init__()
        return result

    @classmethod
    def from_string(cls: Type[PW], rawpath: str) -> PW:
        """Attempt to parse an instance from a raw string."""
        try:
            return cls(Path(rawpath))
        except Exception as exc:
            raise PathWrapperException(exc) from exc

    def to_string(self) -> str:
        """Return a string representation of this wrapped value."""
        return str(self.path)


class PathWrapperException(Exception):
    """Exception subtype for working with paths with a particular property"""

    def __init__(self, original_exception: Exception) -> None:
        super().__init__(str(original_exception))
        self.original = original_exception


class ExtantFile(PathWrapper):
    """Wrapper around a path that validates it as a file which exists"""

    def _invalidate(self) -> None:
        if not self.path.is_file():
            raise TypeError(f"Not an extant file: {self.path}")


class ExtantFolder(PathWrapper):
    """Wrapper around a path that validates it as a folder which exists"""

    def _invalidate(self) -> None:
        if not self.path.is_dir():
            raise TypeError(f"Not an extant folder: {self.path}")


class NonExtantPath(PathWrapper):
    """Wrapper around a path that validates it as nonexistent"""

    def _invalidate(self) -> None:
        if self.path.exists():
            raise TypeError(f"Path already exists: {self.path}")
