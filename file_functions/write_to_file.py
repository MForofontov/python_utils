def write_to_file(text: str, output_file: str, write_mode: str, end_char: str) -> None:
    """
    Write a single string to a file.

    Parameters
    ----------
    text : str
        A single string to write to the output file.
    output_file : str
        Path to the output file.
    write_mode : str
        Specify write mode ('w' creates file if it does not exist and truncates and over-writes existing file,
        'a' creates file if it does not exist and appends to the end of file if it exists).
    end_char : str
        Character added to the end of the file.

    Returns
    -------
    None
    """
    with open(output_file, write_mode) as out:
        out.write(text + end_char)