"""
    PAMOLA Core - IO Package Base Module
    -----------------------------------
    This module provides base interfaces and protocols for all IO operations in the PAMOLA Core
    library. It defines the standard contracts that all format-specific handlers must implement.

    Key features:
    - DataReader protocol for standardized data reading
    - DataWriter protocol for standardized data writing

    This module serves as the foundation for all IO operations in PAMOLA Core, ensuring
    consistency across different data formats and storage methods.

    Copyright (c) 2024-2026 Realm Inveo Inc. (REALMDATA)

    This software is licensed under the MIT License.
    For details, see the LICENSE file or visit:
        https://opensource.org/license/mit
        https://github.com/realmdata-ai/PAMOLA/blob/main/LICENSE

    Author: Realm Inveo Inc.
"""

from typing import Protocol, Any

class DataReader(Protocol):
    def read(self, path: str, **kwargs) -> Any: ...

class DataWriter(Protocol):
    def write(self, data: Any, path: str, **kwargs) -> Any: ...

def data_read(obj: DataReader, path: str, **kwargs) -> Any:
    return obj.read(path, **kwargs)

def data_write(obj: DataWriter, data: Any, path: str, **kwargs) -> Any:
    return obj.write(data, path, **kwargs)
