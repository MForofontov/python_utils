"""
Compare file hashes to detect duplicates.
"""

from pathlib import Path

from .calculate_md5_hash import calculate_md5_hash


def compare_file_hashes(
    file1_path: str | Path,
    file2_path: str | Path,
    hash_algorithm: str = "md5",
    chunk_size: int = 8192,
) -> bool:
    """
    Compare two files by their hash values to determine if they are identical.

    Parameters
    ----------
    file1_path : str | Path
        Path to the first file.
    file2_path : str | Path
        Path to the second file.
    hash_algorithm : str, optional
        Hash algorithm to use: 'md5', 'sha1', or 'sha256' (by default "md5").
    chunk_size : int, optional
        Size of chunks to read at a time in bytes (by default 8192).

    Returns
    -------
    bool
        True if files have identical hashes, False otherwise.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If files don't exist, algorithm is invalid, or chunk_size is invalid.
    OSError
        If there's an error reading the files.

    Examples
    --------
    >>> compare_file_hashes("/path/to/file1.txt", "/path/to/file2.txt")
    True
    >>> compare_file_hashes("/path/to/file1.txt", "/path/to/file2.txt", "sha256")
    False

    Notes
    -----
    This function is useful for detecting duplicate files.
    MD5 is fastest but least secure, SHA256 is most secure but slower.

    Complexity
    ----------
    Time: O(n + m), Space: O(1) where n, m are file sizes.
    """
    # Input validation
    if not isinstance(file1_path, (str, Path)):
        raise TypeError(
            f"file1_path must be a string or Path, got {type(file1_path).__name__}"
        )
    if not isinstance(file2_path, (str, Path)):
        raise TypeError(
            f"file2_path must be a string or Path, got {type(file2_path).__name__}"
        )
    if not isinstance(hash_algorithm, str):
        raise TypeError(
            f"hash_algorithm must be a string, got {type(hash_algorithm).__name__}"
        )
    if not isinstance(chunk_size, int):
        raise TypeError(
            f"chunk_size must be an integer, got {type(chunk_size).__name__}"
        )

    # Validate algorithm
    valid_algorithms = {"md5", "sha1", "sha256"}
    if hash_algorithm.lower() not in valid_algorithms:
        raise ValueError(
            f"hash_algorithm must be one of {valid_algorithms}, got '{hash_algorithm}'"
        )

    # Validate chunk_size
    if chunk_size <= 0:
        raise ValueError(f"chunk_size must be positive, got {chunk_size}")

    # Import hash functions
    from .calculate_sha1_hash import calculate_sha1_hash
    from .calculate_sha256_hash import calculate_sha256_hash

    # Select hash function
    hash_functions = {
        "md5": calculate_md5_hash,
        "sha1": calculate_sha1_hash,
        "sha256": calculate_sha256_hash,
    }

    hash_func = hash_functions[hash_algorithm.lower()]

    # Calculate hashes for both files
    try:
        hash1 = hash_func(file1_path, chunk_size)
        hash2 = hash_func(file2_path, chunk_size)

        return hash1 == hash2
    except (ValueError, OSError) as e:
        raise e


__all__ = ["compare_file_hashes"]
