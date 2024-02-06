Usage examples
==============

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

            # Read response into a temporary buffer.
            response_length_bytes = await stream.readexactly(4)
            response_length = read_int32(io.BytesIO(response_length_bytes))
            response_buffer = io.BytesIO(await stream_reader.readexactly(response_length))

        # Parse header and payload from response buffer.
        response_header = read_header(response_buffer)
        assert response_header.correlation_id == correlation_id
        return read_metadata(response_buffer)


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

            # Read response into a buffer.
            response_length = read_int32(stream)
            response_buffer = io.BytesIO(stream.read(response_length))

        # Parse header and payload from response buffer.
        response_header = read_header(response_buffer)
        assert response_header.correlation_id == correlation_id
        return read_metadata(response_buffer)
