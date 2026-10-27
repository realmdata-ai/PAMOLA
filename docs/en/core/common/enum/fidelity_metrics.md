# Fidelity Metrics Enumeration

**Module:** `pamola_core.common.enum.fidelity_metrics_type`
**Class:** `FidelityMetricsType`

## Table of Contents
1. [Overview](#overview)
2. [Enum Members](#enum-members)
3. [Metric Definitions](#metric-definitions)
4. [Usage Examples](#usage-examples)
5. [Best Practices](#best-practices)
6. [Related Components](#related-components)

## Overview

`FidelityMetricsType` is a string-based enumeration of the statistical metrics that
`FidelityOperation` (`pamola_core.metrics.operations.fidelity_ops`) can compute when comparing
original and anonymized datasets. Every member is wired into the `FidelityOperation` metric
registry, so every member is selectable.

**Parent Class:** `str, Enum`
**Type:** String Enum
**Used By:** `FidelityOperation` (`fidelity_metrics` parameter; default `["ks", "kl"]`)

> Jensen-Shannon (`JS`) and Wasserstein (`WASSERSTEIN`) members were removed in the 1.0
> cleanup because no metric implementation was registered for them. A former duplicate module,
> `pamola_core.common.enum.fidelity_metrics` (`FidelityMetrics`), was removed at the same time.

## Enum Members

| Member | Value | Description |
|--------|-------|-------------|
| `KS` | `"ks"` | Kolmogorov-Smirnov test. Compares distributions via max difference in cumulative distribution functions. |
| `KL` | `"kl"` | Kullback-Leibler divergence. Measures asymmetric divergence between probability distributions. |

## Metric Definitions

### KS (Kolmogorov-Smirnov Test)

**Formula:** `D = max|F_orig(x) - F_anon(x)|`

where F is the cumulative distribution function

**Characteristics:**
- Tests whether two distributions are different
- Computes maximum vertical distance between CDFs
- Distribution-free (no assumptions about distribution shape)
- Sensitive to differences anywhere in distribution
- Range: [0, 1] where 0 = identical, 1 = completely different
- Single-valued test statistic

**Interpretation:**
- KS = 0: Distributions are identical
- KS = 0.05: Slight difference
- KS = 0.2: Moderate difference
- KS = 0.5: Large difference

**Advantages:**
- Non-parametric (no distribution assumptions)
- Easy to interpret
- Fast computation
- Good for continuous data

**Disadvantages:**
- Only considers univariate distributions
- May be overly sensitive to location vs. scale differences
- Doesn't account for probability mass

**Use Cases:**
- Quick distribution comparison
- Goodness-of-fit testing
- Comparing continuous numeric columns

**Example:**
```
Original: Normal distribution (μ=0, σ=1)
Anonymized: Uniform distribution (0-1 range)
KS = 0.45  (Moderate difference in distributions)
```

### KL (Kullback-Leibler Divergence)

**Formula:** `D_KL(P||Q) = Σ P(x) * log(P(x)/Q(x))`

**Characteristics:**
- Asymmetric measure (KL(P||Q) ≠ KL(Q||P))
- Information-theoretic divergence
- Measures information loss when using Q instead of P
- Range: [0, ∞) where 0 = identical
- Undefined if Q(x)=0 and P(x)≠0

**Interpretation:**
- KL = 0: Distributions identical
- KL = 0.01: Very similar
- KL = 0.1: Similar
- KL = 1.0: Significantly different
- KL > 5: Very different

**Advantages:**
- Mathematically elegant
- Theoretically well-founded
- Captures subtle distribution differences
- Useful for optimization

**Disadvantages:**
- Asymmetric (depends on direction)
- Can be infinite/undefined
- Less intuitive interpretation
- Computationally expensive for large data

**Use Cases:**
- Variational inference
- Generative model evaluation
- Distribution divergence measurement
- Optimization objectives

**Example:**
```
Original: {A: 0.5, B: 0.3, C: 0.2}
Anonymized: {A: 0.4, B: 0.4, C: 0.2}
KL(Original||Anonymized) = 0.057
KL(Anonymized||Original) = 0.051
(Different values show asymmetry)
```

## Usage Examples

### Basic Enum Usage

```python
from pamola_core.common.enum.fidelity_metrics_type import FidelityMetricsType

metric = FidelityMetricsType.KS
print(metric.value)                    # "ks"
print(FidelityMetricsType("kl"))       # FidelityMetricsType.KL
print([m.value for m in FidelityMetricsType])  # ["ks", "kl"]
```

### Selecting Metrics for FidelityOperation

```python
from pamola_core import FidelityOperation
from pamola_core.common.enum.fidelity_metrics_type import FidelityMetricsType

op = FidelityOperation(
    fidelity_metrics=[FidelityMetricsType.KS.value, FidelityMetricsType.KL.value],
)
```

## Best Practices

1. **Use both metrics for a complete picture** - KS is bounded and easy to interpret; KL is
   sensitive to probability-mass changes in specific categories/bins.
2. **Use the enum values, not literals** - `FidelityMetricsType.KS.value` instead of `"ks"`
   avoids typos.
3. **Document thresholds** - e.g. KS < 0.1 indicates minimal distribution change; KL close to 0
   indicates very similar distributions.

## Related Components

- **UtilityMetricsType** (`pamola_core.common.enum.utility_metrics_type`) - Utility measurements
- **DistanceMetricType** (`pamola_core.common.enum.distance_metric_type`) - Distance metrics
- **FidelityOperation** ([Fidelity Ops](../../metrics/operations/fidelity_ops.md)) - Computes the metrics
- **Metric implementations** - `pamola_core.metrics.fidelity.distribution.ks_test`, `pamola_core.metrics.fidelity.distribution.kl_divergence`

## Metric Comparison

| Metric | Type | Symmetry | Boundedness | Use Case |
|--------|------|----------|-------------|----------|
| **KS** | Statistical | Yes | [0,1] | Univariate distribution comparison |
| **KL** | Information-theoretic | No | [0,∞) | Divergence / information loss |
