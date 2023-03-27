# ruff: noqa: A003

from __future__ import annotations

import enum
import json
import pathlib
import re
import textwrap
from collections.abc import Callable
from collections.abc import Iterator
from collections.abc import Mapping
from typing import Annotated
from typing import Literal
from typing import NamedTuple
from typing import TypeAlias
from typing import assert_never

import pydantic
from pydantic import root_validator

from .util import BaseModel
from .versions import VersionRange

comment_pattern = re.compile(r"^\s*//")
structs_registry: dict[str, CommonStruct] = {}


class EntityType(str):
    @classmethod
    def __get_validators__(cls) -> Iterator[Callable[[object], EntityType]]:
        def parse_entity_type(value: object) -> EntityType:
            if not isinstance(value, str):
                raise ValueError("EntityType must be str")
            if value.startswith("[]"):
                raise ValueError("EntityType cannot contain []")
            return EntityType(value)

        yield parse_entity_type


class EntityArrayType(str):
    @classmethod
    def __get_validators__(cls) -> Iterator[Callable[[object], EntityArrayType]]:
        def parse_entity_array_type(value: object) -> EntityArrayType:
            if not isinstance(value, str):
                raise ValueError("EntityArrayType must be str")

            if not value.startswith("[]"):
                raise ValueError("EntityArrayType must start with []")

            return EntityArrayType(value.removeprefix("[]"))

        yield parse_entity_array_type


class Primitive(enum.Enum):
    bool_ = "bool"
    int8 = "int8"
    int16 = "int16"
    int32 = "int32"
    int64 = "int64"
    uint16 = "uint16"
    uint32 = "uint32"
    uint64 = "uint64"
    float64 = "float64"
    string = "string"
    bytes_ = "bytes"
    uuid = "uuid"
    records = "records"

    def get_type_hint(self, optional: bool = False) -> str:
        match self:
            case Primitive.int8:
                hint = "i8"
            case Primitive.int16:
                hint = "i16"
            case Primitive.int32:
                hint = "i32"
            case Primitive.int64:
                hint = "i64"
            case Primitive.uint16:
                hint = "u16"
            case Primitive.uint32:
                hint = "u32"
            case Primitive.uint64:
                hint = "u64"
            case Primitive.float64:
                hint = "f64"
            case Primitive.string:
                hint = "str"
            case Primitive.bytes_:
                hint = "bytes"
            case Primitive.bool_:
                hint = "bool"
            case Primitive.uuid:
                hint = "uuid.UUID"
            case Primitive.records:
                return "tuple[bytes | None, ...]"
            case no_match:
                assert_never(no_match)

        if optional:
            return f"{hint} | None"
        return hint


class PrimitiveArrayType(NamedTuple):
    item_type: Primitive

    @classmethod
    def __get_validators__(cls) -> Iterator[Callable[[object], PrimitiveArrayType]]:
        def parse_primitive_array_type(value: object) -> PrimitiveArrayType:
            if not isinstance(value, str):
                raise ValueError("PrimitiveArrayType must be str")
            if not value.startswith("[]"):
                raise ValueError("PrimitiveArrayType must start with '[]'")
            primitive = Primitive(value.removeprefix("[]"))
            return PrimitiveArrayType(primitive)

        yield parse_primitive_array_type


class CommonStructArrayType(NamedTuple):
    item_type: CommonStruct

    @classmethod
    def __get_validators__(cls) -> Iterator[Callable[[object], CommonStructArrayType]]:
        def parse_common_struct_array_type(value: object) -> CommonStructArrayType:
            if not isinstance(value, str):
                raise ValueError("CommonStructArrayType must be str")
            if not value.startswith("[]"):
                raise ValueError("CommonStructArrayType must start with '[]'")

            struct_name = value.removeprefix("[]")

            try:
                struct = structs_registry[struct_name]
            except KeyError:
                raise ValueError(
                    f"No registered common struct named {struct_name!r}"
                ) from None

            return CommonStructArrayType(struct)

        yield parse_common_struct_array_type


