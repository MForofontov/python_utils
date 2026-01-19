import pytest

pytestmark = [pytest.mark.unit, pytest.mark.testing]
from python_utils.testing_functions.mock_helpers.create_mock_object import create_mock_object


def test_create_mock_object_single_attribute() -> None:
    """
    Test case 1: Create mock with single attribute.
    """
    # Act
    mock = create_mock_object(name="test")

    # Assert
    assert mock.name == "test"


def test_create_mock_object_multiple_attributes() -> None:
    """
    Test case 2: Create mock with multiple attributes.
    """
    # Act
    mock = create_mock_object(name="test", value=42, active=True)

    # Assert
    assert mock.name == "test"
    assert mock.value == 42
    assert mock.active is True


def test_create_mock_object_complex_attributes() -> None:
    """
    Test case 3: Create mock with complex attributes.
    """
    # Act
    mock = create_mock_object(
        data=[1, 2, 3], config={"key": "value"}, callback=lambda x: x * 2
    )

    # Assert
    assert mock.data == [1, 2, 3]
    assert mock.config == {"key": "value"}
    assert mock.callback(5) == 10


def test_create_mock_object_no_attributes() -> None:
    """
    Test case 4: Create mock with no attributes.
    """
    # Act
    mock = create_mock_object()

    # Assert
    assert hasattr(mock, "_mock_name")  # Mock object exists


def test_create_mock_object_nested_objects() -> None:
    """
    Test case 5: Create mock with nested object attributes.
    """
    # Act
    inner_mock = create_mock_object(id=1)
    mock = create_mock_object(nested=inner_mock)

    # Assert
    assert mock.nested.id == 1


def test_create_mock_object_override_attribute() -> None:
    """
    Test case 6: Create mock and later modify attribute.
    """
    # Act
    mock = create_mock_object(value=10)
    mock.value = 20

    # Assert
    assert mock.value == 20
