#!/usr/bin/env python3
"""Supervisor of the frozen robustness campaign: adaptive concurrency, resource monitoring, safe pause / resume.

    python scripts/campaign_controller.py start      start (or resume) detached; refuses a second instance
    python scripts/campaign_controller.py status     completed / failed / running / pending, resources, ETA
    python scripts/campaign_controller.py pause      stop scheduling; running jobs finish; then the controller exits
    python scripts/campaign_controller.py stop-now   stop scheduling and terminate running jobs (not recorded)
    python scripts/campaign_controller.py resume     clear the pause request and start detached again
    (Windows: scripts\\campaign.bat start|status|pause|stop-now|resume)

Operational only.  The scientific content is ``scripts/robustness.py`` of the frozen commit, used unchanged: the
same families, levels, runs (``--canonical``), job keys, seeds, adaptive seed rule (``need_more_seeds``, decided
per (family, level) on the completed results of that condition, as the driver decides it), ``run_job`` and
record format (one line per finished attempt in ``jobs.jsonl``, ``attempt`` numbered as the driver numbers it,
``--max-attempts`` 2).  Every job runs in its own Python process with single-threaded BLAS and
``CDF_ANALYSIS_FREEZE_COMMIT`` set, so the order and the number of concurrent jobs cannot change any result.

Concurrency adapts to the measured machine state (sampled every 60 s, decided every 5 min): the controller
launches a job whenever fewer than the current target run, and never stops a running job to lower it.  The
target leaves 3 logical CPUs and 10 GB of RAM free for the system and other users; it rises by at most 2 per
decision while CPU, RAM, page file and disk allow it and falls by 2 when RAM gets short, the page file grows,
the campaign's own workers get less than 75 % of a core each (oversubscription) or other users' load rises.
Pending jobs start longest first (estimated from the completed jobs), so few long jobs remain at the end.

Pause state is persistent (``<results>/control/``): a ``pause`` or ``stop-now`` request is a file the
controller polls every few seconds, so it works whether or not this chat or terminal still exists.  On a pause
the controller stops scheduling, lets the running jobs finish and record, writes ``state.json`` and exits.  On
``stop-now`` it terminates the running job processes and their children, records nothing for them (they stay
pending: interrupted, not failed), removes their scratch copies, writes the state and exits.  ``resume``
verifies the frozen commit, clean tree, code and configuration hashes and the canonical raw data against the
manifest, then continues: every complete job is skipped.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import statistics
import subprocess
import sys
import time
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "scripts")]

PYTHON = sys.executable
# The campaign's code versions: v1 = the frozen tag; v2 = the evaluation revision (docs/FROZEN_CAMPAIGN.md).  A job
# complete under v1 is complete (v2 changes no result where v1 completed); attempts count under v2 only.
V1_COMMIT = "5d7adf764f1b8c3d82e58d91f8bba309da79b7b8"
VERSION_TAG = "robustness-campaign-v2"


def _tag_commit(tag: str) -> str:
    out = subprocess.run(["git", "rev-parse", tag + "^{commit}"], cwd=str(ROOT), capture_output=True, text=True)
    if out.returncode:
        raise RuntimeError("tag {0} not found".format(tag))
    return out.stdout.strip()


try:
    FROZEN_COMMIT: Optional[str] = _tag_commit(VERSION_TAG)
except RuntimeError:  # no tag: the controller refuses to run (verify_freeze)
    FROZEN_COMMIT = None
# Overridable for a test of the controller itself in scratch folders (never for the campaign).
RESULTS = Path(os.environ.get("CDF_CAMPAIGN_RESULTS", str(ROOT / "results" / "robustness" / "frozen_campaign")))
WORK = Path(os.environ.get("CDF_CAMPAIGN_WORK", str(ROOT / "robustness" / "frozen_campaign")))
MANIFEST = ROOT / "results" / "frozen_campaign_manifest.json"
CONTROL = RESULTS / "control"
MIN_WORKERS, MAX_WORKERS = 4, 20
START_WORKERS = int(os.environ.get("CDF_CAMPAIGN_START_WORKERS", "14"))
CPU_HEADROOM, RAM_HEADROOM_GB, DISK_MIN_GB = 3.0, 10.0, 15.0
SAMPLE_S, DECIDE_S, REPORT_S, POLL_S = 60.0, 300.0, 900.0, 3.0
ENV = {"CDF_ANALYSIS_FREEZE_COMMIT": FROZEN_COMMIT or "", "OMP_NUM_THREADS": "1", "MKL_NUM_THREADS": "1",
       "OPENBLAS_NUM_THREADS": "1", "NUMEXPR_NUM_THREADS": "1"}


def now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def log(message: str) -> None:
    CONTROL.mkdir(parents=True, exist_ok=True)
    with (CONTROL / "controller.log").open("a", encoding="utf-8") as handle:
        handle.write("{0} {1}\n".format(now(), message))


def write_json(path: Path, data: Any) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=1, default=str) + "\n", encoding="utf-8")
    os.replace(str(tmp), str(path))


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:  # a line cut by a crash of the writer: ignored, the job stays pending
                pass
    return out


def job_id(key: Tuple[Any, ...]) -> str:
    return hashlib.sha1(json.dumps([str(k) for k in key]).encode("utf-8")).hexdigest()[:16]


def command() -> Optional[str]:
    path = CONTROL / "command"
    return path.read_text(encoding="utf-8").strip() if path.exists() else None


# ------------------------------------------------------------------------------------------------------------
# freeze verification
# ------------------------------------------------------------------------------------------------------------

def verify_freeze() -> Dict[str, Any]:
    """The frozen commit, a clean tracked tree, code / configuration hashes and the canonical raw data, against
    the manifest written before the campaign.  Raises on any difference."""
    from cdf.evaluation.provenance import code_hash, config_hash
    from cdf.reconstruction.config import load_config
    import freeze_manifest
    import robustness
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(ROOT), capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"], cwd=str(ROOT),
                           capture_output=True, text=True).stdout.strip()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    problems = []
    if head != FROZEN_COMMIT:
        problems.append("HEAD {0} is not the frozen commit".format(head))
    if dirty:
        problems.append("tracked files modified: " + dirty.replace("\n", "; "))
    if code_hash() != manifest["code_sha256"]:
        problems.append("code hash differs from the manifest")
    if config_hash(load_config().to_dict()) != manifest["reconstruction_config_sha256"]:
        problems.append("reconstruction configuration differs from the manifest")
    for family, entry in manifest["robustness"]["matrix"].items():
        levels = [label for label, _ in robustness.FAMILIES.get(family, ([], False))[0]]
        if levels != [lev["label"] for lev in entry["levels"]]:
            problems.append("levels of {0} differ from the manifest".format(family))
    for run, record in manifest["canonical_manifest"]["runs"].items():
        if freeze_manifest.raw_hash(ROOT / run)["sha256"] != record["sha256"]:
            problems.append("raw data of {0} changed".format(run))
    if problems:
        raise RuntimeError("freeze verification failed: " + " | ".join(problems))
    return {"commit": head, "code_sha256": manifest["code_sha256"], "config_sha256": manifest["reconstruction_config_sha256"],
            "raw_runs_verified": len(manifest["canonical_manifest"]["runs"])}


# ------------------------------------------------------------------------------------------------------------
# one job in its own process
# ------------------------------------------------------------------------------------------------------------

def run_one(job_path: Path, out_path: Path, work: str) -> int:
    import robustness
    job = json.loads(job_path.read_text(encoding="utf-8"))
    job["parameter"] = _restore_parameter(job)
    result = robustness.run_job(job, work, False)
    write_json(out_path, result)
    return 0


def _restore_parameter(job: Dict[str, Any]) -> Any:
    """The level's parameter exactly as robustness.FAMILIES defines it (JSON turns tuples into lists)."""
    import robustness
    for label, parameter in robustness.FAMILIES[job["family"]][0]:
        if label == job["level"]:
            return parameter
    raise KeyError((job["family"], job["level"]))


