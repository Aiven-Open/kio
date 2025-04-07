import datetime

from typing import IO

import pytest

from kio.records.readers import read_batch
from kio.records.readers import read_header
from kio.records.readers import read_signed_compact_string_as_bytes_nullable
from kio.records.schema import Record
from kio.records.schema import RecordBatch
from kio.records.schema import RecordHeader
from kio.records.writers import write_batch
from kio.serial.writers import write_int8
from kio.serial.writers import write_int16
from kio.serial.writers import write_int32
from kio.serial.writers import write_int64
from kio.serial.writers import write_signed_varint
from kio.serial.writers import write_uint32
from kio.static.primitive import TZAwareMicros
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i64
from kio.static.primitive import u32

from .fixtures import record_batch_data_v2


class TestReadSignedCompactStringAsBytesNullable:
    def test_can_read_bytes(self, buffer: IO[bytes]) -> None:
        write_signed_varint(buffer, 5)
        buffer.write(b"abcde")
        buffer.seek(0)
        assert read_signed_compact_string_as_bytes_nullable(buffer) == b"abcde"

    def test_returns_none_for_length_minus_one(self, buffer: IO[bytes]) -> None:
        write_signed_varint(buffer, -1)
        buffer.seek(0)
        assert read_signed_compact_string_as_bytes_nullable(buffer) is None

    def test_raises_value_error_for_negative_length(self, buffer: IO[bytes]) -> None:
        write_signed_varint(buffer, -2)
        buffer.seek(0)
        with pytest.raises(
            ValueError,
            match=r"^Invalid length for signed compact string: -2$",
        ):
            read_signed_compact_string_as_bytes_nullable(buffer)


def test_read_header(buffer: IO[bytes]) -> None:
    write_signed_varint(buffer, 5)
    buffer.write(b"abcde")
    write_signed_varint(buffer, 5)
    buffer.write(b"bcdef")
    buffer.seek(0)
    assert read_header(buffer) == RecordHeader(
        key=b"abcde",
        value=b"bcdef",
    )


