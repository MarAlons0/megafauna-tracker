# Megafauna Tracker

Real-time megafauna sighting tracker for North America. Shows wildlife observations from iNaturalist on an interactive map, filterable by species group, search radius, and time window. Live at **https://megafauna-tracker.onrender.com**

## Overview

Search any location in North America by name, or pick a Quick Pick (Yellowstone, Glacier NP, Kenai Peninsula, etc.) to instantly center the map. Observations are fetched live from iNaturalist and displayed as color-coded markers. A Conditions card shows ADF&G weekly fishing/wildlife reports summarized by Claude AI for Alaska segments.

**Primary data source:** [iNaturalist API v1](https://api.inaturalist.org/v1/docs/) — no authentication required; supports research-grade, unconfirmed, and all observation grades.

**Conditions data:** ADF&G Region 2 fishing/wildlife reports scraped and summarized by Claude AI; displayed in the Conditions card for Kenai Peninsula and Anchorage Area segments.

---

## Stack

| Layer | Technology |
|---|---|
| Backend | Python / Flask 3 + Jinja2 |
| Frontend | Bootstrap 5 (dark theme) + Leaflet.js |
| Map tiles | OpenStreetMap |
| Geocoding | Nominatim (via `/geocode` proxy) |
| Data | iNaturalist API v1 + ADF&G report scraper |
| Cache | JSON file cache (`.cache/` directory, 1h TTL) |
| AI | Anthropic Claude API (`claude-sonnet-4-6`) |
| Deployment | Gunicorn + Render (https://megafauna-tracker.onrender.com) |

---

## Project Structure

```
megafauna-tracker/
├── app.py                  # Flask app factory + routes
├── wsgi.py                 # Gunicorn entry point
├── species_config.py       # Taxon IDs, species groups, route segments
├── cache.py                # JSON file cache with TTL
├── requirements.txt
├── Procfile                # web: gunicorn wsgi:app
├── .env                    # ANTHROPIC_API_KEY (not committed)
├── sources/
│   ├── inaturalist.py      # iNaturalist API client
│   ├── adfg_fishcounts.py  # ADF&G salmon weir counts (stub — seasonal, Jun–Sep)
│   ├── adfg_reports.py     # ADF&G Region 2 report scraper (live)
│   └── forums.py           # Alaska Outdoors Forums scraper (stub)
├── ai/
│   └── summarizer.py       # Claude-powered report summarizer + bear forecast
├── templates/
│   ├── base.html
│   └── index.html          # Main UI: map + feed sidebar + controls
└── static/
    ├── favicon.png          # Bear paw app icon
    └── css/style.css
```

---

## Species Groups

Six top-level groups, each with distinct species colors visible in drill-down mode.

| Group | Species |
|---|---|
| Bears | Brown/Grizzly Bear · Black Bear · Polar Bear |
| Deer Family | Moose · Elk · Caribou · Bison · Pronghorn · White-tailed Deer · Mule Deer · Muskox |
| Wild Cats | Mountain Lion · Bobcat · Canada Lynx · Jaguar · Ocelot |
| Canids | Gray Wolf · Coyote · Red Fox · Arctic Fox |
| Marine Mammals | Humpback Whale · Gray Whale · Orca · Beluga · Harbor Seal · Steller Sea Lion · California Sea Lion · N. Elephant Seal · Sea Otter · Manatee · Walrus |
| Other | Wolverine · Mountain Goat · Dall Sheep · Bighorn Sheep · American Alligator · Javelina · American Badger · Prairie Dog |

**Drill-down:** Click any group label in the filter bar to switch to per-species checkboxes. Each species gets a unique color on the map and legend. Click "← All groups" to return.

All taxon IDs sourced from the iNaturalist API. See `species_config.py` for the full list.

---

## Quick Picks

| Segment | Location | Notable Species |
|---|---|---|
| Yellowstone | Yellowstone & Grand Teton NPs, WY | Bison, Elk, Grizzly, Wolf |
| Great Plains | Badlands NP, SD | Bison, Pronghorn, Prairie Dog |
| Northern Rockies | Glacier NP, MT | Grizzly, Mountain Goat, Wolf |
| Pacific Coast | CA / OR / WA coastline | Gray Whale, Elephant Seal, Sea Otter |
| Gulf Coast / Southeast | FL, GA, LA | Alligator, Manatee, Black Bear |
| Desert Southwest | AZ, NM, TX border | Mountain Lion, Javelina, Jaguar |
| Canadian Corridor | BC / Yukon Highway | Moose, Caribou, Grizzly, Lynx |
| Kenai Peninsula | Cooper Landing / Seward, AK | Brown Bear, Marine Mammals |
| Anchorage Area | Turnagain Arm / Chugach SP, AK | Beluga Whale, Dall Sheep, Moose |
| Interior / Denali | Denali NP, AK | Grizzly, Caribou, Wolf, Dall Sheep |
| Fairbanks / North | Dalton Highway, AK | Caribou, Muskox, Polar Bear |

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Main UI |
| `GET` | `/sightings` | iNaturalist observations near a point |
| `GET` | `/geocode` | Nominatim geocoding proxy |
| `GET` | `/species` | Priority species list by segment |
| `GET` | `/salmon-count` | ADF&G weir count + bear forecast (stub) |
| `GET` | `/local-conditions` | ADF&G Region 2 report + Claude summary |
| `GET` | `/sources` | Status and cache age for all data sources |
| `GET` | `/health` | Render health check + version |

**`/sightings` parameters:**

| Param | Type | Default | Description |
|---|---|---|---|
| `lat` | float | required | Latitude |
| `lng` | float | required | Longitude |
| `radius` | int | 25 | Search radius in miles (10 / 25 / 50 / 100) |
| `days` | int | 365 | Days back to search (30 / 60 / 180 / 365) |
| `groups` | string (repeatable) | all | Group mode: `groups=bears&groups=canids` |
| `taxon_id` | int (repeatable) | — | Drill mode: specific taxon IDs override groups |
| `quality_grade` | string | `research` | `research` / `research,needs_id` / `any` |
| `segment` | string | — | Quick Pick key for segment-aware taxon filtering |
| `page` | int | 1 | Page number (200 results per page) |

---

## Local Development

```bash
# 1. Clone and set up environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Add API key
cp .env.example .env
# edit .env and set ANTHROPIC_API_KEY=sk-ant-...

# 3. Run
python app.py
# → http://127.0.0.1:5002
```

---

## Deployment (Render)

The app is Render-ready via `Procfile`:

```
web: gunicorn wsgi:app --bind 0.0.0.0:$PORT
```

Set `ANTHROPIC_API_KEY` as an environment variable in the Render dashboard. No database required — all state is either fetched live or cached in `.cache/`. Note: Render's free tier has ephemeral storage, so the cache resets on each restart (~30s cold start after 15 min inactivity).

---

## Roadmap

### v0.5.2 — Current
- Free-text location search (Nominatim geocoder) with autocomplete dropdown
- 6 species groups · 39 species · 11 Quick Pick segments covering all of North America
- Species drill-down: click group → per-species checkboxes with unique colors per species
- Dynamic map legend updates to show individual species in drill-down mode
- iNaturalist quality grade selector (Verified / + Unconfirmed / All)
- Sighting count transparency ("X of Y available") + Load More pagination
- Auto-reload on filter changes
- Source visibility panel with status pills
- ADF&G Region 2 report scraper + Claude AI summarization (Conditions card)
- Deployed to Render

### Planned
- iPhone-first layout overhaul
- Time-dependence visualization (sighting trends, marker age)
- AI Analysis page with Claude chat interface
- ADF&G salmon weir count scraper + Claude bear activity forecast
- Expand ADF&G Conditions card to Regions 1, 3, 5 (Southeast, Interior, Fairbanks)
- Alaska Outdoors Forums scraper
