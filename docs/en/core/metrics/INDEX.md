# Metrics Module Documentation Index

Quick navigation guide for all metrics module documentation.

## Core Framework

- **[Base Metrics Operation](./base_metrics_op.md)** - Foundation class for all metrics operations with lifecycle management, caching, and distributed processing support.

## Commons (Utilities & Shared Components)

Reusable utilities for metric calculation, data processing, and quality assessment. These
modules in `pamola_core.metrics.commons` do not have dedicated pages yet; see their docstrings.
Several of their entry points are part of the public API (`SchemaManager`, `RuleCode`,
`calculate_quality_with_rules`, `calculate_provisional_risk`, `calculate_predicted_utility`).

| Module | Purpose |
|--------|---------|
| `preprocessing` | Convert mixed data types to numeric format for distance calculations |
| `validation` | Dataset compatibility and metric input validation |
| `validation_rules` | Extensible framework for data quality rules (email, phone, date, SSN validation) |
| `aggregation` | Aggregate column/metric scores into dataset-level metrics |
| `normalize` | Normalize values, arrays, and metrics to standard scales |
| `safe_instantiate` | Safe class instantiation from dynamic config |
| `quality_scoring` | Data quality calculation (completeness, validity, diversity) |
| `predicted_utility_scoring` | Quick utility assessment on sampled subsets |
| `risk_scoring` | Re-identification risk estimation with attribute role detection |
| `schema_manager` | Field definitions, validation rule assignment, schema persistence |
| `model_budget` | Row budgets for the model-based utility metrics |

## Fidelity Metrics

Measure preservation of statistical properties and distribution characteristics.

### Distribution-Based
- **[KL Divergence](./fidelity/distribution/kl_divergence.md)** - Kullback-Leibler divergence with confidence levels
- **[KS Test](./fidelity/distribution/ks_test.md)** - Kolmogorov-Smirnov distribution test

### Statistical Properties
- **[Statistical Fidelity](./fidelity/statistical_fidelity.md)** - Mean, variance, correlation preservation metrics

### Operations
- **[Fidelity Operations](./operations/fidelity_ops.md)** - FidelityOperation wrapper for fidelity metric workflows

## Privacy Metrics

Evaluate disclosure risk and privacy preservation.

### Distance-Based
- **[Distance to Closest Record](./privacy/distance.md)** - DCR privacy metric with FAISS support for large-scale nearest neighbor search
- **[CVPL linkage exposure](./privacy/cvpl.md)** - Blocked, projected cosine linkage of a release against its source: existence of a link, and (with ground truth) the probability of the right identity; not a legal verdict

### Risk & Disclosure
- **[Disclosure Risk](./privacy/disclosure_risk.md)** - Prosecutor, journalist, marketer risk models
- **[Identity Risk](./privacy/identity.md)** - Record uniqueness and identity disclosure risk
- **[Nearest Neighbor Distance Ratio (NNDR)](./privacy/neighbor.md)** - Ratio of first to second nearest-neighbor distance

### Operations
- **[Privacy Operations](./operations/privacy_ops.md)** - PrivacyMetricOperation wrapper for privacy metric workflows

## Utility Metrics

Assess data utility and analytical value after anonymization.

### Classification
- **[Classification Utility](./utility/classification.md)** - Classification model performance assessment
- **[F1 Score](./utility/f1_score.md)** - F1 Score for binary and multi-class classification

### Regression
- **[Regression Utility](./utility/regression.md)** - Regression model performance assessment
- **[Mean Squared Error](./utility/mean_squared_error.md)** - MSE/RMSE for regression evaluation
- **[R² Score](./utility/r2_score.md)** - Coefficient of determination

### Information Loss
- **[Information Loss](./utility/information_loss.md)** - Generalization, suppression, and overall information loss
- **[L-Diversity Loss](./utility/ldiversity_loss.md)** - L-diversity preservation as utility metric

### Operations
- **[Utility Operations](./operations/utility_ops.md)** - UtilityMetricOperation wrapper for utility metric workflows

## Operations Wrappers

Higher-level operation interfaces for metric workflows.

- **[Fidelity Operations](./operations/fidelity_ops.md)** - FidelityOperation for end-to-end fidelity assessment
- **[Privacy Operations](./operations/privacy_ops.md)** - PrivacyMetricOperation for privacy evaluation
- **[Utility Operations](./operations/utility_ops.md)** - UtilityMetricOperation for utility assessment

---

## Quick Reference by Use Case

### "How much privacy is preserved?"
→ Start with **[Privacy Operations](./operations/privacy_ops.md)**
→ Then explore **[Distance to Closest Record](./privacy/distance.md)**, **[Disclosure Risk](./privacy/disclosure_risk.md)**

### "Is my anonymized data still useful?"
→ Start with **[Utility Operations](./operations/utility_ops.md)**
→ Then explore **[Classification Utility](./utility/classification.md)**, **[Regression Utility](./utility/regression.md)**, **[Information Loss](./utility/information_loss.md)**

### "Does my synthetic data match the original?"
→ Start with **[Fidelity Operations](./operations/fidelity_ops.md)**
→ Then explore **[Statistical Fidelity](./fidelity/statistical_fidelity.md)**, **[KL Divergence](./fidelity/distribution/kl_divergence.md)**, **[KS Test](./fidelity/distribution/ks_test.md)**

### "What's the data quality before metrics?"
→ Start with `calculate_quality_with_rules()` (`pamola_core.metrics.commons`)
→ Then explore `pamola_core.metrics.commons.validation_rules`

### "How risky is this data?"
→ Start with `calculate_provisional_risk()` (`pamola_core.metrics.commons.risk_scoring`)
→ Then explore **[Disclosure Risk](./privacy/disclosure_risk.md)**, **[Distance to Closest Record](./privacy/distance.md)**

---

## Related Documentation

- **[Documentation Index](../README.md)** - All PAMOLA.CORE module documentation
- **[Attacks](../attacks/index.md)** - Linkage and attribute inference attacks
