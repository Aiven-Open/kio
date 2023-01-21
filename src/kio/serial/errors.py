class DecodeError(Exception):
    ...


class UnexpectedNull(DecodeError):
    ...


class SchemaError(Exception):
    ...
