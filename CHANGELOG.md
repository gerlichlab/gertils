# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.2] - 2024-04-18

### Changed
* Using more updated version of `numpydoc_decorator` for our lab, tagged rather than just commit hashed

## [0.4.1] - 2024-04-17

### Changed
* Bumped up lower bound on `numpydoc_generator` dependency, for compatibility with downstream projects which use a feature not yet in a release version.

## [0.4.0] - 2024-04-17

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
