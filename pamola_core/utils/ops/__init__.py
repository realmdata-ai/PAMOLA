"""
PAMOLA.CORE - Privacy-Preserving AI Data Processors
Part of PAMOLA.CORE, the open-source privacy-engineering library of the PAMOLA ecosystem.

Copyright (c) 2024-2026 Realm Inveo Inc. (REALMDATA)
Licensed under the MIT License; see the LICENSE file or
https://github.com/realmdata-ai/PAMOLA/blob/main/LICENSE

Package: pamola_core.utils.ops
Type: Internal (Non-Public API)

Author: Realm Inveo Inc.
"""

__all__ = [
    # op_base.py
    "BaseOperation",
    # op_data_source.py
    "DataSource",
    # op_result.py
    "OperationStatus",
]

from pamola_core.utils.ops.op_base import BaseOperation

from pamola_core.utils.ops.op_data_source import DataSource

from pamola_core.utils.ops.op_result import OperationStatus

