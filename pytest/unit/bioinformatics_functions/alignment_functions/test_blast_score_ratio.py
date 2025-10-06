import pytest
from bioinformatics_functions.alignment_functions.blast_score_ratio import blast_score_ratio


def test_blast_score_ratio_typical() -> None:
    """
    Test case 1: Typical BSR calculation.
    """
    ref = 200.0
    tgt = 150.0
    result = blast_score_ratio(ref, tgt)
    assert isinstance(result, float)
    assert result == 0.75


def test_blast_score_ratio_equal_scores() -> None:
    """
    Test case 2: BSR is 1.0 when scores are equal.
    """
    ref = 100.0
    tgt = 100.0
    result = blast_score_ratio(ref, tgt)
    assert result == 1.0


def test_blast_score_ratio_zero_target() -> None:
    """
    Test case 3: BSR is 0.0 when target score is zero.
    """
    ref = 100.0
    tgt = 0.0
    result = blast_score_ratio(ref, tgt)
    assert result == 0.0


def test_blast_score_ratio_int_inputs() -> None:
    """
    Test case 4: Accepts integer inputs.
    """
    ref = 50
    tgt = 25
    result = blast_score_ratio(ref, tgt)
    assert result == 0.5


def test_blast_score_ratio_type_error_reference() -> None:
    """
    Test case 5: TypeError for non-numeric reference_score.
    """
    with pytest.raises(TypeError):
        blast_score_ratio("200", 150.0)


def test_blast_score_ratio_type_error_target() -> None:
    """
    Test case 6: TypeError for non-numeric target_score.
    """
    with pytest.raises(TypeError):
        blast_score_ratio(200.0, "150")


def test_blast_score_ratio_value_error_reference() -> None:
    """
    Test case 7: ValueError for zero or negative reference_score.
    """
    with pytest.raises(ValueError):
        blast_score_ratio(0, 100.0)
    with pytest.raises(ValueError):
        blast_score_ratio(-10, 100.0)
