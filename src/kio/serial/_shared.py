import enum

from kio.static.primitive import i8


class NullableEntityMarker(enum.Enum):
    null = i8(-1)
    not_null = i8(1)
