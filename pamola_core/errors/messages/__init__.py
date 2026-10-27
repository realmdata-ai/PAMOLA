"""
PAMOLA.CORE - Privacy-Preserving AI Data Processors
Part of PAMOLA.CORE, the open-source privacy-engineering library of the PAMOLA ecosystem.

Copyright (c) 2024-2026 Realm Inveo Inc. (REALMDATA)
Licensed under the MIT License; see the LICENSE file or
https://github.com/realmdata-ai/PAMOLA/blob/main/LICENSE

Package: pamola_core.errors.messages
Type: Internal (Non-Public API)

Author: Realm Inveo Inc.
"""

__all__ = [
    # registry.py
    "ErrorMessages",
    # utils.py
    "format_message",
    "validate_template_params_str",
]

from pamola_core.errors.messages.registry import ErrorMessages

from pamola_core.errors.messages.utils import format_message
from pamola_core.errors.messages.utils import validate_template_params_str

