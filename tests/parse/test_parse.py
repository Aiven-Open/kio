import io

import pytest

from kio.serial.encoders import write_int32, write_compact_string, write_legacy_string
from kio.serial.parse import get_decoder, parse
from kio.serial import decoders
from kio.schema.metadata.response.v12 import MetadataResponseBroker as MetadataResponseBrokerV12
from kio.schema.metadata.response.v5 import MetadataResponseBroker as MetadataResponseBrokerV5


class TestGetDecoder:
    @pytest.mark.parametrize(
        "kafka_type, flexible, optional, expected",
        (
            ("int8", True, False, decoders.decode_int8),
            ("int8", False, False, decoders.decode_int8),
            ("int16", True, False, decoders.decode_int16),
            ("int16", False, False, decoders.decode_int16),
            ("int32", True, False, decoders.decode_int32),
            ("int32", False, False, decoders.decode_int32),
            ("int64", True, False, decoders.decode_int64),
            ("int64", False, False, decoders.decode_int64),
            ("uint8", True, False, decoders.decode_uint8),
            ("uint8", False, False, decoders.decode_uint8),
            ("uint16", True, False, decoders.decode_uint16),
            ("uint16", False, False, decoders.decode_uint16),
            ("uint32", True, False, decoders.decode_uint32),
            ("uint32", False, False, decoders.decode_uint32),
            ("uint64", True, False, decoders.decode_uint64),
            ("uint64", False, False, decoders.decode_uint64),
            ("string", True, False, decoders.decode_compact_string),
            ("string", True, True, decoders.decode_compact_string_nullable),
            ("string", False, False, decoders.decode_string),
            ("string", False, True, decoders.decode_string_nullable),
        )
    )
    def test_can_match_kafka_type_with_decoder(
        self,
        kafka_type: str,
        flexible: bool,
        optional: bool,
        expected: decoders.Decoder,
    ) -> None:
        assert get_decoder(kafka_type, flexible, optional) == expected

    @pytest.mark.parametrize(
        "kafka_type, flexible, optional",
        (
            ("int32", True, True),
            ("int32", False, True),
        )
    )
    def test_raises_not_implemented_error_for_invalid_combination(
        self,
        kafka_type: str,
        flexible: bool,
        optional: bool,
    ) -> None:
        with pytest.raises(NotImplementedError):
            get_decoder(kafka_type, flexible, optional)


def test_can_parse_entity(buffer: io.BytesIO) -> None:
    assert MetadataResponseBrokerV12.__flexible__
    # node_id
    write_int32(buffer, 123)
    # host
    write_compact_string(buffer, "kafka.aiven.test")
    # port
    write_int32(buffer, 23_126)
    # rack
    write_compact_string(buffer, "da best")

    buffer.seek(0)
    instance = parse(buffer, MetadataResponseBrokerV12)
    assert isinstance(instance, MetadataResponseBrokerV12)

    assert instance.node_id == 123
    assert instance.host == "kafka.aiven.test"
    assert instance.port == 23_126
    assert instance.rack == "da best"


def test_can_parse_legacy_entity(buffer: io.BytesIO) -> None:
    assert not MetadataResponseBrokerV5.__flexible__
    # node_id
    write_int32(buffer, 123)
    # host
    write_legacy_string(buffer, "kafka.aiven.test")
    # port
    write_int32(buffer, 23_126)
    # rack
    write_legacy_string(buffer, "da best")

    buffer.seek(0)
    instance = parse(buffer, MetadataResponseBrokerV5)
    assert isinstance(instance, MetadataResponseBrokerV5)

    assert instance.node_id == 123
    assert instance.host == "kafka.aiven.test"
    assert instance.port == 23_126
    assert instance.rack == "da best"

