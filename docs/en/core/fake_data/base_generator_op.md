# GeneratorOperation Documentation

**Module:** `pamola_core.fake_data.base_generator_op`
**Last Updated:** 2026-03-23

## Overview

The `GeneratorOperation` class serves as the base class for all generator-based synthetic data operations in PAMOLA CORE. It provides a consistent interface for operations that use generator-based approaches (e.g., fake names, fake emails, synthetic IDs), handling consistency mechanisms, mapping stores, metrics collection, and metadata propagation. This class standardizes the lifecycle, execution model, and artifact management across all fake-data generators.

## Key Features

- Standardized operation lifecycle with validation, execution, and result handling
- Support for REPLACE and ENRICH modes for synthetic value injection
- Configurable null handling strategies and conditional processing
- Chunked processing for memory efficiency with Dask and joblib support
- Comprehensive metrics collection and visualization generation
- Deterministic mapping store support for repeatable generation
- Result caching and artifact restoration for faster re-runs
- Consistency mechanism support (PRGN, mapping, etc.)
- Integration with PAMOLA operation framework and reporter interfaces

## Architecture

### Module Position

The `GeneratorOperation` is part of the `pamola_core.fake_data` package and serves as the parent class for all concrete generator operations:

```
pamola_core/fake_data/
├── base_generator_op.py        # GeneratorOperation implementation
├── operations/
│   ├── name_op.py              # FakeNameOperation (subclass)
│   ├── email_op.py             # FakeEmailOperation (subclass)
│   ├── phone_op.py             # FakePhoneOperation (subclass)
│   └── organization_op.py       # FakeOrganizationOperation (subclass)
├── generators/
│   ├── name.py                 # NameGenerator
│   ├── email.py                # EmailGenerator
│   ├── phone.py                # PhoneGenerator
│   └── organization.py         # OrganizationGenerator
└── commons/
    ├── base.py                 # BaseGenerator, BaseOperation interfaces
    └── mapping_store.py        # MappingStore for consistency
```

### Design Principles

- **Type Safety**: Explicit validation for inputs and parameters
- **Extensibility**: Subclasses override batch/value processing and cache parameters
- **Compatibility**: Works seamlessly with PAMOLA operation framework and reporter interfaces
- **Performance**: Efficient batching, optional parallelism, and cached validators
- **Robustness**: Best-effort artifact generation and graceful degradation

## Dependencies

| Dependency | Purpose |
|-----------|---------|
| `pamola_core.fake_data.commons.base` | BaseGenerator interface |
| `pamola_core.fake_data.commons.mapping_store` | Deterministic mapping storage |
| `pamola_core.fake_data.commons.metrics` | Metrics collection and reporting |
| `pamola_core.fake_data.commons.processing_utils` | Dask/joblib processing utilities |
| `pamola_core.utils.ops.op_base` | FieldOperation parent class |
| `pamola_core.utils.ops.op_result` | OperationResult and status |
| `pandas, numpy, dask, joblib` | Data processing and parallelization |

## Core Classes and Methods

### GeneratorOperation Constructor

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `field_name` | str | Target field for generation | Required |
| `generator` | BaseGenerator | Generator instance used to create synthetic data | Required |
| `generator_params` | Dict | Additional generator configuration parameters | {} |
| `consistency_mechanism` | str | Consistency preservation mechanism (`prgn` or `mapping`) | "prgn" |
| `id_field` | str | Unique identifier field for mapping consistency | None |
| `mapping_store_path` | str | Path to persistent mapping store | None |
| `save_mapping` | bool | Whether to persist mapping results after processing | False |
| `include_raw_samples_in_metrics` | bool | Include raw original/synthetic samples in metrics (off by default for privacy) | False |
| `**kwargs` | dict | Additional arguments for FieldOperation/BaseOperation | |

### Key Methods

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `execute` | Execute the generator operation with timing and error handling | `data_source`, `task_dir`, `reporter`, `**kwargs` | OperationResult |
| `process_batch` | Process a batch of data rows | `batch: pd.DataFrame` | pd.DataFrame |
| `_initialize_mapping_store` | Initialize mapping store from a path | `path` | None |
| `_collect_metrics` | Collect metrics for the operation | `df: pd.DataFrame` | Dict |
| `_save_metrics` | Save metrics through the DataWriter and register the artifact | `metrics`, `writer`, `result`, `reporter`, `progress_tracker` | bool |

## Usage Examples

In most cases use the public subclasses (`FakeNameOperation`, `FakeEmailOperation`,
`FakePhoneOperation`, `FakeOrganizationOperation`). `GeneratorOperation` can be used directly
with any `BaseGenerator` instance.

### Basic Usage: Name Generation Operation

```python
from pathlib import Path
from pamola_core.fake_data.generators.name import NameGenerator
from pamola_core.fake_data.base_generator_op import GeneratorOperation
from pamola_core.utils.ops.op_data_source import DataSource
from pamola_core.utils.tasks.task_reporting import TaskReporter

# Create a name generator
name_gen = NameGenerator(config={
    "language": "en",
    "gender": None,
    "format": "FL"
})

# Create a generator operation
name_op = GeneratorOperation(
    field_name="person_name",
    generator=name_gen,
    generator_params={"language": "en", "format": "FL"},
    consistency_mechanism="prgn"
)

# Execute the operation
task_dir = Path("./task_directory")
reporter = TaskReporter(
    task_id="fake_names",
    task_type="fake_data",
    description="Generate synthetic names",
    report_path=task_dir / "report.json",
)
result = name_op.execute(
    data_source=DataSource.from_file_path("path/to/data.csv"),
    task_dir=task_dir,
    reporter=reporter
)

if result.status.name == "SUCCESS":
    print(f"Processing completed. Metrics: {result.metrics}")
else:
    print(f"Error: {result.error_message}")
```

