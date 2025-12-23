"""
Unit tests for analyze_column_cardinality function.

Tests cover cardinality analysis, threshold validation, and optimization recommendations.
"""

import pytest
from sqlalchemy import (
    Column,
    Integer,
    String,
    MetaData,
    Table,
    create_engine,
)

from database_functions.schema_inspection.analyze_column_cardinality import (
    analyze_column_cardinality,
)


@pytest.fixture
def empty_engine():
    """Create empty test database engine without data."""
    engine = create_engine("sqlite:///:memory:")
    yield engine
    engine.dispose()


@pytest.fixture
def test_engine():
    """Create test database engine with sample data."""
    engine = create_engine("sqlite:///:memory:")
    metadata = MetaData()
    
    # Table with mixed cardinality columns
    users = Table(
        "users",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("status", String(20)),  # Low cardinality
        Column("email", String(100)),  # High cardinality
        Column("department", String(50)),  # Medium cardinality
    )
    
    metadata.create_all(engine)
    
    # Insert test data
    with engine.begin() as conn:
        # 100 users with varying cardinality
        data = []
        for i in range(100):
            data.append({
                "id": i + 1,
                "status": ["active", "inactive", "pending"][i % 3],  # 3 distinct
                "email": f"user{i}@example.com",  # 100 distinct
                "department": f"dept_{i % 10}",  # 10 distinct
            })
        conn.execute(users.insert(), data)
    
    yield engine
    engine.dispose()


def test_analyze_column_cardinality_basic_analysis(test_engine) -> None:
    """
    Test basic cardinality analysis on all columns.
    """
    # Arrange & Act
    with test_engine.connect() as conn:
        results = analyze_column_cardinality(
            conn,
            low_cardinality_threshold=0.05,
            high_cardinality_threshold=0.90,
        )
    
    # Assert
    assert len(results) > 0
    
    # Check structure of results
    for result in results:
        assert "table_name" in result
        assert "column_name" in result
        assert "total_rows" in result
        assert "distinct_values" in result
        assert "cardinality_ratio" in result
        assert "cardinality_category" in result


def test_analyze_column_cardinality_low_cardinality_detection(test_engine) -> None:
    """
    Test detection of low cardinality columns.
    """
    # Arrange & Act
    with test_engine.connect() as conn:
        results = analyze_column_cardinality(
            conn,
            low_cardinality_threshold=0.05,  # 5%
            high_cardinality_threshold=0.90,
        )
    
    # Assert - status column should be low cardinality (3/100 = 3%)
    status_result = next((r for r in results if r["column_name"] == "status"), None)
    assert status_result is not None
    assert status_result["cardinality_category"] == "low"
    assert status_result["distinct_values"] == 3
    assert status_result["cardinality_ratio"] < 0.05


def test_analyze_column_cardinality_high_cardinality_detection(test_engine) -> None:
    """
    Test detection of high cardinality columns.
    """
    # Arrange & Act
    with test_engine.connect() as conn:
        results = analyze_column_cardinality(
            conn,
            low_cardinality_threshold=0.05,
            high_cardinality_threshold=0.90,  # 90%
        )
    
    # Assert - email column should be high cardinality (100/100 = 100%)
    email_result = next((r for r in results if r["column_name"] == "email"), None)
    assert email_result is not None
    assert email_result["cardinality_category"] == "high"
    assert email_result["distinct_values"] == 100
    assert email_result["cardinality_ratio"] >= 0.90


def test_analyze_column_cardinality_medium_cardinality_detection(test_engine) -> None:
    """
    Test detection of medium cardinality columns.
    """
    # Arrange & Act
    with test_engine.connect() as conn:
        results = analyze_column_cardinality(
            conn,
            low_cardinality_threshold=0.05,
            high_cardinality_threshold=0.90,
        )
    
    # Assert - department column should be medium cardinality (10/100 = 10%)
    dept_result = next((r for r in results if r["column_name"] == "department"), None)
    assert dept_result is not None
    assert dept_result["cardinality_category"] == "medium"
    assert dept_result["distinct_values"] == 10
    assert 0.05 <= dept_result["cardinality_ratio"] < 0.90


def test_analyze_column_cardinality_specific_tables(test_engine) -> None:
    """
    Test analysis limited to specific tables.
    """
    # Arrange & Act
    with test_engine.connect() as conn:
        results = analyze_column_cardinality(
            conn,
            tables=["users"],
        )
    
    # Assert
    assert all(r["table_name"] == "users" for r in results)


def test_analyze_column_cardinality_with_sample_size(test_engine) -> None:
    """
    Test analysis with sample size limitation.
    """
    # Arrange & Act
    with test_engine.connect() as conn:
        results = analyze_column_cardinality(
            conn,
            sample_size=50,
        )
    
    # Assert - should still return results
    assert len(results) > 0
    # Note: With sampling, total_rows may differ


