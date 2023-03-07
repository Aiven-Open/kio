# This logic is adopted from the Kafka source code, appropriate documentation for
# this seems to be missing.
# https://github.com/apache/kafka/blob/62431dca700fb2c7c3afe1a7c9eb07fe336f9b04/generator/src/main/java/org/apache/kafka/message/ApiMessageTypeGenerator.java#L329

from codegen.parser import DataSchema
from codegen.parser import HeaderSchema
from codegen.parser import MessageSchema


def _get_request_header_schema(
    schema: MessageSchema,
    version: int,
    is_flexible: bool,
) -> str:
    assert schema.type == "request"

    # Version 0 of ControlledShutdownRequest is special, see Kafka source linked above.
    if version == 0 and schema.apiKey == 7:
        return "from kio.schema.request_header.v0.header import RequestHeader\n"
    elif is_flexible:
        return "from kio.schema.request_header.v2.header import RequestHeader\n"
    else:
        return "from kio.schema.request_header.v1.header import RequestHeader\n"


def _get_response_header_schema(
    schema: MessageSchema,
    is_flexible: bool,
) -> str:
    assert schema.type == "response"

    # ApiVersionsResponse is special, see Kafka source linked above.
    if schema.apiKey == 18:
        return "from kio.schema.response_header.v0.header import ResponseHeader\n"
    elif is_flexible:
        return "from kio.schema.response_header.v1.header import ResponseHeader\n"
    else:
        return "from kio.schema.response_header.v0.header import ResponseHeader\n"


def get_header_schema_import(
    schema: MessageSchema | HeaderSchema | DataSchema,
    version: int,
) -> str:
    if not isinstance(schema, MessageSchema):
        return ""
    is_flexible = schema.flexibleVersions.matches(version)
    if schema.type == "request":
        return _get_request_header_schema(schema, version, is_flexible)
    elif schema.type == "response":
        return _get_response_header_schema(schema, is_flexible)
    raise NotImplementedError("Unknown schema type")
