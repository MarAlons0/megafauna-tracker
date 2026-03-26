"""
iNaturalist API client for fetching wildlife observation data.

API docs: https://api.inaturalist.org/v1/docs/
No auth required for reads.
Rate limit: ~1 req/sec, ~10k/day.
"""

import logging
import requests
from datetime import datetime, timedelta
from species_config import TAXON_TO_GROUP, ALL_TAXON_IDS

logger = logging.getLogger(__name__)

INATURALIST_BASE = 'https://api.inaturalist.org/v1'
MILES_TO_KM = 1.60934


class iNaturalistClient:
    """Client for fetching megafauna observations from iNaturalist."""

    VALID_QUALITY_GRADES = {'research', 'research,needs_id', 'any'}

    def get_observations(self, lat, lng, radius_miles, days, taxon_ids=None, quality_grade='research'):
        """
        Fetch observations near a point.

        Args:
            lat: Latitude
            lng: Longitude
            radius_miles: Search radius in miles (converted to km for API)
            days: Number of days back to search
            taxon_ids: List of taxon IDs to filter by. None = all tracked species.
            quality_grade: 'research' | 'research,needs_id' | 'any'

        Returns:
            dict with 'total', 'observations', 'fetched_at'
        """
        if taxon_ids is None:
            taxon_ids = ALL_TAXON_IDS

        if quality_grade not in self.VALID_QUALITY_GRADES:
            quality_grade = 'research'

        radius_km = min(radius_miles * MILES_TO_KM, 200)  # API max ~200km
        days = min(days, 365)

        d1 = (datetime.utcnow() - timedelta(days=days)).strftime('%Y-%m-%d')
        d2 = datetime.utcnow().strftime('%Y-%m-%d')

        # 'any' means no quality_grade filter — omit the param entirely
        params = {
            'lat': lat,
            'lng': lng,
            'radius': radius_km,
            'd1': d1,
            'd2': d2,
            'per_page': 200,
            'order': 'desc',
            'order_by': 'observed_on',
            'photos': 'true',
        }
        if quality_grade != 'any':
            params['quality_grade'] = quality_grade

        # Add taxon_id params (iNaturalist accepts multiple taxon_id[] values)
        observations = []
        # Chunk taxon_ids to stay within URL length limits
        chunk_size = 30
        for i in range(0, len(taxon_ids), chunk_size):
            chunk = taxon_ids[i:i + chunk_size]
            chunk_obs = self._fetch_page(params, chunk)
            observations.extend(chunk_obs)

        # De-duplicate by observation ID
        seen = set()
        unique = []
        for obs in observations:
            if obs['id'] not in seen:
                seen.add(obs['id'])
                unique.append(obs)

        # Sort by observed_on descending
        unique.sort(key=lambda o: o['observed_on'], reverse=True)

        return {
            'total': len(unique),
            'observations': unique,
            'quality_grade': quality_grade,
            'fetched_at': datetime.utcnow().isoformat() + 'Z',
        }

    def _fetch_page(self, base_params, taxon_ids):
        """Fetch one page of observations for a list of taxon IDs."""
        try:
            params = dict(base_params)
            # Build taxon_id[] list
            taxon_params = [('taxon_id[]', tid) for tid in taxon_ids]

            response = requests.get(
                f'{INATURALIST_BASE}/observations',
                params=list(params.items()) + taxon_params,
                timeout=20,
                headers={'Accept': 'application/json'},
            )

            if response.status_code != 200:
                logger.error(f"iNaturalist API error: {response.status_code} — {response.text[:300]}")
                return []

            data = response.json()
            results = data.get('results', [])
            logger.info(f"iNaturalist: fetched {len(results)} observations")
            return [self._transform(r) for r in results]

        except requests.exceptions.Timeout:
            logger.error("iNaturalist API request timed out")
            return []
        except requests.exceptions.RequestException as e:
            logger.error(f"iNaturalist request failed: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error fetching iNaturalist data: {e}")
            return []

    def _transform(self, result):
        """Transform raw iNaturalist result into a clean dict."""
        taxon = result.get('taxon') or {}
        taxon_id = taxon.get('id')

        # Match group by exact taxon_id first, then by ancestor_ids.
        # iNaturalist may return subspecies taxon_ids that aren't in our map,
        # but their ancestor chain includes the genus/species we track.
        group = TAXON_TO_GROUP.get(taxon_id)
        if group is None:
            for ancestor_id in taxon.get('ancestor_ids', []):
                if ancestor_id in TAXON_TO_GROUP:
                    group = TAXON_TO_GROUP[ancestor_id]
                    break
        if group is None:
            group = 'other'

        # Best available location
        lat = result.get('latitude')
        lng = result.get('longitude')
        if lat is None or lng is None:
            loc = result.get('location', '')
            if loc and ',' in str(loc):
                parts = str(loc).split(',')
                try:
                    lat = float(parts[0])
                    lng = float(parts[1])
                except (ValueError, IndexError):
                    lat = lng = None

        # Photo thumbnail
        photo_url = None
        photos = result.get('photos') or []
        if photos:
            url = photos[0].get('url', '')
            photo_url = url.replace('square', 'medium') if url else None

        return {
            'id': result.get('id'),
            'taxon_id': taxon_id,
            'species_name': taxon.get('name', 'Unknown'),
            'common_name': taxon.get('preferred_common_name') or taxon.get('name', 'Unknown'),
            'group': group,
            'lat': lat,
            'lng': lng,
            'observed_on': result.get('observed_on', ''),
            'observer': (result.get('user') or {}).get('login', 'unknown'),
            'photo_url': photo_url,
            'inaturalist_url': f"https://www.inaturalist.org/observations/{result.get('id')}",
            'quality_grade': result.get('quality_grade', ''),
            'place_guess': result.get('place_guess', ''),
        }


# Singleton
_client = None


def get_client():
    global _client
    if _client is None:
        _client = iNaturalistClient()
    return _client
