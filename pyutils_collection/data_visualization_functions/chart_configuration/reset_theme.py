"""
Reset matplotlib configuration to default settings.
"""

import logging

import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


def reset_theme() -> None:
    """
    Reset matplotlib configuration to default settings.

    Examples
    --------
    >>> apply_theme(get_preset_theme('dark'))
    >>> # Create some plots...
    >>> reset_theme()
    >>> # Back to default matplotlib settings

    Notes
    -----
    This resets all matplotlib rcParams to their default values.

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    plt.rcdefaults()
    logger.info("Reset theme to matplotlib defaults")


__all__ = ["reset_theme"]
