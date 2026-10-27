# Attacks Module Documentation

**Module:** `pamola_core.attacks` (experimental, internal package - not exported from `pamola_core.__init__`)

## Table of Contents
1. [Overview](#overview)
2. [Attack Types](#attack-types)
3. [Quick Comparison](#quick-comparison)
4. [Module Architecture](#module-architecture)
5. [Common Workflow](#common-workflow)
6. [Key Concepts](#key-concepts)
7. [Related Components](#related-components)

## Overview

The `attacks` module provides privacy risk simulation tools for testing anonymized data robustness. It carries only the attacks that measure **anonymization** quality:
- Re-identify individuals (linkage attacks)
- Infer hidden sensitive attributes (attribute inference)

**Not in this package:** membership inference (a model-privacy question, outside the scope of
`pamola_core`) and singling-out. Distance to Closest Record (DCR) and Nearest Neighbor Distance
Ratio (NNDR) are privacy metrics in `pamola_core.metrics.privacy`; see
[Distance (DCR)](../metrics/privacy/distance.md) and [Neighbor (NNDR)](../metrics/privacy/neighbor.md).

**Use Case:** After anonymization, run attacks to verify the privacy level achieved:
```python
from pamola_core.attacks import LinkageAttack, AttributeInference, AttackMetrics

# Test if linkage attack can re-identify people
linkage = LinkageAttack()
matches = linkage.record_linkage_attack(original_data, anonymized_data, keys)

# Test if a hidden attribute can be inferred
inference = AttributeInference()
predicted = inference.attribute_inference_attack(train_data, test_data, "diagnosis")
```

## Attack Types

| Attack | Purpose | Input | Output | Difficulty |
|--------|---------|-------|--------|------------|
| **Linkage** | Re-identify records by matching common attributes | 2 datasets + keys | Match pairs (DataFrame) | Medium |
| **Attribute Inference** | Infer missing sensitive attribute | 2 datasets + target field | Predicted values (Series) | Low |

## Quick Comparison

### When to Use Each Attack

**Linkage Attack**
- Goal: Can attacker re-identify individuals?
- When: You have external datasets with overlapping attributes
- Risk: High if quasi-identifiers not removed

**Attribute Inference**
- Goal: Can attacker guess missing sensitive attributes?
- When: Some attributes are partially visible in anonymized data
- Risk: Medium - uses entropy-based feature selection

**DCR / NNDR Metrics** (in `pamola_core.metrics.privacy`, not in this package)
- Goal: Direct privacy metrics without binary prediction
- When: You want numerical risk scores
- See [Distance (DCR)](../metrics/privacy/distance.md) and [Neighbor (NNDR)](../metrics/privacy/neighbor.md)

## Module Architecture

```
pamola_core.attacks/
├── base.py                          # AttackInitialization (abstract)
├── preprocess_data.py               # PreprocessData (TF-IDF + scaling)
├── linkage_attack.py                # LinkageAttack (3 variants)
├── attribute_inference.py           # AttributeInference (entropy-based)
├── attack_metrics.py                # AttackMetrics (evaluation metrics)
└── __init__.py                      # Package exports
```

### Class Hierarchy
```
AttackInitialization (ABC)
  └─ PreprocessData
       ├─ LinkageAttack
       ├─ AttributeInference
       └─ AttackMetrics
```

All attack classes inherit from `PreprocessData`, which provides TF-IDF vectorization and numeric scaling.

## Common Workflow

### 1. Setup
```python
from pamola_core.attacks import LinkageAttack, AttackMetrics
import numpy as np
import pandas as pd

# Load datasets
original = pd.read_csv("original.csv")
anonymized = pd.read_csv("anonymized.csv")
```

### 2. Run Attacks
```python
# Linkage: direct record matching
linkage = LinkageAttack()
matches = linkage.record_linkage_attack(original, anonymized, linkage_keys=["name", "dob"])
```

### 3. Evaluate
```python
# Ground truth and predictions are 0/1 arrays you derive from the attack output
# (for example: 1 = record correctly re-identified)
metrics_obj = AttackMetrics()
results = metrics_obj.attack_metrics(y_true, y_pred)
asr = metrics_obj.attack_success_rate(y_true, y_pred)
rrs = metrics_obj.residual_risk_score(y_true, y_pred)

print(f"Attack Accuracy: {results['Attack Accuracy']}")
print(f"Attack Success Rate: {asr}")
print(f"Residual Risk Score: {rrs}")
```

### 4. Interpret Results
- **High Attack Accuracy (>0.7)** → Anonymization is weak
- **Low Attack Accuracy (<0.55)** → Anonymization is strong
- **ASR > 0.5** → Many true positives identified (risky)
- **RRS > 0.3** → Significant privacy risk

## Key Concepts

### Data Preprocessing
All attacks use `PreprocessData.preprocess_data()`:
- **Categorical columns** → TF-IDF vectorization (`max_features=5000` by default)
- **Numeric columns** → Standard scaling (zero mean, unit variance)
- **Result:** Combined numeric feature matrix for similarity/distance computation

### Feature Importance in Attacks
- **High-entropy features** → Less predictive (removed by AttributeInference)
- **Low-entropy features** → More predictive (used in AttributeInference)
- Entropy = -Σ(p * log2(p)) where p = probability of each value

## Related Components

- **[Profiling Module](../profiling/)** — Analyze dataset characteristics before anonymization
- **[Metrics Module](../metrics/)** — Compute privacy metrics (DCR, NNDR, disclosure risk)
- **[Privacy Models](../privacy_models/)** — Model privacy risks at the data level
- **[Anonymization Module](../anonymization/)** — Apply transformations (masking, generalization)

## Export Reference

Names exported by `pamola_core.attacks`:
```python
from pamola_core.attacks import (
    # Base
    AttackInitialization,
    BaseAttack,            # alias of AttackInitialization

    # Attacks
    LinkageAttack,
    AttributeInference,
    AttributeInferenceAttack,  # alias of AttributeInference

    # Metrics
    AttackMetrics,
)
```

## Next Steps

- **[Base Attack](./base_attack.md)** — Abstract interfaces
- **[Linkage Attack](./linkage_attack.md)** — Re-identification techniques
- **[Attribute Inference](./attribute_inference.md)** — Hidden attribute inference
- **[Distance Metrics](../metrics/privacy/distance.md)** — DCR computation (metrics package)
- **[Attack Metrics](./attack_metrics.md)** — Evaluation and scoring
