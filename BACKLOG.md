# Megafauna Tracker — Project Backlog

Items are not ranked by priority. Status: `[ ]` open · `[x]` done · `[-]` in progress.

---

## UX & Mobile

- [ ] **iPhone-first layout overhaul** — audit and align UI with Bird Tracker conventions; ensure touch targets, font sizes, and panel layout work well on iPhone; map and feed should be usable one-handed while in a vehicle
- [ ] **Time-dependence visualization** — show whether sightings are trending up or down over the selected time window; visually distinguish recent vs. older observations (e.g., marker opacity or color gradient by age; mini sparkline or bar chart in the sidebar)
- [ ] **Geolocation auto-center** — auto-pan map to user's current GPS position on load (already wired up via "My Location" button; make it more prominent or trigger automatically on mobile)

---

## Data & Sources

- [x] **Source visibility and selection** — show which data sources are active in the UI; allow user to toggle sources on/off (iNaturalist, ADF&G fish counts, ADF&G reports, Forums); display freshness per source
- [ ] **Expand to all of North America** — remove the Alaska/road-trip framing as the primary scope; make the app useful anywhere in North America; revisit species list, route segments, and default map center accordingly
- [ ] **ADF&G salmon weir count scraper** — scrape Russian River Sockeye (early + late run) and Kenai Late-Run Sockeye from `adfg.alaska.gov/sf/FishCounts/`; cache 24h; stub exists in `sources/adfg_fishcounts.py`
- [x] **ADF&G weekly fishing/wildlife report scraper** — scrape narrative reports from ADF&G Region 2; pass to Claude for structured extraction (`alerts`, `sightings`, `conditions_summary`); cache 12h
- [ ] **Alaska Outdoors Forums scraper** — scrape recent posts from `forums.outdoorsdirectory.com` filtered to "Russian River" + "bear"; graceful degradation if scrape fails; stub exists in `sources/forums.py`

---

## AI Features

- [ ] **AI Analysis page** — dedicated page (mirroring Bird Tracker's AI page) with: Claude-generated summary of current observations in the selected area; trend analysis (species activity up/down, notable patterns); conversational interface to query the data (e.g., "What bears have been seen within 20 miles in the last 2 weeks?", "Is activity higher than usual for this time of year?")
- [ ] **Bear activity forecast** — use ADF&G weir count + current date/season as context for a Claude-generated 2-sentence bear activity prediction; surface in the Conditions card (currently shows Phase 2 placeholder)
- [x] **Conditions card — activate** — wire up the Conditions card in the sidebar to display live ADF&G + AI output once scrapers and summarizer are implemented

---

## Infrastructure

- [x] **Deploy to Render** — live at https://megafauna-tracker.onrender.com; free tier spins down after 15min inactivity (~30s cold start)

---

## Completed

- [x] iNaturalist live feed with research-grade filtering
- [x] Leaflet map with color-coded species group markers
- [x] Species group checkboxes, radius + time-window selectors (10/25/50/100 mi · 30/60/180/365 days)
- [x] Route segment selector with map centering
- [x] Geolocation "My Location" button
- [x] JSON file cache (1-hour TTL for sightings)
- [x] AI summarizer scaffold (`ai/summarizer.py`) with `bear_forecast()`, `summarize_report()`, `chat()` methods
- [x] Render deployment config (Procfile + wsgi.py)
- [x] README