# ------------------------------------------------------------------------------------------------------------
# resources
# ------------------------------------------------------------------------------------------------------------

class Monitor:
    def __init__(self) -> None:
        import psutil
        self.psutil = psutil
        self.cpus = psutil.cpu_count()
        psutil.cpu_percent(None)
        self.swap0 = psutil.swap_memory().used
        self.io0 = psutil.disk_io_counters()
        self.t0 = time.monotonic()
        self.samples: List[Dict[str, Any]] = []

    def sample(self, workers: Dict[str, Any]) -> Dict[str, Any]:
        ps = self.psutil
        vm, sw = ps.virtual_memory(), ps.swap_memory()
        io, t = ps.disk_io_counters(), time.monotonic()
        dt = max(t - self.t0, 1e-6)
        busy = None
        if io is not None and self.io0 is not None and hasattr(io, "read_time"):
            busy = min(1.0, ((io.read_time - self.io0.read_time) + (io.write_time - self.io0.write_time)) / 1000.0 / dt)
        self.io0, self.t0 = io, t
        own_cpu, own_rss = 0.0, 0
        for w in workers.values():
            for p in w["procs"]:
                try:
                    own_cpu += p.cpu_percent(None)
                    own_rss += p.memory_info().rss
                except Exception:
                    pass
            try:  # children started since the last sample (none expected: one process per job)
                for child in w["proc"].children(recursive=True):
                    if child.pid not in w["pids"]:
                        w["pids"].add(child.pid)
                        w["procs"].append(child)
                        child.cpu_percent(None)
            except Exception:
                pass
        total = ps.cpu_percent(None)
        s = {"time": now(), "cpu_percent": total, "cpu_cores_used": round(total / 100.0 * self.cpus, 2),
             "own_cores": round(own_cpu / 100.0, 2), "other_cores": round(max(0.0, total / 100.0 * self.cpus - own_cpu / 100.0), 2),
             "ram_total_gb": round(vm.total / 2 ** 30, 1), "ram_available_gb": round(vm.available / 2 ** 30, 1),
             "own_rss_gb": round(own_rss / 2 ** 30, 2), "pagefile_used_gb": round(sw.used / 2 ** 30, 2),
             "pagefile_growth_gb": round((sw.used - self.swap0) / 2 ** 30, 2), "pagefile_percent": sw.percent,
             "disk_free_gb": round(shutil.disk_usage(str(ROOT)).free / 2 ** 30, 1),
             "disk_busy_fraction": None if busy is None else round(busy, 3), "running": len(workers)}
        self.samples = (self.samples + [s])[-10:]
        return s

    def others(self, own_pids: set) -> List[Dict[str, Any]]:
        """The largest CPU users that are not campaign workers (other users' workloads, where observable)."""
        rows = []
        for p in self.psutil.process_iter(["pid", "name", "cpu_times"]):
            if p.info["pid"] in own_pids or p.info["pid"] == os.getpid():
                continue
            try:
                rows.append((p.cpu_percent(None), p.info["name"]))
            except Exception:
                pass
        return [{"name": n, "cpu_percent": round(c, 1)} for c, n in sorted(rows, reverse=True)[:5] if c > 5.0]


