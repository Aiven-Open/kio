<h1 align=center>kio</h1>

<p align=center>
    <a href=https://github.com/aiven/kio/actions?query=workflow%3ACI+branch%3Amain><img src=https://github.com/aiven/kio/workflows/CI/badge.svg alt="CI Build Status"></a>
    <a href=https://codecov.io/gh/Aiven-Open/kio><img src="https://codecov.io/gh/Aiven-Open/kio/graph/badge.svg?token=ogJDikql10" alt="Code coverage report"></a>
    <br>
    <a href=https://pypi.org/project/kio/><img src=https://img.shields.io/pypi/v/kio.svg?color=informational&label=PyPI alt="PyPI Package"></a>
    <a href=https://pypi.org/project/kio/><img src=https://img.shields.io/pypi/pyversions/kio.svg?color=informational&label=Python alt="Python versions"></a>
</p>

<p align=center>
    Python data types for the Apache Kafka® Protocol.
</p>

<h4 align=center>
    <a href=https://aiven-open.github.io/kio/>Checkout the complete documentation →</a>
</h4>

## Features

- Exposes immutable dataclass entities for all protocol messages, generated from the
  [same source][schema-source] as used internally in Apache Kafka®.
- Message classes are simple light-weight data containers that do not inherit anything
  or expose any methods other than a regular dataclass. Encoding and decoding is enabled
  by making all the necessary details about Kafka encoding introspectable.
- Widely compatible encoding and decoding of messages through the `IO[bytes]` interface.
- Test suite with focus on roundtrip property tests using Hypothesis, including
  compatibility testing against the internals of upstream Apache Kafka®.

[schema-source]:
  https://github.com/apache/kafka/tree/trunk/clients/src/main/resources/common/message

## Installation

```shell
$ pip install --require-virtualenv kio
```

## Development

Install development requirements.

```shell
$ pip install --require-virtualenv -e .[all]
```

The test suite contains integration tests that expects to be able to connect to an
Apache Kafka® instance running on `127.0.0.1:9092`. There is a Docker Compose file in
`container/compose.yml` that you can use to conveniently start up an instance.

```shell
$ docker compose up -d kafka
```

Run tests.

```shell
$ python3 -X dev -m pytest --cov
```

Setup pre-commit to run on push.

```shell
$ pre-commit install -t pre-push
```

> [!WARNING]\
> Building the schema will delete the `src/kio/schema` directory and recreate it again, hence
> all of the files under this directory will be deleted. Make sure to not put unrelated files
> there and accidentally wipe out your own work.

Fetch, generate, and format schema.

```shell
$ make build-schema
```
