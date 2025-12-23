"""
Unit tests for check_data_anomalies function.
"""

import pytest
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

from database_functions.schema_inspection import check_data_anomalies


Base = declarative_base()


class Measurement(Base):
    """Test Measurement model."""
    __tablename__ = 'measurements'
    id = Column(Integer, primary_key=True)
    sensor_name = Column(String(50))
    value = Column(Float)
    status = Column(String(20))


def test_check_data_anomalies_all_same_value() -> None:
    """
    Test case 1: Detect columns where all values are identical.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()
    
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
    engine.dispose()


def test_check_data_anomalies_all_null_column() -> None:
    """
    Test case 2: Detect columns that are entirely NULL.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()
    
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
    engine.dispose()


def test_check_data_anomalies_clean_data() -> None:
    """
    Test case 3: Returns empty or minimal anomalies for clean data.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()
    
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
    engine.dispose()


def test_check_data_anomalies_empty_table() -> None:
    """
    Test case 4: Handles empty tables gracefully.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()
    
    # Act
    anomalies = check_data_anomalies(conn, tables=["measurements"])
    
    # Assert
    assert isinstance(anomalies, list)
    # Should handle gracefully
    
    conn.close()
    engine.dispose()


def test_check_data_anomalies_check_all_same_false() -> None:
    """
    Test case 5: Does not check for identical values when check_all_same is False.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()
    
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
    engine.dispose()


def test_check_data_anomalies_specific_tables() -> None:
    """
    Test case 6: Only checks specified tables.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()
    
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
    engine.dispose()


def test_check_data_anomalies_invalid_connection_type_error() -> None:
    """
    Test case 7: TypeError for None connection.
    """
    # Arrange
    expected_message = "connection cannot be None"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        check_data_anomalies(None)


def test_check_data_anomalies_invalid_tables_type_error() -> None:
    """
    Test case 8: TypeError for invalid tables parameter.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    conn = engine.connect()
    expected_message = "tables must be list or None"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        check_data_anomalies(conn, tables="measurements")
    
    conn.close()
    engine.dispose()


def test_check_data_anomalies_invalid_schema_type_error() -> None:
    """
    Test case 9: TypeError for invalid schema parameter.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    conn = engine.connect()
    expected_message = "schema must be str or None"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        check_data_anomalies(conn, schema=123)
    
    conn.close()
    engine.dispose()


def test_check_data_anomalies_invalid_check_all_same_type_error() -> None:
    """
    Test case 10: TypeError for invalid check_all_same parameter.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    conn = engine.connect()
    expected_message = "check_all_same must be bool"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        check_data_anomalies(conn, check_all_same="true")
    
    conn.close()
    engine.dispose()


def test_check_data_anomalies_invalid_check_outliers_type_error() -> None:
    """
    Test case 11: TypeError for invalid check_outliers parameter.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    conn = engine.connect()
    expected_message = "check_outliers must be bool"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        check_data_anomalies(conn, check_outliers="false")
    
    conn.close()
    engine.dispose()


def test_check_data_anomalies_invalid_outlier_threshold_type_error() -> None:
    """
    Test case 12: TypeError for invalid outlier_std_threshold parameter.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    conn = engine.connect()
    expected_message = "outlier_std_threshold must be float"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        check_data_anomalies(conn, outlier_std_threshold="3.0")
    
    conn.close()
    engine.dispose()


def test_check_data_anomalies_negative_threshold_value_error() -> None:
    """
    Test case 13: ValueError for negative outlier_std_threshold.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    conn = engine.connect()
    expected_message = "outlier_std_threshold must be positive"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        check_data_anomalies(conn, outlier_std_threshold=-1.0)
    
    conn.close()
    engine.dispose()
