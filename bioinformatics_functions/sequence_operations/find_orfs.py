from collections.abc import Iterator


def find_orfs(seq: str) -> Iterator[tuple[int, int, str]]:
    """
    Find open reading frames (ORFs) in a DNA sequence.

    Parameters
    ----------
    seq : str
        DNA sequence (A, T, C, G).

    Yields
    ------
    Tuple[int, int, str]
        (start, end, orf_sequence) for each ORF found.

    Raises
    ------
    TypeError
        If seq is not a string.
    ValueError
        If seq contains invalid characters.

    Examples
    --------
    >>> list(find_orfs('ATGAAATAGATGTAA'))
    [(0, 9, 'ATGAAATAG'), (9, 15, 'ATGTAA')]
    """
    if not isinstance(seq, str):
        raise TypeError(f"seq must be str, got {type(seq).__name__}")
    seq = seq.upper()
    if not all(base in "ATCG" for base in seq):
        raise ValueError("Sequence contains invalid DNA bases")
    start_codon = "ATG"
    stop_codons = {"TAA", "TAG", "TGA"}
    i = 0
    while i < len(seq) - 2:
        if seq[i : i + 3] == start_codon:
            for j in range(i + 3, len(seq) - 2, 3):
                codon = seq[j : j + 3]
                if codon in stop_codons:
                    yield (i, j + 3, seq[i : j + 3])
                    i = j + 3
                    break
            else:
                i += 3
        else:
            i += 1


__all__ = ["find_orfs"]
