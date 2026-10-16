# Replay viewer

`scripts/replay_run.py` replays a reconstructed run in CARLA 0.9.15.  It shows the **reconstruction**, not the
simulator state: recorder vehicles are CARLA actors moved along their own recorded poses, reconstructed road users
are boxes.  Ground truth is not used.

## Launch

```bat
conda activate carla
:: either your own CARLA 0.9.15 on port 2000, or the project's server on port 3000 (Ctrl-C stops it)
python scripts\start_carla.py

:: menu of the 22 canonical runs (pick a number; close the window to come back; q quits)
python scripts\review_canonical_runs.py --port 3000
:: the same menu on a server already running on port 2000
scripts\review_canonical_runs.bat

:: one run directly
python scripts\replay_run.py traces\S04\run_0_a_front_pushed --port 3000
python scripts\replay_run.py traces\S14\run_0_surrounded --port 3000 --start 5 --speed 0.25 --follow B --focus
```

Useful options: `--start T` (seconds), `--speed X` (default 0.5), `--paused`, `--camera overview|follow|free`,
`--follow ID`, `--focus`, `--hide-tracks`, `--res 1280x720`.  Without a server, `--export DIR` draws top-down
frames of the reconstruction (`--at T`, `--format png|svg|pdf`).

## Controls

| key | action |
|---|---|
| SPACE | play / pause |
| LEFT / RIGHT | seek 0.5 s (SHIFT: 0.05 s) |
| N / P | next / previous reconstructed event |
| 1-4 | speed 0.25 / 0.5 / 1 / 2x |
| C | camera: overview, follow each recorder in turn, free |
| TAB | select the next recorder (its panel is the full one) |
| F | focus: the selected recorder's panel takes the right-hand column (F again: normal layout) |
| PgUp / PgDn | older / newer events of the selected recorder |
| T | radar tracks on / off |
| G | ghost boxes or dots for unfused tracks |
| H | help |
| R | restart |
| ESC | quit |
| free camera | W/A/S/D/Q/E move (SHIFT faster), mouse drag to look, wheel to zoom |

## Reading the screen

- **Upper left**: the run, its time on the global clock, the replay state, the camera, the last and next event.
- **Right column**: one panel per recorder, showing what that recorder perceives and does.
  - *Current state*: its own (`ego: MOVING, BRAKE, INDICATOR_LEFT`), then one line per local track with an active
    state, named after the fusion's identity (`track_001 (B): CLOSING, CRITICAL_TTC`), then anonymous tracks and
    road users.  At most 8 lines; its own state and alerts first.
  - *Recent events*, newest first, with their age (`-0.4 s  EGO_PATH_ENTRY → C (by own lateral motion)`); the
    recorder's own COLLISION events in red.  The selected recorder shows up to 15 (PgUp / PgDn scroll through all),
    the others the 3 latest.
- **Scene**: a letter badge above each recorder; reconstructed road users as boxes (`U1`, `U2`, ...); a coloured
  line joins a recorder to a vehicle it holds CRITICAL_TTC or CUT_IN about and to the nearest vehicle in its path,
  labelled with their body-to-body clearance (`1.4 m`); a red banner names the pairs of a collision.
- **Bottom**: the timeline with the events (click to seek) and the key help.

UNKNOWN states and the measured / predicted provenance are not drawn; they remain in the reconstruction files.
