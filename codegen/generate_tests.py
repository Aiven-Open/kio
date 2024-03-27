# ruff: noqa: T201

import os
import shutil
import sys

from collections import defaultdict
from itertools import chain
from pathlib import Path

from kio.static.constants import EntityType

from .case import to_snake_case
from .introspect_schema import base_dir
from .introspect_schema import get_entities
from .introspect_schema import schema_src_dir

imports = """\
from __future__ import annotations
import io
from hypothesis import given
from hypothesis.strategies import from_type
from kio.serial import entity_writer
from tests.conftest import setup_buffer, JavaTester
from kio.serial import entity_reader
from typing import Final
import pytest
"""
import_code = """\
from {entity_module} import {entity_type}
"""
test_code = """\


read_{entity_snake_case}: Final = entity_reader({entity_type})


@pytest.mark.roundtrip
@given(from_type({entity_type}))
def test_{entity_snake_case}_roundtrip(instance: {entity_type}) -> None:
    writer = entity_writer({entity_type})
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_{entity_snake_case}(buffer)
    assert instance == result
"""

test_code_java = """\
@pytest.mark.java
@given(instance=from_type({entity_type}))
def test_{entity_snake_case}_java(instance: {entity_type}, java_tester: JavaTester) -> None:
    java_tester.test(instance)
"""


generated_tests_module = base_dir / "tests" / "generated"


def build_filename(source_path: str) -> str:
    return "test_" + str(Path(source_path).relative_to(schema_src_dir)).replace(
        "/", "_"
    )


def main() -> None:
    print("Generating tests.", file=sys.stderr)
    shutil.rmtree(generated_tests_module, ignore_errors=True)
    os.mkdir(generated_tests_module)
    (generated_tests_module / "__init__.py").touch()

    module_imports = defaultdict(list)
    module_code = defaultdict(list)

    for entity_type, file in get_entities():
        module_path = generated_tests_module / build_filename(file)
        module_imports[module_path].append(
            import_code.format(
                entity_module=entity_type.__module__,
                entity_type=entity_type.__name__,
            )
        )
        module_code[module_path].append(
            test_code.format(
                entity_type=entity_type.__name__,
                entity_snake_case=to_snake_case(entity_type.__name__),
            )
        )
        if (
            entity_type.__type__ is not EntityType.nested
            and entity_type.__name__
            not in {
                "ProduceRequest",  # Records
                "FetchResponse",  # Records
                "FetchSnapshotResponse",  # Records
            }
        ):
            module_code[module_path].append(
                test_code_java.format(
                    entity_type=entity_type.__name__,
                    entity_snake_case=to_snake_case(entity_type.__name__),
                )
            )

    for module_path, entity_imports in module_imports.items():
        with module_path.open("w") as fd:
            print(imports, file=fd)
            for code in chain(entity_imports, module_code[module_path]):
                print(code, file=fd)


if __name__ == "__main__":
    main()
