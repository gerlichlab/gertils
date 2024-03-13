# gertils
General GERlich group uTILities

These tools are organised by use case at the module level; that is, tools that are used in a similar context will tend to be defined in the same module, with the module name reflecting that shared usage context. If you see that something's not well placed, please open an issue and/or a pull request.

## Index
- [collection_extras.py](collection_extras.py) -- tools for working with generic containers / collections
- [environments.py](./gertils/environments.py) -- tools for working with `conda` and `pip` environments
- [gpu.py](./gertils/gpu.py) -- tools for running computations on GPUs, especially with TensorFlow
- [group_paths.py](./gertils/group_paths.py) -- tools for working with Gerlich group paths on filesystems
- [pathtools.py](./gertils/pathtools.py) -- tools for working with filesystem paths generally

## Development
This project is configured to use Nix for a shell/environment with dependencies, and Nox to make common development commands/workflows easier. Start always with `nix-shell`. If it takes a long time to build, try...
1. Stop the shell build: `Ctrl-c`
1. Remove the Poetry lockfile: `rm poetry.lock`
1. Clear Poetry's PyPI cache (assuming you have an active Nix shell): `poetry cache clear PyPI --all`
1. Say "yes" if/when prompted for confirmation of desire to clear the cache
1. Exit Nix shell: `Ctrl-d`
1. Restart Nix shell: `shell.nix`

