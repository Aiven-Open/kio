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
    entity_type: EntityTypeDef | None,
) -> str:
    if entity_type:
        entity_type_open = f"{entity_type.name}("
        entity_type_close = ")"
    else:
        entity_type_open = ""
        entity_type_close = ""

    match type_, default:
        case _, "null":
            assert optional, "non-optional field cannot be 'null'"
            return "None"
        case Primitive.string, default:
            return f"{entity_type_open}{default!r}{entity_type_close}"
        case (
            Primitive.int8
            | Primitive.int16
            | Primitive.int32
            | Primitive.int64
            | Primitive.uint16
            | Primitive.uint32
            | Primitive.uint64
        ), str(default):
            if entity_type_open:
                return "".join(
                    (
                        entity_type_open,
                        str(int(default, 0)),
                        entity_type_close,
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
            return f"{entity_type_open}{value}{entity_type_close}"
        case Primitive.float64, default:
            return f"{entity_type_open}{default}{entity_type_close}"

    raise NotImplementedError(
        f"Failed parsing default for {type_.value=} field: {default=!r}"
    )


def format_dataclass_field(
    type: Primitive | PrimitiveArrayType,
    default: str | int | float | bool | None,
    optional: bool,
    entity_type: EntityTypeDef | None,
) -> str:
    inner_type = type.type if isinstance(type, PrimitiveArrayType) else type
    kwargs = {
        "metadata": f'{{"kafka_type": {inner_type.value!r}}}',
    }
    if isinstance(type, PrimitiveArrayType):
        kwargs["default"] = "()"
    elif default is not None:
        kwargs["default"] = format_default(type, default, optional, entity_type)
    formatted_kwargs = ", ".join(f"{key}={value}" for key, value in kwargs.items())
    return f" = field({formatted_kwargs})"


@dataclass(frozen=True, slots=True, kw_only=True)
class EntityTypeDef:
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


entities = dict[str, EntityTypeDef]()


def generate_entity_type(
    raw_name: str,
    type_: Primitive,
) -> EntityTypeDef:
    name = capitalize_first(raw_name)
    if (entity_type := entities.get(name)) is not None:
        return entity_type
    entity_type = EntityTypeDef(name=name, type_=type_)
    entities[name] = entity_type
    return entity_type


def generate_primitive_field(
    field: PrimitiveField,
    version: int,
    entity_type: EntityTypeDef | None,
) -> str:
    optional = field.is_nullable(version)
    dataclass_field = format_dataclass_field(
        field.type, field.default, optional, entity_type
    )
    type_hint = (
        field.type.get_type_hint(optional)
        if entity_type is None
        else entity_type.get_type_hint(optional)
    )
    return f"    {to_snake_case(field.name)}: {type_hint}{dataclass_field}\n"


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
) -> Iterator[str | EntityTypeDef]:
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
            entity_type = (
                generate_entity_type(field.entityType, field.type)
                if field.entityType is not None
                else None
            )
            if entity_type is not None:
                yield entity_type
            class_fields.append(
                generate_primitive_field(
                    field=field,
                    version=version,
                    entity_type=entity_type,
                )
            )
        elif isinstance(field, PrimitiveArrayField):
            inner_type = field.type.type
            entity_type = (
                generate_entity_type(field.entityType, inner_type)
                if field.entityType is not None
                else None
            )
            if entity_type is not None:
                yield entity_type
            inner_type_hint = (
                inner_type.get_type_hint()
                if entity_type is None
                else entity_type.get_type_hint()
            )
            dataclass_field = format_dataclass_field(
                type=field.type,
                default=None,
                optional=False,
                # TODO: Support sequences of entity types.
                entity_type=None,
            )
            class_fields.append(
                f"    {to_snake_case(field.name)}: "
                f"tuple[{inner_type_hint}, ...] "
                f"{dataclass_field}\n"
            )
        elif isinstance(field, EntityArrayField):
            yield from generate_dataclass(
                schema=schema,
                name=str(field.type),
                fields=field.fields,
                version=version,
            )
            class_fields.append(
                f"    {to_snake_case(field.name)}: tuple[{field.type}, ...]\n"
            )
        elif isinstance(field, EntityField):
            yield from generate_dataclass(
                schema=schema,
                name=str(field.type),
                fields=field.fields,
                version=version,
            )
            class_fields.append(f"    {to_snake_case(field.name)}: {field.type}\n")
        elif isinstance(field, CommonStructArrayField):
            yield from generate_dataclass(
                schema=schema,
                name=field.type.type.name,
                fields=field.type.type.fields,
                version=version,
            )
            class_fields.append(
                f"    {to_snake_case(field.name)}: tuple[{field.type.type.name}, ...]\n"
            )
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
) -> Iterator[tuple[int, str | EntityTypeDef]]:
    for version in schema.validVersions.iter():
        accumulated_code = ""
        for item in generate_dataclass(
            schema=schema,
            name=schema.name,
            fields=schema.fields,
            version=version,
        ):
            match item:
                case EntityTypeDef() as entity_type:
                    yield version, entity_type
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


seen_entitites = set[str]()
entity_imports = """\
from typing import NewType
from kio.schema.primitive import i8, i16, i32, i64, u8, u16, u32, u64, f64
from phantom import Phantom
"""


def write_entity_type(path: pathlib.Path, entity_type: EntityTypeDef) -> None:
    write_imports = not path.exists()
    if entity_type.name in seen_entitites:
        return
    seen_entitites.add(entity_type.name)
    with path.open("a") as fd:
        if write_imports:
            print(entity_imports, file=fd)
        print(entity_type.get_definition(), file=fd)


SchemaType: TypeAlias = Literal["request", "response", "header", "data"]
module_entity_dependencies = defaultdict[tuple[int, SchemaType], list[EntityTypeDef]](
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
                case (version, EntityTypeDef() as entity_type):
                    module_entity_dependencies[(version, schema.type)].append(
                        entity_type
                    )
                    write_entity_type(types_module_path, entity_type)
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
