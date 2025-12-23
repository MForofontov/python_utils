"""
Unit tests for detect_schema_drift function.
"""

import pytest
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base

from database_functions import detect_schema_drift


Base = declarative_base()


class User(Base):
    """User model for testing."""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(100))


class Product(Base):
    """Product model for testing."""
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))


def test_detect_schema_drift_no_drift() -> None:
    """
    Test case 1: No drift when actual schema matches expected.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()
    
    expected_schema = {
        "users": {
            "name": "users",
            "columns": [
                {"name": "id", "type": "INTEGER", "primary_key": True},
                {"name": "username", "type": "VARCHAR(50)"},
                {"name": "email", "type": "VARCHAR(100)"}
            ],
            "indexes": [],
            "foreign_keys": []
        },
        "products": {
            "name": "products",
            "columns": [
                {"name": "id", "type": "INTEGER", "primary_key": True},
                {"name": "name", "type": "VARCHAR(100)"}
            ],
            "indexes": [],
            "foreign_keys": []
        }
    }
    
    # Act
    result = detect_schema_drift(conn, expected_schema)
    
    # Assert
    assert result["has_drift"] is False
    assert len(result["missing_tables"]) == 0
    assert len(result["unexpected_tables"]) == 0
    assert len(result["table_diffs"]) == 0
    
    conn.close()
    engine.dispose()


def test_detect_schema_drift_missing_tables() -> None:
    """
    Test case 2: Missing tables are detected.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.tables['users'].create(engine)  # Only create users
    conn = engine.connect()
    
    expected_schema = {
        "users": {
            "name": "users",
            "columns": [
                {"name": "id", "type": "INTEGER"},
                {"name": "username", "type": "VARCHAR(50)"},
                {"name": "email", "type": "VARCHAR(100)"}
            ],
            "indexes": [],
            "foreign_keys": []
        },
        "products": {
            "name": "products",
            "columns": [
                {"name": "id", "type": "INTEGER"},
                {"name": "name", "type": "VARCHAR(100)"}
            ],
            "indexes": [],
            "foreign_keys": []
        }
    }
    
    # Act
    result = detect_schema_drift(conn, expected_schema)
    
    # Assert
    assert result["has_drift"] is True
    assert "products" in result["missing_tables"]
    
    conn.close()
    engine.dispose()


