from kio.static.primitive import i8, i16, i32, i64, u8, u16, u32, u64
from typing import TypeVar, TypeAlias

T = TypeVar("T")
_Result: TypeAlias = tuple[T, int]

def read_boolean(
    bytes: bytes,
    offset: int,
) -> _Result[bool]:
    ...

def read_int8(
    bytes: bytes,
    offset: int,
) -> _Result[i8]:
    ...

def read_int16(
    bytes: bytes,
    offset: int,
) -> _Result[i16]:
    ...

def read_int32(
    bytes: bytes,
    offset: int,
) -> _Result[i32]:
    ...
def read_int64(
    bytes: bytes,
    offset: int,
) -> _Result[i64]:
    ...
def read_uint8(
    bytes: bytes,
    offset: int,
) -> _Result[u8]:
    ...
def read_uint16(
    bytes: bytes,
    offset: int,
) -> _Result[u16]:
    ...
def read_uint32(
    bytes: bytes,
    offset: int,
) -> _Result[u32]:
    ...
def read_uint64(
    bytes: bytes,
    offset: int,
) -> _Result[u64]:
    ...
def read_unsigned_varint(
    bytes: bytes,
    offset: int,
) -> _Result[int]:
    ...
