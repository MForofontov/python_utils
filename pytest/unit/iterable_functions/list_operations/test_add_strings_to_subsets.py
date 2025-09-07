import pytest
from iterable_functions.add_strings_to_subsets import add_strings_to_subsets


def test_add_strings_to_subsets_success() -> None:
    """
    Test case 1: Test the add_strings_to_subsets function with valid inputs.
    """
    my_list: list[set[str]] = [{"a", "b"}, {"c", "d"}]
    my_strings: list[str] = ["a", "e"]
    assert add_strings_to_subsets(my_list, my_strings) == True
    assert my_list == [{"a", "b", "e"}, {"c", "d"}]


def test_add_strings_to_subsets_no_match() -> None:
    """
    Test case 2: Test the add_strings_to_subsets function when no strings match.
    """
    my_list: list[set[str]] = [{"a", "b"}, {"c", "d"}]
    my_strings: list[str] = ["e", "f"]
    assert add_strings_to_subsets(my_list, my_strings) == False
    assert my_list == [{"a", "b"}, {"c", "d"}]


def test_add_strings_to_subsets_empty_strings() -> None:
    """
    Test case 3: Test the add_strings_to_subsets function with an empty list of strings.
    """
    my_list: list[set[str]] = [{"a", "b"}, {"c", "d"}]
    my_strings: list[str] = []
    assert add_strings_to_subsets(my_list, my_strings) == False
    assert my_list == [{"a", "b"}, {"c", "d"}]


def test_add_strings_to_subsets_empty_list() -> None:
    """
    Test case 4: Test the add_strings_to_subsets function with an empty list of sets.
    """
    my_list: list[set[str]] = []
    my_strings: list[str] = ["a", "b"]
    assert add_strings_to_subsets(my_list, my_strings) == False
    assert my_list == []


def test_add_strings_to_subsets_two_empty_lists() -> None:
    """
    Test case 5: Test the add_strings_to_subsets function with two empty lists.
    """
    my_list: list[set[str]] = []
    my_strings: list[str] = []
    assert add_strings_to_subsets(my_list, my_strings) == False
    assert my_list == []


def test_add_strings_to_subsets_type_error_list() -> None:
    """
    Test case 6: Test the add_strings_to_subsets function with invalid type for my_list.
    """
    with pytest.raises(TypeError):
        add_strings_to_subsets("not a list", ["a", "b"])


def test_add_strings_to_subsets_type_error_strings() -> None:
    """
    Test case 7: Test the add_strings_to_subsets function with invalid type for my_strings.
    """
    with pytest.raises(TypeError):
        add_strings_to_subsets([{"a", "b"}], "not a list")


def test_add_strings_to_subsets_type_error_list_elements() -> None:
    """
    Test case 8: Test the add_strings_to_subsets function with invalid elements in my_list.
    """
    with pytest.raises(TypeError):
        add_strings_to_subsets([{"a", "b"}, "not a set"], ["a", "b"])


def test_add_strings_to_subsets_type_error_string_elements() -> None:
    """
    Test case 9: Test the add_strings_to_subsets function with invalid elements in my_strings.
    """
    with pytest.raises(TypeError):
        add_strings_to_subsets([{"a", "b"}], ["a", 1])
