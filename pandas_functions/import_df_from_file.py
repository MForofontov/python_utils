import pandas as pd

def import_df_from_file(file_path: str, sep: str) -> pd.DataFrame:
    """
    Using pandas, imports a file path as a dataframe.

    Parameters
    ----------
    file_path : str
        Path to the file.
    sep : str
        String to separate entries in the file.

    Returns
    -------
    pd.DataFrame
        Pandas dataframe that contains the file values separated by sep.
    """
    df: pd.DataFrame = pd.read_csv(file_path, sep=sep)
    return df