from dataclasses import dataclass
from dataclasses import fields
from datetime import timedelta
from uuid import UUID

import pytest

from kio.schema.types import BrokerId
from kio.schema.types import GroupId
from kio.schema.types import ProducerId
from kio.schema.types import TopicName
from kio.schema.types import TransactionalId
from kio.serial._implicit_defaults import get_implicit_default
from kio.serial._implicit_defaults import get_tagged_field_default
from kio.serial.readers import tz_aware_from_i64
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


class TestGetImplicitDefault:
    @pytest.mark.parametrize(
        ("annotation", "expected"),
        (
            (u8, 0),
            (u16, 0),
            (u32, 0),
            (u64, 0),
            (i8, 0),
            (i16, 0),
            (i32, 0),
            (i64, 0),
            (f64, 0.0),
            (i32Timedelta, timedelta(0)),
            (i64Timedelta, timedelta(0)),
            (TZAware, tz_aware_from_i64(i64(0))),
            (UUID, UUID(int=0)),
            (str, ""),
            (bytes, b""),
            (BrokerId, 0),
            (GroupId, ""),
            (ProducerId, 0),
            (TopicName, ""),
            (TransactionalId, ""),
        ),
    )
    def test_returns_expected_value(self, annotation: type, expected: object) -> None:
        assert get_implicit_default(annotation) == expected

    def test_raises_not_implemented_error_for_records(self) -> None:
        with pytest.raises(NotImplementedError):
            get_implicit_default(Records)


class TestGetTaggedFieldDefault:
    def test_raises_type_error_for_optional_field(self) -> None:
        @dataclass
        class A:
            a: u8 | None

        [field] = fields(A)

        with pytest.raises(
            TypeError,
            match=r"Optional fields should have None as explicit default",
        ):
            get_tagged_field_default(field)

    def test_raises_type_error_for_tuple_field(self) -> None:
        @dataclass
        class A:
            a: tuple[u8, ...]

        [field] = fields(A)

        with pytest.raises(
            TypeError,
            match=r"Tuple fields should have the empty tuple as explicit default",
        ):
            get_tagged_field_default(field)

    def test_can_get_default_for_primitive_field(self) -> None:
        @dataclass
        class A:
            a: u8

        [field] = fields(A)
        assert get_tagged_field_default(field) == 0

    def test_can_get_default_for_entity_field(self) -> None:
        @dataclass
        class A:
            a: u8

        @dataclass
        class B:
            b: A

        [field] = fields(B)
        assert get_tagged_field_default(field) == A(a=u8(0))

    def test_returns_explicit_default_if_defined(self) -> None:
        @dataclass
        class A:
            a: u8 = u8(1)

        [field] = fields(A)
        assert get_tagged_field_default(field) == u8(1)
