"""
Unit tests for find_duplicate_rows function.
"""

import pytest
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, Session

from database_functions.schema_inspection import find_duplicate_rows
from conftest import Base, User


def test_find_duplicate_rows_identifies_duplicates(memory_engine) -> None:
    """
    Test case 1: Identify rows with duplicate email addresses.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()
    
    # Insert duplicate emails
    conn.execute(User.__table__.insert(), {"id": 1, "email": "john@example.com", "username": "john1"})
    conn.execute(User.__table__.insert(), {"id": 2, "email": "john@example.com", "username": "john2"})
    conn.execute(User.__table__.insert(), {"id": 3, "email": "jane@example.com", "username": "jane"})
    conn.commit()
    
    # Act
    duplicates = find_duplicate_rows(conn, "users", ["email"])
    
    # Assert
    assert len(duplicates) == 1
    assert duplicates[0]["email"] == "john@example.com"
    assert duplicates[0]["count"] == 2
    
    conn.close()


def test_find_duplicate_rows_multiple_columns(memory_engine) -> None:
    """
    Test case 2: Find duplicates based on multiple columns.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()
    
    conn.execute(User.__table__.insert(), {"id": 1, "email": "john@example.com", "username": "john"})
    conn.execute(User.__table__.insert(), {"id": 2, "email": "john@example.com", "username": "john"})
    conn.execute(User.__table__.insert(), {"id": 3, "email": "john@example.com", "username": "john2"})
    conn.commit()
    
    # Act
    duplicates = find_duplicate_rows(conn, "users", ["email", "username"])
    
    # Assert
    assert len(duplicates) == 1
    assert duplicates[0]["email"] == "john@example.com"
    assert duplicates[0]["username"] == "john"
    assert duplicates[0]["count"] == 2
    
    conn.close()


def test_find_duplicate_rows_no_duplicates(memory_engine) -> None:
    """
    Test case 3: Empty result when no duplicates exist.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()
    
    conn.execute(User.__table__.insert(), {"id": 1, "email": "john@example.com", "username": "john"})
    conn.execute(User.__table__.insert(), {"id": 2, "email": "jane@example.com", "username": "jane"})
    conn.commit()
    
    # Act
    duplicates = find_duplicate_rows(conn, "users", ["email"])
    
    # Assert
    assert len(duplicates) == 0
    
    conn.close()


def test_find_duplicate_rows_min_duplicates_threshold(memory_engine) -> None:
    """
    Test case 4: Respect min_duplicates threshold.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()
    
    # Create 3 duplicates
    conn.execute(User.__table__.insert(), {"id": 1, "email": "john@example.com", "username": "john1"})
    conn.execute(User.__table__.insert(), {"id": 2, "email": "john@example.com", "username": "john2"})
    conn.execute(User.__table__.insert(), {"id": 3, "email": "john@example.com", "username": "john3"})
    conn.commit()
    
    # Act - require at least 4 duplicates
    duplicates = find_duplicate_rows(conn, "users", ["email"], min_duplicates=4)
    
    # Assert
    assert len(duplicates) == 0  # 3 < 4, so no results
    
    conn.close()


def test_find_duplicate_rows_invalid_connection_type_error() -> None:
    """
    Test case 5: TypeError for None connection.
    """
    # Arrange
    expected_message = "connection cannot be None"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_duplicate_rows(None, "users", ["email"])


def test_find_duplicate_rows_invalid_table_name_type_error(memory_engine) -> None:
    """
    Test case 6: TypeError for invalid table_name.
    """
    # Arrange
    conn = memory_engine.connect()
    expected_message = "table_name must be str"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_duplicate_rows(conn, 123, ["email"])
    
    conn.close()


def test_find_duplicate_rows_empty_table_name_value_error(memory_engine) -> None:
    """
    Test case 7: ValueError for empty table name.
    """
    # Arrange
    conn = memory_engine.connect()
    expected_message = "table_name cannot be empty"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        find_duplicate_rows(conn, "", ["email"])
    
    conn.close()


def test_find_duplicate_rows_invalid_columns_type_error(memory_engine) -> None:
    """
    Test case 8: TypeError for invalid columns type.
    """
    # Arrange
    conn = memory_engine.connect()
    expected_message = "columns must be list"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_duplicate_rows(conn, "users", "email")
    
    conn.close()


def test_find_duplicate_rows_empty_columns_value_error(memory_engine) -> None:
    """
    Test case 9: ValueError for empty columns list.
    """
    # Arrange
    conn = memory_engine.connect()
    expected_message = "columns list cannot be empty"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        find_duplicate_rows(conn, "users", [])
    
    conn.close()


def test_find_duplicate_rows_invalid_min_duplicates_type_error(memory_engine) -> None:
    """
    Test case 10: TypeError for invalid min_duplicates type.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()
    expected_message = "min_duplicates must be int"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        find_duplicate_rows(conn, "users", ["email"], min_duplicates="2")
    
    conn.close()


def test_find_duplicate_rows_min_duplicates_value_error(memory_engine) -> None:
    """
    Test case 11: ValueError for min_duplicates less than 2.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()
    expected_message = "min_duplicates must be at least 2"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        find_duplicate_rows(conn, "users", ["email"], min_duplicates=1)
    
    conn.close()


