import pytest
from web_scraping_functions.rotation.get_random_user_agent import (
    get_random_user_agent,
)


def test_get_random_user_agent_returns_from_list() -> None:
    """
    Test case 1: Return a user agent from the list.
    """
    # Arrange
    user_agents = ["UA1", "UA2", "UA3"]

    # Act
    result = get_random_user_agent(user_agents)

    # Assert
    assert result in user_agents


def test_get_random_user_agent_single_user_agent() -> None:
    """
    Test case 2: Return the only user agent from single-element list.
    """
    # Arrange
    user_agents = ["Mozilla/5.0"]

    # Act
    result = get_random_user_agent(user_agents)

    # Assert
    assert result == "Mozilla/5.0"


def test_get_random_user_agent_randomness() -> None:
    """
    Test case 3: Verify random selection over multiple calls.
    """
    # Arrange
    user_agents = ["UA1", "UA2", "UA3", "UA4", "UA5"]

    # Act
    results = {get_random_user_agent(user_agents) for _ in range(50)}

    # Assert - should get at least 2 different UAs in 50 calls
    assert len(results) >= 2


def test_get_random_user_agent_default_user_agents() -> None:
    """
    Test case 4: Use default user agents when None provided.
    """
    # Act
    result = get_random_user_agent()

    # Assert
    assert isinstance(result, str)
    assert len(result) > 0
    assert "Mozilla" in result


def test_get_random_user_agent_list_not_modified() -> None:
    """
    Test case 5: Original list is not modified.
    """
    # Arrange
    user_agents = ["UA1", "UA2", "UA3"]
    original_uas = user_agents.copy()

    # Act
    get_random_user_agent(user_agents)

    # Assert
    assert user_agents == original_uas


def test_get_random_user_agent_type_error_user_agents() -> None:
    """
    Test case 6: TypeError for invalid user_agents type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="user_agents must be a list or None"):
        get_random_user_agent("not a list")


def test_get_random_user_agent_value_error_empty_list() -> None:
    """
    Test case 7: ValueError for empty user agent list.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="user_agents list cannot be empty"):
        get_random_user_agent([])


def test_get_random_user_agent_realistic_user_agents() -> None:
    """
    Test case 9: Handle realistic user agent strings.
    """
    # Arrange
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    ]

    # Act
    result = get_random_user_agent(user_agents)

    # Assert
    assert result in user_agents
    assert "Mozilla/5.0" in result
