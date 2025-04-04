# https://cwiki.apache.org/confluence/display/KAFKA/KIP-98+-+Exactly+Once+Delivery+and+Transactional+Messaging#KIP98ExactlyOnceDeliveryandTransactionalMessaging-MessageFormat
# https://kafka.apache.org/documentation/#messageformat
import datetime
import io

from typing import IO

from crc32c import crc32c

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


def read_signed_compact_string_as_bytes_nullable(buffer: IO[bytes]) -> bytes | None:
    length = read_signed_varint(buffer)
    if length == -1:
        return None
    elif length < 0:
        raise ValueError(f"Invalid length for signed compact string: {length}")
    return buffer.read(length)


def read_header(buffer: IO[bytes]) -> RecordHeader:
    return RecordHeader(
        key=read_signed_compact_string_as_bytes_nullable(buffer),
        value=read_signed_compact_string_as_bytes_nullable(buffer),
    )


def read_record(
    buffer: IO[bytes],
    base_timestamp: i64,
    base_offset: i64,
) -> Record:
    record_length = read_signed_varint(buffer)
    with io.BytesIO(buffer.read(record_length)) as record_buffer:
        record = Record(
            attributes=read_int8(record_buffer),
            timestamp=TZAwareMicros.parse(
                datetime.datetime.fromtimestamp(
                    (base_timestamp + read_signed_varlong(record_buffer)) / 1000,
                    datetime.UTC,
                ).replace(microsecond=0)
            ),
            offset=i64(base_offset + read_signed_varint(record_buffer)),
            key=read_signed_compact_string_as_bytes_nullable(record_buffer),
            value=read_signed_compact_string_as_bytes_nullable(record_buffer),
            headers=tuple(
                read_header(record_buffer)
                for _ in range(read_signed_varint(record_buffer))
            ),
        )
        if record_buffer.read(1) != b"":  # pragma: no cover
            raise ValueError("Record buffer is not empty after reading full record")
    return record


def read_batch(buffer: IO[bytes]) -> RecordBatch:
    base_offset = read_int64(buffer)
    batch_length = read_int32(buffer)

    with io.BytesIO(buffer.read(batch_length)) as batch_buffer:
        partition_leader_epoch = read_int32(batch_buffer)

        # Read and validate magic byte.
        magic_byte = read_int8(batch_buffer)
        if magic_byte != RecordBatch.magic:
            raise ValueError("Expected record batch magic byte == 2")

        # Read checksum, then calculate checksum of rest of batch and verify it against
        # the read value.
        crc = read_uint32(batch_buffer)
        attributes_pos = batch_buffer.tell()
        if crc != crc32c(batch_buffer.read(batch_length - attributes_pos)):
            raise ValueError("Checksum mismatch when reading record batch")
        batch_buffer.seek(attributes_pos)

        attributes = read_int16(batch_buffer)
        last_offset_delta = read_int32(batch_buffer)
        base_timestamp = read_int64(batch_buffer)
        max_timestamp = read_int64(batch_buffer)
        producer_id = read_int64(batch_buffer)
        producer_epoch = read_int16(batch_buffer)
        base_sequence = read_int32(batch_buffer)

        num_records = read_int32(batch_buffer)
        records = []
        for _ in range(num_records):
            record = read_record(batch_buffer, base_timestamp, base_offset)
            if record.timestamp.timestamp() > max_timestamp:
                raise ValueError("Record has timestamp larger than batch max timestamp")
            records.append(record)

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
    )
