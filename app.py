"""
Megafauna Tracker — Flask application.

Endpoints:
  GET /                         Main UI
  GET /sightings                iNaturalist observations near a point
  GET /species                  Priority species list by route segment
  GET /salmon-count             ADF&G weir count + bear forecast (Phase 2)
  GET /local-conditions         ADF&G report summary (Phase 2)
  GET /health                   Render health check
"""

import logging
import os
import requests as http_requests
from datetime import datetime
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from dotenv import load_dotenv

from sources.inaturalist import get_client as get_inaturalist
from cache import cache_get, cache_set, cache_info
from species_config import SPECIES_GROUPS, ROUTE_SEGMENTS, SEGMENT_ORDER, ALL_TAXON_IDS

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

APP_VERSION = '0.5.2'


def create_app():
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    static_dir = os.path.join(os.path.dirname(__file__), 'static')

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    CORS(app)

    @app.context_processor
    def inject_version():
        return {'app_version': APP_VERSION}

    inaturalist = get_inaturalist()

    # ── UI ──────────────────────────────────────────────────────────────

    @app.route('/')
    def index():
        return render_template(
            'index.html',
            species_groups=SPECIES_GROUPS,
            route_segments=ROUTE_SEGMENTS,
            segment_order=SEGMENT_ORDER,
        )

    # ── API ─────────────────────────────────────────────────────────────

    @app.route('/sightings')
    def sightings():
        """
        GET /sightings?lat=&lng=&radius=&days=&groups=bears&groups=canids
        Drill-down mode: pass taxon_id=<id>&taxon_id=<id> instead of groups.
        """
        lat = request.args.get('lat', type=float)
        lng = request.args.get('lng', type=float)
        radius = request.args.get('radius', 25, type=int)
        days = request.args.get('days', 30, type=int)
        groups = request.args.getlist('groups')
        taxon_id_overrides = request.args.getlist('taxon_id', type=int)
        quality_grade = request.args.get('quality_grade', 'research')
        segment = request.args.get('segment', '')
        page = request.args.get('page', 1, type=int)

        if lat is None or lng is None:
            return jsonify({'error': 'lat and lng are required'}), 400

        if taxon_id_overrides:
            # Drill-down mode: caller specifies exact taxon IDs
            taxon_ids = taxon_id_overrides
            cache_key = (
                f"sightings_{lat:.4f}_{lng:.4f}_{radius}_{days}"
                f"_{quality_grade}_drill_p{page}"
                f"_{'_'.join(str(t) for t in sorted(taxon_ids))}"
            )
        else:
            # Group mode: resolve taxon_ids from group names
            if groups:
                taxon_ids = []
                for g in groups:
                    if g in SPECIES_GROUPS:
                        taxon_ids.extend(SPECIES_GROUPS[g]['taxon_ids'])
                if not taxon_ids:
                    return jsonify({'error': f'Unknown groups: {groups}'}), 400
            else:
                taxon_ids = ALL_TAXON_IDS

            # When a segment is selected, intersect with segment's priority taxon_ids
            if segment and segment in ROUTE_SEGMENTS:
                seg_ids = set(ROUTE_SEGMENTS[segment].get('taxon_ids', []))
                intersected = [t for t in taxon_ids if t in seg_ids]
                if intersected:
                    taxon_ids = intersected

            cache_key = (
                f"sightings_{lat:.4f}_{lng:.4f}_{radius}_{days}"
                f"_{quality_grade}_{segment or 'any'}_p{page}"
                f"_{'_'.join(sorted(groups or ['all']))}"
            )
        cached = cache_get(cache_key)
        if cached:
            return jsonify(cached)

        try:
            data = inaturalist.get_observations(
                lat, lng, radius, days, taxon_ids, quality_grade, page
            )
            cache_set(cache_key, data, ttl_hours=1)
            return jsonify(data)
        except Exception as e:
            logger.error(f"Sightings error: {e}")
            return jsonify({'error': 'Failed to fetch sightings'}), 500

    @app.route('/species')
    def species():
        """
        GET /species?segment=kenai_peninsula
        Returns priority species for a route segment (or all segments).
        """
        segment = request.args.get('segment')
        if segment:
            if segment not in ROUTE_SEGMENTS:
                return jsonify({'error': f'Unknown segment: {segment}'}), 400
            return jsonify({segment: ROUTE_SEGMENTS[segment]})
        # Return all segments (ordered)
        return jsonify({k: ROUTE_SEGMENTS[k] for k in SEGMENT_ORDER})

    @app.route('/salmon-count')
    def salmon_count():
        """ADF&G weir count + AI bear forecast (Phase 2)."""
        cached = cache_get('salmon_count')
        if cached:
            return jsonify(cached)

        try:
            from sources.adfg_fishcounts import get_salmon_counts
            data = get_salmon_counts()
            cache_set('salmon_count', data, ttl_hours=24)
            return jsonify(data)
        except NotImplementedError:
            return jsonify({'available': False, 'message': 'Coming in Phase 2'}), 200
        except Exception as e:
            logger.warning(f"Salmon count unavailable: {e}")
            return jsonify({'available': False}), 200

    @app.route('/local-conditions')
    def local_conditions():
        """ADF&G report + Claude summarization."""
        cached = cache_get('local_conditions')
        if cached:
            return jsonify(cached)

        try:
            from sources.adfg_reports import get_local_conditions as fetch_conditions
            data = fetch_conditions()
            cache_set('local_conditions', data, ttl_hours=12)
            return jsonify(data)
        except Exception as e:
            logger.warning(f"Local conditions unavailable: {e}")
            return jsonify({'available': False, 'error': str(e)}), 200

    @app.route('/geocode')
    def geocode():
        """Proxy Nominatim geocoding (avoids browser User-Agent restrictions)."""
        q = request.args.get('q', '').strip()
        if not q:
            return jsonify({'error': 'q parameter required'}), 400
        try:
            resp = http_requests.get(
                'https://nominatim.openstreetmap.org/search',
                params={'q': q, 'format': 'json', 'limit': 5, 'addressdetails': 0},
                headers={'User-Agent': f'MegafaunaTracker/{APP_VERSION} (wildlife observation app)'},
                timeout=10,
            )
            return jsonify(resp.json())
        except Exception as e:
            logger.error(f"Geocode error: {e}")
            return jsonify([]), 200

    @app.route('/sources')
    def sources():
        """Return availability and cache status for all configured data sources."""
        source_defs = [
            {
                'id': 'inaturalist',
                'name': 'iNaturalist',
                'description': 'Research-grade wildlife observations',
                'available': True,
                'cache_key': None,  # per-query cache — no single key
            },
            {
                'id': 'adfg_fishcounts',
                'name': 'ADF&G Fish Counts',
                'description': 'Salmon weir counts (bear activity proxy)',
                'available': False,
                'cache_key': 'salmon_count',
            },
            {
                'id': 'adfg_reports',
                'name': 'ADF&G Reports',
                'description': 'Weekly fishing & wildlife reports',
                'available': True,
                'cache_key': 'local_conditions',
            },
            {
                'id': 'forums',
                'name': 'AK Forums',
                'description': 'Alaska Outdoors Forums trip reports',
                'available': False,
                'cache_key': 'forums',
            },
        ]
        result = []
        for src in source_defs:
            info = cache_info(src['cache_key']) if src['cache_key'] else None
            result.append({
                'id': src['id'],
                'name': src['name'],
                'description': src['description'],
                'available': src['available'],
                'cache_age_hours': info['age_hours'] if info else None,
                'cache_expired': info['expired'] if info else None,
            })
        return jsonify({'sources': result})

    @app.route('/health')
    def health():
        return jsonify({
            'status': 'healthy',
            'service': 'megafauna-tracker',
            'version': APP_VERSION,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
        })

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002, debug=True)
