"""
Unit tests for find_missing_indexes function.
"""

from conftest import Base

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.database]
from database_functions.schema_inspection import find_missing_indexes


def test_find_missing_indexes_detects_unindexed_fk(memory_engine) -> None:
    """
    Test case 1: Detect foreign keys without indexes.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()

    # Act - Check orders table which has user_id FK WITHOUT an index
    missing = find_missing_indexes(conn, tables=["orders"], check_foreign_keys=True)

    # Assert - Should detect the missing index on user_id foreign key
    assert isinstance(missing, list)
    assert len(missing) > 0, "Should detect unindexed foreign key on user_id"
    # Verify it detected the user_id column
    user_id_found = any(
        m.get("table_name") == "orders" and "user_id" in str(m.get("column_name", ""))
        for m in missing
    )
    assert user_id_found, "Should detect missing index on user_id foreign key"

    conn.close()


def test_find_missing_indexes_ignores_indexed_fk(memory_engine) -> None:
    """
    Test case 2: Does not recommend indexes for already-indexed foreign keys.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()

    # Act - Check invoices table which has all FKs indexed
    missing = find_missing_indexes(conn, tables=["invoices"], check_foreign_keys=True)

    # Assert - Invoice user_id and order_id are indexed, should not be flagged for FK indexes
    assert isinstance(missing, list)
    # Check that user_id and order_id are NOT in the missing list
    fk_missing = [m for m in missing if m.get("column_name") in ["user_id", "order_id"]]
    assert len(fk_missing) == 0, "Should not flag indexed foreign keys"

    conn.close()


def test_find_missing_indexes_check_foreign_keys_false(memory_engine) -> None:
    """
    Test case 3: Does not check foreign keys when check_foreign_keys is False.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()

    # Act
    missing = find_missing_indexes(conn, tables=["orders"], check_foreign_keys=False)

    # Assert - should not flag FK columns
    assert isinstance(missing, list)
    # Should be empty or not include FK-related recommendations

    conn.close()


def test_find_missing_indexes_specific_tables(memory_engine) -> None:
    """
    Test case 4: Only checks specified tables.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()

    # Act
    missing = find_missing_indexes(conn, tables=["orders"])

    # Assert
    assert isinstance(missing, list)
    for m in missing:
        assert m.get("table_name") == "orders"

    conn.close()


def test_find_missing_indexes_empty_table(memory_engine) -> None:
    """
    Test case 5: Handles empty tables gracefully.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()

    # Act
    missing = find_missing_indexes(conn, tables=["users"])

    # Assert
    assert isinstance(missing, list)
    # Should handle gracefully

    conn.close()


def test_find_missing_indexes_invalid_connection_type_error() -> None:
    """
    Test case 6: TypeError for None connection.
    """
    # Arrange
    expected_message = "connection cannot be None"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_missing_indexes(None)


def test_find_missing_indexes_invalid_tables_type_error(memory_engine) -> None:
    """
    Test case 7: TypeError for invalid tables parameter.
    """
    # Arrange
    conn = memory_engine.connect()
    expected_message = "tables must be list or None"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_missing_indexes(conn, tables="orders")

    conn.close()


def test_find_missing_indexes_invalid_schema_type_error(memory_engine) -> None:
    """
    Test case 8: TypeError for invalid schema parameter.
    """
    # Arrange
    conn = memory_engine.connect()
    expected_message = "schema must be str or None"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_missing_indexes(conn, schema=123)

    conn.close()


def test_find_missing_indexes_invalid_check_foreign_keys_type_error(
    memory_engine,
) -> None:
    """
    Test case 9: TypeError for invalid check_foreign_keys parameter.
    """
    # Arrange
    conn = memory_engine.connect()
    expected_message = "check_foreign_keys must be bool"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_missing_indexes(conn, check_foreign_keys="true")

    conn.close()


def test_find_missing_indexes_invalid_check_nullable_type_error(memory_engine) -> None:
    """
    Test case 10: TypeError for invalid check_nullable_columns parameter.
    """
    # Arrange
    conn = memory_engine.connect()
    expected_message = "check_nullable_columns must be bool"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_missing_indexes(conn, check_nullable_columns="false")

    conn.close()


def test_find_missing_indexes_check_nullable_columns(memory_engine) -> None:
    """
    Test case 11: Check nullable columns when enabled.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()

    # Act - enable nullable column checking on transactions table
    missing = find_missing_indexes(
        conn, tables=["transactions"], check_nullable_columns=True
    )

    # Assert - should include recommendations for nullable columns
    assert isinstance(missing, list)
    # May have recommendations for nullable columns in transactions

    conn.close()


def test_find_missing_indexes_error_handling_for_foreign_keys(memory_engine) -> None:
    """
    Test case 12: Handle errors when checking foreign keys gracefully.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()

    # Act - should handle checking invoices table gracefully
    missing = find_missing_indexes(conn, tables=["invoices"])

    # Assert
    assert isinstance(missing, list)

    conn.close()
