# Attacks Module Index

**Module:** `pamola_core.attacks` (experimental, internal package - not exported from `pamola_core.__init__`)
**Location:** `docs/en/core/attacks/`

The package carries only the attacks that measure **anonymization** quality: record linkage
and attribute inference. Membership inference (a model-privacy question) and singling-out are
not part of `pamola_core`. Distance to Closest Record (DCR) and Nearest Neighbor Distance Ratio
(NNDR) are privacy **metrics**, implemented in `pamola_core.metrics.privacy` and documented in
[Distance (DCR)](../metrics/privacy/distance.md) and [Neighbor (NNDR)](../metrics/privacy/neighbor.md).

## Quick Navigation

### Start Here
**→ [Attacks Overview](./attacks_overview.md)** — Module entry point with attack comparison table, architecture, and workflow

### Attack Classes

#### Re-Identification Attacks
- **[Linkage Attack](./linkage_attack.md)** — 3 record linkage methods
  - `record_linkage_attack()` — Exact matching
  - `probabilistic_linkage_attack()` — Fuzzy matching (Fellegi-Sunter)
  - `cluster_vector_linkage_attack()` — TruncatedSVD + cosine similarity (CVPLA)

#### Attribute Attacks
- **[Attribute Inference](./attribute_inference.md)** — Sensitive attribute guessing
  - `attribute_inference_attack()` — Entropy-based feature selection

#### Evaluation
- **[Attack Metrics](./attack_metrics.md)** — Attack effectiveness evaluation
  - `attack_metrics()` — Comprehensive metrics (accuracy, precision, recall, F1, AUC, advantage)
  - `attack_success_rate()` — ASR metric
  - `residual_risk_score()` — RRS metric

### Foundation
- **[Base Attack](./base_attack.md)** — Abstract interfaces
  - `AttackInitialization` class (alias `BaseAttack`)
  - `PreprocessData` helper class (`pamola_core.attacks.preprocess_data`)

## By Task

### I need to test privacy of anonymized data
1. Start with [Attacks Overview](./attacks_overview.md) — understand threat model
2. Choose attack type based on your data:
   - Exact/deterministic attributes → [Linkage Attack](./linkage_attack.md) → `record_linkage_attack()`
   - Noisy/real-world attributes → [Linkage Attack](./linkage_attack.md) → `probabilistic_linkage_attack()`
   - Multi-dimensional data → [Linkage Attack](./linkage_attack.md) → `cluster_vector_linkage_attack()`
3. Measure distance-based risk with the privacy metrics:
   - Baseline similarity → [DCR](../metrics/privacy/distance.md)
   - Confidence in matches → [NNDR](../metrics/privacy/neighbor.md)
4. Evaluate success → [Attack Metrics](./attack_metrics.md)

### I need to infer hidden attributes
1. Read [Attribute Inference](./attribute_inference.md) — understand entropy-based selection
2. Run `attribute_inference_attack()` with:
   - Training data (complete attributes)
   - Test data (partial attributes)
   - Target attribute name (to infer)
3. Evaluate prediction accuracy with standard ML metrics

### I'm implementing a custom attack
1. Read [Base Attack](./base_attack.md) — understand interface
2. Inherit from `PreprocessData` (not `AttackInitialization`)
3. Implement required methods:
   - `process()` — your attack logic
   - `preprocess_data()` — inherited from parent
4. Use [Attack Metrics](./attack_metrics.md) to evaluate results

### I need to understand a metric
- **DCR** → [Distance (DCR)](../metrics/privacy/distance.md) — "How far is each transformed record from the nearest original record?"
- **NNDR** → [Neighbor (NNDR)](../metrics/privacy/neighbor.md) — "Is the closest match clearly closer than the second closest?"
- **Accuracy** → [Attack Metrics](./attack_metrics.md) → "Overall correctness of attack predictions"
- **ASR** → [Attack Metrics](./attack_metrics.md) → "What % of actual positives were identified?"
- **RRS** → [Attack Metrics](./attack_metrics.md) → "Is attack better than random guessing?"

