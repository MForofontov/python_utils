
import pytest

pytestmark = [pytest.mark.unit, pytest.mark.testing]
from python_utils.testing_functions.fixture_factories.create_temp_file_fixture import (
    create_temp_file_fixture,
)


def test_create_temp_file_fixture_default_parameters() -> None:
    """
    Test case 1: Create temp file with default parameters.
    """
    # Act & Assert
    with create_temp_file_fixture() as temp_file:
        assert temp_file.exists()
        assert temp_file.suffix == ".txt"
        assert temp_file.read_text() == ""

    # After context, file should be deleted
    assert not temp_file.exists()


def test_create_temp_file_fixture_with_content() -> None:
    """
    Test case 2: Create temp file with content.
    """
    # Arrange
    content = "test content"

    # Act & Assert
    with create_temp_file_fixture(content) as temp_file:
        assert temp_file.read_text() == content


def test_create_temp_file_fixture_custom_suffix() -> None:
    """
    Test case 3: Create temp file with custom suffix.
    """
    # Act & Assert
    with create_temp_file_fixture("", ".py") as temp_file:
        assert temp_file.suffix == ".py"


def test_create_temp_file_fixture_multiline_content() -> None:
    """
    Test case 4: Create temp file with multiline content.
    """
    # Arrange
    content = "line1\nline2\nline3"

    # Act & Assert
    with create_temp_file_fixture(content) as temp_file:
        assert temp_file.read_text() == content
        lines = temp_file.read_text().split("\n")
        assert len(lines) == 3


def test_create_temp_file_fixture_file_cleanup() -> None:
    """
    Test case 5: Verify file is deleted after context.
    """
    # Arrange
    file_path = None

    # Act
    with create_temp_file_fixture("test") as temp_file:
        file_path = temp_file
        assert file_path.exists()

    # Assert
    assert not file_path.exists()


def test_create_temp_file_fixture_type_error_content() -> None:
    """
    Test case 6: TypeError for invalid content type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="content must be a string"):
        with create_temp_file_fixture(123):
            pass


def test_create_temp_file_fixture_type_error_suffix() -> None:
    """
    Test case 7: TypeError for invalid suffix type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="suffix must be a string"):
        with create_temp_file_fixture("", 123):
            pass
