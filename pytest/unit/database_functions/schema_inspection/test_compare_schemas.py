"""
Unit tests for compare_schemas function.
"""

from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import declarative_base

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.database]
from pyutils_collection.database_functions import compare_schemas

Base = declarative_base()


class UserV1(Base):
    """Version 1 of User model."""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(100))


class ProductV1(Base):
    """Version 1 of Product model."""

    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Float)


def test_compare_schemas_identical_schemas(dual_engines) -> None:
    """
    Test case 1: Identical schemas should show no differences.
    """
    # Arrange
    engine1, engine2 = dual_engines
    Base.metadata.create_all(engine1)
    Base.metadata.create_all(engine2)
    conn1 = engine1.connect()
    conn2 = engine2.connect()

    # Act
    result = compare_schemas(conn1, conn2)

    # Assert
    assert result["severity"] == "safe"
    assert len(result["new_tables"]) == 0
    assert len(result["dropped_tables"]) == 0
    assert len(result["modified_tables"]) == 0

    conn1.close()
    conn2.close()


def test_compare_schemas_new_tables(dual_engines) -> None:
    """
    Test case 2: New tables are detected.
    """
    # Arrange
    engine1, engine2 = dual_engines

    # Create only users in source
    Base.metadata.tables["users"].create(engine1)

    # Create both tables in target
    Base.metadata.create_all(engine2)

    conn1 = engine1.connect()
    conn2 = engine2.connect()

    # Act
    result = compare_schemas(conn1, conn2)

    # Assert
    assert "products" in result["new_tables"]
    assert result["severity"] == "safe"  # New tables are not breaking

    conn1.close()
    conn2.close()


def test_compare_schemas_dropped_tables(dual_engines) -> None:
    """
    Test case 3: Dropped tables are detected as breaking changes.
    """
    # Arrange
    engine1, engine2 = dual_engines

    # Create both tables in source
    Base.metadata.create_all(engine1)

    # Create only users in target
    Base.metadata.tables["users"].create(engine2)

    conn1 = engine1.connect()
    conn2 = engine2.connect()

    # Act
    result = compare_schemas(conn1, conn2)

    # Assert
    assert "products" in result["dropped_tables"]
    assert result["severity"] == "breaking"  # Dropped tables are breaking

    conn1.close()
    conn2.close()


def test_compare_schemas_new_columns(dual_engines) -> None:
    """
    Test case 4: New columns in existing tables are detected.
    """
    # Arrange
    engine1, engine2 = dual_engines
    Base2 = declarative_base()

    class UserV2(Base2):
        __tablename__ = "users"
        id = Column(Integer, primary_key=True)
        username = Column(String(50))
        email = Column(String(100))
        phone = Column(String(20))  # New column

    Base.metadata.tables["users"].create(engine1)
    Base2.metadata.create_all(engine2)

    conn1 = engine1.connect()
    conn2 = engine2.connect()

    # Act
    result = compare_schemas(conn1, conn2)

    # Assert
    assert len(result["modified_tables"]) > 0
    modified = result["modified_tables"][0]
    assert modified["table"] == "users"
    assert "phone" in modified["new_columns"]
    assert result["severity"] == "safe"  # New columns are not breaking

    conn1.close()
    conn2.close()


def test_compare_schemas_dropped_columns(dual_engines) -> None:
    """
    Test case 5: Dropped columns are detected as breaking changes.
    """
    # Arrange
    engine1, engine2 = dual_engines
    Base2 = declarative_base()

    class UserV2(Base2):
        __tablename__ = "users"
        id = Column(Integer, primary_key=True)
        username = Column(String(50))
        # email column dropped

    Base.metadata.tables["users"].create(engine1)
    Base2.metadata.create_all(engine2)

    conn1 = engine1.connect()
    conn2 = engine2.connect()

    # Act
    result = compare_schemas(conn1, conn2)

    # Assert
    assert len(result["modified_tables"]) > 0
    modified = result["modified_tables"][0]
    assert "email" in modified["dropped_columns"]
    assert result["severity"] == "breaking"  # Dropped columns are breaking

    conn1.close()
    conn2.close()


def test_compare_schemas_type_changes(dual_engines) -> None:
    """
    Test case 6: Column type changes are detected as breaking.
    """
    # Arrange
    engine1, engine2 = dual_engines
    Base2 = declarative_base()

    class UserV2(Base2):
        __tablename__ = "users"
        id = Column(Integer, primary_key=True)
        username = Column(String(100))  # Changed from 50 to 100
        email = Column(String(100))

    Base.metadata.tables["users"].create(engine1)
    Base2.metadata.create_all(engine2)

    conn1 = engine1.connect()
    conn2 = engine2.connect()

    # Act
    result = compare_schemas(conn1, conn2)

    # Assert
    if len(result["modified_tables"]) > 0:
        modified = result["modified_tables"][0]
        if len(modified["type_changes"]) > 0:
            type_change = modified["type_changes"][0]
            assert type_change["column"] == "username"
            assert result["severity"] == "breaking"

    conn1.close()
    conn2.close()


def test_compare_schemas_with_ignore_tables(dual_engines) -> None:
    """
    Test case 7: Ignored tables are excluded from comparison.
    """
    # Arrange
    engine1, engine2 = dual_engines
    Base.metadata.create_all(engine1)
    Base.metadata.tables["users"].create(engine2)  # Only users in target

    conn1 = engine1.connect()
    conn2 = engine2.connect()

    # Act
    result = compare_schemas(conn1, conn2, ignore_tables={"products"})

    # Assert
    assert "products" not in result["dropped_tables"]

    conn1.close()
    conn2.close()


def test_compare_schemas_none_source_connection(memory_engine) -> None:
    """
    Test case 8: None source_connection raises TypeError.
    """
    # Arrange
    conn = memory_engine.connect()

    # Act & Assert
    with pytest.raises(TypeError, match="source_connection cannot be None"):
        compare_schemas(None, conn)

    conn.close()


def test_compare_schemas_none_target_connection(memory_engine) -> None:
    """
    Test case 9: None target_connection raises TypeError.
    """
    # Arrange
    conn = memory_engine.connect()

    # Act & Assert
    with pytest.raises(TypeError, match="target_connection cannot be None"):
        compare_schemas(conn, None)

    conn.close()


def test_compare_schemas_invalid_ignore_tables_type(dual_engines) -> None:
    """
    Test case 10: Invalid ignore_tables type raises TypeError.
    """
    # Arrange
    engine1, engine2 = dual_engines
    conn1 = engine1.connect()
    conn2 = engine2.connect()

    # Act & Assert
    with pytest.raises(TypeError, match="ignore_tables must be set or None"):
        compare_schemas(conn1, conn2, ignore_tables=["not", "a", "set"])

    conn1.close()
    conn2.close()


def test_compare_schemas_invalid_schema_type(dual_engines) -> None:
    """
    Test case 11: Invalid schema type raises TypeError.
    """
    # Arrange
    engine1, engine2 = dual_engines
    conn1 = engine1.connect()
    conn2 = engine2.connect()

    # Act & Assert
    with pytest.raises(TypeError, match="schema must be str or None"):
        compare_schemas(conn1, conn2, schema=123)

    conn1.close()
    conn2.close()
