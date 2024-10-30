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
from collections.abc import Sequence
from typing import Annotated
from typing import Final
from typing import Literal
from typing import NamedTuple
from typing import TypeAlias
from typing import assert_never

import pydantic

from pydantic import root_validator
from pydantic import validator

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
    error_code = "error_code"
    timedelta_i32 = "timedelta_i32"
    timedelta_i64 = "timedelta_i64"
    datetime_i64 = "datetime_i64"

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
            case Primitive.records:
                hint = "Records"
            case Primitive.bool_:
                hint = "bool"
            case Primitive.uuid:
                hint = "uuid.UUID"
            case Primitive.error_code:
                hint = "ErrorCode"
            case Primitive.timedelta_i32:
                hint = "i32Timedelta"
            case Primitive.timedelta_i64:
                hint = "i64Timedelta"
            case Primitive.datetime_i64:
                hint = "TZAware"
            case no_match:
                assert_never(no_match)

        if optional or self is Primitive.uuid:
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


def parse_common_struct_reference(struct_name: object) -> CommonStruct:
    if not isinstance(struct_name, str):
        raise ValueError("Common struct reference must be str")

    try:
        return structs_registry[struct_name]
    except KeyError:
        raise ValueError(f"No registered common struct named {struct_name!r}") from None


class CommonStructArrayType(NamedTuple):
    struct: CommonStruct

    @classmethod
    def __get_validators__(cls) -> Iterator[Callable[[object], CommonStructArrayType]]:
        def parse_common_struct_array_type(value: object) -> CommonStructArrayType:
            if not isinstance(value, str):
                raise ValueError("CommonStructArrayType must be str")
            if not value.startswith("[]"):
                raise ValueError("CommonStructArrayType must start with '[]'")
            struct_name = value.removeprefix("[]")
            struct = parse_common_struct_reference(struct_name)
            return CommonStructArrayType(struct)

        yield parse_common_struct_array_type


class CommonStructType(NamedTuple):
    struct: CommonStruct

    @classmethod
    def __get_validators__(cls) -> Iterator[Callable[[object], CommonStructType]]:
        def parse_common_struct_type(struct_name: object) -> CommonStructType:
            struct = parse_common_struct_reference(struct_name)
            return CommonStructType(struct)

        yield parse_common_struct_type


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

    # This broke in upstream version 3.5, prior to that every message had the versions
    # field set. It was subsequently fixed, however according to discussion on the PR,
    # there is no intent to treat this strictly, so it needs to be treated as a
    # "feature" of the schema format.
    # https://github.com/apache/kafka/pull/13680
    @root_validator(pre=True)
    @classmethod
    def use_tagged_versions_as_fallback_for_versions(
        cls,
        values: Mapping[str, object],
    ) -> Mapping[str, object]:
        if "versions" in values:
            return values

        try:
            tagged_versions = values["taggedVersions"]
        except KeyError as e:
            raise ValueError(
                "Cannot derive a version range without one of `versions` or "
                "`taggedVersions`, and could not find either"
            ) from e

        return {**values, "versions": tagged_versions}

    @root_validator
    @classmethod
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

    def is_nullable_for_version(self, value: int) -> bool:
        if self.nullableVersions is None:
            return False
        return self.nullableVersions.matches(value)


# Defining this union before its members allows not having to call
# EntityField.update_forward_refs().
Field: TypeAlias = "PrimitiveField | PrimitiveArrayField | EntityArrayField | CommonStructArrayField | EntityField | CommonStructField"
timedelta_names: Final = frozenset(
    {
        "timeoutMs",
        "TimeoutMs",
        "ThrottleTimeMs",
        "MaxWaitMs",
        "SessionLifetimeMs",
        "TransactionTimeoutMs",
        "MaxLifetimeMs",
        "SessionTimeoutMs",
        "RebalanceTimeoutMs",
        "ExpiryTimePeriodMs",
        "RenewPeriodMs",
        "RetentionTimeMs",
        "HeartbeatIntervalMs",
        "PushIntervalMs",
    }
)
datetime_names: Final = frozenset(
    {
        "IssueTimestampMs",
        "ExpiryTimestampMs",
        "MaxTimestampMs",
        "TransactionStartTimeMs",
        "LogAppendTimeMs",
    }
)
excluded_ms_names: Final = frozenset[str]()
error_code_names: Final = frozenset({"ErrorCode", "PartitionErrorCode"})


