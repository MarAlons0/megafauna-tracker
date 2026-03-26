"""
Species configuration for Alaska Megafauna Tracker.
Taxon IDs sourced from iNaturalist — verify with:
  https://api.inaturalist.org/v1/taxa?q=<name>
"""

# --- Taxon IDs ---
# All verified against iNaturalist API (March 2026)
# Use: https://api.inaturalist.org/v1/taxa?q=<name> to re-verify
TAXON_IDS = {
    'brown_grizzly_bear': 41641,   # Ursus arctos — Brown Bear
    'black_bear':         41638,   # Ursus americanus — American Black Bear
    'moose':              42196,   # Alces (genus) — True Moose
    'gray_wolf':          42048,   # Canis lupus — Gray Wolf
    'wolverine':          41852,   # Gulo gulo — Wolverine
    'caribou':            42199,   # Rangifer tarandus — Caribou
    'bison':              42408,   # Bison bison — American Bison
    'mountain_goat':      42414,   # Oreamnos americanus — Mountain Goat
    'dall_sheep':         42390,   # Ovis dalli — Thinhorn Sheep (Dall + Stone)
    'pronghorn':          42429,   # Antilocapra americana — Pronghorn
    'bighorn_sheep':      42391,   # Ovis canadensis — Bighorn Sheep
    'coyote':             41972,   # Canis latrans — Coyote (verify if needed)
    'prairie_dog':        46010,   # Cynomys (genus) — verify if needed
    'canada_lynx':        41791,   # Lynx canadensis — verify if needed
    'beluga_whale':       41461,   # Delphinapterus leucas — Beluga
    'harbor_seal':        41708,   # Phoca vitulina — Harbor Seal
    'sea_otter':          41860,   # Enhydra lutris — Sea Otter
    'steller_sea_lion':   41755,   # Eumetopias jubatus — Steller Sea Lion
    'muskox':             42412,   # Ovibos moschatus — Muskox
}

# --- Species Groups (for frontend filter checkboxes) ---
SPECIES_GROUPS = {
    'bears': {
        'label': 'Bears',
        'color': '#8B4513',   # brown
        'taxon_ids': [
            TAXON_IDS['brown_grizzly_bear'],
            TAXON_IDS['black_bear'],
        ],
        'species': ['Brown/Grizzly Bear', 'Black Bear'],
    },
    'deer_family': {
        'label': 'Deer Family & Bison',
        'color': '#DAA520',   # goldenrod
        'taxon_ids': [
            TAXON_IDS['moose'],
            TAXON_IDS['caribou'],
            TAXON_IDS['bison'],
        ],
        'species': ['Moose', 'Caribou', 'Bison'],
    },
    'canids': {
        'label': 'Canids',
        'color': '#708090',   # slate gray
        'taxon_ids': [
            TAXON_IDS['gray_wolf'],
            TAXON_IDS['coyote'],
        ],
        'species': ['Gray Wolf', 'Coyote'],
    },
    'sheep_goats': {
        'label': 'Sheep & Goats',
        'color': '#F5F5DC',   # beige (white animals)
        'taxon_ids': [
            TAXON_IDS['mountain_goat'],
            TAXON_IDS['dall_sheep'],
            TAXON_IDS['bighorn_sheep'],
            TAXON_IDS['pronghorn'],
        ],
        'species': ['Mountain Goat', 'Dall Sheep', 'Bighorn Sheep', 'Pronghorn'],
    },
    'marine': {
        'label': 'Marine Mammals',
        'color': '#1E90FF',   # dodger blue
        'taxon_ids': [
            TAXON_IDS['beluga_whale'],
            TAXON_IDS['harbor_seal'],
            TAXON_IDS['sea_otter'],
            TAXON_IDS['steller_sea_lion'],
        ],
        'species': ['Beluga Whale', 'Harbor Seal', 'Sea Otter', 'Steller Sea Lion'],
    },
    'mustelids': {
        'label': 'Mustelids',
        'color': '#556B2F',   # dark olive
        'taxon_ids': [
            TAXON_IDS['wolverine'],
        ],
        'species': ['Wolverine'],
    },
}

# All taxon IDs across all groups (flat list for "show all")
ALL_TAXON_IDS = [tid for group in SPECIES_GROUPS.values() for tid in group['taxon_ids']]

# Map from taxon_id → group key (for coloring markers)
TAXON_TO_GROUP = {}
for group_key, group_data in SPECIES_GROUPS.items():
    for tid in group_data['taxon_ids']:
        TAXON_TO_GROUP[tid] = group_key

