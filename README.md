# Alaska Megafauna Tracker

Real-time wildlife sighting tracker for a Cincinnati → Alaska road trip. Shows research-grade observations from iNaturalist on an interactive map, filtered by species group, search radius, and time window.

## Overview

The app covers the full drive corridor — Badlands (SD), Glacier NP (MT), the Canadian Highway, and several Alaska zones — letting you check recent sightings before and during a leg of the trip.

**Data source:** [iNaturalist API v1](https://api.inaturalist.org/v1/docs/) — no authentication required, research-grade observations only.

**Phase 2 (planned):** ADF&G salmon weir counts + Claude AI bear activity forecast.

---

## Stack

| Layer | Technology |
|---|---|
| Backend | Python / Flask 3 + Jinja2 |
| Frontend | Bootstrap 5 (dark theme) + Leaflet.js |
| Map tiles | OpenStreetMap |
| Data | iNaturalist API v1 |
| Cache | JSON file cache (`.cache/` directory) |
| AI (Phase 2) | Anthropic Claude API (`claude-sonnet-4`) |
| Deployment | Gunicorn + Render |

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
│   ├── adfg_fishcounts.py  # ADF&G salmon weir counts (Phase 2 stub)
│   ├── adfg_reports.py     # ADF&G report scraper (Phase 2 stub)
│   └── forums.py           # Alaska Outdoors Forums scraper (Phase 3 stub)
├── ai/
│   └── summarizer.py       # Claude-powered bear forecast + report summarizer
├── templates/
│   ├── base.html
│   └── index.html          # Main UI: map + feed sidebar + controls
└── static/
    └── css/style.css
```

---

## Species Groups

| Group | Species | Color |
|---|---|---|
| Bears | Brown/Grizzly Bear, Black Bear | Brown |
| Deer Family & Bison | Moose, Caribou, Bison | Goldenrod |
| Canids | Gray Wolf, Coyote | Slate gray |
| Sheep & Goats | Mountain Goat, Dall Sheep, Bighorn Sheep, Pronghorn | Beige |
| Marine Mammals | Beluga Whale, Harbor Seal, Sea Otter, Steller Sea Lion | Blue |
| Mustelids | Wolverine | Dark olive |

All taxon IDs verified against the iNaturalist API (March 2026). See `species_config.py` for the full list.

---

## Route Segments

| Segment | Location | Notable Species |
|---|---|---|
| Great Plains | Badlands NP, SD | Bison, Pronghorn, Coyote, Prairie Dog |
| Northern Rockies | Glacier NP, MT | Grizzly, Mountain Goat, Bighorn Sheep, Wolf |
| Canadian Corridor | BC / Yukon Highway | Moose, Caribou, Grizzly, Lynx |
| Kenai Peninsula | Cooper Landing / Seward | Brown Bear, Marine Mammals |
| Anchorage Area | Turnagain Arm / Chugach SP | Beluga Whale, Dall Sheep, Moose |
| Interior / Denali | Denali NP | Grizzly, Caribou, Wolf, Dall Sheep |
| Fairbanks / North | Dalton Highway | Caribou, Muskox, Wolf |

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Main UI |
| `GET` | `/sightings` | iNaturalist observations near a point |
| `GET` | `/species` | Priority species list by route segment |
| `GET` | `/salmon-count` | ADF&G weir count + bear forecast (Phase 2) |
| `GET` | `/local-conditions` | ADF&G report summary (Phase 2) |
| `GET` | `/health` | Render health check |

**`/sightings` parameters:**

| Param | Type | Default | Description |
|---|---|---|---|
| `lat` | float | required | Latitude |
| `lng` | float | required | Longitude |
| `radius` | int | 25 | Search radius in miles (10 / 25 / 50 / 100) |
| `days` | int | 365 | Days back to search (30 / 60 / 180 / 365) |
| `groups` | string (repeatable) | all | Species group keys, e.g. `groups=bears&groups=canids` |

Responses are cached for 1 hour in `.cache/`.

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
web: gunicorn wsgi:app
```

Set `ANTHROPIC_API_KEY` as an environment variable in the Render dashboard. No database required — all state is either fetched live or cached in `.cache/`.

---

## Roadmap

### Phase 1 — Complete
- iNaturalist live feed with research-grade filtering
- Leaflet map with color-coded species markers
- Species group checkboxes, radius + time-window selectors
- Route segment selector with map centering
- Geolocation ("My Location") button
- JSON file cache (1-hour TTL for sightings)
- Render deployment config

### Phase 2 — Planned
- ADF&G salmon weir count scraper (Russian River, Kenai, etc.)
- Claude AI bear activity forecast based on weir counts
- ADF&G report scraper + Claude summarization
- Conditions card in sidebar (currently shows Phase 2 placeholder)

### Phase 3 — Planned
- Alaska Outdoors Forums scraper for local trip reports
- Chatbot interface for natural-language queries
- Mobile layout polish
