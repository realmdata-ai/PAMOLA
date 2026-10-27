# Group Analysis Module Documentation

**Module:** `pamola_core.profiling.analyzers.group`
**Public class:** `GroupAnalyzerOperation` (exported from `pamola_core`)

## Overview

The `group.py` module analyzes groups of records that share the same identifier (for example
several rows per `resume_id`). For each group it computes per-field and weighted variance and
duplication metrics, and decides whether the group is a candidate for aggregation (collapsing)
during anonymization.

## Architecture

The module separates analytical logic from the operation wrapper:

1. **GroupAnalyzer**: Computes group, field and weighted variance metrics (`analyze()`), using
   helper functions from `pamola_core.profiling.commons.group_utils` (`analyze_group`,
   `calculate_field_metrics`, `calculate_weighted_variance`, ...).
2. **GroupAnalyzerOperation**: A `FieldOperation` that loads the data, runs the analysis,
   writes metrics and optional visualizations, and returns an `OperationResult`.

```
┌─────────────────┐      ┌─────────────────────────┐      ┌────────────────────┐
│   DataSource    │──────▶  GroupAnalyzerOperation │─────▶   OperationResult   │
└─────────────────┘      └────────────┬────────────┘      └────────────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │      GroupAnalyzer      │─────▶ group_utils.py helpers
                         └─────────────────────────┘
```

## Key Capabilities

1. **Weighted Variance Analysis**: Variance of each configured field within a group, combined
   into a weighted score using the weights in `fields_config`
2. **Duplication Analysis**: Long text fields (longer than `text_length_threshold`) are compared
   by hash - MD5 or MinHash (`hash_algorithm`)
3. **Aggregation Decision**: A group is marked for aggregation when its weighted variance is
   below `variance_threshold` (or below `large_group_variance_threshold` for groups larger than
   `large_group_threshold`)
4. **Visualization**: Variance distribution histogram and field-variance heatmap (when
   `generate_visualization=True`)
5. **Caching**: Results can be cached and reused (`use_cache`)

## Usage Example

```python
from pathlib import Path
from unittest.mock import MagicMock

from pamola_core import GroupAnalyzerOperation, DataSource

# DataFrame with a group identifier field
data_source = DataSource.from_dataframe(df, "main")
task_dir = Path("output/analysis")

# Weights (importance) of each field inside a group
fields_config = {
    "post": 3,
    "education_level": 2,
    "area_name": 2,
    "salary": 3,
}

operation = GroupAnalyzerOperation(
    field_name="resume_id",
    fields_config=fields_config,
    variance_threshold=0.2,
    hash_algorithm="md5",
    generate_visualization=True,
)

result = operation.execute(
    data_source=data_source,
    task_dir=task_dir,
    reporter=MagicMock(),  # or your reporter object
)

if result.status.name == "SUCCESS":
    print(f"Total groups: {result.metrics['total_groups']}")
    print(f"Groups to aggregate: {result.metrics['groups_to_aggregate']}")
    print(f"Average variance: {result.metrics['avg_variance']}")

    for artifact in result.artifacts:
        print(f"Artifact: {artifact.artifact_type}, Path: {artifact.path}")
```

## Parameters

### GroupAnalyzerOperation Constructor

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `field_name` | str | Yes | - | Field to group by (e.g., `'resume_id'`) |
| `fields_config` | Dict[str, int] | Yes | - | Fields to analyze inside each group, mapped to their weights |
| `text_length_threshold` | int | No | 100 | Minimum length for text values to be compared by hash |
| `variance_threshold` | float | No | 0.2 | Weighted variance below which a group is an aggregation candidate |
| `large_group_threshold` | int | No | 100 | Minimum size for a group to count as "large" |
| `large_group_variance_threshold` | float | No | 0.05 | Variance threshold applied to large groups |
| `hash_algorithm` | str | No | `"md5"` | Text comparison algorithm: `"md5"` or `"minhash"` |
| `minhash_similarity_threshold` | float | No | 0.7 | Similarity threshold for MinHash signatures |
| `**kwargs` | | No | | Common `BaseOperation` parameters (e.g. `description`, `use_cache`, `generate_visualization`, `visualization_backend`, `use_encryption`, `encryption_key`, `engine`, `chunk_size`) |

### execute()

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data_source` | DataSource | Yes | - | Source of data for the operation |
| `task_dir` | Path | Yes | - | Directory for saving artifacts |
| `reporter` | Any | Yes | - | Reporter object for tracking artifacts |
| `progress_tracker` | HierarchicalProgressTracker | No | None | Progress tracking object |

## Return Value

`execute()` returns an `OperationResult`:

| Property | Type | Description |
|----------|------|-------------|
| `status` | OperationStatus | SUCCESS or ERROR |
| `artifacts` | List[OperationArtifact] | Metrics JSON and optional PNG visualizations |
| `metrics` | Dict[str, Any] | Scalar metrics (see below) |
| `error_message` | str | Error details if the operation failed |
| `execution_time` | float | Time taken in seconds |

## Metrics

Scalar values added to `result.metrics`:

| Metric | Description |
|--------|-------------|
| `field` | The grouping field |
| `total_groups` | Number of groups |
| `total_records` | Number of records analyzed |
| `avg_variance` | Mean weighted variance across groups |
| `max_variance` | Maximum weighted variance |
| `groups_to_aggregate` | Number of groups marked for aggregation |

The metrics JSON (`GroupAnalyzerOperation_{field_name}_metrics.json`) additionally contains
`field_metrics` (per-field statistics), `group_metrics` (per-group details),
`threshold_metrics` (variance distribution), `algorithm_info` (thresholds and hash algorithm)
and `fields_analyzed`.

## Generated Artifacts

1. **Metrics JSON**: `GroupAnalyzerOperation_{field_name}_metrics.json`
2. **Visualizations** (only when `generate_visualization=True`):
   - `GroupAnalyzerOperation_{field_name}_variance_dist_{timestamp}.png` - distribution of weighted variance across groups
   - `GroupAnalyzerOperation_{field_name}_field_heatmap_{timestamp}.png` - variance of each field

Profiling artifacts can contain source values (`ARTIFACTS_CONTAIN_SOURCE_VALUES = True`); treat
them as diagnostic output, not as releasable data.

## Integration Points

1. **Data Source System**: Gets data through the `DataSource` abstraction
2. **Operation Framework**: Follows the standard `BaseOperation` lifecycle
3. **Data Writer**: Writes metrics through `DataWriter`
4. **Visualization System**: Uses `pamola_core.utils.visualization` (`create_histogram`, `create_heatmap`)
5. **Reporting System**: Reports the operation and its artifacts to the reporter object
