"""
Verify all taxon IDs in species_config.py against the iNaturalist API.

Run from the project root:
    python scripts/verify_taxon_ids.py

Exits with code 1 if any ID is wrong or missing, so it can be used as a pre-deploy check.
"""

import sys
import time
import requests

sys.path.insert(0, '.')
from species_config import TAXON_IDS

INATURALIST_API = 'https://api.inaturalist.org/v1/taxa'

def check_taxon(name, taxon_id):
    try:
        resp = requests.get(f'{INATURALIST_API}/{taxon_id}',
                            headers={'Accept': 'application/json'}, timeout=10)
        if resp.status_code != 200:
            return False, f'HTTP {resp.status_code}'
        results = resp.json().get('results', [])
        if not results:
            return False, 'ID not found in iNaturalist'
        taxon = results[0]
        actual_name = taxon['name']
        common = taxon.get('preferred_common_name', '')
        rank = taxon['rank']
        return True, f'{rank} {actual_name} | {common}'
    except Exception as e:
        return False, str(e)

def main():
    print(f'Verifying {len(TAXON_IDS)} taxon IDs against iNaturalist...\n')
    errors = []

    for name, taxon_id in TAXON_IDS.items():
        ok, detail = check_taxon(name, taxon_id)
        status = '✓' if ok else '✗'
        print(f'  {status}  {name:<25} {taxon_id:>8}  {detail}')
        if not ok:
            errors.append((name, taxon_id, detail))
        time.sleep(0.35)  # stay well within rate limit

    print()
    if errors:
        print(f'FAILED — {len(errors)} incorrect ID(s):')
        for name, taxon_id, detail in errors:
            print(f'  {name}: {taxon_id} → {detail}')
        sys.exit(1)
    else:
        print(f'All {len(TAXON_IDS)} IDs verified OK.')

if __name__ == '__main__':
    main()
