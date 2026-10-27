"""
PAMOLA.CORE - Column Validation Utilities
This module provides utility functions for validating the existence of columns
in Pandas DataFrames. It ensures that specified columns are present before
performing any operations, preventing runtime errors.

Features:
 - Check if a column exists in a DataFrame.
 - Raise a `ValueError` if the column is missing.
 - Improve code reusability and maintainability.

This module is useful for data preprocessing, validation steps, and ensuring
data integrity before transformations.

Copyright (c) 2024-2026 Realm Inveo Inc. (REALMDATA)

This software is licensed under the MIT License.
For details, see the LICENSE file or visit:

    https://opensource.org/license/mit
    https://github.com/realmdata-ai/PAMOLA/blob/main/LICENSE

Author: Realm Inveo Inc.
"""

from typing import List
import pandas as pd
from pamola_core.errors.exceptions import ColumnNotFoundError


def check_columns_exist(data: pd.DataFrame, target_fields: List):
    """
    Check if all specified columns exist in the DataFrame.

    Parameters
    -----------
    data : pd.DataFrame
        The DataFrame to check.
    target_fields : list
        List of column names to verify existence in the DataFrame.

    Raises
    -------
    ValueError
        If any of the target columns do not exist in the DataFrame.
    """
    missing_cols = [col for col in target_fields if col not in data.columns]
    if missing_cols:
        raise ColumnNotFoundError(
            column_name=missing_cols,
        )
