# https://cwiki.apache.org/confluence/display/KAFKA/KIP-98+-+Exactly+Once+Delivery+and+Transactional+Messaging#KIP98ExactlyOnceDeliveryandTransactionalMessaging-MessageFormat
# https://kafka.apache.org/documentation/#messageformat
import datetime

from typing import TypeVar

from crc32c import crc32c
from typing_extensions import Buffer

from kio.serial.readers import Reader
from kio.serial.readers import SizedResult
from kio.serial.readers import read_int8
from kio.serial.readers import read_int16
from kio.serial.readers import read_int32
from kio.serial.readers import read_int64
from kio.serial.readers import read_signed_varint
from kio.serial.readers import read_signed_varlong
from kio.serial.readers import read_uint32
from kio.static.primitive import TZAwareMicros
from kio.static.primitive import i64

from .schema import Record
from .schema import RecordBatch
from .schema import RecordHeader


def read_signed_compact_string_as_bytes_nullable(
    buffer: Buffer,
    offset: int,
) -> SizedResult[bytes | None]:
    string_length, length_size = read_signed_varint(buffer, offset)
    if string_length == -1:
        return None, length_size
    elif string_length < 0:
        raise ValueError(f"Invalid length for signed compact string: {string_length}")
    string_start_offset = offset + length_size
    string_end_offset = string_start_offset + string_length
    return (
        bytes(memoryview(buffer))[string_start_offset:string_end_offset],
        length_size + string_length,
    )


T = TypeVar("T")


def _read_add_size(
    buffer: Buffer,
    offset: int,
    reader: Reader[T],
) -> tuple[T, int]:
    value, size = reader(buffer, offset)
    return value, offset + size


def read_header(buffer: Buffer, offset: int) -> SizedResult[RecordHeader]:
    key, key_size = read_signed_compact_string_as_bytes_nullable(buffer, offset)
    value, value_size = read_signed_compact_string_as_bytes_nullable(
        buffer,
        offset + key_size,
    )
    return RecordHeader(key=key, value=value), key_size + value_size


def read_record(
    buffer: Buffer,
    base_timestamp: i64,
    base_offset: i64,
    offset: int,
) -> SizedResult[Record]:
    start_offset = offset
    record_length, offset = _read_add_size(buffer, offset, read_signed_varint)
    length_start_offset = offset
    attributes, offset = _read_add_size(buffer, offset, read_int8)
    timestamp_value, offset = _read_add_size(buffer, offset, read_signed_varlong)
    offset_value, offset = _read_add_size(buffer, offset, read_signed_varint)
    key, offset = _read_add_size(
        buffer,
        offset,
        read_signed_compact_string_as_bytes_nullable,
    )
    value, offset = _read_add_size(
        buffer,
        offset,
        read_signed_compact_string_as_bytes_nullable,
    )
    headers_length, offset = _read_add_size(buffer, offset, read_signed_varint)
    headers = []
    for _ in range(headers_length):
        header, offset = _read_add_size(buffer, offset, read_header)
        headers.append(header)

    if offset != length_start_offset + record_length:
        raise ValueError(
            "Record data contains inconsistently sized data that does not match the "
            "record length"
        )

    return (
        Record(
            attributes=attributes,
            timestamp=TZAwareMicros.parse(
                datetime.datetime.fromtimestamp(
                    (base_timestamp + timestamp_value) / 1000,
                    datetime.UTC,
                ).replace(microsecond=0)
            ),
            offset=i64(base_offset + offset_value),
            key=key,
            value=value,
            headers=tuple(headers),
        ),
        offset - start_offset,
    )


def read_batch(buffer: Buffer, offset: int) -> SizedResult[RecordBatch]:
    start_offset = offset
    base_offset, offset = _read_add_size(buffer, offset, read_int64)
    batch_length, offset = _read_add_size(buffer, offset, read_int32)
    # Keep track of "batch start" to validate byte length adds up.
    batch_start_offset = offset

    partition_leader_epoch, offset = _read_add_size(buffer, offset, read_int32)
    # Read and validate magic byte.
    magic_byte, offset = _read_add_size(buffer, offset, read_int8)
    if magic_byte != RecordBatch.magic:
        raise ValueError("Expected record batch magic byte == 2")

    # Read checksum, then calculate checksum of rest of batch and verify it against
    # the read value.
    crc, offset = _read_add_size(buffer, offset, read_uint32)
    if crc != crc32c(memoryview(buffer)[offset : batch_start_offset + batch_length]):
        raise ValueError("Checksum mismatch when reading record batch")

    attributes, offset = _read_add_size(buffer, offset, read_int16)
    last_offset_delta, offset = _read_add_size(buffer, offset, read_int32)
    base_timestamp, offset = _read_add_size(buffer, offset, read_int64)
    max_timestamp, offset = _read_add_size(buffer, offset, read_int64)
    producer_id, offset = _read_add_size(buffer, offset, read_int64)
    producer_epoch, offset = _read_add_size(buffer, offset, read_int16)
    base_sequence, offset = _read_add_size(buffer, offset, read_int32)

    num_records, offset = _read_add_size(buffer, offset, read_int32)
    records = []
    for _ in range(num_records):
        record, size = read_record(buffer, base_timestamp, base_offset, offset)
        offset += size
        if record.timestamp.timestamp() > max_timestamp:
            raise ValueError("Record has timestamp larger than batch max timestamp")
        records.append(record)

    if offset != batch_start_offset + batch_length:
        raise ValueError(
            "Record batch data contains inconsistently sized data that does not match "
            "the batch length"
        )

    return RecordBatch(
        base_offset=base_offset,
        batch_length=batch_length,
        partition_leader_epoch=partition_leader_epoch,
        crc=crc,
        attributes=attributes,
        last_offset_delta=last_offset_delta,
        base_timestamp=base_timestamp,
        max_timestamp=max_timestamp,
        producer_id=producer_id,
        producer_epoch=producer_epoch,
        base_sequence=base_sequence,
        records=tuple(records),
    ), offset - start_offset
