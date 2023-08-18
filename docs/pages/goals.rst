Project goals
=============

Primary goals
-------------

- Provide correct and typing-friendly models for the entirety of the Apache Kafka® Protocol, by
  generating from the upstream schema specification.
- Expose user-friendly APIs for serializing and parsing protocol messages.

Secondary goals
---------------

- Serialization and parsing performance, this might become a primary goal in the future.

Non-goals
---------

- Implementing a full consumer or producer.
- Implementing "client" code. This is avoided to allow this package to be as small and
  maintainable as possible. Implementing features that are subject to tuning, such as
  message retries, timeouts, and all the usual suspects that network calling code has to
  deal with, would be counter-productive to this goal.
