class SerialError(Exception):
    ...


class DecodeError(SerialError):
    ...


class UnexpectedNull(DecodeError):
    ...


class SchemaError(SerialError):
    ...


class OutOfBoundValue(SerialError):
    ...


class EncodeError(SerialError):
    ...
