"""
Unit tests for find_duplicate_rows function.
"""

import pytest
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base

from database_functions.schema_inspection import find_duplicate_rows


Base = declarative_base()


class User(Base):
    """Test User model."""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(100))
    username = Column(String(50))


def test_find_duplicate_rows_identifies_duplicates() -> None:
    """
    Test case 1: Identify rows with duplicate email addresses.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()
    
    # Insert duplicate emails
    conn.execute(User.__table__.insert(), {"id": 1, "email": "john@example.com", "username": "john1"})
    conn.execute(User.__table__.insert(), {"id": 2, "email": "john@example.com", "username": "john2"})
    conn.execute(User.__table__.insert(), {"id": 3, "email": "jane@example.com", "username": "jane"})
    conn.commit()
    
    # Act
    duplicates = find_duplicate_rows(conn, "users", ["email"])
    
    # Assert
    assert len(duplicates) == 1
    assert duplicates[0]["email"] == "john@example.com"
    assert duplicates[0]["count"] == 2
    
    conn.close()
    engine.dispose()


def test_find_duplicate_rows_multiple_columns() -> None:
    """
    Test case 2: Find duplicates based on multiple columns.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()
    
    conn.execute(User.__table__.insert(), {"id": 1, "email": "john@example.com", "username": "john"})
    conn.execute(User.__table__.insert(), {"id": 2, "email": "john@example.com", "username": "john"})
    conn.execute(User.__table__.insert(), {"id": 3, "email": "john@example.com", "username": "john2"})
    conn.commit()
    
    # Act
    duplicates = find_duplicate_rows(conn, "users", ["email", "username"])
    
    # Assert
    assert len(duplicates) == 1
    assert duplicates[0]["email"] == "john@example.com"
    assert duplicates[0]["username"] == "john"
    assert duplicates[0]["count"] == 2
    
    conn.close()
    engine.dispose()


def test_find_duplicate_rows_no_duplicates() -> None:
    """
    Test case 3: Empty result when no duplicates exist.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()
    
    conn.execute(User.__table__.insert(), {"id": 1, "email": "john@example.com", "username": "john"})
    conn.execute(User.__table__.insert(), {"id": 2, "email": "jane@example.com", "username": "jane"})
    conn.commit()
    
    # Act
    duplicates = find_duplicate_rows(conn, "users", ["email"])
    
    # Assert
    assert len(duplicates) == 0
    
    conn.close()
    engine.dispose()


def test_find_duplicate_rows_min_duplicates_threshold() -> None:
    """
    Test case 4: Respect min_duplicates threshold.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()
    
    # Create 3 duplicates
    conn.execute(User.__table__.insert(), {"id": 1, "email": "john@example.com", "username": "john1"})
    conn.execute(User.__table__.insert(), {"id": 2, "email": "john@example.com", "username": "john2"})
    conn.execute(User.__table__.insert(), {"id": 3, "email": "john@example.com", "username": "john3"})
    conn.commit()
    
    # Act - require at least 4 duplicates
    duplicates = find_duplicate_rows(conn, "users", ["email"], min_duplicates=4)
    
    # Assert
    assert len(duplicates) == 0  # 3 < 4, so no results
    
    conn.close()
    engine.dispose()


def test_find_duplicate_rows_invalid_connection_type_error() -> None:
    """
    Test case 5: TypeError for None connection.
    """
    # Arrange
    expected_message = "connection cannot be None"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_duplicate_rows(None, "users", ["email"])


def test_find_duplicate_rows_invalid_table_name_type_error() -> None:
    """
    Test case 6: TypeError for invalid table_name.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    conn = engine.connect()
    expected_message = "table_name must be str"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_duplicate_rows(conn, 123, ["email"])
    
    conn.close()
    engine.dispose()


def test_find_duplicate_rows_empty_table_name_value_error() -> None:
    """
    Test case 7: ValueError for empty table_name.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    conn = engine.connect()
    expected_message = "table_name cannot be empty"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        find_duplicate_rows(conn, "", ["email"])
    
    conn.close()
    engine.dispose()


def test_find_duplicate_rows_invalid_columns_type_error() -> None:
    """
    Test case 8: TypeError for invalid columns parameter.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    conn = engine.connect()
    expected_message = "columns must be list"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_duplicate_rows(conn, "users", "email")
    
    conn.close()
    engine.dispose()


def test_find_duplicate_rows_empty_columns_value_error() -> None:
    """
    Test case 9: ValueError for empty columns list.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    conn = engine.connect()
    expected_message = "columns list cannot be empty"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        find_duplicate_rows(conn, "users", [])
    
    conn.close()
    engine.dispose()


def test_find_duplicate_rows_invalid_min_duplicates_type_error() -> None:
    """
    Test case 10: TypeError for invalid min_duplicates.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()
    expected_message = "min_duplicates must be int"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_duplicate_rows(conn, "users", ["email"], min_duplicates="2")
    
    conn.close()
    engine.dispose()


def test_find_duplicate_rows_min_duplicates_value_error() -> None:
    """
    Test case 11: ValueError for min_duplicates < 2.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()
    expected_message = "min_duplicates must be at least 2"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        find_duplicate_rows(conn, "users", ["email"], min_duplicates=1)
    
    conn.close()
    engine.dispose()


def test_find_duplicate_rows_sorted_by_count() -> None:
    """
    Test case 12: Results sorted by duplicate count descending.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()
    
    # Create different duplicate counts
    conn.execute(User.__table__.insert(), {"id": 1, "email": "a@example.com", "username": "a1"})
    conn.execute(User.__table__.insert(), {"id": 2, "email": "a@example.com", "username": "a2"})
    conn.execute(User.__table__.insert(), {"id": 3, "email": "b@example.com", "username": "b1"})
    conn.execute(User.__table__.insert(), {"id": 4, "email": "b@example.com", "username": "b2"})
    conn.execute(User.__table__.insert(), {"id": 5, "email": "b@example.com", "username": "b3"})
    conn.commit()
    
    # Act
    duplicates = find_duplicate_rows(conn, "users", ["email"])
    
    # Assert
    assert len(duplicates) == 2
    # First result should have higher count
    assert duplicates[0]["count"] >= duplicates[1]["count"]
    
    conn.close()
    engine.dispose()
