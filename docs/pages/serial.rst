Serialization and parsing
=========================

Serial
------

.. py:function:: kio.serial.entity_reader(entity_type: type[Entity], nullable: bool = False) -> Reader[Entity | None]
   :module: kio.serial

   :param entity_type: Entity class to deserialize into.
   :type entity_type: type[Entity]
   :param bool nullable: When ``True``, reading a null value returns ``None``
      instead of raising.
   :rtype: Reader[Entity | None]

.. autofunction:: kio.serial.entity_writer

Readers
-------

.. note::

   The reader functions below document the public API.  The hot-path entity
   decoder in the native extension calls equivalent internal Rust functions
   directly and never crosses the Python boundary per field.

.. py:currentmodule:: kio.serial.readers

.. py:class:: Reader(*args, **kwargs)

   Bases: :class:`~typing.Protocol` [:class:`T_co`]

.. py:function:: read_boolean(buffer: Buffer, offset: int, /) -> tuple[bool, int]

   :param Buffer buffer:
   :param int offset:
   :rtype: tuple[bool, int]

.. py:function:: read_int8(buffer: Buffer, offset: int, /) -> tuple[i8, int]

   :param Buffer buffer:
   :param int offset:
   :rtype: tuple[i8, int]

.. py:function:: read_int16(buffer: Buffer, offset: int, /) -> tuple[i16, int]

   :param Buffer buffer:
   :param int offset:
   :rtype: tuple[i16, int]

.. py:function:: read_int32(buffer: Buffer, offset: int, /) -> tuple[i32, int]

   :param Buffer buffer:
   :param int offset:
   :rtype: tuple[i32, int]

.. py:function:: read_int64(buffer: Buffer, offset: int, /) -> tuple[i64, int]

   :param Buffer buffer:
   :param int offset:
   :rtype: tuple[i64, int]

.. py:function:: read_uint8(buffer: Buffer, offset: int, /) -> tuple[u8, int]

   :param Buffer buffer:
   :param int offset:
   :rtype: tuple[u8, int]

.. py:function:: read_uint16(buffer: Buffer, offset: int, /) -> tuple[u16, int]

   :param Buffer buffer:
   :param int offset:
   :rtype: tuple[u16, int]

.. py:function:: read_uint32(buffer: Buffer, offset: int, /) -> tuple[u32, int]

   :param Buffer buffer:
   :param int offset:
   :rtype: tuple[u32, int]

.. py:function:: read_uint64(buffer: Buffer, offset: int, /) -> tuple[u64, int]

   :param Buffer buffer:
   :param int offset:
   :rtype: tuple[u64, int]

.. py:function:: read_unsigned_varint(buffer: Buffer, offset: int, /) -> tuple[uvarint, int]

   Deserialize an unsigned integer stored in variable-length encoding (1–5 bytes).

   :param Buffer buffer:
   :param int offset:
   :rtype: tuple[uvarint, int]

.. py:function:: read_signed_varint(buffer: Buffer, offset: int, /) -> tuple[svarint, int]

   :param Buffer buffer:
   :param int offset:
   :rtype: tuple[svarint, int]

.. py:function:: read_unsigned_varlong(buffer: Buffer, offset: int, /) -> tuple[uvarlong, int]

   :param Buffer buffer:
   :param int offset:
   :rtype: tuple[uvarlong, int]

.. py:function:: read_signed_varlong(buffer: Buffer, offset: int, /) -> tuple[svarlong, int]

   :param Buffer buffer:
   :param int offset:
   :rtype: tuple[svarlong, int]

.. py:function:: read_float64(buffer: Buffer, offset: int, /) -> tuple[f64, int]

   :param Buffer buffer:
   :param int offset:
   :rtype: tuple[f64, int]

.. py:function:: read_compact_string_as_bytes(buffer: Buffer, offset: int, /) -> tuple[bytes, int]

   :param Buffer buffer:
   :param int offset:
   :rtype: tuple[bytes, int]

.. py:function:: read_compact_string_as_bytes_nullable(buffer: Buffer, offset: int, /) -> tuple[bytes | None, int]

   :param Buffer buffer:
   :param int offset:
   :rtype: tuple[bytes | None, int]

