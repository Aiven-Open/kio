"""
Extend maturin to plug into setuptools-scm for git-based versioning.
"""

import functools
import shutil
import subprocess
import sys

from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import maturin

# ruff: noqa: T201


@contextmanager
def _inject_pyproject_toml_version(version: bytes) -> Iterator[None]:
    print("Injecting version into pyproject.toml.")
    pyproject_toml = Path("pyproject.toml").resolve()
    pyproject_toml_copy = pyproject_toml.parent / "pyproject.toml.bkp"

    shutil.move(pyproject_toml, pyproject_toml_copy)

    with (
        pyproject_toml_copy.open("rb") as copy_fd,
        pyproject_toml.open("wb") as org_fd,
    ):
        for line in copy_fd:
            if line.startswith(b"version ="):
                org_fd.write(b'version = "' + version + b'"\n')
            else:
                org_fd.write(line)

    try:
        yield
    finally:
        shutil.move(pyproject_toml_copy, pyproject_toml)


def _wrap_hook(hook):
    @functools.wraps(hook)
    def wrapper(*args, **kwargs) -> str:
        print("Generating version file with setuptools-scm.")
        setuptools_scm_process = subprocess.run(  # noqa: S603
            [
                sys.executable,
                "-m",
                "setuptools_scm",
                "--force-write-version-files",
            ],
            check=True,
            stdout=subprocess.PIPE,
        )
        version = setuptools_scm_process.stdout.strip()
        print(f"Determined version is {version}.")

        with _inject_pyproject_toml_version(version):
            return hook(*args, **kwargs)

    return wrapper


build_wheel = _wrap_hook(maturin.build_wheel)
build_editable = _wrap_hook(maturin.build_editable)
build_sdist = _wrap_hook(maturin.build_sdist)