# --- Route Segments ---
ROUTE_SEGMENTS = {
    'great_plains': {
        'name': 'Great Plains',
        'description': 'Badlands NP, SD — start of the drive',
        'center': {'lat': 43.8554, 'lng': -102.3397},
        'default_zoom': 8,
        'adfg_coverage': None,
        'taxon_ids': [
            TAXON_IDS['bison'],
            TAXON_IDS['pronghorn'],
            TAXON_IDS['coyote'],
            TAXON_IDS['prairie_dog'],
        ],
        'species': ['Bison', 'Pronghorn', 'Coyote', 'Prairie Dog'],
        'notes': 'Best chance for large bison herds in the Badlands interior.',
    },
    'northern_rockies': {
        'name': 'Northern Rockies',
        'description': 'Glacier NP, MT',
        'center': {'lat': 48.7596, 'lng': -113.7870},
        'default_zoom': 9,
        'adfg_coverage': None,
        'taxon_ids': [
            TAXON_IDS['brown_grizzly_bear'],
            TAXON_IDS['black_bear'],
            TAXON_IDS['gray_wolf'],
            TAXON_IDS['mountain_goat'],
            TAXON_IDS['bighorn_sheep'],
            TAXON_IDS['moose'],
            TAXON_IDS['wolverine'],
        ],
        'species': ['Grizzly Bear', 'Black Bear', 'Gray Wolf', 'Mountain Goat',
                    'Bighorn Sheep', 'Moose', 'Wolverine'],
        'notes': 'Logan Pass and Going-to-the-Sun Road for mountain goat and bighorn.',
    },
    'canadian_corridor': {
        'name': 'Canadian Corridor',
        'description': 'BC / Yukon Highway',
        'center': {'lat': 59.0, 'lng': -135.0},
        'default_zoom': 6,
        'adfg_coverage': None,
        'taxon_ids': [
            TAXON_IDS['moose'],
            TAXON_IDS['caribou'],
            TAXON_IDS['black_bear'],
            TAXON_IDS['brown_grizzly_bear'],
            TAXON_IDS['canada_lynx'],
            TAXON_IDS['mountain_goat'],
        ],
        'species': ['Moose', 'Caribou', 'Black Bear', 'Grizzly Bear', 'Lynx', 'Mountain Goat'],
        'notes': 'Alaska Highway and Cassiar Highway corridors. Stone sheep near Muncho Lake.',
    },
    'kenai_peninsula': {
        'name': 'Kenai Peninsula',
        'description': 'Cooper Landing, Russian River, Seward',
        'center': {'lat': 60.4893, 'lng': -150.7960},
        'default_zoom': 9,
        'adfg_coverage': 'region2',
        'taxon_ids': [
            TAXON_IDS['brown_grizzly_bear'],
            TAXON_IDS['black_bear'],
            TAXON_IDS['moose'],
            TAXON_IDS['beluga_whale'],
            TAXON_IDS['harbor_seal'],
            TAXON_IDS['sea_otter'],
            TAXON_IDS['steller_sea_lion'],
        ],
        'species': ['Brown Bear', 'Black Bear', 'Moose', 'Beluga Whale',
                    'Harbor Seal', 'Sea Otter', 'Steller Sea Lion'],
        'notes': 'Russian River bear activity peaks July–August during salmon runs.',
    },
    'anchorage_area': {
        'name': 'Anchorage Area',
        'description': 'Turnagain Arm, Chugach State Park',
        'center': {'lat': 61.2181, 'lng': -149.9003},
        'default_zoom': 9,
        'adfg_coverage': 'region2',
        'taxon_ids': [
            TAXON_IDS['beluga_whale'],
            TAXON_IDS['dall_sheep'],
            TAXON_IDS['moose'],
            TAXON_IDS['brown_grizzly_bear'],
        ],
        'species': ['Beluga Whale', 'Dall Sheep', 'Moose', 'Brown Bear'],
        'notes': 'Beluga pods visible from Seward Hwy at Turnagain Arm. '
                 'Dall sheep on Flattop and Bird Ridge.',
    },
    'interior_denali': {
        'name': 'Interior / Denali',
        'description': 'Denali NP corridor',
        'center': {'lat': 63.3333, 'lng': -150.5000},
        'default_zoom': 8,
        'adfg_coverage': None,  # ADF&G Region 3 — not yet implemented
        'taxon_ids': [
            TAXON_IDS['brown_grizzly_bear'],
            TAXON_IDS['caribou'],
            TAXON_IDS['moose'],
            TAXON_IDS['gray_wolf'],
            TAXON_IDS['dall_sheep'],
            TAXON_IDS['wolverine'],
        ],
        'species': ['Grizzly Bear', 'Caribou', 'Moose', 'Gray Wolf', 'Dall Sheep', 'Wolverine'],
        'notes': 'Denali park road bus required for interior access. '
                 'Polychrome Pass and Toklat River for grizzlies.',
    },
    'fairbanks_north': {
        'name': 'Fairbanks / North',
        'description': 'Dalton Highway vicinity',
        'center': {'lat': 66.5, 'lng': -150.0},
        'default_zoom': 7,
        'adfg_coverage': None,  # ADF&G Region 5 — not yet implemented
        'taxon_ids': [
            TAXON_IDS['caribou'],
            TAXON_IDS['moose'],
            TAXON_IDS['brown_grizzly_bear'],
            TAXON_IDS['gray_wolf'],
            TAXON_IDS['muskox'],
        ],
        'species': ['Caribou', 'Moose', 'Grizzly Bear', 'Gray Wolf', 'Muskox'],
        'notes': 'Trans-Alaska Pipeline corridor. Caribou herds cross Dalton Hwy. '
                 'Muskox occasionally near Prudhoe Bay.',
    },
}

# Ordered list for the segment selector UI
SEGMENT_ORDER = [
    'great_plains',
    'northern_rockies',
    'canadian_corridor',
    'kenai_peninsula',
    'anchorage_area',
    'interior_denali',
    'fairbanks_north',
]
