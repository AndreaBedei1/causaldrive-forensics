# Environment

Everything below was measured on the machine this project was developed and run
on. Where a value was chosen rather than observed, the reason is given.

## Tested configuration

| Component | Version | Note |
|---|---|---|
| OS | Windows 11 Enterprise 10.0.26200 | |
| CARLA simulator | 0.9.15 (`WindowsNoEditor` package) | server and client versions both report 0.9.15 |
| Python | 3.8.20 (conda) | see "Why Python 3.8" below |
| numpy | **1.24.3** | the version actually imported; see the note below |
| scipy | 1.10.1 | `linear_sum_assignment` for tracking and track association |
| networkx | 3.1 | graph construction, DAG checks, path queries |
| pandas | 2.0.3 | aggregate report tables |
| PyYAML | 6.0.3 | configuration |
| matplotlib | 3.7.5 | figures (Agg backend, no GUI) |
| pytest | 8.3.5 | |
| CPU | 40 logical cores | only relevant to test parallelism |
| RAM | 146 GB | the simulator never approached this |
| GPU | NVIDIA RTX 6000 Ada Generation | used only for offscreen rendering |

> **A version-reporting discrepancy worth knowing about.** In this environment
> `pip` reports `numpy 1.23.5` while `import numpy; numpy.__version__` reports
> **1.24.3**. The dist-info metadata is stale relative to what is actually on
> `sys.path`, an ordinary consequence of a conda-installed package later
> overlaid by pip. The runtime value is the one that matters and the one
> recorded above; `scripts/check_environment.py` reports the runtime value for
> exactly this reason. If you are reproducing these results, check
> `numpy.__version__` rather than `pip list`.

The `carla` Python API is deliberately **not** a hard dependency of the package.
Every module except `cdf.simulation.*` and `cdf.oracle.logger` imports and runs
without a simulator, and the whole test-suite except the `carla`-marked
integration test passes with no server present.

## Why Python 3.8 rather than 3.10

CARLA 0.9.15 ships Python API wheels for **cp37 and cp38 only**:

```
<CARLA>/PythonAPI/carla/dist/carla-0.9.15-cp37-cp37m-win_amd64.whl
<CARLA>/PythonAPI/carla/dist/carla-0.9.15-py3.7-win-amd64.egg
```

A 3.10 environment therefore cannot import the simulator API that matches this
server build. Rather than upgrade CARLA and silently change simulator
behaviour, the project targets Python 3.8, which is the newest interpreter the
shipped wheels support. All code is written to 3.8 syntax: `from __future__
import annotations` everywhere, `typing.List`/`Dict`/`Optional` rather than
builtin generics, and no `X | Y` unions.

## Installation

```bash
conda env create -f environment.yml
conda activate cdf
pip install -e .
```

Then install the CARLA API from your simulator distribution — the wheel must
match the server:

```bash
pip install "<CARLA>/PythonAPI/carla/dist/carla-0.9.15-cp38-cp38-win_amd64.whl"
```

Verify with:

```bash
python scripts/check_environment.py
```

which reports the Python version, every dependency, whether `carla` imports,
whether a server is reachable and on which map, and the detected CARLA root. A
missing simulator is reported as a **warning**, not a failure, because the whole
non-CARLA stack still works.

## Starting the simulator

```bash
CarlaUE4.exe -carla-server -quality-level=Low -RenderOffScreen -nosound
```

or let the tooling do it:

```bash
python scripts/check_environment.py --start-server
```

`cdf.simulation.carla_client.CarlaServer` uses exactly the flags above.
`CARLA_ROOT` overrides the installation path; otherwise a short list of
conventional locations is probed.

## Simulator behaviour observed on this build

These are not general CARLA facts — they are what this server build did on this
machine, and the code is shaped around them. Each one cost real debugging time,
so they are recorded rather than left to be rediscovered.

1. **Reloading the current map crashes the server.** `client.load_world(X)`
   while the server is already running map `X` killed the process. `ensure_map`
   therefore compares the current map first and switches only when it differs.

2. **A map switch returns before the world is usable.** The call succeeds and the
   next request times out. `ensure_map` polls the new world until it both reports
   the expected map and answers a settings query.

