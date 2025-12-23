# Performance Tests

This directory contains performance tests for validating the scalability and efficiency of utility functions under load.

## Directory Structure

```
performance/
├── README.md (this file)
└── database_functions/
    └── schema_inspection/
        └── test_migrate_id_type_performance.py
```

## Running Performance Tests

Performance tests are marked with `@pytest.mark.performance` and are excluded from regular unit test runs.

### Run All Performance Tests

```bash
pytest pytest/performance/ -m performance -v
```

### Run Performance Tests (Excluding Slow Tests)

Some tests are marked with both `@pytest.mark.performance` and `@pytest.mark.slow` (e.g., 1M row stress tests).

```bash
pytest pytest/performance/ -m "performance and not slow" -v
```

### Run Only Slow Stress Tests

```bash
pytest pytest/performance/ -m "performance and slow" -v
```

### Run Specific Performance Test File

```bash
pytest pytest/performance/database_functions/schema_inspection/test_migrate_id_type_performance.py -v
```

## Test Marks

- **`@pytest.mark.performance`**: Marks test as a performance test
- **`@pytest.mark.slow`**: Marks test as slow-running (use for stress tests)

## Current Performance Test Coverage

### `test_migrate_id_type_performance.py`

Tests the `migrate_id_type` function's performance characteristics:

1. **test_migrate_id_type_performance_10k_rows**: 10K rows with 2 FK tables (35K total FK references)
2. **test_migrate_id_type_performance_100k_rows**: 100K rows without FK relationships
3. **test_migrate_id_type_performance_complex_fk_relationships**: 5K rows with 5 FK tables (25K references)
4. **test_migrate_id_type_performance_small_batch_size**: 10K rows with batch_size=100
5. **test_migrate_id_type_performance_uuid_generation**: 10K rows with UUID generation overhead
6. **test_migrate_id_type_performance_memory_efficiency**: 50K rows with full ID mapping
7. **test_migrate_id_type_performance_stress_test_1m_rows**: 1M rows stress test (marked as `slow`)

## Performance Benchmarks

All tests include performance assertions to ensure the function maintains acceptable performance:

- **10K rows**: < 5 seconds
- **50K rows**: < 15 seconds
- **100K rows**: < 30 seconds
- **1M rows**: < 300 seconds (5 minutes)

Tests print execution time and throughput for performance tracking.

## Best Practices

1. **Separate from Unit Tests**: Performance tests are in a separate directory to avoid slowing down development workflows
2. **Pytest Marks**: Use marks to selectively run or skip tests
3. **CI/CD Integration**: Run performance tests in CI/CD pipelines or nightly builds
4. **Performance Assertions**: Include time-based assertions to catch performance regressions
5. **Realistic Scenarios**: Test with realistic data volumes and complexity

## Adding New Performance Tests

When adding new performance tests:

1. Place them in the appropriate subdirectory under `pytest/performance/`
2. Mark tests with `@pytest.mark.performance`
3. Mark extremely slow tests with `@pytest.mark.slow` as well
4. Include performance assertions with reasonable time limits
5. Print execution time and throughput for tracking
6. Add complete type annotations for mypy compliance
7. Follow the naming convention: `test_<function_name>_performance_<scenario>`
8. Update this README with the new test coverage
