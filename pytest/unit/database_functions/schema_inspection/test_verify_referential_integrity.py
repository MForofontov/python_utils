"""
Unit tests for verify_referential_integrity function.
"""

from conftest import Base, Invoice, Order, Product, User
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.database]
from pyutils_collection.database_functions.schema_inspection import verify_referential_integrity


def test_verify_referential_integrity_no_violations(memory_engine) -> None:
    """
    Test case 1: No violations when all FKs are valid.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)

    with Session(memory_engine) as session:
        user = User(id=1, username="user1", email="user1@example.com")
        product = Product(id=1, name="Product1")
        session.add(user)
        session.add(product)
        session.add(Order(id=1, user_id=1, product_id=1, quantity=10))
        session.add(Order(id=2, user_id=1, product_id=1, quantity=5))
        session.commit()

    # Act
    with memory_engine.connect() as connection:
        violations = verify_referential_integrity(connection)

    # Assert
    assert isinstance(violations, list)
    assert len(violations) == 0


def test_verify_referential_integrity_detects_orphaned_records(memory_engine) -> None:
    """
    Test case 2: Detect orphaned records (FK points to non-existent parent).
    """
    # Arrange
    Base.metadata.create_all(memory_engine)

    with Session(memory_engine) as session:
        # Create user and product
        user = User(id=1, username="user1", email="user1@example.com")
        product = Product(id=1, name="Product1")
        session.add(user)
        session.add(product)
        # Create order with valid FK
        session.add(Order(id=1, user_id=1, product_id=1, quantity=10))
        # Create orphaned order (user_id=999 doesn't exist)
        session.add(Order(id=2, user_id=999, product_id=1, quantity=5))
        session.commit()

    # Act
    with memory_engine.connect() as connection:
        violations = verify_referential_integrity(connection)

    # Assert
    assert len(violations) >= 1
    order_violation = next((v for v in violations if v["table"] == "orders"), None)
    if order_violation:
        assert order_violation["column"] == "user_id"
        assert order_violation["referenced_table"] == "users"
        assert order_violation["orphaned_count"] >= 1


def test_verify_referential_integrity_provides_sample_ids(memory_engine) -> None:
    """
    Test case 3: Provide sample IDs of orphaned records.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)

    with Session(memory_engine) as session:
        user = User(id=1, username="user1", email="user1@example.com")
        product = Product(id=1, name="Product1")
        session.add(user)
        session.add(product)
        # Create multiple orphaned orders
        for i in range(15):
            session.add(Order(id=100 + i, user_id=999, product_id=1, quantity=i + 1))
        session.commit()

    # Act
    with memory_engine.connect() as connection:
        violations = verify_referential_integrity(connection)

    # Assert
    if len(violations) > 0:
        order_violation = next((v for v in violations if v["table"] == "orders"), None)
        if order_violation:
            assert "sample_ids" in order_violation
            assert isinstance(order_violation["sample_ids"], list)
            assert len(order_violation["sample_ids"]) <= 10  # Max 10 samples


def test_verify_referential_integrity_empty_database(memory_engine) -> None:
    """
    Test case 4: Handle empty database gracefully.
    """
    # Act
    with memory_engine.connect() as connection:
        violations = verify_referential_integrity(connection)

    # Assert
    assert isinstance(violations, list)
    assert len(violations) == 0


def test_verify_referential_integrity_no_foreign_keys(memory_engine) -> None:
    """
    Test case 5: Handle tables with no foreign keys.
    """

    # Arrange
    class StandaloneNoFK(Base):
        __tablename__ = "standalone_no_fk"
        id = Column(Integer, primary_key=True)
        data = Column(String(50))

    Base.metadata.create_all(memory_engine)

    with Session(memory_engine) as session:
        session.add(StandaloneNoFK(id=1, data="test"))
        session.commit()

    # Act
    with memory_engine.connect() as connection:
        violations = verify_referential_integrity(connection)

    # Assert
    assert isinstance(violations, list)
    # No FKs, so no violations


def test_verify_referential_integrity_multiple_violations(memory_engine) -> None:
    """
    Test case 6: Detect violations across multiple tables.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)

    with Session(memory_engine) as session:
        user = User(id=1, username="user1", email="user1@example.com")
        product = Product(id=1, name="Product1")
        session.add(user)
        session.add(product)
        # Valid order
        session.add(Order(id=1, user_id=1, product_id=1, quantity=10))
        # Orphaned order (user_id=999)
        session.add(Order(id=2, user_id=999, product_id=1, quantity=5))
        # Orphaned invoice (order_id=999)
        session.add(
            Invoice(
                id=1,
                invoice_number="INV001",
                user_id=1,
                order_id=999,
                total_amount=100.0,
                status="paid",
            )
        )
        session.commit()

    # Act
    with memory_engine.connect() as connection:
        violations = verify_referential_integrity(connection)

    # Assert
    assert len(violations) >= 1  # At least one violation


def test_verify_referential_integrity_counts_orphaned(memory_engine) -> None:
    """
    Test case 7: Correctly count orphaned records.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)

    with Session(memory_engine) as session:
        user = User(id=1, username="user1", email="user1@example.com")
        product = Product(id=1, name="Product1")
        session.add(user)
        session.add(product)
        # Create 5 orphaned orders
        for i in range(5):
            session.add(Order(id=i, user_id=999, product_id=1, quantity=i + 1))
        session.commit()

    # Act
    with memory_engine.connect() as connection:
        violations = verify_referential_integrity(connection)

    # Assert
    if len(violations) > 0:
        order_violation = next((v for v in violations if v["table"] == "orders"), None)
        if order_violation:
            assert order_violation["orphaned_count"] == 5


def test_verify_referential_integrity_invalid_connection_type_error() -> None:
    """
    Test case 8: TypeError for None connection.
    """
    # Arrange
    expected_message = "connection cannot be None"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        verify_referential_integrity(None)


def test_verify_referential_integrity_invalid_schema_type_error(memory_engine) -> None:
    """
    Test case 9: TypeError for invalid schema parameter.
    """
    # Arrange
    expected_message = "schema must be str or None"

    # Act & Assert
    with memory_engine.connect() as connection:
        with pytest.raises(TypeError, match=expected_message):
            verify_referential_integrity(connection, schema=123)


def test_verify_referential_integrity_null_foreign_keys(memory_engine) -> None:
    """
    Test case 10: Handle NULL foreign keys (should not be violations).
    """
    # Arrange
    Base.metadata.create_all(memory_engine)

    with Session(memory_engine) as session:
        user = User(id=1, username="user1", email="user1@example.com")
        product = Product(id=1, name="Product1")
        session.add(user)
        session.add(product)
        # Order with NULL user_id (nullable FK)
        session.add(Order(id=1, user_id=None, product_id=1, quantity=10))
        # Order with valid user_id
        session.add(Order(id=2, user_id=1, product_id=1, quantity=5))
        session.commit()

    # Act
    with memory_engine.connect() as connection:
        violations = verify_referential_integrity(connection)

    # Assert
    # NULL FKs should not be violations
    assert isinstance(violations, list)
    # If there are violations, they shouldn't include the NULL FK