def decide(target: int, samples: List[Dict[str, Any]], running: int, cpus: int) -> Tuple[int, str]:
    """The next concurrency target from the recent samples (module docstring)."""
    if not samples:
        return target, "no sample"
    recent = samples[-5:]
    avail = min(s["ram_available_gb"] for s in recent)
    other = statistics.median(s["other_cores"] for s in recent)
    own = statistics.median(s["own_cores"] for s in recent)
    growth = recent[-1]["pagefile_growth_gb"] - recent[0]["pagefile_growth_gb"]
    disk = recent[-1]["disk_free_gb"]
    per_worker = own / running if running else 1.0
    if disk < DISK_MIN_GB:
        return MIN_WORKERS, "disk free {0} GB below {1}".format(disk, DISK_MIN_GB)
    if avail < RAM_HEADROOM_GB:
        return max(MIN_WORKERS, target - 2), "RAM available {0} GB below {1}".format(avail, RAM_HEADROOM_GB)
    if growth > 1.0:
        return max(MIN_WORKERS, target - 2), "page file grew {0:.1f} GB".format(growth)
    if running >= target and running >= 6 and per_worker < 0.75:
        return max(MIN_WORKERS, target - 2), "workers get {0:.2f} core each (oversubscribed)".format(per_worker)
    capacity = int(cpus - CPU_HEADROOM - other)
    if capacity < target:
        return max(MIN_WORKERS, max(capacity, target - 2)), "other load {0:.1f} cores".format(other)
    ram_per_worker = max(0.5, (recent[-1]["own_rss_gb"] / running) if running else 0.5)
    if capacity >= target + 1 and avail - 2 * ram_per_worker > RAM_HEADROOM_GB + 4 and running >= target:
        return min(MAX_WORKERS, capacity, target + 2), "headroom: {0} cores free for the campaign".format(capacity - target)
    return target, "steady"


