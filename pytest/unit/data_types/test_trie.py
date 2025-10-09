"""Unit tests for Trie class."""
from data_types.trie import Trie, TrieNode


def test_trie_initialization() -> None:
    """
    Test case 1: Trie initialization.
    """
    # Act
    trie = Trie()

    # Assert
    assert trie.root is not None
    assert len(trie.root.children) == 0
    assert trie.root.is_end_of_word is False


def test_trie_insert_single_word() -> None:
    """
    Test case 2: Insert single word.
    """
    # Arrange
    trie = Trie()

    # Act
    trie.insert("hello")

    # Assert
    assert trie.search("hello") is True


def test_trie_insert_multiple_words() -> None:
    """
    Test case 3: Insert multiple words.
    """
    # Arrange
    trie = Trie()
    words = ["hello", "world", "hi", "help"]

    # Act
    for word in words:
        trie.insert(word)

    # Assert
    for word in words:
        assert trie.search(word) is True


def test_trie_search_nonexistent() -> None:
    """
    Test case 4: Search for non-existent word.
    """
    # Arrange
    trie = Trie()
    trie.insert("hello")

    # Act & Assert
    assert trie.search("hell") is False
    assert trie.search("hellos") is False
    assert trie.search("world") is False


def test_trie_search_prefix_not_word() -> None:
    """
    Test case 5: Search for prefix that isn't a complete word.
    """
    # Arrange
    trie = Trie()
    trie.insert("hello")

    # Act & Assert
    assert trie.search("hel") is False


def test_trie_starts_with_existing_prefix() -> None:
    """
    Test case 6: Check if prefix exists.
    """
    # Arrange
    trie = Trie()
    trie.insert("hello")
    trie.insert("help")

    # Act & Assert
    assert trie.starts_with("hel") is True
    assert trie.starts_with("hello") is True
    assert trie.starts_with("help") is True


def test_trie_starts_with_nonexistent_prefix() -> None:
    """
    Test case 7: Check for non-existent prefix.
    """
    # Arrange
    trie = Trie()
    trie.insert("hello")

    # Act & Assert
    assert trie.starts_with("world") is False
    assert trie.starts_with("x") is False


def test_trie_empty_string() -> None:
    """
    Test case 8: Insert and search empty string.
    """
    # Arrange
    trie = Trie()

    # Act
    trie.insert("")

    # Assert
    assert trie.search("") is True
    assert trie.starts_with("") is True


def test_trie_node_initialization() -> None:
    """
    Test case 9: TrieNode initialization.
    """
    # Act
    node = TrieNode()

    # Assert
    assert len(node.children) == 0
    assert node.is_end_of_word is False


def test_trie_insert_overlapping_words() -> None:
    """
    Test case 10: Insert overlapping words.
    """
    # Arrange
    trie = Trie()

    # Act
    trie.insert("app")
    trie.insert("apple")
    trie.insert("application")

    # Assert
    assert trie.search("app") is True
    assert trie.search("apple") is True
    assert trie.search("application") is True
    assert trie.starts_with("app") is True


def test_trie_insert_special_characters() -> None:
    """
    Test case 11: Insert words with special characters.
    """
    # Arrange
    trie = Trie()

    # Act
    trie.insert("hello-world")
    trie.insert("test@123")
    trie.insert("foo_bar")

    # Assert
    assert trie.search("hello-world") is True
    assert trie.search("test@123") is True
    assert trie.search("foo_bar") is True


def test_trie_insert_numbers() -> None:
    """
    Test case 12: Insert numeric strings.
    """
    # Arrange
    trie = Trie()

    # Act
    trie.insert("123")
    trie.insert("456")

    # Assert
    assert trie.search("123") is True
    assert trie.search("456") is True
    assert trie.search("789") is False


def test_trie_case_sensitive() -> None:
    """
    Test case 13: Verify Trie is case-sensitive.
    """
    # Arrange
    trie = Trie()

    # Act
    trie.insert("Hello")
    trie.insert("hello")

    # Assert
    assert trie.search("Hello") is True
    assert trie.search("hello") is True
    assert trie.search("HELLO") is False


def test_trie_single_character_words() -> None:
    """
    Test case 14: Insert and search single character words.
    """
    # Arrange
    trie = Trie()

    # Act
    trie.insert("a")
    trie.insert("b")
    trie.insert("c")

    # Assert
    assert trie.search("a") is True
    assert trie.search("b") is True
    assert trie.search("c") is True
    assert trie.search("d") is False


def test_trie_very_long_word() -> None:
    """
    Test case 15: Insert and search very long word.
    """
    # Arrange
    trie = Trie()
    long_word = "a" * 1000

    # Act
    trie.insert(long_word)

    # Assert
    assert trie.search(long_word) is True
    assert trie.starts_with("a" * 500) is True


def test_trie_insert_duplicate_word() -> None:
    """
    Test case 16: Insert same word multiple times.
    """
    # Arrange
    trie = Trie()

    # Act
    trie.insert("test")
    trie.insert("test")
    trie.insert("test")

    # Assert
    assert trie.search("test") is True
