"""
JSON file cache with TTL.
Stores cached data in a local .cache/ directory.
Upgrade to Redis later if needed.
"""

import json
import os
import time
import logging

logger = logging.getLogger(__name__)

CACHE_DIR = os.path.join(os.path.dirname(__file__), '.cache')


def _ensure_cache_dir():
    os.makedirs(CACHE_DIR, exist_ok=True)


def _cache_path(key):
    safe_key = key.replace('/', '_').replace('?', '_').replace('&', '_')
    return os.path.join(CACHE_DIR, f"{safe_key}.json")


def cache_get(key):
    """Return cached value if it exists and has not expired. Otherwise None."""
    _ensure_cache_dir()
    path = _cache_path(key)
    try:
        with open(path, 'r') as f:
            entry = json.load(f)
        if time.time() < entry['expires_at']:
            age_hours = (time.time() - entry['cached_at']) / 3600
            data = entry['data']
            if isinstance(data, dict):
                data['_cache_age_hours'] = round(age_hours, 2)
            return data
        # Expired — remove file
        os.remove(path)
    except FileNotFoundError:
        pass
    except Exception as e:
        logger.warning(f"Cache read error for '{key}': {e}")
    return None


def cache_set(key, data, ttl_hours=1):
    """Store data in cache with a TTL in hours."""
    _ensure_cache_dir()
    path = _cache_path(key)
    now = time.time()
    entry = {
        'cached_at': now,
        'expires_at': now + ttl_hours * 3600,
        'data': data,
    }
    try:
        with open(path, 'w') as f:
            json.dump(entry, f)
    except Exception as e:
        logger.warning(f"Cache write error for '{key}': {e}")


def cache_delete(key):
    """Invalidate a cache entry."""
    path = _cache_path(key)
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


def cache_info(key):
    """Return cache metadata for a key without modifying cache state.
    Returns dict with 'age_hours' and 'expired', or None if no file exists."""
    path = _cache_path(key)
    try:
        with open(path, 'r') as f:
            entry = json.load(f)
        now = time.time()
        age_hours = (now - entry['cached_at']) / 3600
        expired = now >= entry['expires_at']
        return {'age_hours': round(age_hours, 2), 'expired': expired}
    except FileNotFoundError:
        return None
    except Exception as e:
        logger.warning(f"Cache info error for '{key}': {e}")
        return None


def cache_clear_all():
    """Delete all cache files."""
    _ensure_cache_dir()
    for fname in os.listdir(CACHE_DIR):
        if fname.endswith('.json'):
            try:
                os.remove(os.path.join(CACHE_DIR, fname))
            except Exception:
                pass