# ------------------------------------------------------------------------------------------------------------
# the supervisor
# ------------------------------------------------------------------------------------------------------------

def estimate(job: Dict[str, Any], walls: Dict[Tuple[str, ...], List[float]]) -> float:
    run = Path(job["run"]).as_posix()
    for key in ((run, job["family"], job["level"]), (run, job["family"]), (job["family"], job["level"]), (run,)):
        if key in walls:
            return statistics.median(walls[key])
    return 300.0


def supervise(args: argparse.Namespace) -> int:
    import psutil
    import robustness
    from validate_canonical import canonical_runs
    CONTROL.mkdir(parents=True, exist_ok=True)
    (CONTROL / "running").mkdir(exist_ok=True)
    lock = CONTROL / "controller.lock"
    if lock.exists():
        try:
            other = json.loads(lock.read_text(encoding="utf-8"))
            if psutil.pid_exists(other["pid"]) and "campaign_controller" in " ".join(psutil.Process(other["pid"]).cmdline()):
                print("a controller is already running (pid {0})".format(other["pid"]))
                return 1
        except Exception:
            pass
    for p in psutil.process_iter(["pid", "cmdline"]):
        cmd = " ".join(p.info["cmdline"] or [])
        rel = os.path.relpath(str(RESULTS.resolve()), str(ROOT)).replace("\\", "/")
        if "robustness.py" in cmd and rel in cmd.replace("\\", "/") and "campaign_controller" not in cmd:
            print("refusing: a robustness.py campaign process is running (pid {0})".format(p.info["pid"]))
            return 1
    write_json(lock, {"pid": os.getpid(), "started": now()})
    os.environ.update(ENV)
    try:
        freeze = verify_freeze()
    except Exception as exc:
        log("freeze verification FAILED: {0}".format(exc))
        write_json(CONTROL / "state.json", {"state": "REFUSED", "time": now(), "reason": str(exc)})
        lock.unlink()
        return 2
    log("controller started (pid {0}); freeze verified: {1}".format(os.getpid(), freeze))
    families = [f for f in args.families.split(",") if f] if args.families else list(robustness.FAMILIES)
    runs = [Path(r) for r in canonical_runs()]
    runs = [r for r in runs if (r / "reconstruction" / "global" / "global_graph.json").exists()]
    jobs_file = RESULTS / "jobs.jsonl"
    done = read_jsonl(jobs_file)
    key = robustness.job_key
    finished = {key(r) for r in done if r.get("status") == "complete"}
    attempts: Dict[Tuple[Any, ...], int] = {}
    for r in done:  # attempts of the current version only: a v1 failure (evaluation defect) is attempted again
        if (r.get("provenance") or {}).get("git_commit") == FROZEN_COMMIT:
            attempts[key(r)] = attempts.get(key(r), 0) + 1
    walls: Dict[Tuple[str, ...], List[float]] = {}

    def learn(r: Dict[str, Any]) -> None:
        run = Path(r["run"]).as_posix()
        for k in ((run, r["family"], r["level"]), (run, r["family"]), (r["family"], r["level"]), (run,)):
            walls.setdefault(k, []).append(float(r.get("wall_s") or 0.0))
    for r in done:
        learn(r)
    seeds = {(f, label): list(range(args.min_seeds)) for f in families for label, _ in robustness.FAMILIES[f][0]}
    stochastic = {f: robustness.FAMILIES[f][1] for f in families}
    # Seeds already decided before this start: re-derive them exactly as the driver does (one at a time, from the
    # completed results), so a resumed campaign makes the same decisions as an uninterrupted one.
    while True:
        grew = False
        for (f, label), ss in seeds.items():
            if not stochastic[f] or len(ss) >= args.max_seeds:
                continue
            cond = [j for run in runs for j in robustness.jobs_for(run, f, ss) if j["level"] == label]
            if all(key(j) in finished or attempts.get(key(j), 0) >= args.max_attempts for j in cond) \
                    and robustness.need_more_seeds(done, f, label):
                ss.append(len(ss))
                grew = True
        if not grew:
            break
    workers: Dict[str, Dict[str, Any]] = {}
    monitor = Monitor()
    target, reason = min(START_WORKERS, MAX_WORKERS), "start"
    last_sample = last_decide = last_report = 0.0
    completed_times: List[Tuple[float, float]] = []  # (monotonic time, wall_s) of jobs completed by this controller
    state = "RUNNING"
    log("start: {0} records, {1} complete; target {2} workers".format(len(done), len(finished), target))

    def pending_jobs() -> List[Dict[str, Any]]:
        """As robustness.main builds its pending list: every job of the seeds decided so far, not complete, with
        attempts left, and not running now; longest first."""
        unique: Dict[Tuple[Any, ...], Dict[str, Any]] = {}
        for f in families:
            union = sorted({s for (ff, _), ss in seeds.items() if ff == f for s in ss})
            for run in runs:
                for j in robustness.jobs_for(run, f, union):
                    if j["seed"] not in seeds[(f, j["level"])]:
                        continue
                    k = key(j)
                    if k in finished or attempts.get(k, 0) >= args.max_attempts or job_id(k) in workers:
                        continue
                    unique.setdefault(k, j)
        return sorted(unique.values(), key=lambda j: -estimate(j, walls))

    def launch(job: Dict[str, Any]) -> None:
        k = key(job)
        jid = job_id(k)
        job_path, out_path = CONTROL / "running" / (jid + ".job.json"), CONTROL / "running" / (jid + ".result.json")
        if out_path.exists():
            out_path.unlink()
        record = dict(job)
        record["run"] = str(job["run"])
        write_json(job_path, record)
        err = (CONTROL / "running" / (jid + ".stderr.txt")).open("w", encoding="utf-8")
        proc = subprocess.Popen([PYTHON, str(Path(__file__).resolve()), "_run-job", str(job_path), str(out_path), str(WORK)],
                                cwd=str(ROOT), env=dict(os.environ, **ENV), stdout=subprocess.DEVNULL, stderr=err,
                                creationflags=getattr(subprocess, "BELOW_NORMAL_PRIORITY_CLASS", 0))
        p = psutil.Process(proc.pid)
        p.cpu_percent(None)
        workers[jid] = {"job": job, "key": k, "popen": proc, "proc": p, "procs": [p], "pids": {p.pid}, "started": time.monotonic(),
                        "started_at": now(), "out": out_path, "job_path": job_path, "stderr": err}

    def reap() -> int:
        reaped = 0
        for jid, w in list(workers.items()):
            code = w["popen"].poll()
            if code is None:
                continue
            w["stderr"].close()
            result = None
            if w["out"].exists():
                try:
                    result = json.loads(w["out"].read_text(encoding="utf-8"))
                except Exception:
                    result = None
            if result is None:
                stderr = (CONTROL / "running" / (jid + ".stderr.txt")).read_text(encoding="utf-8", errors="replace")[-3000:]
                result = dict(w["job"], run=str(w["job"]["run"]), status="failed",
                              error="job process exited with code {0} without a result".format(code), trace=stderr,
                              wall_s=round(time.monotonic() - w["started"], 2))
            k = w["key"]
            result["attempt"] = attempts.get(k, 0) + 1
            attempts[k] = result["attempt"]
            with jobs_file.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(result) + "\n")
                handle.flush()
                os.fsync(handle.fileno())
            done.append(result)
            learn(result)
            if result.get("status") == "complete":
                finished.add(k)
                completed_times.append((time.monotonic(), float(result.get("wall_s") or 0.0)))
            else:
                log("job FAILED {0} {1} {2} {3}: {4}".format(result["family"], result["level"], result["run"],
                                                            result.get("recorder"), result.get("error")))
            for path in (w["out"], w["job_path"], CONTROL / "running" / (jid + ".stderr.txt")):
                try:
                    path.unlink()
                except OSError:
                    pass
            del workers[jid]
            reaped += 1
        return reaped

    def extend_seeds() -> None:
        for (f, label), ss in seeds.items():
            if not stochastic[f] or len(ss) >= args.max_seeds:
                continue
            cond = [j for run in runs for j in robustness.jobs_for(run, f, ss) if j["level"] == label]
            if any(job_id(key(j)) in workers for j in cond):
                continue
            if all(key(j) in finished or attempts.get(key(j), 0) >= args.max_attempts for j in cond) \
                    and robustness.need_more_seeds(done, f, label):
                ss.append(len(ss))
                log("seed {0} added for {1} / {2}".format(len(ss) - 1, f, label))

    def snapshot(pending: List[Dict[str, Any]], final: Optional[str] = None) -> Dict[str, Any]:
        latest = robustness.latest_results(done)
        hour = time.monotonic() - 3600.0
        recent = [w for t, w in completed_times if t >= hour]
        rate = sum(recent) / 3600.0 if completed_times and completed_times[0][0] <= hour else (
            sum(w for _, w in completed_times) / max(time.monotonic() - started, 1.0) if completed_times else None)
        remaining_work = sum(estimate(j, walls) for j in pending) + sum(
            max(0.0, estimate(w["job"], walls) - (time.monotonic() - w["started"])) for w in workers.values())
        eta_h = (remaining_work / rate / 3600.0) if rate else None
        return {"state": final or state, "time": now(), "controller_pid": os.getpid(), "freeze": freeze,
                "workers_target": target, "workers_running": len(workers), "target_reason": reason,
                "jobs_records": len(done), "jobs_complete": sum(1 for r in latest if r.get("status") == "complete"),
                "jobs_failed_final": sum(1 for r in latest if r.get("status") != "complete"
                                         and attempts.get(key(r), 0) >= args.max_attempts),
                "jobs_pending_scheduled": len(pending), "pending_note": "jobs of the seeds decided so far; adaptive seeds may add more",
                "running": [{"family": w["job"]["family"], "level": w["job"]["level"], "run": str(w["job"]["run"]),
                             "recorder": w["job"].get("recorder"), "seed": w["job"]["seed"], "started": w["started_at"]}
                            for w in workers.values()],
                "completed_last_hour": len(recent), "work_seconds_per_hour": None if rate is None else round(rate * 3600.0),
                "estimated_remaining_hours": None if eta_h is None else round(eta_h, 2),
                "resources": monitor.samples[-1] if monitor.samples else None,
                "seeds": {"{0} / {1}".format(f, label): len(ss) for (f, label), ss in seeds.items() if stochastic[f]}}

    started = time.monotonic()
    pending = pending_jobs()
    last_pending = time.monotonic()
    try:
        while True:
            changed = reap()
            cmd = command()
            t = time.monotonic()
            if t - last_sample >= SAMPLE_S:
                monitor.sample(workers)
                last_sample = t
            if cmd == "stop-now":
                state = "STOPPING"
                for jid, w in list(workers.items()):
                    try:
                        for child in w["proc"].children(recursive=True):
                            child.terminate()
                        w["proc"].terminate()
                    except Exception:
                        pass
                gone, alive = psutil.wait_procs([p for w in workers.values() for p in w["procs"]], timeout=30)
                for p in alive:
                    p.kill()
                interrupted = []
                for jid, w in list(workers.items()):
                    w["stderr"].close()
                    interrupted.append({"family": w["job"]["family"], "level": w["job"]["level"], "run": str(w["job"]["run"]),
                                        "recorder": w["job"].get("recorder"), "seed": w["job"]["seed"]})
                    for path in (w["out"], w["job_path"], CONTROL / "running" / (jid + ".stderr.txt")):
                        try:
                            path.unlink()
                        except OSError:
                            pass
                    del workers[jid]
                shutil.rmtree(str(WORK), ignore_errors=True)  # the scratch copies of the interrupted jobs
                pending = pending_jobs()
                snap = snapshot(pending, "PAUSED")
                snap["interrupted_jobs"] = interrupted
                snap["interrupted_note"] = "terminated on stop-now: not recorded, pending again (same seeds and keys)"
                write_json(CONTROL / "state.json", snap)
                log("stopped now: {0} running jobs interrupted (pending again)".format(len(interrupted)))
                return 0
            if cmd == "pause":
                state = "PAUSING"
                if not workers:
                    pending = pending_jobs()
                    write_json(CONTROL / "state.json", snapshot(pending, "PAUSED"))
                    log("paused: running jobs finished; {0} pending".format(len(pending)))
                    return 0
            else:
                state = "RUNNING"
            if t - last_decide >= DECIDE_S and len(monitor.samples) >= 3:
                new, why = decide(target, monitor.samples, len(workers), monitor.cpus)
                if new != target:
                    log("concurrency {0} -> {1}: {2}".format(target, new, why))
                target, reason = new, why
                last_decide = t
            if state == "RUNNING":
                if changed or t - last_pending >= SAMPLE_S:
                    if changed:
                        extend_seeds()
                    pending = pending_jobs()
                    last_pending = t
                while len(workers) < target and pending:
                    job = pending.pop(0)
                    if key(job) in finished or job_id(key(job)) in workers:
                        continue
                    launch(job)
                if not pending and not workers:
                    extend_seeds()
                    pending = pending_jobs()
                    if not pending:
                        robustness.summarize(done, RESULTS)
                        write_json(CONTROL / "state.json", snapshot([], "COMPLETE"))
                        log("campaign complete: {0} records; summary written".format(len(done)))
                        return 0
            if t - last_report >= REPORT_S or not (CONTROL / "state.json").exists():
                snap = snapshot(pending if state == "RUNNING" else pending_jobs())
                snap["other_workloads"] = monitor.others({pid for w in workers.values() for pid in w["pids"]})
                write_json(CONTROL / "state.json", snap)
                with (CONTROL / "monitor.jsonl").open("a", encoding="utf-8") as handle:
                    handle.write(json.dumps({k: snap[k] for k in ("time", "state", "workers_target", "workers_running",
                                                                  "target_reason", "jobs_records", "jobs_complete",
                                                                  "jobs_pending_scheduled", "completed_last_hour",
                                                                  "work_seconds_per_hour", "estimated_remaining_hours",
                                                                  "resources", "other_workloads")}) + "\n")
                last_report = t
            time.sleep(POLL_S)
    except Exception:
        log("controller error: " + traceback.format_exc())
        write_json(CONTROL / "state.json", {"state": "CONTROLLER_ERROR", "time": now(), "trace": traceback.format_exc()[-3000:],
                                            "note": "running job processes continue and their results are lost; "
                                                    "resume re-runs them"})
        raise
    finally:
        try:
            lock.unlink()
        except OSError:
            pass


