import sys
from unittest.mock import patch

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.print_functions]
from print_functions.print_dependencies_info_in_terminal import (
    print_dependencies_info_in_terminal,
)


def test_print_dependencies_info_in_terminal_installed(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """
    Test case 1: Dependency is installed, prints version info.
    """
    mod = sys.modules["print_functions.print_dependencies_info_in_terminal"]
    monkeypatch.setattr(mod, "version", lambda dep: "1.2.3")
    print_dependencies_info_in_terminal(["pytest"])
    out = capsys.readouterr().out
    assert "pytest version: 1.2.3" in out


def test_print_dependencies_info_in_terminal_not_installed(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """
    Test case 2: Dependency is not installed, prints warning.
    """

    class DummyException(Exception):
        pass

    def raise_not_found(dep: str) -> None:
        raise DummyException()

    mod = sys.modules["print_functions.print_dependencies_info_in_terminal"]
    monkeypatch.setattr(mod, "version", raise_not_found)
    monkeypatch.setattr(mod, "PackageNotFoundError", DummyException)
    print_dependencies_info_in_terminal(["not_installed"])
    out = capsys.readouterr().out
    assert "not_installed is not installed" in out


def test_print_dependencies_info_in_terminal_separator_and_title(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    Test case 3: Prints separator and title.
    """
    with patch(
        "print_functions.print_dependencies_info_in_terminal.version",
        lambda dep: "1.0.0",
    ):
        print_dependencies_info_in_terminal(["pytest"])
        out = capsys.readouterr().out
        assert "Dependencies Information" in out
        assert "=" in out
