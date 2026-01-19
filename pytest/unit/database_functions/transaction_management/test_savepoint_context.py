"""
Unit tests for savepoint_context function.
"""

import sqlite3

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.database]
from python_utils.database_functions import savepoint_context


def test_savepoint_context_successful_release() -> None:
    """
    Test case 1: Successful savepoint is released.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE data (value INTEGER)")
    cursor.execute("BEGIN")
    cursor.execute("INSERT INTO data VALUES (1)")

    # Act
    with savepoint_context(
        cursor,
        savepoint_name="sp1",
        create_savepoint_func=lambda name: cursor.execute(f"SAVEPOINT {name}"),
        release_savepoint_func=lambda name: cursor.execute(f"RELEASE SAVEPOINT {name}"),
    ):
        cursor.execute("INSERT INTO data VALUES (2)")

    conn.commit()

    # Assert
    result = cursor.execute("SELECT COUNT(*) FROM data").fetchone()
    assert result == (2,)

    conn.close()


def test_savepoint_context_rollback_mode() -> None:
    """
    Test case 2: Rollback mode rolls back to savepoint on error.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE data (value INTEGER)")
    cursor.execute("BEGIN")
    cursor.execute("INSERT INTO data VALUES (1)")

    # Act & Assert
    with pytest.raises(ValueError):
        with savepoint_context(
            cursor,
            savepoint_name="sp1",
            on_error="rollback",
            create_savepoint_func=lambda name: cursor.execute(f"SAVEPOINT {name}"),
            rollback_savepoint_func=lambda name: cursor.execute(
                f"ROLLBACK TO SAVEPOINT {name}"
            ),
        ):
            cursor.execute("INSERT INTO data VALUES (2)")
            raise ValueError("Test error")

    conn.commit()

    # Assert - only first insert should remain
    result = cursor.execute("SELECT value FROM data").fetchall()
    assert result == [(1,)]

    conn.close()


def test_savepoint_context_ignore_mode() -> None:
    """
    Test case 3: Ignore mode ignores errors and continues.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE data (value INTEGER)")
    cursor.execute("BEGIN")
    cursor.execute("INSERT INTO data VALUES (1)")

    # Act - No exception should be raised
    with savepoint_context(
        cursor,
        savepoint_name="sp1",
        on_error="ignore",
        create_savepoint_func=lambda name: cursor.execute(f"SAVEPOINT {name}"),
    ):
        cursor.execute("INSERT INTO data VALUES (2)")
        raise ValueError("Ignored error")

    conn.commit()

    # Assert - both inserts should be there (error ignored)
    result = cursor.execute("SELECT COUNT(*) FROM data").fetchone()
    assert result == (2,)

    conn.close()


def test_savepoint_context_optional_operation() -> None:
    """
    Test case 4: Use case for optional operations that may fail.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    cursor.execute("BEGIN")
    cursor.execute("INSERT INTO users VALUES (1, 'Alice')")

    # Act - Try to insert duplicate (optional operation)
    with savepoint_context(
        cursor,
        savepoint_name="optional_insert",
        on_error="ignore",
        create_savepoint_func=lambda name: cursor.execute(f"SAVEPOINT {name}"),
    ):
        try:
            cursor.execute("INSERT INTO users VALUES (1, 'Duplicate')")
        except sqlite3.IntegrityError:
            pass

    conn.commit()

    # Assert - original data remains
    result = cursor.execute("SELECT name FROM users WHERE id = 1").fetchone()
    assert result == ("Alice",)

    conn.close()


def test_savepoint_context_nested_savepoints() -> None:
    """
    Test case 5: Multiple nested savepoints work independently.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE data (value INTEGER)")
    cursor.execute("BEGIN")
    cursor.execute("INSERT INTO data VALUES (1)")

    # Act
    with savepoint_context(
        cursor,
        savepoint_name="outer",
        create_savepoint_func=lambda name: cursor.execute(f"SAVEPOINT {name}"),
        release_savepoint_func=lambda name: cursor.execute(f"RELEASE SAVEPOINT {name}"),
    ):
        cursor.execute("INSERT INTO data VALUES (2)")

        try:
            with savepoint_context(
                cursor,
                savepoint_name="inner",
                on_error="rollback",
                create_savepoint_func=lambda name: cursor.execute(f"SAVEPOINT {name}"),
                rollback_savepoint_func=lambda name: cursor.execute(
                    f"ROLLBACK TO SAVEPOINT {name}"
                ),
            ):
                cursor.execute("INSERT INTO data VALUES (3)")
                raise ValueError("Inner error")
        except ValueError:
            pass

    conn.commit()

    # Assert - 1 and 2 remain, 3 was rolled back
    result = cursor.execute("SELECT value FROM data ORDER BY value").fetchall()
    assert result == [(1,), (2,)]

    conn.close()


def test_savepoint_context_fallback_to_sql() -> None:
    """
    Test case 6: Falls back to SQL when no functions provided.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE data (value INTEGER)")
    cursor.execute("BEGIN")

    # Act
    with savepoint_context(cursor, savepoint_name="sp1"):
        cursor.execute("INSERT INTO data VALUES (1)")

    conn.commit()

    # Assert
    result = cursor.execute("SELECT COUNT(*) FROM data").fetchone()
    assert result == (1,)

    conn.close()


def test_savepoint_context_none_connection() -> None:
    """
    Test case 7: None connection raises TypeError.
    """
    # Act & Assert
    with pytest.raises(TypeError):
        with savepoint_context(None, savepoint_name="sp1"):
            pass


def test_savepoint_context_empty_savepoint_name() -> None:
    """
    Test case 8: Empty savepoint_name raises ValueError.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")

    # Act & Assert
    with pytest.raises(ValueError):
        with savepoint_context(conn, savepoint_name=""):
            pass

    conn.close()


def test_savepoint_context_invalid_on_error() -> None:
    """
    Test case 9: Invalid on_error value raises ValueError.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")

    # Act & Assert
    with pytest.raises(ValueError):
        with savepoint_context(conn, savepoint_name="sp1", on_error="invalid"):
            pass

    conn.close()


def test_savepoint_context_invalid_create_func() -> None:
    """
    Test case 10: Non-callable create_savepoint_func raises TypeError.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")

    # Act & Assert
    with pytest.raises(TypeError):
        with savepoint_context(
            conn, savepoint_name="sp1", create_savepoint_func="not_callable"
        ):
            pass

    conn.close()
