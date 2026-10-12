# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
* `compute_pixel_statistics_for_channel`, the single-channel counterpart of `compute_pixel_statistics`, also available at package level. `compute_pixel_statistics` now calls it for each channel.
See [Issue 32](https://github.com/gerlichlab/gertils/issues/32).

### Changed
* gertils is type-checked with pyright instead of mypy, in strict mode for the package itself, as looptrace and VS Code's Pylance use pyright. Type information for `numpydoc_decorator` and for the part of `zarr` that gertils uses is in `typings/`.
* `read_zarr` opens the array read-only. It returns the same data as before.

### Fixed
* The documentation of `RegionalPixelStatistics` listed ten parameters that no longer exist, and described the statistics as coming from a single z-slice. The summary of `ImagePoint3D` described it as a 2D point.

## [v0.6.2] - 2026-10-12

### Fixed
* `get_fov_sort_key`, and so `find_single_path_by_fov` and `find_multiple_paths_by_fov`, misread the field of view when the file extension contains a digit; e.g. `P0012.nd2` was parsed as FOV 1, and `P0002.nd2` raised an error. Legacy `.zarr.zarr` names now emit the intended warning, and names starting with more than one `P` are no longer accepted. The warning is a `FutureWarning`, so that Python shows it by default.
See [Issue 41](https://github.com/gerlichlab/gertils/issues/41).
* `get_fov_sort_key` raised a `ValueError` for a name with the number 0, such as `P0000.zarr`, which made `find_single_path_by_fov` and `find_multiple_paths_by_fov` fail for the whole folder. It now returns `None`, as for any other name that doesn't give a field of view.
See [Issue 47](https://github.com/gerlichlab/gertils/issues/47).
* `get_fov_sort_key` also accepted spaces, a leading `+`, underscores and non-ASCII digits in the number, because it used `int()`, so `P1_2.zarr` got the same field of view as `P0012.zarr`. Only plain ASCII digits are accepted now.
See [Issue 48](https://github.com/gerlichlab/gertils/issues/48).
* `RegionalPixelStatistics.from_image`, and so `compute_pixel_statistics`, failed or used the wrong z-planes when the window around a point extended below plane 0; with the default padding, this affected every point with `z <= 0.5`. The window is now truncated at plane 0, as it already was at the top of the stack.
See [Issue 40](https://github.com/gerlichlab/gertils/issues/40).
* `compute_pixel_statistics` and `RegionalPixelStatistics.from_image` failed on dask arrays, because `np.median` can't take the median of a whole dask array. Only the region around the point is now loaded into memory, and of it only the planes of the z-window. The statistics are plain numbers.
See [Issue 33](https://github.com/gerlichlab/gertils/issues/33).
* `compute_pixel_statistics` reported the bounds of the whole region around a point, even where that region extends past the edge of the image, so bounds could be negative or beyond the image size. The reported bounds are now those of the pixels actually measured. A region entirely outside the image, or a diameter that isn't positive, now raises a `ValueError` with a clear message.
See [Issue 34](https://github.com/gerlichlab/gertils/issues/34).
* `compute_pixel_statistics` centred a region with an odd diameter one pixel away from the point for about half of all coordinates, in x and in y, because `round` rounds halves to the nearest even number. Regions are now centred on the nearest pixel, rounding halves up. For even diameters, only coordinates exactly half-way between two pixels change.
See [Issue 46](https://github.com/gerlichlab/gertils/issues/46).
* `compute_pixel_statistics` raises a `ValueError` saying so when the image isn't 4D (channel, z, y, x). Before, a 5D image gave a misleading message about 3D images, and a 3D image an `IndexError`.
* The package-level names are now declared in `__all__`. gertils ships `py.typed`, so without it, type checkers treated them as private to `gertils/__init__.py`: pyright, and mypy with `--no-implicit-reexport`, reported every `from gertils import ExtantFile` as importing a name the package does not export.

## [v0.6.1] - 2025-10-28

### Fixed
* The check for a negative `z` component of an `ImagePoint3D` instance is not correct. 
See [Issue 39](https://github.com/gerlichlab/gertils/issues/39).

### Changed
* Removed `get_x_coordinate` and `get_y_coordinate` members from `ImagePoint2D` and `ImagePoint3D`, and `get_z_coordinate` from `ImagePoint3D`.

## [v0.6.0] - 2025-03-21

### Changed
* Simplify `compute_pixel_statistics`, emitting just one collection of statistics rather than three; 
namely, the $z$-slice closest to a point will be used, plus/minus some optional slices of padding on above and below that slice.

## [v0.5.1] - 2024-11-21

### Added
* `__version__` attribute on the top-level package object

### Changed
* Parameter `signal_column` in `compute_pixel_statistics` is now `channel_column`.

## [v0.5.0] - 2024-11-21

### Added
* `ImagingChannel` wrapper type
* Cross-chanel signal extraction/analysis tool for images; see [Issue 27](https://github.com/gerlichlab/gertils/issues/27).

### Changed
* Depend on v2.2.1 of `numpydoc_decorator` directly from PyPI, rather than our custom release from earlier.
* Support Python 3.12

## [v0.4.4] - 2024-04-19

### Fixed
* Fix the return type in signature of `find_multiple_paths_by_fov`.

## [v0.4.3] - 2024-04-19

### Added
* Add type checking/hinting information to the package distribution.

## [v0.4.2] - 2024-04-18

### Changed
* Using more updated version of `numpydoc_decorator` for our lab, tagged rather than just commit hashed

## [v0.4.1] - 2024-04-17

### Changed
* Bumped up lower bound on `numpydoc_generator` dependency, for compatibility with downstream projects which use a feature not yet in a release version.

## [v0.4.0] - 2024-04-17

### Added
* Types and functions related to `geometry`
* Types and functions related to paths (`pathtools`)
* ZARR tools (`zarr_tools`)
* Some generally useful data types for genome biology (`types`)

### Changed
* Adopted `ruff` for formatting (rather than `black`) and for linting (rather than `pylint`).

### Removed
* All custom error types were removed; namely, absence of TensorFlow now will give `ModuleNotFoundError` (built-in) rather than a narrower error type.

## [v0.3.0] - 2024-03-13
* Made it so that `PathWrapperException` is always what arises when construction of a value of a refined path type fails, rather than having direct construction with a `Path` giving a `TypeError` as it was previously.

## [v0.2.0] - 2023-08-01

### Changed
* Exposed names, mainly from `pathtools` and `exceptions`, at the package level, for more stable use in dependent projects.

## [v0.1.0] - 2023-07-14
 
### Added
* This package, first release
