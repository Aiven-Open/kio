from dataclasses import Field
from dataclasses import dataclass
from dataclasses import field
from dataclasses import fields
from uuid import UUID

import pytest

from kio.serial._introspect import FieldKind
from kio.serial._introspect import classify_field
from kio.serial._introspect import get_schema_field_type
from kio.serial._introspect import is_optional
from kio.serial.errors import SchemaError


@dataclass
class Nested: ...


@dataclass
class A:
    missing_kafka_type: int
    invalid_kafka_type: int = field(metadata={"kafka_type": 123})
    valid_kafka_type: int = field(metadata={"kafka_type": "some_type"})

    none_union: int
    verbose_union_with_none: int | None
    verbose_union_without_none: int | str
    pep_604_union_with_none: int | None
    pep_604_union_without_none: int | str

    primitive: int
    primitive_tuple: tuple[int, ...]
    primitive_tuple_optional: tuple[int | None, ...]
    entity: Nested
    entity_tuple: tuple[Nested, ...]
    nullable_entity: Nested | None
    nullable_entity_tuple: tuple[Nested, ...] | None
    backwards_nullable_entity: None | Nested
    unsupported_tuple: tuple[int, str]
    unsupported_union: int | str | bool

    uuid_or_none: UUID | None


model_fields = {field.name: field for field in fields(A)}


class TestGetSchemaFieldType:
    def test_raises_schema_error_for_missing_kafka_type(self) -> None:
        with pytest.raises(SchemaError, match=r"^Missing `kafka_type` in metadata"):
            get_schema_field_type(model_fields["missing_kafka_type"])

    def test_raises_schema_error_for_invalid_kafka_type_value(self) -> None:
        with pytest.raises(SchemaError, match=r"^`kafka_type` must be of type str"):
            get_schema_field_type(model_fields["invalid_kafka_type"])

    def test_returns_valid_kafka_type(self) -> None:
        assert get_schema_field_type(model_fields["valid_kafka_type"]) == "some_type"


class TestIsOptional:
    def test_returns_false_for_none_union_type(self) -> None:
        assert is_optional(model_fields["none_union"]) is False

    def test_returns_true_for_verbose_union_with_none(self) -> None:
        assert is_optional(model_fields["verbose_union_with_none"]) is True

    def test_returns_true_for_pep_604_union_with_none(self) -> None:
        assert is_optional(model_fields["pep_604_union_with_none"]) is True

    def test_returns_true_for_inner_optional(self) -> None:
        assert is_optional(model_fields["primitive_tuple_optional"]) is True

    def test_returns_false_for_verbose_union_without_none(self) -> None:
        assert is_optional(model_fields["verbose_union_without_none"]) is False

    def test_returns_false_for_pep_604_union_without_none(self) -> None:
        assert is_optional(model_fields["pep_604_union_without_none"]) is False

    def test_returns_false_for_non_nullable_entity(self) -> None:
        assert is_optional(model_fields["entity"]) is False

    def test_returns_true_for_nullable_entity(self) -> None:
        assert is_optional(model_fields["nullable_entity"]) is True

    def test_returns_true_for_nullable_entity_tuple(self) -> None:
        assert is_optional(model_fields["nullable_entity_tuple"]) is True

    def test_returns_true_for_nullable_uuid(self) -> None:
        assert is_optional(model_fields["uuid_or_none"]) is True

    def test_raises_schema_error_for_invalid_tuple_type(self) -> None:
        with pytest.raises(SchemaError, match=r"has invalid tuple type"):
            is_optional(model_fields["unsupported_tuple"])


class TestClassifyField:
    def test_raises_schema_error_for_invalid_tuple_type(self) -> None:
        with pytest.raises(SchemaError, match=r"has invalid tuple type"):
            classify_field(model_fields["unsupported_tuple"])

    def test_raises_schema_error_for_invalid_union_type(self) -> None:
        with pytest.raises(SchemaError, match=r"has unsupported union type"):
            classify_field(model_fields["unsupported_union"])

    def test_raises_schema_error_for_non_none_union(self) -> None:
        with pytest.raises(SchemaError, match=r"Only union with None is supported"):
            classify_field(model_fields["verbose_union_without_none"])

    def test_can_classify_primitive_field(self) -> None:
        assert classify_field(model_fields["primitive"]) == (FieldKind.primitive, int)

    def test_can_classify_primitive_tuple_field(self) -> None:
        assert classify_field(model_fields["primitive_tuple"]) == (
            FieldKind.primitive_tuple,
            int,
        )

    def test_can_classify_entity_tuple_field(self) -> None:
        assert classify_field(model_fields["entity_tuple"]) == (
            FieldKind.entity_tuple,
            Nested,
        )

    def test_can_classify_nullable_nested_entity_tuple(self) -> None:
        assert classify_field(model_fields["nullable_entity_tuple"]) == (
            FieldKind.entity_tuple,
            Nested,
        )

    def test_can_classify_simple_nested_entity(self) -> None:
        assert classify_field(model_fields["entity"]) == (FieldKind.entity, Nested)

    # See KIP-893.
    @pytest.mark.parametrize(
        "field",
        (
            model_fields["nullable_entity"],
            model_fields["backwards_nullable_entity"],
        ),
    )
    def test_can_classify_nullable_nested_entity(self, field: Field) -> None:
        assert classify_field(field) == (FieldKind.entity, Nested)

    def test_can_classify_uuid_or_none(self) -> None:
        assert classify_field(model_fields["uuid_or_none"]) == (
            FieldKind.primitive,
            UUID,
        )
