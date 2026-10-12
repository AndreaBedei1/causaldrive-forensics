#!/usr/bin/env python3
"""PRIVILEGED debug evaluator: raw radar/body attribution, never runtime input.

Ground truth labels the saved returns only here. Outputs are diagnostic artifacts,
not a source of identity for reconstruction, fusion or replay.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from audit_radar_visibility import Box, _rotation
from cdf.recording.compact_observations import load_radar_observations
from cdf.reconstruction.config import load_config
from cdf.reconstruction.local import read_jsonl, reconstruct_vehicle
from cdf.reconstruction.tracking import RadarMount, RadarStream, radar_sweeps, associate_returns, filter_and_smooth


def diagnose(run, owner, start, end):
    cfg = load_config()
    local = reconstruct_vehicle(run / 'vehicles' / owner, cfg)
    alignment = json.loads((run / 'reconstruction/global/alignment.json').read_text(encoding='utf-8'))
    offset = alignment['graphs'][owner]['offset_to_global']
    states = read_jsonl(run / 'ground_truth/states.jsonl')
    frames = {}
    for state in states:
        frames.setdefault(int(state['frame']), {})[state['participant_id']] = state
    streams = [RadarStream(RadarMount.from_metadata(o.metadata), o)
               for o in load_radar_observations(run / 'vehicles' / owner)]
    sweeps = radar_sweeps(streams, local.ego, local.clock_origin, cfg.tracking, local.footprint)
    raw_tracks = associate_returns(sweeps, cfg.tracking)
    measurements = {round(m.t_local, 4): [] for sw in sweeps for m in [sw]}
    for tr in raw_tracks:
        initial, _, _ = filter_and_smooth(tr.measurements, cfg.tracking)
        for m, state in zip(tr.measurements, initial):
            measurements[round(m.t_local, 4)].append((tr.track_id, m, state))
    rows, relative, claimed = [], [], []
    first = read_jsonl(run / 'vehicles' / owner / 'ego.jsonl')[0]
    yaw0 = math.radians(first['yaw_deg'])
    rot0 = np.array([[math.cos(yaw0), -math.sin(yaw0)], [math.sin(yaw0), math.cos(yaw0)]])
    for stream in streams:
        meta = stream.observations.metadata
        mount = meta.get('sensor_transform') or {}
        mount_pos = np.array([mount.get('x', 0), mount.get('y', 0), mount.get('z', .6)])
        mount_rot = _rotation(mount.get('yaw_deg', 0), mount.get('pitch_deg', 0), 0)
        obs = stream.observations
        for i, frame in enumerate(obs.frames):
            t = round(float(obs.timestamps[i]) - local.clock_origin, 4)
            if not start <= t <= end:
                continue
            world = frames[int(frame)]
            own = world[owner]['transform']
            own_pos = np.array([own['x'], own['y'], own['z']])
            own_rot = _rotation(own['yaw_deg'], own['pitch_deg'], own['roll_deg'])
            sensor = own_pos + own_rot @ mount_pos
            sensor_rot = own_rot @ mount_rot
            data = np.asarray(obs.frame_detections(i), dtype=float).reshape(-1, 4)
            depth, az, el, velocity = data.T
            los = np.column_stack([np.cos(el)*np.cos(az), np.cos(el)*np.sin(az), np.sin(el)])
            points = sensor + (los * depth[:, None]) @ sensor_rot.T
            height = mount_pos[2] + depth * np.sin(el)
            filtered = (height >= cfg.tracking.min_height_m) & (height <= cfg.tracking.max_height_m)
            for target, state in world.items():
                if target == owner:
                    continue
                box = Box(state)
                on = box.contains(points, .5)
                body = (box.surface_points() - sensor) @ sensor_rot
                az_body = np.arctan2(body[:, 1], body[:, 0])
                el_body = np.arctan2(body[:, 2], np.hypot(body[:, 0], body[:, 1]))
                fov = bool(((np.linalg.norm(body, axis=1) <= float(meta.get('range_m', 90)))
                            & (np.abs(az_body) <= math.radians(meta['horizontal_fov_deg'])/2)
                            & (np.abs(el_body) <= math.radians(meta['vertical_fov_deg'])/2)).any())
                occlusion = any(Box(s).blocks(sensor, box.centre) for pid,s in world.items() if pid not in (owner,target))
                def bounds(values):
                    return [round(float(v), 4) for v in [values.min(), np.median(values), values.max()]] if len(values) else None
                rows.append(dict(t_local=t, t_global=round(t+offset,4), radar=stream.sensor_id, target=target,
                                 raw=int(on.sum()), height_pass=int((on & filtered).sum()), fov=fov,
                                 centre_ray_occluded=occlusion, range_m=bounds(depth[on]),
                                 azimuth_deg=bounds(np.degrees(az[on])), range_rate_mps=bounds(velocity[on])))
    for sw in sweeps:
        t = sw.t_local
        if not start <= t <= end:
            continue
        nearest = min(frames.values(), key=lambda w:abs(float(w[owner]['timestamp'])-local.clock_origin-t))
        boxes = {pid:Box(s) for pid,s in nearest.items() if pid != owner}
        pts = np.column_stack([np.array([first['x'],first['y']])+sw.points @ rot0.T, np.zeros(len(sw.points))])
        for pid,box in boxes.items():
            pts[:,2]=box.centre[2]
            on=box.contains(pts,.5)
            relative.append(dict(t_local=t,t_global=round(t+offset,4),target=pid,
                longitudinal_m=round(float(((box.centre[:2]-np.array([nearest[owner]['transform']['x'],nearest[owner]['transform']['y']])) @ _rotation(nearest[owner]['transform']['yaw_deg'],0,0)[:2,:2])[0]),4),
                lateral_m=round(float(((box.centre[:2]-np.array([nearest[owner]['transform']['x'],nearest[owner]['transform']['y']])) @ _rotation(nearest[owner]['transform']['yaw_deg'],0,0)[:2,:2])[1]),4),
                filtered_returns=int(on.sum()),moving_returns=int((on & (np.abs(sw.radial_speed)>=cfg.tracking.moving_speed_mps)).sum())))
        for tid,m,state in measurements[t]:
            if m.points is None:
                continue
            world_xy=np.array([first['x'],first['y']])+m.points @ rot0.T
            counts={pid:int(box.contains(np.column_stack([world_xy,np.zeros(len(world_xy))+box.centre[2]]),.5).sum()) for pid,box in boxes.items()}
            speed=np.linalg.norm(state[2:])
            span=np.percentile(m.points @ np.array([-state[3],state[2]])/speed,[5,95]) if speed>1e-6 else [0,0]
            claimed.append(dict(t_local=t,t_global=round(t+offset,4),track=tid,radars=m.radars,n_returns=m.n_returns,
                                body_votes=counts,transverse_span_m=round(float(span[1]-span[0]),4)))
    events=[n.to_dict() for n in local.graph.nodes if n.event_type in ('TRACK_LOST','TRACK_APPEARED','EGO_PATH_ENTRY','CRITICAL_TTC_START','CRITICAL_TTC_END') or n.event_type.startswith('CUT_IN')]
    return dict(privileged=True,ground_truth_runtime=False,run=run.as_posix(),owner=owner,offset_to_global=offset,
                window_local=[start,end],raw_by_radar=rows,filtered_by_sweep=relative,claimed_by_track=claimed,
                segments=[dict(track=t.track_id,first=t.first_t,last=t.last_t,ambiguous=t.identity_ambiguous) for t in local.tracks],events=events)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run',type=Path)
    parser.add_argument('--owner',default='C')
    parser.add_argument('--start',type=float,default=2.65)
    parser.add_argument('--end',type=float,default=7.0)
    parser.add_argument('--json',type=Path,required=True)
    args=parser.parse_args()
    result=diagnose(args.run,args.owner,args.start,args.end)
    args.json.parent.mkdir(parents=True,exist_ok=True)
    args.json.write_text(json.dumps(result,indent=1)+'\n',encoding='utf-8')
    print('PRIVILEGED diagnostic written:',args.json)


if __name__=='__main__':
    main()