def test_detect_schema_drift_unexpected_tables() -> None:
    """
    Test case 3: Unexpected tables are detected.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()
    
    expected_schema = {
        "users": {
            "name": "users",
            "columns": [
                {"name": "id", "type": "INTEGER"},
                {"name": "username", "type": "VARCHAR(50)"},
                {"name": "email", "type": "VARCHAR(100)"}
            ],
            "indexes": [],
            "foreign_keys": []
        }
        # products table not expected
    }
    
    # Act
    result = detect_schema_drift(conn, expected_schema)
    
    # Assert
    assert result["has_drift"] is True
    assert "products" in result["unexpected_tables"]
    
    conn.close()
    engine.dispose()


def test_detect_schema_drift_missing_columns() -> None:
    """
    Test case 4: Missing columns in existing tables are detected.
    """
    # Arrange
    Base2 = declarative_base()
    
    class UserPartial(Base2):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        username = Column(String(50))
        # email column missing
    
    engine = create_engine("sqlite:///:memory:")
    Base2.metadata.create_all(engine)
    conn = engine.connect()
    
    expected_schema = {
        "users": {
            "name": "users",
            "columns": [
                {"name": "id", "type": "INTEGER"},
                {"name": "username", "type": "VARCHAR(50)"},
                {"name": "email", "type": "VARCHAR(100)"}
            ],
            "indexes": [],
            "foreign_keys": []
        }
    }
    
    # Act
    result = detect_schema_drift(conn, expected_schema)
    
    # Assert
    assert result["has_drift"] is True
    assert len(result["table_diffs"]) > 0
    table_diff = result["table_diffs"][0]
    assert table_diff["table"] == "users"
    assert "email" in table_diff["missing_columns"]
    
    conn.close()
    engine.dispose()


def test_detect_schema_drift_unexpected_columns() -> None:
    """
    Test case 5: Unexpected columns in existing tables are detected.
    """
    # Arrange
    Base2 = declarative_base()
    
    class UserExtended(Base2):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        username = Column(String(50))
        email = Column(String(100))
        phone = Column(String(20))  # Extra column
    
    engine = create_engine("sqlite:///:memory:")
    Base2.metadata.create_all(engine)
    conn = engine.connect()
    
    expected_schema = {
        "users": {
            "name": "users",
            "columns": [
                {"name": "id", "type": "INTEGER"},
                {"name": "username", "type": "VARCHAR(50)"},
                {"name": "email", "type": "VARCHAR(100)"}
            ],
            "indexes": [],
            "foreign_keys": []
        }
    }
    
    # Act
    result = detect_schema_drift(conn, expected_schema)
    
    # Assert
    assert result["has_drift"] is True
    assert len(result["table_diffs"]) > 0
    table_diff = result["table_diffs"][0]
    assert "phone" in table_diff["unexpected_columns"]
    
    conn.close()
    engine.dispose()


def test_detect_schema_drift_multiple_diffs() -> None:
    """
    Test case 6: Multiple types of drift detected simultaneously.
    """
    # Arrange
    Base2 = declarative_base()
    
    class UserPartial(Base2):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        username = Column(String(50))
        phone = Column(String(20))  # Extra column, email missing
    
    engine = create_engine("sqlite:///:memory:")
    Base2.metadata.create_all(engine)
    conn = engine.connect()
    
    expected_schema = {
        "users": {
            "name": "users",
            "columns": [
                {"name": "id", "type": "INTEGER"},
                {"name": "username", "type": "VARCHAR(50)"},
                {"name": "email", "type": "VARCHAR(100)"}
            ],
            "indexes": [],
            "foreign_keys": []
        },
        "products": {
            "name": "products",
            "columns": [
                {"name": "id", "type": "INTEGER"},
                {"name": "name", "type": "VARCHAR(100)"}
            ],
            "indexes": [],
            "foreign_keys": []
        }
    }
    
    # Act
    result = detect_schema_drift(conn, expected_schema)
    
    # Assert
    assert result["has_drift"] is True
    assert "products" in result["missing_tables"]
    assert len(result["table_diffs"]) > 0
    table_diff = result["table_diffs"][0]
    assert "email" in table_diff["missing_columns"]
    assert "phone" in table_diff["unexpected_columns"]
    
    conn.close()
    engine.dispose()


def test_detect_schema_drift_empty_expected_schema() -> None:
    """
    Test case 7: Empty expected schema shows all tables as unexpected.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()
    
    expected_schema = {}
    
    # Act
    result = detect_schema_drift(conn, expected_schema)
    
    # Assert
    assert result["has_drift"] is True
    assert "users" in result["unexpected_tables"]
    assert "products" in result["unexpected_tables"]
    
    conn.close()
    engine.dispose()


def test_detect_schema_drift_none_connection() -> None:
    """
    Test case 8: None connection raises TypeError.
    """
    # Arrange
    expected_schema = {"users": ["id", "username"]}
    
    # Act & Assert
    with pytest.raises(TypeError, match="connection cannot be None"):
        detect_schema_drift(None, expected_schema)


def test_detect_schema_drift_invalid_expected_schema_type() -> None:
    """
    Test case 9: Invalid expected_schema type raises TypeError.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    conn = engine.connect()
    
    # Act & Assert
    with pytest.raises(TypeError, match="expected_schema must be dict"):
        detect_schema_drift(conn, "not a dict")
    
    conn.close()
    engine.dispose()


def test_detect_schema_drift_invalid_schema_type() -> None:
    """
    Test case 10: Invalid schema parameter type raises TypeError.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    conn = engine.connect()
    expected_schema = {"users": ["id", "username"]}
    
    # Act & Assert
    with pytest.raises(TypeError, match="schema must be str or None"):
        detect_schema_drift(conn, expected_schema, schema=123)
    
    conn.close()
    engine.dispose()
