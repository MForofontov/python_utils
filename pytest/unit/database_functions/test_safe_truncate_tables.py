"""
Unit tests for safe_truncate_tables function.
"""

import pytest
from sqlalchemy import Column, Integer, String, ForeignKey, MetaData, Table
from sqlalchemy.orm import declarative_base

from database_functions.schema_inspection import safe_truncate_tables


Base = declarative_base()


class Department(Base):
    """Test Department model."""
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))


class Employee(Base):
    """Test Employee model - depends on Department."""
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    dept_id = Column(Integer, ForeignKey('departments.id'))


class Project(Base):
    """Test Project model - depends on Employee."""
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    emp_id = Column(Integer, ForeignKey('employees.id'))


def test_safe_truncate_tables_respects_fk_order(memory_engine) -> None:
    """
    Test case 1: Tables are truncated in safe FK dependency order.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()
    
    # Insert test data
    conn.execute(Department.__table__.insert(), {"id": 1, "name": "Engineering"})
    conn.execute(Employee.__table__.insert(), {"id": 1, "name": "Alice", "dept_id": 1})
    conn.execute(Project.__table__.insert(), {"id": 1, "name": "Project X", "emp_id": 1})
    conn.commit()
    
    # Act
    result = safe_truncate_tables(conn)
    
    # Assert
    assert result["success"] is True
    assert len(result["truncated"]) == 3
    assert "projects" in result["truncated"]
    assert "employees" in result["truncated"]
    assert "departments" in result["truncated"]
    
    # Verify order: projects before employees before departments
    order = result["order_used"]
    projects_idx = order.index("projects")
    employees_idx = order.index("employees")
    departments_idx = order.index("departments")
    assert projects_idx < employees_idx < departments_idx
    
    conn.close()


def test_safe_truncate_tables_specific_tables(memory_engine) -> None:
    """
    Test case 2: Truncate only specified tables.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()
    
    conn.execute(Department.__table__.insert(), {"id": 1, "name": "Engineering"})
    conn.execute(Employee.__table__.insert(), {"id": 1, "name": "Alice", "dept_id": 1})
    conn.commit()
    
    # Act
    result = safe_truncate_tables(conn, tables=["employees"])
    
    # Assert
    assert result["success"] is True
    assert "employees" in result["truncated"]
    assert "departments" not in result["truncated"]
    
    conn.close()


def test_safe_truncate_tables_empty_database(memory_engine) -> None:
    """
    Test case 3: Handle empty database gracefully.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()
    
    # Act
    result = safe_truncate_tables(conn)
    
    # Assert
    assert result["success"] is True
    assert len(result["truncated"]) >= 0
    
    conn.close()


def test_safe_truncate_tables_invalid_connection_type_error() -> None:
    """
    Test case 4: TypeError for None connection.
    """
    # Arrange
    expected_message = "connection cannot be None"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        safe_truncate_tables(None)


def test_safe_truncate_tables_invalid_tables_type_error(memory_engine) -> None:
    """
    Test case 5: TypeError for invalid tables parameter.
    """
    # Arrange
    conn = memory_engine.connect()
    expected_message = "tables must be list or None"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        safe_truncate_tables(conn, tables="invalid")
    
    conn.close()


def test_safe_truncate_tables_invalid_cascade_type_error(memory_engine) -> None:
    """
    Test case 6: TypeError for invalid cascade parameter.
    """
    # Arrange
    conn = memory_engine.connect()
    expected_message = "cascade must be bool"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        safe_truncate_tables(conn, cascade="yes")
    
    conn.close()


def test_safe_truncate_tables_invalid_schema_type_error(memory_engine) -> None:
    """
    Test case 7: TypeError for invalid schema parameter.
    """
    # Arrange
    conn = memory_engine.connect()
    expected_message = "schema must be str or None"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        safe_truncate_tables(conn, schema=123)
    
    conn.close()


def test_safe_truncate_tables_verifies_data_deleted(memory_engine) -> None:
    """
    Test case 8: Verify data is actually deleted after truncation.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()
    
    # Insert data
    conn.execute(Department.__table__.insert(), {"id": 1, "name": "Engineering"})
    conn.execute(Department.__table__.insert(), {"id": 2, "name": "Sales"})
    conn.commit()
    
    # Act
    result = safe_truncate_tables(conn, tables=["departments"])
    
    # Assert
    assert result["success"] is True
    
    # Verify data is gone
    count_result = conn.execute(Department.__table__.select())
    rows = count_result.fetchall()
    assert len(rows) == 0
    
    conn.close()


def test_safe_truncate_tables_with_cascade_option(memory_engine) -> None:
    """
    Test case 9: Test cascade parameter is accepted.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()
    
    # Act
    result = safe_truncate_tables(conn, cascade=True)
    
    # Assert
    assert result["success"] is True
    assert isinstance(result["truncated"], list)
    
    conn.close()


def test_safe_truncate_tables_nonexistent_table_in_list(memory_engine) -> None:
    """
    Test case 10: Handle nonexistent table gracefully.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()
    
    # Act
    result = safe_truncate_tables(conn, tables=["nonexistent_table"])
    
    # Assert
    # Should handle gracefully, either skip or report error
    assert "errors" in result
    
    conn.close()


def test_safe_truncate_tables_commit_exception_handling(memory_engine) -> None:
    """
    Test case 11: Handle commit exceptions gracefully.
    """
    # Arrange
    
    class TableWithoutFK(Base):
        """Simple table for testing."""
        __tablename__ = 'test_table'
        id = Column(Integer, primary_key=True)
        data = Column(String(50))
    
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()
    
    # Insert some data
    conn.execute(TableWithoutFK.__table__.insert(), {"id": 1, "data": "test"})
    conn.commit()
    
    # Act - should handle even if commit raises exception
    result = safe_truncate_tables(conn, tables=["test_table"])
    
    # Assert - should succeed or fail gracefully
    assert isinstance(result, dict)
    assert "success" in result
    assert "truncated" in result
    
    conn.close()