class PrimitiveField(_BaseField):
    type: Primitive
    default: str | int | float | bool | None

    def is_nullable(self, version: int) -> bool:
        # Primitive types are never optional
        if self.type in {
            Primitive.int8,
            Primitive.int16,
            Primitive.int32,
            Primitive.int64,
            Primitive.uint16,
            Primitive.uint32,
            Primitive.uint64,
            Primitive.float64,
        }:
            return False

        return (
            (
                # Tagged fields that are ignorable and don't have a default are optional.
                self.get_tag(version) is not None
                and self.ignorable
                and self.default is None
            )
            or (
                False
                if self.nullableVersions is None
                else self.nullableVersions.matches(version)
            )
            or (
                # Datetime fields might not be optional in the underlying representation,
                # but if they have a default of -1, we want to represent that as None.
                self.type is Primitive.datetime_i64 and self.default == "-1"
            )
        )

    @root_validator(pre=True)
    @classmethod
    def special_case_error_code(
        cls,
        values: Mapping[str, object],
    ) -> Mapping[str, object]:
        if values["name"] in error_code_names:
            return {**values, "type": "error_code"}
        return values

    @staticmethod
    def _drop_ms_suffix(name: str) -> str:
        return name.removesuffix("Ms")

    @root_validator(pre=True)
    @classmethod
    def special_case_time_fields(
        cls,
        values: Mapping[str, object],
    ) -> Mapping[str, object]:
        name = values["name"]
        assert isinstance(name, str)
        if name in timedelta_names:
            match values["type"]:
                case Primitive.int32.value:
                    primitive = Primitive.timedelta_i32
                case Primitive.int64.value:
                    primitive = Primitive.timedelta_i64
                case _:
                    raise NotImplementedError(
                        f"Unknown timedelta primitive type: {values['type']!r}"
                    )
            return {
                **values,
                "type": primitive.value,
                "name": cls._drop_ms_suffix(name),
            }
        elif name in datetime_names:
            if values["type"] != Primitive.int64.value:
                raise NotImplementedError(
                    f"Unknown datetime primitive type: {values['type']!r}"
                )
            return {
                **values,
                "type": Primitive.datetime_i64.value,
                "name": cls._drop_ms_suffix(name),
            }
        elif name.endswith("Ms") and name not in excluded_ms_names:
            raise NotImplementedError(
                f"The field {name!r} looks like a time field, but is not "
                f"explicitly included or excluded."
            )
        return values


class RecordsField(_BaseField):
    type: Literal["records"]


class PrimitiveArrayField(_BaseField):
    type: PrimitiveArrayType


class CommonStructArrayField(_BaseField):
    type: CommonStructArrayType


class CommonStructField(_BaseField):
    type: CommonStructType
    default: Literal["null"] | None = None


class EntityArrayField(_BaseField):
    type: EntityArrayType
    fields: tuple[Field, ...]


class EntityField(_BaseField):
    type: EntityType
    fields: tuple[Field, ...]
    default: Literal["null"] | None = None


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
    commonStructs: tuple[CommonStruct, ...] = ()

    @validator("commonStructs", pre=True, always=False)
    @classmethod
    def solve_forward_references(cls, value: object) -> object:
        """
        Upstream version 3.5 introduced a schema construct in the common structs of
        AddPartitionsToTxnResponse that is only solvable by keeping track of forward
        references. This method does that in a somewhat crude but effective way: we
        assume that any ValidationError raised when parsing a CommonStruct could be
        solved by first resolving the other available common structs.

        This is implemented with a recursive function, but guarding itself against a
        situation where it's no longer making progress.
        """
        global structs_registry

        if not isinstance(value, Sequence) or not value:
            return value

        def resolve_structs(raw_structs: Sequence[object]) -> Iterator[CommonStruct]:
            unsolved = []
            for struct_data in raw_structs:
                try:
                    struct = CommonStruct.parse_obj(struct_data)
                except pydantic.ValidationError:
                    unsolved.append(struct_data)
                    continue
                yield struct

            if not unsolved:
                # All structs are resolved, we're done.
                return

            # If unsolved contain as many values as we started out with, it means we
            # made no progress at all in this pass, and there's no point in keeping
            # trying.
            if len(unsolved) == len(raw_structs):
                raise RuntimeError(
                    "Last pass made no progress, and there are still unsolved structs"
                )

            yield from resolve_structs(unsolved)

        for resolved_struct in resolve_structs(value):
            if resolved_struct.name in structs_registry:
                raise RuntimeError("Struct with conflicting name is already registered")
            structs_registry[resolved_struct.name] = resolved_struct

        yield from resolve_structs(value)


EntityArrayField.update_forward_refs()


def get_error_json(data: object, location: tuple[str | int, ...]) -> object:
    extracted = data
    for level in location:
        assert isinstance(extracted, dict)
        extracted = extracted[level]
    return extracted


def parse_common_structs(json_structure: object) -> dict[str, CommonStruct]:
    return {
        struct.name: struct
        for struct in CommonStructSchema.parse_obj(json_structure).commonStructs
    }


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
    structs_registry = parse_common_structs(parsed_json)

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
