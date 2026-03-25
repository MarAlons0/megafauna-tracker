"""
ADF&G Weekly Fishing/Wildlife Report scraper.

Scrapes narrative reports from ADF&G Region 2 for three areas relevant
to the Alaska route: Southern Kenai, Anchorage, and Mat-Su.

Reports include fishing conditions, wildlife sightings, bear activity,
trail closures, and emergency orders.

Cache TTL: 12 hours.
"""

import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime

logger = logging.getLogger(__name__)

BASE_URL = 'https://www.adfg.alaska.gov/sf/FishingReports/index.cfm'
ADFG_ROOT = 'https://www.adfg.alaska.gov'

# Area keys verified March 2026
AREAS = {
    'southern_kenai': {'name': 'Southern Kenai/LCI', 'area_key': 8},
    'anchorage':      {'name': 'Anchorage',           'area_key': 1},
    'mat_su':         {'name': 'Mat-Su',              'area_key': 29},
}

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/122.0.0.0 Safari/537.36'
    ),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.adfg.alaska.gov/sf/FishingReports/',
}


def get_local_conditions():
    """
    Scrape current ADF&G reports for all three route areas and return
    structured data ready for the Conditions card.

    Returns:
        dict with 'areas', 'emergency_orders', 'report_date', 'fetched_at'
    """
    scraped = []
    all_emergency_orders = []
    report_date = ''

    for area_key_name, area in AREAS.items():
        try:
            result = _scrape_area(area['area_key'], area['name'])
            scraped.append(result)
            if not report_date and result.get('report_date'):
                report_date = result['report_date']
            # Collect unique emergency orders across areas
            for eo in result.get('emergency_orders', []):
                if eo['url'] not in {e['url'] for e in all_emergency_orders}:
                    all_emergency_orders.append(eo)
        except Exception as e:
            logger.warning(f"Failed to scrape {area['name']}: {e}")

    if not scraped:
        raise RuntimeError("All ADF&G area scrapes failed")

    # Pass combined narrative text to Claude for a unified conditions summary
    ai_summary = _get_ai_summary(scraped)

    return {
        'report_date': report_date,
        'areas_covered': [s['area'] for s in scraped],
        'emergency_orders': all_emergency_orders[:8],  # cap at 8 most recent
        'ai_summary': ai_summary,
        'fetched_at': datetime.utcnow().isoformat() + 'Z',
    }


def _scrape_area(area_key, area_name):
    """Fetch and parse one area's report page."""
    url = f'{BASE_URL}?ADFG=R2.reportDetail&area_key={area_key}'
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    # Report date and narrative — inside div.afterpadder > div.printPadding
    afterpadder = soup.find(class_='afterpadder')
    report_div = afterpadder.find(class_='printPadding') if afterpadder else None

    report_date = ''
    report_text = ''
    if report_div:
        date_tag = report_div.find('h3')
        if date_tag:
            report_date = date_tag.get_text(strip=True)
        report_text = report_div.get_text(separator='\n', strip=True)

    # Emergency orders from div#EOs
    emergency_orders = []
    eos_div = soup.find(id='EOs')
    if eos_div:
        for link in eos_div.select('ul li a'):
            title = link.get('title') or link.get_text(strip=True)
            href = link.get('href', '')
            # Skip the "All Emergency Orders" catch-all link
            if title and href and 'region.r2' not in href:
                emergency_orders.append({
                    'title': title,
                    'url': f'{ADFG_ROOT}{href}' if href.startswith('/') else href,
                })

    logger.info(f"Scraped ADF&G report: {area_name} ({report_date}), "
                f"{len(emergency_orders)} emergency orders")

    return {
        'area': area_name,
        'report_date': report_date,
        'report_text': report_text,
        'emergency_orders': emergency_orders,
    }


def _get_ai_summary(scraped_areas):
    """
    Pass combined report text to Claude for a unified conditions summary.
    Returns the summary dict, or a fallback if AI is unavailable.
    """
    try:
        from ai.summarizer import get_summarizer
        summarizer = get_summarizer()
        if not summarizer.is_available:
            return _fallback_summary(scraped_areas)

        # Combine reports from all areas into one text block
        combined = ''
        for area in scraped_areas:
            if area.get('report_text'):
                combined += f"\n\n=== {area['area']} (as of {area['report_date']}) ===\n"
                combined += area['report_text']

        return summarizer.summarize_report(combined) or _fallback_summary(scraped_areas)

    except Exception as e:
        logger.warning(f"AI summarization failed: {e}")
        return _fallback_summary(scraped_areas)


def _fallback_summary(scraped_areas):
    """Return minimal summary when Claude is unavailable."""
    dates = [a['report_date'] for a in scraped_areas if a.get('report_date')]
    return {
        'alerts': [],
        'sightings': [],
        'conditions_summary': (
            f"ADF&G reports fetched for {', '.join(a['area'] for a in scraped_areas)}. "
            f"AI summary unavailable — check ANTHROPIC_API_KEY."
        ),
    }
