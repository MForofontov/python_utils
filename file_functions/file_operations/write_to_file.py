"""Write data to file utility."""


def write_to_file(
    data: str, file_path: str, mode: str = "w", end_char: str = ""
) -> None:
    """
    Write string data to a file.

    Parameters
    ----------
    data : str
        The string data to write to the file.
    file_path : str
        The path to the file where data will be written.
    mode : str, optional
        File mode for writing: 'w' (write/overwrite), 'a' (append), or 'x' (exclusive create)
        (by default "w").
    end_char : str, optional
        Character(s) to append at the end of the data (by default "").

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If parameters have invalid values.
    FileExistsError
        If mode is 'x' and file already exists.

    Examples
    --------
    >>> write_to_file("Hello, World!", "output.txt")
    >>> write_to_file("Additional content", "output.txt", mode="a")
    >>> write_to_file("Content with ending", "output.txt", end_char="\\n")
    >>> write_to_file("New file", "new.txt", mode="x")  # Creates new file only

    Notes
    -----
    The function writes data with UTF-8 encoding to handle Unicode characters properly.

    Complexity
    ----------
    Time: O(n), Space: O(1) where n is the length of data
    """
    # Input validation
    if not isinstance(data, str):
        raise TypeError(f"data must be a string, got {type(data).__name__}")
    if not isinstance(file_path, str):
        raise TypeError(f"file_path must be a string, got {type(file_path).__name__}")
    if not isinstance(mode, str):
        raise TypeError(f"mode must be a string, got {type(mode).__name__}")
    if not isinstance(end_char, str):
        raise TypeError(f"end_char must be a string, got {type(end_char).__name__}")

    # Value validation
    if not file_path:
        raise ValueError("file_path cannot be empty")
    if mode not in ("w", "a", "x"):
        raise ValueError("mode must be 'w', 'a', or 'x'")

    # Write data to file
    with open(file_path, mode, encoding="utf-8") as file:
        file.write(data + end_char)


__all__ = ["write_to_file"]
