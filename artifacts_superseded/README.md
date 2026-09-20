# Superseded recordings

Runs kept out of every active campaign root because the scenario definitions
that produced them were wrong, not because the recordings are old.

## `pre_s16_rebuild/`

S10 to S16, seeds 0 1 2, recorded before the scenario corrections of September
2026. Every one of them is a recording of a scenario that was not doing what it
said: vehicles that never reached the junction they were named for, a lane shift
the controller silently ignored because the parameter had the wrong name, a
"pushed" vehicle that reached the car in front under its own throttle, a
deflection that was an unconditional timed lane change, and routes short enough
that a vehicle outran them and circled into the scenery.

They are kept so that the corrections can be compared against what they replaced,
and for no other purpose. They are not evidence, no current figure is computed
from them, and nothing in `docs/` or `results/` quotes them. The replacements
live in `artifacts_v2/`.
