from __future__ import annotations

from collections.abc import Mapping
from dataclasses import MISSING
from dataclasses import Field
from dataclasses import fields
from datetime import timedelta
from types import MappingProxyType
from typing import Final
from typing import TypeVar
from typing import assert_never
from uuid import UUID

from kio.serial._introspect import EntityField
from kio.serial._introspect import EntityTupleField
from kio.serial._introspect import PrimitiveField
from kio.serial._introspect import PrimitiveTupleField
from kio.serial._introspect import classify_field
from kio.serial._introspect import is_optional
from kio.serial.readers import tz_aware_from_i64
from kio.static.constants import uuid_zero
from kio.static.primitive import Records
from kio.static.primitive import TZAware
from kio.static.primitive import f64
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta
from kio.static.primitive import i64
from kio.static.primitive import i64Timedelta
from kio.static.primitive import u8
from kio.static.primitive import u16
from kio.static.primitive import u32
from kio.static.primitive import u64
from kio.static.protocol import Entity

T = TypeVar("T")

primitive_implicit_defaults: Final[Mapping[type, object]] = MappingProxyType(
    {
        u8: u8(0),
        u16: u16(0),
        u32: u32(0),
        u64: u64(0),
        i8: i8(0),
        i16: i16(0),
        i32: i32(0),
        i64: i64(0),
        f64: f64(0.0),
        i32Timedelta: i32Timedelta.parse(timedelta(0)),
        i64Timedelta: i64Timedelta.parse(timedelta(0)),
        TZAware: tz_aware_from_i64(i64(0)),
        UUID: uuid_zero,
        str: "",
        bytes: b"",
    }
)


def get_implicit_default(field_type: type[T]) -> T:
    # Records fields have null as implicit default, supporting this requires changing
    # code generation to always expect null for a tagged records field. As of writing
    # there are no tagged records fields, or other occurrences where we would need such
    # implicit default, so this can be safely deferred.
    if issubclass(field_type, Records):
        raise NotImplementedError("Tagged record fields are not supported")

    try:
        # mypy has no way of typing a mapping as T -> T on a per-item level.
        return primitive_implicit_defaults[field_type]  # type: ignore[return-value]
    except KeyError:
        return primitive_implicit_defaults[field_type.__bases__[0]]  # type: ignore[return-value]


U = TypeVar("U", bound=Entity)


def get_tagged_field_default(field: Field[U]) -> U:
    if field.default is not MISSING:
        return field.default

    if is_optional(field):
        raise TypeError("Optional fields should have None as explicit default")

    field_class = classify_field(field)

    if isinstance(field_class, PrimitiveField):
        return get_implicit_default(field_class.type_)
    elif isinstance(field_class, EntityField):
        return field.type(
            **{
                nested_field.name: get_tagged_field_default(nested_field)
                for nested_field in fields(field.type)
            }
        )
    elif isinstance(field_class, PrimitiveTupleField | EntityTupleField):
        raise TypeError("Tuple fields should have the empty tuple as explicit default")

    assert_never(field_class)
