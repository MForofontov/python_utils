"""Unit tests for SkipList class."""
from unittest.mock import MagicMock, patch

from data_types.skip_list import SkipList, SkipNode


def test_skip_list_initialization() -> None:
    """
    Test case 1: SkipList initialization.
    """
    # Act
    skip_list = SkipList(max_level=4)

    # Assert
    assert skip_list.max_level == 4
    assert skip_list.level == 0
    assert skip_list.header is not None
    assert skip_list.header.key == -1


def test_skip_list_insert_single_element() -> None:
    """
    Test case 2: Insert single element into skip list.
    """
    # Arrange
    skip_list = SkipList(max_level=4)

    # Act
    skip_list.insert(10)

    # Assert
    result = skip_list.search(10)
    assert result is not None
    assert result.key == 10


def test_skip_list_insert_multiple_elements() -> None:
    """
    Test case 3: Insert multiple elements.
    """
    # Arrange
    skip_list = SkipList(max_level=4)

    # Act
    values = [10, 20, 5, 15, 25]
    for val in values:
        skip_list.insert(val)

    # Assert
    for val in values:
        result = skip_list.search(val)
        assert result is not None
        assert result.key == val


def test_skip_list_search_nonexistent() -> None:
    """
    Test case 4: Search for non-existent element.
    """
    # Arrange
    skip_list = SkipList(max_level=4)
    skip_list.insert(10)
    skip_list.insert(20)

    # Act
    result = skip_list.search(15)

    # Assert
    assert result is None


def test_skip_list_delete_existing_element() -> None:
    """
    Test case 5: Delete existing element.
    """
    # Arrange
    skip_list = SkipList(max_level=4)
    skip_list.insert(10)
    skip_list.insert(20)
    skip_list.insert(30)

    # Act
    skip_list.delete(20)
    result = skip_list.search(20)

    # Assert
    assert result is None
    assert skip_list.search(10) is not None
    assert skip_list.search(30) is not None


def test_skip_list_delete_nonexistent() -> None:
    """
    Test case 6: Delete non-existent element (no error).
    """
    # Arrange
    skip_list = SkipList(max_level=4)
    skip_list.insert(10)

    # Act & Assert (should not raise)
    skip_list.delete(20)
    assert skip_list.search(10) is not None


def test_skip_node_initialization() -> None:
    """
    Test case 7: SkipNode initialization.
    """
    # Act
    node = SkipNode(key=42, level=3)

    # Assert
    assert node.key == 42
    assert len(node.forward) == 4  # level + 1


@patch("random.random")
def test_skip_list_random_level(mock_random: MagicMock) -> None:
    """
    Test case 8: Random level generation.
    """
    # Arrange
    skip_list = SkipList(max_level=4)
    mock_random.side_effect = [0.3, 0.3, 0.6]  # Two successes, then fail

    # Act
    level = skip_list.random_level()

    # Assert
    assert level == 2
