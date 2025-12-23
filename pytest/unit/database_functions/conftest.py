"""
Shared pytest fixtures for database function tests.

Provides common database engines and setup utilities to avoid code duplication
across test files.
"""

from collections.abc import Generator
from typing import Any

import pytest
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Index, Text
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.orm import declarative_base, Session


# Shared declarative base for all test models
Base = declarative_base()


# Core table models - minimal set to cover all test scenarios
class User(Base):
    """Generic user table - covers most test scenarios including duplicate detection."""
    __tablename__ = 'users'
    __table_args__ = (
        Index('idx_user_email', 'email'),
        Index('idx_user_username', 'username'),
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
    __tablename__ = 'products'
    __table_args__ = (
        Index('idx_product_name', 'name'),
        Index('idx_product_category', 'category'),
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
    __tablename__ = 'orders'
    __table_args__ = (
        Index('idx_order_product', 'product_id'),  # Only product_id has index
    )
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=True)  # No index!
    quantity = Column(Integer, nullable=False)


class Transaction(Base):
    """Transaction table - for column statistics and unused column tests."""
    __tablename__ = 'transactions'
    __table_args__ = (
        Index('idx_transaction_ref', 'reference'),
    )
    
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
    __tablename__ = 'invoices'
    __table_args__ = (
        Index('idx_invoice_user', 'user_id'),
        Index('idx_invoice_order', 'order_id'),
        Index('idx_invoice_number', 'invoice_number'),
    )
    
    id = Column(Integer, primary_key=True)
    invoice_number = Column(String(50), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete='SET NULL'), nullable=True)
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
def empty_engine() -> Generator[Engine, None, None]:
    """
    Fixture providing an empty SQLite in-memory database engine.
    
    Alias for memory_engine with semantic meaning - use this when you need
    an empty database to create tables in.
    
    Yields
    ------
    Engine
        SQLAlchemy engine connected to an empty in-memory SQLite database.
    """
    engine = create_engine("sqlite:///:memory:")
    yield engine
    engine.dispose()


@pytest.fixture
def test_engine() -> Generator[Engine, None, None]:
    """
    Fixture providing a pre-populated test database engine.
    
    Use this when you need a database with test data already loaded.
    For empty databases, use empty_engine instead.
    
    Yields
    ------
    Engine
        SQLAlchemy engine connected to an in-memory SQLite database.
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


@pytest.fixture
def base_metadata():
    """
    Fixture providing access to the shared Base metadata.
    
    Use this to create all tables defined in conftest.py models.
    
    Returns
    -------
    DeclarativeMeta
        The shared declarative base with common table models.
    
    Examples
    --------
    >>> def test_with_tables(memory_engine, base_metadata):
    ...     base_metadata.metadata.create_all(memory_engine)
    ...     # Tables now exist in memory_engine
    """
    return Base


@pytest.fixture
def db_connection(memory_engine: Engine) -> Generator[Connection, None, None]:
    """
    Fixture providing a database connection from memory_engine.
    
    Parameters
    ----------
    memory_engine : Engine
        The SQLAlchemy engine to create connection from.
    
    Yields
    ------
    Connection
        Active database connection that will be closed after test.
    
    Examples
    --------
    >>> def test_with_connection(db_connection):
    ...     result = db_connection.execute("SELECT 1")
    """
    connection = memory_engine.connect()
    yield connection
    connection.close()


@pytest.fixture
def db_session(memory_engine: Engine) -> Generator[Session, None, None]:
    """
    Fixture providing a database session from memory_engine.
    
    Parameters
    ----------
    memory_engine : Engine
        The SQLAlchemy engine to create session from.
    
    Yields
    ------
    Session
        Active database session that will be closed after test.
    
    Examples
    --------
    >>> def test_with_session(db_session):
    ...     user = User(username="test")
    ...     db_session.add(user)
    ...     db_session.commit()
    """
    session = Session(memory_engine)
    yield session
    session.close()


@pytest.fixture
def populated_db(memory_engine: Engine) -> Generator[tuple[Engine, Connection], None, None]:
    """
    Fixture providing a database with common tables already created.
    
    Creates all tables from the Base metadata and provides both
    the engine and a connection.
    
    Parameters
    ----------
    memory_engine : Engine
        The SQLAlchemy engine to use.
    
    Yields
    ------
    tuple[Engine, Connection]
        Tuple of (engine, connection) with tables created.
    
    Examples
    --------
    >>> def test_with_populated_db(populated_db):
    ...     engine, conn = populated_db
    ...     # All Base tables exist, ready to insert data
    """
    Base.metadata.create_all(memory_engine)
    connection = memory_engine.connect()
    yield memory_engine, connection
    connection.close()


@pytest.fixture
def dual_connections(dual_engines: tuple[Engine, Engine]) -> Generator[tuple[Connection, Connection], None, None]:
    """
    Fixture providing two database connections for comparison tests.
    
    Parameters
    ----------
    dual_engines : tuple[Engine, Engine]
        Two separate database engines.
    
    Yields
    ------
    tuple[Connection, Connection]
        Tuple of (conn1, conn2) - two independent database connections.
    
    Examples
    --------
    >>> def test_compare_data(dual_connections):
    ...     conn1, conn2 = dual_connections
    ...     # Compare data between databases
    """
    engine1, engine2 = dual_engines
    conn1 = engine1.connect()
    conn2 = engine2.connect()
    yield conn1, conn2
    conn1.close()
    conn2.close()


@pytest.fixture
def schema_dict() -> dict[str, Any]:
    """
    Fixture providing expected schema dictionary for User and Product tables.
    
    Returns
    -------
    dict[str, Any]
        Dictionary with expected schema structure for common tables.
    
    Examples
    --------
    >>> def test_schema_drift(db_connection, schema_dict):
    ...     result = detect_schema_drift(db_connection, schema_dict)
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
                {"name": "score", "type": "FLOAT"}
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


# Export Base for use in test files
__all__ = [
    'Base', 
    'User', 
    'Product', 
    'Order',
    'Transaction',
    'Invoice',
]
