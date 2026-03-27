"""
Species configuration for Megafauna Tracker — North America.
Taxon IDs sourced from iNaturalist — verify with:
  https://api.inaturalist.org/v1/taxa?q=<name>
"""

# --- Taxon IDs ---
TAXON_IDS = {
    # Bears
    'brown_grizzly_bear':      41641,   # Ursus arctos
    'black_bear':              41638,   # Ursus americanus
    'polar_bear':              41671,   # Ursus maritimus

    # Deer Family
    'moose':                   42196,   # Alces (genus)
    'elk':                     42160,   # Cervus canadensis
    'caribou':                 42199,   # Rangifer tarandus
    'bison':                   42408,   # Bison bison
    'pronghorn':               42429,   # Antilocapra americana
    'white_tailed_deer':       42219,   # Odocoileus virginianus
    'mule_deer':               42157,   # Odocoileus hemionus
    'muskox':                  42412,   # Ovibos moschatus

    # Wild Cats
    'mountain_lion':           41975,   # Puma concolor
    'bobcat':                  41790,   # Lynx rufus
    'canada_lynx':             41791,   # Lynx canadensis
    'jaguar':                  41963,   # Panthera onca
    'ocelot':                  41961,   # Leopardus pardalis

    # Canids
    'gray_wolf':               42048,   # Canis lupus
    'coyote':                  41972,   # Canis latrans
    'red_fox':                 42053,   # Vulpes vulpes
    'arctic_fox':              41878,   # Vulpes lagopus

    # Marine Mammals
    'humpback_whale':          43697,   # Megaptera novaeangliae
    'gray_whale':              41483,   # Eschrichtius robustus
    'orca':                    41424,   # Orcinus orca
    'beluga_whale':            41461,   # Delphinapterus leucas
    'harbor_seal':             41708,   # Phoca vitulina
    'steller_sea_lion':        41755,   # Eumetopias jubatus
    'california_sea_lion':     41756,   # Zalophus californianus
    'northern_elephant_seal':  41734,   # Mirounga angustirostris
    'sea_otter':               41860,   # Enhydra lutris
    'manatee':                 44343,   # Trichechus manatus
    'walrus':                  41714,   # Odobenus rosmarus

    # Other Megafauna
    'wolverine':               41852,   # Gulo gulo
    'mountain_goat':           42414,   # Oreamnos americanus
    'dall_sheep':              42390,   # Ovis dalli (Thinhorn Sheep)
    'bighorn_sheep':           42391,   # Ovis canadensis
    'american_alligator':      26175,   # Alligator mississippiensis
    'javelina':                42464,   # Pecari tajacu (Collared Peccary)
    'american_badger':         41859,   # Taxidea taxus
    'prairie_dog':             46010,   # Cynomys (genus)
}

