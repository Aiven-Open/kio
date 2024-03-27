from __future__ import annotations

from collections.abc import Iterator
from importlib import import_module
from pathlib import Path
from pkgutil import walk_packages
from types import ModuleType
from typing import TYPE_CHECKING
from typing import Final

import kio.schema

from kio.static.constants import EntityType

# Chickens and eggs ...
if TYPE_CHECKING:
    from kio.static.protocol import Entity


base_dir: Final = Path(__file__).parent.parent.resolve()
schema_src_dir: Final = Path(kio.schema.__file__).parent.resolve()
ignore_modules: Final = frozenset({"index"})


def generate_modules(parent: ModuleType) -> Iterator[ModuleType]:
    for package in walk_packages(parent.__path__):
        if package.name in ignore_modules:
            continue
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


def get_message_entities() -> Iterator[tuple[type[Entity], str]]:
    for entity, file_path in get_entities():
        if entity.__type__ is EntityType.nested:
            continue
        yield entity, file_path
