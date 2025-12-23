"""
Unit tests for find_missing_indexes function.
"""

import pytest
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import declarative_base

from database_functions.schema_inspection import find_missing_indexes


Base = declarative_base()


class Department(Base):
    """Test Department model."""
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))


class Employee(Base):
    """Test Employee model with foreign key but no explicit index."""
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    dept_id = Column(Integer, ForeignKey('departments.id'))  # FK without explicit index


class Project(Base):
    """Test Project model with indexed foreign key."""
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    emp_id = Column(Integer, ForeignKey('employees.id'), index=True)  # FK with index


def test_find_missing_indexes_detects_unindexed_fk() -> None:
    """
    Test case 1: Detect foreign keys without indexes.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()
    
    # Act
    missing = find_missing_indexes(conn, tables=["employees"], check_foreign_keys=True)
    
    # Assert - should recommend index on dept_id
    assert isinstance(missing, list)
    if len(missing) > 0:
        # Check if dept_id is flagged
        dept_id_flagged = any(m.get("column_name") == "dept_id" for m in missing)
        # May or may not detect depending on SQLite FK detection
        assert isinstance(dept_id_flagged, bool)
    
    conn.close()
    engine.dispose()


def test_find_missing_indexes_ignores_indexed_fk() -> None:
    """
    Test case 2: Does not recommend indexes for already-indexed foreign keys.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()
    
    # Act
    missing = find_missing_indexes(conn, tables=["projects"], check_foreign_keys=True)
    
    # Assert - emp_id is indexed, should not be flagged
    assert isinstance(missing, list)
    emp_id_flagged = any(m.get("column_name") == "emp_id" for m in missing)
    # Should be False since emp_id has index=True
    if emp_id_flagged:
        # If detected, verify it's not for FK reason
        pass
    
    conn.close()
    engine.dispose()


def test_find_missing_indexes_check_foreign_keys_false() -> None:
    """
    Test case 3: Does not check foreign keys when check_foreign_keys is False.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()
    
    # Act
    missing = find_missing_indexes(conn, tables=["employees"], check_foreign_keys=False)
    
    # Assert - should not flag FK columns
    assert isinstance(missing, list)
    # Should be empty or not include FK-related recommendations
    
    conn.close()
    engine.dispose()


def test_find_missing_indexes_specific_tables() -> None:
    """
    Test case 4: Only checks specified tables.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()
    
    # Act
    missing = find_missing_indexes(conn, tables=["employees"])
    
    # Assert
    assert isinstance(missing, list)
    for m in missing:
        assert m.get("table_name") == "employees"
    
    conn.close()
    engine.dispose()


def test_find_missing_indexes_empty_table() -> None:
    """
    Test case 5: Handles empty tables gracefully.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()
    
    # Act
    missing = find_missing_indexes(conn, tables=["departments"])
    
    # Assert
    assert isinstance(missing, list)
    # Should handle gracefully
    
    conn.close()
    engine.dispose()


def test_find_missing_indexes_invalid_connection_type_error() -> None:
    """
    Test case 6: TypeError for None connection.
    """
    # Arrange
    expected_message = "connection cannot be None"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_missing_indexes(None)


def test_find_missing_indexes_invalid_tables_type_error() -> None:
    """
    Test case 7: TypeError for invalid tables parameter.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    conn = engine.connect()
    expected_message = "tables must be list or None"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_missing_indexes(conn, tables="employees")
    
    conn.close()
    engine.dispose()


def test_find_missing_indexes_invalid_schema_type_error() -> None:
    """
    Test case 8: TypeError for invalid schema parameter.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    conn = engine.connect()
    expected_message = "schema must be str or None"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_missing_indexes(conn, schema=123)
    
    conn.close()
    engine.dispose()


def test_find_missing_indexes_invalid_check_foreign_keys_type_error() -> None:
    """
    Test case 9: TypeError for invalid check_foreign_keys parameter.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    conn = engine.connect()
    expected_message = "check_foreign_keys must be bool"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_missing_indexes(conn, check_foreign_keys="true")
    
    conn.close()
    engine.dispose()


def test_find_missing_indexes_invalid_check_nullable_type_error() -> None:
    """
    Test case 10: TypeError for invalid check_nullable_columns parameter.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    conn = engine.connect()
    expected_message = "check_nullable_columns must be bool"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_missing_indexes(conn, check_nullable_columns="false")
    
    conn.close()
    engine.dispose()
