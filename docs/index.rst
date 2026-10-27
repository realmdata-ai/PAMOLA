PAMOLA Core API Reference
=========================

**PAMOLA Core** is an open-source Python library for privacy-preserving data
operations developed by `Realm Inveo Inc. (REALMDATA) <https://realmdata.ai>`_.

Complete reference for every public symbol exported by ``pamola_core``.
All public APIs are importable directly from the top-level package.

Quick Example
-------------

.. code-block:: python

   import pamola_core as pc

   df = pc.read_csv("data.csv")
   op = pc.FullMaskingOperation(...)
   result = op.execute(df)


API Reference
-------------

.. autosummary::
   :toctree: generated

   pamola_core
   pamola_core.anonymization
   pamola_core.fake_data
   pamola_core.profiling
   pamola_core.transformations
   pamola_core.metrics
   pamola_core.analysis
   pamola_core.io
   pamola_core.utils

----

Indices and Tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
