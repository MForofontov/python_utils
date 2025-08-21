import json
from pathlib import Path

import importlib
import pytest

wdj = importlib.import_module("file_functions.write_dict_to_json")


def test_write_dict_to_json_writes_expected(tmp_path: Path) -> None:
    """Ensure dictionary is correctly serialized to a JSON file."""
    data: dict[str, object] = {"a": 1, "b": [1, 2]}
    output_file: Path = tmp_path / "output.json"
    wdj.write_dict_to_json(str(output_file), data, indent=2)
    assert json.loads(output_file.read_text()) == data


def test_write_dict_to_json_writes_empty_dict(tmp_path: Path) -> None:
    """Ensure an empty dictionary produces an empty JSON object."""
    output_file: Path = tmp_path / "output.json"
    wdj.write_dict_to_json(str(output_file), {})
    assert output_file.read_text() == "{}"


def test_write_dict_to_json_raises_permission_error(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Ensure PermissionError is raised when the file cannot be written."""
    data: dict[str, int] = {"a": 1}
    file_path: Path = tmp_path / "output.json"

    def mock_open(*args, **kwargs):
        raise PermissionError("No permission")

    monkeypatch.setattr("builtins.open", mock_open)
    with pytest.raises(PermissionError):
        wdj.write_dict_to_json(str(file_path), data)
