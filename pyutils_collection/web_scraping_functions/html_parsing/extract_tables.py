"""
Extract tables from HTML content.
"""

from bs4 import BeautifulSoup, Tag


def extract_tables(
    element: BeautifulSoup | Tag,
    header_row: bool = True,
) -> list[list[list[str]]]:
    """
    Extract all tables from HTML element as nested lists.

    Parameters
    ----------
    element : BeautifulSoup | Tag
        HTML element to extract tables from.
    header_row : bool, optional
        Whether first row is header (by default True).

    Returns
    -------
    list[list[list[str]]]
        List of tables, each table is a list of rows,
        each row is a list of cell values.

    Raises
    ------
    TypeError
        If parameters are of wrong type.

    Examples
    --------
    >>> from bs4 import BeautifulSoup
    >>> html = '''<table>
    ...     <tr><th>Name</th><th>Age</th></tr>
    ...     <tr><td>Alice</td><td>30</td></tr>
    ... </table>'''
    >>> soup = BeautifulSoup(html, "html.parser")
    >>> tables = extract_tables(soup)
    >>> len(tables)
    1
    >>> tables[0]
    [['Name', 'Age'], ['Alice', '30']]

    Notes
    -----
    Handles both <th> and <td> elements.
    Preserves table structure including empty cells.

    Complexity
    ----------
    Time: O(n*m), Space: O(n*m), where n is tables, m is cells per table
    """
    if not isinstance(element, (BeautifulSoup, Tag)):
        raise TypeError(
            f"element must be BeautifulSoup or Tag, got {type(element).__name__}"
        )
    if not isinstance(header_row, bool):
        raise TypeError(
            f"header_row must be a boolean, got {type(header_row).__name__}"
        )

    tables = []

    for table in element.find_all("table"):
        rows = []
        for tr in table.find_all("tr"):
            cells = []
            # Extract both th and td cells
            for cell in tr.find_all(["th", "td"]):
                cells.append(cell.get_text(strip=True))
            if cells:
                rows.append(cells)

        if rows:
            tables.append(rows)

    return tables


__all__ = ["extract_tables"]
