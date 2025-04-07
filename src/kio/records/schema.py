from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from kio.static.primitive import TZAwareMicros
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i64
from kio.static.primitive import u32


@dataclass(frozen=True, slots=True, kw_only=True)
class RecordHeader:
    key: bytes | None
    value: bytes | None


@dataclass(frozen=True, slots=True, kw_only=True)
class Record:
    attributes: i8
    # Resolved from the base timestamp of the batch.
    timestamp: TZAwareMicros
    # Resolved from the base offset of the batch.
    # It's interesting that base offset, offset delta, and last offset delta use three
    # distinct data types.
    offset: i64
    key: bytes | None
    value: bytes | None
    headers: tuple[RecordHeader, ...]


@dataclass(frozen=True, slots=True, kw_only=True)
class RecordBatch:
    magic: ClassVar = i8(2)

    base_offset: i64
    batch_length: i32
    partition_leader_epoch: i32
    crc: u32
    attributes: i16
    last_offset_delta: i32
    base_timestamp: i64
    max_timestamp: i64
    producer_id: i64
    producer_epoch: i16
    base_sequence: i32
    records: tuple[Record, ...]


# We model batches that are about to be produced separately from ones returned from a
# broker. The reason for this is that a full RecordBatch contains many fields that are
# derived from the data it contains, such as the crc checksum and the batch length.
@dataclass(frozen=True, slots=True, kw_only=True)
class NewRecordBatch:
    producer_id: i64
    producer_epoch: i16
    partition_leader_epoch: i32 = i32(0)
    base_sequence: i32
    records: tuple[Record, ...]
    attributes: i16
