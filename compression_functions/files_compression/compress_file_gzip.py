import gzip
import shutil
import os

def compress_file_gzip(input_file: str, output_file: str) -> None:
    """
    Compress a file using gzip.

    Parameters
    ----------
    input_file : str
        The path to the input file to be compressed.
    output_file : str
        The path to the output file to save the compressed data.

    Raises
    ------
    TypeError
        If input_file or output_file is not a string.
    FileNotFoundError
        If the input file does not exist.
    IOError
        If an I/O error occurs during compression.
    """
    # Check if input_file and output_file are strings
    if not isinstance(input_file, str):
        raise TypeError("input_file must be a string")
    if not isinstance(output_file, str):
        raise TypeError("output_file must be a string")

    try:
        if not os.access(input_file, os.R_OK):
            raise OSError("Input file is not readable")
        output_dir = os.path.dirname(output_file) or "."
        if not os.access(output_dir, os.W_OK):
            raise OSError("Output location is not writable")
        # Open the input file in binary read mode
        with open(input_file, 'rb') as f_in:
            # Open the output file in binary write mode with gzip compression
            with gzip.open(output_file, 'wb') as f_out:
                # Copy the contents of the input file to the output file
                shutil.copyfileobj(f_in, f_out)
    except FileNotFoundError:
        # Raise a FileNotFoundError if the input file does not exist
        raise FileNotFoundError(f"The input file {input_file} does not exist.")
    except OSError as e:
        # Raise an IOError if an I/O error occurs during compression
        raise OSError(f"An I/O error occurred during compression: {e}")
