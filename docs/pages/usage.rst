Usage examples
==============

Asynchronous writing and reading
--------------------------------

In this example we show how message entities can be used to serialize and send a request
to Kafka, and receive and parse the response into a full entity.

.. code-block:: python

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


Synchronous writing and reading
--------------------------------

This example is equivalent to the asynchronous one above, except it uses synchronous,
blocking facilities for IO.

.. code-block:: python

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

            # Read message size, header, and payload from connection stream.
            read_sync(stream, decode_int32)
            response_header = read_sync(stream, decode_header)
            assert response_header.correlation_id == correlation_id
            return read_sync(stream, decode_metadata)
