# ruff: noqa: T201

import pathlib
import shutil
import sys

from .util import create_package


def main() -> None:
    print("Deleting existing schema directory.", file=sys.stderr)

    schema_output_path = pathlib.Path("src/kio/schema/")
    try:
        shutil.rmtree(schema_output_path)
    except FileNotFoundError:
        pass
    create_package(schema_output_path)


if __name__ == "__main__":
    main()
