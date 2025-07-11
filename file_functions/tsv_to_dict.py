
def tsv_to_dict(file_path: str, skip_header: bool = False, sep: str = '\t') -> dict[str, list[str]]:
    """
    Converts input TSV into a dict based on the desired separator.
    
    Parameters
    ----------
    file_path : str
        Path to the TSV file.
    skip_header : bool, optional
        If to ignore the header when importing.
    sep : str, optional
        String to separate the values inside the TSV file.
    
    Returns
    -------
    dict
        Returns the TSV file converted to the dict.
    """
    data_dict = {}

    with open(file_path) as f:
        for i, line in enumerate(f):
            if i == 0 and skip_header:
                continue
                
            values = line.strip().split(sep)
            key = values[0]
            rest_values = values[1:]
            data_dict[key] = rest_values

    return data_dict