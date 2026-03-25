"""
ADF&G Salmon Weir Count scraper — Phase 2.

Scrapes Russian River and Kenai River sockeye counts from:
  https://www.adfg.alaska.gov/sf/FishCounts/

Bear density at Russian River correlates with salmon run intensity.
Cache TTL: 24 hours.
"""

import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

ADFG_URL = 'https://www.adfg.alaska.gov/sf/FishCounts/'


def get_salmon_counts():
    """
    Scrape current weir counts and return structured data.

    Returns:
        dict with count data, or raises Exception on failure.
    """
    # TODO (Phase 2): implement HTML scrape
    # Pre-build check: fetch page manually to confirm HTML structure before coding
    raise NotImplementedError("Phase 2 — ADF&G salmon counts not yet implemented")


def _parse_counts(html):
    """Parse weir count HTML. Implement after inspecting live page structure."""
    soup = BeautifulSoup(html, 'html.parser')
    # TODO: implement based on actual HTML structure
    return {}
