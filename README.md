<h1 align=center>kafka-protocol</h1>

<p align=center>
    <a href=https://github.com/aiven/python-kafka-protocol/actions?query=workflow%3ACI+branch%3Amain><img src=https://github.com/aiven/python-kafka-protocol/workflows/CI/badge.svg alt="CI Build Status"></a>
</p>

Kafka Protocol data types for Python.

## Features

- Exposes immutable dataclass entities for all Kafka Protocol messages, generated from
  the same source as Kafka's internals.
- Message classes are simply light-weight data containers and does not inherit anything
  or expose any methods other than a vanilla dataclass. Encoding and decoding is enabled
  by making all the necessary details about Kafka encoding introspectable.
- Supports synchronous encoding and decoding of messages with `IO[bytes]`.
- Supports asynchronous encoding and decoding with `asyncio.StreamReader` and
  `asyncio.StreamWriter`.
- Test suite with focus on roundtrip property tests using Hypothesis.

## Usage

Here's a simple example of how message entities can be used to serialize and send a
request to Kafka, and receive and parse the response into a full entity.

```python
import asyncio
from kio.schema.metadata.request.v12 import MetadataRequest
from kio.schema.metadata.response.v12 import MetadataResponse
from kio.serial import entity_writer
from kio.serial import entity_decoder
from kio.serial import read_async
from contextlib import closing

write_metadata = entity_writer(MetadataRequest)
read_metadata = entity_decoder(MetadataResponse)


async def get_metadata(request: MetadataRequest) -> MetadataResponse:
    stream_reader, stream_writer = await asyncio.open_connection(
        host="127.0.0.1",
        port=9092,
    )
    with closing(stream_writer):
        write_metadata(stream_writer, request)
        await stream_writer.drain()
        return await read_async(stream_reader, read_metadata)
```

## Development

Generate and format schema.

```shell
$ python -m codegen.generator
$ pre-commit run --all-files
```

Run tests.

```shell
$ python -X dev -m pytest --cov
```
