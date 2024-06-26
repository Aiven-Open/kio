# ruff: noqa: T201

import pathlib
import sys

from dataclasses import dataclass
from typing import Final
from typing import Self

from .introspect_schema import base_dir

target_path: Final = base_dir / "src/kio/schema/errors.py"

indent: Final = "    "
module_setup: Final = """\
from __future__ import annotations

import enum

from typing import TYPE_CHECKING

from kio.static.primitive import i16


class ErrorCode(enum.IntEnum):
    retriable: bool
    value: i16

    # Note: Pragma is needed to ignore the negative branch, the branch where the
    # conditional check fails.
    if not TYPE_CHECKING:  # pragma: no cover

        def __new__(cls, value: int, retriable: bool) -> ErrorCode:
            normalized_value = i16(value)
            obj = int.__new__(cls, normalized_value)
            obj._value_ = normalized_value
            obj.retriable = retriable
            return obj

"""


def parse_name(value: str) -> str:
    name = value.lower()
    if not str.isidentifier(name):
        raise ValueError(f"{value!r} is not a valid name")
    return name


def parse_bool(value: str) -> bool:
    if value == "True":
        return True
    elif value == "False":
        return False
    else:
        raise ValueError(f"{value!r} is not a valid bool")


@dataclass(frozen=True, slots=True, kw_only=True)
class ErrorCode:
    code: int
    name: str
    retriable: bool
    message: str

    @classmethod
    def parse_line(cls, line: str) -> Self:
        code, name, retriable, message = line.strip().split(" ", 3)
        return cls(
            code=int(code),
            name=parse_name(name),
            retriable=parse_bool(retriable),
            message=message,
        )


def main() -> None:
    try:
        source_path = pathlib.Path(sys.argv[1])
    except (IndexError, ValueError):
        print(
            "Error: must be called with path to extracted error codes as single argument",
            file=sys.stderr,
        )
        raise SystemExit(1) from None

    print("Generating error codes.", file=sys.stderr)

    with (
        source_path.open() as source_fd,
        target_path.open("w") as target_fd,
    ):
        print(module_setup, file=target_fd)

        for line in source_fd.readlines():
            code = ErrorCode.parse_line(line)
            print(
                f"{indent}{code.name} = {code.code}, {code.retriable}",
                file=target_fd,
            )
            if code.code != 0:
                print(f'{indent}"""{code.message}"""', file=target_fd)


if __name__ == "__main__":
    main()
