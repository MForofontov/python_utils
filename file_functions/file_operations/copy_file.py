import shutil


def copy_file(source_file: str, destination_file: str) -> None:
    """
    Copies the source file to the destination.

    Parameters
    ----------
    source_file : str
        Path to the source file.
    destination_file : str
        Path to where to copy the file.

    Returns
    -------
    None
    """
    shutil.copy(source_file, destination_file)


__all__ = ['copy_file']
