import datetime
import io
from typing import IO

from kio.records.readers import read_batch
from kio.records.readers import read_signed_compact_string_as_bytes_nullable
from kio.serial.readers import read_int8
from kio.serial.readers import read_int16
from kio.serial.readers import read_int32
from kio.serial.readers import read_int64
from kio.serial.readers import read_signed_varint
from kio.serial.readers import read_signed_varlong
from kio.serial.readers import read_uint32

from .fixtures import record_batch_data_v2


# This is an artifact from discovery of the record batch format, should likely be
# removed.
def test_read_record_batch_primitive(buffer: IO[bytes]) -> None:
    buffer.write(b"".join(record_batch_data_v2))
    buffer.seek(0)

    assert read_int64(buffer) == 0  # base offset
    assert read_int32(buffer) == 59  # batch length
    assert read_int32(buffer) == 1  # partition leader epoch
    assert read_int8(buffer) == 2  # magic byte

    # fixme! python-kafka says this is unsigned, docs say signed ...
    #   ... comment in kafka impl also says unsigned.
    # assert read_int32(buffer) == 51946096  # crc
    assert read_uint32(buffer) == 51946096  # crc
    assert read_int16(buffer) == 0  # attributes
    assert read_int32(buffer) == 0  # last offset delta
    assert read_int64(buffer) == 1503229838908  # base timestamp
    assert read_int64(buffer) == 1503229838908  # max timestamp
    assert read_int64(buffer) == -1  # producer id
    assert read_int16(buffer) == -1  # producer epoch
    assert read_int32(buffer) == -1  # base sequence

    assert read_int32(buffer) == 1  # num records

    # single record ...
    record_length = read_signed_varint(buffer)
    assert record_length == 9

    record_buffer = io.BytesIO(buffer.read(record_length))

    assert read_int8(record_buffer) == 0  # attributes
    assert read_signed_varlong(record_buffer) == 0  # ts delta, varlong
    assert read_signed_varint(record_buffer) == 0  # offset delta, varint
    assert read_signed_compact_string_as_bytes_nullable(record_buffer) is None  # key
    assert read_signed_compact_string_as_bytes_nullable(record_buffer) == b"123"
    assert read_signed_varint(record_buffer) == 0  # num headers

    assert record_buffer.read(1) == b""  # record buffer exhausted

    # ---

    # second batch
    assert read_int64(buffer) == 1  # base offset
    assert read_int32(buffer) == 64  # batch length
    assert read_int32(buffer) == 2  # partition leader epoch
    assert read_int8(buffer) == 2  # magic byte

    assert read_uint32(buffer) == 3361520931  # crc
    assert read_int16(buffer) == 0  # attributes
    assert read_int32(buffer) == 1  # last offset delta
    assert read_int64(buffer) == 1503229959532  # base timestamp
    assert read_int64(buffer) == 1503229959700  # max timestamp
    assert read_int64(buffer) == -1  # producer id
    assert read_int16(buffer) == -1  # producer epoch
    assert read_int32(buffer) == -1  # base sequence

    assert read_int32(buffer) == 2  # num records

    # first record
    record_length = read_signed_varint(buffer)
    assert record_length == 6
    record_buffer = io.BytesIO(buffer.read(record_length))
    assert read_int8(record_buffer) == 0  # attributes
    assert read_signed_varlong(record_buffer) == 0  # ts delta, varlong
    assert read_signed_varint(record_buffer) == 0  # offset delta, varint
    assert read_signed_compact_string_as_bytes_nullable(record_buffer) is None  # key
    assert read_signed_compact_string_as_bytes_nullable(record_buffer) == b""
    assert read_signed_varint(record_buffer) == 0  # num headers
    assert record_buffer.read(1) == b""  # record buffer exhausted

    # second record
    record_length = read_signed_varint(buffer)
    assert record_length == 7
    record_buffer = io.BytesIO(buffer.read(record_length))
    assert read_int8(record_buffer) == 0  # attributes
    assert read_signed_varlong(record_buffer) == 168  # ts delta
    assert read_signed_varint(record_buffer) == 1  # offset delta
    assert read_signed_compact_string_as_bytes_nullable(record_buffer) is None  # key
    assert read_signed_compact_string_as_bytes_nullable(record_buffer) == b""
    assert read_signed_varint(record_buffer) == 0  # num headers
    assert record_buffer.read(1) == b""  # record buffer exhausted

    # ---

    # third batch
    assert read_int64(buffer) == 3  # base offset
    assert read_int32(buffer) == 59  # batch length
    assert read_int32(buffer) == 2  # partition leader epoch
    assert read_int8(buffer) == 2  # magic byte

    assert read_uint32(buffer) == 772507063  # crc
    assert read_int16(buffer) == 0  # attributes
    assert read_int32(buffer) == 0  # last offset delta
    assert read_int64(buffer) == 1503229962141  # base timestamp
    assert read_int64(buffer) == 1503229962141  # max timestamp
    assert read_int64(buffer) == -1  # producer id
    assert read_int16(buffer) == -1  # producer epoch
    assert read_int32(buffer) == -1  # base sequence

    assert read_int32(buffer) == 1  # num records

    # single record
    record_length = read_signed_varint(buffer)
    assert record_length == 9
    record_buffer = io.BytesIO(buffer.read(record_length))
    assert read_int8(record_buffer) == 0  # attributes
    assert read_signed_varlong(record_buffer) == 0  # ts delta, varlong
    assert read_signed_varint(record_buffer) == 0  # offset delta, varint
    assert read_signed_compact_string_as_bytes_nullable(record_buffer) is None  # key
    assert read_signed_compact_string_as_bytes_nullable(record_buffer) == b"123"
    assert read_signed_varint(record_buffer) == 0  # num headers
    assert record_buffer.read(1) == b""  # record buffer exhausted

    # ---

    # fourth batch
    assert read_int64(buffer) == 0  # base offset
    assert read_int32(buffer) == 69  # batch length
    assert read_int32(buffer) == 0  # partition leader epoch
    assert read_int8(buffer) == 2  # magic byte

    assert read_uint32(buffer) == 1557720914  # crc
    assert read_int16(buffer) == 0  # attributes
    assert read_int32(buffer) == 0  # last offset delta
    assert read_int64(buffer) == 1535546684353  # base timestamp
    assert read_int64(buffer) == 1535546684353  # max timestamp
    assert read_int64(buffer) == -1  # producer id
    assert read_int16(buffer) == -1  # producer epoch
    assert read_int32(buffer) == -1  # base sequence

    assert read_int32(buffer) == 1  # num records

    # single record
    record_length = read_signed_varint(buffer)
    assert record_length == 19
    record_buffer = io.BytesIO(buffer.read(record_length))
    assert read_int8(record_buffer) == 0  # attributes
    assert read_signed_varlong(record_buffer) == 0  # ts delta, varlong
    assert read_signed_varint(record_buffer) == 0  # offset delta, varint
    assert read_signed_compact_string_as_bytes_nullable(record_buffer) is None  # key
    assert read_signed_compact_string_as_bytes_nullable(record_buffer) == b"hdr"
    assert read_signed_varint(record_buffer) == 1  # num headers

    # single header
    assert read_signed_compact_string_as_bytes_nullable(record_buffer) == b"hkey"
    assert read_signed_compact_string_as_bytes_nullable(record_buffer) == b"hval"

    assert record_buffer.read(1) == b""  # record buffer exhausted


def test_read_record_batch(buffer: IO[bytes]) -> None:
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
        2017, 8, 20, 11, 50, 38, 908000, tzinfo=datetime.UTC
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
        2017, 8, 20, 11, 52, 39, 532000, tzinfo=datetime.UTC
    )
    assert first_record.offset == 1
    assert first_record.key is None
    assert first_record.value == b""
    assert first_record.headers == ()
    assert second_record.attributes == 0
    assert second_record.timestamp == datetime.datetime(
        2017, 8, 20, 11, 52, 39, 700000, tzinfo=datetime.UTC
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
        2017, 8, 20, 11, 52, 42, 141000, tzinfo=datetime.UTC
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
        2018, 8, 29, 12, 44, 44, 353000, tzinfo=datetime.UTC
    )
    assert record.offset == 0
    assert record.key is None
    assert record.value == b"hdr"
    (header,) = record.headers
    assert header.key == b"hkey"
    assert header.value == b"hval"
