# Megafauna Tracker — agent guide

Real-time North American wildlife dashboard via the iNaturalist API, with a Leaflet map, heatmap,
and a Claude-powered conditions card. Flask, deployed on Render. `app.py` reads the version from
the `VERSION` file.

## Project standards (read these before related work)
This repo follows shared standards documented at its root:
- **VERSIONING.md** — when shipping a feature, bump `VERSION`, add a `CHANGELOG.md` entry (Keep a Changelog), and tag per SemVer.
- **BACKLOG_FORMAT.md** — keep `BACKLOG.md` in the standard format (priority sections, checkbox status, type tags, ✅ Shipped). Long design specs go in `docs/` (see `docs/DESIGN.md`).
- **FAVICON.md** — favicon kit + root serving + Safari rules.

These three docs are synced from the `project-dashboard` repo (the source of truth) — don't edit
them here; change the master there and run its `sync-standards.sh`.
