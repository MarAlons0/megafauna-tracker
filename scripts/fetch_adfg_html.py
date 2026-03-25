"""
Diagnostic script — fetch ADF&G report pages and print their HTML.
Run this locally to inspect page structure before writing the scraper.

Usage:
    python scripts/fetch_adfg_html.py
"""

import requests
from bs4 import BeautifulSoup

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

AREAS = {
    'Southern Kenai': 8,
    'Anchorage':      1,
    'Mat-Su':         29,
}

BASE = 'https://www.adfg.alaska.gov/sf/FishingReports/index.cfm'

for name, key in AREAS.items():
    url = f'{BASE}?ADFG=R2.reportDetail&area_key={key}'
    print(f'\n{"="*60}')
    print(f'Area: {name} (area_key={key})')
    print(f'URL:  {url}')
    print('='*60)

    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        print(f'Status: {r.status_code}')

        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')

            # Remove nav, header, footer, scripts, styles to reduce noise
            for tag in soup(['nav', 'header', 'footer', 'script', 'style']):
                tag.decompose()

            # Try to find main content area
            main = (
                soup.find(id='mainContent') or
                soup.find(id='content') or
                soup.find('main') or
                soup.find(class_='content') or
                soup.find('body')
            )

            print('\n--- Main content HTML (first 4000 chars) ---\n')
            print(str(main)[:4000])
        else:
            print(f'Error body: {r.text[:500]}')

    except Exception as e:
        print(f'Request failed: {e}')
