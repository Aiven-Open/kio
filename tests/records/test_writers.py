import datetime
import io

import pytest

from kio.records.schema import NewRecordBatch
from kio.records.schema import Record
from kio.records.schema import RecordBatch
from kio.records.schema import RecordHeader
from kio.records.writers import write_batch
from kio.static.primitive import TZAwareMicros
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i64
from kio.static.primitive import u32

from .fixtures import record_batch_data_v2


def test_write_record_batch() -> None:
    expected_result = b"".join(record_batch_data_v2)
    batches = [
        RecordBatch(
            base_offset=i64(0),
            batch_length=i32(59),
            partition_leader_epoch=i32(1),
            crc=u32(51946096),
            attributes=i16(0),
            last_offset_delta=i32(0),
            base_timestamp=i64(1503229838908),
            max_timestamp=i64(1503229838908),
            producer_id=i64(-1),
            producer_epoch=i16(-1),
            base_sequence=i32(-1),
            records=(
                Record(
                    attributes=i8(0),
                    timestamp=TZAwareMicros.parse(
                        datetime.datetime(
                            2017, 8, 20, 11, 50, 38, 908000, tzinfo=datetime.UTC
                        )
                    ),
                    offset=i64(0),
                    key=None,
                    value=b"123",
                    headers=(),
                ),
            ),
        ),
        RecordBatch(
            base_offset=i64(1),
            batch_length=i32(64),
            partition_leader_epoch=i32(2),
            crc=u32(3361520931),
            attributes=i16(0),
            last_offset_delta=i32(1),
            base_timestamp=i64(1503229959532),
            max_timestamp=i64(1503229959700),
            producer_id=i64(-1),
            producer_epoch=i16(-1),
            base_sequence=i32(-1),
            records=(
                Record(
                    attributes=i8(0),
                    timestamp=TZAwareMicros.parse(
                        datetime.datetime(
                            2017, 8, 20, 11, 52, 39, 532000, tzinfo=datetime.UTC
                        )
                    ),
                    offset=i64(1),
                    key=None,
                    value=b"",
                    headers=(),
                ),
                Record(
                    attributes=i8(0),
                    timestamp=TZAwareMicros.parse(
                        datetime.datetime(
                            2017, 8, 20, 11, 52, 39, 700000, tzinfo=datetime.UTC
                        )
                    ),
                    offset=i64(2),
                    key=None,
                    value=b"",
                    headers=(),
                ),
            ),
        ),
        RecordBatch(
            base_offset=i64(3),
            batch_length=i32(59),
            partition_leader_epoch=i32(2),
            crc=u32(772507063),
            attributes=i16(0),
            last_offset_delta=i32(0),
            base_timestamp=i64(1503229962141),
            max_timestamp=i64(1503229962141),
            producer_id=i64(-1),
            producer_epoch=i16(-1),
            base_sequence=i32(-1),
            records=(
                Record(
                    attributes=i8(0),
                    timestamp=TZAwareMicros.parse(
                        datetime.datetime(
                            2017, 8, 20, 11, 52, 42, 141000, tzinfo=datetime.UTC
                        )
                    ),
                    offset=i64(3),
                    key=None,
                    value=b"123",
                    headers=(),
                ),
            ),
        ),
        RecordBatch(
            base_offset=i64(0),
            batch_length=i32(69),
            partition_leader_epoch=i32(0),
            crc=u32(1557720914),
            attributes=i16(0),
            last_offset_delta=i32(0),
            base_timestamp=i64(1535546684353),
            max_timestamp=i64(1535546684353),
            producer_id=i16(-1),
            producer_epoch=i16(-1),
            base_sequence=i32(-1),
            records=(
                Record(
                    attributes=i8(0),
                    timestamp=TZAwareMicros.parse(
                        datetime.datetime(
                            2018, 8, 29, 12, 44, 44, 353000, tzinfo=datetime.UTC
                        )
                    ),
                    offset=i64(0),
                    key=None,
                    value=b"hdr",
                    headers=(
                        RecordHeader(
                            key=b"hkey",
                            value=b"hval",
                        ),
                    ),
                ),
            ),
        ),
    ]

    with io.BytesIO() as buffer:
        for batch in batches:
            write_batch(buffer, batch)

        assert buffer.getvalue() == expected_result


