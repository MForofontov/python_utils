"""
Unit tests for execute_bulk_chunked function.
"""

import sqlite3

import pytest

from database_functions import execute_bulk_chunked


def test_execute_bulk_chunked_successful_insert() -> None:
    """
    Test case 1: Successful bulk insert with real SQLite database.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    
    data = [
        {"id": 1, "name": "Alice", "age": 30},
        {"id": 2, "name": "Bob", "age": 25},
        {"id": 3, "name": "Charlie", "age": 35},
    ]
    
    def executor(chunk):
        cursor.executemany(
            "INSERT INTO users (id, name, age) VALUES (:id, :name, :age)",
            chunk
        )
    
    # Act
    result = execute_bulk_chunked(
        conn,
        executor,
        data,
        chunk_size=2
    )
    conn.commit()
    
    # Assert
    assert result["successful"] == 3
    assert result["failed"] == 0
    assert result["total"] == 3
    assert len(result["errors"]) == 0
    
    rows = cursor.execute("SELECT * FROM users ORDER BY id").fetchall()
    assert len(rows) == 3
    assert rows[0] == (1, "Alice", 30)
    
    conn.close()


def test_execute_bulk_chunked_with_updates() -> None:
    """
    Test case 2: Successful bulk update operation.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, score INTEGER)")
    cursor.executemany(
        "INSERT INTO users VALUES (?, ?, ?)",
        [(1, "Alice", 100), (2, "Bob", 200), (3, "Charlie", 300)]
    )
    conn.commit()
    
    update_data = [
        {"id": 1, "score": 150},
        {"id": 2, "score": 250},
        {"id": 3, "score": 350},
    ]
    
    def executor(chunk):
        for row in chunk:
            cursor.execute("UPDATE users SET score = :score WHERE id = :id", row)
    
    # Act
    result = execute_bulk_chunked(
        conn,
        executor,
        update_data,
        chunk_size=2
    )
    conn.commit()
    
    # Assert
    assert result["successful"] == 3
    assert result["failed"] == 0
    
    rows = cursor.execute("SELECT score FROM users ORDER BY id").fetchall()
    assert rows == [(150,), (250,), (350,)]
    
    conn.close()


def test_execute_bulk_chunked_skip_mode() -> None:
    """
    Test case 3: Skip mode skips failed chunks and continues.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    cursor.execute("INSERT INTO users VALUES (2, 'Existing')")
    conn.commit()
    
    data = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"},  # Will fail - duplicate key
        {"id": 3, "name": "Charlie"},
        {"id": 4, "name": "David"},
    ]
    
    def executor(chunk):
        cursor.executemany(
            "INSERT INTO users (id, name) VALUES (:id, :name)",
            chunk
        )
    
    # Act
    result = execute_bulk_chunked(
        conn,
        executor,
        data,
        chunk_size=2,
        on_error="skip",
        commit_func=lambda: conn.commit(),
        rollback_func=lambda: conn.rollback()
    )
    
    # Assert
    assert result["failed"] == 2  # First chunk with id=1,2 failed
    assert result["successful"] == 2  # Second chunk with id=3,4 succeeded
    
    rows = cursor.execute("SELECT id FROM users ORDER BY id").fetchall()
    assert rows == [(2,), (3,), (4,)]
    
    conn.close()


def test_execute_bulk_chunked_continue_mode() -> None:
    """
    Test case 4: Continue mode processes rows individually on chunk failure.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    cursor.execute("INSERT INTO users VALUES (2, 'Existing')")
    conn.commit()
    
    data = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"},  # Will fail - duplicate key
        {"id": 3, "name": "Charlie"},
    ]
    
    def executor(chunk):
        cursor.executemany(
            "INSERT INTO users (id, name) VALUES (:id, :name)",
            chunk
        )
    
    # Act
    result = execute_bulk_chunked(
        conn,
        executor,
        data,
        chunk_size=10,
        on_error="continue",
        commit_func=lambda: conn.commit(),
        rollback_func=lambda: conn.rollback()
    )
    
    # Assert
    assert result["successful"] == 2  # Alice and Charlie
    assert result["failed"] == 1  # Bob
    assert len(result["errors"]) == 1
    
    rows = cursor.execute("SELECT id FROM users ORDER BY id").fetchall()
    assert rows == [(1,), (2,), (3,)]
    
    conn.close()


