"""
Set operation utilities.

Functions for working with sets, including set comparisons,
conversions, shared elements, cartesian products, power sets,
partitions, and combinations.
"""

from .check_if_all_sets_are_same import check_if_all_sets_are_same
from .convert_set_elements_to_strings import convert_set_elements_to_strings
from .get_shared_elements import get_shared_elements
from .set_symmetric_difference import set_symmetric_difference
from .get_unique_elements_across_sets import get_unique_elements_across_sets
from .set_cartesian_product import set_cartesian_product
from .set_cartesian_product_as_list import set_cartesian_product_as_list
from .set_power_set import set_power_set
from .set_power_set_as_lists import set_power_set_as_lists
from .get_subsets_of_size import get_subsets_of_size
from .set_partition import partition_set_by_predicate
from .partition_set_into_n_parts import partition_set_into_n_parts
from .get_set_partitions import get_set_partitions
from .partition_set_by_sizes import partition_set_by_sizes
from .get_combinations import get_combinations
from .get_combinations_with_replacement import get_combinations_with_replacement
from .get_permutations import get_permutations
from .count_combinations import count_combinations

__all__ = [
    'check_if_all_sets_are_same',
    'convert_set_elements_to_strings',
    'get_shared_elements',
    'set_symmetric_difference',
    'get_unique_elements_across_sets',
    'set_cartesian_product',
    'set_cartesian_product_as_list',
    'set_power_set',
    'set_power_set_as_lists',
    'get_subsets_of_size',
    'partition_set_by_predicate',
    'partition_set_into_n_parts',
    'get_set_partitions',
    'partition_set_by_sizes',
    'get_combinations',
    'get_combinations_with_replacement',
    'get_permutations',
    'count_combinations',
]