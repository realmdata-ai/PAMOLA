"""
PAMOLA.CORE - Privacy-Preserving AI Data Processors
Part of PAMOLA.CORE, the open-source privacy-engineering library of the PAMOLA ecosystem.

Copyright (c) 2024-2026 Realm Inveo Inc. (REALMDATA)
Licensed under the MIT License; see the LICENSE file or
https://github.com/realmdata-ai/PAMOLA/blob/main/LICENSE

Package: pamola_core.io
Type: Public API Package

Author: Realm Inveo Inc.
"""

__all__ = [
    # csv/
    "read_csv",
    # json/
    "read_json",
    # excel/
    "read_excel",
    # parquet/
    "read_parquet",
]

from pamola_core.io.csv import read_csv

from pamola_core.io.json import read_json

from pamola_core.io.excel import read_excel

from pamola_core.io.parquet import read_parquet

