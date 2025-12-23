"""
Performance test suite for migrate_id_type function.

These tests measure performance characteristics with large datasets and multiple
FK relationships. Tests are marked with @pytest.mark.performance to allow
selective execution.

Uses SQLite file-based storage for more realistic performance testing that better
reflects production database behavior (2-5x slower than in-memory, but still
5-10x faster than PostgreSQL).

Run with: pytest -m performance
Skip with: pytest -m "not performance"
"""

import sys
import tempfile
import time
import uuid
from collections.abc import Generator
from pathlib import Path

import psutil
import pytest
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    text,
)
from sqlalchemy.engine import Engine

from database_functions.schema_inspection.migrate_id_type import migrate_id_type


@pytest.fixture
def performance_engine() -> Generator[Engine, None, None]:
    """
    Test case setup: Create file-based SQLite database engine for performance tests.
    
    Uses temporary file for more realistic performance testing compared to in-memory.
    File is automatically cleaned up after test completion.
    """
    # Create temporary directory and database file
    temp_dir = tempfile.mkdtemp()
    db_path = Path(temp_dir) / "test_performance.db"
    
    engine = create_engine(f"sqlite:///{db_path}")
    yield engine
    
    # Cleanup: close connections and remove temp file
    engine.dispose()
    if db_path.exists():
        db_path.unlink()
    Path(temp_dir).rmdir()
    engine.dispose()


@pytest.mark.performance
def test_migrate_id_type_performance_10k_rows(performance_engine: Engine) -> None:
    """
    Test case 1: Performance with 10,000 rows in main table and 2 FK tables.
    
    Validates:
    - Migration completes within acceptable time (< 5 seconds)
    - Correct row counts
    - Memory efficiency
    """
    # Arrange
    engine = performance_engine
    metadata = MetaData()
    
    # Main table: users
    users = Table(
        "users",
        metadata,
        Column("id", String(36), primary_key=True),
        Column("name", String(100)),
        Column("email", String(100)),
    )
    
    # FK table 1: orders
    orders = Table(
        "orders",
        metadata,
        Column("order_id", Integer, primary_key=True),
        Column("user_id", String(36), ForeignKey("users.id")),
        Column("amount", Integer),
    )
    
    # FK table 2: sessions
    sessions = Table(
        "sessions",
        metadata,
        Column("session_id", Integer, primary_key=True),
        Column("user_id", String(36), ForeignKey("users.id")),
        Column("login_time", String(50)),
    )
    
    metadata.create_all(engine)
    
    # Insert 10,000 users
    with engine.begin() as conn:
        user_data = [
            {"id": f"user-{i}", "name": f"User{i}", "email": f"user{i}@example.com"}
            for i in range(10000)
        ]
        conn.execute(users.insert(), user_data)
        
        # Insert 20,000 orders (2 per user on average)
        order_data = [
            {"order_id": i, "user_id": f"user-{i % 10000}", "amount": (i * 100) % 10000}
            for i in range(20000)
        ]
        conn.execute(orders.insert(), order_data)
        
        # Insert 15,000 sessions (1.5 per user on average)
        session_data = [
            {"session_id": i, "user_id": f"user-{i % 10000}", "login_time": f"2025-01-{(i % 28) + 1:02d}"}
            for i in range(15000)
        ]
        conn.execute(sessions.insert(), session_data)
    
    id_counter = [0]
    
    def generate_new_id() -> str:
        id_counter[0] += 1
        return f"new-user-{id_counter[0]}"
    
    # Memory measurement
    process = psutil.Process()
    mem_before = process.memory_info().rss / 1024 / 1024  # MB
    
    # Act
    start_time = time.time()
    result = migrate_id_type(
        engine=engine,
        table_name="users",
        id_generator=generate_new_id,
        id_column="id",
        batch_size=1000,
    )
    elapsed_time = time.time() - start_time
    
    mem_after = process.memory_info().rss / 1024 / 1024  # MB
    mem_used = mem_after - mem_before
    
    # Assert
    assert result["rows_migrated"] == 10000
    assert result["fk_relationships_updated"] == 35000  # 20k orders + 15k sessions
    assert result["rows_per_table"]["users"] == 10000
    assert result["rows_per_table"]["orders"] == 20000
    assert result["rows_per_table"]["sessions"] == 15000
    assert len(result["tables_affected"]) == 2
    
    # Performance assertion: should complete within 5 seconds
    assert elapsed_time < 5.0, f"Migration took {elapsed_time:.2f}s, expected < 5s"
    assert mem_used < 50.0, f"Memory usage {mem_used:.2f} MB exceeds limit of 50 MB"
    
    print(f"\n✓ Migrated 10k users with 35k FK references in {elapsed_time:.2f}s")
    print(f"  Memory used: {mem_used:.2f} MB")


