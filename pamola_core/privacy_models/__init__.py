"""
PAMOLA.CORE - Privacy-Preserving AI Data Processors
Part of PAMOLA.CORE, the open-source privacy-engineering library of the PAMOLA ecosystem.

Copyright (c) 2024-2026 Realm Inveo Inc. (REALMDATA)
Licensed under the MIT License; see the LICENSE file or
https://github.com/realmdata-ai/PAMOLA/blob/main/LICENSE

Package: pamola_core.privacy_models
Type: Public API Package

Author: Realm Inveo Inc.
"""

__all__ = [
    # Base
    "BasePrivacyModelProcessor",
    "PrivacyModel",
    # Core models
    "KAnonymityProcessor",
    "KAnonymityModel",
    "LDiversityCalculator",
    "LDiversityModel",
    "TCloseness",
    "TClosenessModel",
    # Reports
    "KAnonymityReport",
    "LDiversityReport",
    # Metrics / risk
    "LDiversityMetricsCalculator",
    "LDiversityPrivacyRiskAssessor",
    "AttributeDisclosureRiskAnalyzer",
    "RiskInterpreter",
    # Strategies / config
    "AnonymizationStrategy",
    "SuppressionStrategy",
    "FullMaskingStrategy",
    "PartialMaskingStrategy",
    "LDiversityModelApplicator",
]

from pamola_core.privacy_models.base import BasePrivacyModelProcessor
from pamola_core.privacy_models.base import BasePrivacyModelProcessor as PrivacyModel

from pamola_core.privacy_models.k_anonymity.calculation import KAnonymityProcessor
from pamola_core.privacy_models.k_anonymity.calculation import KAnonymityProcessor as KAnonymityModel

from pamola_core.privacy_models.l_diversity.calculation import LDiversityCalculator
from pamola_core.privacy_models.l_diversity.calculation import LDiversityCalculator as LDiversityModel

from pamola_core.privacy_models.t_closeness.calculation import TCloseness
from pamola_core.privacy_models.t_closeness.calculation import TCloseness as TClosenessModel

from pamola_core.privacy_models.k_anonymity.ka_reporting import KAnonymityReport

from pamola_core.privacy_models.l_diversity.reporting import LDiversityReport

from pamola_core.privacy_models.l_diversity.metrics import LDiversityMetricsCalculator

from pamola_core.privacy_models.l_diversity.privacy import LDiversityPrivacyRiskAssessor

from pamola_core.privacy_models.l_diversity.attribute_risk import AttributeDisclosureRiskAnalyzer

from pamola_core.privacy_models.l_diversity.interpretation import RiskInterpreter

from pamola_core.privacy_models.l_diversity.apply_model import AnonymizationStrategy
from pamola_core.privacy_models.l_diversity.apply_model import SuppressionStrategy
from pamola_core.privacy_models.l_diversity.apply_model import FullMaskingStrategy
from pamola_core.privacy_models.l_diversity.apply_model import PartialMaskingStrategy
from pamola_core.privacy_models.l_diversity.apply_model import LDiversityModelApplicator