## Attack Selection Guide

| If You Have | Best Attack | Alternative |
|------------|-------------|-------------|
| Original + anonymized datasets | Linkage | DCR/NNDR metrics |
| Clear quasi-identifiers | Record Linkage | Probabilistic Linkage |
| Noisy/misspelled data | Probabilistic Linkage | Record Linkage |
| High-dimensional data | CVPLA Linkage | NNDR metric |
| Partial sensitive attributes | Attribute Inference | None (use together) |
| Need to compare methods | Attack Metrics | All metrics |

## Code Examples By Topic

### Basic Usage
```python
from pamola_core.attacks import LinkageAttack, AttackMetrics
import pandas as pd

# Load data
original = pd.read_csv('original.csv')
anonymized = pd.read_csv('anonymized.csv')

# Run a linkage attack
linkage = LinkageAttack()
matches = linkage.record_linkage_attack(original, anonymized, ['age', 'city'])

# Evaluate predictions against ground truth (y_true, y_pred are 0/1 arrays you supply)
metrics = AttackMetrics()
results = metrics.attack_metrics(y_true, y_pred)
print(f"Attack Accuracy: {results['Attack Accuracy']}")
```

### Threshold Optimization
See [Attack Metrics](./attack_metrics.md#threshold-optimization) for example showing:
- Try multiple threshold values
- Compare accuracy across thresholds
- Find optimal for your privacy goals

## Import Reference

```python
# Base classes
from pamola_core.attacks import AttackInitialization, BaseAttack
from pamola_core.attacks.preprocess_data import PreprocessData

# Attacks
from pamola_core.attacks import LinkageAttack
from pamola_core.attacks import AttributeInference, AttributeInferenceAttack

# Evaluation
from pamola_core.attacks import AttackMetrics

# Distance-based privacy metrics live in the metrics package
from pamola_core.metrics.privacy.distance import DistanceToClosestRecord
from pamola_core.metrics.privacy.neighbor import NearestNeighborDistanceRatio
```

## Common Workflows

### Privacy Risk Assessment (Complete)
1. **Baseline Metrics** → [DCR](../metrics/privacy/distance.md)
2. **Re-identification Test** → [Linkage Attack](./linkage_attack.md)
3. **Attribute Risk** → [Attribute Inference](./attribute_inference.md)
4. **Comprehensive Evaluation** → [Attack Metrics](./attack_metrics.md)

### Anonymization Validation
1. Apply anonymization technique
2. Run baseline attacks (Linkage) and the DCR metric
3. Check metrics improve
4. Iterate until risk acceptable

## Troubleshooting Quick Links

- **"No matches found"** → [Linkage Attack Troubleshooting](./linkage_attack.md#troubleshooting)
- **"Threshold issues"** → [Attack Metrics Troubleshooting](./attack_metrics.md#troubleshooting)
- **"Performance too slow"** → [Linkage Attack Performance](./linkage_attack.md#troubleshooting)

## Related Documentation

- **[Profiling Module](../profiling/)** — Analyze data before anonymization
- **[Metrics Module](../metrics/)** — Privacy metrics (DCR, NNDR, disclosure risk)
- **[Anonymization Module](../anonymization/)** — Apply protective transformations
- **[Privacy Models](../privacy_models/)** — Theoretical privacy foundations

## File Summary

| File | Purpose | Key Classes |
|------|---------|-------------|
| attacks_overview.md | Module entry point | All classes overview |
| base_attack.md | Abstract interfaces | AttackInitialization, PreprocessData |
| linkage_attack.md | Re-identification | LinkageAttack (3 methods) |
| attribute_inference.md | Attribute inference | AttributeInference |
| attack_metrics.md | Evaluation | AttackMetrics (3 methods) |
