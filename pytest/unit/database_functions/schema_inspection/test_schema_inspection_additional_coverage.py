"""
Additional test cases to improve coverage for schema inspection functions.

Test case 1: check_data_anomalies - Primary key columns should be skipped
Test case 2: check_data_anomalies - Outlier detection with check_outliers=True (SQLite limitation)
Test case 3: find_duplicate_rows - Multiple duplicate groups with different counts
Test case 4: find_unused_columns - Mixed columns (some used, some unused)
"""

import pytest
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, Session

from database_functions.schema_inspection.check_data_anomalies import check_data_anomalies
from database_functions.schema_inspection.find_duplicate_rows import find_duplicate_rows
from database_functions.schema_inspection.find_unused_columns import find_unused_columns

Base = declarative_base()


class Product(Base):
    """Test model with primary key and numeric columns for outlier detection."""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Float)
    quantity = Column(Integer)


class DataTable(Base):
    """Test model with mixed NULL/non-NULL columns."""
    __tablename__ = "data_table"

    id = Column(Integer, primary_key=True)
    used_column = Column(String(50))
    mostly_null_column = Column(String(50))
    completely_null_column = Column(String(50))


class PersonTable(Base):
    """Test model for duplicate detection with multiple groups."""
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    age = Column(Integer)
    city = Column(String(50))


def test_check_data_anomalies_skips_primary_key_columns(memory_engine) -> None:
    """
    Test case 1: Primary key columns should be skipped in anomaly detection.
    
    Verifies that columns marked as primary keys are not checked for anomalies,
    even if they have patterns that would normally be flagged.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)

    with Session(memory_engine) as session:
        # All products have same ID pattern but IDs should be skipped
        products = [
            Product(id=1, name="Widget", price=10.0, quantity=100),
            Product(id=2, name="Gadget", price=10.0, quantity=100),
            Product(id=3, name="Device", price=10.0, quantity=100),
        ]
        session.add_all(products)
        session.commit()

    # Act
    with memory_engine.connect() as connection:
        anomalies = check_data_anomalies(connection, check_all_same=True, check_outliers=False)

    # Assert
    # Should detect all-same values in price and quantity, but NOT in id (primary key)
    anomaly_columns = {(a["table_name"], a["column_name"]) for a in anomalies}
    assert ("products", "id") not in anomaly_columns, "Primary key should be skipped"
    assert ("products", "price") in anomaly_columns, "Price column should be flagged"
    assert ("products", "quantity") in anomaly_columns, "Quantity column should be flagged"


def test_check_data_anomalies_outlier_detection_sqlite_limitation(memory_engine) -> None:
    """
    Test case 2: Outlier detection with check_outliers=True on SQLite.
    
    Tests that the outlier detection runs without errors even though SQLite
    doesn't support the stddev function. This tests the error handling path
    when statistical functions are not available.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)

    with Session(memory_engine) as session:
        # Create data with clear outliers
        products = [
            Product(id=i, name=f"Product{i}", price=10.0, quantity=100)
            for i in range(1, 21)
        ]
        products.extend([
            Product(id=21, name="Outlier1", price=1000.0, quantity=100),
            Product(id=22, name="Outlier2", price=2000.0, quantity=100),
        ])
        session.add_all(products)
        session.commit()

    # Act
    with memory_engine.connect() as connection:
        anomalies = check_data_anomalies(
            connection,
            check_all_same=False,
            check_outliers=True,
            outlier_std_threshold=3.0,
        )

    # Assert
    # SQLite doesn't support stddev, so no outliers will be detected
    # But the function should execute without error
    assert isinstance(anomalies, list), "Function should return a list"
    # On databases with stddev support, this would detect outliers


def test_find_duplicate_rows_multiple_duplicate_groups(memory_engine) -> None:
    """
    Test case 3: Multiple groups of duplicates with different counts.
    
    Tests that find_duplicate_rows correctly identifies multiple distinct
    groups of duplicate rows and returns them sorted by duplicate count.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)

    with Session(memory_engine) as session:
        # Create multiple duplicate groups
        # Group 1: "John Doe" appears 5 times
        persons = [
            PersonTable(id=i, first_name="John", last_name="Doe", age=30, city="NYC")
            for i in range(1, 6)
        ]
        # Group 2: "Jane Smith" appears 3 times
        persons.extend([
            PersonTable(id=i, first_name="Jane", last_name="Smith", age=25, city="LA")
            for i in range(6, 9)
        ])
        # Group 3: "Bob Wilson" appears 2 times
        persons.extend([
            PersonTable(id=9, first_name="Bob", last_name="Wilson", age=35, city="SF"),
            PersonTable(id=10, first_name="Bob", last_name="Wilson", age=35, city="SF"),
        ])
        # Unique person
        persons.append(
            PersonTable(id=11, first_name="Alice", last_name="Brown", age=28, city="Boston")
        )
        session.add_all(persons)
        session.commit()

    # Act
    with memory_engine.connect() as connection:
        duplicates = find_duplicate_rows(
            connection,
            table_name="persons",
            columns=["first_name", "last_name", "age", "city"],
            min_duplicates=2,
        )

    # Assert
    assert len(duplicates) == 3, "Should find 3 groups of duplicates"
    
    # Check sorted order (highest count first) - key is "count" not "duplicate_count"
    assert duplicates[0]["count"] >= duplicates[1]["count"]
    assert duplicates[1]["count"] >= duplicates[2]["count"]
    
    # Verify the groups - values are directly in the dict, not nested
    john_doe = next((d for d in duplicates if d["first_name"] == "John"), None)
    assert john_doe is not None
    assert john_doe["count"] == 5
    
    jane_smith = next((d for d in duplicates if d["first_name"] == "Jane"), None)
    assert jane_smith is not None
    assert jane_smith["count"] == 3
    
    bob_wilson = next((d for d in duplicates if d["first_name"] == "Bob"), None)
    assert bob_wilson is not None
    assert bob_wilson["count"] == 2


def test_find_unused_columns_mixed_usage(memory_engine) -> None:
    """
    Test case 4: Mixed columns - some used, some unused.
    
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


__all__ = [
    'test_check_data_anomalies_skips_primary_key_columns',
    'test_check_data_anomalies_outlier_detection_sqlite_limitation',
    'test_find_duplicate_rows_multiple_duplicate_groups',
    'test_find_unused_columns_mixed_usage',
]
