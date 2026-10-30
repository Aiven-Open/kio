Project goals
=============

Goals
-----

- Provide correct and typing-friendly models for the entirety of the Apache Kafka® Protocol, by
  generating from the upstream schema specification.
- Expose user-friendly APIs for serializing and parsing protocol messages.
- Provide a `sans-IO`_ implementation of the protocol. Messages are parsed from any
  object that implements the buffer protocol and serialized to any writable binary
  stream, leaving all network IO to the caller. This keeps kio usable as the protocol
  layer of any client, synchronous or asynchronous.
- Deliver high serialization and parsing performance. Parsing is implemented natively in
  Rust, and the goal is to move serialization and record batch handling into the native
  extension as well. Progress is tracked in `issue #214`_.

.. _sans-IO: https://sans-io.readthedocs.io/how-to-sans-io.html
.. _issue #214: https://github.com/Aiven-Open/kio/issues/214

Non-goals
---------

- Implementing a full consumer or producer.
- Implementing "client" code. This is avoided to allow this package to be as small and
  maintainable as possible. Implementing features that are subject to tuning, such as
  message retries, timeouts, and all the usual suspects that network calling code has to
  deal with, would be counter-productive to this goal.
