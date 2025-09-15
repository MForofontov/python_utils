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
    """
    joined_lines: str = joiner.join(lines)
    write_to_file(joined_lines, output_file, write_mode, "\n")


__all__ = ["write_lines"]
