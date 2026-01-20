"""
List comparison utilities.

Functions for comparing lists, finding common elements, checking for
sublists, and performing various list matching operations.
"""

from .all_match_lists import all_match_lists
from .any_match_lists import any_match_lists
from .contains_sublist import contains_sublist
from .find_sublist_index import find_sublist_index
from .get_common_elements_in_lists import get_common_elements_in_lists
from .partially_contains_fragment_of_list import partially_contains_fragment_of_list
from .partially_contains_sublist import partially_contains_sublist

__all__ = [
    "all_match_lists",
    "any_match_lists",
    "contains_sublist",
    "find_sublist_index",
    "get_common_elements_in_lists",
    "partially_contains_fragment_of_list",
    "partially_contains_sublist",
]
