"""Tests for read_excel_sheet module."""

import pytest
from pathlib import Path
from serialization_functions.excel_operations.read_excel_sheet import read_excel_sheet


def test_read_excel_sheet_entire_sheet(tmp_path: Path) -> None:
    """
    Test case 1: Test reading entire sheet.
    """
    # Arrange

    file_path = tmp_path / "data.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.append(["Name", "Age"])
    ws.append(["Alice", 30])
    wb.save(file_path)
    wb.close()

    # Act
    data = read_excel_sheet(str(file_path))

    # Assert
    assert len(data) == 2
    assert data[0] == ["Name", "Age"]
    assert data[1] == ["Alice", 30]


def test_read_excel_sheet_with_row_range(tmp_path: Path) -> None:
    """
    Test case 2: Test reading specific row range.
    """
    # Arrange

    file_path = tmp_path / "data.xlsx"
    wb = Workbook()
    ws = wb.active
    for i in range(1, 11):
        ws.append([i])
    wb.save(file_path)
    wb.close()

    # Act
    data = read_excel_sheet(str(file_path), min_row=2, max_row=5)

    # Assert
    assert len(data) == 4  # rows 2-5


def test_read_excel_sheet_with_column_range(tmp_path: Path) -> None:
    """
    Test case 3: Test reading specific column range.
    """
    # Arrange

    file_path = tmp_path / "data.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.append(["A", "B", "C", "D"])
    wb.save(file_path)
    wb.close()

    # Act
    data = read_excel_sheet(str(file_path), min_col=2, max_col=3)

    # Assert
    assert data[0] == ["B", "C"]


def test_read_excel_sheet_by_sheet_name(tmp_path: Path) -> None:
    """
    Test case 4: Test reading from specific sheet by name.
    """
    # Arrange

    file_path = tmp_path / "multi.xlsx"
    wb = Workbook()
    ws2 = wb.create_sheet("Data")
    ws2.append(["Test"])
    wb.save(file_path)
    wb.close()

    # Act
    data = read_excel_sheet(str(file_path), sheet_name="Data")

    # Assert
    assert data[0][0] == "Test"


def test_read_excel_sheet_by_sheet_index(tmp_path: Path) -> None:
    """
    Test case 5: Test reading from specific sheet by index.
    """
    # Arrange

    file_path = tmp_path / "multi.xlsx"
    wb = Workbook()
    wb.create_sheet("Second")
    wb.worksheets[1].append(["Second"])
    wb.save(file_path)
    wb.close()

    # Act
    data = read_excel_sheet(str(file_path), sheet_name=1)

    # Assert
    assert data[0][0] == "Second"


def test_read_excel_sheet_invalid_file_path_type_raises_error() -> None:
    """
    Test case 6: Test TypeError for invalid file_path type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="file_path must be a string"):
        read_excel_sheet(123)


def test_read_excel_sheet_invalid_min_row_type_raises_error(tmp_path: Path) -> None:
    """
    Test case 7: Test TypeError for invalid min_row type.
    """
    # Arrange

    file_path = tmp_path / "data.xlsx"
    wb = Workbook()
    wb.save(file_path)
    wb.close()

    # Act & Assert
    with pytest.raises(TypeError, match="min_row must be int or None"):
        read_excel_sheet(str(file_path), min_row="invalid")


def test_read_excel_sheet_invalid_min_row_value_raises_error(tmp_path: Path) -> None:
    """
    Test case 8: Test ValueError for invalid min_row value.
    """
    # Arrange

    file_path = tmp_path / "data.xlsx"
    wb = Workbook()
    wb.save(file_path)
    wb.close()

    # Act & Assert
    with pytest.raises(ValueError, match="min_row must be >= 1"):
        read_excel_sheet(str(file_path), min_row=0)


def test_read_excel_sheet_invalid_sheet_index_raises_error(tmp_path: Path) -> None:
    """
    Test case 9: Test ValueError for invalid sheet index.
    """
    # Arrange

    file_path = tmp_path / "data.xlsx"
    wb = Workbook()
    wb.save(file_path)
    wb.close()

    # Act & Assert
    with pytest.raises(ValueError, match="sheet_name index.*out of range"):
        read_excel_sheet(str(file_path), sheet_name=10)


def test_read_excel_sheet_nonexistent_sheet_name_raises_error(tmp_path: Path) -> None:
    """
    Test case 10: Test ValueError for non-existent sheet name.
    """
    # Arrange

    file_path = tmp_path / "data.xlsx"
    wb = Workbook()
    wb.save(file_path)
    wb.close()

    # Act & Assert
    with pytest.raises(ValueError, match="sheet_name.*not found"):
        read_excel_sheet(str(file_path), sheet_name="NonExistent")