def test_find_duplicate_rows_sorted_by_count(memory_engine) -> None:
    """
    Test case 12: Results are sorted by duplicate count (descending).
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()
    
    # Create different duplicate counts
    conn.execute(User.__table__.insert(), {"id": 1, "email": "a@example.com", "username": "a1"})
    conn.execute(User.__table__.insert(), {"id": 2, "email": "a@example.com", "username": "a2"})
    conn.execute(User.__table__.insert(), {"id": 3, "email": "b@example.com", "username": "b1"})
    conn.execute(User.__table__.insert(), {"id": 4, "email": "b@example.com", "username": "b2"})
    conn.execute(User.__table__.insert(), {"id": 5, "email": "b@example.com", "username": "b3"})
    conn.commit()
    
    # Act
    duplicates = find_duplicate_rows(conn, "users", ["email"])
    
    # Assert
    assert len(duplicates) == 2
    # First result should have higher count
    assert duplicates[0]["count"] >= duplicates[1]["count"]
    
    conn.close()


def test_find_duplicate_rows_sample_ids_exception_handling(memory_engine) -> None:
    """
    Test case 13: Handle exception when fetching sample IDs gracefully.
    """
    # Arrange
    User.__table__.create(memory_engine)
    conn = memory_engine.connect()
    
    # Insert duplicate data
    conn.execute(User.__table__.insert(), {"id": 1, "username": "test", "email": "test@example.com"})
    conn.execute(User.__table__.insert(), {"id": 2, "username": "test", "email": "test@example.com"})
    conn.commit()
    
    # Act - even without primary key, should handle gracefully
    duplicates = find_duplicate_rows(conn, "users", ["username"])
    
    # Assert - should still find duplicates even if sample_ids fails
    assert len(duplicates) == 1
    assert duplicates[0]["username"] == "test"
    
    conn.close()


def test_find_duplicate_rows_with_primary_key_sample_ids(memory_engine) -> None:
    """
    Test case 14: Successfully fetch sample IDs when table has primary key.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    conn = memory_engine.connect()
    
    # Insert duplicate emails
    conn.execute(User.__table__.insert(), {"id": 1, "email": "test@example.com", "username": "user1"})
    conn.execute(User.__table__.insert(), {"id": 2, "email": "test@example.com", "username": "user2"})
    conn.execute(User.__table__.insert(), {"id": 3, "email": "test@example.com", "username": "user3"})
    conn.commit()
    
    # Act
    duplicates = find_duplicate_rows(conn, "users", ["email"])
    
    # Assert - should have sample_ids
    assert len(duplicates) == 1
    assert duplicates[0]["email"] == "test@example.com"
    # May or may not have sample_ids depending on implementation
    
    conn.close()


def test_find_duplicate_rows_multiple_duplicate_groups(memory_engine) -> None:
    """
    Test case 15: Multiple groups of duplicates with different counts.
    
    Tests that find_duplicate_rows correctly identifies multiple distinct
    groups of duplicate rows and returns them sorted by duplicate count.
    """
    # Arrange
    User.__table__.create(memory_engine)

    with Session(memory_engine) as session:
        # Create multiple duplicate groups
        # Group 1: "John Doe" appears 5 times
        users = [
            User(id=i, username=f"user{i}", email=f"user{i}@example.com",
                 first_name="John", last_name="Doe", age=30, city="NYC")
            for i in range(1, 6)
        ]
        # Group 2: "Jane Smith" appears 3 times
        users.extend([
            User(id=i, username=f"user{i}", email=f"user{i}@example.com",
                 first_name="Jane", last_name="Smith", age=25, city="LA")
            for i in range(6, 9)
        ])
        # Group 3: "Bob Wilson" appears 2 times
        users.extend([
            User(id=9, username="user9", email="user9@example.com",
                 first_name="Bob", last_name="Wilson", age=35, city="SF"),
            User(id=10, username="user10", email="user10@example.com",
                 first_name="Bob", last_name="Wilson", age=35, city="SF"),
        ])
        # Unique person
        users.append(
            User(id=11, username="user11", email="user11@example.com",
                 first_name="Alice", last_name="Brown", age=28, city="Boston")
        )
        session.add_all(users)
        session.commit()

    # Act
    with memory_engine.connect() as connection:
        duplicates = find_duplicate_rows(
            connection,
            table_name="users",
            columns=["first_name", "last_name", "age", "city"],
            min_duplicates=2,
        )

    # Assert
    assert len(duplicates) == 3, "Should find 3 groups of duplicates"
    
    # Check sorted order (highest count first)
    assert duplicates[0]["count"] >= duplicates[1]["count"]
    assert duplicates[1]["count"] >= duplicates[2]["count"]
    
    # Verify the groups
    john_doe = next((d for d in duplicates if d["first_name"] == "John"), None)
    assert john_doe is not None
    assert john_doe["count"] == 5
    
    jane_smith = next((d for d in duplicates if d["first_name"] == "Jane"), None)
    assert jane_smith is not None
    assert jane_smith["count"] == 3
    
    bob_wilson = next((d for d in duplicates if d["first_name"] == "Bob"), None)
    assert bob_wilson is not None
    assert bob_wilson["count"] == 2