### Mapping-Based Consistency

```python
import pandas as pd
from pathlib import Path
from unittest.mock import MagicMock
from pamola_core.fake_data.generators.email import EmailGenerator
from pamola_core.fake_data.base_generator_op import GeneratorOperation
from pamola_core.utils.ops.op_data_source import DataSource

email_gen = EmailGenerator(config={
    "domains": ["newemail.com", "corporate.org"],
    "format": "name_surname",
    "preserve_domain_ratio": 0.3
})

# The same original value always maps to the same synthetic value.
# save_mapping=True writes the mapping (it holds original values) only encrypted,
# so it requires use_encryption=True and the task encryption key.
email_op = GeneratorOperation(
    field_name="email",
    generator=email_gen,
    consistency_mechanism="mapping",
    mapping_store_path="./mappings/email.json",
    save_mapping=True,
    use_encryption=True,
    encryption_key="<task key>"
)

df = pd.DataFrame({
    'email': ['john.doe@example.com', 'jane.smith@company.org'],
    'first_name': ['John', 'Jane']
})

result = email_op.execute(
    data_source=DataSource.from_dataframe(df),
    task_dir=Path("./output"),
    reporter=MagicMock()  # or a TaskReporter
)
```

### Large Datasets: Dask and Chunked Processing

Processing options are the common `BaseOperation` constructor parameters:

```python
from pamola_core.fake_data.generators.phone import PhoneGenerator
from pamola_core.fake_data.base_generator_op import GeneratorOperation

phone_gen = PhoneGenerator(config={
    "country_codes": ["us", "ca", "uk"],
    "region": "us"
})

# Dask-based processing
phone_op = GeneratorOperation(
    field_name="phone_number",
    generator=phone_gen,
    use_dask=True,
    npartitions=4,
    dask_partition_size="100MB"
)

# Chunked / parallel processing
phone_op_chunked = GeneratorOperation(
    field_name="phone_number",
    generator=phone_gen,
    chunk_size=5000,
    parallel_processes=4
)
```

## Return Values

The `execute` method returns an `OperationResult` object containing:

- **status** - `OperationStatus` (`SUCCESS`, `ERROR`, ...)
- **metrics** - Dictionary of operation metrics
- **artifacts** - List of `OperationArtifact` objects (output data, metrics JSON, visualizations, mapping files)
- **error_message** - Error description (if any)
- **execution_time** - Time taken for execution in seconds

The processed data is written to the task's `output/` directory (when `save_output=True`).

## Processing Options

| Option | Description | Configuration |
|--------|-------------|---------------|
| Chunked | Sequential chunk-based processing | `chunk_size` |
| Parallel | Parallel processing with joblib | `parallel_processes`, `chunk_size` |
| Dask | Distributed processing using Dask | `use_dask`, `npartitions`, `dask_partition_size` |

## Consistency Mechanisms

| Mechanism | Description | Use Case |
|-----------|-------------|----------|
| `prgn` | Pseudo-Random Number Generator for deterministic generation | Default, consistent across runs with the same key/salt |
| `mapping` | Store-based mapping for exact value reuse | When same original values must map to same synthetic values |

## Limitations

1. **Memory Usage**: Large datasets with detailed metrics enabled may consume significant memory
2. **Generator Dependencies**: Quality depends on the underlying generator implementation
3. **Mapping Storage**: Mapping store can grow large with extensive datasets
4. **Retry Overhead**: Retry mechanisms improve robustness but may increase processing time
5. **Performance Trade-offs**: More detailed metrics collection impacts performance
6. **Visualization Limits**: Generated visualizations are limited to supported chart types
7. **Error Recovery**: Some error conditions may require manual intervention

## Best Practices

1. **Choose Appropriate Processing Options**: Use `chunk_size` for small/medium data, `parallel_processes` for multi-core systems, `use_dask` for distributed processing
2. **Configure Chunk Sizes**: Adjust `chunk_size` based on available memory and data characteristics
3. **Use Mapping Stores for Consistency**: Save and reuse mappings when reproducibility is important
4. **Monitor Progress**: Use progress trackers for long-running operations
5. **Handle Null Values Appropriately**: Configure null strategy based on data semantics
6. **Test with Sample Data**: Verify configuration with small dataset before processing large volumes
7. **Archive Mappings**: Save mapping store files for future reference and auditing

## Related Components

- **BaseGenerator** - Abstract interface for all data generators
- **FieldOperation** - Parent class providing field-specific functionality
- **MappingStore** - Persistent storage for value mappings
- **ProcessingUtils** - Dask/joblib integration utilities
- **OperationResult** - Standardized result container

## Summary Analysis

The `GeneratorOperation` class provides a robust, extensible framework for implementing synthetic data generation operations. By inheriting from `FieldOperation`, it gains standardized field-specific processing capabilities while adding generator-specific functionality like mapping store support, metrics collection, and multiple processing strategies. The class is designed for flexibility, allowing subclasses to customize batch processing, value generation, and cache parameters while maintaining consistency with the PAMOLA operation framework. Its integration with multiple processing backends (chunk-based, joblib, Dask) makes it suitable for datasets ranging from small to distributed workloads.
