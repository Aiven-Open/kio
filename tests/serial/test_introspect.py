from dataclasses import Field
from dataclasses import dataclass
from dataclasses import field
from dataclasses import fields

import pytest

from kio.serial.errors import SchemaError
from kio.serial.introspect import FieldKind
from kio.serial.introspect import classify_field
from kio.serial.introspect import get_schema_field_type
from kio.serial.introspect import is_optional


@dataclass
class Nested:
    ...


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

    simple_primitive: int
    complex_primitive: int | str
    primitive_tuple: tuple[int, ...]
    primitive_tuple_optional: tuple[int | None, ...]
    entity: Nested
    entity_tuple: tuple[Nested, ...]
    unsupported_tuple: tuple[int, str]


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


class TestClassifyField:
    def test_raises_schema_error_for_invalid_tuple_type(self) -> None:
        with pytest.raises(SchemaError, match=r"has invalid tuple type"):
            classify_field(model_fields["unsupported_tuple"])

    @pytest.mark.parametrize(
        "field",
        (
            model_fields["simple_primitive"],
            model_fields["complex_primitive"],
        ),
    )
    def test_can_classify_primitive_field(self, field: Field) -> None:
        assert classify_field(field) == (FieldKind.primitive, field.type)

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

    def test_can_classify_simple_nested_entity(self) -> None:
        assert classify_field(model_fields["entity"]) == (FieldKind.entity, Nested)