3. **A second map switch in one server process is unreliable.** One switch from
   the freshly booted default map is dependable; a later one sometimes hangs.
   `SimulatorSession` tracks whether the process has already switched and
   restarts the simulator instead of switching twice. A suite that runs nine
   scenarios on one map and one on another pays that restart exactly once.

4. **Town03 cannot be loaded at all by this tested build.** Every attempt killed
   or failed to connect to the server: from a freshly booted process and after a
   prior switch, both with `-RenderOffScreen` and windowed. The active S09
   configuration therefore uses **Town03_Opt**, which loads successfully and
   exposes the same Town03 roundabout geometry. The last completed S09 campaign
   used **Town04**; every other scenario uses **Town05**. Town04 loads in ~19 s
   and exposes 372 spawn points.

5. **The map cannot be selected from the command line.** Passing
   `/Game/Carla/Maps/Town05` as the first argument was ignored and the server
   booted its default map (`Town10HD_Opt`) regardless. Map selection always goes
   through `ensure_map`.

6. **Spawning at a settled actor's transform fails.** After a few ticks of
   physics a vehicle carries a small suspension pitch/roll, and reusing that
   transform produces `Spawn failed because of collision at spawn position`. All
   spawns are derived from lane waypoints with a small vertical offset and a
   yaw-only rotation.

7. **Synchronous mode is stable at 20 Hz.** `fixed_delta_seconds = 0.05` with
   substepping (`max_substep_delta_time = 0.01`, `max_substeps = 10`) delivered
   79 radar frames over 80 ticks in the first smoke test and 131/131 in a full
   two-vehicle scenario.

8. **A run is reproducible only on a freshly booted server.** This is the single
   most consequential finding for the experiment protocol, and it was measured
   rather than assumed.

   Running scenario S05 three times *in one server session*, with an identical
   specification and seed, gave minimum separations of

   | repeat | min separation | outcome |
   |---|---|---|
   | 1 | 6.996 m | near miss |
   | 2 | 6.687 m | near miss |
   | 3 | 6.228 m | near miss |

   — drifting monotonically, with the vehicles' final positions differing by
   about a metre. Actors are destroyed and world settings restored between runs,
   so the drift is accumulated simulator state we cannot reach through the API.

   Running the *same* specification twice, each time on a **freshly started
   server process**, reproduced the result exactly: minimum separation
   `3.453 m`, collision at `t = 3.75 s`, final pose `(108.3544, 1.0848)` on both
   occasions — and matching the value recorded earlier in the campaign on
   another fresh server.

   Note also that the drifted result and the reproducible one differ by enough to
   flip the outcome class (near miss versus collision). Server reuse is therefore
   not a small numerical nuisance; it can change what the experiment concludes.

   **Consequence:** the experiment protocol restarts the simulator process before
   every recorded run. It costs roughly 45 s per run and it is what makes the
   artifacts reproducible. Reusing one server for a whole suite is faster and
   produces results that cannot be reproduced.

9. **`CarlaUE4.exe` is a launcher, not the server.** It spawns
   `CarlaUE4-Win64-Shipping.exe` (~2.5 GB resident) and exits, so terminating the
   process handle you launched does **not** stop the simulator.

   Two consequences, the second much worse than the first:

   * the engine leaks — nine of them, about 20 GB, had accumulated by the end of
     one replay campaign;
   * the leaked engine keeps holding RPC port 2000, so every subsequent "fresh"
     server fails to bind and the client silently reconnects to the **first**
     one. A restart intended to give each run an independent simulator therefore
     gives it the shared, drifting state of finding 8 while appearing to succeed.

   `CarlaServer` now records the engine pids present before it starts one,
   identifies the pid it started, and kills that on stop — leaving an engine the
   user started themselves alone. If you manage the simulator yourself, kill the
   image name (`CarlaUE4-Win64-Shipping.exe`), not the launcher.

   Leaving an engine alone is correct and it is also what makes the trap
   possible, so **the restart is no longer assumed to have worked**. After every
   restart `CarlaServer` reads the connected world's clock: a freshly booted
   engine has been ticking for seconds, one that has served a campaign has not.
   The verdict is exposed as `CarlaServer.last_restart_verified` and recorded in
   each counterfactual report as `replay_protocol.restarts_verified_fresh`; the
   sweep driver marks the affected runs and exits non-zero, and the viewer prints
   a banner above any verdict produced that way.

   This was not hypothetical. An orphaned engine from an interrupted run held
   port 2000 for over an hour and served several sweeps whose reports claimed a
   fresh server per replay, and one of them produced a verdict that did not
   reproduce. Before a comparison that depends on independent runs, confirm
   nothing is listening:

   ```powershell
   Get-NetTCPConnection -LocalPort 2000 -State Listen
   ```


