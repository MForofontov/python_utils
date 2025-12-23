"""
Shared pytest fixtures for database function tests.

Provides common database engines and setup utilities to avoid code duplication
across test files.
"""

from collections.abc import Generator

import pytest
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base


# Shared declarative base for all test models
Base = declarative_base()


# Common table models used across multiple tests
class Department(Base):
    """Parent table for FK relationship tests."""
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))


class Employee(Base):
    """Child table with FK to Department."""
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    dept_id = Column(Integer, ForeignKey('departments.id'))


class Project(Base):
    """Grandchild table with FK to Employee."""
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    emp_id = Column(Integer, ForeignKey('employees.id'))


class User(Base):
    """Generic user table for cardinality/statistics tests."""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    role = Column(String(20))
    status = Column(String(10))
    score = Column(Float)


class Customer(Base):
    """Customer table for column statistics tests."""
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    age = Column(Integer)
    balance = Column(Float)


class Product(Base):
    """Product table for data type optimization tests."""
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sku = Column(String(500))
    name = Column(String(100))
    description = Column(String(500))
    price = Column(Float)
    status = Column(String(20))


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
