from .write_to_file import write_to_file


def write_lines(
    lines: list[str], output_file: str, joiner: str = "\n", write_mode: str = "w"
) -> None:
    """
    Write a list of strings to a file.

    Parameters
    ----------
    lines : list[str]
        List with the lines/strings to write to the output file.
    output_file : str
        Path to the output file.
    joiner : str, optional
        Character used to join lines (default is '\n').
    write_mode : str, optional
        Specify write mode ('w' creates file if it does not exist and truncates and over-writes existing file,
        'a' creates file if it does not exist and appends to the end of file if it exists) (default is 'w').

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If parameters have invalid values.
    """
    # Input validation
    if not isinstance(lines, list):
        raise TypeError(f"lines must be a list, got {type(lines).__name__}")
    if not isinstance(output_file, str):
        raise TypeError(f"file_path must be a string, got {type(output_file).__name__}")
    if not isinstance(joiner, str):
        raise TypeError(f"joiner must be a string, got {type(joiner).__name__}")
    if not isinstance(write_mode, str):
        raise TypeError(f"write_mode must be a string, got {type(write_mode).__name__}")

    # Validate output_file is not empty
    if not output_file.strip():
        raise ValueError("file_path cannot be empty")

    # Validate write_mode values
    valid_modes = {"w", "a"}
    if write_mode not in valid_modes:
        raise ValueError("write_mode must be 'w' or 'a'")

    # Convert all items in lines to strings
    string_lines = [str(line) for line in lines]

    joined_lines: str = joiner.join(string_lines)
    write_to_file(joined_lines, output_file, write_mode, "\n")


__all__ = ["write_lines"]
