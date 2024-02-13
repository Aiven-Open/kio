import os
import shutil

from collections import defaultdict
from collections.abc import Iterator
from importlib import import_module
from itertools import chain
from pathlib import Path
from pkgutil import walk_packages
from types import ModuleType

import kio.schema

from kio.static.constants import EntityType
from kio.static.protocol import Entity

from .case import to_snake_case


def generate_modules(parent: ModuleType) -> Iterator[ModuleType]:
    for package in walk_packages(parent.__path__):
        module = import_module(f"{parent.__name__}.{package.name}")
        if package.ispkg:
            yield from generate_modules(module)
        else:
            yield module


def get_entities() -> Iterator[tuple[type[Entity], str]]:
    modules = list(generate_modules(import_module("kio.schema")))
    for module in modules:
        items = module.__dict__.copy()
        # Eliminate non-entity modules, situated directly under `kio.schema`.
        if sum(1 for c in module.__name__ if c == ".") < 3:
            continue
        for key, value in items.items():
            if key.startswith("__"):
                continue
            # Eliminate anything not defined in the module.
            if getattr(value, "__module__", None) != module.__name__:
                continue
            # Eliminate anything that's not a class.
            if type(value) is not type:
                continue
            assert isinstance(module.__file__, str)
            yield value, module.__file__


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


base_dir = Path(__file__).parent.parent.resolve()
generated_tests_module = base_dir / "tests" / "generated"
schema_src_dir = Path(kio.schema.__file__).parent.resolve()


def build_filename(source_path: str) -> str:
    return "test_" + str(Path(source_path).relative_to(schema_src_dir)).replace(
        "/", "_"
    )


def main() -> None:
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