class _BaseField(BaseModel):
    name: str
    versions: VersionRange
    nullableVersions: VersionRange | None = None
    ignorable: bool = False
    mapKey: bool = False
    about: str | None = None
    entityType: str | None = None
    tag: int | None = None
    taggedVersions: VersionRange | None = None

    @classmethod
    @root_validator
    def validate_tag_tagged_versions_composite(
        cls,
        values: Mapping[str, object],
    ) -> Mapping[str, object]:
        tag = values["tag"]
        tagged_versions = values["taggedVersions"]
        if (tag is None and tagged_versions is not None) or (
            tag is not None and tagged_versions is None
        ):
            raise ValueError(
                f"`tag` and `taggedVersions` must either both be set or both be "
                f"omitted, got {tag=!r} {tagged_versions=!r}"
            )
        return values

    def get_tag(self, version: int) -> int | None:
        if self.taggedVersions is None or not self.taggedVersions.matches(version):
            return None
        assert self.tag is not None  # guaranteed by model validator
        return self.tag


# Defining this union before its members allows not having to call
# EntityField.update_forward_refs().
Field: TypeAlias = "PrimitiveField | PrimitiveArrayField | EntityArrayField | CommonStructArrayField | EntityField"


class PrimitiveField(_BaseField):
    type: Primitive
    default: str | int | float | bool | None

    def is_nullable(self, version: int) -> bool:
        return (
            # Tagged fields that are ignorable and don't have a default are optional.
            self.get_tag(version) is not None
            and self.ignorable
            and self.default is None
        ) or (
            False
            if self.nullableVersions is None
            else self.nullableVersions.matches(version)
        )


class RecordsField(_BaseField):
    type: Literal["records"]


class PrimitiveArrayField(_BaseField):
    type: PrimitiveArrayType


class CommonStructArrayField(_BaseField):
    type: CommonStructArrayType


class EntityArrayField(_BaseField):
    type: EntityArrayType
    fields: tuple[Field, ...]


class EntityField(_BaseField):
    type: EntityType
    fields: tuple[Field, ...]


class _BaseSchema(BaseModel):
    name: str
    validVersions: VersionRange
    flexibleVersions: VersionRange
    fields: tuple[Field, ...]


class MessageSchema(_BaseSchema):
    apiKey: int
    type: Literal["request", "response"]


class HeaderSchema(_BaseSchema):
    type: Literal["header"]


class DataSchema(_BaseSchema):
    type: Literal["data"]


class Schema(BaseModel):
    __root__: Annotated[
        MessageSchema | HeaderSchema | DataSchema,
        pydantic.Field(discriminator="type"),
    ]


class CommonStruct(BaseModel):
    name: str
    versions: VersionRange
    fields: tuple[Field, ...]


class CommonStructSchema(BaseModel):
    commonStructs: tuple[CommonStruct, ...]


EntityArrayField.update_forward_refs()


def get_error_json(data: object, location: tuple[str | int, ...]) -> object:
    extracted = data
    for level in location:
        assert isinstance(extracted, dict)
        extracted = extracted[level]
    return extracted


def parse_file(path: pathlib.Path) -> MessageSchema | HeaderSchema | DataSchema:
    global structs_registry
    structs_registry = {}

    contents = ""
    with path.open("r") as fd:
        for line in fd.readlines():
            if comment_pattern.match(line):
                continue
            contents += line

    parsed_json = json.loads(contents)

    try:
        parsed_structs = CommonStructSchema.parse_obj(parsed_json)
    except pydantic.ValidationError:
        if "commonStructs" in parsed_json:
            raise
    else:
        structs_registry = {
            struct.name: struct for struct in parsed_structs.commonStructs
        }

    try:
        parsed_schema = Schema.parse_obj(parsed_json)
    except pydantic.ValidationError as exc:
        location = exc.errors()[-1]["loc"]
        extracted = textwrap.indent(
            json.dumps(
                get_error_json(parsed_json, location[:-1]),
                indent=2,
            ),
            prefix="  ",
        )
        exc.add_note(
            f"\n🧑‍🚒 Location of last error: {location}, value:\n\n{extracted}\n"
        )
        raise exc

    return parsed_schema.__root__
