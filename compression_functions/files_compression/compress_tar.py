import tarfile
import os


def compress_tar(input_path: str, output_tar: str) -> None:
    """
    Compress a file or folder using tar with gzip compression.

    Parameters
    ----------
    input_path : str
        The path to the input file or folder to be compressed.
    output_tar : str
        The path to the output tar file to save the compressed data.

    Raises
    ------
    TypeError
        If input_path or output_tar is not a string.
    FileNotFoundError
        If the input path does not exist.
    IOError
        If an I/O error occurs during compression.
    """
    # Check if input_path and output_tar are strings
    if not isinstance(input_path, str):
        raise TypeError("input_path must be a string")
    if not isinstance(output_tar, str):
        raise TypeError("output_tar must be a string")

    # Check if the input path exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"The input path {input_path} does not exist.")

    try:
        check_path = (
            input_path
            if os.path.isdir(input_path)
            else os.path.dirname(input_path) or "."
        )
        if os.path.isdir(input_path):
            if os.stat(check_path).st_mode & 0o444 == 0:
                raise OSError("Input path is not readable")
        else:
            if os.stat(input_path).st_mode & 0o444 == 0:
                raise OSError("Input path is not readable")

        output_dir = os.path.dirname(output_tar) or "."
        if os.stat(output_dir).st_mode & 0o222 == 0:
            raise OSError("Output location is not writable")
        if os.path.exists(output_tar) and os.stat(output_tar).st_mode & 0o222 == 0:
            raise OSError("Output file is not writable")

        with tarfile.open(output_tar, "w:gz") as tar:
            if os.path.isdir(input_path):
                tar.add(input_path, arcname=os.path.basename(input_path))
            else:
                tar.add(input_path, arcname=os.path.basename(input_path))
    except FileNotFoundError:
        raise
    except (PermissionError, OSError) as e:
        raise OSError(f"An I/O error occurred during compression: {e}")
