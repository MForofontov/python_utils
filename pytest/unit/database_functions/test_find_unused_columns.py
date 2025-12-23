"""
Unit tests for find_unused_columns function.
"""

import pytest
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, Session

from database_functions.schema_inspection import find_unused_columns


Base = declarative_base()


class Customer(Base):
    """Test Customer model."""
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    phone = Column(String(20))
    notes = Column(String(500))


class NullableTable(Base):
    """Table with nullable columns for testing."""
    __tablename__ = 'nullable_table'
    id = Column(Integer, primary_key=True)
    optional_field = Column(String(100), nullable=True)
    another_field = Column(String(100), nullable=True)


class DataTable(Base):
    """Test model with mixed NULL/non-NULL columns."""
    __tablename__ = "data_table"

    id = Column(Integer, primary_key=True)
    used_column = Column(String(50))
    mostly_null_column = Column(String(50))
    completely_null_column = Column(String(50))


def test_find_unused_columns_detects_high_null_percentage(memory_engine) -> None:
    """
    Test case 1: Identify columns with high NULL percentage.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()
    
    # Insert data with mostly NULL in 'notes' column
    for i in range(100):
        conn.execute(Customer.__table__.insert(), {
            "id": i,
            "name": f"Customer{i}",
            "email": f"customer{i}@example.com",
            "phone": None,
            "notes": None  # 100% NULL
        })
    conn.commit()
    
    # Act
    unused = find_unused_columns(conn, tables=["customers"], null_threshold=0.90)
    
    # Assert
    assert len(unused) >= 2  # phone and notes should be flagged
    column_names = [u["column_name"] for u in unused]
    assert "phone" in column_names
    assert "notes" in column_names
    
    # Verify structure
    for col in unused:
        assert "table_name" in col
        assert "column_name" in col
        assert "null_count" in col
        assert "total_rows" in col
        assert "null_percentage" in col
        assert col["null_percentage"] >= 0.90
    
    conn.close()


def test_find_unused_columns_no_unused_columns(memory_engine) -> None:
    """
    Test case 2: Returns empty list when all columns have low NULL percentage.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()
    
    # Insert data with all columns populated
    for i in range(10):
        conn.execute(Customer.__table__.insert(), {
            "id": i,
            "name": f"Customer{i}",
            "email": f"customer{i}@example.com",
            "phone": f"555-{i:04d}",
            "notes": f"Notes {i}"
        })
    conn.commit()
    
    # Act
    unused = find_unused_columns(conn, tables=["customers"], null_threshold=0.95)
    
    # Assert
    assert len(unused) == 0
    
    conn.close()


def test_find_unused_columns_custom_threshold(memory_engine) -> None:
    """
    Test case 3: Respects custom null_threshold parameter.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()
    
    # Insert data with 50% NULL
    for i in range(100):
        conn.execute(Customer.__table__.insert(), {
            "id": i,
            "name": f"Customer{i}",
            "email": f"customer{i}@example.com",
            "phone": f"555-{i:04d}" if i % 2 == 0 else None,  # 50% NULL
            "notes": "Some notes"
        })
    conn.commit()
    
    # Act - set threshold to 40% (should catch phone column)
    unused = find_unused_columns(conn, tables=["customers"], null_threshold=0.40)
    
    # Assert
    assert any(col["column_name"] == "phone" for col in unused)
    
    conn.close()


def test_find_unused_columns_empty_table(memory_engine) -> None:
    """
    Test case 4: Handles empty tables gracefully.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()
    
    # Act
    unused = find_unused_columns(conn, tables=["customers"])
    
    # Assert - should handle gracefully, not crash
    assert isinstance(unused, list)
    
    conn.close()


