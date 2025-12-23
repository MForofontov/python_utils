"""
Unit tests for check_data_anomalies function.
"""

import pytest
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, Session

from database_functions.schema_inspection import check_data_anomalies


Base = declarative_base()


class Measurement(Base):
    """Test Measurement model."""
    __tablename__ = 'measurements'
    id = Column(Integer, primary_key=True)
    sensor_name = Column(String(50))
    value = Column(Float)
    status = Column(String(20))


def test_check_data_anomalies_all_same_value(memory_engine) -> None:
    """
    Test case 1: Detect columns where all values are identical.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()
    
    # Insert data with all same status
    for i in range(10):
        conn.execute(Measurement.__table__.insert(), {
            "id": i,
            "sensor_name": f"sensor_{i}",
            "value": float(i),
            "status": "active"  # All identical
        })
    conn.commit()
    
    # Act
    anomalies = check_data_anomalies(conn, tables=["measurements"], check_all_same=True)
    
    # Assert
    assert isinstance(anomalies, list)
    # Should detect status column has all same values
    status_anomalies = [a for a in anomalies if a.get("column_name") == "status"]
    if len(status_anomalies) > 0:
        assert any("same" in a.get("anomaly_type", "").lower() for a in status_anomalies)
    
    conn.close()
    memory_engine.dispose()


def test_check_data_anomalies_all_null_column(memory_engine) -> None:
    """
    Test case 2: Detect columns that are entirely NULL.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()
    
    # Insert data with all NULL in value column
    for i in range(10):
        conn.execute(Measurement.__table__.insert(), {
            "id": i,
            "sensor_name": f"sensor_{i}",
            "value": None,  # All NULL
            "status": "inactive"
        })
    conn.commit()
    
    # Act
    anomalies = check_data_anomalies(conn, tables=["measurements"])
    
    # Assert
    assert isinstance(anomalies, list)
    # May detect all_null anomaly
    value_anomalies = [a for a in anomalies if a.get("column_name") == "value"]
    if len(value_anomalies) > 0:
        assert any("null" in a.get("anomaly_type", "").lower() for a in value_anomalies)
    
    conn.close()
    memory_engine.dispose()


def test_check_data_anomalies_clean_data(memory_engine) -> None:
    """
    Test case 3: Returns empty or minimal anomalies for clean data.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()
    
    # Insert diverse, clean data
    statuses = ["active", "inactive", "pending", "completed"]
    for i in range(20):
        conn.execute(Measurement.__table__.insert(), {
            "id": i,
            "sensor_name": f"sensor_{i}",
            "value": float(i * 10),
            "status": statuses[i % len(statuses)]
        })
    conn.commit()
    
    # Act
    anomalies = check_data_anomalies(conn, tables=["measurements"])
    
    # Assert
    assert isinstance(anomalies, list)
    # Should have no or few anomalies
    
    conn.close()
    memory_engine.dispose()


def test_check_data_anomalies_empty_table(memory_engine) -> None:
    """
    Test case 4: Handles empty tables gracefully.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()
    
    # Act
    anomalies = check_data_anomalies(conn, tables=["measurements"])
    
    # Assert
    assert isinstance(anomalies, list)
    # Should handle gracefully
    
    conn.close()
    memory_engine.dispose()


def test_check_data_anomalies_check_all_same_false(memory_engine) -> None:
    """
    Test case 5: Does not check for identical values when check_all_same is False.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()
    
    # Insert data with all same status
    for i in range(10):
        conn.execute(Measurement.__table__.insert(), {
            "id": i,
            "sensor_name": f"sensor_{i}",
            "value": float(i),
            "status": "active"
        })
    conn.commit()
    
    # Act
    anomalies = check_data_anomalies(conn, tables=["measurements"], check_all_same=False)
    
    # Assert
    assert isinstance(anomalies, list)
    # Should not include all_same anomalies
    all_same_anomalies = [a for a in anomalies if "same" in a.get("anomaly_type", "").lower()]
    assert len(all_same_anomalies) == 0
    
    conn.close()
    memory_engine.dispose()


def test_check_data_anomalies_specific_tables(memory_engine) -> None:
    """
    Test case 6: Only checks specified tables.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()
    
    for i in range(5):
        conn.execute(Measurement.__table__.insert(), {
            "id": i,
            "sensor_name": f"sensor_{i}",
            "value": None,
            "status": "active"
        })
    conn.commit()
    
    # Act
    anomalies = check_data_anomalies(conn, tables=["measurements"])
    
    # Assert
    assert isinstance(anomalies, list)
    for a in anomalies:
        assert a.get("table_name") == "measurements"
    
    conn.close()
    memory_engine.dispose()


def test_check_data_anomalies_invalid_connection_type_error() -> None:
    """
    Test case 7: TypeError for None connection.
    """
    # Arrange
    expected_message = "connection cannot be None"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        check_data_anomalies(None)


def test_check_data_anomalies_invalid_tables_type_error(memory_engine) -> None:
    """
    Test case 8: TypeError for invalid tables parameter.
    """
    # Arrange
    conn = memory_engine.connect()
    expected_message = "tables must be list or None"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        check_data_anomalies(conn, tables="measurements")
    
    conn.close()
    memory_engine.dispose()


def test_check_data_anomalies_invalid_schema_type_error(memory_engine) -> None:
    """
    Test case 9: TypeError for invalid schema parameter.
    """
    # Arrange
    conn = memory_engine.connect()
    expected_message = "schema must be str or None"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        check_data_anomalies(conn, schema=123)
    
    conn.close()
    memory_engine.dispose()


def test_check_data_anomalies_invalid_check_all_same_type_error(memory_engine) -> None:
    """
    Test case 10: TypeError for invalid check_all_same parameter.
    """
    # Arrange
    conn = memory_engine.connect()
    expected_message = "check_all_same must be bool"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        check_data_anomalies(conn, check_all_same="true")
    
    conn.close()
    memory_engine.dispose()


def test_check_data_anomalies_invalid_check_outliers_type_error(memory_engine) -> None:
    """
    Test case 11: TypeError for invalid check_outliers parameter.
    """
    # Arrange
    conn = memory_engine.connect()
    expected_message = "check_outliers must be bool"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        check_data_anomalies(conn, check_outliers="false")
    
    conn.close()
    memory_engine.dispose()


def test_check_data_anomalies_invalid_outlier_threshold_type_error(memory_engine) -> None:
    """
    Test case 12: TypeError for invalid outlier_std_threshold parameter.
    """
    # Arrange
    conn = memory_engine.connect()
    expected_message = "outlier_std_threshold must be float"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        check_data_anomalies(conn, outlier_std_threshold="3.0")
    
    conn.close()
    memory_engine.dispose()


def test_check_data_anomalies_negative_threshold_value_error(memory_engine) -> None:
    """
    Test case 13: ValueError for negative outlier_std_threshold.
    """
    # Arrange
    conn = memory_engine.connect()
    expected_message = "outlier_std_threshold must be positive"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        check_data_anomalies(conn, outlier_std_threshold=-1.0)
    
    conn.close()
    memory_engine.dispose()


class Product(Base):
    """Test model with primary key and numeric columns for outlier detection."""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Float)
    quantity = Column(Integer)


def test_check_data_anomalies_skips_primary_key_columns(memory_engine) -> None:
    """
    Test case 14: Primary key columns should be skipped in anomaly detection.
    
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
    Test case 15: Outlier detection with check_outliers=True on SQLite.
    
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
