import zipfile
import os

def compress_zip(input_path: str, output_zip: str) -> None:
    """
    Compress a file or folder using zip.

    Parameters
    ----------
    input_path : str
        The path to the input file or folder to be compressed.
    output_zip : str
        The path to the output zip file to save the compressed data.

    Raises
    ------
    TypeError
        If input_path or output_zip is not a string.
    FileNotFoundError
        If the input path does not exist.
    IOError
        If an I/O error occurs during compression.
    """
    # Check if input_path and output_zip are strings
    if not isinstance(input_path, str):
        raise TypeError("input_path must be a string")
    if not isinstance(output_zip, str):
        raise TypeError("output_zip must be a string")

    # Check if the input path exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"The input path {input_path} does not exist.")

    try:
        check_path = input_path if os.path.isdir(input_path) else os.path.dirname(input_path) or "."
        if not os.access(check_path, os.R_OK):
            raise OSError("Input path is not readable")
        output_dir = os.path.dirname(output_zip) or "."
        if not os.access(output_dir, os.W_OK):
            raise OSError("Output location is not writable")
        # Open the output zip file in write mode with deflated compression
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # If the input path is a directory, walk through the directory and its subdirectories
            if os.path.isdir(input_path):
                for root, dirs, files in os.walk(input_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, start=input_path)
                        # Write the file to the zip archive with the relative path as the archive name
                        zipf.write(file_path, arcname=arcname)
            else:
                # If the input path is a file, add the file to the zip archive
                zipf.write(input_path, arcname=os.path.basename(input_path))
    except OSError as e:
        # Raise an IOError if an I/O error occurs during compression
        raise OSError(f"An I/O error occurred during compression: {e}")
