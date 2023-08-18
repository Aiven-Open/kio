<h1 align=center>kio</h1>

<p align=center>
    <a href=https://github.com/aiven/kio/actions?query=workflow%3ACI+branch%3Amain><img src=https://github.com/aiven/kio/workflows/CI/badge.svg alt="CI Build Status"></a>
</p>

<p align=center>
    Python data types for the Apache Kafka® Protocol.
</p>

## Features

- Exposes immutable dataclass entities for all protocol messages, generated from the
  [same source][schema-source] as used internally in Apache Kafka®.
- Message classes are simply light-weight data containers and does not inherit anything
  or expose any methods other than a vanilla dataclass. Encoding and decoding is enabled
  by making all the necessary details about Kafka encoding introspectable.
- Supports encoding and decoding of messages through `IO[bytes]`.
- Test suite with focus on roundtrip property tests using Hypothesis.

[schema-source]:
  https://github.com/apache/kafka/tree/trunk/clients/src/main/resources/common/message

## Development

Install development requirements.

```shell
$ python3 -m pip install -e .[all]
```

The test suite contains integration tests that expects to be able to connect to an
Apache Kafka® instance running on `127.0.0.1:9092`. There is a Docker Compose file in
`container/compose.yml` that you can use to conveniently start up an instance.

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
