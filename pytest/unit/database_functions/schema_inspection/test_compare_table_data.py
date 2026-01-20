"""
Unit tests for compare_table_data function.
"""

from conftest import Base, User
from sqlalchemy.engine import Engine

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.database]
from pyutils_collection.database_functions.schema_inspection import compare_table_data


def test_compare_table_data_identical_tables(memory_engine: Engine) -> None:
    """
    Test case 1: Compare identical tables returns match.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()

    # Insert identical data
    conn.execute(
        User.__table__.insert(),
        {"id": 1, "username": "alice", "email": "alice@example.com"},
    )
    conn.execute(
        User.__table__.insert(),
        {"id": 2, "username": "bob", "email": "bob@example.com"},
    )
    conn.commit()

    # Act - compare same table with itself
    result = compare_table_data(conn, conn, "users", "users")

    # Assert
    assert result["source_count"] == result["target_count"]
    assert result["count_match"] is True
    assert result["source_count"] == 2

    conn.close()


def test_compare_table_data_different_row_counts(
    dual_engines: tuple[Engine, Engine],
) -> None:
    """
    Test case 2: Detect different row counts.
    """
    # Arrange
    engine1, engine2 = dual_engines
    Base.metadata.create_all(engine1)
    Base.metadata.create_all(engine2)
    conn1 = engine1.connect()
    conn2 = engine2.connect()

    # Insert different amounts of data
    conn1.execute(
        User.__table__.insert(),
        {"id": 1, "username": "alice", "email": "alice@example.com"},
    )
    conn1.execute(
        User.__table__.insert(),
        {"id": 2, "username": "bob", "email": "bob@example.com"},
    )
    conn1.commit()

    conn2.execute(
        User.__table__.insert(),
        {"id": 1, "username": "alice", "email": "alice@example.com"},
    )
    conn2.commit()

    # Act
    result = compare_table_data(conn1, conn2, "users", "users")

    # Assert
    assert result["source_count"] == 2
    assert result["target_count"] == 1
    assert result["count_match"] is False

    conn1.close()
    conn2.close()


def test_compare_table_data_empty_tables(memory_engine: Engine) -> None:
    """
    Test case 3: Compare empty tables.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()

    # Act
    result = compare_table_data(conn, conn, "users", "users")

    # Assert
    assert result["source_count"] == 0
    assert result["target_count"] == 0
    assert result["count_match"] is True

    conn.close()


def test_compare_table_data_common_columns(memory_engine: Engine) -> None:
    """
    Test case 4: Identifies common columns between tables.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()

    conn.execute(
        User.__table__.insert(),
        {"id": 1, "username": "alice", "email": "alice@example.com"},
    )
    conn.commit()

    # Act
    result = compare_table_data(conn, conn, "users", "users")

    # Assert
    assert "common_columns" in result
    assert isinstance(result["common_columns"], list)
    assert len(result["common_columns"]) > 0

    conn.close()


def test_compare_table_data_specific_columns(memory_engine: Engine) -> None:
    """
    Test case 5: Compare only specified columns.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()

    conn.execute(
        User.__table__.insert(),
        {"id": 1, "username": "alice", "email": "alice@example.com"},
    )
    conn.commit()

    # Act - compare only username column
    result = compare_table_data(
        conn, conn, "users", "users", compare_columns=["username"]
    )

    # Assert
    assert result["count_match"] is True

    conn.close()


def test_compare_table_data_invalid_source_connection_type_error(
    memory_engine: Engine,
) -> None:
    """
    Test case 6: TypeError for None source_connection.
    """
    # Arrange
    conn = memory_engine.connect()
    expected_message = "source_connection cannot be None"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        compare_table_data(None, conn, "users")

    conn.close()


def test_compare_table_data_invalid_target_connection_type_error(
    memory_engine: Engine,
) -> None:
    """
    Test case 7: TypeError for None target_connection.
    """
    # Arrange
    conn = memory_engine.connect()
    expected_message = "target_connection cannot be None"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        compare_table_data(conn, None, "users")

    conn.close()


def test_compare_table_data_invalid_source_table_type_error(
    memory_engine: Engine,
) -> None:
    """
    Test case 8: TypeError for invalid source_table.
    """
    # Arrange
    conn = memory_engine.connect()
    expected_message = "source_table must be str"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        compare_table_data(conn, conn, 123)

    conn.close()


def test_compare_table_data_empty_source_table_value_error(
    memory_engine: Engine,
) -> None:
    """
    Test case 9: ValueError for empty source_table.
    """
    # Arrange
    conn = memory_engine.connect()
    expected_message = "source_table cannot be empty"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        compare_table_data(conn, conn, "")

    conn.close()


def test_compare_table_data_invalid_compare_columns_type_error(
    memory_engine: Engine,
) -> None:
    """
    Test case 10: TypeError for invalid compare_columns.
    """
    # Arrange
    conn = memory_engine.connect()
    expected_message = "compare_columns must be list or None"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        compare_table_data(conn, conn, "users", compare_columns="username")

    conn.close()


def test_compare_table_data_invalid_sample_differences_type_error(
    memory_engine: Engine,
) -> None:
    """
    Test case 11: TypeError for invalid sample_differences.
    """
    # Arrange
    conn = memory_engine.connect()
    expected_message = "sample_differences must be int"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        compare_table_data(conn, conn, "users", sample_differences="10")

    conn.close()


def test_compare_table_data_negative_sample_differences_value_error(
    memory_engine: Engine,
) -> None:
    """
    Test case 12: ValueError for negative sample_differences.
    """
    # Arrange
    conn = memory_engine.connect()
    expected_message = "sample_differences must be non-negative"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        compare_table_data(conn, conn, "users", sample_differences=-1)

    conn.close()
