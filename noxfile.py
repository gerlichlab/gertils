"""Declaration of Nox commands which can be run for this package"""

import hashlib
from pathlib import Path
from typing import Iterable

import nox

PYTHON_VERSIONS = ["3.10", "3.11", "3.12"]
TESTS_SUBFOLDER = "tests"
PACKAGE_NAME = "gertils"


def install_groups(
    session: nox.Session,
    *,
    include: Iterable[str] = (),
    include_self: bool = True,
) -> None:
    """Install Poetry dependency groups.

    Install the given dependency groups into the session's virtual environment.
    When 'include_self' is true, also installs this package and default dependencies.

    We cannot use `poetry install` here, because it ignores the
    session's environment and installs into Poetry's own environment.
    Instead, use `poetry export` with suitable options to generate a requirements.txt
    file to pass to session.install().

    Auto-skip the `poetry export` step if the poetry.lock file is unchanged
    (matching hash) since the last time this session was run.
    """
    if isinstance(session.virtualenv, nox.virtualenv.PassthroughEnv):
        session.warn(
            "Running outside a Nox virtualenv! We will skip installation here, "
            "and simply assume that the necessary dependency groups have "
            "already been installed by other means!"
        )
        return

    lockdata = Path("poetry.lock").read_bytes()
    digest = hashlib.blake2b(lockdata).hexdigest()
    requirements_txt = Path(session.cache_dir, session.name, "reqs_from_poetry.txt")
    hashfile = requirements_txt.with_suffix(".hash")

    if not hashfile.is_file() or hashfile.read_text() != digest:
        # First, adjust settings to avoid warning that we cover in shell.nix.
        # See: https://python-poetry.org/blog/announcing-poetry-1.7.0/
        argv = [
            "poetry",
            "config", 
            "warnings.export",
            "false",
        ]
        session.log(f"Will generate requirements hashfile: {hashfile}")
        requirements_txt.parent.mkdir(parents=True, exist_ok=True)
        argv = [
            "poetry",
            "export",
            "--format=requirements.txt",
            f"--output={requirements_txt}",
        ]
        if include:
            option = "only" if not include_self else "with"
            argv.append(f"--{option}={','.join(include)}")
        session.debug(f"Running command: {' '.join(argv)}")
        session.run_always(*argv, external=True)
        session.debug(f"Writing requirements hashfile: {hashfile}")
        hashfile.write_text(digest)

    session.log("Installing requirements")
    session.install("-r", str(requirements_txt))
    if include_self:
        session.log(f"Installing {PACKAGE_NAME}")
        session.install("-e", ".")
    else:
        session.debug(f"Skipping installation of {PACKAGE_NAME}")


@nox.session(python=PYTHON_VERSIONS)
def tests(session):
    install_groups(session, include=["test"])
    session.run(
        "pytest",
        "-x",
        "--log-level=debug",
        "--durations=10",
        "--hypothesis-show-statistics",
        *session.posargs,
    )


@nox.session(python=PYTHON_VERSIONS)
def lint(session):
    install_groups(session, include=["lint"])
    session.run("mypy")
    session.run("pylint", PACKAGE_NAME)
    extra_warnings_to_disable_for_tests_subfolder = [
        "invalid-name",
        "missing-function-docstring",
        "protected-access",
        "redefined-outer-name",
        "too-many-arguments",
        "too-many-instance-attributes",
        "too-many-lines",
        "unused-argument",
        "use-implicit-booleaness-not-comparison",
    ]
    session.run(
        "pylint",
        f"--disable={','.join(extra_warnings_to_disable_for_tests_subfolder)}",
        TESTS_SUBFOLDER,
    )


@nox.session
def format(session):
    install_groups(session, include=["format"], include_self=False)
    session.run("codespell", "--enable-colors")
    session.run("isort", PACKAGE_NAME, TESTS_SUBFOLDER, "--check", "--diff", "--color")
    session.run("black", ".", "--check", "--diff", "--color")


@nox.session
def reformat(session):
    install_groups(session, include=["format"], include_self=False)
    session.run("codespell", "--write-changes")
    session.run("isort", PACKAGE_NAME, TESTS_SUBFOLDER)
    session.run("black", ".")
