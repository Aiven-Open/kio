<h1 align=center>kafka-protocol</h1>

<p align=center>
    <a href=https://github.com/aiven/python-kafka-protocol/actions?query=workflow%3ACI+branch%3Amain><img src=https://github.com/aiven/python-kafka-protocol/workflows/CI/badge.svg alt="CI Build Status"></a>
</p>

<p align=center>
    Kafka Protocol data types for Python.
</p>

## Features

- Exposes immutable dataclass entities for all Kafka Protocol messages, generated from
  the [same source][schema-source] as used by Kafka's internals.
- Message classes are simply light-weight data containers and does not inherit anything
  or expose any methods other than a vanilla dataclass. Encoding and decoding is enabled
  by making all the necessary details about Kafka encoding introspectable.
- Supports synchronous encoding and decoding of messages with `IO[bytes]`.
- Supports asynchronous encoding and decoding with `asyncio.StreamReader` and
  `asyncio.StreamWriter`.
- Test suite with focus on roundtrip property tests using Hypothesis.

[schema-source]:
  https://github.com/apache/kafka/tree/trunk/clients/src/main/resources/common/message

## Usage

Here's an example of how message entities can be used to serialize and send a request to
Kafka, and receive and parse the response into a full entity.

```python
import asyncio
import io
import random
from contextlib import closing

from kio.schema.metadata.v12.request import MetadataRequest
from kio.schema.metadata.v12.response import MetadataResponse
from kio.schema.primitive import i32
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_async
from kio.serial.decoders import decode_int32
from kio.serial.encoders import write_int32

write_metadata = entity_writer(MetadataRequest)
decode_metadata = entity_decoder(MetadataResponse)
write_header = entity_writer(MetadataRequest.__header_schema__)
decode_header = entity_decoder(MetadataResponse.__header_schema__)


async def get_metadata(request: MetadataRequest) -> MetadataResponse:
    correlation_id = random.randint(0, 2**31 - 1)
    request_header = MetadataRequest.__header_schema__(
        request_api_key=MetadataRequest.__api_key__,
        request_api_version=MetadataRequest.__version__,
        correlation_id=correlation_id,
        client_id="test",
    )
    stream_reader, stream_writer = await asyncio.open_connection(
        host="127.0.0.1",
        port=9092,
    )
    with closing(stream_writer), io.BytesIO() as message_buffer:
        # Write message to a temporary buffer.
        write_header(message_buffer, request_header)
        write_metadata(message_buffer, request)
        # Write message size, then message itself, to the connection stream.
        write_int32(stream_writer, i32(message_buffer.tell()))
        message_buffer.seek(0)
        stream_writer.write(message_buffer.getvalue())
        await stream_writer.drain()
        # Read message size, header, and payload from connection stream.
        await read_async(stream_reader, decode_int32)
        response_header = await read_async(stream_reader, decode_header)
        assert response_header.correlation_id == correlation_id
        return await read_async(stream_reader, decode_metadata)
```

Here's an equivalent example using non-async facilities.

```python
import io
import random
import socket
from contextlib import closing

from kio.schema.metadata.v12.request import MetadataRequest
from kio.schema.metadata.v12.response import MetadataResponse
from kio.schema.primitive import i32
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from kio.serial.decoders import decode_int32
from kio.serial.encoders import write_int32

write_metadata = entity_writer(MetadataRequest)
decode_metadata = entity_decoder(MetadataResponse)
write_header = entity_writer(MetadataRequest.__header_schema__)
decode_header = entity_decoder(MetadataResponse.__header_schema__)


def get_metadata(request: MetadataRequest) -> MetadataResponse:
    correlation_id = random.randint(0, 2**31 - 1)
    request_header = MetadataRequest.__header_schema__(
        request_api_key=MetadataRequest.__api_key__,
        request_api_version=MetadataRequest.__version__,
        correlation_id=correlation_id,
        client_id="test",
    )
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 9092))
    with closing(sock), io.BytesIO() as message_buffer:
        stream = sock.makefile("rwb")
        # Write message to a temporary buffer.
        write_header(message_buffer, request_header)
        write_metadata(message_buffer, request)
        # Write message size, then message itself, to the connection stream.
        write_int32(stream, i32(message_buffer.tell()))
        message_buffer.seek(0)
        stream.write(message_buffer.getvalue())
        stream.flush()
        # Read message size, header, and payload from connection stream.
        read_sync(stream, decode_int32)
        response_header = read_sync(stream, decode_header)
        assert response_header.correlation_id == correlation_id
        return read_sync(stream, decode_metadata)
```

## Development

Install development requirements.

```shell
$ python3 -m pip install -e .[all]
```

The test suite contains integration tests that expects to be able to connect to a Kafka
instance running on `127.0.0.1:9092`. There is a Docker Compose file in
`container/compose.yml` that you can use to conveniently start up a Kafka instance.

```shell
$ docker compose --file=container/compose.yml up -d
```

Run tests.

```shell
$ python3 -X dev -m pytest --cov
```

Setup pre-commit to run on push.

```shell
$ pre-commit install -t pre-push
```

Fetch, generate, and format schema.

```shell
$ make build-schema
```
