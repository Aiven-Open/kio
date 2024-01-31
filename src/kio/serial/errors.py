class SerialError(Exception):
    ...


class DecodeError(SerialError):
    ...


class UnexpectedNull(DecodeError):
    ...


class BufferUnderflow(DecodeError):
    ...


class EncodeError(SerialError):
    ...


class OutOfBoundValue(SerialError):
    ...


class SchemaError(SerialError):
    ...
