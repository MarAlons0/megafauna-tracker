"""
Audit megafauna classification across multiple ecosystems.

Two checks:
  1. TRACKED SPECIES — fetches observations using our taxon IDs, verifies
     every one maps to the expected group (catches wrong IDs or broken
     ancestor fallback).
  2. UNTRACKED MEGAFAUNA — fetches all observations at each location and
     flags large mammals we might be missing from our species list.

Usage:
    venv/bin/python3 scripts/audit_classification.py

No API key required (iNaturalist public API).
"""

import sys
import re
import time
import requests
from collections import defaultdict

sys.path.insert(0, '.')
from species_config import TAXON_TO_GROUP, ALL_TAXON_IDS, SPECIES_GROUPS

INATURALIST_API = 'https://api.inaturalist.org/v1'

# 4 locations chosen to maximise group diversity across distinct ecosystems
LOCATIONS = [
    ('Yellowstone NP, WY (Bears / Canids / Deer)',       44.428,  -110.588, 40),
    ('Kenai Peninsula, AK (Bears / Marine Mammals)',     60.489,  -150.796, 50),
    ('Pacific Coast, CA (Marine Mammals)',               36.800,  -121.900, 60),
    ('Gulf Coast / Everglades, FL (Alligator / Manatee)', 25.400,  -80.900, 50),
]

# Keywords that suggest an observation is a large mammal we might want to track.
# Used to surface missing-species candidates in the untracked sweep.
MEGAFAUNA_KEYWORDS = [
    'bear', 'wolf', 'coyote', 'fox', 'lynx', 'bobcat', 'cougar', 'panther',
    'lion', 'jaguar', 'ocelot', 'deer', 'elk', 'moose', 'caribou', 'bison',
    'pronghorn', 'sheep', 'goat', 'muskox', 'bison', 'antelope',
    'whale', 'dolphin', 'porpoise', 'seal', 'sea lion', 'walrus', 'otter',
    'manatee', 'dugong', 'alligator', 'crocodile', 'wolverine', 'badger',
    'skunk', 'raccoon', 'opossum', 'armadillo', 'javelina', 'peccary',
    'prairie dog', 'beaver', 'porcupine', 'marten', 'fisher',
]

def is_megafauna_candidate(common_name):
    name = common_name.lower()
    return any(re.search(r'\b' + re.escape(kw) + r'\b', name)
               for kw in MEGAFAUNA_KEYWORDS)

def classify(taxon):
    """Mirror the logic in sources/inaturalist.py _transform()."""
    taxon_id = taxon.get('id')
    group = TAXON_TO_GROUP.get(taxon_id)
    if group is None:
        for ancestor_id in taxon.get('ancestor_ids', []):
            if ancestor_id in TAXON_TO_GROUP:
                group = TAXON_TO_GROUP[ancestor_id]
                break
    return group  # None = unclassified

def fetch_tracked(lat, lng, radius_km, days=365):
    """Fetch observations of our tracked taxon IDs at this location."""
    observations = []
    chunk_size = 30
    for i in range(0, len(ALL_TAXON_IDS), chunk_size):
        chunk = ALL_TAXON_IDS[i:i + chunk_size]
        params = {
            'lat': lat, 'lng': lng, 'radius': radius_km,
            'per_page': 200, 'page': 1, 'photos': 'true',
            'quality_grade': 'research',
        }
        taxon_params = [('taxon_id[]', tid) for tid in chunk]
        r = requests.get(f'{INATURALIST_API}/observations',
                         params=list(params.items()) + taxon_params, timeout=30)
        if r.status_code == 200:
            observations.extend(r.json().get('results', []))
        time.sleep(0.5)
    return observations

def fetch_all_mammals(lat, lng, radius_km):
    """Fetch all mammal observations at this location (taxon_id 40151 = Mammalia)."""
    params = {
        'lat': lat, 'lng': lng, 'radius': radius_km,
        'taxon_id': 40151,  # Mammalia
        'per_page': 200, 'page': 1,
        'quality_grade': 'research',
    }
    r = requests.get(f'{INATURALIST_API}/observations', params=params, timeout=30)
    if r.status_code == 200:
        return r.json().get('results', [])
    return []

