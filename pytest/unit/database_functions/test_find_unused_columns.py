"""
Unit tests for find_unused_columns function.
"""

import pytest
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

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


def test_find_unused_columns_detects_high_null_percentage() -> None:
    """
    Test case 1: Identify columns with high NULL percentage.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()
    
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
    engine.dispose()


def test_find_unused_columns_no_unused_columns() -> None:
    """
    Test case 2: Returns empty list when all columns have low NULL percentage.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()
    
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
    engine.dispose()


def test_find_unused_columns_custom_threshold() -> None:
    """
    Test case 3: Respects custom null_threshold parameter.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()
    
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
    engine.dispose()


def test_find_unused_columns_empty_table() -> None:
    """
    Test case 4: Handles empty tables gracefully.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()
    
    # Act
    unused = find_unused_columns(conn, tables=["customers"])
    
    # Assert - should handle gracefully, not crash
    assert isinstance(unused, list)
    
    conn.close()
    engine.dispose()


def test_find_unused_columns_specific_tables() -> None:
    """
    Test case 5: Only checks specified tables.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()
    
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
    engine.dispose()


def test_find_unused_columns_invalid_connection_type_error() -> None:
    """
    Test case 6: TypeError for None connection.
    """
    # Arrange
    expected_message = "connection cannot be None"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_unused_columns(None)


def test_find_unused_columns_invalid_tables_type_error() -> None:
    """
    Test case 7: TypeError for invalid tables parameter.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    conn = engine.connect()
    expected_message = "tables must be list or None"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_unused_columns(conn, tables="customers")
    
    conn.close()
    engine.dispose()


def test_find_unused_columns_invalid_schema_type_error() -> None:
    """
    Test case 8: TypeError for invalid schema parameter.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    conn = engine.connect()
    expected_message = "schema must be str or None"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_unused_columns(conn, schema=123)
    
    conn.close()
    engine.dispose()


def test_find_unused_columns_invalid_threshold_type_error() -> None:
    """
    Test case 9: TypeError for invalid null_threshold parameter.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    conn = engine.connect()
    expected_message = "null_threshold must be float"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_unused_columns(conn, null_threshold="0.95")
    
    conn.close()
    engine.dispose()


def test_find_unused_columns_threshold_out_of_range_value_error() -> None:
    """
    Test case 10: ValueError for null_threshold out of range.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    conn = engine.connect()
    expected_message = "null_threshold must be between 0 and 1"
    
    # Act & Assert - test > 1
    with pytest.raises(ValueError, match=expected_message):
        find_unused_columns(conn, null_threshold=1.5)
    
    # Test < 0
    with pytest.raises(ValueError, match=expected_message):
        find_unused_columns(conn, null_threshold=-0.1)
    
    conn.close()
    engine.dispose()
