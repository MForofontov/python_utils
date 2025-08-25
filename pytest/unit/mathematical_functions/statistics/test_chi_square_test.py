import pytest
from mathematical_functions.statistics.chi_square_test import chi_square_test


def test_chi_square_test_independence() -> None:
    """
    Test case 1: Test chi-square test for independence with known result.
    """
    # Simple 2x2 contingency table
    observed = [
        [10, 10, 20],
        [20, 20, 40]
    ]
    
    statistic, p_value, dof, expected = chi_square_test(observed)
    
    assert isinstance(statistic, float)
    assert isinstance(p_value, float)
    assert isinstance(dof, int)
    assert isinstance(expected, list)
    assert 0.0 <= p_value <= 1.0
    assert dof == (len(observed) - 1) * (len(observed[0]) - 1)


def test_chi_square_test_perfect_independence() -> None:
    """
    Test case 2: Test chi-square test with perfect independence (low chi-square).
    """
    # Table with perfect proportional relationship
    observed = [
        [10, 20],
        [20, 40]
    ]
    
    statistic, p_value, dof, expected = chi_square_test(observed)
    
    # Should have very low chi-square statistic and high p-value
    assert statistic < 0.1
    assert p_value > 0.5


def test_chi_square_test_strong_association() -> None:
    """
    Test case 3: Test chi-square test with strong association (high chi-square).
    """
    # Table with strong association
    observed = [
        [50, 5],
        [5, 50]
    ]
    
    statistic, p_value, dof, expected = chi_square_test(observed)
    
    # Should have high chi-square statistic and low p-value
    assert statistic > 10.0
    assert p_value < 0.05


def test_chi_square_test_3x3_table() -> None:
    """
    Test case 4: Test chi-square test with 3x3 contingency table.
    """
    observed = [
        [10, 15, 20],
        [25, 30, 35],
        [40, 45, 50]
    ]
    
    statistic, p_value, dof, expected = chi_square_test(observed)
    
    assert dof == 4  # (3-1) * (3-1)
    assert len(expected) == 3
    assert len(expected[0]) == 3


def test_chi_square_test_single_cell_table() -> None:
    """
    Test case 5: Test chi-square test with 1x1 table (should raise error).
    """
    with pytest.raises(ValueError, match="Contingency table must be at least 2x2"):
        chi_square_test([[10]])


def test_chi_square_test_empty_table() -> None:
    """
    Test case 6: Test chi-square test with empty table.
    """
    with pytest.raises(ValueError, match="Contingency table cannot be empty"):
        chi_square_test([])


def test_chi_square_test_invalid_type() -> None:
    """
    Test case 7: Test chi-square test with invalid input type.
    """
    with pytest.raises(TypeError, match="observed must be a list"):
        chi_square_test("invalid")


def test_chi_square_test_non_rectangular() -> None:
    """
    Test case 8: Test chi-square test with non-rectangular table.
    """
    with pytest.raises(ValueError, match="All rows must have the same length"):
        chi_square_test([[1, 2], [3, 4, 5]])


def test_chi_square_test_negative_values() -> None:
    """
    Test case 9: Test chi-square test with negative values.
    """
    with pytest.raises(ValueError, match="All observed frequencies must be non-negative"):
        chi_square_test([[10, -5], [20, 15]])


def test_chi_square_test_non_numeric() -> None:
    """
    Test case 10: Test chi-square test with non-numeric values.
    """
    with pytest.raises(TypeError, match="All observed frequencies must be numeric"):
        chi_square_test([[10, "5"], [20, 15]])


def test_chi_square_test_zero_margin() -> None:
    """
    Test case 11: Test chi-square test with zero row or column sum.
    """
    with pytest.raises(ValueError, match="All row and column totals must be positive"):
        chi_square_test([[0, 0], [10, 20]])


def test_chi_square_test_expected_frequencies() -> None:
    """
    Test case 12: Test that expected frequencies are calculated correctly.
    """
    observed = [
        [10, 20],
        [30, 40]
    ]
    
    statistic, p_value, dof, expected = chi_square_test(observed)
    
    # Check expected frequencies sum to same totals
    row_totals_obs = [sum(row) for row in observed]
    col_totals_obs = [sum(observed[i][j] for i in range(len(observed))) for j in range(len(observed[0]))]
    
    row_totals_exp = [sum(row) for row in expected]
    col_totals_exp = [sum(expected[i][j] for i in range(len(expected))) for j in range(len(expected[0]))]
    
    for i in range(len(row_totals_obs)):
        assert abs(row_totals_obs[i] - row_totals_exp[i]) < 1e-10
    
    for j in range(len(col_totals_obs)):
        assert abs(col_totals_obs[j] - col_totals_exp[j]) < 1e-10
