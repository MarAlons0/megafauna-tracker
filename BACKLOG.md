# Megafauna Tracker — Backlog
_Last updated: 2026-07-11_

## 🔴 High
- [ ] **AI Analysis page** — dedicated page (mirroring Bird Tracker): Claude summary of current observations, trend analysis, and a conversational query interface. `[feature]`
- [ ] **Heatmap — trend visualization** — overlay showing whether sightings are increasing/decreasing per location over 30 days. See [docs/DESIGN.md](docs/DESIGN.md#heatmap--trend-visualization). `[feature]`

## 🟡 Medium
- [ ] **Bear activity forecast** — ADF&G weir count + season as context for a Claude 2-sentence prediction in the Conditions card. `[feature]`
- [ ] **ADF&G salmon weir count scraper** — scrape Russian River + Kenai late-run sockeye; cache 24h; stub in `sources/adfg_fishcounts.py`. `[feature]`
- [ ] **Expand ADF&G coverage to more regions** — add Region 1/3/5 report scrapers (same HTML, different area keys) to make the Conditions card location-aware Alaska-wide. `[feature]`
- [ ] **iPhone-first layout overhaul** — align UI with Bird Tracker conventions; one-handed usability in a vehicle. `[chore]`

## 🟢 Low / Nice to have
- [ ] **Per-marker age encoding** — distinguish recent vs older observations (opacity/color by age, or a sidebar sparkline). `[feature]`
- [ ] **Geolocation auto-center** — auto-pan to the user's GPS on load (especially on mobile). `[chore]`
- [ ] **Alaska Outdoors Forums scraper** — scrape recent "Russian River" + "bear" posts; graceful degradation; stub in `sources/forums.py`. `[feature]`

## ✅ Shipped
- [x] **TripPlanner wildlife-report provider endpoint** — v0.6.0
- [x] **Marker clustering** — v0.5.5
- [x] **Species drill-down (per-species colors + dynamic legend)** — v0.5.2
- [x] **Expand to all of North America (location search, 6 groups, 39 species, 11 Quick Picks)** — v0.5.0
- [x] **iNaturalist quality-grade selector** — v0.4.0
- [x] **Sighting count transparency + pagination** — v0.4.0
- [x] **Auto-reload on filter changes** — v0.4.0
- [x] **ADF&G weekly report scraper + Conditions card** — Claude-structured extraction, location-aware coverage
- [x] **Source visibility / selection** — active sources shown and toggleable
- [x] **Core MVP** — iNaturalist live feed, Leaflet map, species groups, radius/time selectors, "My Location", JSON cache, Render deploy
