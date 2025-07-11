import csv

def read_tabular(input_file: str, delimiter: str = '\t') -> list[list[str]]:
    """
    Read a tabular (TSV) file.

    Parameters
    ----------
    input_file : str
        Path to a tabular file.
    delimiter : str, optional
        Delimiter used to separate file fields (default is '\t').

    Returns
    -------
    List[List[str]]
        A list with a sublist per line in the input file. Each sublist has the fields that were separated by the defined delimiter.
    """
    with open(input_file) as infile:
        reader = csv.reader(infile, delimiter=delimiter)
        lines: list[list[str]] = [line for line in reader]

    return lines