import os
import shutil
from collections.abc import Iterator
from importlib import import_module
from pathlib import Path
from pkgutil import walk_packages
from types import ModuleType

from codegen.case import to_snake_case

import kio.schema


def generate_modules(parent: ModuleType) -> Iterator[ModuleType]:
    for package in walk_packages(parent.__path__):
        module = import_module(f"{parent.__name__}.{package.name}")
        if package.ispkg:
            yield from generate_modules(module)
        else:
            yield module


def get_entities() -> Iterator[tuple[type, str]]:
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
import io
from hypothesis import given, settings
from hypothesis.strategies import from_type
from kio.serial import entity_writer
from tests.conftest import setup_buffer
from kio.serial import read_sync
from kio.serial import entity_decoder
"""
test_code = """\
from {entity_module} import {entity_type}

@given(from_type({entity_type}))
@settings(max_examples=1)
def test_{entity_snake_case}_roundtrip(instance: {entity_type}) -> None:
    writer = entity_writer({entity_type})
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder({entity_type}))
    assert instance == result
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

    for entity_type, file in get_entities():
        module_path = generated_tests_module / build_filename(file)
        write_imports = not module_path.exists()
        with module_path.open("a") as fd:
            if write_imports:
                print(imports, file=fd)
            print(
                test_code.format(
                    entity_module=entity_type.__module__,
                    entity_type=entity_type.__name__,
                    entity_snake_case=to_snake_case(entity_type.__name__),
                ),
                file=fd,
            )


if __name__ == "__main__":
    main()
