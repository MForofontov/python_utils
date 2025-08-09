import pytest
import importlib

wdt = importlib.import_module("file_functions.write_dict_to_tsv")


def test_write_dict_to_tsv_writes_padded_rows_and_preserves_order(tmp_path) -> None:
    """Ensure unequal column lengths are padded and header order is preserved."""
    data = {
        "col1": [1, 2],
        "col2": ["a"],
        "col3": ["x", "y", "z"],
    }
    output_file = tmp_path / "output.tsv"
    wdt.write_dict_to_tsv(str(output_file), data)

    expected_lines = [
        "col1\tcol2\tcol3\n",
        "1\ta\tx\n",
        "2\t\ty\n",
        "\t\tz\n",
    ]
    assert output_file.read_text().splitlines(keepends=True) == expected_lines


def test_write_dict_to_tsv_raises_permission_error(monkeypatch, tmp_path) -> None:
    """Ensure PermissionError is raised when the file cannot be written."""
    data = {"col1": [1]}
    file_path = tmp_path / "output.tsv"

    def mock_open(*args, **kwargs):
        raise PermissionError("No permission")

    monkeypatch.setattr("builtins.open", mock_open)
    with pytest.raises(PermissionError):
        wdt.write_dict_to_tsv(str(file_path), data)
