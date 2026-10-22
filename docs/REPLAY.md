# Replay viewers

There are two independent viewers.  They use the same window, keys, options, cameras and speeds, and run on the
same CARLA 0.9.15 server.

| | GROUND TRUTH viewer | RECONSTRUCTION viewer |
|---|---|---|
| script | `scripts/view_ground_truth.py` | `scripts/replay_run.py` |
| reads | `<run>/ground_truth/` only (privileged) | the recorders' own files and `<run>/reconstruction/` only |
| shows | every vehicle on its true trajectory, the physical contact episodes (COLLISION banner, CONTACT_START / END) | recorders at the pose the reconstruction used, fused road users U1, U2, ... as boxes, radar tracks, associations, collisions and semantic events |
| clock | `t_contact`: seconds from the first true vehicle-vehicle contact | `t_global`: the reconstruction's clock, 0 at its reference collision |

In all 22 canonical runs the reconstruction aligns the recorders on the first collision, so `t_contact` and
`t_global` are the same instant: `--start T` / `--at T` show the same moment in both viewers.  The recorders'
pose in the RECONSTRUCTION viewer is never the simulator's:
* in G0 it is the recorded synthetic GNSS/INS stream;
* after a perturbation or a pose refinement it is `reconstruction/global/recorder_poses.json`
  (`docs/SENSORS_AND_GROUND_TRUTH.md`).

The review menu (`scripts/review_canonical_runs.py`) opens the GROUND TRUTH viewer of the chosen run first.  When
its window closes, the RECONSTRUCTION viewer of the same run opens.  `Ng` opens only the ground truth of run N, and
`Nr` only its reconstruction.

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
python scripts\view_ground_truth.py traces\S04\run_0_a_front_pushed --port 3000
python scripts\replay_run.py traces\S04\run_0_a_front_pushed --port 3000
python scripts\replay_run.py traces\S14\run_0_surrounded --port 3000 --start 5 --speed 0.25 --follow B --focus

:: without a server: top-down frames of both viewers at the same instants
python scripts\view_ground_truth.py traces\S10\run_0_deflected_into_c --export out\gt --at -1 --at 0 --at 1
python scripts\replay_run.py traces\S10\run_0_deflected_into_c --export out\rec --at -1 --at 0 --at 1
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
