class TrieNode:
    """
    A TrieNode used in a Trie data structure.

    Attributes
    ----------
    children : Dict[str, TrieNode]
        A dictionary storing child nodes indexed by characters.
    is_end_of_word : bool
        Indicates if the node marks the end of a word.
    """

    def __init__(self) -> None:
        """
        Initializes a TrieNode.
        """
        self.children: dict[str, TrieNode] = {}
        self.is_end_of_word = False


class Trie:
    """
    A Trie (Prefix Tree) data structure.

    Attributes
    ----------
    root : TrieNode
        The root node of the trie.

    Methods
    -------
    insert(word)
        Inserts a word into the trie.
    search(word)
        Searches for a word in the trie.
    starts_with(prefix)
        Checks if there is any word in the trie that starts with the given prefix.
    """

    def __init__(self) -> None:
        """
        Initializes an empty trie.
        """
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """
        Inserts a word into the trie.

        Parameters
        ----------
        word : str
            The word to insert.
        """
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        """
        Searches for a word in the trie.

        Parameters
        ----------
        word : str
            The word to search for.

        Returns
        -------
        bool
            True if the word exists, False otherwise.
        """
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        """
        Checks if there is any word in the trie that starts with the given prefix.

        Parameters
        ----------
        prefix : str
            The prefix to check.

        Returns
        -------
        bool
            True if any word starts with the prefix, False otherwise.
        """
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
