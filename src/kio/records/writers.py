import io
from typing import IO

from kio.records.schema import RecordBatch, RecordHeader, Record
from kio.serial.writers import write_signed_varint, write_int8, write_signed_varlong, \
    write_int64, write_int32, write_uint32, write_int16
from kio.static.primitive import i64, i32


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


def write_batch(buffer: IO[bytes], batch: RecordBatch) -> None:
    write_int64(buffer, batch.base_offset)
    write_int32(buffer, batch.batch_length)
    write_int32(buffer, batch.partition_leader_epoch)
    write_int8(buffer, batch.magic)
    write_uint32(buffer, batch.crc)
    write_int16(buffer, batch.attributes)
    write_int32(buffer, batch.last_offset_delta)
    write_int64(buffer, batch.base_timestamp)
    write_int64(buffer, batch.max_timestamp)
    write_int64(buffer, batch.producer_id)
    write_int16(buffer, batch.producer_epoch)
    write_int32(buffer, batch.base_sequence)

    write_int32(buffer, i32(len(batch.records)))
    for record in batch.records:
        write_record(
            buffer=buffer,
            record=record,
            base_timestamp=batch.base_timestamp,
            base_offset=batch.base_offset,
        )
