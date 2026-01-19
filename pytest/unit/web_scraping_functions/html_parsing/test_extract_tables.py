import pytest

# Try to import BeautifulSoup - tests will be skipped if not available
try:
    from bs4 import BeautifulSoup
    from web_scraping_functions.html_parsing.extract_tables import extract_tables
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    BeautifulSoup = None  # type: ignore
    extract_tables = None  # type: ignore

pytestmark = pytest.mark.skipif(not BS4_AVAILABLE, reason="beautifulsoup4 not installed")
pytestmark = [pytestmark, pytest.mark.unit, pytest.mark.web_scraping]


def test_extract_tables_simple_table() -> None:
    """
    Test case 1: Extract simple table.
    """
    # Arrange
    html = """<table>
        <tr><th>Name</th><th>Age</th></tr>
        <tr><td>Alice</td><td>30</td></tr>
    </table>"""
    soup = BeautifulSoup(html, "html.parser")

    # Act
    result = extract_tables(soup)

    # Assert
    assert len(result) == 1
    assert result[0] == [["Name", "Age"], ["Alice", "30"]]


def test_extract_tables_multiple_tables() -> None:
    """
    Test case 2: Extract multiple tables.
    """
    # Arrange
    html = """
        <table><tr><td>A</td></tr></table>
        <table><tr><td>B</td></tr></table>
    """
    soup = BeautifulSoup(html, "html.parser")

    # Act
    result = extract_tables(soup)

    # Assert
    assert len(result) == 2
    assert result[0] == [["A"]]
    assert result[1] == [["B"]]


def test_extract_tables_mixed_th_td() -> None:
    """
    Test case 3: Extract table with mixed th and td.
    """
    # Arrange
    html = """<table>
        <tr><th>Header1</th><th>Header2</th></tr>
        <tr><td>Data1</td><td>Data2</td></tr>
    </table>"""
    soup = BeautifulSoup(html, "html.parser")

    # Act
    result = extract_tables(soup)

    # Assert
    assert result[0][0] == ["Header1", "Header2"]
    assert result[0][1] == ["Data1", "Data2"]


def test_extract_tables_empty_cells() -> None:
    """
    Test case 4: Extract table with empty cells.
    """
    # Arrange
    html = """<table>
        <tr><td>A</td><td></td></tr>
        <tr><td></td><td>B</td></tr>
    </table>"""
    soup = BeautifulSoup(html, "html.parser")

    # Act
    result = extract_tables(soup)

    # Assert
    assert result[0][0] == ["A", ""]
    assert result[0][1] == ["", "B"]


def test_extract_tables_no_tables() -> None:
    """
    Test case 5: Extract from HTML with no tables.
    """
    # Arrange
    html = "<div>No tables here</div>"
    soup = BeautifulSoup(html, "html.parser")

    # Act
    result = extract_tables(soup)

    # Assert
    assert result == []


def test_extract_tables_whitespace_handling() -> None:
    """
    Test case 6: Verify whitespace is stripped from cells.
    """
    # Arrange
    html = """<table>
        <tr><td>  Padded  </td><td>  Text  </td></tr>
    </table>"""
    soup = BeautifulSoup(html, "html.parser")

    # Act
    result = extract_tables(soup)

    # Assert
    assert result[0][0] == ["Padded", "Text"]


def test_extract_tables_type_error_element() -> None:
    """
    Test case 7: TypeError for invalid element type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="element must be BeautifulSoup or Tag"):
        extract_tables("not a soup")


def test_extract_tables_type_error_header_row() -> None:
    """
    Test case 8: TypeError for invalid header_row type.
    """
    # Arrange
    html = "<table><tr><td>A</td></tr></table>"
    soup = BeautifulSoup(html, "html.parser")

    # Act & Assert
    with pytest.raises(TypeError, match="header_row must be a boolean"):
        extract_tables(soup, header_row="yes")
