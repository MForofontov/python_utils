import os


def load_dotenv(dotenv_path: str | None = None, override: bool = False) -> None:
    """
    Load environment variables from a .env file into os.environ.

    Parameters
    ----------
    dotenv_path : str, optional
        Path to the .env file. If None, uses '.env' in current directory.
    override : bool, optional
        If True, override existing environment variables. Default is False.

    Returns
    -------
    None

    Examples
    --------
    >>> load_dotenv('.env')
    >>> import os; os.environ['MY_VAR']
    'some_value'
    """
    path = dotenv_path or ".env"
    if not os.path.exists(path):
        return
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if override or key not in os.environ:
                os.environ[key] = value
