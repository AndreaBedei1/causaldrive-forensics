# Replay viewers

There are two independent viewers.  They use the same window, keys, options, cameras and speeds, and run each on a
CARLA 0.9.15 server.

| | GROUND TRUTH viewer | RECONSTRUCTION viewer |
|---|---|---|
| script | `scripts/view_ground_truth.py` | `scripts/replay_run.py` |
| reads | `<run>/ground_truth/` only (privileged) | the recorders' own files and `<run>/reconstruction/` only |
| shows | every vehicle on its true trajectory, the physical collisions (COLLISION banner, CONTACT_START / END; a recontact of the same pair, the bodies never more than 1 m apart within 2 s, is RECONTACT_START / END of that collision) | recorders at the pose the reconstruction used, fused road users U1, U2, ... as boxes, radar tracks, associations, collisions (a recontact labelled RECONTACT, by the same rule on the recorders' own poses) and semantic events |
| clock shown | `t_contact`: seconds from the first true vehicle-vehicle contact | `t_global`: the reconstruction's clock, 0 at its reference collision |

**Recorder poses.**  The recorders' pose in the RECONSTRUCTION viewer is never the simulator's:
* in G0 it is the recorded synthetic GNSS/INS stream;
* after a perturbation or a pose refinement it is `reconstruction/global/recorder_poses.json`
  (`docs/SENSORS_AND_GROUND_TRUTH.md`).

## Both viewers side by side, synchronised

The review menu opens the two viewers of a run at the same time, each on its own CARLA server, so they never
share or disturb a simulation.
* **Either window drives both.**  Play, pause, seek (keys, N / P, a click on the timeline), speed and restart act on
  both windows, whichever one has the keyboard.  So does the camera: C, TAB while following, mouse drag and wheel,
  the free camera.  ESC, or closing either window, closes both.  Panels and overlays (F, T, G, H, PgUp / PgDn) stay
  each window's own.
* **Leader and follower.**  The GROUND TRUTH window (left) keeps the clock; the RECONSTRUCTION window (right)
  follows it.  A clock action in the follower's window goes to the leader as a numbered command, and the follower
  keeps its own clock until the leader has applied it, so a pause or a seek never jumps back.
* **What crosses.**  Two local UDP ports (`--sync-lead PORT` sends on PORT and listens on PORT + 1, `--sync-follow
  PORT` the other way round; `cdf.replay.sync`).  They carry the instant shown on the recording clock, the play state,
  the speed, the camera and the quit.  The recording clock is the recorders' own clock, which in the canonical runs
  is the simulator's.  No position, no event and no identity crosses, except the name of a recorder both viewers
  replay (the followed vehicle).  Side by side, the camera of both viewers moves over the recorders: the GROUND TRUTH
  viewer still draws the vehicles that record nothing, but its overview frames the recorders and C follows only
  them, as in the RECONSTRUCTION viewer.
* **The follower's mapping.**  The RECONSTRUCTION viewer maps the instant through its own alignment and the
  recorders' timestamps, so it never reads ground truth.
* **The two clocks.**  The labels stay each viewer's own clock.  `t_global` = 0 is the reconstruction's strongest
  matched contact; in 21 of the 22 runs it is also the first true contact, so `t_contact` and `t_global` read the
  same.  In S04 `b_rear_first` the strongest contact (A-B) comes 1.55 s after the first one (B-C).  At the same
  instant the GROUND TRUTH window then shows `t_contact` 1.55 s more than the RECONSTRUCTION window's `t_global`.
  The menu prints this offset when it opens a single viewer of that run.

## Launch

```bat
conda activate carla
:: two CARLA 0.9.15 servers, one per viewer (each in its own terminal; Ctrl-C stops it)
python scripts\start_carla.py --carla-root F:\Carla9_15\WindowsNoEditor --port 3000
python scripts\start_carla.py --carla-root F:\Carla9_15\WindowsNoEditor --port 3100

:: menu of the 22 canonical runs: N = both viewers side by side and synchronised, Ng / Nr = one of them, q = quit
python scripts\review_canonical_runs.py --port 3000 --gt-port 3100 --res 960x540 --speed 0.5

:: with one server only: N opens the GROUND TRUTH viewer, then the RECONSTRUCTION viewer when its window closes
python scripts\review_canonical_runs.py --port 3000

:: one run directly
python scripts\view_ground_truth.py traces\S04\run_0_a_front_pushed --port 3100
python scripts\replay_run.py traces\S04\run_0_a_front_pushed --port 3000
python scripts\replay_run.py traces\S14\run_0_surrounded --port 3000 --start 5 --speed 0.25 --follow B --focus

:: without a server: top-down frames of both viewers at the same displayed times
python scripts\view_ground_truth.py traces\S10\run_0_deflected_into_c --export out\gt --at -1 --at 0 --at 1
python scripts\replay_run.py traces\S10\run_0_deflected_into_c --export out\rec --at -1 --at 0 --at 1
```

Useful options: `--start T` (seconds), `--speed X` (default 0.5), `--paused`, `--camera overview|follow|free`,
`--follow ID`, `--focus`, `--hide-tracks`, `--res 1280x720`, `--sync-lead PORT` / `--sync-follow PORT` (what the
menu passes), `--map NAME`.  Without a server, `--export DIR` draws top-down frames (`--at T`, `--format png|svg|pdf`).

**Map.**  The RECONSTRUCTION viewer loads the road map named by the run's supplied incident context
(`incident_context.json`: `map`, the incident location, read as the reconstruction reads it: Town05, Town03_Opt for
S07, Town04 for S19), never the map the server happens to have loaded; switching between runs on different maps
reloads the server's world.  A run recorded before its incident context named the map falls back on the map whose
driving lanes carry the recorded positions, else `--map`.  The GROUND TRUTH viewer loads the acquisition map of its
own `ground_truth/metadata.json`.

## Controls

| key | action |
|---|---|
| SPACE | play / pause |
| LEFT / RIGHT | seek 0.5 s (SHIFT: 0.05 s) |
| N / P | next / previous event (reconstructed, or true contact in the GROUND TRUTH viewer) |
| 1-4 | speed 0.25 / 0.5 / 1 / 2x |
| C | camera: overview, follow each recorder in turn, free |
| TAB | select the next recorder (its panel is the full one) |
| F | focus: the selected recorder's panel takes the right-hand column (F again: normal layout) |
| PgUp / PgDn | older / newer events of the selected recorder |
| T | radar tracks on / off |
| G | ghost boxes or dots for unfused tracks |
| H | help |
| R | restart |
| ESC | quit (side by side: both viewers) |
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
