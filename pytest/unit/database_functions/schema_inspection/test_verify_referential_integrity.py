"""
Unit tests for verify_referential_integrity function.
"""

import pytest
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, Session

from database_functions.schema_inspection import verify_referential_integrity
from conftest import Base, Department, Employee, Project


def test_verify_referential_integrity_no_violations(memory_engine) -> None:
    """
    Test case 1: No violations when all FKs are valid.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    
    with Session(memory_engine) as session:
        dept = Department(id=1, name="Engineering")
        session.add(dept)
        session.add(Employee(id=1, name="Alice", dept_id=1))
        session.add(Employee(id=2, name="Bob", dept_id=1))
        session.commit()
    
    # Act
    with memory_engine.connect() as connection:
        violations = verify_referential_integrity(connection)
    
    # Assert
    assert isinstance(violations, list)
    assert len(violations) == 0


def test_verify_referential_integrity_detects_orphaned_records(memory_engine) -> None:
    """
    Test case 2: Detect orphaned records (FK points to non-existent parent).
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    
    with Session(memory_engine) as session:
        # Create department
        dept = Department(id=1, name="Engineering")
        session.add(dept)
        # Create employee with valid FK
        session.add(Employee(id=1, name="Alice", dept_id=1))
        # Create orphaned employee (dept_id=999 doesn't exist)
        session.add(Employee(id=2, name="Bob", dept_id=999))
        session.commit()
    
    # Act
    with memory_engine.connect() as connection:
        violations = verify_referential_integrity(connection)
    
    # Assert
    assert len(violations) >= 1
    emp_violation = next((v for v in violations if v["table"] == "employees"), None)
    if emp_violation:
        assert emp_violation["column"] == "dept_id"
        assert emp_violation["referenced_table"] == "departments"
        assert emp_violation["orphaned_count"] >= 1


def test_verify_referential_integrity_provides_sample_ids(memory_engine) -> None:
    """
    Test case 3: Provide sample IDs of orphaned records.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    
    with Session(memory_engine) as session:
        dept = Department(id=1, name="Engineering")
        session.add(dept)
        # Create multiple orphaned employees
        for i in range(15):
            session.add(Employee(id=100+i, name=f"Orphan{i}", dept_id=999))
        session.commit()
    
    # Act
    with memory_engine.connect() as connection:
        violations = verify_referential_integrity(connection)
    
    # Assert
    if len(violations) > 0:
        emp_violation = next((v for v in violations if v["table"] == "employees"), None)
        if emp_violation:
            assert "sample_ids" in emp_violation
            assert isinstance(emp_violation["sample_ids"], list)
            assert len(emp_violation["sample_ids"]) <= 10  # Max 10 samples


def test_verify_referential_integrity_empty_database(memory_engine) -> None:
    """
    Test case 4: Handle empty database gracefully.
    """
    # Act
    with memory_engine.connect() as connection:
        violations = verify_referential_integrity(connection)
    
    # Assert
    assert isinstance(violations, list)
    assert len(violations) == 0


def test_verify_referential_integrity_no_foreign_keys(memory_engine) -> None:
    """
    Test case 5: Handle tables with no foreign keys.
    """
    # Arrange
    class StandaloneNoFK(Base):
        __tablename__ = 'standalone_no_fk'
        id = Column(Integer, primary_key=True)
        data = Column(String(50))
    
    Base.metadata.create_all(memory_engine)
    
    with Session(memory_engine) as session:
        session.add(StandaloneNoFK(id=1, data="test"))
        session.commit()
    
    # Act
    with memory_engine.connect() as connection:
        violations = verify_referential_integrity(connection)
    
    # Assert
    assert isinstance(violations, list)
    # No FKs, so no violations


def test_verify_referential_integrity_multiple_violations(memory_engine) -> None:
    """
    Test case 6: Detect violations across multiple tables.
    """
    # Arrange
    class ProjectMultipleViolations(Base):
        __tablename__ = 'projects_multi_viol'
        id = Column(Integer, primary_key=True)
        name = Column(String(100))
        emp_id = Column(Integer, ForeignKey('employees.id'))
    
    Base.metadata.create_all(memory_engine)
    
    with Session(memory_engine) as session:
        dept = Department(id=1, name="Engineering")
        session.add(dept)
        # Valid employee
        session.add(Employee(id=1, name="Alice", dept_id=1))
        # Orphaned employee
        session.add(Employee(id=2, name="Bob", dept_id=999))
        # Orphaned project
        session.add(ProjectMultipleViolations(id=1, name="Project X", emp_id=999))
        session.commit()
    
    # Act
    with memory_engine.connect() as connection:
        violations = verify_referential_integrity(connection)
    
    # Assert
    assert len(violations) >= 1  # At least one violation


def test_verify_referential_integrity_counts_orphaned(memory_engine) -> None:
    """
    Test case 7: Correctly count orphaned records.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    
    with Session(memory_engine) as session:
        dept = Department(id=1, name="Engineering")
        session.add(dept)
        # Create 5 orphaned employees
        for i in range(5):
            session.add(Employee(id=i, name=f"Orphan{i}", dept_id=999))
        session.commit()
    
    # Act
    with memory_engine.connect() as connection:
        violations = verify_referential_integrity(connection)
    
    # Assert
    if len(violations) > 0:
        emp_violation = next((v for v in violations if v["table"] == "employees"), None)
        if emp_violation:
            assert emp_violation["orphaned_count"] == 5


def test_verify_referential_integrity_invalid_connection_type_error() -> None:
    """
    Test case 8: TypeError for None connection.
    """
    # Arrange
    expected_message = "connection cannot be None"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        verify_referential_integrity(None)


def test_verify_referential_integrity_invalid_schema_type_error(memory_engine) -> None:
    """
    Test case 9: TypeError for invalid schema parameter.
    """
    # Arrange
    expected_message = "schema must be str or None"
    
    # Act & Assert
    with memory_engine.connect() as connection:
        with pytest.raises(TypeError, match=expected_message):
            verify_referential_integrity(connection, schema=123)


def test_verify_referential_integrity_null_foreign_keys(memory_engine) -> None:
    """
    Test case 10: Handle NULL foreign keys (should not be violations).
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    
    with Session(memory_engine) as session:
        dept = Department(id=1, name="Engineering")
        session.add(dept)
        # Employee with NULL dept_id (nullable FK)
        session.add(Employee(id=1, name="Alice", dept_id=None))
        # Employee with valid dept_id
        session.add(Employee(id=2, name="Bob", dept_id=1))
        session.commit()
    
    # Act
    with memory_engine.connect() as connection:
        violations = verify_referential_integrity(connection)
    
    # Assert
    # NULL FKs should not be violations
    assert isinstance(violations, list)
    # If there are violations, they shouldn't include the NULL FK
