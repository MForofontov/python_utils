class SegmentTree:
    """
    A Segment Tree data structure.

    Attributes
    ----------
    tree : List[int]
        A list representing the segment tree.
    n : int
        The size of the input array.

    Methods
    -------
    build(arr: List[int]) -> None
        Builds the segment tree from the input array.
    update(index: int, value: int) -> None
        Updates the value at the specified index.
    query(left: int, right: int) -> int
        Queries the range from left to right for the sum.
    """

    def __init__(self) -> None:
        self.tree: list[int] = []
        self.n: int = 0

    def build(self, arr: list[int]) -> None:
        """
        Builds the segment tree from the input array.

        Parameters
        ----------
        arr : List[int]
            The array to build the segment tree from.
        """
        self.n = len(arr)
        self.tree = [0] * (2 * self.n)
        for i in range(self.n):
            self.tree[self.n + i] = arr[i]
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]

    def update(self, index: int, value: int) -> None:
        """
        Updates the value at the specified index.

        Parameters
        ----------
        index : int
            The index to update.
        value : int
            The new value at the specified index.
        """
        index += self.n
        self.tree[index] = value
        while index > 1:
            index //= 2
            self.tree[index] = self.tree[2 * index] + self.tree[2 * index + 1]

    def query(self, left: int, right: int) -> int:
        """
        Queries the range from left to right for the sum.

        Parameters
        ----------
        left : int
            The starting index of the range.
        right : int
            The ending index of the range.

        Returns
        -------
        int
            The sum of elements in the range.
        """
        left += self.n
        right += self.n
        result = 0
        while left <= right:
            if left % 2 == 1:
                result += self.tree[left]
                left += 1
            if right % 2 == 0:
                result += self.tree[right]
                right -= 1
            left //= 2
            right //= 2
        return result
