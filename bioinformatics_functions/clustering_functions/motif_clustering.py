from typing import Sequence
from sklearn.cluster import KMeans
import numpy as np

def motif_clustering(motifs: Sequence[str], n_clusters: int = 2) -> list[int]:
    """
    Cluster motifs using k-means on one-hot encoded representations.

    Parameters
    ----------
    motifs : Sequence[str]
        List of motifs (equal length).
    n_clusters : int, optional
        Number of clusters (default 2).

    Returns
    -------
    list[int]
        Cluster labels for each motif.

    Raises
    ------
    ValueError
        If motifs are not all the same length or empty.

    Examples
    --------
    >>> motif_clustering(["ATGC", "ATGT", "GTGC"], n_clusters=2)
    [0, 0, 1]

    Complexity
    ----------
    Time: O(n*m), Space: O(n*m)
    """
    if not motifs:
        raise ValueError("motifs cannot be empty")
    length = len(motifs[0])
    if any(len(m) != length for m in motifs):
        raise ValueError("All motifs must be the same length")
    # One-hot encoding
    alphabet = sorted(set(''.join(motifs)))
    char_to_idx = {c: i for i, c in enumerate(alphabet)}
    X = np.zeros((len(motifs), length * len(alphabet)), dtype=int)
    for i, motif in enumerate(motifs):
        for j, char in enumerate(motif):
            idx = j * len(alphabet) + char_to_idx[char]
            X[i, idx] = 1
    kmeans = KMeans(n_clusters=n_clusters, n_init=10)
    labels = kmeans.fit_predict(X)
    return labels.tolist()

__all__ = ['motif_clustering']
