# ruff: noqa: S603
import asyncio
import base64
import contextlib
import dataclasses
import io
import json
import os

from collections.abc import AsyncIterator
from collections.abc import Iterator
from contextlib import closing
from datetime import datetime
from datetime import timedelta
from json import JSONEncoder
from pathlib import Path
from subprocess import PIPE
from subprocess import Popen
from subprocess import TimeoutExpired
from types import NoneType
from types import UnionType
from typing import Any
from typing import get_args
from typing import get_origin
from uuid import UUID

import pytest
import pytest_asyncio

from kio._utils import DataclassInstance
from kio.serial import entity_writer
from kio.static.protocol import Entity

from .hypothesis import configure_hypothesis

configure_hypothesis()


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


async def async_buffers() -> (
    AsyncIterator[tuple[asyncio.StreamReader, asyncio.StreamWriter]]
):
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


def is_nullable_entity_field(field: dataclasses.Field) -> bool:
    if get_origin(field.type) is not UnionType:
        return False
    try:
        a, b = get_args(field.type)
    except ValueError:
        return False
    return (a is NoneType and dataclasses.is_dataclass(b)) or (
        b is NoneType and dataclasses.is_dataclass(a)
    )


def map_nullable_entity_fields(obj: DataclassInstance) -> dict[str, bool]:
    """Return map of KIP-893 nullable entity fields."""
    return {
        field.name: is_nullable_entity_field(field) for field in dataclasses.fields(obj)
    }


class JavaTester:
    class _Encoder(JSONEncoder):
        def default(self, o: Any) -> Any:
            if dataclasses.is_dataclass(o):
                return self._replace_tzaware_nulls(
                    {
                        k: v
                        for k, v in dataclasses.asdict(o).items()
                        if (v is not None or not map_nullable_entity_fields(o)[k])
                    }
                )
            if isinstance(o, timedelta):
                return round(o.total_seconds() * 1000)
            if isinstance(o, datetime):
                return round(o.timestamp() * 1000)
            if isinstance(o, UUID):
                return str(o)
            if isinstance(o, bytes):
                return base64.b64encode(o).decode("utf-8")
            return super().default(o)

        def _replace_tzaware_nulls(self, o: Any) -> Any:
            if isinstance(o, dict):
                result = {}
                for k, v in o.items():
                    if k == "log_append_time" and v is None:
                        result[k] = -1
                    else:
                        result[k] = self._replace_tzaware_nulls(v)
                return result
            elif isinstance(o, list):
                return [self._replace_tzaware_nulls(e) for e in o]
            elif isinstance(o, tuple):
                return tuple(self._replace_tzaware_nulls(e) for e in o)
            else:
                return o

    def __init__(self) -> None:
        cmd = [
            "docker",
            "compose",
            "-f",
            str(Path(__file__).parent / "docker-compose-java-tester.yaml"),
            "run",
            "--build",
            "--rm",
            "-i",
            "java_tester",
        ]
        self._p = Popen(cmd, stdin=PIPE, stdout=PIPE, shell=False, text=True)
        assert self._p.stdout is not None
        while self._p.stdout.readline().strip() != "Java tester started":
            pass

    def test(self, instance: Entity) -> None:
        instance_type = type(instance)
        buffer = io.BytesIO()
        writer = entity_writer(instance_type)
        writer(buffer, instance)
        buffer.seek(0)

        case = {
            "class": instance_type.__name__,
            "version": instance_type.__version__,
            "json": instance,
            "serialized": buffer.getvalue(),
        }
        case_str = json.dumps(case, cls=self._Encoder) + "\n"

        assert self._p.stdin is not None
        assert self._p.stdout is not None

        self._p.stdin.write(case_str)
        self._p.stdin.flush()

        line = self._p.stdout.readline()
        response = json.loads(line)
        assert response["success"], response.get("message") or response.get("exception")

    def close(self) -> None:
        if self._p.stdin is not None:
            self._p.stdin.flush()
            self._p.stdin.close()
        if self._p.stdout is not None:
            self._p.stdout.close()
        try:
            self._p.wait(timeout=10)
        except TimeoutExpired:
            self._p.kill()
            self._p.wait(timeout=10)


@pytest.fixture(name="java_tester", scope="session")
def fixture_java_tester() -> Iterator[JavaTester]:
    jt = JavaTester()
    try:
        yield jt
    finally:
        jt.close()