def test_execute_bulk_chunked_with_progress_callback() -> None:
    """
    Test case 5: Progress callback receives correct counts.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    
    data = [{"id": i, "name": f"User{i}"} for i in range(1, 11)]
    
    progress_calls = []
    
    def progress_callback(completed, total):
        progress_calls.append((completed, total))
    
    def executor(chunk):
        cursor.executemany(
            "INSERT INTO users (id, name) VALUES (:id, :name)",
            chunk
        )
    
    # Act
    result = execute_bulk_chunked(
        conn,
        executor,
        data,
        chunk_size=3,
        progress_callback=progress_callback
    )
    conn.commit()
    
    # Assert
    assert result["successful"] == 10
    assert len(progress_calls) == 4
    assert progress_calls[-1] == (10, 10)
    
    conn.close()


def test_execute_bulk_chunked_empty_data() -> None:
    """
    Test case 6: Empty data list returns zero results.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    
    def executor(chunk):
        cursor.executemany("INSERT INTO users VALUES (:id, :name)", chunk)
    
    # Act
    result = execute_bulk_chunked(
        conn,
        executor,
        [],
        chunk_size=100
    )
    
    # Assert
    assert result["successful"] == 0
    assert result["failed"] == 0
    assert result["total"] == 0
    
    conn.close()


def test_execute_bulk_chunked_single_row() -> None:
    """
    Test case 7: Single row is processed correctly.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    
    data = [{"id": 1, "name": "Alice"}]
    
    def executor(chunk):
        cursor.executemany("INSERT INTO users VALUES (:id, :name)", chunk)
    
    # Act
    result = execute_bulk_chunked(
        conn,
        executor,
        data,
        chunk_size=100
    )
    conn.commit()
    
    # Assert
    assert result["successful"] == 1
    assert result["failed"] == 0
    
    rows = cursor.execute("SELECT * FROM users").fetchall()
    assert len(rows) == 1
    
    conn.close()


def test_execute_bulk_chunked_large_chunk_size() -> None:
    """
    Test case 8: Chunk size larger than data processes all in one chunk.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    
    data = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
    
    def executor(chunk):
        cursor.executemany("INSERT INTO users VALUES (:id, :name)", chunk)
    
    # Act
    result = execute_bulk_chunked(
        conn,
        executor,
        data,
        chunk_size=1000
    )
    conn.commit()
    
    # Assert
    assert result["successful"] == 2
    assert result["failed"] == 0
    
    conn.close()


def test_execute_bulk_chunked_fail_fast_raises() -> None:
    """
    Test case 9: Fail-fast mode raises on first error.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    cursor.execute("INSERT INTO users VALUES (2, 'Existing')")
    conn.commit()
    
    data = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"},
        {"id": 3, "name": "Charlie"},
    ]
    
    def executor(chunk):
        cursor.executemany("INSERT INTO users VALUES (:id, :name)", chunk)
    
    # Act & Assert
    with pytest.raises(sqlite3.IntegrityError):
        execute_bulk_chunked(
            conn,
            executor,
            data,
            chunk_size=10,
            on_error="fail_fast"
        )
    
    conn.close()


def test_execute_bulk_chunked_invalid_chunk_size() -> None:
    """
    Test case 10: Invalid chunk_size raises ValueError.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    
    def executor(chunk):
        pass
    
    # Act & Assert
    with pytest.raises(ValueError):
        execute_bulk_chunked(conn, executor, [], chunk_size=0)
    
    with pytest.raises(ValueError):
        execute_bulk_chunked(conn, executor, [], chunk_size=-1)
    
    conn.close()


def test_execute_bulk_chunked_none_connection() -> None:
    """
    Test case 11: None connection raises TypeError.
    """
    # Arrange
    def executor(chunk):
        pass
    
    # Act & Assert
    with pytest.raises(TypeError):
        execute_bulk_chunked(None, executor, [])


def test_execute_bulk_chunked_invalid_executor() -> None:
    """
    Test case 12: Non-callable executor raises TypeError.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    
    # Act & Assert
    with pytest.raises(TypeError):
        execute_bulk_chunked(conn, "not_callable", [])
    
    conn.close()


def test_execute_bulk_chunked_invalid_data_type() -> None:
    """
    Test case 13: Invalid data type raises TypeError.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    
    def executor(chunk):
        pass
    
    # Act & Assert
    with pytest.raises(TypeError, match="data must be a Sequence"):
        execute_bulk_chunked(conn, executor, 12345)  # int is not a Sequence
    
    conn.close()


def test_execute_bulk_chunked_invalid_on_error() -> None:
    """
    Test case 14: Invalid on_error value raises ValueError.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    
    def executor(chunk):
        pass
    
    # Act & Assert
    with pytest.raises(ValueError):
        execute_bulk_chunked(conn, executor, [], on_error="invalid")
    
    conn.close()
