# Changelog

All notable changes to Megafauna Tracker are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/);
this project adheres to [Semantic Versioning](https://semver.org/) per `VERSIONING.md`.

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
