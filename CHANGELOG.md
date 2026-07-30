# Changelog

All notable changes to Megafauna Tracker are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/);
this project adheres to [Semantic Versioning](https://semver.org/) per `VERSIONING.md`.

## [0.6.2] – 2026-07-30
### Fixed
- AI errors no longer fail silently. `/api/analyze` and `/api/chat` previously swallowed API failures (invalid key, rate limit, timeout) and returned `200` with empty content, so the UI showed nothing. They now return `502` with the actual error message, and `/api/chat` returns `503` when no key is configured. The summarizer's `analyze_observations`/`chat` methods raise instead of returning `None`/a fallback string.

## [0.6.1] – 2026-07-30
### Fixed
- AI Analysis no longer times out on Render. Gunicorn ran with the default 30 s worker timeout, which SIGKILL'd the worker mid-request during the Claude briefing call. Set `--timeout 120` and switched to a threaded worker (`gthread`, 4 threads) so a slow AI request completes and doesn't block other requests.

## [0.6.0] – 2026-07-11
### Added
- **TripPlanner wildlife-report provider** — `POST /api/wildlife-report` implements the shared Wildlife Report Provider Contract v1.1, so Megafauna sightings appear as a section in TripPlanner's Daily Digest.
  - Bearer-token auth (timing-safe, `MEGAFAUNA_API_TOKEN`); returns `503` until configured, `401` on bad/missing token, `400` on malformed request.
  - Maps the request onto the iNaturalist client (`radius_mi` default 50, clamped to ~200 km; `recency_days` window) and transforms observations into the contract's `items[]` shape, most-recent-first, capped at `max_items`.
  - Responses cached 12h keyed on lat/lng/radius/recency (not `target_date`); null coordinates return a `200` empty section.
  - New `wildlife_report.py` module; `MEGAFAUNA_API_TOKEN` added to `.env.example`.

## [0.5.5] – 2026-06-07
### Added
- Marker clustering toggle (Cluster / Uncluster button in the filters bar).
  - Groups nearby markers into `L.markerClusterGroup` bubbles; clicking zooms in, spiderifies at max zoom.
  - Cluster icons are neutral gray in all-groups mode; switch to the active group's color in species drill-down.
  - Icon size scales with count: 30 px (< 10) · 38 px (< 100) · 46 px (100+).
  - Mutually exclusive with Heatmap in both directions — activating one silently deactivates the other.
  - Markers land at true coordinates in cluster mode (jitter bypassed).
- `VERSION` file at project root; `app.py` now reads the version from it instead of a hardcoded string.

## [0.5.4] – 2026-04-05
### Added
- ADF&G context in the AI Analysis briefing.
### Changed
- Heatmap polish and Conditions card UX refinements.
- New bear-paw + location-pin favicon.

## [0.5.3] – 2026-03-28
### Added
- iPhone-first mobile layout: bottom navigation, collapsible controls bar, full-height map with safe-area padding.
- Heatmap feature with selectable time window.
- 10 additional species (dolphins, fur seals, blue whale, gray fox).
### Fixed
- Verified all taxon IDs against the iNaturalist API; deterministic marker jitter to separate stacked observations.

## [0.5.2] – 2026-03-27
### Added
- AI Analysis page — wildlife briefing plus multi-turn chat.
- Species drill-down with per-species colors and a dynamic legend.
- Fullscreen map toggle for mobile.

## [0.4.0] – 2026-03-26
### Added
- iNaturalist quality-grade selector.
- Total-available count, segment filtering, and load-more.
- Auto-reload on filter changes.

## [0.3.0] – 2026-03-25
### Added
- Initial release as "Megafauna Tracker": Alaska wildlife MVP via iNaturalist with map, species config, Conditions card, and bear-paw app icon.
