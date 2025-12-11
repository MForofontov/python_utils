"""Pagination utilities."""

from .paginate_links import paginate_links
from .extract_next_page import extract_next_page
from .paginate_with_callback import paginate_with_callback

__all__ = [
    'paginate_links',
    'extract_next_page',
    'paginate_with_callback',
]
