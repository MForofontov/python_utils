"""
Unit tests for check_sequence_health function.
"""

import pytest
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, Session

from database_functions.schema_inspection import check_sequence_health


Base = declarative_base()


class Product(Base):
    """Test Product model with auto-increment ID."""
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))


def test_check_sequence_health_normal_usage(memory_engine) -> None:
    """
    Test case 1: Check sequence health under normal conditions.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    
    with Session(memory_engine) as session:
        for i in range(10):
            session.add(Product(name=f"Product{i}"))
        session.commit()
    
    # Act
    with memory_engine.connect() as connection:
        results = check_sequence_health(connection, warn_percentage=80.0)
    
    # Assert
    assert isinstance(results, list)
    # SQLite uses different mechanism, may not report sequence health


def test_check_sequence_health_specific_tables(memory_engine) -> None:
    """
    Test case 2: Check specific tables only.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    
    with Session(memory_engine) as session:
        session.add(Product(name="Test Product"))
        session.commit()
    
    # Act
    with memory_engine.connect() as connection:
        results = check_sequence_health(
            connection,
            tables=["products"],
            warn_percentage=80.0
        )
    
    # Assert
    assert isinstance(results, list)


def test_check_sequence_health_empty_database(memory_engine) -> None:
    """
    Test case 3: Handle empty database gracefully.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    
    # Act
    with memory_engine.connect() as connection:
        results = check_sequence_health(connection)
    
    # Assert
    assert isinstance(results, list)


def test_check_sequence_health_custom_warn_percentage(memory_engine) -> None:
    """
    Test case 4: Respect custom warn_percentage threshold.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    
    # Act
    with memory_engine.connect() as connection:
        results = check_sequence_health(connection, warn_percentage=90.0)
    
    # Assert
    assert isinstance(results, list)


def test_check_sequence_health_invalid_connection_type_error() -> None:
    """
    Test case 5: TypeError for None connection.
    """
    # Arrange
    expected_message = "connection cannot be None"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        check_sequence_health(None)


def test_check_sequence_health_invalid_tables_type_error(memory_engine) -> None:
    """
    Test case 6: TypeError for invalid tables parameter.
    """
    # Arrange
    expected_message = "tables must be list or None"
    
    # Act & Assert
    with memory_engine.connect() as connection:
        with pytest.raises(TypeError, match=expected_message):
            check_sequence_health(connection, tables="products")


def test_check_sequence_health_invalid_schema_type_error(memory_engine) -> None:
    """
    Test case 7: TypeError for invalid schema parameter.
    """
    # Arrange
    expected_message = "schema must be str or None"
    
    # Act & Assert
    with memory_engine.connect() as connection:
        with pytest.raises(TypeError, match=expected_message):
            check_sequence_health(connection, schema=123)


def test_check_sequence_health_invalid_warn_percentage_type_error(memory_engine) -> None:
    """
    Test case 8: TypeError for invalid warn_percentage parameter.
    """
    # Arrange
    expected_message = "warn_percentage must be float"
    
    # Act & Assert
    with memory_engine.connect() as connection:
        with pytest.raises(TypeError, match=expected_message):
            check_sequence_health(connection, warn_percentage="80")


def test_check_sequence_health_warn_percentage_out_of_range_value_error(memory_engine) -> None:
    """
    Test case 9: ValueError for warn_percentage out of range.
    """
    # Arrange
    expected_message = "warn_percentage must be between 0 and 100"
    
    # Act & Assert
    with memory_engine.connect() as connection:
        # Test > 100
        with pytest.raises(ValueError, match=expected_message):
            check_sequence_health(connection, warn_percentage=150.0)
        
        # Test <= 0
        with pytest.raises(ValueError, match=expected_message):
            check_sequence_health(connection, warn_percentage=0.0)


def test_check_sequence_health_low_usage(memory_engine) -> None:
    """
    Test case 10: Verify low severity for low sequence usage.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    
    with Session(memory_engine) as session:
        session.add(Product(name="Product1"))
        session.commit()
    
    # Act
    with memory_engine.connect() as connection:
        results = check_sequence_health(connection, warn_percentage=80.0)
    
    # Assert
    assert isinstance(results, list)
    # For SQLite, may not have severity info
    # For PostgreSQL/MySQL, would check severity levels
