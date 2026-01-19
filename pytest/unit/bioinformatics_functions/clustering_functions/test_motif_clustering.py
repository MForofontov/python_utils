try:
    import numpy as np

    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    np = None  # type: ignore

import pytest
from python_utils.bioinformatics_functions.clustering_functions.motif_clustering import (
    motif_clustering,
)

pytestmark = pytest.mark.skipif(not NUMPY_AVAILABLE, reason="numpy not installed")
pytestmark = [pytestmark, pytest.mark.unit, pytest.mark.bioinformatics]


def test_motif_clustering_two_clusters() -> None:
    """
    Test case 1: Cluster motifs into two groups.
    """
    # Arrange
    motifs = ["ATGC", "ATGT", "GTGC"]
    n_clusters = 2

    # Act
    result = motif_clustering(motifs, n_clusters=n_clusters)

    # Assert
    assert len(result) == 3
    assert all(isinstance(label, (int, np.integer)) for label in result)
    assert len(set(result)) <= n_clusters


def test_motif_clustering_single_cluster() -> None:
    """
    Test case 2: Cluster all motifs into one group.
    """
    # Arrange
    motifs = ["ATGC", "ATGT", "GTGC"]
    n_clusters = 1

    # Act
    result = motif_clustering(motifs, n_clusters=n_clusters)

    # Assert
    assert len(result) == 3
    assert all(label == 0 for label in result)


def test_motif_clustering_many_clusters() -> None:
    """
    Test case 3: Number of clusters equals number of motifs.
    """
    # Arrange
    motifs = ["AAAA", "TTTT", "GGGG", "CCCC"]
    n_clusters = 4

    # Act
    result = motif_clustering(motifs, n_clusters=n_clusters)

    # Assert
    assert len(result) == 4
    assert len(set(result)) <= n_clusters


def test_motif_clustering_identical_motifs() -> None:
    """
    Test case 4: All identical motifs should be in same cluster.
    """
    # Arrange
    motifs = ["ATGC", "ATGC", "ATGC"]
    n_clusters = 2

    # Act
    result = motif_clustering(motifs, n_clusters=n_clusters)

    # Assert
    assert len(result) == 3
    # All should be in same cluster since they're identical
    assert len(set(result)) == 1


def test_motif_clustering_default_clusters() -> None:
    """
    Test case 5: Default number of clusters is 2.
    """
    # Arrange
    motifs = ["ATGC", "ATGT", "GTGC", "GGGG"]

    # Act
    result = motif_clustering(motifs)

    # Assert
    assert len(result) == 4
    assert len(set(result)) <= 2


def test_motif_clustering_long_motifs() -> None:
    """
    Test case 6: Clustering with longer motifs.
    """
    # Arrange
    motifs = ["ATGCATGCATGC", "ATGCATGCATGT", "GTGCGTGCGTGC"]
    n_clusters = 2

    # Act
    result = motif_clustering(motifs, n_clusters=n_clusters)

    # Assert
    assert len(result) == 3
    assert all(isinstance(label, (int, np.integer)) for label in result)


def test_motif_clustering_many_motifs() -> None:
    """
    Test case 7: Clustering with many motifs.
    """
    # Arrange
    motifs = ["ATGC", "ATGT", "GTGC", "GGGG", "AAAA", "TTTT", "CCCC", "AGCT"]
    n_clusters = 3

    # Act
    result = motif_clustering(motifs, n_clusters=n_clusters)

    # Assert
    assert len(result) == 8
    assert len(set(result)) <= n_clusters


def test_motif_clustering_value_error_empty_motifs() -> None:
    """
    Test case 8: ValueError for empty motifs list.
    """
    # Arrange
    empty_motifs = []  # type: ignore
    expected_message = "motifs cannot be empty"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        motif_clustering(empty_motifs)


def test_motif_clustering_value_error_unequal_length() -> None:
    """
    Test case 9: ValueError when motifs have different lengths.
    """
    # Arrange
    unequal_motifs = ["ATGC", "ATG", "ATGCG"]
    expected_message = "All motifs must be the same length"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        motif_clustering(unequal_motifs)


def test_motif_clustering_value_error_single_short_motif() -> None:
    """
    Test case 10: ValueError with mixed short and long motifs.
    """
    # Arrange
    mixed_motifs = ["ATGC", "A", "ATGC"]
    expected_message = "All motifs must be the same length"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        motif_clustering(mixed_motifs)
