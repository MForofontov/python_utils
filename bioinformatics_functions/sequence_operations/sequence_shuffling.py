import random

def sequence_shuffling(sequence: str) -> str:
    """
    Randomly shuffle a sequence while preserving composition.

    Parameters
    ----------
    sequence : str
        Input sequence.

    Returns
    -------
    str
        Shuffled sequence.

    Raises
    ------
    TypeError
        If sequence is not a string.

    Examples
    --------
    >>> sequence_shuffling("ATGC")
    'GCAT'  # Output may vary

    Complexity
    ----------
    Time: O(n), Space: O(n)
    """
    if not isinstance(sequence, str):
        raise TypeError("sequence must be a string")
    seq_list = list(sequence)
    random.shuffle(seq_list)
    return ''.join(seq_list)

__all__ = ['sequence_shuffling']
