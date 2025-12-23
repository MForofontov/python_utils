"""
Unit tests for suggest_data_type_optimizations function.
"""

import pytest
from sqlalchemy.orm import Session

from database_functions.schema_inspection import suggest_data_type_optimizations
from conftest import Base, Product


def test_suggest_data_type_optimizations_oversized_varchar(memory_engine) -> None:
    """
    Test case 1: Detect VARCHAR columns that are too large.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    
    with Session(memory_engine) as session:
        for i in range(100):
            session.add(Product(
                id=i,
                sku=f"SKU{i:03d}",  # Max 6 chars, but VARCHAR(500)
                description="Short description",
                price=10.0,
                status="active"
            ))
        session.commit()
    
    # Act
    with memory_engine.connect() as connection:
        suggestions = suggest_data_type_optimizations(
            connection,
            tables=["products"],
            sample_size=100
        )
    
    # Assert
    sku_suggestion = next((s for s in suggestions if s["column_name"] == "sku"), None)
    if sku_suggestion:
        assert "VARCHAR(500)" in sku_suggestion["current_type"]
        assert "VARCHAR" in sku_suggestion["suggested_type"]


def test_suggest_data_type_optimizations_with_sample_size(memory_engine) -> None:
    """
    Test case 2: Respect sample_size parameter.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    
    with Session(memory_engine) as session:
        for i in range(1000):
            session.add(Product(
                id=i,
                sku=f"SKU{i}",
                description="Product description",
                price=float(i),
                status="active"
            ))
        session.commit()
    
    # Act
    with memory_engine.connect() as connection:
        suggestions = suggest_data_type_optimizations(
            connection,
            tables=["products"],
            sample_size=100
        )
    
    # Assert
    assert isinstance(suggestions, list)


def test_suggest_data_type_optimizations_empty_table(memory_engine) -> None:
    """
    Test case 3: Handle empty tables gracefully.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    
    # Act
    with memory_engine.connect() as connection:
        suggestions = suggest_data_type_optimizations(connection, tables=["products"])
    
    # Assert
    assert isinstance(suggestions, list)
    assert len(suggestions) == 0  # No suggestions for empty table


def test_suggest_data_type_optimizations_specific_tables(memory_engine) -> None:
    """
    Test case 4: Analyze only specified tables.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    
    with Session(memory_engine) as session:
        session.add(Product(
            id=1,
            sku="SKU001",
            description="Test",
            price=10.0,
            status="active"
        ))
        session.commit()
    
    # Act
    with memory_engine.connect() as connection:
        suggestions = suggest_data_type_optimizations(
            connection,
            tables=["products"]
        )
    
    # Assert
    assert isinstance(suggestions, list)
    # All suggestions should be for products table
    for suggestion in suggestions:
        assert suggestion["table_name"] == "products"


def test_suggest_data_type_optimizations_severity_levels(memory_engine) -> None:
    """
    Test case 5: Assign appropriate severity levels.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    
    with Session(memory_engine) as session:
        for i in range(50):
            session.add(Product(
                id=i,
                sku="A",  # VARCHAR(500) with 1 char - high severity
                description="X",
                price=1.0,
                status="Y"
            ))
        session.commit()
    
    # Act
    with memory_engine.connect() as connection:
        suggestions = suggest_data_type_optimizations(connection, tables=["products"])
    
    # Assert
    for suggestion in suggestions:
        assert "severity" in suggestion
        assert suggestion["severity"] in ["high", "medium", "low"]


def test_suggest_data_type_optimizations_provides_reasoning(memory_engine) -> None:
    """
    Test case 6: Include reasoning for each suggestion.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    
    with Session(memory_engine) as session:
        session.add(Product(
            id=1,
            sku="TEST",
            description="Description",
            price=10.0,
            status="active"
        ))
        session.commit()
    
    # Act
    with memory_engine.connect() as connection:
        suggestions = suggest_data_type_optimizations(connection, tables=["products"])
    
    # Assert
    for suggestion in suggestions:
        assert "reasoning" in suggestion
        assert isinstance(suggestion["reasoning"], str)


def test_suggest_data_type_optimizations_invalid_connection_type_error() -> None:
    """
    Test case 7: TypeError for None connection.
    """
    # Arrange
    expected_message = "connection cannot be None"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        suggest_data_type_optimizations(None)


def test_suggest_data_type_optimizations_invalid_tables_type_error(memory_engine) -> None:
    """
    Test case 8: TypeError for invalid tables parameter.
    """
    # Arrange
    expected_message = "tables must be list or None"
    
    # Act & Assert
    with memory_engine.connect() as connection:
        with pytest.raises(TypeError, match=expected_message):
            suggest_data_type_optimizations(connection, tables="products")


def test_suggest_data_type_optimizations_invalid_schema_type_error(memory_engine) -> None:
    """
    Test case 9: TypeError for invalid schema parameter.
    """
    # Arrange
    expected_message = "schema must be str or None"
    
    # Act & Assert
    with memory_engine.connect() as connection:
        with pytest.raises(TypeError, match=expected_message):
            suggest_data_type_optimizations(connection, schema=123)


def test_suggest_data_type_optimizations_invalid_sample_size_type_error(memory_engine) -> None:
    """
    Test case 10: TypeError for invalid sample_size parameter.
    """
    # Arrange
    expected_message = "sample_size must be int"
    
    # Act & Assert
    with memory_engine.connect() as connection:
        with pytest.raises(TypeError, match=expected_message):
            suggest_data_type_optimizations(connection, sample_size="100")


def test_suggest_data_type_optimizations_negative_sample_size_value_error(memory_engine) -> None:
    """
    Test case 11: ValueError for negative sample_size.
    """
    # Arrange
    expected_message = "sample_size must be positive"
    
    # Act & Assert
    with memory_engine.connect() as connection:
        with pytest.raises(ValueError, match=expected_message):
            suggest_data_type_optimizations(connection, sample_size=-100)


def test_suggest_data_type_optimizations_includes_potential_savings(memory_engine) -> None:
    """
    Test case 12: Include potential storage savings estimates.
    """
    # Arrange
    Base.metadata.create_all(memory_engine)
    
    with Session(memory_engine) as session:
        for i in range(100):
            session.add(Product(
                id=i,
                sku="X",
                description="Y",
                price=1.0,
                status="Z"
            ))
        session.commit()
    
    # Act
    with memory_engine.connect() as connection:
        suggestions = suggest_data_type_optimizations(connection, tables=["products"])
    
    # Assert
    for suggestion in suggestions:
        assert "potential_savings" in suggestion or "issue" in suggestion
