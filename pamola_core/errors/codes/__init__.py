"""
PAMOLA.CORE - Privacy-Preserving AI Data Processors
Part of PAMOLA.CORE, the open-source privacy-engineering library of the PAMOLA ecosystem.

Copyright (c) 2024-2026 Realm Inveo Inc. (REALMDATA)
Licensed under the MIT License; see the LICENSE file or
https://github.com/realmdata-ai/PAMOLA/blob/main/LICENSE

Package: pamola_core.errors.codes
Type: Internal (Non-Public API)

Author: Realm Inveo Inc.
"""

__all__ = [
    # registry.py
    "ErrorCode",
    # metadata.py
    "ERROR_CODE_METADATA",
    "get_error_metadata",
    # utils.py
    "validate_error_code_usage",
    "get_error_info",
    "format_error_help",
]

from pamola_core.errors.codes.registry import ErrorCode

from pamola_core.errors.codes.metadata import ERROR_CODE_METADATA
from pamola_core.errors.codes.metadata import get_error_metadata

from pamola_core.errors.codes.utils import validate_error_code_usage
from pamola_core.errors.codes.utils import get_error_info
from pamola_core.errors.codes.utils import format_error_help

