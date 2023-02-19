import asyncio
import contextlib
import io
import os
from collections.abc import AsyncIterator
from collections.abc import Iterator
from contextlib import closing

import pytest
import pytest_asyncio


def buffer() -> Iterator[io.BytesIO]:
    with closing(io.BytesIO()) as buffer:
        yield buffer
        # Make sure buffer is exhausted.
        assert buffer.read(1) == b"", "buffer not exhausted"


buffer_fixture = pytest.fixture(
    scope="function",
    name="buffer",
)(buffer)
setup_buffer = contextlib.contextmanager(buffer)


async def async_buffers() -> AsyncIterator[
    tuple[asyncio.StreamReader, asyncio.StreamWriter]
]:
    read_fd, write_fd = os.pipe()
    reader = asyncio.StreamReader()
    reader_protocol = asyncio.StreamReaderProtocol(reader)
    loop = asyncio.get_running_loop()
    read_transport, _ = await loop.connect_read_pipe(
        protocol_factory=lambda: reader_protocol,
        pipe=os.fdopen(read_fd),
    )
    write_protocol = asyncio.StreamReaderProtocol(asyncio.StreamReader())
    write_transport, _ = await loop.connect_write_pipe(
        protocol_factory=lambda: write_protocol,
        pipe=os.fdopen(write_fd, "w"),
    )
    writer = asyncio.StreamWriter(write_transport, write_protocol, None, loop)

    try:
        yield reader, writer
    finally:
        writer.close()
        assert await reader.read(1) == b"", "reader not exhausted"


async_buffers_fixture = pytest_asyncio.fixture(
    scope="function",
    name="async_buffers",
)(async_buffers)
setup_async_buffers = contextlib.asynccontextmanager(async_buffers)


@pytest_asyncio.fixture(scope="function")
async def stream_reader(
    async_buffers: tuple[asyncio.StreamReader, object],
) -> asyncio.StreamReader:
    return async_buffers[0]


@pytest_asyncio.fixture(scope="function")
async def stream_writer(
    async_buffers: tuple[object, asyncio.StreamWriter],
) -> asyncio.StreamWriter:
    return async_buffers[1]
