from collections.abc import Hashable
from typing import Generic, TypeVar

T = TypeVar("T", bound=Hashable)


class UnionFind(Generic[T]):
    """
    A Union-Find (Disjoint Set) data structure.

    Attributes
    ----------
    parent : dict[T, T]
        A dictionary that maps each element to its parent.
    rank : dict[T, int]
        A dictionary that stores the rank (or depth) of each element's tree.

    Methods
    -------
    find(element: T) -> T
        Finds the representative of the set containing the element.
    union(element1: T, element2: T) -> None
        Merges the sets containing the two elements.
    connected(element1: T, element2: T) -> bool
        Checks if the two elements are in the same set.
    """

    def __init__(self) -> None:
        self.parent: dict[T, T] = {}
        self.rank: dict[T, int] = {}

    def find(self, element: T) -> T:
        """
        Finds the representative of the set containing the element.

        Parameters
        ----------
        element : T
            The element to find.

        Returns
        -------
        T
            The representative (root) of the set containing the element.
        """
        if self.parent.get(element) != element:
            self.parent[element] = self.find(self.parent[element])
        return self.parent.get(element, element)

    def union(self, element1: T, element2: T) -> None:
        """
        Merges the sets containing the two elements.

        Parameters
        ----------
        element1 : T
            The first element.
        element2 : T
            The second element.
        """
        root1 = self.find(element1)
        root2 = self.find(element2)

        if root1 != root2:
            # Union by rank
            if self.rank.get(root1, 0) > self.rank.get(root2, 0):
                self.parent[root2] = root1
            elif self.rank.get(root1, 0) < self.rank.get(root2, 0):
                self.parent[root1] = root2
            else:
                self.parent[root2] = root1
                self.rank[root1] = self.rank.get(root1, 0) + 1

    def connected(self, element1: T, element2: T) -> bool:
        """
        Checks if the two elements are in the same set.

        Parameters
        ----------
        element1 : T
            The first element.
        element2 : T
            The second element.

        Returns
        -------
        bool
            True if the two elements are in the same set, False otherwise.
        """
        return self.find(element1) == self.find(element2)
