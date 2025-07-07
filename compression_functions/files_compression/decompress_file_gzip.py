import gzip
import shutil
import os

def decompress_file_gzip(input_gzip: str, output_file: str) -> None:
    """
    Decompress a gzip-compressed file.

    Parameters
    ----------
    input_gzip : str
        The path to the input gzip-compressed file.
    output_file : str
        The path to the output file to save the decompressed data.

    Raises
    ------
    TypeError
        If input_gzip or output_file is not a string.
    FileNotFoundError
        If the input file does not exist.
    IOError
        If an I/O error occurs during decompression.
    """
    # Check if input_gzip and output_file are strings
    if not isinstance(input_gzip, str):
        raise TypeError("input_gzip must be a string")
    if not isinstance(output_file, str):
        raise TypeError("output_file must be a string")

    try:
        if not os.access(input_gzip, os.R_OK):
            raise OSError("Input file is not readable")
        output_dir = os.path.dirname(output_file) or "."
        if not os.access(output_dir, os.W_OK):
            raise OSError("Output location is not writable")
        # Open the input gzip-compressed file in binary read mode
        with gzip.open(input_gzip, 'rb') as f_in:
            # Open the output file in binary write mode
            with open(output_file, 'wb') as f_out:
                # Copy the contents of the input file to the output file
                shutil.copyfileobj(f_in, f_out)
    except FileNotFoundError:
        # Raise a FileNotFoundError if the input file does not exist
        raise FileNotFoundError(f"The input file {input_gzip} does not exist.")
    except OSError as e:
        # Raise an IOError if an I/O error occurs during decompression
        raise OSError(f"An I/O error occurred during decompression: {e}")
