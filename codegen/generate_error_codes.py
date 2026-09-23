# ruff: noqa: T201

import pathlib
import sys

from dataclasses import dataclass
from typing import Final
from typing import Self

from . import build_tag
from .custom_error_codes import CUSTOM_ERROR_CODES
from .custom_error_codes import CustomErrorCode
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


def merge_error_codes(
    source_codes: list[ErrorCode],
    custom_codes: tuple[CustomErrorCode, ...],
) -> list[ErrorCode]:
    by_code = {code.code: code for code in source_codes}
    by_name = {code.name: code for code in source_codes}

    for custom_code in custom_codes:
        code = ErrorCode(
            code=custom_code.code,
            name=custom_code.name,
            retriable=custom_code.retriable,
            message=custom_code.message,
        )
        existing_code = by_code.get(code.code)
        existing_name = by_name.get(code.name)
        if existing_code is None and existing_name is None:
            by_code[code.code] = code
            by_name[code.name] = code
        elif existing_code == code and existing_name == code:
            continue
        else:
            raise ValueError(f"Conflicting custom error code: {code!r}")

    return sorted(by_code.values(), key=lambda value: value.code)


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

        source_codes = [ErrorCode.parse_line(line) for line in source_fd.readlines()]
        error_codes = merge_error_codes(
            source_codes,
            CUSTOM_ERROR_CODES.get(build_tag, ()),
        )
        for code in error_codes:
            print(
                f"{indent}{code.name} = {code.code}, {code.retriable}",
                file=target_fd,
            )
            if code.code != 0:
                print(f'{indent}"""{code.message}"""', file=target_fd)


if __name__ == "__main__":
    main()
