import pytest
from web_scraping_functions.rotation.rotate_user_agent import rotate_user_agent


def test_rotate_user_agent_case_1_basic_rotation() -> None:
    """
    Test case 1: Basic user agent rotation.
    """
    # Arrange
    user_agents = ["UA1", "UA2", "UA3"]
    rotator = rotate_user_agent(user_agents)
    
    # Act
    result1 = next(rotator)
    result2 = next(rotator)
    result3 = next(rotator)
    result4 = next(rotator)
    
    # Assert
    assert result1 == "UA1"
    assert result2 == "UA2"
    assert result3 == "UA3"
    assert result4 == "UA1"  # Cycles back


def test_rotate_user_agent_case_2_single_user_agent() -> None:
    """
    Test case 2: Rotation with single user agent.
    """
    # Arrange
    user_agents = ["Mozilla/5.0"]
    rotator = rotate_user_agent(user_agents)
    
    # Act
    result1 = next(rotator)
    result2 = next(rotator)
    
    # Assert
    assert result1 == "Mozilla/5.0"
    assert result2 == "Mozilla/5.0"


def test_rotate_user_agent_case_3_infinite_cycling() -> None:
    """
    Test case 3: Verify infinite cycling.
    """
    # Arrange
    user_agents = ["UA1", "UA2"]
    rotator = rotate_user_agent(user_agents)
    
    # Act
    results = [next(rotator) for _ in range(8)]
    
    # Assert
    assert results == ["UA1", "UA2"] * 4


def test_rotate_user_agent_case_4_list_not_modified() -> None:
    """
    Test case 4: Original list is not modified.
    """
    # Arrange
    user_agents = ["UA1", "UA2", "UA3"]
    original_uas = user_agents.copy()
    rotator = rotate_user_agent(user_agents)
    
    # Act
    next(rotator)
    next(rotator)
    
    # Assert
    assert user_agents == original_uas


def test_rotate_user_agent_case_5_type_error_user_agents() -> None:
    """
    Test case 5: TypeError for invalid user_agents type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="user_agents must be a list"):
        rotate_user_agent("not a list")


def test_rotate_user_agent_case_6_value_error_empty_list() -> None:
    """
    Test case 6: ValueError for empty user agent list.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="user_agents cannot be empty"):
        rotate_user_agent([])


def test_rotate_user_agent_case_7_type_error_non_string_elements() -> None:
    """
    Test case 7: TypeError for non-string elements in list.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="all elements in user_agents must be strings"):
        rotate_user_agent(["UA1", 123, "UA3"])


def test_rotate_user_agent_case_8_realistic_user_agents() -> None:
    """
    Test case 8: Rotation with realistic user agent strings.
    """
    # Arrange
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    ]
    rotator = rotate_user_agent(user_agents)
    
    # Act
    result1 = next(rotator)
    result2 = next(rotator)
    
    # Assert
    assert "Windows NT 10.0" in result1
    assert "Macintosh" in result2
