# Alaska Megafauna Tracker — Project Outline
*For Claude Code / development reference*

---

## 1. Project Summary

A real-time wildlife sighting tracker for large mammals encountered during the full road trip from Cincinnati to Alaska (and return), covering Badlands, Glacier NP, the Canadian corridor, and all major Alaska zones. Primary use case is a **live sighting feed while traveling**. Standalone app, separate from Bird Tracker, but mirroring its stack for maintainability.

---

## 2. Route Segments & Target Species

| Segment | Key Locations | Priority Megafauna |
|---|---|---|
| **Great Plains** | Badlands NP, SD | Bison, pronghorn, coyote, prairie dog |
| **Northern Rockies** | Glacier NP, MT | Grizzly, black bear, wolf, mountain goat, bighorn sheep, moose, wolverine |
| **Canadian Corridor** | BC / Yukon Hwy | Moose, caribou, black bear, grizzly, lynx, mountain goat |
| **Kenai Peninsula** | Cooper Landing, Russian River, Seward | Brown bear, black bear, moose, beluga, harbor seal, sea otter, Steller sea lion |
| **Anchorage Area** | Turnagain Arm, Chugach | Beluga, Dall sheep, moose, brown bear |
| **Interior / Denali** | Denali NP corridor | Grizzly, caribou, moose, wolf, Dall sheep, wolverine |
| **Fairbanks / North** | Dalton Hwy vicinity | Caribou, moose, grizzly, wolf, muskox |

---

## 3. Data Sources

### 3a. iNaturalist API — backbone
- Base URL: `https://api.inaturalist.org/v1/observations`
- No auth needed for reads
- Key params: `taxon_id`, `lat/lng/radius`, `d1/d2` (rolling 30-day), `quality_grade=research`, `per_page=200`
- Rate limit: ~1 req/sec, ~10k/day — well within needs
- Use `taxon_id` (not `taxon_name`) for precision. Key IDs to hardcode:

| Species | taxon_id |
|---|---|
| Brown/grizzly bear | 41688 |
| Black bear | 41694 |
| Moose | 41823 |
| Gray wolf | 42048 |
| Wolverine | 41663 |
| Caribou | 61948 |
| Bison | 43365 |
| Mountain goat | 42415 |
| Dall sheep | 42416 |
| Pronghorn | 42471 |

> **Note:** Verify all taxon_ids against the iNaturalist API before hardcoding — taxonomy reorganizations do occur. Use `https://api.inaturalist.org/v1/taxa?q=<name>` to confirm.

### 3b. ADF&G Salmon Weir Counts — bear activity proxy
- URL: `https://www.adfg.alaska.gov/sf/FishCounts/`
- Access: HTML scrape (BeautifulSoup — page is not JS-rendered)
- Scope: Russian River Sockeye (Early + Late Run), Kenai Late-Run Sockeye
- Logic: Daily weir counts posted June–September. Bear density at Russian River correlates predictably with salmon run intensity. Pass count + escapement goal to Claude → 2-sentence bear forecast.
- Cache: 24 hours
- **Pre-build check:** Fetch page manually first to confirm HTML structure before writing scraper

### 3c. ADF&G Weekly Fishing/Wildlife Reports — qualitative conditions
- URL: `https://www.adfg.alaska.gov/sf/FishingReports/index.cfm?ADFG=R2.Home`
- Access: HTML scrape
- Value: Narrative reports frequently include bear closures, trail restrictions, notable sightings — context iNaturalist doesn't capture
- Pass raw text to Claude → extract structured JSON: `{alerts: [], sightings: [], conditions_summary: ""}`
- Cache: 12 hours

### 3d. Alaska Outdoors Forums — optional/fragile
- URL: `https://forums.outdoorsdirectory.com`
- Most timely real-time human reports for Russian River specifically
- Implement with graceful degradation — if scrape fails, suppress silently
- Scope to keyword search: "Russian River" + "bear" in recent posts

---

## 4. Backend Architecture

