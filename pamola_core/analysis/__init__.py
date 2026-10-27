"""
PAMOLA.CORE - Privacy-Preserving AI Data Processors
Part of PAMOLA.CORE, the open-source privacy-engineering library of the PAMOLA ecosystem.

Copyright (c) 2024-2026 Realm Inveo Inc. (REALMDATA)
Licensed under the MIT License; see the LICENSE file or
https://github.com/realmdata-ai/PAMOLA/blob/main/LICENSE

Package: pamola_core.analysis
Type: Public API Package

Author: Realm Inveo Inc.
"""

__all__ = [
    # dataset_summary.py
    "analyze_dataset_summary",
    # privacy_risk.py
    "calculate_full_risk",
    # descriptive_stats.py
    "analyze_descriptive_stats",
    # distribution.py
    "visualize_distribution_df",
    # correlation.py
    "analyze_correlation",
]

from pamola_core.analysis.correlation import analyze_correlation

from pamola_core.analysis.dataset_summary import analyze_dataset_summary

from pamola_core.analysis.descriptive_stats import analyze_descriptive_stats

from pamola_core.analysis.privacy_risk import calculate_full_risk

from pamola_core.analysis.distribution import visualize_distribution_df

