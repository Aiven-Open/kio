from types import UnionType, NoneType
from typing import get_origin, Union, get_args
from dataclasses import Field
from .errors import MissingKafkaType


def get_schema_field_type(field: Field) -> str:
    try:
        return field.metadata["kafka_type"]
    except KeyError as exception:
        raise MissingKafkaType(
            f"Missing `kafka_type` in metadata for {field=}") from exception


def is_optional(field: Field) -> bool:
    if get_origin(field.type) not in [UnionType, Union]:
        return False
    return NoneType in get_args(field.type)
