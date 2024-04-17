# gertils
General GERlich group uTILities

These tools are organised by use case at the module level; that is, tools that are used in a similar context will tend to be defined in the same module, with the module name reflecting that shared usage context. If you see that something's not well placed, please open an issue and/or a pull request.

## Index: modules and packages
- [collection_extras](collection_extras.py) -- tools for working with generic containers / collections
- [environments](./gertils/environments.py) -- tools for working with `conda` and `pip` environments
- [geometry](./gertils/geometry.py) -- tools for working with entities in space
- [gpu](./gertils/gpu.py) -- tools for running computations on GPUs, especially with TensorFlow
- [pathtools](./gertils/pathtools.py) -- tools for working with filesystem paths generally
- [types](./gertils/pathtools.py) -- data types for working with genome biology, especially imaging
- [zarr_tools](./gertils/zarr_tools.py) -- functions and types for working with ZARR-stored data

## Development
This project is configured to use Nix for a shell/environment with dependencies, and Nox to make common development commands/workflows easier. Start always with `nix-shell`. If it takes a long time to build, try...
1. Stop the shell build: `Ctrl-c`
1. Remove the Poetry lockfile: `rm poetry.lock`
1. Clear Poetry's PyPI cache (assuming you have an active Nix shell): `poetry cache clear PyPI --all`
1. Say "yes" if/when prompted for confirmation of desire to clear the cache
1. Exit Nix shell: `Ctrl-d`
1. Restart Nix shell: `shell.nix`

### Testing
From the Nix shell, run `nox --list` to see a list of available commands, notably to run tests against different versions of Python, to reformat code to be style-compliant, and to run the linter.

NB: To pass arguments through `nox` to `pytest`, separate the argument strings with `--`, e.g.:
```shell
nox -s tests-3.11 -- -vv
```
to run the tests with additional verbosity (e.g., `pytest -vv`)
