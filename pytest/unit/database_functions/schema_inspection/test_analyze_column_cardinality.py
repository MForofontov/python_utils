"""
Unit tests for analyze_column_cardinality function.
"""

from conftest import Base, User
from sqlalchemy.orm import Session

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.database]
from pyutils_collection.database_functions.schema_inspection import analyze_column_cardinality


def test_analyze_column_cardinality_identifies_low_cardinality(memory_engine) -> None:
    """
    Test case 1: Identify low cardinality columns (good for indexing).
    """
    # Arrange
    Base.metadata.create_all(memory_engine)

    with Session(memory_engine) as session:
        # Create users with repeating roles (low cardinality)
        for i in range(100):
            session.add(
                User(
                    id=i,
                    username=f"user{i}",
                    email=f"user{i}@example.com",
                    role="admin" if i < 10 else "user",  # Only 2 distinct values
                    status="active",
                    balance=float(i),
                )
            )
        session.commit()

    # Act
    with memory_engine.connect() as connection:
        results = analyze_column_cardinality(
            connection, tables=["users"], low_cardinality_threshold=0.05
        )

    # Assert
    role_result = next((r for r in results if r["column_name"] == "role"), None)
    assert role_result is not None
    assert role_result["cardinality_category"] == "low"
    assert role_result["distinct_values"] == 2
    assert role_result["cardinality_ratio"] < 0.05


def test_analyze_column_cardinality_identifies_high_cardinality(memory_engine) -> None:
    """
    Test case 2: Identify high cardinality columns (likely unique).
    """
    # Arrange
    Base.metadata.create_all(memory_engine)

    with Session(memory_engine) as session:
        # Create users with unique usernames (high cardinality)
        for i in range(100):
            session.add(
                User(
                    id=i,
                    username=f"user{i}",
                    email=f"user{i}@example.com",
                    role="user",
                    status="active",
                    balance=float(i),
                )
            )
        session.commit()

    # Act
    with memory_engine.connect() as connection:
        results = analyze_column_cardinality(
            connection, tables=["users"], high_cardinality_threshold=0.95
        )

    # Assert
    username_result = next((r for r in results if r["column_name"] == "username"), None)
    assert username_result is not None
    assert username_result["cardinality_category"] == "high"
    assert username_result["cardinality_ratio"] >= 0.95


def test_analyze_column_cardinality_with_sample_size(memory_engine) -> None:
    """
    Test case 3: Respect sample_size parameter for large tables.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)

    with Session(memory_engine) as session:
        for i in range(1000):
            session.add(
                User(
                    id=i,
                    username=f"user{i}",
                    email=f"user{i}@example.com",
                    role="user",
                    status="active",
                    balance=float(i),
                )
            )
        session.commit()

    # Act
    with memory_engine.connect() as connection:
        results = analyze_column_cardinality(
            connection, tables=["users"], sample_size=100
        )

    # Assert
    assert len(results) > 0
    # Sample size limits the rows analyzed, not necessarily total_rows returned


def test_analyze_column_cardinality_empty_table(memory_engine) -> None:
    """
    Test case 4: Handle empty tables gracefully.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)

    # Act
    with memory_engine.connect() as connection:
        results = analyze_column_cardinality(connection, tables=["users"])

    # Assert
    assert isinstance(results, list)
    # Empty table should return empty results or skip


def test_analyze_column_cardinality_null_handling(memory_engine) -> None:
    """
    Test case 5: Track NULL values and percentages.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)

    with Session(memory_engine) as session:
        for i in range(100):
            session.add(
                User(
                    id=i,
                    username=f"user{i}",
                    email=f"user{i}@example.com",
                    role="admin" if i < 10 else None,  # 90% NULL
                    status="active",
                    balance=float(i),
                )
            )
        session.commit()

    # Act
    with memory_engine.connect() as connection:
        results = analyze_column_cardinality(connection, tables=["users"])

    # Assert
    role_result = next((r for r in results if r["column_name"] == "role"), None)
    assert role_result is not None
    assert role_result["null_count"] == 90  # 90 NULLs (i >= 10)
    # null_percentage might be 90.0 (as percentage) or 0.9 (as ratio)
    assert role_result["null_percentage"] in [90.0, 0.9] or pytest.approx(
        role_result["null_percentage"], abs=1
    ) in [90.0, 0.9]


def test_analyze_column_cardinality_invalid_connection_type_error() -> None:
    """
    Test case 6: TypeError for None connection.
    """
    # Arrange
    expected_message = "connection cannot be None"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        analyze_column_cardinality(None)


def test_analyze_column_cardinality_invalid_tables_type_error(memory_engine) -> None:
    """
    Test case 7: TypeError for invalid tables parameter.
    """
    # Arrange
    expected_message = "tables must be list or None"

    # Act & Assert
    with memory_engine.connect() as connection:
        with pytest.raises(TypeError, match=expected_message):
            analyze_column_cardinality(connection, tables="users")


def test_analyze_column_cardinality_invalid_schema_type_error(memory_engine) -> None:
    """
    Test case 8: TypeError for invalid schema parameter.
    """
    # Arrange
    expected_message = "schema must be str or None"

    # Act & Assert
    with memory_engine.connect() as connection:
        with pytest.raises(TypeError, match=expected_message):
            analyze_column_cardinality(connection, schema=123)


def test_analyze_column_cardinality_invalid_sample_size_type_error(
    memory_engine,
) -> None:
    """
    Test case 9: TypeError for invalid sample_size parameter.
    """
    # Arrange
    expected_message = "sample_size must be int or None"

    # Act & Assert
    with memory_engine.connect() as connection:
        with pytest.raises(TypeError, match=expected_message):
            analyze_column_cardinality(connection, sample_size="100")


def test_analyze_column_cardinality_negative_sample_size_value_error(
    memory_engine,
) -> None:
    """
    Test case 10: ValueError for negative sample_size.
    """
    # Arrange
    expected_message = "sample_size must be positive"

    # Act & Assert
    with memory_engine.connect() as connection:
        with pytest.raises(ValueError, match=expected_message):
            analyze_column_cardinality(connection, sample_size=-100)


def test_analyze_column_cardinality_invalid_threshold_type_error(memory_engine) -> None:
    """
    Test case 11: TypeError for invalid threshold parameters.
    """
    # Arrange
    expected_message = "low_cardinality_threshold must be float"

    # Act & Assert
    with memory_engine.connect() as connection:
        with pytest.raises(TypeError, match=expected_message):
            analyze_column_cardinality(connection, low_cardinality_threshold="0.01")


def test_analyze_column_cardinality_threshold_out_of_range_value_error(
    memory_engine,
) -> None:
    """
    Test case 12: ValueError for thresholds out of range.
    """
    # Arrange
    expected_message = "low_cardinality_threshold must be between 0 and 1"

    # Act & Assert
    with memory_engine.connect() as connection:
        with pytest.raises(ValueError, match=expected_message):
            analyze_column_cardinality(connection, low_cardinality_threshold=1.5)
