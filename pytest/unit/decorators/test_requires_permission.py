import pytest
import logging
import re
from decorators.requires_permission import requires_permission

# Configure test_logger
test_logger = logging.getLogger("test_logger")
test_logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
test_logger.addHandler(handler)


# Sample function to be decorated
@requires_permission("admin")
def sample_function() -> str:
    return "Function executed"


def test_requires_permission_success():
    """
    Test case 1: User has the required permission
    """
    assert sample_function(["admin"]) == "Function executed"


def test_requires_permission_with_args():
    """
    Test case 2: Function with positional arguments
    """

    @requires_permission("admin")
    def function_with_args(user_permissions: list[str], a: int, b: int) -> int:
        return a + b

    assert function_with_args(["admin"], 1, 2) == 3


def test_requires_permission_with_kwargs():
    """
    Test case 3: Function with keyword arguments
    """

    @requires_permission("admin")
    def function_with_kwargs(user_permissions: list[str], a: int, b: int = 0) -> int:
        return a + b

    assert function_with_kwargs(["admin"], 1, b=2) == 3


def test_requires_permission_with_var_args():
    """
    Test case 4: Function with variable length arguments (*args and **kwargs)
    """

    @requires_permission("admin")
    def function_with_var_args(
        user_permissions: list[str], a: int, *args: str, **kwargs: float
    ) -> str:
        return f"{a} - {args} - {kwargs}"

    assert (
        function_with_var_args(["admin"], 1, "arg1", "arg2", kwarg1=1.0, kwarg2=2.0)
        == "1 - ('arg1', 'arg2') - {'kwarg1': 1.0, 'kwarg2': 2.0}"
    )


def test_requires_permission_invalid_permission_type():
    """
    Test case 5: Invalid permission type for requires_permission decorator
    """
    with pytest.raises(TypeError, match="permission must be a string"):

        @requires_permission(123)
        def invalid_permission_type_function() -> None:
            pass


def test_requires_permission_type_with_logger(caplog):
    """
    Test case 6: Logger functionality when type error occurs for permission
    """
    with caplog.at_level(logging.ERROR):
        with pytest.raises(TypeError, match="permission must be a string"):

            @requires_permission(123, logger=test_logger)
            def invalid_logger_function() -> None:
                pass

        assert (
            "Type error in requires_permission decorator: permission must be a string"
            in caplog.text
        )


def test_requires_permission_no_permissions():
    """
    Test case 7: User has no permissions
    """
    with pytest.raises(
        PermissionError, match="User does not have the required permission."
    ):
        sample_function([])


def test_requires_permission_permission_not_list():
    """
    Test case 8: User permissions is not a list
    """
    with pytest.raises(TypeError, match="user_permissions must be a list."):
        sample_function("admin")


def test_requires_permission_permission_not_list_with_logger(caplog):
    """
    Test case 9: Logger functionality when type error occurs
    """

    @requires_permission("admin", logger=test_logger)
    def logged_function() -> str:
        return "Function executed"

    with caplog.at_level(logging.ERROR):
        with pytest.raises(TypeError, match="user_permissions must be a list."):
            logged_function("admin")
        assert (
            "Type error in logged_function: user_permissions must be a list."
            in caplog.text
        )


def test_requires_permission_failure():
    """
    Test case 10: User does not have the required permission
    """
    with pytest.raises(
        PermissionError, match="User does not have the required permission."
    ):
        sample_function(["user"])


def test_requires_permission_with_logger(caplog):
    """
    Test case 11: Logger functionality when permission error occurs
    """

    @requires_permission("admin", logger=test_logger)
    def logged_function() -> str:
        return "Function executed"

    with caplog.at_level(logging.ERROR):
        with pytest.raises(
            PermissionError,
            match=re.escape(
                "User does not have the required permission. Required permission: 'admin', User permissions: ['user']"
            ),
        ):
            logged_function(["user"])
        assert (
            "User does not have the required permission. Required permission: 'admin', User permissions: ['user']"
            in caplog.text
        )


def test_invalid_permission_type():
    """
    Test case 12: Invalid permission type
    """
    with pytest.raises(TypeError, match="permission must be a string"):

        @requires_permission(123)
        def invalid_permission_type_function() -> None:
            pass


def test_invalid_logger_type():
    """
    Test case 13: Invalid logger type
    """
    with pytest.raises(
        TypeError, match="logger must be an instance of logging.Logger or None"
    ):

        @requires_permission("admin", logger="not_a_logger")
        def invalid_logger_function() -> None:
            pass
