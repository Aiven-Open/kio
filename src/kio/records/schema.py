from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from phantom.datetime import TZAware

from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i64
from kio.static.primitive import u32


@dataclass(frozen=True, slots=True, kw_only=True)
class RecordHeader:
    key: bytes
    value: bytes


@dataclass(frozen=True, slots=True, kw_only=True)
class Record:
    attributes: i8
    # Resolved from the base timestamp of the batch.
    timestamp: TZAware
    # Resolved from the base offset of the batch.
    # It's interesting that base offset, offset delta, and last offset delta use three
    # distinct data types.
    offset: i64
    key: bytes | None
    value: bytes | None
    headers: tuple[RecordHeader, ...]


@dataclass(frozen=True, slots=True, kw_only=True)
class RecordBatch:
    magic: ClassVar[i8] = 2

    base_offset: i64
    batch_length: i32
    partition_leader_epoch: i32
    crc: u32 | None = None
    attributes: i16
    last_offset_delta: i32
    base_timestamp: i64
    max_timestamp: i64
    producer_id: i64
    producer_epoch: i16
    base_sequence: i32
    records: tuple[Record, ...]
