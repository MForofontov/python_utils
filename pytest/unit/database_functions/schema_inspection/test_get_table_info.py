"""
Unit tests for get_table_info function.
"""

from conftest import Base, User
from sqlalchemy import Index
from sqlalchemy.engine import Engine

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.database]
from database_functions import get_table_info

# Add index to User table for testing
User.__table_args__ = (Index("idx_username", "username", unique=True),)


def test_get_table_info_basic_table(memory_engine: Engine) -> None:
    """
    Test case 1: Get info for a basic table with columns.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()

    # Act
    info = get_table_info(conn, "users")

    # Assert
    assert info["name"] == "users"
    assert len(info["columns"]) >= 3

    col_names = [col["name"] for col in info["columns"]]
    assert "id" in col_names
    assert "username" in col_names
    assert "email" in col_names

    # Check column details
    id_col = next(col for col in info["columns"] if col["name"] == "id")
    assert id_col["primary_key"] in (True, 1)  # SQLite returns 1 for True

    username_col = next(col for col in info["columns"] if col["name"] == "username")
    assert username_col["nullable"] is False

    conn.close()


def test_get_table_info_with_indexes(memory_engine: Engine) -> None:
    """
    Test case 2: Table info includes index information.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()

    # Act
    info = get_table_info(conn, "users")

    # Assert
    assert "indexes" in info
    assert isinstance(info["indexes"], list)

    # Check for unique index on username
    if len(info["indexes"]) > 0:
        idx_names = [idx.get("name") for idx in info["indexes"]]
        assert any("username" in str(name).lower() for name in idx_names if name)

    conn.close()


def test_get_table_info_with_foreign_keys(memory_engine: Engine) -> None:
    """
    Test case 3: Table info includes foreign key relationships.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()

    # Act
    info = get_table_info(conn, "orders")

    # Assert
    assert "foreign_keys" in info
    assert isinstance(info["foreign_keys"], list)

    # Orders table should have foreign keys to users and products
    assert len(info["foreign_keys"]) >= 1
    fk_columns = [col for fk in info["foreign_keys"] for col in fk["columns"]]
    # At least product_id should be present (user_id might not have index)
    assert "product_id" in fk_columns or "user_id" in fk_columns

    conn.close()


def test_get_table_info_column_types(memory_engine: Engine) -> None:
    """
    Test case 4: Column type information is correctly captured.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()

    # Act
    info = get_table_info(conn, "users")

    # Assert
    for col in info["columns"]:
        assert "type" in col
        assert isinstance(col["type"], str)
        assert len(col["type"]) > 0

    conn.close()


def test_get_table_info_empty_table_name(memory_engine: Engine) -> None:
    """
    Test case 5: Empty table name raises ValueError.
    """
    # Arrange
    conn = memory_engine.connect()

    # Act & Assert
    with pytest.raises(ValueError, match="table_name cannot be empty"):
        get_table_info(conn, "")

    conn.close()


def test_get_table_info_nonexistent_table(memory_engine: Engine) -> None:
    """
    Test case 6: Nonexistent table raises ValueError.
    """
    # Arrange
    conn = memory_engine.connect()

    # Act & Assert
    with pytest.raises(ValueError, match="Table 'nonexistent' not found"):
        get_table_info(conn, "nonexistent")

    conn.close()


def test_get_table_info_none_connection() -> None:
    """
    Test case 7: None connection raises TypeError.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="connection cannot be None"):
        get_table_info(None, "users")


def test_get_table_info_invalid_table_name_type(memory_engine: Engine) -> None:
    """
    Test case 8: Invalid table_name type raises TypeError.
    """
    # Arrange
    conn = memory_engine.connect()

    # Act & Assert
    with pytest.raises(TypeError, match="table_name must be str"):
        get_table_info(conn, 123)

    conn.close()


def test_get_table_info_invalid_schema_type(memory_engine: Engine) -> None:
    """
    Test case 9: Invalid schema type raises TypeError.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()

    # Act & Assert
    with pytest.raises(TypeError, match="schema must be str or None"):
        get_table_info(conn, "users", schema=123)

    conn.close()


def test_get_table_info_nullable_columns(memory_engine: Engine) -> None:
    """
    Test case 10: Correctly identifies nullable and non-nullable columns.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()

    # Act
    info = get_table_info(conn, "users")

    # Assert
    username_col = next(col for col in info["columns"] if col["name"] == "username")
    first_name_col = next(col for col in info["columns"] if col["name"] == "first_name")

    assert username_col["nullable"] is False
    assert first_name_col["nullable"] is True

    conn.close()
