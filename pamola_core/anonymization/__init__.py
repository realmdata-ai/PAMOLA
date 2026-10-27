"""
PAMOLA.CORE - Privacy-Preserving AI Data Processors
Part of PAMOLA.CORE, the open-source privacy-engineering library of the PAMOLA ecosystem.

Copyright (c) 2024-2026 Realm Inveo Inc. (REALMDATA)
Licensed under the MIT License; see the LICENSE file or
https://github.com/realmdata-ai/PAMOLA/blob/main/LICENSE

Package: pamola_core.anonymization
Type: Public API Package

Author: Realm Inveo Inc.
"""

__all__ = [
    "AttributeSuppressionOperation",
    "CategoricalGeneralizationOperation",
    "CellSuppressionOperation",
    "ConsistentMappingPseudonymizationOperation",
    "DateTimeGeneralizationOperation",
    "FullMaskingOperation",
    "HashBasedPseudonymizationOperation",
    "NumericGeneralizationOperation",
    "PartialMaskingOperation",
    "RecordSuppressionOperation",
    "UniformNumericNoiseOperation",
    "UniformTemporalNoiseOperation",
]

from pamola_core.anonymization.suppression.attribute_op import AttributeSuppressionOperation

from pamola_core.anonymization.generalization.categorical_op import CategoricalGeneralizationOperation

from pamola_core.anonymization.suppression.cell_op import CellSuppressionOperation

from pamola_core.anonymization.pseudonymization.mapping_op import ConsistentMappingPseudonymizationOperation

from pamola_core.anonymization.generalization.datetime_op import DateTimeGeneralizationOperation

from pamola_core.anonymization.masking.full_masking_op import FullMaskingOperation

from pamola_core.anonymization.pseudonymization.hash_based_op import HashBasedPseudonymizationOperation

from pamola_core.anonymization.generalization.numeric_op import NumericGeneralizationOperation

from pamola_core.anonymization.masking.partial_masking_op import PartialMaskingOperation

from pamola_core.anonymization.suppression.record_op import RecordSuppressionOperation

from pamola_core.anonymization.noise.uniform_numeric_op import UniformNumericNoiseOperation

from pamola_core.anonymization.noise.uniform_temporal_op import UniformTemporalNoiseOperation