# ------------------------------------------------------------------------------------------------------------
# commands
# ------------------------------------------------------------------------------------------------------------

def start_detached(extra: List[str]) -> int:
    CONTROL.mkdir(parents=True, exist_ok=True)
    flags = 0x00000008 | 0x00000200  # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP: survives the terminal / chat
    out = (CONTROL / "controller.stdout.txt").open("a", encoding="utf-8")
    proc = subprocess.Popen([PYTHON, str(Path(__file__).resolve()), "_supervise"] + extra, cwd=str(ROOT),
                            env=dict(os.environ, **ENV), stdin=subprocess.DEVNULL, stdout=out, stderr=out,
                            creationflags=flags, close_fds=True)
    print("controller started detached: pid {0}; status: python scripts\\campaign_controller.py status".format(proc.pid))
    return 0


def status() -> int:
    import psutil
    state_path = CONTROL / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {}
    lock = CONTROL / "controller.lock"
    alive = False
    if lock.exists():
        try:
            alive = psutil.pid_exists(json.loads(lock.read_text(encoding="utf-8"))["pid"])
        except Exception:
            pass
    import robustness
    records = read_jsonl(RESULTS / "jobs.jsonl")
    latest = robustness.latest_results(records)
    print("controller running: {0}; requested: {1}".format(alive, command() or "none (RUNNING)"))
    print("state ({0}): {1}".format(state.get("time"), state.get("state")))
    print("job records {0}; jobs complete {1}; failed (latest attempt) {2}".format(
        len(records), sum(1 for r in latest if r.get("status") == "complete"),
        sum(1 for r in latest if r.get("status") != "complete")))
    for k in ("workers_target", "workers_running", "target_reason", "jobs_pending_scheduled", "completed_last_hour",
              "work_seconds_per_hour", "estimated_remaining_hours"):
        print("  {0}: {1}".format(k, state.get(k)))
    res = state.get("resources") or {}
    if res:
        print("  resources: CPU {0}% ({1} cores campaign, {2} other), RAM available {3}/{4} GB, campaign RSS {5} GB, "
              "page file {6} GB, disk free {7} GB".format(res.get("cpu_percent"), res.get("own_cores"), res.get("other_cores"),
                                                         res.get("ram_available_gb"), res.get("ram_total_gb"),
                                                         res.get("own_rss_gb"), res.get("pagefile_used_gb"),
                                                         res.get("disk_free_gb")))
    if state.get("interrupted_jobs"):
        print("  interrupted (pending again): {0}".format(len(state["interrupted_jobs"])))
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=("start", "status", "pause", "stop-now", "resume", "_supervise", "_run-job"))
    parser.add_argument("rest", nargs="*")
    parser.add_argument("--families", default="")
    parser.add_argument("--min-seeds", type=int, default=3)
    parser.add_argument("--max-seeds", type=int, default=8)
    parser.add_argument("--max-attempts", type=int, default=2)
    args = parser.parse_args(argv)
    if args.command == "_run-job":
        os.environ.update(ENV)
        return run_one(Path(args.rest[0]), Path(args.rest[1]), args.rest[2])
    if args.command == "_supervise":
        return supervise(args)
    if args.command == "status":
        return status()
    CONTROL.mkdir(parents=True, exist_ok=True)
    if args.command in ("pause", "stop-now"):
        (CONTROL / "command").write_text(args.command, encoding="utf-8")
        print("{0} requested; the controller acts on it within a few seconds (check: status)".format(args.command))
        return 0
    extra = ["--families", args.families] if args.families else []
    if args.command == "resume":
        try:
            (CONTROL / "command").unlink()
        except OSError:
            pass
    if command() in ("pause", "stop-now"):
        print("a {0} request is pending: use resume".format(command()))
        return 1
    return start_detached(extra)


if __name__ == "__main__":
    raise SystemExit(main())
