"""
Unit tests for detect_schema_drift function.
"""

import pytest
from sqlalchemy import Column, Integer, String
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base

from database_functions import detect_schema_drift
from conftest import Base, User, Product


@pytest.fixture
def schema_dict() -> dict:
    """
    Local fixture providing expected schema for drift detection tests.
    
    Only used by 2 tests in this file, so kept local rather than in conftest.py.
    """
    return {
        "users": {
            "name": "users",
            "columns": [
                {"name": "id", "type": "INTEGER", "primary_key": True},
                {"name": "username", "type": "VARCHAR(50)"},
                {"name": "email", "type": "VARCHAR(100)"},
                {"name": "role", "type": "VARCHAR(20)"},
                {"name": "status", "type": "VARCHAR(10)"},
                {"name": "balance", "type": "FLOAT"}
            ],
            "indexes": [],
            "foreign_keys": []
        },
        "products": {
            "name": "products",
            "columns": [
                {"name": "id", "type": "INTEGER", "primary_key": True},
                {"name": "sku", "type": "VARCHAR(500)"},
                {"name": "name", "type": "VARCHAR(100)"},
                {"name": "description", "type": "VARCHAR(500)"},
                {"name": "price", "type": "FLOAT"},
                {"name": "status", "type": "VARCHAR(20)"}
            ],
            "indexes": [],
            "foreign_keys": []
        }
    }