.. py:function:: read_compact_string(buffer: Buffer, offset: int, /) -> tuple[str, int]

   :param Buffer buffer:
   :param int offset:
   :rtype: tuple[str, int]

.. py:function:: read_compact_string_nullable(buffer: Buffer, offset: int, /) -> tuple[str | None, int]

   :param Buffer buffer:
   :param int offset:
   :rtype: tuple[str | None, int]

.. py:function:: read_legacy_bytes(buffer: Buffer, offset: int, /) -> tuple[bytes, int]

   :param Buffer buffer:
   :param int offset:
   :rtype: tuple[bytes, int]

.. py:function:: read_nullable_legacy_bytes(buffer: Buffer, offset: int, /) -> tuple[bytes | None, int]

   :param Buffer buffer:
   :param int offset:
   :rtype: tuple[bytes | None, int]

.. py:function:: read_legacy_string(buffer: Buffer, offset: int, /) -> tuple[str, int]

   :param Buffer buffer:
   :param int offset:
   :rtype: tuple[str, int]

.. py:function:: read_nullable_legacy_string(buffer: Buffer, offset: int, /) -> tuple[str | None, int]

   :param Buffer buffer:
   :param int offset:
   :rtype: tuple[str | None, int]

.. py:function:: read_legacy_array_length(buffer: Buffer, offset: int, /) -> tuple[i32, int]

   :param Buffer buffer:
   :param int offset:
   :rtype: tuple[i32, int]

.. py:function:: read_compact_array_length(buffer: Buffer, offset: int, /) -> tuple[int | None, int]

   :param Buffer buffer:
   :param int offset:
   :rtype: tuple[int | None, int]

.. py:function:: read_uuid(buffer: Buffer, offset: int, /) -> tuple[UUID | None, int]

   :param Buffer buffer:
   :param int offset:
   :rtype: tuple[UUID | None, int]

.. py:function:: compact_array_reader(item_reader: Reader[T]) -> Reader[tuple[T, ...] | None]

   :param item_reader: Reader for each array element.
   :type item_reader: Reader[T]
   :rtype: Reader[tuple[T, ...] | None]

.. py:function:: legacy_array_reader(item_reader: Reader[T]) -> Reader[tuple[T, ...] | None]

   :param item_reader: Reader for each array element.
   :type item_reader: Reader[T]
   :rtype: Reader[tuple[T, ...] | None]

.. py:function:: read_error_code(buffer: Buffer, offset: int, /) -> tuple[ErrorCode, int]

   :param Buffer buffer:
   :param int offset:
   :rtype: tuple[ErrorCode, int]

.. py:function:: read_timedelta_i32(buffer: Buffer, offset: int, /) -> tuple[i32Timedelta, int]

   :param Buffer buffer:
   :param int offset:
   :rtype: tuple[i32Timedelta, int]

.. py:function:: read_timedelta_i64(buffer: Buffer, offset: int, /) -> tuple[i64Timedelta, int]

   :param Buffer buffer:
   :param int offset:
   :rtype: tuple[i64Timedelta, int]

.. py:function:: tz_aware_from_i64(timestamp_ms: i64) -> TZAware

   Convert a millisecond timestamp to :class:`~kio.static.primitive.TZAware`.

   :param i64 timestamp_ms:
   :rtype: TZAware

.. py:function:: read_datetime_i64(buffer: Buffer, offset: int, /) -> tuple[TZAware, int]

   :param Buffer buffer:
   :param int offset:
   :rtype: tuple[TZAware, int]

.. py:function:: read_nullable_datetime_i64(buffer: Buffer, offset: int, /) -> tuple[TZAware | None, int]

   :param Buffer buffer:
   :param int offset:
   :rtype: tuple[TZAware | None, int]

Writers
-------

.. automodule:: kio.serial.writers
    :members:
    :undoc-members:
    :show-inheritance:

Errors
------

.. automodule:: kio.serial.errors
    :members:
    :undoc-members:
    :show-inheritance:
