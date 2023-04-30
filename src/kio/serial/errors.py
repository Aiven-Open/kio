class SerialError(Exception):
    ...


class DecodeError(SerialError):
    ...


class UnexpectedNull(DecodeError):
    ...


# todo: Consider sub-classing UnicodeDecodeError.
class InvalidUnicode(DecodeError):
    ...


class NegativeByteLength(DecodeError):
    ...


class SchemaError(SerialError):
    ...


class OutOfBoundValue(SerialError):
    ...


class EncodeError(SerialError):
    ...