def test_analyze_column_cardinality_invalid_connection() -> None:
    """
    Test TypeError when connection is None.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="connection cannot be None"):
        analyze_column_cardinality(None)


def test_analyze_column_cardinality_invalid_tables_type(empty_engine) -> None:
    """
    Test TypeError when tables is not a list.
    """
    # Act & Assert
    with empty_engine.connect() as conn:
        with pytest.raises(TypeError, match="tables must be list or None"):
            analyze_column_cardinality(
                conn,
                tables="not_a_list",  # type: ignore
            )


def test_analyze_column_cardinality_invalid_schema_type(empty_engine) -> None:
    """
    Test TypeError when schema is not a string.
    """
    # Act & Assert
    with empty_engine.connect() as conn:
        with pytest.raises(TypeError, match="schema must be str or None"):
            analyze_column_cardinality(
                conn,
                schema=123,  # type: ignore
            )


def test_analyze_column_cardinality_invalid_sample_size_type(empty_engine) -> None:
    """
    Test TypeError when sample_size is not an integer.
    """
    # Act & Assert
    with empty_engine.connect() as conn:
        with pytest.raises(TypeError, match="sample_size must be int or None"):
            analyze_column_cardinality(
                conn,
                sample_size="invalid",  # type: ignore
            )


def test_analyze_column_cardinality_invalid_sample_size_value(empty_engine) -> None:
    """
    Test ValueError when sample_size is zero or negative.
    """
    # Act & Assert - Zero
    with empty_engine.connect() as conn:
        with pytest.raises(ValueError, match="sample_size must be positive"):
            analyze_column_cardinality(conn, sample_size=0)
    
    # Act & Assert - Negative
    with empty_engine.connect() as conn:
        with pytest.raises(ValueError, match="sample_size must be positive"):
            analyze_column_cardinality(conn, sample_size=-10)


def test_analyze_column_cardinality_invalid_low_threshold_type(empty_engine) -> None:
    """
    Test TypeError when low_cardinality_threshold is not numeric.
    """
    # Act & Assert
    with empty_engine.connect() as conn:
        with pytest.raises(TypeError, match="low_cardinality_threshold must be float"):
            analyze_column_cardinality(
                conn,
                low_cardinality_threshold="invalid",  # type: ignore
            )


def test_analyze_column_cardinality_invalid_low_threshold_range(empty_engine) -> None:
    """
    Test ValueError when low_cardinality_threshold is out of range.
    """
    # Act & Assert - Below 0
    with empty_engine.connect() as conn:
        with pytest.raises(ValueError, match="must be between 0 and 1"):
            analyze_column_cardinality(conn, low_cardinality_threshold=-0.1)
    
    # Act & Assert - Above 1
    with empty_engine.connect() as conn:
        with pytest.raises(ValueError, match="must be between 0 and 1"):
            analyze_column_cardinality(conn, low_cardinality_threshold=1.5)


def test_analyze_column_cardinality_invalid_high_threshold_range(empty_engine) -> None:
    """
    Test ValueError when high_cardinality_threshold is out of range.
    """
    # Act & Assert - Below 0
    with empty_engine.connect() as conn:
        with pytest.raises(ValueError, match="must be between 0 and 1"):
            analyze_column_cardinality(conn, high_cardinality_threshold=-0.1)
    
    # Act & Assert - Above 1
    with empty_engine.connect() as conn:
        with pytest.raises(ValueError, match="must be between 0 and 1"):
            analyze_column_cardinality(conn, high_cardinality_threshold=1.5)


def test_analyze_column_cardinality_threshold_order(empty_engine) -> None:
    """
    Test ValueError when low threshold >= high threshold.
    """
    # Act & Assert
    with empty_engine.connect() as conn:
        with pytest.raises(ValueError, match="low_cardinality_threshold must be less than"):
            analyze_column_cardinality(
                conn,
                low_cardinality_threshold=0.8,
                high_cardinality_threshold=0.5,
            )


def test_analyze_column_cardinality_empty_table(empty_engine) -> None:
    """
    Test handling of empty tables.
    """
    # Arrange
    metadata = MetaData()
    
    empty_table = Table(
        "empty",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(50)),
    )
    
    metadata.create_all(empty_engine)
    
    # Act
    with empty_engine.connect() as conn:
        results = analyze_column_cardinality(conn)
    
    # Assert - empty table should be skipped
    empty_results = [r for r in results if r["table_name"] == "empty"]
    assert len(empty_results) == 0


def test_analyze_column_cardinality_primary_key_skipped(test_engine) -> None:
    """
    Test that primary key columns are skipped from analysis.
    """
    # Arrange & Act
    with test_engine.connect() as conn:
        results = analyze_column_cardinality(conn)
    
    # Assert - id column (primary key) should not be in results
    id_results = [r for r in results if r["column_name"] == "id"]
    assert len(id_results) == 0