```
megafauna-tracker/
├── app.py                      # Flask app, route definitions
├── sources/
│   ├── inaturalist.py          # iNaturalist API client
│   ├── adfg_fishcounts.py      # Weir count scraper
│   ├── adfg_reports.py         # Fishing report scraper
│   └── forums.py               # Optional forum scraper (graceful degradation)
├── ai/
│   └── summarizer.py           # Claude API calls
├── cache.py                    # JSON file cache (Redis later if needed)
├── species_config.py           # Taxon IDs, route segments, species metadata
├── requirements.txt
└── Procfile                    # Render deployment
```

### API Endpoints

| Endpoint | Description |
|---|---|
| `GET /sightings?lat=&lng=&radius=&days=` | iNaturalist observations near location |
| `GET /salmon-count` | Weir count + AI bear proxy interpretation |
| `GET /local-conditions` | Scraped + summarized ADF&G report |
| `GET /species?segment=` | Priority species list for route segment |
| `GET /health` | Render health check |

---

## 5. Frontend / UX

Three-panel layout:

1. **Map panel** (Leaflet.js): Sighting dots color-coded by species group. Click → species, date, observer, photo thumbnail, iNaturalist record link. Geolocation auto-center on current position.
2. **Live feed panel**: Reverse-chronological sightings list within selected radius — species icon, common name, date, distance from current location.
3. **Conditions card**: AI-generated summary of bear activity level, salmon run status, ADF&G alerts. Refreshed every 12 hours. Shows "last updated X hours ago" prominently.

### Controls
- Radius slider: 10 / 25 / 50 / 100 miles
- Days slider: 7 / 14 / 30 / 60 days
- Species filter checkboxes by group (bears, deer family, canids, marine mammals)
- Route segment selector for pre-trip planning by zone

---

## 6. AI Integration (Claude API)

Three distinct tasks:

1. **Bear forecast**: Given current weir count + historical escapement goal → 2-sentence bear activity prediction for Russian River. Prompt should include species context and current date/season.

2. **Report summarization**: Raw ADF&G HTML text → structured JSON:
   ```json
   {
     "alerts": [],
     "sightings": [],
     "conditions_summary": ""
   }
   ```

3. **Chatbot (Phase 2)**: Conversational interface, same pattern as Bird Tracker chatbot. Context window includes recent sightings data and conditions summary. Example queries: *"What bears have been seen within 20 miles in the last 2 weeks?"* / *"Is the Russian River trail open today?"*

---

## 7. Tech Stack

Mirrors Bird Tracker for maintainability:

| Component | Technology |
|---|---|
| Backend | Python 3.11+, Flask |
| Scraping | BeautifulSoup4, requests |
| Mapping | Leaflet.js (frontend only) |
| AI | Anthropic Claude API (claude-sonnet) |
| Caching | JSON file cache (upgrade to Redis if needed) |
| Hosting | Render (free tier to start) |

### Required Environment Variables
```
ANTHROPIC_API_KEY=
```
iNaturalist read API is open (no key needed). ADF&G data is scraped.

---

## 8. Build Phases

### Phase 1 — MVP
- iNaturalist sighting feed with Leaflet map
- Radius / days / species group filters
- Hardcoded route segments with species context
- Render deployment

### Phase 2 — Data Enrichment
- ADF&G weir count scraper + bear proxy conditions card
- ADF&G report scraper + Claude summarization
- Conditions card surfaced in UI

### Phase 3 — Polish
- Chatbot interface (Bird Tracker pattern)
- Alaska Outdoors Forums scraper (optional, graceful degradation)
- Mobile-responsive layout (critical — primary use is in-vehicle on phone/tablet)
- Geolocation auto-center

---

## 9. Key Design Constraints

- **Mobile-first**: App used primarily on phone/tablet while traveling. Touch targets, readable fonts, minimal chrome.
- **Cache aggressively**: Spotty Alaska connectivity is real. Show data freshness indicator ("last updated X hours ago") on all panels.
- **Use taxon_id not taxon_name**: Avoids ambiguous iNaturalist matches due to taxonomy synonyms.
- **Research-grade only** in main feed; casual-grade sightings optional as a secondary map layer.
- **Graceful degradation**: App must function on iNaturalist data alone if ADF&G scrapers or forum scraper fail. Suppress failed source cards silently rather than showing errors.
- **No authentication required**: Keep frictionless for field use.
