import pytest
from data_types.hash_table import HashTable


def test_insert_and_get() -> None:
    """
    Test case 1: Test inserting and retrieving key-value pairs.
    """
    hash_table = HashTable[int, str]()
    hash_table.insert(1, "one")
    hash_table.insert(2, "two")
    assert hash_table.get(1) == "one"
    assert hash_table.get(2) == "two"


def test_update_value() -> None:
    """
    Test case 2: Test updating the value of an existing key.
    """
    hash_table = HashTable[int, str]()
    hash_table.insert(1, "one")
    hash_table.insert(1, "updated_one")
    assert hash_table.get(1) == "updated_one"


def test_remove_key() -> None:
    """
    Test case 3: Test removing a key-value pair.
    """
    hash_table = HashTable[int, str]()
    hash_table.insert(1, "one")
    hash_table.remove(1)
    assert not hash_table.contains(1)


def test_contains_key() -> None:
    """
    Test case 4: Test checking if a key exists in the hash table.
    """
    hash_table = HashTable[int, str]()
    hash_table.insert(1, "one")
    assert hash_table.contains(1) is True
    assert hash_table.contains(2) is False


def test_collision_handling() -> None:
    """
    Test case 5: Test handling of hash collisions.
    """
    hash_table = HashTable[int, str](
        size=1
    )  # Force collisions by using a single bucket
    hash_table.insert(1, "one")
    hash_table.insert(2, "two")
    assert hash_table.get(1) == "one"
    assert hash_table.get(2) == "two"


def test_large_number_of_keys() -> None:
    """
    Test case 6: Test inserting and retrieving a large number of keys.
    """
    hash_table = HashTable[int, int]()
    for i in range(1000):
        hash_table.insert(i, i * 10)
    for i in range(1000):
        assert hash_table.get(i) == i * 10


def test_large_keys_and_values() -> None:
    """
    Test case 7: Test inserting and retrieving very large keys and values.
    """
    large_key = "x" * 1000  # A very large string key
    large_value = "y" * 1000  # A very large string value
    hash_table = HashTable[str, str]()
    hash_table.insert(large_key, large_value)
    assert hash_table.get(large_key) == large_value


def test_custom_key_type() -> None:
    """
    Test case 8: Test the hash table with custom key types.
    """

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
    Test case 9: Test the hash table with custom value types.
    """

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


def test_in_operator() -> None:
    """
    Test case 10: Test using the ``in`` operator with :class:`HashTable`.
    """
    hash_table = HashTable[int, str]()
    hash_table.insert(1, "one")
    assert (1 in hash_table) is True
    assert (2 in hash_table) is False
def test_empty_hash_table() -> None:
    """
    Test case 11: Test operations on an empty hash table.
    """
    hash_table = HashTable[int, str]()
    assert not hash_table.contains(1)
    with pytest.raises(KeyError, match="Key 1 not found in the hash table"):
        hash_table.get(1)


def test_get_nonexistent_key() -> None:
    """
    Test case 12: Test retrieving a value for a nonexistent key.
    """
    hash_table = HashTable[int, str]()
    with pytest.raises(KeyError, match="Key 1 not found in the hash table"):
        hash_table.get(1)


def test_remove_nonexistent_key() -> None:
    """
    Test case 13: Test removing a nonexistent key.
    """
    hash_table = HashTable[int, str]()
    with pytest.raises(KeyError, match="Key 1 not found in the hash table"):
        hash_table.remove(1)
