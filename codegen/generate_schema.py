# ruff: noqa: T201
# ruff: noqa: A003

from __future__ import annotations

import pathlib
import textwrap

from collections import defaultdict
from collections.abc import Iterable
from collections.abc import Iterator
from collections.abc import Sequence
from dataclasses import dataclass
from operator import attrgetter
from typing import Final
from typing import Literal
from typing import TypeAlias
from typing import assert_never

from pydantic import ValidationError

from . import build_tag
from .case import capitalize_first
from .case import to_snake_case
from .header_schema import get_header_schema_import
from .parser import CommonStructArrayField
from .parser import CommonStructField
from .parser import CommonStructType
from .parser import DataSchema
from .parser import EntityArrayField
from .parser import EntityField
from .parser import EntityType
from .parser import Field
from .parser import HeaderSchema
from .parser import MessageSchema
from .parser import Primitive
from .parser import PrimitiveArrayField
from .parser import PrimitiveArrayType
from .parser import PrimitiveField
from .parser import parse_file
from .util import create_package

schema_repository_source: Final = "clients/src/main/resources/common/message/"
imports_and_docstring: Final = '''\
"""
Generated from ``{schema_repository_source}{schema_source}``.
"""

import datetime
from dataclasses import dataclass, field
from typing import Annotated, ClassVar
import uuid
from kio.schema.errors import ErrorCode
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i64
from kio.static.primitive import u8
from kio.static.primitive import u16
from kio.static.primitive import u32
from kio.static.primitive import u64
from kio.static.primitive import f64
from kio.static.primitive import i32Timedelta
from kio.static.primitive import i64Timedelta
from kio.static.primitive import TZAware
from kio.static.primitive import Records
from kio.static.constants import EntityType
'''


def format_default(
    type_: Primitive | EntityType | CommonStructType,
    default: str | int | float | bool,
    optional: bool,
    custom_type: CustomTypeDef | None,
) -> str:
    if custom_type:
        custom_type_open = f"{custom_type.name}("
        custom_type_close = ")"
    else:
        custom_type_open = ""
        custom_type_close = ""

    match type_, default:
        case _, "null":
            assert optional, "non-optional field cannot be 'null'"
            return "None"
        case Primitive.string, default:
            return f"{custom_type_open}{default!r}{custom_type_close}"
        case (
            (
                Primitive.int8
                | Primitive.int16
                | Primitive.int32
                | Primitive.int64
                | Primitive.uint16
                | Primitive.uint32
                | Primitive.uint64
            ),
            str(default),
        ):
            assert not isinstance(type_, EntityType | CommonStructType)
            if custom_type_open:
                return "".join(
                    (
                        custom_type_open,
                        str(int(default, 0)),
                        custom_type_close,
                    )
                )
            return "".join(
                (
                    f"{type_.get_type_hint()}(",
                    str(int(default, 0)),
                    ")",
                )
            )
        case Primitive.bool_, str(default):
            value = default.capitalize()
            assert value in ("True", "False"), f"invalid default for bool: {default}"
            return f"{custom_type_open}{value}{custom_type_close}"
        case Primitive.float64, default:
            return f"{custom_type_open}{default}{custom_type_close}"
        case Primitive.error_code, default:
            return f"ErrorCode({default})"
        case Primitive.timedelta_i32, str(default):
            millis = int(default)
            return f"i32Timedelta.parse(datetime.timedelta(milliseconds={millis}))"
        case Primitive.timedelta_i64, str(default):
            millis = int(default)
            return f"i64Timedelta.parse(datetime.timedelta(milliseconds={millis}))"
        case Primitive.datetime_i64, "-1":
            assert optional
            return "None"

    raise NotImplementedError(
        f"Failed parsing default for {type_=} field: {default=!r}"
    )


def format_dataclass_field(
    field_type: Primitive | PrimitiveArrayType | EntityType | CommonStructType,
    default: str | int | float | bool | None,
    optional: bool,
    custom_type: CustomTypeDef | None,
    tag: int | None,
    ignorable: bool,
    nested_entity_defaults_only: bool = False,
) -> str:
    metadata: dict[str, object] = {}
    inner_type = (
        field_type.item_type
        if isinstance(field_type, PrimitiveArrayType)
        else field_type
    )

    if isinstance(field_type, Primitive | PrimitiveArrayType):
        metadata["kafka_type"] = inner_type.value  # type: ignore[union-attr]

    if tag is not None:
        metadata["tag"] = tag

    field_kwargs = {}

    if metadata:
        field_kwargs["metadata"] = repr(metadata)

    if isinstance(field_type, PrimitiveArrayType):
        field_kwargs["default"] = "()"
    elif default is not None:
        field_kwargs["default"] = format_default(
            field_type, default, optional, custom_type
        )
    elif (
        tag is not None
        and isinstance(field_type, EntityType | CommonStructType)
        and nested_entity_defaults_only
    ):
        # As of writing, this caters to a single field in the schema, the v15
        # FetchRequest.ReplicaState. When values of the nested entity are all defaults,
        # the tagged field is expected to be omitted. By making the default value of the
        # parent field equal to instantiating the child with only defaults, this doesn't
        # need any special treatment in parsers/serializers and functions as other
        # tagged fields in this respect.
        field_kwargs["default"] = f"{field_type}()"
    elif tag is not None and ignorable:
        field_kwargs["default"] = _format_default_for_tagged(field_type)

    if not field_kwargs:
        return ""

    formatted_kwargs = ", ".join(
        f"{key}={value}" for key, value in field_kwargs.items()
    )
    return f" = field({formatted_kwargs})"


def _format_default_for_tagged(
    field_type: Primitive | PrimitiveArrayType | EntityType | CommonStructType,
) -> str:
    match field_type:
        case Primitive.int8:
            result = "i8(0)"
        case Primitive.int16:
            result = "i16(0)"
        case Primitive.int32:
            result = "i32(0)"
        case Primitive.int64:
            result = "i64(0)"
        case Primitive.uint16:
            result = "u16(0)"
        case Primitive.uint32:
            result = "u32(0)"
        case Primitive.uint64:
            result = "u64(0)"
        case Primitive.float64:
            result = "f64(0.0)"
        case Primitive.bool_:
            result = "false"
        case Primitive.error_code:
            result = "ErrorCode.none"
        case (
            Primitive.string
            | Primitive.bytes_
            | Primitive.records
            | Primitive.uuid
            | Primitive.datetime_i64
            | Primitive.timedelta_i32
            | Primitive.timedelta_i64
        ):
            result = "None"
        case _ if isinstance(
            field_type, PrimitiveArrayType | EntityType | CommonStructType
        ):
            result = "None"
        case no_match:
            assert_never(no_match)
    return result


@dataclass(frozen=True, slots=True, kw_only=True, order=True)
class CustomTypeDef:
    name: str
    type_: Primitive

    def get_definition(self) -> str:
        type_hint = self.type_.get_type_hint()
        if self.type_ in (
            Primitive.string,
            Primitive.int8,
            Primitive.int16,
            Primitive.int32,
            Primitive.int64,
            Primitive.uint16,
            Primitive.uint32,
            Primitive.uint64,
            Primitive.float64,
        ):
            return textwrap.dedent(
                f"""\
                class {self.name}({type_hint}):
                    ...
                """
            )
        return f'{self.name} = NewType("{self.name}", {type_hint})'

    def get_import(self) -> str:
        return f"from kio.schema.types import {self.name}"

    def get_type_hint(self, optional: bool = False) -> str:
        return f"{self.name} | None" if optional else self.name


custom_types = dict[str, CustomTypeDef]()


def generate_custom_type(
    raw_name: str,
    type_: Primitive,
) -> CustomTypeDef:
    name = capitalize_first(raw_name)
    if (custom_type := custom_types.get(name)) is not None:
        return custom_type
    custom_type = CustomTypeDef(name=name, type_=type_)
    custom_types[name] = custom_type
    return custom_type


def generate_primitive_field(
    field: PrimitiveField,
    version: int,
    custom_type: CustomTypeDef | None,
) -> str:
    optional = field.is_nullable(version)
    dataclass_field = format_dataclass_field(
        field_type=field.type,
        default=field.default,
        optional=optional,
        custom_type=custom_type,
        tag=field.get_tag(version),
        ignorable=field.ignorable,
    )
    type_hint = (
        field.type.get_type_hint(optional)
        if custom_type is None
        else custom_type.get_type_hint(optional)
    )
    return f"    {to_snake_case(field.name)}: {type_hint}{dataclass_field}\n"


def generate_primitive_array_field(
    field: PrimitiveArrayField,
    inner_type: Primitive,
    version: int,
    custom_type: CustomTypeDef | None,
) -> str:
    inner_type_hint = (
        inner_type.get_type_hint()
        if custom_type is None
        else custom_type.get_type_hint()
    )
    dataclass_field = format_dataclass_field(
        field_type=field.type,
        default=None,
        optional=False,
        custom_type=None,
        tag=field.get_tag(version),
        ignorable=field.ignorable,
    )
    return (
        f"    {to_snake_case(field.name)}: "
        f"tuple[{inner_type_hint}, ...] "
        f"{dataclass_field}\n"
    )


def format_array_field_call(
    field: EntityArrayField | CommonStructArrayField,
    version: int,
) -> str:
    metadata: dict[str, object] = {}

    tag = field.get_tag(version)
    if tag is not None:
        metadata["tag"] = tag

    field_kwargs = {}
    if metadata:
        field_kwargs["metadata"] = repr(metadata)
    if tag is not None and field.ignorable:
        field_kwargs["default"] = "()"

    if not field_kwargs:
        return ""

    formatted_kwargs = ", ".join(
        f"{key}={value}" for key, value in field_kwargs.items()
    )
    return f" = field({formatted_kwargs})"


def format_non_primitive_array_field(
    field: EntityArrayField | CommonStructArrayField,
    version: int,
    inner_type_name: str,
) -> str:
    field_call = format_array_field_call(field, version)
    optional = " | None" if field.is_nullable_for_version(version) else ""
    return (
        f"    {to_snake_case(field.name)}: "
        f"tuple[{inner_type_name}, ...]{optional}"
        f"{field_call}\n"
    )


def entity_annotation(field: EntityField | CommonStructField, optional: bool) -> str:
    return f"{field.type} | None" if optional else str(field.type)


def nested_entity_has_only_defaults(field: EntityField | CommonStructField) -> bool:
    # TODO: This behavior should likely apply to a tagged to a CommonStructField as
    #  well. For now we don't have the required introspection capabilities of its
    #  fields, so that's left for when it becomes required.
    return isinstance(field, EntityField) and all(
        not isinstance(
            field,
            PrimitiveArrayField
            | EntityArrayField
            | CommonStructArrayField
            | CommonStructField,
        )
        and field.default is not None
        for field in field.fields
    )


def generate_entity_field(
    field: EntityField | CommonStructField,
    version: int,
) -> str:
    optional = field.is_nullable_for_version(version)
    field_call = format_dataclass_field(
        field_type=field.type,
        default=field.default,
        optional=optional,
        custom_type=None,
        tag=field.get_tag(version),
        ignorable=field.ignorable,
        nested_entity_defaults_only=nested_entity_has_only_defaults(field),
    )
    annotation = entity_annotation(field, optional)
    return f"    {to_snake_case(field.name)}: {annotation}{field_call}\n"


def generate_common_struct_field(
    field: CommonStructField,
    version: int,
) -> str:
    field_call = format_dataclass_field(
        field_type=field.type,
        default=None,
        optional=field.is_nullable_for_version(version),
        custom_type=None,
        tag=field.get_tag(version),
        ignorable=field.ignorable,
    )
    return f"    {to_snake_case(field.name)}: {field.type.struct.name}{field_call}\n"


seen = set[tuple[str, int]]()


def filter_version_fields(version: int, fields: Iterable[Field]) -> Iterator[Field]:
    for field in fields:
        if field.versions.matches(version):
            yield field


def message_class_vars(
    schema: MessageSchema | HeaderSchema | DataSchema,
) -> Iterator[str]:
    if not isinstance(schema, MessageSchema):
        return
    yield f"    __api_key__: ClassVar[i16] = i16({schema.apiKey})\n"
    if schema.type == "request":
        yield "    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader\n"
    elif schema.type == "response":
        yield "    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader\n"
    else:
        raise NotImplementedError("Unknown message schema type")


