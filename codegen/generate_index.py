# ruff: noqa: T201

import sys

from collections import defaultdict
from collections.abc import Iterator
from collections.abc import Mapping
from functools import partial
from typing import Final
from typing import NamedTuple
from typing import TypeAlias

from kio.static.constants import EntityType
from kio.static.protocol import Entity

from .introspect_schema import base_dir
from .introspect_schema import get_message_entities

target_path: Final = base_dir / "src/kio/schema/index.py"
prefix: Final = "kio.schema."
indent: Final = "    "

module_setup: Final = """\
from collections.abc import Mapping
from types import MappingProxyType
from typing import Final
from typing import Literal
from typing import TypeAlias

from kio.static.constants import EntityType

__all__ = (
    "api_key_map",
    "schema_name_map",
    "PayloadEntityType",
    "LoadableEntityType",
)

PayloadEntityType: TypeAlias = Literal[EntityType.response, EntityType.request]
LoadableEntityType: TypeAlias = (
    Literal[EntityType.header, EntityType.data] | PayloadEntityType
)
TypeMap: TypeAlias = Mapping[LoadableEntityType, str]
VersionMap: TypeAlias = Mapping[int, TypeMap]
SchemaNameMap: TypeAlias = Mapping[str, VersionMap]
APIKeyMap: TypeAlias = Mapping[int, str]

"""


class PathParts(NamedTuple):
    api_name: str
    version: int
    entity_type: EntityType
    entity_name: str


def module_path_parts(entity: type[Entity]) -> PathParts:
    without_prefix = entity.__module__.removeprefix(prefix)
    parts = without_prefix.split(".")
    assert parts[-1] == entity.__type__.name
    return PathParts(
        api_name=parts[0],
        version=int(parts[1][1:]),
        entity_type=entity.__type__,
        entity_name=entity.__qualname__,
    )


def fqn(parts: PathParts) -> str:
    return (
        f"{prefix}"
        f"{parts.api_name}"
        f".v{parts.version}"
        f".{parts.entity_type.name}"
        f":{parts.entity_name}"
    )


TypeMap: TypeAlias = Mapping[EntityType, str]
VersionMap: TypeAlias = Mapping[int, TypeMap]
SchemaNameMap: TypeAlias = Mapping[str, VersionMap]
APIKeyMap: TypeAlias = Mapping[int, str]


def build_index() -> tuple[SchemaNameMap, APIKeyMap]:
    schema_name_map: defaultdict[str, defaultdict[int, dict[EntityType, str]]] = (
        defaultdict(partial(defaultdict, dict))
    )
    api_key_map = {}
    for entity, _ in get_message_entities():
        parts = module_path_parts(entity)
        schema_name_map[parts.api_name][parts.version][parts.entity_type] = fqn(parts)
        if (api_key := getattr(entity, "__api_key__", None)) is not None:
            api_key_map[api_key] = parts.api_name
    api_key_map = dict(sorted(api_key_map.items()))
    return schema_name_map, api_key_map


def format_schema_name_map(index: SchemaNameMap) -> Iterator[str]:
    yield "schema_name_map: Final[SchemaNameMap] = MappingProxyType({"

    for schema_name, version_map in index.items():
        yield f'{indent}"{schema_name}": MappingProxyType({{'

        for version, type_map in version_map.items():
            yield f"{indent}{indent}{version}: MappingProxyType({{"

            for entity_type, entity_path in type_map.items():
                yield (
                    f"{indent}{indent}{indent}EntityType.{entity_type.name}: ("
                    f'"{entity_path}"),'
                )

            yield f"{indent}{indent}}}),"

        yield f"{indent}}}),"

    yield "})"
    yield ""


def format_api_key_map(index: APIKeyMap) -> Iterator[str]:
    yield "api_key_map: Final[APIKeyMap] = MappingProxyType({"

    for api_key, module_name in index.items():
        yield f'{indent}{api_key}: "{module_name}",'

    yield "})"
    yield ""


def main() -> None:
    print("Generating index.", file=sys.stderr)
    print("Introspecting modules ...", file=sys.stderr, flush=True)
    schema_name_map, api_key_map = build_index()

    # Smoke test
    assert (
        schema_name_map["metadata"][11][EntityType.request]
        == "kio.schema.metadata.v11.request:MetadataRequest"
    )
    assert api_key_map[3] == "metadata"

    print("Writing index file ...", file=sys.stderr, flush=True)

    with target_path.open("w") as target:
        print(module_setup, file=target)

        for line in format_api_key_map(api_key_map):
            print(line, file=target)

        for line in format_schema_name_map(schema_name_map):
            print(line, file=target)

    print("Done.", file=sys.stderr, flush=True)


if __name__ == "__main__":
    main()