# --- Species Groups ---
# Each group has a 'members' list of {label, taxon_id} dicts.
# taxon_ids and species are derived from members for backward compatibility.
SPECIES_GROUPS = {
    'bears': {
        'label': 'Bears',
        'color': '#8B4513',   # group color (used in all-groups mode)
        'members': [
            {'label': 'Brown/Grizzly Bear', 'taxon_id': TAXON_IDS['brown_grizzly_bear'], 'color': '#8B4513'},
            {'label': 'Black Bear',         'taxon_id': TAXON_IDS['black_bear'],          'color': '#2C2C2C'},
            {'label': 'Polar Bear',         'taxon_id': TAXON_IDS['polar_bear'],          'color': '#89CFF0'},
        ],
    },
    'deer_family': {
        'label': 'Deer Family',
        'color': '#DAA520',
        'members': [
            {'label': 'Moose',             'taxon_id': TAXON_IDS['moose'],             'color': '#3B1F00'},
            {'label': 'Elk',               'taxon_id': TAXON_IDS['elk'],               'color': '#8B4513'},
            {'label': 'Caribou',           'taxon_id': TAXON_IDS['caribou'],           'color': '#DAA520'},
            {'label': 'Bison',             'taxon_id': TAXON_IDS['bison'],             'color': '#5C3D00'},
            {'label': 'Pronghorn',         'taxon_id': TAXON_IDS['pronghorn'],         'color': '#C8902A'},
            {'label': 'White-tailed Deer', 'taxon_id': TAXON_IDS['white_tailed_deer'], 'color': '#D2B48C'},
            {'label': 'Mule Deer',         'taxon_id': TAXON_IDS['mule_deer'],         'color': '#A0785A'},
            {'label': 'Muskox',            'taxon_id': TAXON_IDS['muskox'],            'color': '#4A3728'},
        ],
    },
    'wild_cats': {
        'label': 'Wild Cats',
        'color': '#FF8C00',
        'members': [
            {'label': 'Mountain Lion', 'taxon_id': TAXON_IDS['mountain_lion'], 'color': '#FF8C00'},
            {'label': 'Bobcat',        'taxon_id': TAXON_IDS['bobcat'],        'color': '#D2691E'},
            {'label': 'Canada Lynx',   'taxon_id': TAXON_IDS['canada_lynx'],   'color': '#FFD700'},
            {'label': 'Jaguar',        'taxon_id': TAXON_IDS['jaguar'],        'color': '#8B0000'},
            {'label': 'Ocelot',        'taxon_id': TAXON_IDS['ocelot'],        'color': '#C8A000'},
        ],
    },
    'canids': {
        'label': 'Canids',
        'color': '#708090',
        'members': [
            {'label': 'Gray Wolf',  'taxon_id': TAXON_IDS['gray_wolf'],  'color': '#708090'},
            {'label': 'Coyote',     'taxon_id': TAXON_IDS['coyote'],     'color': '#A0856C'},
            {'label': 'Red Fox',    'taxon_id': TAXON_IDS['red_fox'],     'color': '#CC3300'},
            {'label': 'Arctic Fox', 'taxon_id': TAXON_IDS['arctic_fox'], 'color': '#C8DCF0'},
        ],
    },
    'marine': {
        'label': 'Marine Mammals',
        'color': '#1E90FF',
        'members': [
            {'label': 'Humpback Whale',        'taxon_id': TAXON_IDS['humpback_whale'],        'color': '#1E90FF'},
            {'label': 'Gray Whale',             'taxon_id': TAXON_IDS['gray_whale'],            'color': '#778899'},
            {'label': 'Orca',                   'taxon_id': TAXON_IDS['orca'],                  'color': '#101010'},
            {'label': 'Beluga Whale',           'taxon_id': TAXON_IDS['beluga_whale'],          'color': '#B0D8F0'},
            {'label': 'Harbor Seal',            'taxon_id': TAXON_IDS['harbor_seal'],           'color': '#6B8E5A'},
            {'label': 'Steller Sea Lion',       'taxon_id': TAXON_IDS['steller_sea_lion'],      'color': '#CD853F'},
            {'label': 'California Sea Lion',    'taxon_id': TAXON_IDS['california_sea_lion'],   'color': '#B8860B'},
            {'label': 'N. Elephant Seal',       'taxon_id': TAXON_IDS['northern_elephant_seal'],'color': '#607080'},
            {'label': 'Sea Otter',              'taxon_id': TAXON_IDS['sea_otter'],             'color': '#8B6914'},
            {'label': 'Manatee',                'taxon_id': TAXON_IDS['manatee'],               'color': '#7B9E9E'},
            {'label': 'Walrus',                 'taxon_id': TAXON_IDS['walrus'],                'color': '#A0522D'},
        ],
    },
    'other': {
        'label': 'Other',
        'color': '#556B2F',
        'members': [
            {'label': 'Wolverine',          'taxon_id': TAXON_IDS['wolverine'],          'color': '#556B2F'},
            {'label': 'Mountain Goat',      'taxon_id': TAXON_IDS['mountain_goat'],      'color': '#D8D8C0'},
            {'label': 'Dall Sheep',         'taxon_id': TAXON_IDS['dall_sheep'],         'color': '#F5F5DC'},
            {'label': 'Bighorn Sheep',      'taxon_id': TAXON_IDS['bighorn_sheep'],      'color': '#C2A868'},
            {'label': 'American Alligator', 'taxon_id': TAXON_IDS['american_alligator'], 'color': '#2D5A1B'},
            {'label': 'Javelina',           'taxon_id': TAXON_IDS['javelina'],           'color': '#696969'},
            {'label': 'American Badger',    'taxon_id': TAXON_IDS['american_badger'],    'color': '#8B7355'},
            {'label': 'Prairie Dog',        'taxon_id': TAXON_IDS['prairie_dog'],        'color': '#C68642'},
        ],
    },
}

