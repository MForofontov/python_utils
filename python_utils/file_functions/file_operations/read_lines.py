"""File line reading utilities."""

from itertools import islice


def read_lines(
    input_file: str, strip: bool = True, num_lines: int | None = None
) -> list[str]:
    """
    Read lines in a file.

    Parameters
    ----------
    input_file : str
        Path to the input file.
    strip : bool, optional
        Specify if lines should be stripped of leading and trailing white spaces and new line characters (default is True).
    num_lines : int | None, optional
        Number of lines to read from the file (default is None, which reads all lines).

    Returns
    -------
    list[str]
        List with the lines read from the input file.
    """
    with open(input_file) as infile:
        if num_lines is None:
            lines: list[str] = [line for line in infile.readlines()]
        elif num_lines <= 0:
            lines = []
        else:
            lines = list(islice(infile, num_lines))

    if strip:
        lines = [line.strip() for line in lines]

    return lines


__all__ = ["read_lines"]
