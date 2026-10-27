"""
PAMOLA.CORE - Privacy-Preserving AI Data Processors
Part of PAMOLA.CORE, the open-source privacy-engineering library of the PAMOLA ecosystem.

Copyright (c) 2024-2026 Realm Inveo Inc. (REALMDATA)
Licensed under the MIT License; see the LICENSE file or
https://github.com/realmdata-ai/PAMOLA/blob/main/LICENSE

Package: pamola_core.fake_data
Type: Public API Package

Author: Realm Inveo Inc.
"""

__all__ = [
    "FakeEmailOperation",
    "FakeNameOperation",
    "FakeOrganizationOperation",
    "FakePhoneOperation",
]

from pamola_core.fake_data.operations.email_op import FakeEmailOperation

from pamola_core.fake_data.operations.name_op import FakeNameOperation

from pamola_core.fake_data.operations.organization_op import FakeOrganizationOperation

from pamola_core.fake_data.operations.phone_op import FakePhoneOperation

