"""
Configure default export settings for matplotlib.
"""

import logging
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


def configure_export_defaults(
    dpi: int = 300,
    format: str = 'png',
    bbox_inches: str = 'tight',
    transparent: bool = False,
) -> None:
    """
    Configure default export settings for matplotlib.

    Parameters
    ----------
    dpi : int, optional
        Default resolution in dots per inch (by default 300).
    format : str, optional
        Default output format (by default 'png').
    bbox_inches : str, optional
        Default bounding box (by default 'tight').
    transparent : bool, optional
        Default transparency setting (by default False).

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If dpi is invalid or format is unsupported.

    Examples
    --------
    >>> configure_export_defaults(dpi=600, format='pdf')
    >>> # All subsequent saves will use these defaults

    >>> configure_export_defaults(transparent=True, bbox_inches='tight')

    Notes
    -----
    Settings apply to all figures saved after calling this function.
    Use plt.rcParams to modify matplotlib defaults globally.

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    # Type validation
    if not isinstance(dpi, int):
        raise TypeError(f"dpi must be an integer, got {type(dpi).__name__}")

    if not isinstance(format, str):
        raise TypeError(f"format must be a string, got {type(format).__name__}")

    if not isinstance(bbox_inches, str):
        raise TypeError(
            f"bbox_inches must be a string, got {type(bbox_inches).__name__}"
        )

    if not isinstance(transparent, bool):
        raise TypeError(
            f"transparent must be a boolean, got {type(transparent).__name__}"
        )

    # Value validation
    if dpi < 1:
        raise ValueError(f"dpi must be positive, got {dpi}")

    valid_formats = ['png', 'pdf', 'svg', 'jpg', 'jpeg', 'eps', 'ps', 'tiff']
    if format.lower() not in valid_formats:
        raise ValueError(
            f"format must be one of {valid_formats}, got '{format}'"
        )

    logger.debug(
        f"Configuring export defaults: dpi={dpi}, format={format}, "
        f"bbox_inches={bbox_inches}, transparent={transparent}"
    )

    # Configure matplotlib defaults
    plt.rcParams['savefig.dpi'] = dpi
    plt.rcParams['savefig.format'] = format.lower()
    plt.rcParams['savefig.bbox'] = bbox_inches
    plt.rcParams['savefig.transparent'] = transparent

    logger.info(
        f"Export defaults configured: {dpi} dpi, {format} format, "
        f"bbox={bbox_inches}, transparent={transparent}"
    )


__all__ = ['configure_export_defaults']
