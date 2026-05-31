# Megafauna Tracker — Project Backlog

Items are not ranked by priority. Status: `[ ]` open · `[x]` done · `[-]` in progress.

---

## UX & Mobile — Map

- [ ] **Heatmap — trend visualization** — toggle overlay on the map showing whether sightings are increasing or decreasing at each location over the last 30 days.

  **Library:** `leaflet.heat` (CDN `unpkg.com/leaflet.heat@0.2.0`) — takes `[lat, lng, intensity]` arrays, overlays directly on the Leaflet map.

  **Implementation:**
  - Add a "Heatmap" toggle button to the controls bar
  - When activated: fetch 30 days of observations for the current location (re-use `/sightings?days=30`), hide dot markers, render heat layer
  - Split the 30-day window into two 15-day halves; count observations per ~1km grid cell (`lat/lng` rounded to 2 decimal places) in each half
  - Map intensity to trend: `0.0` = strongly decreasing · `0.5` = stable · `1.0` = strongly increasing
  - Gradient: blue (`#4363d8`) → white (`#ffffff`) → red (`#e41a1c`)
  - Legend updates to: 🔴 Increasing · ⚪ Stable · 🔵 Decreasing (days 1–15 vs 16–30)
  - Heatmap respects active group/drill-down filters
  - Reset heatmap state (clear cached observations, remove layer) when location changes
  - Observation field names: `lat` / `lng` / `observed_on` (iNaturalist format — different from bird-tracker's `latitude` / `longitude` / `timestamp`)

  **Data density caveat (key difference from bird-tracker):** iNaturalist megafauna sightings are far sparser than eBird data. In low-density areas a 30-day window may have too few observations per grid cell for trend comparison to be meaningful. Mitigations:
  - Use a coarser grid (1 decimal place ≈ 11km) as a fallback if fewer than ~50 total observations are returned
  - If total observations < 20, show a "Not enough data for trend view — showing density only" notice and render a plain density heatmap (intensity = total count, normalized) rather than a trend heatmap
  - Consider offering a 90-day or 180-day window option for the heatmap specifically, since iNaturalist supports up to 365 days (unlike eBird's 30-day cap)

- [x] **Marker clustering** — Cluster toggle button groups nearby markers into `L.markerClusterGroup` bubbles; cluster icons are neutral gray in all-groups mode, switch to active group color in drill-down; size scales with count (30/38/46 px); mutually exclusive with Heatmap in both directions; Uncluster returns to jittered dot view.

- [ ] **iPhone-first layout overhaul** — audit and align UI with Bird Tracker conventions; ensure touch targets, font sizes, and panel layout work well on iPhone; map and feed should be usable one-handed while in a vehicle
- [ ] **Time-dependence visualization** — visually distinguish recent vs. older observations (e.g., marker opacity or color gradient by age; mini sparkline or bar chart in the sidebar). Note: the heatmap item above covers trend direction; this is about per-marker age encoding on the dot view.
- [ ] **Geolocation auto-center** — auto-pan map to user's current GPS position on load (already wired up via "My Location" button; make it more prominent or trigger automatically on mobile)

---

## Data & Sources

- [x] **iNaturalist quality grade selector** — Verified only / + Unconfirmed / All grades toggle; status bar notes when unconfirmed observations are included
- [x] **Sighting count transparency + pagination** — status bar shows "X of Y available"; segment-aware taxon filtering; Load More button appends next page
- [x] **Auto-reload on filter changes** — species checkboxes, radius, days, and quality grade trigger reload automatically when a location is set
- [x] **Source visibility and selection** — show which data sources are active in the UI; allow user to toggle sources on/off; display freshness per source
- [x] **Expand to all of North America** — free-text location search (Nominatim geocoder via `/geocode` proxy); 6-group species hierarchy (Bears, Deer Family, Wild Cats, Canids, Marine Mammals, Other); 39 species total; 11 Quick Pick segments including Yellowstone, Pacific Coast, Gulf Coast, Desert Southwest; default map centered on North America
- [ ] **ADF&G salmon weir count scraper** — scrape Russian River Sockeye (early + late run) and Kenai Late-Run Sockeye from `adfg.alaska.gov/sf/FishCounts/`; cache 24h; stub exists in `sources/adfg_fishcounts.py`
- [x] **ADF&G weekly fishing/wildlife report scraper** — scrape narrative reports from ADF&G Region 2; pass to Claude for structured extraction (`alerts`, `sightings`, `conditions_summary`); cache 12h
- [ ] **Alaska Outdoors Forums scraper** — scrape recent posts from `forums.outdoorsdirectory.com` filtered to "Russian River" + "bear"; graceful degradation if scrape fails; stub exists in `sources/forums.py`

---

## AI Features

- [ ] **AI Analysis page** — dedicated page (mirroring Bird Tracker's AI page) with: Claude-generated summary of current observations in the selected area; trend analysis (species activity up/down, notable patterns); conversational interface to query the data (e.g., "What bears have been seen within 20 miles in the last 2 weeks?", "Is activity higher than usual for this time of year?")
- [ ] **Bear activity forecast** — use ADF&G weir count + current date/season as context for a Claude-generated 2-sentence bear activity prediction; surface in the Conditions card (currently shows Phase 2 placeholder)
- [x] **Conditions card — hide when no coverage** — suppress the Conditions card for route segments without ADF&G Region 2 coverage (e.g. Great Plains, Northern Rockies, Canadian Corridor); show only when selected segment is in Southcentral Alaska
- [x] **Link to README from the app** — About link in navbar pointing to GitHub README
- [ ] **Expand ADF&G coverage to additional regions** — add Region 1 (Southeast AK), Region 3 (Interior/Denali), and Region 5 (Fairbanks/North) report scrapers; same HTML structure as Region 2, different area keys; makes Conditions card location-aware for all Alaska segments
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
- [x] Bear paw favicon (PNG app icon)
- [x] App renamed to Megafauna Tracker (removed Alaska-only framing)
- [x] Version badge in navbar (v0.3); version exposed on `/health`
- [x] v0.5 — North America expansion (location search, 6 species groups, 11 Quick Picks, 39 species)
- [x] v0.5.2 — Species drill-down (click group label → per-species checkboxes; distinct color per species on markers, legend, and filter; dynamic map legend updates on mode switch)