# This was extracted by running the test_read_write_serde_v2 test from the
# kafka-python suite, with no compression.
# https://github.com/dpkp/kafka-python/blob/0864817de97549ad71e7bc2432c53108c5806cf1/test/record/test_default_records.py#L18
expected_bytes = (
    # baseOffset: int64
    b"\x00\x00\x00\x00\x00\x00\x00\x00"
    # batchLength: int32
    b"\x00\x00\x01\xc1"
    # partitionLeaderEpoch: int32
    b"\x00\x00\x00\x00"
    # magic: int8 (current magic value is 2)
    b"\x02"
    # crc: uint32
    b"\xd4D\x83L"
    # attributes: int16
    b"\x00\x10"
    # lastOffsetDelta: int32
    b"\x00\x00\x00\t"
    # baseTimestamp: int64
    b"\x00\x00\x00\x00\x00\x98\x96\x7f"
    # maxTimestamp: int64
    b"\x00\x00\x00\x00\x00\x98\x96\x7f"
    # producerId: int64
    b"\x00\x00\x00\x00\x00\x01\xe2@"
    # producerEpoch: int16
    b"\x00{"
    # baseSequence: int32
    b"\x00\x00'\x0f"
    # records
    b"\x00\x00\x00\n"
    b"N\x00\x00\x00\x08test\nSuper\x04\x0eheader1\x06aaa\x0eheader2\x06bbb"
    b"N\x00\x00\x02\x08test\nSuper\x04\x0eheader1\x06aaa\x0eheader2\x06bbb"
    b"N\x00\x00\x04\x08test\nSuper\x04\x0eheader1\x06aaa\x0eheader2\x06bbb"
    b"N\x00\x00\x06\x08test\nSuper\x04\x0eheader1\x06aaa\x0eheader2\x06bbb"
    b"N\x00\x00\x08\x08test\nSuper\x04\x0eheader1\x06aaa\x0eheader2\x06bbb"
    b"N\x00\x00\n\x08test\nSuper\x04\x0eheader1\x06aaa\x0eheader2\x06bbb"
    b"N\x00\x00\x0c\x08test\nSuper\x04\x0eheader1\x06aaa\x0eheader2\x06bbb"
    b"N\x00\x00\x0e\x08test\nSuper\x04\x0eheader1\x06aaa\x0eheader2\x06bbb"
    b"N\x00\x00\x10\x08test\nSuper\x04\x0eheader1\x06aaa\x0eheader2\x06bbb"
    b"N\x00\x00\x12\x08test\nSuper\x04\x0eheader1\x06aaa\x0eheader2\x06bbb"
)


def test_can_write_new_batch_like_kafka_python() -> None:
    batch = NewRecordBatch(
        producer_id=i64(123_456),
        producer_epoch=i16(123),
        base_sequence=i32(9_999),
        # 0b10000 because transactional=true
        attributes=i16(0b10000),
        records=tuple(
            Record(
                attributes=i8(0),
                timestamp=TZAwareMicros.parse(
                    datetime.datetime.fromtimestamp(9_999_999 / 1000, tz=datetime.UTC)
                ),
                offset=i64(offset),
                key=b"test",
                value=b"Super",
                headers=(
                    RecordHeader(key=b"header1", value=b"aaa"),
                    RecordHeader(key=b"header2", value=b"bbb"),
                ),
            )
            for offset in range(10)
        ),
    )

    with io.BytesIO() as buffer:
        write_batch(buffer, batch)
        assert buffer.getvalue() == expected_bytes


def test_write_new_batch_raises_value_error_for_empty_batch() -> None:
    batch = NewRecordBatch(
        producer_id=i64(123_456),
        producer_epoch=i16(123),
        base_sequence=i32(9_999),
        attributes=i16(0),
        records=(),
    )

    with (
        io.BytesIO() as buffer,
        pytest.raises(
            ValueError,
            match=r"^Need at least one record to construct batch$",
        ),
    ):
        write_batch(buffer, batch)


def test_can_write_existing_batch_like_kafka_python() -> None:
    batch = RecordBatch(
        base_offset=i64(0),
        batch_length=i32(449),
        partition_leader_epoch=i32(0),
        crc=u32(3_561_259_852),
        # 0b10000 because transactional=true
        attributes=i16(0b10000),
        last_offset_delta=i32(9),
        base_timestamp=i64(9_999_999),
        max_timestamp=i64(9_999_999),
        producer_id=i64(123_456),
        producer_epoch=i16(123),
        base_sequence=i32(9_999),
        records=tuple(
            Record(
                attributes=i8(0),
                timestamp=TZAwareMicros.parse(
                    datetime.datetime.fromtimestamp(9_999_999 / 1000, tz=datetime.UTC)
                ),
                offset=i64(offset),
                key=b"test",
                value=b"Super",
                headers=(
                    RecordHeader(key=b"header1", value=b"aaa"),
                    RecordHeader(key=b"header2", value=b"bbb"),
                ),
            )
            for offset in range(10)
        ),
    )

    with io.BytesIO() as buffer:
        write_batch(buffer, batch)
        assert buffer.getvalue() == expected_bytes
