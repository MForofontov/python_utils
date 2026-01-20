"""
Shared pytest fixtures for database function tests.

Provides common database engines and setup utilities to avoid code duplication
across test files.
"""

from collections.abc import Generator

import pytest

# Skip all tests in this directory if sqlalchemy is not installed
pytest.importorskip("sqlalchemy")

from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base

# Shared declarative base for all test models
Base = declarative_base()


# Core table models - minimal set to cover all test scenarios
class User(Base):
    """Generic user table - covers most test scenarios including duplicate detection."""

    __tablename__ = "users"
    __table_args__ = (
        Index("idx_user_email", "email"),
        Index("idx_user_username", "username"),
    )

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    role = Column(String(20), nullable=True)
    status = Column(String(10), nullable=True)
    age = Column(Integer, nullable=True)
    city = Column(String(50), nullable=True)
    balance = Column(Float, nullable=True)


class Product(Base):
    """Product table - covers sizing, ordering, optimization, and content tests."""

    __tablename__ = "products"
    __table_args__ = (
        Index("idx_product_name", "name"),
        Index("idx_product_category", "category"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    sku = Column(String(500), nullable=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=True)
    description = Column(String(500), nullable=True)
    title = Column(String(200), nullable=True)
    content = Column(Text, nullable=True)
    price = Column(Float, nullable=True)
    quantity = Column(Integer, nullable=True)
    status = Column(String(20), nullable=True)


class Order(Base):
    """Order table - child table with FK for relationship testing.
    Note: user_id has NO index to test find_missing_indexes function."""

    __tablename__ = "orders"
    __table_args__ = (
        Index("idx_order_product", "product_id"),  # Only product_id has index
    )

    id = Column(Integer, primary_key=True)
    product_id = Column(
        Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=True
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True
    )  # No index!
    quantity = Column(Integer, nullable=False)


class Transaction(Base):
    """Transaction table - for column statistics and unused column tests."""

    __tablename__ = "transactions"
    __table_args__ = (Index("idx_transaction_ref", "reference"),)

    id = Column(Integer, primary_key=True)
    transaction_type = Column(String(100), nullable=False)
    reference = Column(String(100), nullable=False)
    payment_method = Column(String(20), nullable=True)
    description = Column(String(500), nullable=True)
    amount = Column(Integer, nullable=True)
    balance = Column(Float, nullable=True)
    merchant_id = Column(String(100), nullable=True)
    customer_notes = Column(String(100), nullable=True)
    receipt_url = Column(String(50), nullable=True)
    promo_code = Column(String(50), nullable=True)
    gift_message = Column(String(50), nullable=True)


class Invoice(Base):
    """Invoice table - child of User and Order for testing FK chains."""

    __tablename__ = "invoices"
    __table_args__ = (
        Index("idx_invoice_user", "user_id"),
        Index("idx_invoice_order", "order_id"),
        Index("idx_invoice_number", "invoice_number"),
    )

    id = Column(Integer, primary_key=True)
    invoice_number = Column(String(50), nullable=False, unique=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    order_id = Column(
        Integer, ForeignKey("orders.id", ondelete="SET NULL"), nullable=True
    )
    total_amount = Column(Float, nullable=False)
    status = Column(String(20), nullable=False)


@pytest.fixture
def memory_engine() -> Generator[Engine, None, None]:
    """
    Fixture providing a fresh SQLite in-memory database engine for each test.

    Yields
    ------
    Engine
        SQLAlchemy engine connected to an in-memory SQLite database.

    Examples
    --------
    >>> def test_something(memory_engine):
    ...     metadata = MetaData()
    ...     table = Table('test', metadata, Column('id', Integer, primary_key=True))
    ...     metadata.create_all(memory_engine)
    """
    engine = create_engine("sqlite:///:memory:")
    yield engine
    engine.dispose()


@pytest.fixture
def dual_engines() -> Generator[tuple[Engine, Engine], None, None]:
    """
    Fixture providing two separate database engines for comparison tests.

    Useful for testing schema comparison, data synchronization, etc.

    Yields
    ------
    tuple[Engine, Engine]
        Tuple of (engine1, engine2) - two independent SQLite databases.

    Examples
    --------
    >>> def test_compare_schemas(dual_engines):
    ...     engine1, engine2 = dual_engines
    ...     # Create different schemas in each
    ...     # Compare them
    """
    engine1 = create_engine("sqlite:///:memory:")
    engine2 = create_engine("sqlite:///:memory:")
    yield engine1, engine2
    engine1.dispose()
    engine2.dispose()


# Export Base for use in test files
__all__ = [
    "Base",
    "User",
    "Product",
    "Order",
    "Transaction",
    "Invoice",
]
