from typing import Union
from dataclasses import dataclass, field, fields

import pytest

from kio.serial.errors import SchemaError
from kio.serial.introspect import get_schema_field_type, is_optional


@dataclass
class A:
    missing_kafka_type: int
    invalid_kafka_type: int = field(metadata={"kafka_type": 123})
    valid_kafka_type: int = field(metadata={"kafka_type": "some_type"})

    none_union: int
    verbose_union_with_none: Union[int, None]
    verbose_union_without_none: Union[int, str]
    pep_604_union_with_none: int | None
    pep_604_union_without_none: int | str


model_fields = {field.name: field for field in fields(A)}


class TestGetSchemaFieldType:
    def test_raises_schema_error_for_missing_kafka_type(self):
        with pytest.raises(SchemaError, match=r"^Missing `kafka_type` in metadata"):
            get_schema_field_type(model_fields["missing_kafka_type"])

    def test_raises_schema_error_for_invalid_kafka_type_value(self):
        with pytest.raises(SchemaError, match=r"^`kafka_type` must be of type str"):
            get_schema_field_type(model_fields["invalid_kafka_type"])

    def test_returns_valid_kafka_type(self):
        assert get_schema_field_type(model_fields["valid_kafka_type"]) == "some_type"


class TestIsOptional:
    def test_returns_false_for_none_union_type(self):
        assert is_optional(model_fields["none_union"]) is False

    def test_returns_true_for_verbose_union_with_none(self):
        assert is_optional(model_fields["verbose_union_with_none"]) is True

    def test_returns_true_for_pep_604_union_with_none(self):
        assert is_optional(model_fields["pep_604_union_with_none"]) is True

    def test_returns_false_for_verbose_union_without_none(self):
        assert is_optional(model_fields["verbose_union_without_none"]) is False

    def test_returns_false_for_pep_604_union_without_none(self):
        assert is_optional(model_fields["pep_604_union_without_none"]) is False
