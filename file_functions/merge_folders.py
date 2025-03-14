import os
import shutil

def merge_folders(folder1: str, folder2: str, output_folder: str) -> None:
    """
    Merge the contents of two folders into an output folder.

    Parameters
    ----------
    folder1 : str
        Path to the first folder to merge.
    folder2 : str
        Path to the second folder to merge.
    output_folder : str
        Path to the output folder where the merged contents will be stored.

    Returns
    -------
    None

    Notes
    -----
    - If the output folder does not exist, it will be created.
    - If there are file naming conflicts, the conflicting files will be renamed with a "_copy" suffix.
    - The function ensures that all intermediate directories are created as needed.
    """
    def copy_files(src_folder: str) -> None:
        """
        Copy files from the source folder to the output folder.

        Parameters
        ----------
        src_folder : str
            Path to the source folder from which files will be copied.

        Returns
        -------
        None
        """
        for root, _, files in os.walk(src_folder):
            for file in files:
                src_file_path: str = os.path.join(root, file)
                relative_path: str = os.path.relpath(src_file_path, src_folder)
                dest_file_path: str = os.path.join(output_folder, relative_path)
                
                os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
                
                if os.path.exists(dest_file_path):
                    base, ext = os.path.splitext(dest_file_path)
                    dest_file_path = f"{base}_copy{ext}"
                
                shutil.copy2(src_file_path, dest_file_path)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    copy_files(folder1)
    copy_files(folder2)