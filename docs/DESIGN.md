# Megafauna Tracker — Design Notes

Detailed design specs for planned/complex backlog items. The backlog keeps a one-line summary
and links here. Shipped features are recorded in `CHANGELOG.md`.

---

## Heatmap — trend visualization
_Backlog: 🔴 High_

Toggle overlay showing whether sightings are increasing or decreasing at each location over the
last 30 days.

**Library:** `leaflet.heat` (CDN `unpkg.com/leaflet.heat@0.2.0`) — takes `[lat, lng, intensity]`
arrays, overlays directly on the Leaflet map.

**Implementation:**
- Add a "Heatmap" toggle button to the controls bar.
- On activate: fetch 30 days of observations for the current location (reuse `/sightings?days=30`),
  hide dot markers, render the heat layer.
- Split the 30-day window into two 15-day halves; count observations per ~1 km grid cell
  (lat/lng rounded to 2 decimals) in each half.
- Map intensity to trend: `0.0` strongly decreasing · `0.5` stable · `1.0` strongly increasing.
- Gradient: blue (`#4363d8`) → white (`#ffffff`) → red (`#e41a1c`).
- Legend: 🔴 Increasing · ⚪ Stable · 🔵 Decreasing (days 1–15 vs 16–30).
- Respect active group/drill-down filters; reset heatmap state when location changes.
- Observation field names: `lat` / `lng` / `observed_on` (iNaturalist format — different from
  bird-tracker's `latitude` / `longitude` / `timestamp`).

**Data-density caveat (key difference from bird-tracker):** iNaturalist megafauna sightings are
far sparser than eBird data. In low-density areas a 30-day window may have too few observations
per grid cell for a meaningful trend. Mitigations:
- Use a coarser grid (1 decimal ≈ 11 km) if fewer than ~50 total observations are returned.
- If total observations < 20, show a "Not enough data for trend view — showing density only"
  notice and render a plain density heatmap (intensity = normalized total count).
- Consider a 90/180-day window option for the heatmap specifically (iNaturalist supports up to
  365 days, unlike eBird's 30-day cap).