@pytest.mark.performance
def test_migrate_id_type_performance_100k_rows(performance_engine: Engine) -> None:
    """
    Test case 2: Performance with 100,000 rows in main table.
    
    Validates:
    - Migration completes within acceptable time (< 30 seconds)
    - Batch processing efficiency
    - Correct row counts
    """
    # Arrange
    engine = performance_engine
    metadata = MetaData()
    
    # Main table: items
    items = Table(
        "items",
        metadata,
        Column("id", String(36), primary_key=True),
        Column("name", String(100)),
    )
    
    metadata.create_all(engine)
    
    # Insert 100,000 items
    with engine.begin() as conn:
        # Insert in batches for faster setup
        batch_size = 5000
        for batch_start in range(0, 100000, batch_size):
            item_data = [
                {"id": f"item-{i}", "name": f"Item{i}"}
                for i in range(batch_start, min(batch_start + batch_size, 100000))
            ]
            conn.execute(items.insert(), item_data)
    
    id_counter = [0]
    
    def generate_new_id() -> str:
        id_counter[0] += 1
        return f"new-item-{id_counter[0]}"
    
    # Memory measurement
    process = psutil.Process()
    mem_before = process.memory_info().rss / 1024 / 1024  # MB
    
    # Act
    start_time = time.time()
    result = migrate_id_type(
        engine=engine,
        table_name="items",
        id_generator=generate_new_id,
        id_column="id",
        batch_size=1000,
    )
    elapsed_time = time.time() - start_time
    
    mem_after = process.memory_info().rss / 1024 / 1024  # MB
    mem_used = mem_after - mem_before
    
    # Assert
    assert result["rows_migrated"] == 100000
    assert result["fk_relationships_updated"] == 0
    assert result["rows_per_table"]["items"] == 100000
    
    # Performance assertion: should complete within 30 seconds
    assert elapsed_time < 30.0, f"Migration took {elapsed_time:.2f}s, expected < 30s"
    assert mem_used < 100.0, f"Memory usage {mem_used:.2f} MB exceeds limit of 100 MB"
    
    print(f"\n✓ Migrated 100k rows in {elapsed_time:.2f}s ({100000/elapsed_time:.0f} rows/sec)")
    print(f"  Memory used: {mem_used:.2f} MB")


@pytest.mark.performance
def test_migrate_id_type_performance_complex_fk_relationships(performance_engine: Engine) -> None:
    """
    Test case 3: Performance with complex FK relationships (5 FK tables).
    
    Validates:
    - Handles multiple FK relationships efficiently
    - Correct FK discovery and updates
    - Performance with complex schema
    """
    # Arrange
    engine = performance_engine
    metadata = MetaData()
    
    # Main table: users
    users = Table(
        "users",
        metadata,
        Column("id", String(36), primary_key=True),
        Column("name", String(100)),
    )
    
    # 5 different FK tables
    orders = Table(
        "orders",
        metadata,
        Column("order_id", Integer, primary_key=True),
        Column("user_id", String(36), ForeignKey("users.id")),
    )
    
    addresses = Table(
        "addresses",
        metadata,
        Column("address_id", Integer, primary_key=True),
        Column("user_id", String(36), ForeignKey("users.id")),
    )
    
    payments = Table(
        "payments",
        metadata,
        Column("payment_id", Integer, primary_key=True),
        Column("user_id", String(36), ForeignKey("users.id")),
    )
    
    reviews = Table(
        "reviews",
        metadata,
        Column("review_id", Integer, primary_key=True),
        Column("user_id", String(36), ForeignKey("users.id")),
    )
    
    sessions = Table(
        "sessions",
        metadata,
        Column("session_id", Integer, primary_key=True),
        Column("user_id", String(36), ForeignKey("users.id")),
    )
    
    metadata.create_all(engine)
    
    # Insert 5,000 users with data in all FK tables
    with engine.begin() as conn:
        user_data = [{"id": f"user-{i}", "name": f"User{i}"} for i in range(5000)]
        conn.execute(users.insert(), user_data)
        
        # Each user has records in all 5 FK tables
        for i in range(5000):
            conn.execute(orders.insert(), {"order_id": i, "user_id": f"user-{i}"})
            conn.execute(addresses.insert(), {"address_id": i, "user_id": f"user-{i}"})
            conn.execute(payments.insert(), {"payment_id": i, "user_id": f"user-{i}"})
            conn.execute(reviews.insert(), {"review_id": i, "user_id": f"user-{i}"})
            conn.execute(sessions.insert(), {"session_id": i, "user_id": f"user-{i}"})
    
    id_counter = [0]
    
    def generate_new_id() -> str:
        id_counter[0] += 1
        return f"new-user-{id_counter[0]}"
    
    # Memory measurement
    process = psutil.Process()
    mem_before = process.memory_info().rss / 1024 / 1024  # MB
    
    # Act
    start_time = time.time()
    result = migrate_id_type(
        engine=engine,
        table_name="users",
        id_generator=generate_new_id,
        id_column="id",
        batch_size=500,
    )
    elapsed_time = time.time() - start_time
    
    mem_after = process.memory_info().rss / 1024 / 1024  # MB
    mem_used = mem_after - mem_before
    
    # Assert
    assert result["rows_migrated"] == 5000
    assert result["fk_relationships_updated"] == 25000  # 5k × 5 tables
    assert len(result["tables_affected"]) == 5
    assert result["rows_per_table"]["users"] == 5000
    assert result["rows_per_table"]["orders"] == 5000
    assert result["rows_per_table"]["addresses"] == 5000
    assert result["rows_per_table"]["payments"] == 5000
    assert result["rows_per_table"]["reviews"] == 5000
    assert result["rows_per_table"]["sessions"] == 5000
    
    # Performance assertion: should complete within 10 seconds
    assert elapsed_time < 10.0, f"Migration took {elapsed_time:.2f}s, expected < 10s"
    assert mem_used < 50.0, f"Memory usage {mem_used:.2f} MB exceeds limit of 50 MB"
    
    print(f"\n✓ Migrated 5k users with 5 FK tables (25k references) in {elapsed_time:.2f}s")
    print(f"  Memory used: {mem_used:.2f} MB")


@pytest.mark.performance
def test_migrate_id_type_performance_small_batch_size(performance_engine: Engine) -> None:
    """
    Test case 4: Performance impact of small batch size.
    
    Validates:
    - Small batch size impact on performance
    - Correctness with more frequent batch commits
    """
    # Arrange
    engine = performance_engine
    metadata = MetaData()
    
    items = Table(
        "items",
        metadata,
        Column("id", String(36), primary_key=True),
        Column("value", Integer),
    )
    
    metadata.create_all(engine)
    
    # Insert 10,000 items
    with engine.begin() as conn:
        item_data = [{"id": f"item-{i}", "value": i} for i in range(10000)]
        conn.execute(items.insert(), item_data)
    
    id_counter = [0]
    
    def generate_new_id() -> str:
        id_counter[0] += 1
        return f"new-item-{id_counter[0]}"
    
    # Memory measurement
    process = psutil.Process()
    mem_before = process.memory_info().rss / 1024 / 1024  # MB
    
    # Act - Use very small batch size
    start_time = time.time()
    result = migrate_id_type(
        engine=engine,
        table_name="items",
        id_generator=generate_new_id,
        batch_size=100,  # Small batch
    )
    elapsed_time = time.time() - start_time
    
    mem_after = process.memory_info().rss / 1024 / 1024  # MB
    mem_used = mem_after - mem_before
    
    # Assert
    assert result["rows_migrated"] == 10000
    assert result["rows_per_table"]["items"] == 10000
    
    # Performance assertion: should still complete reasonably fast
    assert elapsed_time < 10.0, f"Migration with batch_size=100 took {elapsed_time:.2f}s, expected < 10s"
    assert mem_used < 50.0, f"Memory usage {mem_used:.2f} MB exceeds limit of 50 MB"
    
    print(f"\n✓ Migrated 10k rows with batch_size=100 in {elapsed_time:.2f}s")
    print(f"  Memory used: {mem_used:.2f} MB")


@pytest.mark.performance
def test_migrate_id_type_performance_uuid_generation(performance_engine: Engine) -> None:
    """
    Test case 5: Performance with UUID generation.
    
    Validates:
    - UUID generation overhead
    - Performance with realistic ID generator
    """
    # Arrange
    engine = performance_engine
    metadata = MetaData()
    
    users = Table(
        "users",
        metadata,
        Column("id", String(36), primary_key=True),
        Column("name", String(100)),
    )
    
    metadata.create_all(engine)
    
    # Insert 10,000 users
    with engine.begin() as conn:
        user_data = [{"id": f"user-{i}", "name": f"User{i}"} for i in range(10000)]
        conn.execute(users.insert(), user_data)
    
    # Act - Use UUID4 generator (realistic scenario)
    start_time = time.time()
    result = migrate_id_type(
        engine=engine,
        table_name="users",
        id_generator=lambda: str(uuid.uuid4()),
        id_column="id",
        batch_size=1000,
    )
    elapsed_time = time.time() - start_time
    
    # Assert
    assert result["rows_migrated"] == 10000
    assert result["rows_per_table"]["users"] == 10000
    
    # All IDs should be valid UUIDs (contain hyphens)
    for old_id, new_id in result["id_mapping"].items():
        assert "-" in new_id, f"Generated ID {new_id} doesn't look like a UUID"
    
    # Memory measurement
    process = psutil.Process()
    mem_before = process.memory_info().rss / 1024 / 1024  # MB
    
    # Act - Use UUID4 generator (realistic scenario)
    start_time = time.time()
    result = migrate_id_type(
        engine=engine,
        table_name="users",
        id_generator=lambda: str(uuid.uuid4()),
        id_column="id",
        batch_size=1000,
    )
    elapsed_time = time.time() - start_time
    
    mem_after = process.memory_info().rss / 1024 / 1024  # MB
    mem_used = mem_after - mem_before
    
    # Assert
    assert result["rows_migrated"] == 10000
    assert result["rows_per_table"]["users"] == 10000
    
    # All IDs should be valid UUIDs (contain hyphens)
    for old_id, new_id in result["id_mapping"].items():
        assert "-" in new_id, f"Generated ID {new_id} doesn't look like a UUID"
    
    # Performance assertion
    assert elapsed_time < 5.0, f"UUID migration took {elapsed_time:.2f}s, expected < 5s"
    assert mem_used < 50.0, f"Memory usage {mem_used:.2f} MB exceeds limit of 50 MB"
    
    print(f"\n✓ Migrated 10k rows with UUID generation in {elapsed_time:.2f}s")
    print(f"  Memory used: {mem_used:.2f} MB")


@pytest.mark.performance
def test_migrate_id_type_performance_batch_size_comparison(performance_engine: Engine) -> None:
    """
    Test case 7: Batch size impact comparison on speed and memory.
    
    Validates:
    - Different batch sizes (100, 500, 1000, 5000, 10000) impact on performance
    - Optimal batch size for different scenarios
    - Memory usage vs speed tradeoffs
    """
    # Arrange
    engine = performance_engine
    batch_sizes = [100, 500, 1000, 5000, 10000]
    results = {}
    
    print("\n📊 Batch Size Performance Comparison (20K rows)")
    print("=" * 70)
    
    for batch_size in batch_sizes:
        # Create fresh metadata for each test
        metadata = MetaData()
        
        items = Table(
            "items",
            metadata,
            Column("id", String(36), primary_key=True),
            Column("data", String(100)),
        )
        
        metadata.create_all(engine)
        
        # Insert 20,000 items
        with engine.begin() as conn:
            item_data = [
                {"id": f"item-{batch_size}-{i}", "data": f"Data{i}"}
                for i in range(20000)
            ]
            conn.execute(items.insert(), item_data)
        
        id_counter = [0]
        
        def generate_new_id() -> str:
            id_counter[0] += 1
            return f"new-item-{batch_size}-{id_counter[0]}"
        
        # Get process for memory measurement
        process = psutil.Process()
        mem_before = process.memory_info().rss / 1024 / 1024  # MB
        
        # Act
        start_time = time.time()
        result = migrate_id_type(
            engine=engine,
            table_name="items",
            id_generator=generate_new_id,
            batch_size=batch_size,
        )
        elapsed_time = time.time() - start_time
        
        mem_after = process.memory_info().rss / 1024 / 1024  # MB
        mem_used = mem_after - mem_before
        
        # Store results
        results[batch_size] = {
            "time": elapsed_time,
            "memory": mem_used,
            "rows_per_sec": 20000 / elapsed_time,
        }
        
        # Cleanup for next iteration
        metadata.drop_all(engine)
        
        # Print results
        print(f"Batch size {batch_size:>5}: {elapsed_time:>6.3f}s | "
              f"{results[batch_size]['rows_per_sec']:>8.0f} rows/sec | "
              f"{mem_used:>6.2f} MB")
    
    print("=" * 70)
    
    # Find optimal batch size (best speed)
    fastest_batch = min(results.items(), key=lambda x: x[1]["time"])
    most_efficient_mem = min(results.items(), key=lambda x: x[1]["memory"])
    
    print(f"\n✓ Fastest: batch_size={fastest_batch[0]} ({fastest_batch[1]['time']:.3f}s)")
    print(f"✓ Most memory efficient: batch_size={most_efficient_mem[0]} ({most_efficient_mem[1]['memory']:.2f} MB)")
    
    # Assert all completed successfully
    for batch_size, stats in results.items():
        assert stats["time"] < 10.0, f"Batch size {batch_size} took {stats['time']:.2f}s, expected < 10s"
        assert stats["memory"] < 50.0, f"Batch size {batch_size} used {stats['memory']:.2f} MB, expected < 50 MB"
    
    # Performance insights
    slowest_time = max(stats["time"] for stats in results.values())
    fastest_time = min(stats["time"] for stats in results.values())
    speedup = slowest_time / fastest_time
    
    print(f"\n📈 Performance Insights:")
    print(f"   • Speed variation: {speedup:.2f}x between slowest and fastest")
    print(f"   • Batch sizes 1000-5000 recommended for balanced performance")


@pytest.mark.performance
@pytest.mark.slow
def test_migrate_id_type_performance_stress_test_1m_rows(performance_engine: Engine) -> None:
    """
    Test case 7: Stress test with 1 million rows (marked as slow).
    
    This test is marked with both @pytest.mark.performance and @pytest.mark.slow.
    
    Run with: pytest -m "performance and slow"
    Skip with: pytest -m "performance and not slow"
    
    Validates:
    - Function can handle very large datasets
    - Performance remains acceptable at scale
    - Memory usage doesn't grow excessively
    """
    # Arrange
    engine = performance_engine
    metadata = MetaData()
    
    items = Table(
        "items",
        metadata,
        Column("id", String(36), primary_key=True),
        Column("value", Integer),
    )
    
    metadata.create_all(engine)
    
    # Insert 1,000,000 items in batches
    print("\n⏳ Setting up 1M rows...")
    with engine.begin() as conn:
        batch_size = 10000
        for batch_start in range(0, 1000000, batch_size):
            if batch_start % 100000 == 0:
                print(f"  Inserted {batch_start:,} rows...")
            item_data = [
                {"id": f"item-{i}", "value": i}
                for i in range(batch_start, min(batch_start + batch_size, 1000000))
            ]
            conn.execute(items.insert(), item_data)
    print("  ✓ Setup complete")
    
    id_counter = [0]
    
    def generate_new_id() -> str:
        id_counter[0] += 1
        return f"new-item-{id_counter[0]}"
    
    # Get process for memory measurement
    process = psutil.Process()
    
    # Measure memory before migration
    mem_before = process.memory_info().rss / 1024 / 1024  # Convert to MB
    
    # Act
    print("⏳ Starting migration...")
    start_time = time.time()
    result = migrate_id_type(
        engine=engine,
        table_name="items",
        id_generator=generate_new_id,
        batch_size=5000,
    )
    elapsed_time = time.time() - start_time
    
    # Measure memory after migration
    mem_after = process.memory_info().rss / 1024 / 1024  # Convert to MB
    mem_used = mem_after - mem_before
    
    # Calculate ID mapping size
    id_mapping_size = sys.getsizeof(result["id_mapping"])
    id_mapping_size_mb = id_mapping_size / 1024 / 1024
    
    # Assert
    assert result["rows_migrated"] == 1000000
    assert result["rows_per_table"]["items"] == 1000000
    
    # Performance assertion: should complete within 5 minutes
    assert elapsed_time < 300.0, f"Migration took {elapsed_time:.2f}s, expected < 300s"
    
    # Memory assertion: should not exceed 500 MB for 1M rows (including id_mapping ~80MB)
    assert mem_used < 500.0, f"Memory usage {mem_used:.2f} MB exceeds limit of 500 MB"
    
    rows_per_second = 1000000 / elapsed_time
    print(f"\n✓ Migrated 1M rows in {elapsed_time:.2f}s ({rows_per_second:.0f} rows/sec)")
    print(f"  Memory used: {mem_used:.2f} MB (id_mapping: {id_mapping_size_mb:.2f} MB)")
    print(f"  Memory efficiency: {mem_used / 1000:.2f} KB per 1k rows")
