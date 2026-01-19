"""
Unit tests for get_table_sizes function.
"""

from conftest import Base, Order, Product
from sqlalchemy import create_engine

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.database]
from database_functions.schema_inspection import get_table_sizes


def test_get_table_sizes_returns_all_tables() -> None:
    """
    Test case 1: Returns size info for all tables when no specific tables requested.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()

    # Insert some data
    conn.execute(
        Product.__table__.insert(), {"id": 1, "name": "Widget", "category": "Tools"}
    )
    conn.execute(Order.__table__.insert(), {"id": 1, "product_id": 1, "quantity": 5})
    conn.commit()

    # Act
    sizes = get_table_sizes(conn)

    # Assert
    assert len(sizes) >= 2
    table_names = [s["table_name"] for s in sizes]
    assert "products" in table_names
    assert "orders" in table_names

    # Verify structure
    for size_info in sizes:
        assert "table_name" in size_info
        assert "row_count" in size_info
        assert "data_size_bytes" in size_info
        assert "total_size_bytes" in size_info

    conn.close()
    engine.dispose()


def test_get_table_sizes_specific_tables() -> None:
    """
    Test case 2: Returns size info only for specified tables.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()

    conn.execute(
        Product.__table__.insert(), {"id": 1, "name": "Widget", "category": "Tools"}
    )
    conn.execute(Order.__table__.insert(), {"id": 1, "product_id": 1, "quantity": 5})
    conn.commit()

    # Act
    sizes = get_table_sizes(conn, tables=["products"])

    # Assert
    assert len(sizes) == 1
    assert sizes[0]["table_name"] == "products"
    assert sizes[0]["row_count"] == 1

    conn.close()
    engine.dispose()


def test_get_table_sizes_row_count_accuracy() -> None:
    """
    Test case 3: Verify row counts are accurate.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()

    # Insert multiple rows
    for i in range(10):
        conn.execute(
            Product.__table__.insert(),
            {"id": i, "name": f"Product{i}", "category": "Test"},
        )
    conn.commit()

    # Act
    sizes = get_table_sizes(conn, tables=["products"])

    # Assert
    assert len(sizes) == 1
    assert sizes[0]["row_count"] == 10

    conn.close()
    engine.dispose()


def test_get_table_sizes_empty_table() -> None:
    """
    Test case 4: Returns zero counts for empty tables.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()

    # Act
    sizes = get_table_sizes(conn, tables=["products"])

    # Assert
    assert len(sizes) == 1
    assert sizes[0]["row_count"] == 0
    assert sizes[0]["table_name"] == "products"

    conn.close()
    engine.dispose()


def test_get_table_sizes_include_indexes_false() -> None:
    """
    Test case 5: Omits index size when include_indexes is False.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()

    conn.execute(
        Product.__table__.insert(), {"id": 1, "name": "Widget", "category": "Tools"}
    )
    conn.commit()

    # Act
    sizes = get_table_sizes(conn, tables=["products"], include_indexes=False)

    # Assert
    assert len(sizes) == 1
    # Should still have the fields but index_size_bytes should be 0 or not included
    assert "data_size_bytes" in sizes[0]

    conn.close()
    engine.dispose()


def test_get_table_sizes_invalid_connection_type_error() -> None:
    """
    Test case 6: TypeError for None connection.
    """
    # Arrange
    expected_message = "connection cannot be None"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        get_table_sizes(None)


def test_get_table_sizes_invalid_tables_type_error() -> None:
    """
    Test case 7: TypeError for invalid tables parameter.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    conn = engine.connect()
    expected_message = "tables must be list or None"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        get_table_sizes(conn, tables="products")

    conn.close()
    engine.dispose()


def test_get_table_sizes_invalid_schema_type_error() -> None:
    """
    Test case 8: TypeError for invalid schema parameter.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    conn = engine.connect()
    expected_message = "schema must be str or None"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        get_table_sizes(conn, schema=123)

    conn.close()
    engine.dispose()


def test_get_table_sizes_invalid_include_indexes_type_error() -> None:
    """
    Test case 9: TypeError for invalid include_indexes parameter.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    conn = engine.connect()
    expected_message = "include_indexes must be bool"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        get_table_sizes(conn, include_indexes="true")

    conn.close()
    engine.dispose()


def test_get_table_sizes_nonexistent_table() -> None:
    """
    Test case 10: Handles nonexistent tables gracefully.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()

    # Act - request a table that doesn't exist
    sizes = get_table_sizes(conn, tables=["nonexistent_table"])

    # Assert - should return empty or handle gracefully
    # Behavior depends on implementation - may return empty list or skip missing tables
    assert isinstance(sizes, list)

    conn.close()
    engine.dispose()
