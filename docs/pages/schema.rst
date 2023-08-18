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
