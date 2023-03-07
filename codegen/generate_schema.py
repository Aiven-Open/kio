from __future__ import annotations

import pathlib
import shutil
import textwrap
from collections import defaultdict
from collections.abc import Iterable
from collections.abc import Iterator
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Final
from typing import Literal
from typing import TypeAlias

from pydantic import ValidationError
from typing_extensions import assert_never

from .case import capitalize_first
from .case import to_snake_case
from .parser import CommonStructArrayField
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

imports_and_docstring: Final = '''\
"""
Generated from {schema_source}.
"""
from dataclasses import dataclass, field
from typing import Annotated, ClassVar
import uuid
from kio.schema.primitive import i8, i16, i32, i64, u8, u16, u32, u64, f64
'''


def format_default(
    type_: Primitive,
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
            Primitive.int8
            | Primitive.int16
            | Primitive.int32
            | Primitive.int64
            | Primitive.uint16
            | Primitive.uint32
            | Primitive.uint64
        ), str(default):
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

    raise NotImplementedError(
        f"Failed parsing default for {type_.value=} field: {default=!r}"
    )


def format_dataclass_field(
    field_type: Primitive | PrimitiveArrayType | EntityType,
    default: str | int | float | bool | None,
    optional: bool,
    custom_type: CustomTypeDef | None,
    tag: int | None,
) -> str:
    metadata: dict[str, object] = {}
    inner_type = (
        field_type.type if isinstance(field_type, PrimitiveArrayType) else field_type
    )

    if isinstance(field_type, (Primitive, PrimitiveArrayType)):
        metadata["kafka_type"] = inner_type.value  # type: ignore[union-attr]

    if tag is not None:
        metadata["tag"] = tag

    field_kwargs = {}

    if metadata:
        field_kwargs["metadata"] = repr(metadata)

    if isinstance(field_type, PrimitiveArrayType):
        field_kwargs["default"] = "()"
    elif default is not None:
        assert not isinstance(field_type, EntityType)
        field_kwargs["default"] = format_default(
            field_type, default, optional, custom_type
        )

    if not field_kwargs:
        return ""

    formatted_kwargs = ", ".join(
        f"{key}={value}" for key, value in field_kwargs.items()
    )
    return f" = field({formatted_kwargs})"


@dataclass(frozen=True, slots=True, kw_only=True, order=True)
class CustomTypeDef:
    name: str
    type_: Primitive

    def get_definition(self) -> str:
        type_hint = self.type_.get_type_hint()
        if self.type_ is Primitive.string:
            return textwrap.dedent(
                f"""\
                class {self.name}({type_hint}):
                    ...
                """
            )
        elif self.type_ in (
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


def generate_entity_array_field(
    field: EntityArrayField,
    version: int,
) -> str:
    field_call = format_array_field_call(field, version)
    return f"    {to_snake_case(field.name)}: tuple[{field.type}, ...]{field_call}\n"


def generate_entity_field(field: EntityField, version: int) -> str:
    field_call = format_dataclass_field(
        field_type=field.type,
        default=None,
        optional=field.nullableVersions.matches(version)
        if field.nullableVersions
        else False,
        custom_type=None,
        tag=field.get_tag(version),
    )
    return f"    {to_snake_case(field.name)}: {field.type}{field_call}\n"


def generate_common_struct_array_field(
    field: CommonStructArrayField,
    version: int,
) -> str:
    field_call = format_array_field_call(field, version)
    return (
        f"    {to_snake_case(field.name)}: tuple[{field.type.type.name}, ...]"
        f"{field_call}\n"
    )


seen = set[tuple[str, int]]()


def filter_version_fields(version: int, fields: Iterable[Field]) -> Iterator[Field]:
    for field in fields:
        if field.versions.matches(version):
            yield field


# TODO: Address complexity.
def generate_dataclass(  # noqa: C901
    schema: MessageSchema | HeaderSchema | DataSchema,
    name: str,
    fields: Sequence[Field],
    version: int,
) -> Iterator[str | CustomTypeDef]:
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
            inner_type = field.type.type
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
                generate_entity_array_field(
                    field=field,
                    version=version,
                )
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
                name=field.type.type.name,
                fields=field.type.type.fields,
                version=version,
            )
            class_fields.append(generate_common_struct_array_field(field, version))
        else:
            assert_never(field)

        if field.about:
            class_fields.append(f'    """{field.about}"""\n')

    yield class_start
    yield (
        "    __flexible__: ClassVar[bool] = True\n"
        if schema.flexibleVersions.matches(version)
        else "    __flexible__: ClassVar[bool] = False\n"
    )
    yield from class_fields


def generate_models(
    schema: MessageSchema | HeaderSchema | DataSchema,
) -> Iterator[tuple[int, str | CustomTypeDef]]:
    for version in schema.validVersions.iter():
        accumulated_code = ""
        for item in generate_dataclass(
            schema=schema,
            name=schema.name,
            fields=schema.fields,
            version=version,
        ):
            match item:
                case CustomTypeDef() as custom_type:
                    yield version, custom_type
                case str(code):
                    accumulated_code += code
                case no_match:
                    assert_never(no_match)
        yield version, accumulated_code


def basic_name(schema_name: str) -> str:
    return to_snake_case(schema_name).removesuffix("_response").removesuffix("_request")


def create_package(path: pathlib.Path) -> None:
    path.mkdir(exist_ok=True)
    (path / "__init__.py").touch(exist_ok=True)


seen_custom_types = set[str]()
custom_type_imports = """\
from typing import NewType
from kio.schema.primitive import i8, i16, i32, i64, u8, u16, u32, u64, f64
from phantom import Phantom
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
                imports_and_docstring.format(schema_source=schema_path.name),
                file=fd,
            )
            entities = module_entity_dependencies[(version, schema.type)]
            for entity in entities:
                print(entity.get_import(), file=fd)
        print(code, file=fd)
    print(" done.")


def create_module_primitive(destination: pathlib.Path) -> None:
    source = pathlib.Path(__file__).parent.resolve() / "template/primitive.py"
    shutil.copy(source, destination)


def main() -> None:
    schema_output_path = pathlib.Path("src/kio/schema/")
    types_module_path = schema_output_path / "types.py"
    shutil.rmtree(schema_output_path)
    create_package(schema_output_path)
    schemas = pathlib.Path("schema/").glob("*.json")
    create_module_primitive(schema_output_path / "primitive.py")
    custom_types = set[CustomTypeDef]()

    for path in schemas:
        try:
            schema = parse_file(path)
        except ValidationError as exc:
            exc.add_note(f"💥 Failed parsing schema in {path}")  # type: ignore[attr-defined]
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
