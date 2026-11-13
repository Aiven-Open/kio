Usage examples
==============

kio performs no IO of its own, so the examples below manage the connection to the broker
themselves. Only the IO differs between the asynchronous and the synchronous example;
the calls into kio are identical.

The examples are minimal, showing only what it takes to send a single request and parse
its response. Everything else a client needs around its network connections, such as
retries, timeouts, error handling, and multiplexing requests over a connection, is the
responsibility of the calling code.

Asynchronous writing and reading
--------------------------------

In this example we show how message entities can be used to serialize and send a request
to Apache Kafka®, and receive and parse the response into a full entity.

.. code-block:: python

    import asyncio
    import io
    import random
    from contextlib import closing

    from kio.schema.metadata.v12 import MetadataRequest
    from kio.schema.metadata.v12 import MetadataResponse
    from kio.static.primitive import i32
    from kio.serial import entity_reader
    from kio.serial import entity_writer
    from kio.serial.readers import read_int32
    from kio.serial.writers import write_int32

    write_metadata = entity_writer(MetadataRequest)
    read_metadata = entity_reader(MetadataResponse)
    write_header = entity_writer(MetadataRequest.__header_schema__)
    read_header = entity_reader(MetadataResponse.__header_schema__)


    async def get_metadata(request: MetadataRequest) -> MetadataResponse:
        # Choose a random correlation ID.
        correlation_id = random.randint(0, 2**31 - 1)

        # Build request header.
        request_header = MetadataRequest.__header_schema__(
            request_api_key=MetadataRequest.__api_key__,
            request_api_version=MetadataRequest.__version__,
            correlation_id=correlation_id,
            client_id="test",
        )

        # Open connection with broker.
        stream_reader, stream_writer = await asyncio.open_connection("127.0.0.1", 9092)

        with (
            closing(stream_writer),
            io.BytesIO() as request_buffer,
        ):
            # Write request to a temporary buffer.
            write_header(request_buffer, request_header)
            write_metadata(request_buffer, request)

            # Write message size, then message itself, to the connection stream.
            write_int32(stream_writer, i32(request_buffer.tell()))
            request_buffer.seek(0)
            stream_writer.write(request_buffer.getvalue())
            await stream_writer.drain()

            # Read message size, then message itself, from the connection stream.
            response_length, _ = read_int32(await stream_reader.readexactly(4), 0)
            response_bytes = await stream_reader.readexactly(response_length)

        # Parse header and payload from response bytes. Readers return the parsed
        # value along with the number of bytes consumed, which is the offset to
        # continue reading the payload from.
        response_header, header_size = read_header(response_bytes, 0)
        assert response_header.correlation_id == correlation_id
        response, _ = read_metadata(response_bytes, header_size)
        return response


Synchronous writing and reading
--------------------------------

This example is equivalent to the asynchronous one above, except it uses synchronous,
blocking facilities for IO.

.. code-block:: python

    import io
    import random
    import socket
    from contextlib import closing

    from kio.schema.metadata.v12 import MetadataRequest
    from kio.schema.metadata.v12 import MetadataResponse
    from kio.static.primitive import i32
    from kio.serial import entity_reader
    from kio.serial import entity_writer
    from kio.serial.readers import read_int32
    from kio.serial.writers import write_int32

    write_metadata = entity_writer(MetadataRequest)
    read_metadata = entity_reader(MetadataResponse)
    write_header = entity_writer(MetadataRequest.__header_schema__)
    read_header = entity_reader(MetadataResponse.__header_schema__)


    def get_metadata(request: MetadataRequest) -> MetadataResponse:
        # Choose a random correlation ID.
        correlation_id = random.randint(0, 2**31 - 1)

        # Build request header.
        request_header = MetadataRequest.__header_schema__(
            request_api_key=MetadataRequest.__api_key__,
            request_api_version=MetadataRequest.__version__,
            correlation_id=correlation_id,
            client_id="test",
        )

        # Open connection with broker.
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

            # Read message size, then message itself, from the connection stream.
            response_length, _ = read_int32(stream.read(4), 0)
            response_bytes = stream.read(response_length)

        # Parse header and payload from response bytes.
        response_header, header_size = read_header(response_bytes, 0)
        assert response_header.correlation_id == correlation_id
        response, _ = read_metadata(response_bytes, header_size)
        return response
