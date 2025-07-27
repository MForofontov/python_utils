from typing import Any


class UnionFind:
    """
    A Union-Find (Disjoint Set) data structure.

    Attributes
    ----------
    parent : Dict[Any, Any]
        A dictionary that maps each element to its parent.
    rank : Dict[Any, int]
        A dictionary that stores the rank (or depth) of each element's tree.

    Methods
    -------
    find(element: Any) -> Any
        Finds the representative of the set containing the element.
    union(element1: Any, element2: Any) -> None
        Merges the sets containing the two elements.
    connected(element1: Any, element2: Any) -> bool
        Checks if the two elements are in the same set.
    """

    def __init__(self) -> None:
        self.parent: dict[Any, Any] = {}
        self.rank: dict[Any, int] = {}

    def find(self, element: Any) -> Any:
        """
        Finds the representative of the set containing the element.

        Parameters
        ----------
        element : Any
            The element to find.

        Returns
        -------
        Any
            The representative (root) of the set containing the element.
        """
        if self.parent.get(element) != element:
            self.parent[element] = self.find(self.parent[element])  # Path compression
        return self.parent.get(element, element)

    def union(self, element1: Any, element2: Any) -> None:
        """
        Merges the sets containing the two elements.

        Parameters
        ----------
        element1 : Any
            The first element.
        element2 : Any
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

    def connected(self, element1: Any, element2: Any) -> bool:
        """
        Checks if the two elements are in the same set.

        Parameters
        ----------
        element1 : Any
            The first element.
        element2 : Any
            The second element.

        Returns
        -------
        bool
            True if the two elements are in the same set, False otherwise.
        """
        return self.find(element1) == self.find(element2)
