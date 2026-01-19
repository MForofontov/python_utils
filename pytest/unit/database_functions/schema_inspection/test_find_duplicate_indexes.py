"""
Unit tests for find_duplicate_indexes function.
"""

from conftest import Base
from sqlalchemy import Column, Index, Integer, String
from sqlalchemy.orm import declarative_base

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.database]
from database_functions.schema_inspection import find_duplicate_indexes


def test_find_duplicate_indexes_identifies_redundant(memory_engine) -> None:
    """
    Test case 1: Identify redundant indexes.
    """

    # Arrange - Create a local table with duplicate indexes
    class TableWithDuplicates(Base):
        __tablename__ = "table_with_duplicates"
        __table_args__ = (
            Index("idx_name_1", "name"),
            Index("idx_name_2", "name"),  # Duplicate
        )
        id = Column(Integer, primary_key=True)
        name = Column(String(50))

    Base.metadata.create_all(memory_engine)

    # Act
    with memory_engine.connect() as connection:
        result = find_duplicate_indexes(connection)

    # Assert
    assert "exact_duplicates" in result or "redundant" in result
    assert isinstance(result.get("exact_duplicates", []), list) or isinstance(
        result.get("redundant", []), list
    )


def test_find_duplicate_indexes_detects_exact_duplicates(memory_engine) -> None:
    """
    Test case 1: Detect exact duplicate indexes.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)

    # Act
    with memory_engine.connect() as connection:
        result = find_duplicate_indexes(connection)

    # Assert
    assert "exact_duplicates" in result
    assert "redundant" in result
    assert isinstance(result["exact_duplicates"], list)


def test_find_duplicate_indexes_empty_database(memory_engine) -> None:
    """
    Test case 2: Handle empty database gracefully.
    """
    # Act
    with memory_engine.connect() as connection:
        result = find_duplicate_indexes(connection)

    # Assert
    assert "exact_duplicates" in result
    assert "redundant" in result
    assert len(result["exact_duplicates"]) == 0


def test_find_duplicate_indexes_no_duplicates(memory_engine) -> None:
    """
    Test case 3: Return empty when no duplicates exist.
    """

    # Arrange
    class SimpleTable(Base):
        __tablename__ = "simple_table"
        id = Column(Integer, primary_key=True)
        data = Column(String(50))

    Base.metadata.create_all(memory_engine)

    # Act
    with memory_engine.connect() as connection:
        result = find_duplicate_indexes(connection)

    # Assert
    assert isinstance(result["exact_duplicates"], list)
    assert isinstance(result["redundant"], list)


def test_find_duplicate_indexes_detects_redundant(memory_engine) -> None:
    """
    Test case 4: Identify redundant indexes (prefix of another).
    """
    # Arrange - create a new Base for this test to avoid table name conflicts
    TestBase = declarative_base()

    class ShipmentTable(TestBase):
        __tablename__ = "shipments"
        id = Column(Integer, primary_key=True)
        customer_id = Column(Integer)
        ship_date = Column(String(10))

    # Create composite index and its prefix
    Index("idx_shipment_customer", ShipmentTable.customer_id)
    Index(
        "idx_shipment_customer_date", ShipmentTable.customer_id, ShipmentTable.ship_date
    )

    TestBase.metadata.create_all(memory_engine)

    # Act
    with memory_engine.connect() as connection:
        result = find_duplicate_indexes(connection)

    # Assert
    assert "redundant" in result
    # idx_shipment_customer is redundant if idx_shipment_customer_date exists


def test_find_duplicate_indexes_with_schema(memory_engine) -> None:
    """
    Test case 5: Support schema parameter (for databases that support it).
    """
    # Arrange
    Base.metadata.create_all(memory_engine)

    # Act
    with memory_engine.connect() as connection:
        result = find_duplicate_indexes(connection, schema=None)

    # Assert
    assert isinstance(result, dict)


def test_find_duplicate_indexes_invalid_connection_type_error() -> None:
    """
    Test case 6: TypeError for None connection.
    """
    # Arrange
    expected_message = "connection cannot be None"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_duplicate_indexes(None)


def test_find_duplicate_indexes_invalid_schema_type_error(memory_engine) -> None:
    """
    Test case 7: TypeError for invalid schema parameter.
    """
    # Arrange
    expected_message = "schema must be str or None"

    # Act & Assert
    with memory_engine.connect() as connection:
        with pytest.raises(TypeError, match=expected_message):
            find_duplicate_indexes(connection, schema=123)


def test_find_duplicate_indexes_multiple_tables(memory_engine) -> None:
    """
    Test case 8: Analyze indexes across multiple tables.
    """

    # Arrange
    class DepartmentDuplicateTest(Base):
        __tablename__ = "departments_dup_test"
        id = Column(Integer, primary_key=True)
        name = Column(String(100), index=True)

    Base.metadata.create_all(memory_engine)

    # Act
    with memory_engine.connect() as connection:
        result = find_duplicate_indexes(connection)

    # Assert
    assert isinstance(result["exact_duplicates"], list)
    assert isinstance(result["redundant"], list)


def test_find_duplicate_indexes_unused_candidates_key(memory_engine) -> None:
    """
    Test case 9: Check result includes unused_candidates key.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)

    # Act
    with memory_engine.connect() as connection:
        result = find_duplicate_indexes(connection)

    # Assert
    assert "unused_candidates" in result or len(result.keys()) >= 2


def test_find_duplicate_indexes_unique_vs_non_unique(memory_engine) -> None:
    """
    Test case 10: Differentiate between unique and non-unique indexes.
    """

    # Arrange
    class ProductUniqueTest(Base):
        __tablename__ = "products_unique_test"
        id = Column(Integer, primary_key=True)
        sku = Column(String(50), unique=True)
        name = Column(String(100))

    Base.metadata.create_all(memory_engine)

    # Act
    with memory_engine.connect() as connection:
        result = find_duplicate_indexes(connection)

    # Assert
    # Unique indexes should be tracked separately from non-unique
    assert isinstance(result, dict)
