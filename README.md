<h1 align=center>kafka-protocol</h1>

<p align=center>
    <a href=https://github.com/aiven/python-kafka-protocol/actions?query=workflow%3ACI+branch%3Amain><img src=https://github.com/aiven/python-kafka-protocol/workflows/CI/badge.svg alt="CI Build Status"></a>
</p>

Kafka Protocol data types for Python.

### Features

- Exposes immutable dataclass entities for all Kafka Protocol messages, generated from
  the same source as Kafka's internals.
- Message classes are simply light-weight data containers and does not inherit anything
  or expose any methods other than a vanilla dataclass. Encoding and decoding is enabled
  by making all the necessary details about Kafka encoding introspectable.
- Supports synchronous encoding and decoding of messages with `IO[bytes]`.
- Supports asynchronous encoding and decoding with `asyncio.StreamReader` and
  `asyncio.StreamWriter`.
- Test suite with focus on roundtrip property tests using Hypothesis.

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

### Todo

- [ ] Research `ignorable`, handled correct?
- [ ] Use `extra=forbid` to make sure all details of schema handled.
- [ ] Use `mapKey`?
- [ ] Test suite that tests sending and receiving a few messages to an actual Kafka
      instance, should be pretty trivial to setup with docker.
- [ ] Introduce specialized types for primitives with limits (bytes and str) probably
      fine as-is, but all numeric types need validation.
- [ ] Use hypothesis to build entities and roundtrip-test all entities through an
      encode-decode cycle. The above point is required for this to work, ie all fields
      must use types that Hypothesis can introspect and yield valid values for. There is
      a test checked-in that uses this strategy, currently disabled with xfail.
- [ ] Github CI.
  - Automate download of schema from Kafka repo.
  - Generate schema and check for changes.
- [ ] Evaluate license, necessary to match Kafka, ie Apache?
- [ ] Treat `error_code` specially and generate an Enum for its values.
- [ ] Break out `Primitive` from `codegen` and define it in `kio`?? Should be useful for
      deserializing. Use it instead of strings inside Annotated, ie:
      `field(metadata={"kafka_type": Primitive.string})`.
- [ ] Setup sphinx docs with read-the-docs.
- [ ] Implement tagged fields as a dict on all flexible entities.
- [ ] NewType-types are named "entity", this should be renamed to something else. Entity
      is not wrong, but isn't very specific, and is too easy to mix up with schema model
      classes.

[revert]: https://github.com/python/cpython/issues/82423