# Derive taxon_ids and species lists from members (used by backend)
for _group in SPECIES_GROUPS.values():
    _group['taxon_ids'] = [m['taxon_id'] for m in _group['members']]
    _group['species'] = [m['label'] for m in _group['members']]

# All taxon IDs across all groups
ALL_TAXON_IDS = [tid for group in SPECIES_GROUPS.values() for tid in group['taxon_ids']]

# Map from taxon_id → group key (for coloring markers)
TAXON_TO_GROUP = {}
for group_key, group_data in SPECIES_GROUPS.items():
    for tid in group_data['taxon_ids']:
        TAXON_TO_GROUP[tid] = group_key

# --- Route Segments (Quick Picks) ---
ROUTE_SEGMENTS = {
    'great_plains': {
        'name': 'Great Plains',
        'description': 'Badlands NP, SD',
        'center': {'lat': 43.8554, 'lng': -102.3397},
        'default_zoom': 8,
        'adfg_coverage': None,
        'taxon_ids': [
            TAXON_IDS['bison'],
            TAXON_IDS['pronghorn'],
            TAXON_IDS['coyote'],
            TAXON_IDS['prairie_dog'],
            TAXON_IDS['white_tailed_deer'],
            TAXON_IDS['elk'],
        ],
        'species': ['Bison', 'Pronghorn', 'Coyote', 'Prairie Dog', 'White-tailed Deer', 'Elk'],
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
            TAXON_IDS['elk'],
            TAXON_IDS['wolverine'],
            TAXON_IDS['mountain_lion'],
        ],
        'species': ['Grizzly Bear', 'Black Bear', 'Gray Wolf', 'Mountain Goat',
                    'Bighorn Sheep', 'Moose', 'Elk', 'Wolverine', 'Mountain Lion'],
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
            TAXON_IDS['gray_wolf'],
        ],
        'species': ['Moose', 'Caribou', 'Black Bear', 'Grizzly Bear', 'Lynx',
                    'Mountain Goat', 'Gray Wolf'],
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
            TAXON_IDS['orca'],
        ],
        'species': ['Brown Bear', 'Black Bear', 'Moose', 'Beluga Whale',
                    'Harbor Seal', 'Sea Otter', 'Steller Sea Lion', 'Orca'],
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
            TAXON_IDS['arctic_fox'],
            TAXON_IDS['polar_bear'],
        ],
        'species': ['Caribou', 'Moose', 'Grizzly Bear', 'Gray Wolf', 'Muskox',
                    'Arctic Fox', 'Polar Bear'],
        'notes': 'Trans-Alaska Pipeline corridor. Caribou herds cross Dalton Hwy. '
                 'Muskox occasionally near Prudhoe Bay.',
    },
    'yellowstone': {
        'name': 'Yellowstone',
        'description': 'Yellowstone & Grand Teton NPs, WY',
        'center': {'lat': 44.4280, 'lng': -110.5885},
        'default_zoom': 8,
        'adfg_coverage': None,
        'taxon_ids': [
            TAXON_IDS['bison'],
            TAXON_IDS['elk'],
            TAXON_IDS['brown_grizzly_bear'],
            TAXON_IDS['gray_wolf'],
            TAXON_IDS['pronghorn'],
            TAXON_IDS['moose'],
            TAXON_IDS['bighorn_sheep'],
            TAXON_IDS['mountain_lion'],
        ],
        'species': ['Bison', 'Elk', 'Grizzly Bear', 'Gray Wolf', 'Pronghorn',
                    'Moose', 'Bighorn Sheep', 'Mountain Lion'],
        'notes': 'Lamar Valley for wolves; Hayden Valley for bison and bears.',
    },
    'pacific_coast': {
        'name': 'Pacific Coast',
        'description': 'CA / OR / WA coastline',
        'center': {'lat': 38.0, 'lng': -123.0},
        'default_zoom': 7,
        'adfg_coverage': None,
        'taxon_ids': [
            TAXON_IDS['gray_whale'],
            TAXON_IDS['humpback_whale'],
            TAXON_IDS['orca'],
            TAXON_IDS['northern_elephant_seal'],
            TAXON_IDS['california_sea_lion'],
            TAXON_IDS['harbor_seal'],
            TAXON_IDS['sea_otter'],
            TAXON_IDS['mountain_lion'],
        ],
        'species': ['Gray Whale', 'Humpback Whale', 'Orca', 'Northern Elephant Seal',
                    'California Sea Lion', 'Harbor Seal', 'Sea Otter', 'Mountain Lion'],
        'notes': 'Gray whale migration Feb–May. Elephant seals at Año Nuevo and Piedras Blancas.',
    },
    'gulf_coast': {
        'name': 'Gulf Coast / Southeast',
        'description': 'FL, GA, LA coastline',
        'center': {'lat': 29.5, 'lng': -83.0},
        'default_zoom': 7,
        'adfg_coverage': None,
        'taxon_ids': [
            TAXON_IDS['american_alligator'],
            TAXON_IDS['manatee'],
            TAXON_IDS['black_bear'],
            TAXON_IDS['white_tailed_deer'],
            TAXON_IDS['bobcat'],
            TAXON_IDS['mountain_lion'],
        ],
        'species': ['American Alligator', 'Manatee', 'Black Bear', 'White-tailed Deer',
                    'Bobcat', 'Florida Panther (Mountain Lion)'],
        'notes': 'Everglades and Big Cypress for alligators. '
                 'Crystal River for manatees Nov–Mar.',
    },
    'southwest': {
        'name': 'Desert Southwest',
        'description': 'AZ, NM, TX border region',
        'center': {'lat': 31.5, 'lng': -110.0},
        'default_zoom': 7,
        'adfg_coverage': None,
        'taxon_ids': [
            TAXON_IDS['mountain_lion'],
            TAXON_IDS['javelina'],
            TAXON_IDS['ocelot'],
            TAXON_IDS['jaguar'],
            TAXON_IDS['bobcat'],
            TAXON_IDS['coyote'],
            TAXON_IDS['mule_deer'],
            TAXON_IDS['bighorn_sheep'],
        ],
        'species': ['Mountain Lion', 'Javelina', 'Ocelot', 'Jaguar', 'Bobcat',
                    'Coyote', 'Mule Deer', 'Bighorn Sheep'],
        'notes': 'Sky Islands for jaguar and ocelot. Big Bend for unusual border species.',
    },
}

# Ordered list for the segment selector UI
SEGMENT_ORDER = [
    'yellowstone',
    'great_plains',
    'northern_rockies',
    'pacific_coast',
    'gulf_coast',
    'southwest',
    'canadian_corridor',
    'kenai_peninsula',
    'anchorage_area',
    'interior_denali',
    'fairbanks_north',
]
