import shutil


def concat_files(source_file: str, destination_file: str) -> None:
    """
    Concatenates the source file to the destination file.

    Parameters
    ----------
    source_file : str
        The path to the source file.
    destination_file : str
        The path to the destination file.

    Returns
    -------
    None
    """
    with open(destination_file, "a") as outfile, open(source_file) as infile:
        shutil.copyfileobj(infile, outfile)


__all__ = ['concat_files']