def _entity_type_line(
    schema: MessageSchema | HeaderSchema | DataSchema,
    top_level: bool,
) -> str:
    return (
        f"    __type__: ClassVar = EntityType.{schema.type}\n"
        if top_level
        else "    __type__: ClassVar = EntityType.nested\n"
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class ExportName:
    name: str
    type: Literal["request", "response", "header", "data"]

    def get_import(self) -> str:
        return f"from .{self.type} import {self.name}"


# TODO: Address complexity.
def generate_dataclass(  # noqa: C901
    schema: MessageSchema | HeaderSchema | DataSchema,
    name: str,
    fields: Sequence[Field],
    version: int,
    top_level: bool = False,
) -> Iterator[str | CustomTypeDef | ExportName]:
    if (name, version) in seen:
        return
    seen.add((name, version))

    class_start = textwrap.dedent(
        f"""\
        @dataclass(frozen=True, slots=True, kw_only=True)
        class {name}:
        """
    )
    class_fields = []
    for field in filter_version_fields(version, fields):
        if isinstance(field, PrimitiveField):
            custom_type = (
                generate_custom_type(field.entityType, field.type)
                if field.entityType is not None
                else None
            )
            if custom_type is not None:
                yield custom_type
            class_fields.append(
                generate_primitive_field(
                    field=field,
                    version=version,
                    custom_type=custom_type,
                )
            )
        elif isinstance(field, PrimitiveArrayField):
            inner_type = field.type.item_type
            custom_type = (
                generate_custom_type(field.entityType, inner_type)
                if field.entityType is not None
                else None
            )
            if custom_type is not None:
                yield custom_type
            class_fields.append(
                generate_primitive_array_field(
                    field=field,
                    inner_type=inner_type,
                    version=version,
                    custom_type=custom_type,
                )
            )
        elif isinstance(field, EntityArrayField):
            yield from generate_dataclass(
                schema=schema,
                name=str(field.type),
                fields=field.fields,
                version=version,
            )
            class_fields.append(
                format_non_primitive_array_field(field, version, field.type)
            )
        elif isinstance(field, EntityField):
            yield from generate_dataclass(
                schema=schema,
                name=str(field.type),
                fields=field.fields,
                version=version,
            )
            class_fields.append(generate_entity_field(field, version))
        elif isinstance(field, CommonStructArrayField):
            yield from generate_dataclass(
                schema=schema,
                name=field.type.struct.name,
                fields=field.type.struct.fields,
                version=version,
            )
            class_fields.append(
                format_non_primitive_array_field(field, version, field.type.struct.name)
            )
        elif isinstance(field, CommonStructField):
            yield from generate_dataclass(
                schema=schema,
                name=field.type.struct.name,
                fields=field.type.struct.fields,
                version=version,
            )
            class_fields.append(generate_common_struct_field(field, version))
        else:
            assert_never(field)

        if field.about:
            class_fields.append(f'    """{field.about}"""\n')

    yield class_start
    yield _entity_type_line(schema, top_level)
    yield f"    __version__: ClassVar[i16] = i16({version})\n"
    is_flexible = str(schema.flexibleVersions.matches(version))
    yield f"    __flexible__: ClassVar[bool] = {is_flexible}\n"
    yield from message_class_vars(schema)
    yield from class_fields

    if top_level:
        yield ExportName(name=name, type=schema.type)


def generate_models(
    schema: MessageSchema | HeaderSchema | DataSchema,
) -> Iterator[tuple[int, str | CustomTypeDef | ExportName]]:
    for version in schema.validVersions.iterator():
        accumulated_code = ""
        export = None
        for item in generate_dataclass(
            schema=schema,
            name=schema.name,
            fields=schema.fields,
            version=version,
            top_level=True,
        ):
            match item:
                case CustomTypeDef() as instruction:
                    yield version, instruction
                case ExportName() as instruction:
                    export = instruction
                case str(code):
                    accumulated_code += code
                case no_match:
                    assert_never(no_match)
        yield version, accumulated_code
        if export is not None:
            yield version, export


def basic_name(schema_name: str) -> str:
    return to_snake_case(schema_name).removesuffix("_response").removesuffix("_request")


seen_custom_types = set[str]()
custom_type_imports = """\
from typing import NewType
from kio.static.primitive import i8, i16, i32, i64, u8, u16, u32, u64, f64
"""


def write_custom_type(path: pathlib.Path, custom_type: CustomTypeDef) -> None:
    write_imports = not path.exists()
    if custom_type.name in seen_custom_types:
        return
    seen_custom_types.add(custom_type.name)
    with path.open("a") as fd:
        if write_imports:
            print(custom_type_imports, file=fd)
        print(custom_type.get_definition(), file=fd)


SchemaType: TypeAlias = Literal["request", "response", "header", "data"]
module_entity_dependencies = defaultdict[tuple[int, SchemaType], list[CustomTypeDef]](
    list
)


def write_to_version_module(
    schema: MessageSchema | HeaderSchema | DataSchema,
    schema_path: pathlib.Path,
    api_name: str,
    api_package_path: pathlib.Path,
    version: int,
    code: str,
) -> None:
    global seen
    seen = set()
    module_path = api_package_path / f"v{version}" / f"{schema.type}.py"
    create_package(module_path.resolve().parent)
    write_imports = not module_path.exists()
    print(f"-> [{schema.type}] {api_name} v{version} ...", end="")

    with module_path.open("a") as fd:
        if write_imports:
            print(
                imports_and_docstring.format(
                    schema_repository_source=schema_repository_source,
                    schema_source=schema_path.name,
                ),
                file=fd,
            )
            print(get_header_schema_import(schema, version), file=fd)
            entities = module_entity_dependencies[(version, schema.type)]
            for entity in entities:
                print(entity.get_import(), file=fd)
        print(code, file=fd)
    print(" done.")


module_exports = defaultdict[pathlib.Path, set[ExportName]](set)


def write_version_export(
    api_name: str,
    api_package_path: pathlib.Path,
    name: ExportName,
    version: int,
) -> None:
    print(f"-> [{name.type}] {api_name} Exporting {name.name} v{version} ...", end="")
    module_path = api_package_path / f"v{version}" / "__init__.py"
    module_exports[module_path].add(name)
    with module_path.open("a") as fd:
        print(name.get_import(), file=fd, flush=True)
    print(" done.")


def finalize_exports() -> None:
    for path, names in module_exports.items():
        with path.open("a") as fd:
            print("__all__ = (", file=fd)
            for name in sorted(names, key=attrgetter("name")):
                print(f'    "{name.name}",', file=fd)
            print(")", file=fd, flush=True)


def main() -> None:
    schema_output_path = pathlib.Path("src/kio/schema/")
    types_module_path = schema_output_path / "types.py"
    schemas = (pathlib.Path("schema") / build_tag).glob("*.json")
    custom_types = set[CustomTypeDef]()

    for path in schemas:
        try:
            schema = parse_file(path)
        except ValidationError as exc:
            exc.add_note(f"💥 Failed parsing schema in {path}")
            raise exc

        api_name = basic_name(schema.name)

        api_package = schema_output_path / api_name
        create_package(api_package)

        for chunk in generate_models(schema):
            match chunk:
                case (version, CustomTypeDef() as custom_type):
                    key = (version, schema.type)
                    module_entity_dependencies[key].append(custom_type)
                    custom_types.add(custom_type)
                case (version, ExportName() as name):
                    write_version_export(  # type: ignore[unreachable]
                        api_name=api_name,
                        api_package_path=api_package,
                        name=name,
                        version=version,
                    )
                case (version, code):
                    write_to_version_module(  # type: ignore[unreachable]
                        schema=schema,
                        api_name=api_name,
                        api_package_path=api_package,
                        schema_path=path,
                        version=version,
                        code=code,
                    )
                case no_match:
                    assert_never(no_match)  # type: ignore[arg-type]

    # We accumulate entity types and process them separately here, so that they can
    # be sorted before written, otherwise they become a source of in-determinism.
    for custom_type in sorted(custom_types):
        print(f"-> [custom type] {custom_type.name}")
        write_custom_type(types_module_path, custom_type)

    # Generate __all__ for accumulated module exports.
    finalize_exports()