class TestReadBatch:
    def test_can_read_record_batches(self, buffer: IO[bytes]) -> None:
        buffer.write(b"".join(record_batch_data_v2))
        buffer.seek(0)

        batch = read_batch(buffer)
        assert batch.base_offset == 0
        assert batch.batch_length == 59
        assert batch.partition_leader_epoch == 1
        assert batch.crc == 51946096
        assert batch.attributes == 0
        assert batch.last_offset_delta == 0
        assert batch.base_timestamp == 1503229838908
        assert batch.max_timestamp == 1503229838908
        assert batch.producer_id == -1
        assert batch.producer_epoch == -1
        assert batch.base_sequence == -1
        (record,) = batch.records
        assert record.attributes == 0
        assert record.timestamp == datetime.datetime(
            2017, 8, 20, 11, 50, 38, tzinfo=datetime.UTC
        )
        assert record.offset == 0
        assert record.key is None
        assert record.value == b"123"
        assert record.headers == ()

        batch = read_batch(buffer)
        assert batch.base_offset == 1
        assert batch.batch_length == 64
        assert batch.partition_leader_epoch == 2
        assert batch.crc == 3361520931
        assert batch.attributes == 0
        assert batch.last_offset_delta == 1
        assert batch.base_timestamp == 1503229959532
        assert batch.max_timestamp == 1503229959700
        assert batch.producer_id == -1
        assert batch.producer_epoch == -1
        assert batch.base_sequence == -1
        first_record, second_record = batch.records
        assert first_record.attributes == 0
        assert first_record.timestamp == datetime.datetime(
            2017, 8, 20, 11, 52, 39, tzinfo=datetime.UTC
        )
        assert first_record.offset == 1
        assert first_record.key is None
        assert first_record.value == b""
        assert first_record.headers == ()
        assert second_record.attributes == 0
        assert second_record.timestamp == datetime.datetime(
            2017, 8, 20, 11, 52, 39, tzinfo=datetime.UTC
        )
        assert second_record.offset == 2
        assert second_record.key is None
        assert second_record.value == b""
        assert second_record.headers == ()

        batch = read_batch(buffer)
        assert batch.base_offset == 3
        assert batch.batch_length == 59
        assert batch.partition_leader_epoch == 2
        assert batch.crc == 772507063
        assert batch.attributes == 0
        assert batch.last_offset_delta == 0
        assert batch.base_timestamp == 1503229962141
        assert batch.max_timestamp == 1503229962141
        assert batch.producer_id == -1
        assert batch.producer_epoch == -1
        assert batch.base_sequence == -1
        (record,) = batch.records
        assert record.attributes == 0
        assert record.timestamp == datetime.datetime(
            2017, 8, 20, 11, 52, 42, tzinfo=datetime.UTC
        )
        assert record.offset == 3
        assert record.key is None
        assert record.value == b"123"
        assert record.headers == ()

        batch = read_batch(buffer)
        assert batch.base_offset == 0
        assert batch.batch_length == 69
        assert batch.partition_leader_epoch == 0
        assert batch.crc == 1557720914
        assert batch.attributes == 0
        assert batch.last_offset_delta == 0
        assert batch.base_timestamp == 1535546684353
        assert batch.max_timestamp == 1535546684353
        assert batch.producer_id == -1
        assert batch.producer_epoch == -1
        assert batch.base_sequence == -1
        (record,) = batch.records
        assert record.attributes == 0
        assert record.timestamp == datetime.datetime(
            2018, 8, 29, 12, 44, 44, tzinfo=datetime.UTC
        )
        assert record.offset == 0
        assert record.key is None
        assert record.value == b"hdr"
        (header,) = record.headers
        assert header.key == b"hkey"
        assert header.value == b"hval"

    def test_raises_value_error_for_unrecognized_magic_byte(
        self,
        buffer: IO[bytes],
    ) -> None:
        # base offset
        write_int64(buffer, i64(0))
        # batch length
        write_int32(buffer, i32(5))
        # partition leader epoch
        write_int32(buffer, i32(0))
        # magic byte value
        write_int8(buffer, i8(RecordBatch.magic - 1))

        buffer.seek(0)

        with pytest.raises(
            ValueError,
            match=r"^Expected record batch magic byte == 2$",
        ):
            read_batch(buffer)

    def test_raises_value_error_for_checksum_mismatch(self, buffer: IO[bytes]) -> None:
        # base offset
        write_int64(buffer, i64(0))
        # batch length
        write_int32(buffer, i32(15))
        # partition leader epoch
        write_int32(buffer, i32(0))
        # magic byte value
        write_int8(buffer, RecordBatch.magic)
        # crc
        write_uint32(buffer, u32(0))
        # attributes
        write_int16(buffer, i16(0))
        # last offset delta
        write_int32(buffer, i32(0))

        buffer.seek(0)

        with pytest.raises(
            ValueError,
            match=r"^Checksum mismatch when reading record batch$",
        ):
            read_batch(buffer)

    def test_raises_value_error_for_timestamp_larger_than_max(
        self,
        buffer: IO[bytes],
    ) -> None:
        write_batch(
            buffer,
            RecordBatch(
                base_offset=i64(0),
                batch_length=i32(60),
                partition_leader_epoch=i16(0),
                crc=u32(3388129145),
                attributes=i16(0),
                last_offset_delta=i32(0),
                base_timestamp=i64(0),
                max_timestamp=i64(0),
                producer_id=i64(0),
                producer_epoch=i16(0),
                base_sequence=i32(0),
                records=(
                    Record(
                        attributes=i8(0),
                        timestamp=TZAwareMicros.parse(
                            datetime.datetime(1970, 1, 1, 1, tzinfo=datetime.UTC)
                        ),
                        offset=i64(0),
                        key=None,
                        value=None,
                        headers=(),
                    ),
                ),
            ),
        )

        buffer.seek(0)

        with pytest.raises(
            ValueError,
            match=r"^Record has timestamp larger than batch max timestamp$",
        ):
            read_batch(buffer)
