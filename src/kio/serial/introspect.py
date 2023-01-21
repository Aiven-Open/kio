from dataclasses import Field
from types import NoneType
from types import UnionType
from typing import Union
from typing import get_args
from typing import get_origin

from .errors import SchemaError


def get_schema_field_type(field: Field) -> str:
    try:
        value = field.metadata["kafka_type"]
    except KeyError as exception:
        raise SchemaError(
            f"Missing `kafka_type` in metadata for {field=}"
        ) from exception
    if not isinstance(value, str):
        raise SchemaError(f"`kafka_type` must be of type str, found {type(value)}")
    return value


def is_optional(field: Field) -> bool:
    if get_origin(field.type) not in [UnionType, Union]:
        return False
    return NoneType in get_args(field.type)
