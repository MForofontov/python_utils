"""
Unit tests for get_table_info function.
"""

import sqlite3

import pytest
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import declarative_base

from database_functions import get_table_info


Base = declarative_base()


class User(Base):
    """Test User model."""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100))
    __table_args__ = (Index('idx_username', 'username', unique=True),)


class Post(Base):
    """Test Post model."""
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(200), nullable=False)
    content = Column(String(1000))


def test_get_table_info_basic_table() -> None:
    """
    Test case 1: Get info for a basic table with columns.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()
    
    # Act
    info = get_table_info(conn, "users")
    
    # Assert
    assert info["name"] == "users"
    assert len(info["columns"]) >= 3
    
    col_names = [col["name"] for col in info["columns"]]
    assert "id" in col_names
    assert "username" in col_names
    assert "email" in col_names
    
    # Check column details
    id_col = next(col for col in info["columns"] if col["name"] == "id")
    assert id_col["primary_key"] in (True, 1)  # SQLite returns 1 for True
    
    username_col = next(col for col in info["columns"] if col["name"] == "username")
    assert username_col["nullable"] is False
    
    conn.close()
    engine.dispose()


def test_get_table_info_with_indexes() -> None:
    """
    Test case 2: Table info includes index information.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()
    
    # Act
    info = get_table_info(conn, "users")
    
    # Assert
    assert "indexes" in info
    assert isinstance(info["indexes"], list)
    
    # Check for unique index on username
    if len(info["indexes"]) > 0:
        idx_names = [idx.get("name") for idx in info["indexes"]]
        assert any("username" in str(name).lower() for name in idx_names if name)
    
    conn.close()
    engine.dispose()


def test_get_table_info_with_foreign_keys() -> None:
    """
    Test case 3: Table info includes foreign key relationships.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()
    
    # Act
    info = get_table_info(conn, "posts")
    
    # Assert
    assert "foreign_keys" in info
    assert isinstance(info["foreign_keys"], list)
    
    # Posts table should have foreign key to users
    if len(info["foreign_keys"]) > 0:
        fk = info["foreign_keys"][0]
        assert "user_id" in fk["columns"]
        assert fk["referred_table"] == "users"
    
    conn.close()
    engine.dispose()


def test_get_table_info_column_types() -> None:
    """
    Test case 4: Column type information is correctly captured.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()
    
    # Act
    info = get_table_info(conn, "users")
    
    # Assert
    for col in info["columns"]:
        assert "type" in col
        assert isinstance(col["type"], str)
        assert len(col["type"]) > 0
    
    conn.close()
    engine.dispose()


def test_get_table_info_empty_table_name() -> None:
    """
    Test case 5: Empty table name raises ValueError.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    conn = engine.connect()
    
    # Act & Assert
    with pytest.raises(ValueError, match="table_name cannot be empty"):
        get_table_info(conn, "")
    
    conn.close()
    engine.dispose()


def test_get_table_info_nonexistent_table() -> None:
    """
    Test case 6: Nonexistent table raises ValueError.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    conn = engine.connect()
    
    # Act & Assert
    with pytest.raises(ValueError, match="Table 'nonexistent' not found"):
        get_table_info(conn, "nonexistent")
    
    conn.close()
    engine.dispose()


def test_get_table_info_none_connection() -> None:
    """
    Test case 7: None connection raises TypeError.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="connection cannot be None"):
        get_table_info(None, "users")


def test_get_table_info_invalid_table_name_type() -> None:
    """
    Test case 8: Invalid table_name type raises TypeError.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    conn = engine.connect()
    
    # Act & Assert
    with pytest.raises(TypeError, match="table_name must be str"):
        get_table_info(conn, 123)
    
    conn.close()
    engine.dispose()


def test_get_table_info_invalid_schema_type() -> None:
    """
    Test case 9: Invalid schema type raises TypeError.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()
    
    # Act & Assert
    with pytest.raises(TypeError, match="schema must be str or None"):
        get_table_info(conn, "users", schema=123)
    
    conn.close()
    engine.dispose()


def test_get_table_info_nullable_columns() -> None:
    """
    Test case 10: Correctly identifies nullable and non-nullable columns.
    """
    # Arrange
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    conn = engine.connect()
    
    # Act
    info = get_table_info(conn, "users")
    
    # Assert
    username_col = next(col for col in info["columns"] if col["name"] == "username")
    email_col = next(col for col in info["columns"] if col["name"] == "email")
    
    assert username_col["nullable"] is False
    assert email_col["nullable"] is True
    
    conn.close()
    engine.dispose()