def test_detect_schema_drift_no_drift(memory_engine: Engine) -> None:
    """
    Test case 1: No drift when actual schema matches expected.
    """
    # Arrange - Create only User and Product tables
    User.__table__.create(memory_engine)
    Product.__table__.create(memory_engine)
    conn = memory_engine.connect()
    
    expected_schema = {
        "users": {
            "name": "users",
            "columns": [
                {"name": "id", "type": "INTEGER", "primary_key": True},
                {"name": "username", "type": "VARCHAR(50)"},
                {"name": "email", "type": "VARCHAR(100)"},
                {"name": "first_name", "type": "VARCHAR(50)"},
                {"name": "last_name", "type": "VARCHAR(50)"},
                {"name": "role", "type": "VARCHAR(20)"},
                {"name": "status", "type": "VARCHAR(10)"},
                {"name": "age", "type": "INTEGER"},
                {"name": "city", "type": "VARCHAR(50)"},
                {"name": "balance", "type": "FLOAT"}
            ],
            "indexes": [],
            "foreign_keys": []
        },
        "products": {
            "name": "products",
            "columns": [
                {"name": "id", "type": "INTEGER", "primary_key": True},
                {"name": "sku", "type": "VARCHAR(500)"},
                {"name": "name", "type": "VARCHAR(100)"},
                {"name": "category", "type": "VARCHAR(50)"},
                {"name": "description", "type": "VARCHAR(500)"},
                {"name": "title", "type": "VARCHAR(200)"},
                {"name": "content", "type": "TEXT"},
                {"name": "price", "type": "FLOAT"},
                {"name": "quantity", "type": "INTEGER"},
                {"name": "status", "type": "VARCHAR(20)"}
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


def test_detect_schema_drift_missing_tables(memory_engine: Engine, schema_dict: dict) -> None:
    """
    Test case 2: Missing tables are detected.
    """
    # Arrange
    Base.metadata.tables['users'].create(memory_engine)  # Only create users
    conn = memory_engine.connect()
    
    # Act
    result = detect_schema_drift(conn, schema_dict)
    
    # Assert
    assert result["has_drift"] is True
    assert "products" in result["missing_tables"]
    
    conn.close()


def test_detect_schema_drift_unexpected_tables(memory_engine: Engine) -> None:
    """
    Test case 3: Unexpected tables are detected.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()
    
    expected_schema = {
        "users": {
            "name": "users",
            "columns": [
                {"name": "id", "type": "INTEGER"},
                {"name": "username", "type": "VARCHAR(50)"},
                {"name": "email", "type": "VARCHAR(100)"},
                {"name": "role", "type": "VARCHAR(20)"},
                {"name": "status", "type": "VARCHAR(10)"},
                {"name": "score", "type": "FLOAT"}
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


def test_detect_schema_drift_missing_columns(memory_engine: Engine) -> None:
    """
    Test case 4: Missing columns in existing tables are detected.
    """
    # Arrange
    Base2 = declarative_base()
    
    class UserPartial(Base2):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        username = Column(String(50))
        # email and other columns missing
    
    _ = UserPartial  # Suppress unused warning - class is used via Base2.metadata
    Base2.metadata.create_all(memory_engine)
    conn = memory_engine.connect()
    
    expected_schema = {
        "users": {
            "name": "users",
            "columns": [
                {"name": "id", "type": "INTEGER"},
                {"name": "username", "type": "VARCHAR(50)"},
                {"name": "email", "type": "VARCHAR(100)"},
                {"name": "role", "type": "VARCHAR(20)"}
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
    assert "role" in table_diff["missing_columns"]
    
    conn.close()


def test_detect_schema_drift_unexpected_columns(memory_engine: Engine) -> None:
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
    
    _ = UserExtended  # Suppress unused warning - class is used via Base2.metadata
    Base2.metadata.create_all(memory_engine)
    conn = memory_engine.connect()
    
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


def test_detect_schema_drift_multiple_diffs(memory_engine: Engine, schema_dict: dict) -> None:
    """
    Test case 6: Multiple types of drift detected simultaneously.
    """
    # Arrange
    Base2 = declarative_base()
    
    class UserPartial(Base2):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        username = Column(String(50))
        phone = Column(String(20))  # Extra column, other columns missing
    
    _ = UserPartial  # Suppress unused warning - class is used via Base2.metadata
    Base2.metadata.create_all(memory_engine)
    conn = memory_engine.connect()
    
    # Act
    result = detect_schema_drift(conn, schema_dict)
    
    # Assert
    assert result["has_drift"] is True
    assert "products" in result["missing_tables"]
    assert len(result["table_diffs"]) > 0
    table_diff = result["table_diffs"][0]
    assert "email" in table_diff["missing_columns"]
    assert "phone" in table_diff["unexpected_columns"]
    
    conn.close()


def test_detect_schema_drift_empty_expected_schema(memory_engine: Engine) -> None:
    """
    Test case 7: Empty expected schema shows all tables as unexpected.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()
    
    expected_schema = {}
    
    # Act
    result = detect_schema_drift(conn, expected_schema)
    
    # Assert
    assert result["has_drift"] is True
    assert "users" in result["unexpected_tables"]
    assert "products" in result["unexpected_tables"]
    
    conn.close()


def test_detect_schema_drift_none_connection() -> None:
    """
    Test case 8: None connection raises TypeError.
    """
    # Arrange
    expected_schema = {"users": ["id", "username"]}
    
    # Act & Assert
    with pytest.raises(TypeError, match="connection cannot be None"):
        detect_schema_drift(None, expected_schema)


def test_detect_schema_drift_invalid_expected_schema_type(memory_engine: Engine) -> None:
    """
    Test case 9: Invalid expected_schema type raises TypeError.
    """
    # Arrange
    conn = memory_engine.connect()
    
    # Act & Assert
    with pytest.raises(TypeError, match="expected_schema must be dict"):
        detect_schema_drift(conn, "not a dict")
    
    conn.close()


def test_detect_schema_drift_invalid_schema_type(memory_engine: Engine) -> None:
    """
    Test case 10: Invalid schema parameter type raises TypeError.
    """
    # Arrange
    conn = memory_engine.connect()
    expected_schema = {"users": ["id", "username"]}
    
    # Act & Assert
    with pytest.raises(TypeError, match="schema must be str or None"):
        detect_schema_drift(conn, expected_schema, schema=123)
    
    conn.close()
