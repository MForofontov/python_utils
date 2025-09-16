from pathlib import Path

import pytest
from file_functions.data_format_operations.write_dict_to_tsv import write_dict_to_tsv


def test_write_dict_to_tsv_writes_padded_rows_and_preserves_order(
    tmp_path: Path,
) -> None:
    """
    Test case 1: Ensure unequal column lengths are padded and header order is preserved.
    """
    data: dict[str, list[object]] = {
        "col1": [1, 2],
        "col2": ["a"],
        "col3": ["x", "y", "z"],
    }
    output_file: Path = tmp_path / "output.tsv"
    write_dict_to_tsv(str(output_file), data)

    expected_lines: list[str] = [
        "col1\tcol2\tcol3\n",
        "1\ta\tx\n",
        "2\t\ty\n",
        "\t\tz\n",
    ]
    assert output_file.read_text().splitlines(keepends=True) == expected_lines, (
        "Output file should contain padded rows in order"
    )


def test_write_dict_to_tsv_writes_only_newline_with_empty_dict(
    tmp_path: Path,
) -> None:
    """
    Test case 2: Ensure an empty dictionary produces a file containing only a newline.
    """
    output_file: Path = tmp_path / "output.tsv"
    write_dict_to_tsv(str(output_file), {})

    assert output_file.read_text() == "\n", "File should contain only a newline"


def test_write_dict_to_tsv_raises_permission_error(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """
    Test case 3: Ensure PermissionError is raised when the file cannot be written.
    """
    data: dict[str, list[int]] = {"col1": [1]}
    file_path: Path = tmp_path / "output.tsv"

    def mock_open(*args, **kwargs):
        raise PermissionError("No permission")

    monkeypatch.setattr("builtins.open", mock_open)
    with pytest.raises(PermissionError):
        write_dict_to_tsv(str(file_path), data)
