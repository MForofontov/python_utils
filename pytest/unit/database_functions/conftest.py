"""
Shared pytest fixtures for database function tests.

Provides common database engines and setup utilities to avoid code duplication
across test files.
"""

from collections.abc import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


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
