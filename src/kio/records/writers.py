import io
from collections.abc import Sequence
from typing import IO
from typing import assert_never

import crc32c

from kio.records.schema import NewRecordBatch
from kio.records.schema import Record
from kio.records.schema import RecordBatch
from kio.records.schema import RecordHeader
from kio.serial.writers import write_int8
from kio.serial.writers import write_int16
from kio.serial.writers import write_int32
from kio.serial.writers import write_int64
from kio.serial.writers import write_signed_varint
from kio.serial.writers import write_signed_varlong
from kio.serial.writers import write_uint32
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i64
from kio.static.primitive import u32


def write_signed_compact_bytes(buffer: IO[bytes], value: bytes | None) -> None:
    if value is None:
        write_signed_varint(buffer, -1)
        return
    write_signed_varint(buffer, len(value))
    buffer.write(value)


def write_header(buffer: IO[bytes], header: RecordHeader) -> None:
    write_signed_compact_bytes(buffer, header.key)
    write_signed_compact_bytes(buffer, header.value)


def write_record(
    buffer: IO[bytes],
    record: Record,
    base_timestamp: i64,
    base_offset: i64,
) -> None:
    # Write record into a temporary buffer.
    with io.BytesIO() as record_buffer:
        write_int8(record_buffer, record.attributes),
        write_signed_varlong(
            record_buffer,
            int(record.timestamp.timestamp() * 1000) - base_timestamp,
        )
        write_signed_varint(record_buffer, record.offset - base_offset)
        write_signed_compact_bytes(record_buffer, record.key)
        write_signed_compact_bytes(record_buffer, record.value)

        write_signed_varint(record_buffer, len(record.headers))
        for header in record.headers:
            write_header(record_buffer, header)

        # Write length of record buffer, followed by the record itself.
        write_signed_varint(buffer, record_buffer.tell())
        buffer.write(record_buffer.getvalue())


def _write_batch_pre_checksum(
    buffer: IO[bytes],
    base_offset: i64,
    batch_length: i32,
    partition_leader_epoch: i32,
    magic: i8,
    crc: u32,
) -> None:
    write_int64(buffer, base_offset)
    write_int32(buffer, batch_length)
    write_int32(buffer, partition_leader_epoch)
    write_int8(buffer, magic)
    write_uint32(buffer, crc)


def _write_batch_post_checksum(
    buffer: IO[bytes],
    attributes: i16,
    last_offset_delta: i32,
    base_timestamp: i64,
    max_timestamp: i64,
    producer_id: i64,
    producer_epoch: i16,
    base_sequence: i32,
    base_offset: i64,
    records: Sequence[Record],
) -> None:
    write_int16(buffer, attributes)
    write_int32(buffer, last_offset_delta)
    write_int64(buffer, base_timestamp)
    write_int64(buffer, max_timestamp)
    write_int64(buffer, producer_id)
    write_int16(buffer, producer_epoch)
    write_int32(buffer, base_sequence)

    write_int32(buffer, i32(len(records)))
    for record in records:
        write_record(
            buffer=buffer,
            record=record,
            base_timestamp=base_timestamp,
            base_offset=base_offset,
        )


def write_new_batch(buffer: IO[bytes], new_batch: NewRecordBatch) -> None:
    match new_batch.records:
        case (first_record, *_, last_record):
            first_record = first_record
            last_record = last_record
        case (first_record,):
            first_record = last_record = first_record
        case _:
            raise ValueError("Need at least one record to construct batch")

    batch_length = i32(len(new_batch.records))
    base_offset = first_record.offset
    last_offset_delta = i32(last_record.offset - base_offset)
    base_timestamp = i64(int(first_record.timestamp.timestamp()))
    max_timestamp = i64(
        int(max(record.timestamp for record in new_batch.records).timestamp())
    )

    with io.BytesIO() as crc_buffer:
        _write_batch_post_checksum(
            buffer=buffer,
            attributes=new_batch.attributes,
            last_offset_delta=last_offset_delta,
            base_timestamp=base_timestamp,
            max_timestamp=max_timestamp,
            producer_id=new_batch.producer_id,
            producer_epoch=new_batch.producer_epoch,
            base_sequence=new_batch.base_sequence,
            base_offset=base_offset,
            records=new_batch.records,
        )

        post_checksum = crc_buffer.getvalue()
        crc = crc32c.crc32c(post_checksum)

    _write_batch_pre_checksum(
        buffer=buffer,
        base_offset=base_offset,
        batch_length=batch_length,
        partition_leader_epoch=new_batch.partition_leader_epoch,
        magic=RecordBatch.magic,
        crc=crc,
    )
    buffer.write(post_checksum)


def write_prepared_batch(buffer: IO[bytes], batch: RecordBatch) -> None:
    _write_batch_pre_checksum(
        buffer=buffer,
        base_offset=batch.base_offset,
        batch_length=batch.batch_length,
        partition_leader_epoch=batch.partition_leader_epoch,
        magic=batch.magic,
        crc=batch.crc,
    )
    write_uint32(buffer, batch.crc)
    _write_batch_post_checksum(
        buffer=buffer,
        attributes=batch.attributes,
        last_offset_delta=batch.last_offset_delta,
        base_timestamp=batch.base_timestamp,
        max_timestamp=batch.max_timestamp,
        producer_id=batch.producer_id,
        producer_epoch=batch.producer_epoch,
        base_sequence=batch.base_sequence,
        base_offset=batch.base_offset,
        records=batch.records,
    )


def write_batch(buffer: IO[bytes], batch: RecordBatch | NewRecordBatch) -> None:
    if isinstance(batch, RecordBatch):
        write_prepared_batch(buffer, batch)
    elif isinstance(batch, NewRecordBatch):
        write_new_batch(buffer, batch)
    else:
        assert_never(batch)
