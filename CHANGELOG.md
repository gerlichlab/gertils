# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