def test_find_unused_columns_specific_tables(memory_engine) -> None:
    """
    Test case 5: Only checks specified tables.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()
    
    for i in range(10):
        conn.execute(Customer.__table__.insert(), {
            "id": i,
            "name": f"Customer{i}",
            "email": f"customer{i}@example.com",
            "phone": None,
            "notes": None
        })
    conn.commit()
    
    # Act
    unused = find_unused_columns(conn, tables=["customers"])
    
    # Assert
    assert all(col["table_name"] == "customers" for col in unused)
    
    conn.close()


def test_find_unused_columns_invalid_connection_type_error() -> None:
    """
    Test case 6: TypeError for None connection.
    """
    # Arrange
    expected_message = "connection cannot be None"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_unused_columns(None)


def test_find_unused_columns_invalid_tables_type_error(memory_engine) -> None:
    """
    Test case 7: TypeError for invalid tables parameter.
    """
    # Arrange
    conn = memory_engine.connect()
    expected_message = "tables must be list or None"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_unused_columns(conn, tables="customers")
    
    conn.close()


def test_find_unused_columns_invalid_schema_type_error(memory_engine) -> None:
    """
    Test case 8: TypeError for invalid schema parameter.
    """
    # Arrange
    conn = memory_engine.connect()
    expected_message = "schema must be str or None"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_unused_columns(conn, schema=123)
    
    conn.close()


def test_find_unused_columns_invalid_threshold_type_error(memory_engine) -> None:
    """
    Test case 9: TypeError for invalid null_threshold parameter.
    """
    # Arrange
    conn = memory_engine.connect()
    expected_message = "null_threshold must be float"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_unused_columns(conn, null_threshold="0.95")
    
    conn.close()


def test_find_unused_columns_threshold_out_of_range_value_error(memory_engine) -> None:
    """
    Test case 10: ValueError for null_threshold out of range.
    """
    # Arrange
    conn = memory_engine.connect()
    expected_message = "null_threshold must be between 0 and 1"
    
    # Act & Assert - test > 1
    with pytest.raises(ValueError, match=expected_message):
        find_unused_columns(conn, null_threshold=1.5)
    
    # Test < 0
    with pytest.raises(ValueError, match=expected_message):
        find_unused_columns(conn, null_threshold=-0.1)
    
    conn.close()


def test_find_unused_columns_distinct_count_exception(memory_engine) -> None:
    """
    Test case 11: Handle exception when getting distinct count.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()
    
    # Insert data with all NULL in optional_field
    for i in range(10):
        conn.execute(NullableTable.__table__.insert(), {
            "id": i,
            "optional_field": None,
            "another_field": None
        })
    conn.commit()
    
    # Act - should handle potential exceptions in distinct count
    unused = find_unused_columns(conn, tables=["nullable_table"], null_threshold=0.5)
    
    # Assert
    assert len(unused) >= 2  # Both nullable fields should be flagged
    
    conn.close()


def test_find_unused_columns_with_some_distinct_values(memory_engine) -> None:
    """
    Test case 12: Handle columns with some non-NULL values for cardinality calculation.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()
    
    # Insert data with some NULL and some non-NULL
    for i in range(100):
        conn.execute(NullableTable.__table__.insert(), {
            "id": i,
            "optional_field": "value1" if i < 10 else None,  # 10% non-NULL
            "another_field": None  # 100% NULL
        })
    conn.commit()
    
    # Act
    unused = find_unused_columns(conn, tables=["nullable_table"], null_threshold=0.50)
    
    # Assert
    assert len(unused) >= 1
    # Should include cardinality_ratio for optional_field if it has non-NULL values
    
    conn.close()


def test_find_unused_columns_mixed_usage(memory_engine) -> None:
    """
    Test case 13: Mixed columns - some used, some unused.
    
    Tests find_unused_columns with a table containing columns with varying
    NULL percentages to verify correct identification of unused columns.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)

    with Session(memory_engine) as session:
        # Create 100 rows with mixed NULL patterns
        for i in range(1, 101):
            # used_column: always has values (0% NULL)
            # mostly_null_column: 85% NULL
            # completely_null_column: 100% NULL
            session.add(DataTable(
                id=i,
                used_column=f"value_{i}",
                mostly_null_column=f"value_{i}" if i <= 15 else None,
                completely_null_column=None,
            ))
        session.commit()

    # Act
    with memory_engine.connect() as connection:
        unused = find_unused_columns(
            connection,
            tables=["data_table"],
            null_threshold=0.80,  # 80% threshold
        )

    # Assert
    assert len(unused) == 2, "Should find 2 unused columns"
    
    unused_names = {col["column_name"] for col in unused}
    assert "used_column" not in unused_names, "used_column should not be flagged"
    assert "mostly_null_column" in unused_names, "mostly_null_column should be flagged (85% NULL)"
    assert "completely_null_column" in unused_names, "completely_null_column should be flagged (100% NULL)"
    
    # Verify percentages
    mostly_null = next(c for c in unused if c["column_name"] == "mostly_null_column")
    assert mostly_null["null_percentage"] == 0.85
    
    completely_null = next(c for c in unused if c["column_name"] == "completely_null_column")
    assert completely_null["null_percentage"] == 1.0
