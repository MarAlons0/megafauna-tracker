"""
TripPlanner wildlife-report provider.

Implements the shared Wildlife Report Provider Contract so Megafauna sightings
can appear as a section in TripPlanner's Daily Digest. See
TripPlanner/docs/WILDLIFE_PROVIDER_CONTRACT.md (authoritative spec).

Read-only, idempotent: maps a report request onto the iNaturalist client and
transforms recent observations into the contract's `items[]` shape. Responses
are cached keyed on lat/lng/radius/recency (not target_date), since the
recent-sightings data barely moves day to day.
"""

import logging
from datetime import datetime

from sources.inaturalist import get_client as get_inaturalist
from cache import cache_get, cache_set
from species_config import ALL_TAXON_IDS

logger = logging.getLogger(__name__)

CONTRACT_VERSION = '1.1'
DEFAULT_RADIUS_MI = 50
MAX_RADIUS_MI = 124          # ~200 km — iNaturalist API ceiling
DEFAULT_RECENCY_DAYS = 14
DEFAULT_MAX_ITEMS = 8
CACHE_TTL_HOURS = 12


def _section_title(destination_name):
    """'Megafauna near <first segment of the place name>'."""
    short = (destination_name or '').split(',')[0].strip() or 'your destination'
    return f"Megafauna near {short}"


def _to_item(obs):
    """Transform an iNaturalist observation into a contract items[] object."""
    return {
        'name': obs.get('common_name') or obs.get('species_name') or 'Unknown',
        'scientific_name': obs.get('species_name'),
        'location': obs.get('place_guess') or None,
        'lat': obs.get('lat'),
        'lng': obs.get('lng'),
        'date': obs.get('observed_on') or None,
        'source': 'iNaturalist',
        'source_url': obs.get('inaturalist_url'),
    }


def build_report(destination_name, lat, lng,
                 radius_mi=DEFAULT_RADIUS_MI,
                 recency_days=DEFAULT_RECENCY_DAYS,
                 max_items=DEFAULT_MAX_ITEMS):
    """
    Build a contract-shaped response body for a wildlife report request.

    Returns a dict ready to `jsonify`. Never raises for "nothing found" —
    an empty `items` list is a normal `200`.
    """
    section_title = _section_title(destination_name)
    now_iso = datetime.utcnow().isoformat() + 'Z'

    # No coordinates → we can't do a radius search. Return an empty section.
    if lat is None or lng is None:
        return {
            'contract_version': CONTRACT_VERSION,
            'section_title': section_title,
            'items': [],
            'empty_note': 'No coordinates provided for this destination.',
            'generated_at': now_iso,
        }

    radius_mi = min(max(int(radius_mi), 1), MAX_RADIUS_MI)
    recency_days = max(int(recency_days), 1)
    max_items = max(int(max_items), 0)

    cache_key = f"report_{lat:.4f}_{lng:.4f}_{radius_mi}_{recency_days}"
    cached = cache_get(cache_key)
    if cached is not None:
        observations = cached.get('observations', [])
    else:
        data = get_inaturalist().get_observations(
            lat, lng, radius_mi, recency_days, ALL_TAXON_IDS, 'research', page=1
        )
        observations = data.get('observations', [])
        cache_set(cache_key, {'observations': observations}, ttl_hours=CACHE_TTL_HOURS)

    # get_observations already sorts most-recent-first; cap at max_items.
    items = [_to_item(o) for o in observations[:max_items]]

    return {
        'contract_version': CONTRACT_VERSION,
        'section_title': section_title,
        'items': items,
        'empty_note': None if items else 'No recent megafauna sightings in this area.',
        'generated_at': now_iso,
    }
