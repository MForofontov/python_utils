"""Match sequence patterns with IUPAC support."""

import re


def sequence_pattern_match(seq: str, pattern: str, use_iupac: bool = True) -> list[int]:
    """
    Find all positions matching a pattern with support for IUPAC ambiguity codes.

    Parameters
    ----------
    seq : str
        Sequence to search in.
    pattern : str
        Pattern to match. Can include IUPAC ambiguity codes if use_iupac=True.
    use_iupac : bool, optional
        If True, interprets IUPAC ambiguity codes in pattern (by default True).
        If False, treats pattern as literal string.

    Returns
    -------
    list[int]
        List of 0-based positions where pattern matches.

    Raises
    ------
    TypeError
        If seq or pattern is not a string.
        If use_iupac is not a boolean.
    ValueError
        If pattern is empty or longer than sequence.
        If pattern contains invalid IUPAC codes when use_iupac=True.

    Examples
    --------
    >>> sequence_pattern_match("ATGCATGC", "ATG")
    [0, 4]
    >>> sequence_pattern_match("ATGCATGC", "ARG", use_iupac=True)  # R = A or G
    [0, 4]
    >>> sequence_pattern_match("ATGCTTGC", "AYGC", use_iupac=True)  # Y = C or T
    [0, 4]
    >>> sequence_pattern_match("ATGCATGC", "N", use_iupac=True)  # N = any base
    [0, 1, 2, 3, 4, 5, 6, 7]

    Notes
    -----
    IUPAC ambiguity codes supported:
    - R = A or G (purine)
    - Y = C or T (pyrimidine)
    - S = G or C (strong)
    - W = A or T (weak)
    - K = G or T (keto)
    - M = A or C (amino)
    - B = C, G, or T (not A)
    - D = A, G, or T (not C)
    - H = A, C, or T (not G)
    - V = A, C, or G (not T)
    - N = A, C, G, or T (any)

    Case-insensitive matching.

    Complexity
    ----------
    Time: O(n*m), Space: O(k) where n is sequence length, m is pattern length, k is matches
    """
    # Input validation
    if not isinstance(seq, str):
        raise TypeError(f"seq must be a string, got {type(seq).__name__}")
    if not isinstance(pattern, str):
        raise TypeError(f"pattern must be a string, got {type(pattern).__name__}")
    if not isinstance(use_iupac, bool):
        raise TypeError(f"use_iupac must be a boolean, got {type(use_iupac).__name__}")

    if len(pattern) == 0:
        raise ValueError("Pattern cannot be empty")
    if len(pattern) > len(seq):
        raise ValueError(
            f"Pattern length ({len(pattern)}) cannot be greater than sequence length ({len(seq)})"
        )

    # Convert to uppercase
    seq_upper = seq.upper()
    pattern_upper = pattern.upper()

    if use_iupac:
        # IUPAC ambiguity code mappings
        iupac_codes = {
            "A": "A",
            "T": "T",
            "G": "G",
            "C": "C",
            "R": "[AG]",  # purine
            "Y": "[CT]",  # pyrimidine
            "S": "[GC]",  # strong
            "W": "[AT]",  # weak
            "K": "[GT]",  # keto
            "M": "[AC]",  # amino
            "B": "[CGT]",  # not A
            "D": "[AGT]",  # not C
            "H": "[ACT]",  # not G
            "V": "[ACG]",  # not T
            "N": "[ACGT]",  # any
        }

        # Validate pattern contains only valid IUPAC codes
        valid_codes = set(iupac_codes.keys())
        pattern_codes = set(pattern_upper)
        invalid_codes = pattern_codes - valid_codes
        if invalid_codes:
            raise ValueError(
                f"Invalid IUPAC codes in pattern: {', '.join(sorted(invalid_codes))}"
            )

        # Convert pattern to regex
        regex_pattern = "".join(iupac_codes[base] for base in pattern_upper)

        # Find all matches
        positions = []
        for match in re.finditer(regex_pattern, seq_upper):
            positions.append(match.start())
    else:
        # Literal string matching
        positions = []
        start = 0
        while start <= len(seq_upper) - len(pattern_upper):
            pos = seq_upper.find(pattern_upper, start)
            if pos == -1:
                break
            positions.append(pos)
            start = pos + 1

    return positions


__all__ = ["sequence_pattern_match"]
