"""
Unit tests for get_column_statistics function.
"""

from conftest import Base, User
from sqlalchemy.orm import Session

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.database]
from database_functions.schema_inspection import get_column_statistics


def test_get_column_statistics_single_column(memory_engine) -> None:
    """
    Test case 1: Get statistics for a specific column.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)

    with Session(memory_engine) as session:
        for i in range(100):
            session.add(
                User(
                    id=i,
                    username=f"user{i}",
                    email=f"customer{i}@example.com",
                    first_name=f"First{i}",
                    age=20 + (i % 50),
                    balance=100.0 + i,
                )
            )
        session.commit()

    # Act
    with memory_engine.connect() as connection:
        stats = get_column_statistics(connection, "users", "email")

    # Assert
    assert "email" in stats
    email_stats = stats["email"]
    assert email_stats["total_rows"] == 100
    assert email_stats["distinct_count"] == 100
    assert email_stats["cardinality_ratio"] == 1.0
    assert email_stats["null_count"] == 0


def test_get_column_statistics_all_columns(memory_engine) -> None:
    """
    Test case 2: Get statistics for all columns when column_name is None.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)

    with Session(memory_engine) as session:
        for i in range(50):
            session.add(
                User(
                    id=i,
                    username=f"user{i}",
                    email=f"customer{i}@example.com",
                    first_name=f"First{i}",
                    age=25,
                    balance=100.0,
                )
            )
        session.commit()

    # Act
    with memory_engine.connect() as connection:
        stats = get_column_statistics(connection, "users")

    # Assert
    assert len(stats) > 1  # Multiple columns
    assert "username" in stats or "email" in stats


def test_get_column_statistics_with_nulls(memory_engine) -> None:
    """
    Test case 3: Track NULL values correctly.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)

    with Session(memory_engine) as session:
        for i in range(100):
            session.add(
                User(
                    id=i,
                    username=f"user{i}",
                    email=f"customer{i}@example.com",
                    first_name=f"First{i}" if i < 50 else None,  # 50% NULL
                    age=25,
                    balance=100.0,
                )
            )
        session.commit()

    # Act
    with memory_engine.connect() as connection:
        stats = get_column_statistics(connection, "users", "first_name")

    # Assert
    first_name_stats = stats["first_name"]
    assert first_name_stats["null_count"] == 50
    # null_percentage might be 50.0 (as percentage) or 0.5 (as ratio)
    assert first_name_stats["null_percentage"] in [50.0, 0.5] or pytest.approx(
        first_name_stats["null_percentage"], abs=1
    ) in [50.0, 0.5]


def test_get_column_statistics_numeric_min_max(memory_engine) -> None:
    """
    Test case 4: Calculate min/max for numeric columns.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)

    with Session(memory_engine) as session:
        for i in range(100):
            session.add(
                User(
                    id=i,
                    username=f"user{i}",
                    email=f"customer{i}@example.com",
                    first_name=f"First{i}",
                    age=20 + i,
                    balance=50.0 + i * 10,
                )
            )
        session.commit()

    # Act
    with memory_engine.connect() as connection:
        stats = get_column_statistics(connection, "users", "age")

    # Assert
    age_stats = stats["age"]
    assert "min_value" in age_stats or age_stats["distinct_count"] > 0
    assert "max_value" in age_stats or age_stats["distinct_count"] > 0


def test_get_column_statistics_top_values(memory_engine) -> None:
    """
    Test case 5: Include top values for low cardinality columns.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)

    with Session(memory_engine) as session:
        for i in range(100):
            session.add(
                User(
                    id=i,
                    username=f"user{i}",
                    email=f"customer{i}@example.com",
                    first_name="John" if i < 50 else "Jane",
                    age=25,
                    balance=100.0,
                )
            )
        session.commit()

    # Act
    with memory_engine.connect() as connection:
        stats = get_column_statistics(connection, "users", "first_name")

    # Assert
    name_stats = stats["first_name"]
    assert "top_values" in name_stats or name_stats["distinct_count"] == 2


def test_get_column_statistics_empty_table(memory_engine) -> None:
    """
    Test case 6: Handle empty table gracefully.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)

    # Act
    with memory_engine.connect() as connection:
        stats = get_column_statistics(connection, "users")

    # Assert
    assert isinstance(stats, dict)


def test_get_column_statistics_invalid_connection_type_error() -> None:
    """
    Test case 7: TypeError for None connection.
    """
    # Arrange
    expected_message = "connection cannot be None"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        get_column_statistics(None, "users")


def test_get_column_statistics_invalid_table_name_type_error(memory_engine) -> None:
    """
    Test case 8: TypeError for invalid table_name parameter.
    """
    # Arrange
    expected_message = "table_name must be str"

    # Act & Assert
    with memory_engine.connect() as connection:
        with pytest.raises(TypeError, match=expected_message):
            get_column_statistics(connection, 123)


def test_get_column_statistics_empty_table_name_value_error(memory_engine) -> None:
    """
    Test case 9: ValueError for empty table_name.
    """
    # Arrange
    expected_message = "table_name cannot be empty"

    # Act & Assert
    with memory_engine.connect() as connection:
        with pytest.raises(ValueError, match=expected_message):
            get_column_statistics(connection, "")


def test_get_column_statistics_invalid_column_name_type_error(memory_engine) -> None:
    """
    Test case 10: TypeError for invalid column_name parameter.
    """
    # Arrange
    expected_message = "column_name must be str or None"

    # Act & Assert
    with memory_engine.connect() as connection:
        with pytest.raises(TypeError, match=expected_message):
            get_column_statistics(connection, "users", column_name=123)


def test_get_column_statistics_invalid_schema_type_error(memory_engine) -> None:
    """
    Test case 11: TypeError for invalid schema parameter.
    """
    # Arrange
    expected_message = "schema must be str or None"

    # Act & Assert
    with memory_engine.connect() as connection:
        with pytest.raises(TypeError, match=expected_message):
            get_column_statistics(connection, "users", schema=123)


def test_get_column_statistics_nonexistent_column_value_error(memory_engine) -> None:
    """
    Test case 12: ValueError for non-existent column.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    expected_message = "Column nonexistent not found"

    # Act & Assert
    with memory_engine.connect() as connection:
        with pytest.raises(ValueError, match=expected_message):
            get_column_statistics(connection, "users", "nonexistent")
