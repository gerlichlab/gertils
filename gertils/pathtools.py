"""Tools for working with paths"""

import os
import warnings
from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, TypeVar

from numpydoc_decorator import doc  # type: ignore[import]

from .types import FieldOfViewFrom1, PathLike

PW = TypeVar("PW", bound="PathWrapper")


@dataclass(frozen=True)
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

    @classmethod
    def from_string(cls: type[PW], rawpath: str) -> PW:
        """Attempt to parse an instance from a raw string."""
        return cls(Path(rawpath))

    def to_string(self) -> str:
        """Return a string representation of this wrapped value."""
        return str(self.path)


class PathWrapperException(Exception):
    """Exception subtype for working with paths with a particular property"""


class ExtantFile(PathWrapper):
    """Wrapper around a path that validates it as a file which exists"""

    def _invalidate(self) -> None:
        if not self.path.is_file():
            raise PathWrapperException(f"Not an extant file: {self.path}")


class ExtantFolder(PathWrapper):
    """Wrapper around a path that validates it as a folder which exists"""

    def _invalidate(self) -> None:
        if not self.path.is_dir():
            raise PathWrapperException(f"Not an extant folder: {self.path}")


class NonExtantPath(PathWrapper):
    """Wrapper around a path that validates it as nonexistent"""

    def _invalidate(self) -> None:
        if self.path.exists():
            raise PathWrapperException(f"Path already exists: {self.path}")


@doc(
    summary=(
        "Directly in given folder, find all filepaths with a field" " of view embedded in filename."
    ),
    parameters=dict(
        folder="Path to folder in which to find files",
        extensions="The file extensions to try to match",
    ),
    returns="Mapping from field of view to filepath",
    see_also=dict(
        find_single_path_by_fov="Similar function, for unique path by FOV, and particular extension",
        get_fov_sort_key="The function used to try to parse FOV from filename",
    ),
)
def find_multiple_paths_by_fov(  # noqa: D103
    folder: PathLike, *, extensions: Iterable[str]
) -> dict[str, list[Path]]:
    if isinstance(folder, str):
        folder = Path(folder)
    paths: dict[str, list[Path]] = {}
    for fn in os.listdir(folder):
        fp = folder / fn
        for ext in extensions:
            fov = get_fov_sort_key(fp, extension=ext)
            if fov is not None:
                paths.setdefault(fov, []).append(fp)
                break
    return paths


@doc(
    summary=(
        "Directly in given folder, find filepath with given extension and a field"
        " of view embedded in filename."
    ),
    parameters=dict(
        folder="Path to folder in which to find files",
        extension="The extension of files to find",
    ),
    raises=dict(RuntimeError="If the same FOV is found to correspond to more than one path"),
    returns="Mapping from field of view to filepath",
    see_also=dict(
        find_multiple_paths_by_fov="Similar function, for multiple paths by FOV, no particular extension",
        get_fov_sort_key="The function used to try to parse FOV from filename",
    ),
)
def find_single_path_by_fov(folder: PathLike, *, extension: str) -> dict[FieldOfViewFrom1, Path]:  # noqa: D103
    if isinstance(folder, str):
        folder = Path(folder)
    image_paths = {}
    for fn in os.listdir(folder):
        fp = folder / fn
        fov = get_fov_sort_key(fp, extension=extension)
        if fov is not None:
            if fov in image_paths:
                raise RuntimeError(f"FOV {fov} already seen in folder! {folder}")
            image_paths[fov] = fp
    return image_paths


@doc(
    summary="Get the sort key (by FOV) for the given filename or filepath.",
    parameters=dict(
        path="The path for which to get the FOV (to be used as sort key)",
        extension="The expected extension of the file name or path",
    ),
    raises=dict(
        TypeError="If the given value is neither a path nor a string",
    ),
    returns="Field of view parsed from filename, if parse succeeded; otherwise, None",
)
def get_fov_sort_key(path: PathLike, *, extension: str) -> Optional[FieldOfViewFrom1]:  # noqa: D103
    if not isinstance(path, str | Path):
        raise TypeError(
            f"Cannot parse sort-by-FOV key for {extension} stack from alleged path:"
            f" {path} (type {type(path).__name__})"
        )
    _, fn = os.path.split(path)
    if not (fn.startswith("P") and fn.endswith(extension)):
        return None
    rawval: str = fn.lstrip("P").rstrip(extension)
    if extension == ".zarr" and rawval.endswith(extension):
        # Support older looptrace-emitted data.
        warnings.warn(
            message=f"Stripping second '{extension}' extension; use data from newer software",
            category=DeprecationWarning,
            stacklevel=1,  # This deprecation is about underlying data, not about the call site.
        )
        rawval = rawval.rstrip(extension)
    try:
        rawval: int = int(rawval)  # type: ignore[no-redef]
    except ValueError:
        return None
    return FieldOfViewFrom1(rawval)  # type: ignore[arg-type]
