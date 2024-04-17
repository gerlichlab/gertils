# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
* Types and functions related to `geometry`
* Types and functions related to paths (`pathtools`)
* ZARR tools (`zarr_tools`)
* Some generally useful data types for genome biology (`types`)

### Changed
* Adopted `ruff` for formatting (rather than `black`) and for linting (rather than `pylint`).

### Removed
* All custom error types were removed; namely, absence of TensorFlow now will give `ModuleNotFoundError` (built-in) rather than a narrower error type.

## [2024-03-13] - 2024-03-13
* Made it so that `PathWrapperException` is always what arises when construction of a value of a refined path type fails, rather than having direct construction with a `Path` giving a `TypeError` as it was previously.

## [2023-08-01] - 2023-08-01

### Changed
* Exposed names, mainly from `pathtools` and `exceptions`, at the package level, for more stable use in dependent projects.

## [2023-07-14] - 2023-07-14
 
### Added
* This package, first release
