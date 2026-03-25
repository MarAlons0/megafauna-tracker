# Megafauna Tracker

Real-time megafauna sighting tracker for North America. Shows research-grade wildlife observations from iNaturalist on an interactive map, filtered by species group, search radius, and time window. Live at **https://megafauna-tracker.onrender.com**

## Overview

The app covers the full Cincinnati → Alaska drive corridor — Badlands (SD), Glacier NP (MT), the Canadian Highway, and Alaska zones — and is being expanded to all of North America.

**Primary data source:** [iNaturalist API v1](https://api.inaturalist.org/v1/docs/) — no authentication required, research-grade observations only.

**Conditions data:** ADF&G Region 2 fishing/wildlife reports scraped and summarized by Claude AI; displayed in the Conditions card.

---

## Stack

| Layer | Technology |
|---|---|
| Backend | Python / Flask 3 + Jinja2 |
| Frontend | Bootstrap 5 (dark theme) + Leaflet.js |
| Map tiles | OpenStreetMap |
| Data | iNaturalist API v1 + ADF&G report scraper |
| Cache | JSON file cache (`.cache/` directory) |
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
| `GET` | `/salmon-count` | ADF&G weir count + bear forecast (seasonal stub) |
| `GET` | `/local-conditions` | ADF&G Region 2 report + Claude summary (live) |
| `GET` | `/sources` | Status and cache age for all data sources |
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
web: gunicorn wsgi:app --bind 0.0.0.0:$PORT
```

Set `ANTHROPIC_API_KEY` as an environment variable in the Render dashboard. No database required — all state is either fetched live or cached in `.cache/`. Note: Render's free tier has ephemeral storage, so the cache resets on each restart.

---

## Roadmap

### v0.3 — Current
- iNaturalist live feed with research-grade filtering
- Leaflet map with color-coded species markers
- Species group checkboxes, radius + time-window selectors
- Route segment selector with map centering
- Geolocation ("My Location") button
- Source visibility panel with status pills and toggle
- ADF&G Region 2 report scraper + Claude AI summarization
- Live Conditions card (alerts, sightings, AI summary)
- Deployed to Render (https://megafauna-tracker.onrender.com)
- Bear paw favicon + version badge in navbar

### Planned
- Time-dependence visualization (sighting trends, marker age)
- AI Analysis page with Claude chat interface
- iPhone-first layout overhaul
- North America expansion (beyond Alaska route)
- ADF&G salmon weir count scraper (seasonal — Jun–Sep)
- ADF&G salmon weir count + Claude bear activity forecast
