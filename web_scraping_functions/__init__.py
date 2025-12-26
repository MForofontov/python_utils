"""
Web scraping utilities module.

This module provides utilities for web scraping including HTML parsing,
pagination handling, rate limiting, session management, and selector utilities.
"""

from .html_parsing.parse_html import parse_html
from .html_parsing.extract_text import extract_text
from .html_parsing.extract_links import extract_links
from .html_parsing.extract_tables import extract_tables
from .html_parsing.find_elements_by_class import find_elements_by_class
from .html_parsing.find_elements_by_id import find_elements_by_id

from .pagination.paginate_links import paginate_links
from .pagination.extract_next_page import extract_next_page
from .pagination.paginate_with_callback import paginate_with_callback

from .rate_limiting.rate_limited_scraper import rate_limited_scraper
from .rate_limiting.create_rate_limiter import create_rate_limiter

from .rotation.rotate_proxy import rotate_proxy
from .rotation.rotate_user_agent import rotate_user_agent
from .rotation.get_random_proxy import get_random_proxy
from .rotation.get_random_user_agent import get_random_user_agent

from .selectors.select_by_css import select_by_css
from .selectors.select_by_xpath import select_by_xpath
from .selectors.extract_attribute import extract_attribute

__all__ = [
    # HTML parsing
    'parse_html',
    'extract_text',
    'extract_links',
    'extract_tables',
    'find_elements_by_class',
    'find_elements_by_id',
    
    # Pagination
    'paginate_links',
    'extract_next_page',
    'paginate_with_callback',
    
    # Rate limiting
    'rate_limited_scraper',
    'create_rate_limiter',
    
    # Rotation
    'rotate_proxy',
    'rotate_user_agent',
    'get_random_proxy',
    'get_random_user_agent',
    
    # Selectors
    'select_by_css',
    'select_by_xpath',
    'extract_attribute',
]

from _version import __version__