def audit_location(name, lat, lng, radius_km):
    print(f"\n{'='*65}")
    print(f"  {name}")
    print(f"{'='*65}")

    # ── Check 1: tracked species ──────────────────────────────────────
    print("\n[1] TRACKED SPECIES — verifying group assignment")
    obs = fetch_tracked(lat, lng, radius_km)

    seen = {}  # taxon_id → (common_name, assigned_group, expected_group)
    mismatches = []

    for o in obs:
        taxon = o.get('taxon') or {}
        tid = taxon.get('id')
        if not tid or tid in seen:
            continue
        common = taxon.get('preferred_common_name') or taxon.get('name', '?')
        assigned = classify(taxon)
        # Expected group = whichever group directly owns this taxon_id
        expected = TAXON_TO_GROUP.get(tid)
        seen[tid] = (common, assigned, expected)
        if assigned != expected and expected is not None:
            mismatches.append((common, tid, expected, assigned))

    by_group = defaultdict(list)
    for tid, (common, assigned, _) in seen.items():
        by_group[assigned or 'UNCLASSIFIED'].append(common)

    for group_key, group_data in SPECIES_GROUPS.items():
        items = sorted(by_group[group_key])
        if items:
            print(f"  {group_data['label'].upper()} ({len(items)}): {', '.join(items)}")

    unclassified = sorted(by_group['UNCLASSIFIED'])
    if unclassified:
        print(f"\n  ⚠ UNCLASSIFIED ({len(unclassified)}): {', '.join(unclassified)}")
    else:
        print(f"\n  ✓ All {len(seen)} tracked species classified correctly")

    if mismatches:
        print(f"\n  ✗ GROUP MISMATCHES ({len(mismatches)}):")
        for common, tid, expected, assigned in mismatches:
            print(f"    {common} (id={tid}): expected '{expected}', got '{assigned}'")

    # ── Check 2: untracked mammals ────────────────────────────────────
    print("\n[2] ALL MAMMALS — flagging untracked megafauna candidates")
    time.sleep(0.5)
    all_mammals = fetch_all_mammals(lat, lng, radius_km)

    untracked_candidates = {}
    for o in all_mammals:
        taxon = o.get('taxon') or {}
        tid = taxon.get('id')
        if tid in TAXON_TO_GROUP:
            continue  # already tracked
        # Check ancestor chain too
        if any(a in TAXON_TO_GROUP for a in taxon.get('ancestor_ids', [])):
            continue
        common = taxon.get('preferred_common_name') or taxon.get('name', '?')
        if is_megafauna_candidate(common) and tid not in untracked_candidates:
            sci = taxon.get('name', '')
            untracked_candidates[tid] = (common, sci)

    if untracked_candidates:
        print(f"  Potential missing species ({len(untracked_candidates)}):")
        for tid, (common, sci) in sorted(untracked_candidates.items(),
                                          key=lambda x: x[1][0]):
            print(f"    {common} ({sci})  id={tid}")
    else:
        print("  No untracked megafauna candidates found")

    return mismatches, unclassified, list(untracked_candidates.values())


if __name__ == '__main__':
    all_mismatches = []
    all_unclassified = []
    all_candidates = []

    for name, lat, lng, radius_km in LOCATIONS:
        mismatches, unclassified, candidates = audit_location(name, lat, lng, radius_km)
        all_mismatches.extend(mismatches)
        all_unclassified.extend(unclassified)
        all_candidates.extend(candidates)

    print(f"\n{'='*65}")
    print("CONSOLIDATED SUMMARY")
    print(f"{'='*65}")

    if all_mismatches:
        print(f"\n✗ Group mismatches (fix taxon IDs or TAXON_TO_GROUP):")
        for common, tid, expected, assigned in sorted(set(all_mismatches)):
            print(f"  {common} (id={tid}): expected '{expected}', got '{assigned}'")
    else:
        print("\n✓ No group mismatches — all tracked species classify correctly")

    if all_unclassified:
        unique = sorted(set(all_unclassified))
        print(f"\n⚠ Unclassified tracked species ({len(unique)}):")
        for s in unique:
            print(f"  {s}")
    else:
        print("✓ No unclassified tracked species")

    if all_candidates:
        unique = sorted(set(c[0] for c in all_candidates))
        print(f"\n? Untracked megafauna candidates — consider adding ({len(unique)}):")
        for s in unique:
            print(f"  {s}")
    else:
        print("✓ No untracked megafauna candidates found")
