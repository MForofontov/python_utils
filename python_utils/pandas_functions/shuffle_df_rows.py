import pandas as pd


def shuffle_df_rows(df: pd.DataFrame, random_state: int | None = None) -> pd.DataFrame:
    """Shuffle rows of ``df``.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame whose rows will be shuffled.
    random_state : int | None, optional
        Random seed for reproducibility. Defaults to ``None``.

    Returns
    -------
    pd.DataFrame
        Shuffled DataFrame with index reset.
    """
    return df.sample(frac=1, random_state=random_state).reset_index(drop=True)


__all__ = ["shuffle_df_rows"]
