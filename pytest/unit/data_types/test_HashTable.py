import pytest
from data_types.hash_table import HashTable


def test_insert_and_get() -> None:
    """
    Test inserting and retrieving key-value pairs.
    """
    # Test case 1: Insert and get
    hash_table = HashTable[int, str]()
    hash_table.insert(1, "one")
    hash_table.insert(2, "two")
    assert hash_table.get(1) == "one"
    assert hash_table.get(2) == "two"


def test_update_value() -> None:
    """
    Test updating the value of an existing key.
    """
    # Test case 2: Update value
    hash_table = HashTable[int, str]()
    hash_table.insert(1, "one")
    hash_table.insert(1, "updated_one")
    assert hash_table.get(1) == "updated_one"


def test_remove_key() -> None:
    """
    Test removing a key-value pair.
    """
    # Test case 3: Remove key
    hash_table = HashTable[int, str]()
    hash_table.insert(1, "one")
    hash_table.remove(1)
    assert not hash_table.contains(1)


def test_contains_key() -> None:
    """
    Test checking if a key exists in the hash table.
    """
    # Test case 4: Contains key
    hash_table = HashTable[int, str]()
    hash_table.insert(1, "one")
    assert hash_table.contains(1) is True
    assert hash_table.contains(2) is False


def test_collision_handling() -> None:
    """
    Test handling of hash collisions.
    """
    # Test case 5: Collision handling
    hash_table = HashTable[int, str](
        size=1
    )  # Force collisions by using a single bucket
    hash_table.insert(1, "one")
    hash_table.insert(2, "two")
    assert hash_table.get(1) == "one"
    assert hash_table.get(2) == "two"


def test_large_number_of_keys() -> None:
    """
    Test inserting and retrieving a large number of keys.
    """
    # Test case 6: Large number of keys
    hash_table = HashTable[int, int]()
    for i in range(1000):
        hash_table.insert(i, i * 10)
    for i in range(1000):
        assert hash_table.get(i) == i * 10


def test_large_keys_and_values() -> None:
    """
    Test inserting and retrieving very large keys and values.
    """
    # Test case 7: Large keys and values
    large_key = "x" * 1000  # A very large string key
    large_value = "y" * 1000  # A very large string value
    hash_table = HashTable[str, str]()
    hash_table.insert(large_key, large_value)
    assert hash_table.get(large_key) == large_value


def test_custom_key_type() -> None:
    """
    Test the hash table with custom key types.
    """

    # Test case 8: Custom key type
    class CustomKey:
        def __init__(self, key: int) -> None:
            self.key = key

        def __hash__(self) -> int:
            return hash(self.key)

        def __eq__(self, other: object) -> bool:
            if isinstance(other, CustomKey):
                return self.key == other.key
            return False

    hash_table = HashTable[CustomKey, str]()
    key1 = CustomKey(1)
    key2 = CustomKey(2)
    hash_table.insert(key1, "one")
    hash_table.insert(key2, "two")
    assert hash_table.get(key1) == "one"
    assert hash_table.get(key2) == "two"


def test_custom_value_type() -> None:
    """
    Test the hash table with custom value types.
    """

    # Test case 9: Custom value type
    class CustomValue:
        def __init__(self, value: int) -> None:
            self.value = value

        def __eq__(self, other: object) -> bool:
            if isinstance(other, CustomValue):
                return self.value == other.value
            return False

    hash_table = HashTable[int, CustomValue]()
    hash_table.insert(1, CustomValue(100))
    hash_table.insert(2, CustomValue(200))
    assert hash_table.get(1).value == 100
    assert hash_table.get(2).value == 200


def test_empty_hash_table() -> None:
    """
    Test operations on an empty hash table.
    """
    # Test case 10: Empty hash table
    hash_table = HashTable[int, str]()
    assert not hash_table.contains(1)
    with pytest.raises(KeyError, match="Key 1 not found in the hash table"):
        hash_table.get(1)


def test_get_nonexistent_key() -> None:
    """
    Test retrieving a value for a nonexistent key.
    """
    # Test case 11: Get nonexistent key
    hash_table = HashTable[int, str]()
    with pytest.raises(KeyError, match="Key 1 not found in the hash table"):
        hash_table.get(1)


def test_remove_nonexistent_key() -> None:
    """
    Test removing a nonexistent key.
    """
    # Test case 12: Remove nonexistent key
    hash_table = HashTable[int, str]()
    with pytest.raises(KeyError, match="Key 1 not found in the hash table"):
        hash_table.remove(1)
