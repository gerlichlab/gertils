# gertils
General GERlich group uTILities

These tools are organised by use case at the module level; that is, tools that are used in a similar context will tend to be defined in the same module, with the module name reflecting that shared usage context. If you see that something's not well placed, please open an issue and/or a pull request.

## Index: modules and packages
- [collection_extras](./gertils/collection_extras.py) -- tools for working with generic containers / collections
- [geometry](./gertils/geometry.py) -- tools for working with entities in space
- [gpu](./gertils/gpu.py) -- tools for running computations on GPUs, especially with TensorFlow
- [pathtools](./gertils/pathtools.py) -- tools for working with filesystem paths generally
- [pixel_value_statistics](./gertils/pixel_value_statistics.py) -- tools for computing statistics of pixel values
- [types](./gertils/types.py) -- data types for working with genome biology, especially imaging
- [zarr_tools](./gertils/zarr_tools.py) -- functions and types for working with ZARR-stored data

## Development
This project is configured to use Nix for a shell/environment with dependencies. Start always with `nix-shell`. If it takes a long time to build, try...
1. Stop the shell build: `Ctrl-c`
1. Remove the Poetry lockfile: `rm poetry.lock`
1. Clear Poetry's PyPI cache (assuming you have an active Nix shell): `poetry cache clear PyPI --all`
1. Say "yes" if/when prompted for confirmation of desire to clear the cache
1. Exit Nix shell: `Ctrl-d`
1. Restart Nix shell: `nix-shell`

### Checks and tests
The checks that CI runs are pre-commit hooks, defined in `.pre-commit-config.yaml`. Install them once, from the Nix shell:
```shell
pre-commit install
```
Then codespell, ruff and pyright run on every commit, and the tests before every push. To run all the checks by hand: `pre-commit run --all-files`.

Each tool can also be run on its own, from the Nix shell:
- `pytest` for the tests, e.g. `pytest -vv` for more detail
- `pyright` for type checking
- `ruff check .` for linting
- `ruff format .` for formatting
- `codespell` for spelling
