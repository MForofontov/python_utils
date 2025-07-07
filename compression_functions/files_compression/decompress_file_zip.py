import os
import zipfile

def decompress_file_zip(input_zip: str, output_dir: str) -> None:
    """
    Decompress a zip-compressed file.

    Parameters
    ----------
    input_zip : str
        The path to the input zip-compressed file.
    output_dir : str
        The path to the output directory to extract the decompressed files.

    Raises
    ------
    TypeError
        If input_zip or output_dir is not a string.
    FileNotFoundError
        If the input zip file does not exist.
    IOError
        If an I/O error occurs during decompression.
    """
    # Check if input_zip and output_dir are strings
    if not isinstance(input_zip, str):
        raise TypeError("input_zip must be a string")
    if not isinstance(output_dir, str):
        raise TypeError("output_dir must be a string")

    try:
        if not os.access(input_zip, os.R_OK):
            raise OSError("Input file is not readable")
        if not os.access(output_dir or ".", os.W_OK):
            raise OSError("Output location is not writable")
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Open the input zip-compressed file in read mode
        with zipfile.ZipFile(input_zip, 'r') as zipf:
            # Extract all files to the specified output directory
            zipf.extractall(output_dir)
    except FileNotFoundError:
        # Raise a FileNotFoundError if the input zip file does not exist
        raise FileNotFoundError(f"The input zip file {input_zip} does not exist.")
    except OSError as e:
        # Raise an IOError if an I/O error occurs during decompression
        raise OSError(f"An I/O error occurred during decompression: {e}")
