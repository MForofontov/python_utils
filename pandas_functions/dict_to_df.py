import pandas as pd
from typing import Any

def dict_to_df(dictionary: dict[str, Any]) -> pd.DataFrame:
    """
    Convert a dictionary to a pandas DataFrame.

    Parameters
    ----------
    dictionary : dict
        The dictionary to convert. Keys are used as column headers.

    Returns
    -------
    pd.DataFrame
        The resulting DataFrame, where each key-value pair in the dictionary corresponds to a column in the DataFrame.
    """
    return pd.DataFrame.from_dict(dictionary)