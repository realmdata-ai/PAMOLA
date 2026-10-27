"""HIER-01: a hierarchy level may keep a value as it is.

In the classic Adult education hierarchy "HS-grad" stays "HS-grad" at the first level while
"10th" becomes "Dropout"; ARX and anjana accept this. The dictionary validator called such an
entry a "potential circular reference", so ``CategoricalGeneralizationOperation`` refused the
whole file — and since only the first 100 entries were checked, the outcome depended on the
order of the rows.
"""

import pandas as pd
import pytest

from pamola_core.anonymization.commons.hierarchy_dictionary import HierarchyDictionary
from pamola_core.anonymization.generalization.categorical_op import CategoricalGeneralizationOperation
from pamola_core.utils.ops.op_data_source import DataSource
from pamola_core.utils.ops.op_result import OperationStatus

EDUCATION = [
    ("10th", "Dropout", "Low"),
    ("11th", "Dropout", "Low"),
    ("HS-grad", "HS-grad", "Low"),
    ("Some-college", "Some-college", "Medium"),
    ("Bachelors", "Bachelors", "High"),
    ("Masters", "Postgraduate", "High"),
]


def _write_hierarchy(path, rows):
    pd.DataFrame(rows, columns=["value", "level_1", "level_2"]).to_csv(path, index=False)
    return path


@pytest.mark.parametrize("filler", [0, 150], ids=["short", "identity_after_row_100"])
def test_identity_level_is_a_valid_hierarchy(tmp_path, filler):
    rows = [(f"code-{i}", f"group-{i % 7}", "Other") for i in range(filler)] + EDUCATION
    hierarchy = HierarchyDictionary()
    hierarchy.load_from_file(_write_hierarchy(tmp_path / "education.csv", rows), "csv")

    is_valid, issues = hierarchy.validate_structure()

    assert is_valid, issues
    assert hierarchy.get_hierarchy("HS-grad", 1) == "HS-grad"


@pytest.mark.parametrize("level,expected", [(1, ["Dropout", "HS-grad", "Bachelors", "Postgraduate"]),
                                            (2, ["Low", "Low", "High", "High"])])
def test_generalization_applies_a_hierarchy_with_identity_levels(tmp_path, level, expected):
    path = _write_hierarchy(tmp_path / "education.csv", EDUCATION)
    frame = pd.DataFrame({"education": ["10th", "HS-grad", "Bachelors", "Masters"]})
    op = CategoricalGeneralizationOperation(field_name="education", strategy="hierarchy",
                                            hierarchy_level=level, external_dictionary_path=str(path),
                                            use_cache=False)

    result = op.execute(DataSource(dataframes={"main": frame}), tmp_path / "task", None)

    assert result.status == OperationStatus.SUCCESS, result.error_message
    out = pd.read_csv(next((tmp_path / "task" / "output").glob("*_output_*.csv")))
    assert out["education"].tolist() == expected