10. **A client outlives the server it was talking to, and enough of them abort
    the interpreter.** Every `carla.Client` owns a background streaming client
    that reconnects to the sensor port by itself. When the server it was bound
    to is killed, that thread does not stop; it retries, which is what the
    repeated

    ```
    INFO: streaming client: connection failed: ... destination computer refused
    ```

    lines in a campaign log are. Those threads are not harmless. With the
    clients of several dead servers alive in one process, an exception escaping
    one of them terminates the interpreter outright:

    ```
    Fatal Python error: Aborted
      File "src/cdf/simulation/world.py", line 165 in __enter__   # apply_settings
      File "src/cdf/causal/counterfactuals.py", line 364 in run_counterfactual_suite
    ```

    Measured behaviour: a counterfactual suite that restarts the simulator
    before each replay died on the **third** replay, every time, in
    `world.apply_settings()` on a server that had just come up cleanly — with no
    Python traceback, no Windows error report, and a shell exit status of 127.
    The first two replays always completed. The abort is in the native client,
    so it cannot be caught and retried in-process.

    The obvious hypothesis is that the accumulating clients are the cause, so
    `SimulatorSession.release_client()` now drops the client and forces a
    collection *before* the server is replaced -- and callers holding their own
    reference drop it first, or the session's release is not the last one and
    the C++ destructor never runs.

    **It did not fix it.** With that change in place the suite aborted again, at
    the same point, after the same two replays. The release is kept because
    leaving a client bound to a killed server is wrong regardless, but the
    accumulation hypothesis is *not* confirmed and the real cause is not
    established. What is established is the symptom and its position: an abort
    inside the native client, in `apply_settings()`, on the third simulator
    process of a suite.

    What actually gets a campaign through is therefore not a fix but a
    structure: `counterfactual.resume` reuses the replays already on disk, and
    the campaign driver retries each suite up to four times. Each attempt
    completes two more replays before dying, so a four-intervention suite
    finishes in two attempts. This is a workaround, and it is recorded as one.

    The engine kill was also narrowed from `taskkill /F /T` to `taskkill /F`:
    `/T` walks the process tree by parent pid, and the engine's recorded parent
    is the launcher, which exited long ago and whose pid Windows is free to
    reassign — so a tree kill can reach an unrelated process that happens to
    have inherited it. The kill is now verified by re-listing the engine pids
    instead of being assumed.

## Radar characteristics measured on this build

The radar conventions were measured rather than assumed, because getting either
sign wrong would silently mirror or invert the entire reconstruction. The
procedure is in `docs/EXPERIMENT_PROTOCOL.md`.

* **Range rate: negative means closing.** A receding target read `+0.709 m/s`; an
  approaching one read `-1.402 m/s`.
* **Azimuth: positive means right of boresight.** Measured medians ordered
  strictly right > centre > left (`+0.0726`, `+0.0260`, `+0.0169` rad for targets
  at `+3.56 m`, `+0.06 m`, `-3.44 m` lateral offset).
* **Output is clutter-dominated.** Roughly 145 detections per frame at
  6000 points/s, most of them road-surface reflections below the sensor plane.
* **The first frame after spawn is unreliable**, once reporting a target
  velocity of `100.66 m/s`. Plausibility filtering is mandatory, not cosmetic.

## Reproducibility

Every run records, in `manifest.json`: the scenario id, variant and seed, the
full resolved configuration and its hash, the map, the fixed time step, the
package version, the git commit, the Python and CARLA versions, the platform,
and the per-participant sensor profile and scripted action timeline. Re-running
the same command on the same commit reproduces the run.

`evidence_manifest.json` additionally records a SHA-256 digest of every artifact
file in the run directory.
