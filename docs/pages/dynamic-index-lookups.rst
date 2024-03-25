Dynamic index lookups
=====================

For many applications it is useful to be able to dynamically load schema
entities. For instance, if building an application that inspects the traffic
between a consumer or producer and a broker, we would like the ability to parse
arbitrary requests and responses sent between the two.

The Apache Kafka® Protocol has *lots of entities*, and while loading them all at
import time is definitely sometimes an option, as this is a fairly slow process,
it is not suitable for all applications.

The kio library provides the following APIs for applications where it's instead
deemed preferable to dynamically load schema entities.

Schema entity import functions
------------------------------

.. automodule:: kio.index
    :members:
    :show-inheritance:
