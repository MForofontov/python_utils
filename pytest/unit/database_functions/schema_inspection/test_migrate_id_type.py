"""
Comprehensive test suite for migrate_id_type function.

Tests cover ID type migration with foreign key handling and various ID type
conversions (UUID, integer, string).
"""

import logging
import uuid
from unittest.mock import Mock

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
from sqlalchemy.exc import SQLAlchemyError

from database_functions.schema_inspection.migrate_id_type import migrate_id_type


@pytest.fixture
def in_memory_engine():
    """
    Test case setup: Create in-memory SQLite database engine.
    """
    engine = create_engine("sqlite:///:memory:")
    yield engine
    engine.dispose()


@pytest.fixture
def sample_database(in_memory_engine):
    """
    Test case setup: Create complex database with multiple tables and relationships.
    
    Schema:
    - users (main table to migrate): id, name, email
    - orders: order_id, user_id (FK -> users.id), amount
    - addresses: address_id, user_id (FK -> users.id), street, city
    - reviews: review_id, user_id (FK -> users.id), order_id (FK -> orders.order_id), rating
    - standalone: id, data (no foreign keys)
    
    Relationships:
    - orders.user_id -> users.id
    - addresses.user_id -> users.id
    - reviews.user_id -> users.id
    - reviews.order_id -> orders.order_id (relationship outside main table)
    - standalone has no relationships
    """
    engine = in_memory_engine
    metadata = MetaData()

    # Main table: users
    users = Table(
        "users",
        metadata,
        Column("id", String(36), primary_key=True),
        Column("name", String(100)),
        Column("email", String(100)),
    )

    # Orders table with FK to users
    orders = Table(
        "orders",
        metadata,
        Column("order_id", Integer, primary_key=True),
        Column("user_id", String(36), ForeignKey("users.id")),
        Column("amount", Integer),
    )

    # Addresses table with FK to users
    addresses = Table(
        "addresses",
        metadata,
        Column("address_id", Integer, primary_key=True),
        Column("user_id", String(36), ForeignKey("users.id")),
        Column("street", String(200)),
        Column("city", String(100)),
    )

    # Reviews table with FK to both users AND orders (cross-table relationship)
    reviews = Table(
        "reviews",
        metadata,
        Column("review_id", Integer, primary_key=True),
        Column("user_id", String(36), ForeignKey("users.id")),
        Column("order_id", Integer, ForeignKey("orders.order_id")),
        Column("rating", Integer),
        Column("comment", String(500)),
    )

    # Standalone table with no foreign keys
    standalone = Table(
        "standalone",
        metadata,
        Column("id", String(36), primary_key=True),
        Column("data", String(200)),
        Column("value", Integer),
    )

    metadata.create_all(engine)

    # Insert sample data
    with engine.begin() as conn:
        # Insert users
        conn.execute(
            users.insert(),
            [
                {"id": "user-1", "name": "Alice", "email": "alice@example.com"},
                {"id": "user-2", "name": "Bob", "email": "bob@example.com"},
                {"id": "user-3", "name": "Charlie", "email": "charlie@example.com"},
            ],
        )
        
        # Insert orders
        conn.execute(
            orders.insert(),
            [
                {"order_id": 1, "user_id": "user-1", "amount": 100},
                {"order_id": 2, "user_id": "user-1", "amount": 200},
                {"order_id": 3, "user_id": "user-2", "amount": 150},
                {"order_id": 4, "user_id": "user-3", "amount": 300},
            ],
        )
        
        # Insert addresses
        conn.execute(
            addresses.insert(),
            [
                {"address_id": 1, "user_id": "user-1", "street": "123 Main St", "city": "New York"},
                {"address_id": 2, "user_id": "user-1", "street": "456 Oak Ave", "city": "Boston"},
                {"address_id": 3, "user_id": "user-2", "street": "789 Pine Rd", "city": "Chicago"},
            ],
        )
        
        # Insert reviews (with relationships to both users and orders)
        conn.execute(
            reviews.insert(),
            [
                {"review_id": 1, "user_id": "user-1", "order_id": 1, "rating": 5, "comment": "Great!"},
                {"review_id": 2, "user_id": "user-1", "order_id": 2, "rating": 4, "comment": "Good"},
                {"review_id": 3, "user_id": "user-2", "order_id": 3, "rating": 5, "comment": "Excellent"},
                {"review_id": 4, "user_id": "user-3", "order_id": 4, "rating": 4, "comment": "Nice"},
            ],
        )
        
        # Insert standalone data
        conn.execute(
            standalone.insert(),
            [
                {"id": "standalone-1", "data": "Independent data 1", "value": 100},
                {"id": "standalone-2", "data": "Independent data 2", "value": 200},
            ],
        )

    return engine, metadata


def test_migrate_id_type_successful_complex_migration(sample_database) -> None:
    """
    Test case 1: Successfully migrate IDs with all FK relationships updated across 4 tables.
    """
    # Arrange
    engine, metadata = sample_database
    id_counter = [0]

    def generate_new_id():
        id_counter[0] += 1
        return f"new-user-{id_counter[0]}"

    # Act
    result = migrate_id_type(
        engine=engine,
        table_name="users",
        id_generator=generate_new_id,
        id_column="id",
        batch_size=10,
    )

    # Assert - Main counts
    assert result["rows_migrated"] == 3
    assert result["fk_relationships_updated"] == 11  # 4 orders + 3 addresses + 4 reviews
    assert len(result["id_mapping"]) == 3
    
    # Assert - Tables affected
    assert "orders" in result["tables_affected"]
    assert "addresses" in result["tables_affected"]
    assert "reviews" in result["tables_affected"]
    assert len(result["tables_affected"]) == 3
    
    # Assert - Rows per table breakdown
    assert "rows_per_table" in result
    assert result["rows_per_table"]["users"] == 3
    assert result["rows_per_table"]["orders"] == 4
    assert result["rows_per_table"]["addresses"] == 3
    assert result["rows_per_table"]["reviews"] == 4
    assert len(result["rows_per_table"]) == 4  # users + 3 FK tables
    
    # Assert - ID mapping
    assert "user-1" in result["id_mapping"]
    assert "user-2" in result["id_mapping"]
    assert "user-3" in result["id_mapping"]
    
    # Assert - No schema_verified in result
    assert "schema_verified" not in result

    # Verify data integrity in all related tables
    with engine.connect() as conn:
        # Check users table
        users_result = conn.execute(text("SELECT id FROM users ORDER BY name"))
        user_ids = [row[0] for row in users_result]
        assert all(uid.startswith("new-user-") for uid in user_ids)
        assert len(user_ids) == 3

        # Check orders table
        orders_result = conn.execute(text("SELECT user_id FROM orders ORDER BY order_id"))
        order_user_ids = [row[0] for row in orders_result]
        assert all(uid.startswith("new-user-") for uid in order_user_ids)
        assert len(order_user_ids) == 4
        
        # Check addresses table
        addresses_result = conn.execute(text("SELECT user_id FROM addresses ORDER BY address_id"))
        address_user_ids = [row[0] for row in addresses_result]
        assert all(uid.startswith("new-user-") for uid in address_user_ids)
        assert len(address_user_ids) == 3
        
        # Check reviews table
        reviews_result = conn.execute(text("SELECT user_id FROM reviews ORDER BY review_id"))
        review_user_ids = [row[0] for row in reviews_result]
        assert all(uid.startswith("new-user-") for uid in review_user_ids)
        assert len(review_user_ids) == 4
        
        # Verify standalone table was NOT affected
        standalone_result = conn.execute(text("SELECT id FROM standalone ORDER BY id"))
        standalone_ids = [row[0] for row in standalone_result]
        assert standalone_ids == ["standalone-1", "standalone-2"]


def test_migrate_id_type_with_uuid_generator(in_memory_engine) -> None:
    """
    Test case 2: Migration with UUID generator function.
    """
    # Arrange
    engine = in_memory_engine
    metadata = MetaData()

    Table(
        "products",
        metadata,
        Column("id", String(50), primary_key=True),
        Column("name", String(100)),
    )
    metadata.create_all(engine)

    with engine.begin() as conn:
        conn.execute(text("INSERT INTO products (id, name) VALUES ('prod-1', 'Widget')"))
        conn.execute(text("INSERT INTO products (id, name) VALUES ('prod-2', 'Gadget')"))

    # Act
    result = migrate_id_type(
        engine=engine,
        table_name="products",
        id_generator=lambda: str(uuid.uuid4()),
        id_column="id",
    )

    # Assert
    assert result["rows_migrated"] == 2
    assert result["rows_per_table"]["products"] == 2
    assert result["fk_relationships_updated"] == 0
    assert len(result["tables_affected"]) == 0
    assert len(result["id_mapping"]) == 2
    
    # Verify UUIDs were generated
    with engine.connect() as conn:
        products_result = conn.execute(text("SELECT id FROM products"))
        product_ids = [row[0] for row in products_result]
        # Check they look like UUIDs (contain hyphens)
        assert all("-" in pid for pid in product_ids)


def test_migrate_id_type_invalid_engine_type() -> None:
    """
    Test case 3: TypeError when engine is not SQLAlchemy Engine.
    """
    # Arrange
    invalid_engine = "not_an_engine"
    expected_message = "engine must be an SQLAlchemy Engine, got str"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        migrate_id_type(
            engine=invalid_engine,
            table_name="users",
            id_generator=uuid.uuid4,
        )


def test_migrate_id_type_invalid_table_name_type(in_memory_engine) -> None:
    """
    Test case 4: TypeError when table_name is not a string.
    """
    # Arrange
    expected_message = "table_name must be a string, got int"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        migrate_id_type(
            engine=in_memory_engine,
            table_name=123,
            id_generator=uuid.uuid4,
        )


def test_migrate_id_type_empty_table_name(in_memory_engine) -> None:
    """
    Test case 5: ValueError when table_name is empty string.
    """
    # Arrange
    expected_message = "table_name cannot be empty"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        migrate_id_type(
            engine=in_memory_engine,
            table_name="",
            id_generator=uuid.uuid4,
        )


def test_migrate_id_type_non_callable_id_generator(in_memory_engine) -> None:
    """
    Test case 6: TypeError when id_generator is not callable.
    """
    # Arrange
    expected_message = "id_generator must be callable"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        migrate_id_type(
            engine=in_memory_engine,
            table_name="users",
            id_generator="not_callable",
        )


def test_migrate_id_type_invalid_batch_size(in_memory_engine) -> None:
    """
    Test case 7: ValueError when batch_size is not positive.
    """
    # Arrange
    expected_message = "batch_size must be positive, got -5"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        migrate_id_type(
            engine=in_memory_engine,
            table_name="users",
            id_generator=uuid.uuid4,
            batch_size=-5,
        )


def test_migrate_id_type_table_not_exists(in_memory_engine) -> None:
    """
    Test case 8: ValueError when table doesn't exist in database.
    """
    # Arrange
    expected_message = "Table 'nonexistent_table' does not exist in database"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        migrate_id_type(
            engine=in_memory_engine,
            table_name="nonexistent_table",
            id_generator=uuid.uuid4,
        )


def test_migrate_id_type_column_not_exists(in_memory_engine) -> None:
    """
    Test case 9: ValueError when column doesn't exist in table.
    """
    # Arrange
    metadata = MetaData()
    Table(
        "users",
        metadata,
        Column("id", String(36), primary_key=True),
        Column("name", String(100)),
    )
    metadata.create_all(in_memory_engine)

    expected_message = "Column 'nonexistent_column' does not exist in table 'users'"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        migrate_id_type(
            engine=in_memory_engine,
            table_name="users",
            id_generator=uuid.uuid4,
            id_column="nonexistent_column",
        )


def test_migrate_id_type_multiple_fk_columns_same_table(in_memory_engine) -> None:
    """
    Test case 10: Handle multiple FK columns in same table referencing main table.
    """
    # Arrange
    metadata = MetaData()

    users = Table(
        "users",
        metadata,
        Column("id", String(36), primary_key=True),
        Column("name", String(100)),
    )

    # Table with two FKs to users
    messages = Table(
        "messages",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("sender_id", String(36), ForeignKey("users.id")),
        Column("receiver_id", String(36), ForeignKey("users.id")),
        Column("content", String(200)),
    )

    metadata.create_all(in_memory_engine)

    with in_memory_engine.begin() as conn:
        conn.execute(
            users.insert(),
            [
                {"id": "user-1", "name": "Alice"},
                {"id": "user-2", "name": "Bob"},
            ],
        )
        conn.execute(
            messages.insert(),
            [
                {"id": 1, "sender_id": "user-1", "receiver_id": "user-2", "content": "Hello"},
                {"id": 2, "sender_id": "user-2", "receiver_id": "user-1", "content": "Hi"},
            ],
        )

    id_counter = [0]

    def generate_new_id():
        id_counter[0] += 1
        return f"new-user-{id_counter[0]}"

    # Act
    result = migrate_id_type(
        engine=in_memory_engine,
        table_name="users",
        id_generator=generate_new_id,
        id_column="id",
    )

    # Assert
    assert result["rows_migrated"] == 2
    assert result["fk_relationships_updated"] == 4  # 2 rows × 2 FK columns
    assert "messages" in result["tables_affected"]
    assert result["rows_per_table"]["users"] == 2
    assert result["rows_per_table"]["messages"] == 4  # Both sender_id and receiver_id updated


def test_migrate_id_type_with_custom_value_converter(in_memory_engine) -> None:
    """
    Test case 11: Use custom value converter for ID conversion.
    """
    # Arrange
    metadata = MetaData()

    Table(
        "products",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(100)),
    )
    metadata.create_all(in_memory_engine)

    with in_memory_engine.begin() as conn:
        conn.execute(text("INSERT INTO products (id, name) VALUES (1, 'Widget')"))
        conn.execute(text("INSERT INTO products (id, name) VALUES (2, 'Gadget')"))

    id_counter = [100]

    def generate_new_id():
        id_counter[0] += 1
        return id_counter[0]

    def int_converter(value):
        return str(int(value))

    # Act
    result = migrate_id_type(
        engine=in_memory_engine,
        table_name="products",
        id_generator=generate_new_id,
        id_column="id",
        value_converter=int_converter,
    )

    # Assert
    assert result["rows_migrated"] == 2
    assert "1" in result["id_mapping"]
    assert "2" in result["id_mapping"]
    assert result["rows_per_table"]["products"] == 2


def test_migrate_id_type_with_logger(sample_database, caplog) -> None:
    """
    Test case 12: Verify logging output during migration.
    """
    # Arrange
    engine, metadata = sample_database
    logger = logging.getLogger("test_migration")
    logger.setLevel(logging.INFO)

    def generate_new_id():
        return str(uuid.uuid4())

    # Act
    with caplog.at_level(logging.INFO, logger="test_migration"):
        result = migrate_id_type(
            engine=engine,
            table_name="users",
            id_generator=generate_new_id,
            logger=logger,
        )

    # Assert
    assert result["rows_migrated"] == 3
    assert result["fk_relationships_updated"] == 11
    assert result["rows_per_table"]["users"] == 3


def test_migrate_id_type_small_batch_size(in_memory_engine) -> None:
    """
    Test case 13: Verify batch processing with small batch size.
    """
    # Arrange
    metadata = MetaData()

    Table(
        "items",
        metadata,
        Column("id", String(36), primary_key=True),
        Column("value", Integer),
    )
    metadata.create_all(in_memory_engine)

    # Insert 10 records
    with in_memory_engine.begin() as conn:
        for i in range(10):
            conn.execute(text(f"INSERT INTO items (id, value) VALUES ('item-{i}', {i})"))

    id_counter = [0]

    def generate_new_id():
        id_counter[0] += 1
        return f"new-item-{id_counter[0]}"

    # Act - Use batch size of 3
    result = migrate_id_type(
        engine=in_memory_engine,
        table_name="items",
        id_generator=generate_new_id,
        batch_size=3,
    )

    # Assert
    assert result["rows_migrated"] == 10
    assert len(result["id_mapping"]) == 10
    assert result["rows_per_table"]["items"] == 10


def test_migrate_id_type_invalid_logger_type(in_memory_engine) -> None:
    """
    Test case 14: TypeError when logger is not Logger instance or None.
    """
    # Arrange
    expected_message = "logger must be a Logger instance or None"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        migrate_id_type(
            engine=in_memory_engine,
            table_name="users",
            id_generator=uuid.uuid4,
            logger="not_a_logger",
        )


def test_migrate_id_type_no_fk_relationships(in_memory_engine) -> None:
    """
    Test case 15: Migration succeeds when table has no FK relationships.
    """
    # Arrange
    metadata = MetaData()

    Table(
        "standalone",
        metadata,
        Column("id", String(36), primary_key=True),
        Column("data", String(100)),
    )
    metadata.create_all(in_memory_engine)

    with in_memory_engine.begin() as conn:
        conn.execute(text("INSERT INTO standalone (id, data) VALUES ('item-1', 'test')"))

    # Act
    result = migrate_id_type(
        engine=in_memory_engine,
        table_name="standalone",
        id_generator=lambda: str(uuid.uuid4()),
    )

    # Assert
    assert result["rows_migrated"] == 1
    assert result["fk_relationships_updated"] == 0
    assert len(result["tables_affected"]) == 0
    assert result["rows_per_table"]["standalone"] == 1
    assert len(result["rows_per_table"]) == 1  # Only standalone table


def test_migrate_id_type_empty_table(in_memory_engine) -> None:
    """
    Test case 16: Migration succeeds with empty table.
    """
    # Arrange
    metadata = MetaData()

    Table(
        "empty_table",
        metadata,
        Column("id", String(36), primary_key=True),
        Column("data", String(100)),
    )
    metadata.create_all(in_memory_engine)

    # Act
    result = migrate_id_type(
        engine=in_memory_engine,
        table_name="empty_table",
        id_generator=lambda: str(uuid.uuid4()),
    )

    # Assert
    assert result["rows_migrated"] == 0
    assert len(result["id_mapping"]) == 0
    assert result["rows_per_table"]["empty_table"] == 0
    assert result["fk_relationships_updated"] == 0


def test_migrate_id_type_custom_id_column_name(in_memory_engine) -> None:
    """
    Test case 17: Migration with custom ID column name.
    """
    # Arrange
    metadata = MetaData()

    Table(
        "products",
        metadata,
        Column("product_code", String(50), primary_key=True),
        Column("name", String(100)),
    )
    metadata.create_all(in_memory_engine)

    with in_memory_engine.begin() as conn:
        conn.execute(text("INSERT INTO products (product_code, name) VALUES ('P001', 'Widget')"))

    # Act
    result = migrate_id_type(
        engine=in_memory_engine,
        table_name="products",
        id_column="product_code",
        id_generator=lambda: f"NEW-{uuid.uuid4().hex[:8]}",
    )

    # Assert
    assert result["rows_migrated"] == 1
    assert "P001" in result["id_mapping"]
    assert result["rows_per_table"]["products"] == 1


def test_migrate_id_type_invalid_value_converter_type(in_memory_engine) -> None:
    """
    Test case 18: TypeError when value_converter is not callable or None.
    """
    # Arrange
    expected_message = "value_converter must be callable or None"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        migrate_id_type(
            engine=in_memory_engine,
            table_name="users",
            id_generator=uuid.uuid4,
            value_converter="not_callable",
        )


def test_migrate_id_type_invalid_id_column_type(in_memory_engine) -> None:
    """
    Test case 19: TypeError when id_column is not a string.
    """
    # Arrange
    expected_message = "id_column must be a string, got list"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        migrate_id_type(
            engine=in_memory_engine,
            table_name="users",
            id_generator=uuid.uuid4,
            id_column=[],
        )


def test_migrate_id_type_zero_batch_size(in_memory_engine) -> None:
    """
    Test case 20: ValueError when batch_size is zero.
    """
    # Arrange
    expected_message = "batch_size must be positive, got 0"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        migrate_id_type(
            engine=in_memory_engine,
            table_name="users",
            id_generator=uuid.uuid4,
            batch_size=0,
        )
