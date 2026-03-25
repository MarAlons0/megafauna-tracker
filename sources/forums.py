"""
Alaska Outdoors Forums scraper — Phase 3 (optional, graceful degradation).

Scrapes recent posts from https://forums.outdoorsdirectory.com
scoped to "Russian River" + "bear" keyword search.

Fail silently — if this source is unavailable, suppress it rather than
showing an error. The app must function on iNaturalist data alone.
"""

import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

FORUMS_BASE = 'https://forums.outdoorsdirectory.com'
SEARCH_KEYWORDS = ['Russian River', 'bear']


def get_recent_posts():
    """
    Scrape recent forum posts. Returns list of dicts or empty list on failure.
    Never raises — graceful degradation only.
    """
    # TODO (Phase 3): implement with graceful degradation
    return []
