Schema
======

Schema entities are generated from `the upstream schema specification
<https://github.com/apache/kafka/tree/79b5f7f/clients/src/main/resources/common/message>`_.
Every API version has separate schema entities, to allow best-in-class typing support
for message models. Schema entities are exposed in sub-modules under the
:mod:`kio.schema` package, following this structure:
``kio.schema.<api-name>.<version>.<type>``. So for example, if you want to use the
response for version 12 of the metadata API, you would import it like so.

.. code-block:: python

    from kio.schema.metadata.v12.request import MetadataRequest

Aiven protocol extensions
-------------------------

KIO also includes the pre-KIP Aiven ``DecommissionController`` v0 extension
at API key 94. Its request and response wire layout is compatible with the
upstream ``UnregisterController`` v0 API introduced by KIP-1312, but the
Aiven operation records a decommission marker and does not physically remove
the controller registration. KIO provides only the protocol types; server
lifecycle behavior belongs to the Kafka implementation and its caller.

Introspection protocols
-----------------------

.. automodule:: kio.static.protocol
    :members:
    :show-inheritance:
    :special-members: __version__, __flexible__, __api_key__, __header_schema__

Primitives
----------

.. automodule:: kio.static.primitive
    :members:
    :show-inheritance:

Types
-----

.. automodule:: kio.schema.types
    :members:
    :show-inheritance:

Constants
---------

.. automodule:: kio.static.constants
    :members:
    :show-inheritance:
