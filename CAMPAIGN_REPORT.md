# 360-degree surround radar campaign (2026-10-02)

Every run of the campaign was re-recorded with CARLA 0.9.15 (Epic quality, seed 0, private engine) with a
logical 360-degree surround radar per vehicle, then reconstructed and evaluated again. No raw data of the former
200-degree recordings remains in `traces/`. S04 was removed from the campaign (configuration, traces,
aggregates); S05-S16 keep their numbers, and S14 has not existed since `cfb4b87`. The campaign has 32 runs:
S01 {avoided, crash}, S02 {avoided, crash, critical_before_cut_in}, S03 crash, S05 crash, S06 {a_front_pushed,
b_rear_first}, S07 {full_view, occluded}, S08 crash, S09 merge_conflict (Town03_Opt), S10 and S11
{rolls_through, stops_safely, stops_then_proceeds}, S12 {a_arrives_first, b_arrives_first, b_fails_to_stop,
near_simultaneous}, S13 {accelerates_into_gap, cut_in, safe_lane_change}, S15 {b_stops, deflected_into_c,
single_impact}, S16 {avoided, consequential, independent}. All on Town05 except S09; speed limit 50 km/h.

Campaign files: `traces/campaign_runs.json` (recording log), `traces/campaign_summary.json`,
`traces/radar_visibility_audit.json` and `traces/stop_sign_audit.json` (both privileged), and
`traces/vocabulary_comparison.json`, a historical comparison of the event vocabularies on the 2026-09-29
recordings, with S04 removed. The former reports are in git: commit `4d0159e` (200-degree radar) and
earlier.

## 1. Sensor model

Every vehicle carries one logical radar, `surround`: the aggregate coverage of the radars distributed
around a car, modelled as one sensor centred over the vehicle above its roof.

| Property | Value |
|---|---|
| Mount (vehicle frame) | x = 0, y = 0, yaw = 0, pitch = 0 |
| Height | 0.30 m above the top of the vehicle's own bounding box: model3 1.78 m, audi.tt 1.69 m, nissan.patrol 2.16 m, mercedes.sprinter 2.87 m |
| Horizontal / vertical FOV | 360 deg / 30 deg (+-15 deg) |
| Points per second | 21600 (6 x 3600) |
| Range / tick | 90 m radial / 0.05 s |
| Physical make-up | six co-located CARLA radars of 90 deg at yaws 0, 60, ..., 300 deg (15 deg overlap each side), merged into one sensor frame at recording time |

The vehicle's own bounding box is recorded as `ego_footprint` in `vehicles/X/metadata.json`.

### 1.1 CARLA does not support a single 360-degree radar

Measured on our CARLA 0.9.15 build: one `sensor.other.radar` (range 90 m, vertical FOV 30 deg,
10800 pps) in an empty map surrounded by parked cars, 20 sweeps per setting.

| `horizontal_fov` set | Returns in 20 sweeps | Azimuth of the returns |
|---:|---:|---|
| 360 deg | 4217 | -0.0 .. +0.0 deg |
| 359 deg | 4217 | -0.5 .. +0.5 deg |
| 270 deg | 3764 | -44.5 .. +44.8 deg |
| 200 deg | 2293 | -79.8 .. +79.5 deg |
| 181 deg | 487 | -88.7 .. +87.0 deg |
| 180 deg | 0 | none |
| 179 deg | 517 | -88.6 .. +86.4 deg |
| 170 deg | 1856 | -84.8 .. +84.1 deg |
| 120 deg | 3584 | -59.8 .. +59.3 deg |
| 90 deg | 3721 | -44.8 .. +44.5 deg |

The radar traces its rays inside a cone around its x axis whose lateral half-width is
`tan(horizontal_fov / 2) * range`. A horizontal FOV of 180 deg or more therefore folds back: 200 deg
behaves as +-80 deg, 270 deg as +-45 deg, 360 deg as a vertical slice straight ahead, and 180 deg returns
nothing. The forward component of every ray is the range, so off-axis rays reach beyond it. Hence the
fallback, six physical radars merged into one logical sensor. Each sweep's azimuths are rotated by the radar's yaw
into the logical frame and wrapped to (-180, 180]. Depth and radial velocity lie along the line of sight
and are unchanged. Returns beyond 90 m radial are dropped. The reconstruction never sees the six radars.

### 1.2 Points per second, layout, vertical FOV, mount height

Returns per sweep on a parked car ahead, empty map, mount 1.78 m (model3 roof + 0.30 m), 40 sweeps:

| Configuration | Returns per sweep (all) | Car at 12 m | 25 m | 40 m | 60 m |
|---|---:|---:|---:|---:|---:|
| former radar: 200 deg (effective +-80), 10 deg, 6000 pps, bumper x=2.2 z=1.0 | 170.5 | 24.23 | 4.33 | 1.61 | 0.42 |
| 6 x 90 deg, 30 deg, 10800 pps | 187.6 | 5.1 | 1.31 | 0.38 | 0.31 |
| **6 x 90 deg, 30 deg, 21600 pps (chosen)** | 370.1 | 10.07 | 2.74 | 0.87 | 0.56 |
| 6 x 90 deg, 30 deg, 43200 pps | 741.8 | 20.21 | 5.09 | 1.79 | 1.15 |
| 6 x 90 deg, 20 deg, 21600 pps | 318.2 | 8.93 | 3.46 | 1.11 | 0.79 |
| 4 x 120 deg, 30 deg, 21600 pps | 345.0 | 8.41 | 2.83 | 1.31 | 0.58 |

At 10800 pps (= 6000 x 360/200, the former horizontal density) and a 30 deg vertical FOV, a car 25-40 m
away got 3-4x fewer returns than from the former radar. The rays are spread over 360 x 30 deg instead of
about 160 x 10 deg. 21600 pps gives 0.5-1.3x the former returns at 25-60 m. The layouts differ
little; 6 x 90 deg spreads the returns most evenly over the azimuth (4.5-5.7 per sweep on twelve cars
around at 12 m). Engine cost on Town05 with three vehicles: 11-13 ms per tick for 10800-43200 pps, no
callback lost. Returns per vehicle and sweep on Town05: about 970 at 21600 pps, against about 220 for the
former radar. The radar data of the campaign grows accordingly.

Near field: an audi.tt (roof 1.39 m) at a known gap from a model3 recorder. Each cell gives the share of
sweeps that see it and the error of the nearest return's clearance against the true gap.

| Mount | VFOV | Target | Front 0.3 m | Side 0.3 m | Rear 0.3 m | Front 2 m | Side 2 m |
|---|---:|---|---|---|---|---|---|
| fixed 2.80 m | 20 deg | audi.tt | not seen | not seen | not seen | not seen | not seen |
| fixed 2.80 m | 30 deg | audi.tt | not seen | not seen | not seen | 95% seen, +1.49 m | not seen |
| roof + 0.40 m | 20 deg | audi.tt | 100% seen, +1.12 m | not seen | 100% seen, +1.55 m | 100% seen, +0.58 m | 100% seen, +0.80 m |
| roof + 0.40 m | 30 deg | audi.tt | 100% seen, +0.57 m | 100% seen, +0.89 m | 100% seen, +0.91 m | 100% seen, +0.07 m | 100% seen, +0.38 m |
| roof + 0.25 m | 20 deg | audi.tt | 100% seen, +0.85 m | 80% seen, +1.13 m | 100% seen, +1.30 m | 100% seen, +0.26 m | 100% seen, +0.45 m |
| roof + 0.25 m | 30 deg | audi.tt | 100% seen, +0.30 m | 100% seen, +0.48 m | 100% seen, +0.60 m | 100% seen, +0.05 m | 100% seen, +0.19 m |

A single absolute height cannot serve roofs of 1.39-2.57 m (the Sprinter, S16). At 2.8 m, just above
the Sprinter, a sedan sees nothing of a car within 2-4 m ahead or behind, or within 4-8 m beside it. The
mount is therefore a fixed 0.30 m above each vehicle's own roof, and the vertical FOV 30 deg, the top
of the suggested 20-30 deg. The final setting, every campaign blueprint as recorder, gives these
nearest-return clearance errors in metres ("-" = not seen):

| Ego (radar height) | Target | 0.3 m front / side / rear | 1 m front / side / rear | 4 m front / side / rear | Own-body returns per sweep |
|---|---|---|---|---|---:|
| model3 (1.78 m) | tt | +0.40 / +0.57 / +0.67 | +0.17 / +0.45 / +0.37 | +0.05 / +0.09 / +0.08 | 0.0 |
| model3 (1.78 m) | model3 | +0.09 / +0.43 / +0.74 | +0.09 / +0.36 / +0.46 | +0.05 / +0.17 / +0.07 | 0.0 |
| model3 (1.78 m) | sprinter | +0.03 / -0.03 / +0.22 | +0.03 / +0.04 / +0.14 | +0.03 / +0.03 / +0.05 | 0.1 |
| tt (1.69 m) | tt | +0.38 / +0.48 / +0.61 | +0.16 / +0.40 / +0.32 | +0.05 / +0.06 / +0.08 | 0.0 |
| tt (1.69 m) | model3 | +0.09 / +0.39 / +0.69 | +0.08 / +0.32 / +0.41 | +0.05 / +0.16 / +0.06 | 0.0 |
| tt (1.69 m) | sprinter | +0.03 / +0.02 / +0.20 | +0.03 / +0.03 / +0.13 | +0.03 / +0.03 / +0.05 | 0.1 |
| patrol (2.16 m) | tt | +1.11 / - / +1.85 | +0.93 / - / +1.63 | +0.10 / +0.33 / +0.53 | 4.5 |
| patrol (2.16 m) | model3 | - / +1.54 / +1.91 | +0.60 / +1.05 / +1.69 | +0.06 / +0.29 / +0.59 | 4.5 |
| patrol (2.16 m) | sprinter | +0.05 / +0.10 / +0.99 | +0.05 / +0.08 / +0.85 | +0.03 / +0.04 / +0.20 | 4.5 |
| sprinter (2.87 m) | tt | - / - / - | +1.95 / - / - | +0.66 / - / - | 14.5 |
| sprinter (2.87 m) | model3 | +2.14 / - / - | +1.74 / - / - | +0.37 / +1.38 / - | 14.5 |
| sprinter (2.87 m) | sprinter | +0.12 / +0.29 / +1.87 | +0.11 / +0.25 / +1.83 | +0.06 / +0.11 / +1.50 | 14.5 |

The tall vehicles see low cars close by from far above: the patrol misses an audi.tt within about 1 m
beside it, and the Sprinter misses low cars within 4 m beside or behind it. Their own roofs also return a
few rays (4.5 and 14.5 per sweep), which the reconstruction drops.

## 2. Reconstruction changes

- Clearance. A range is measured from the radar, at the vehicle centre. With the footprint (half-length
  L/2, half-width W/2 around the radar), every return and track also gets
  `clearance_m = max(0, planar_range_m - ego_extent(theta))`, where
  `ego_extent(theta) = min((L/2) / |cos theta|, (W/2) / |sin theta|)`. A zero cosine or sine leaves the
  other side; the code computes the ray's exit from the rectangle, which also covers an off-centre radar.
  A track's clearance belongs to its near surface: per sweep, the 10th percentile of its returns'
  clearances. Its depth behind the Kalman-tracked median point is smoothed over five sweeps. The raw
  `range_m` stays in TRACK_STATE.
- TTC is `clearance / closing speed`, and CRITICAL_TTC's braking need uses the clearance. The closing
  speed (line-of-sight range rate) and the closest point of approach (relative position and velocity)
  are unchanged. `d_cpa_clearance_m` is added.
- EGO_PATH and CUT_IN: "ahead" means beyond the recorder's front edge (`ahead_of_front_m`), not merely
  ahead of the radar.
- Identity association uses the clearance for the approach trend and at the contact. `contact_window_s`
  is 1.0 s: a track may be lost up to 1 s before its contact. The tracker still ends a silent track after
  0.5 s, and persistence, approach, speed, the matched collision and uniqueness are still required.
- Own body: returns inside the footprint (at least 0.05 m in) are dropped.
- Ego motion: the radar's own velocity is its displacement over the last sweep, from the recorder's
  own poses (position, heading, pitch, roll), because that is how CARLA's radar measures it. Static
  scenery then stays static in turns, under braking and through an impact. The instantaneous vehicle
  velocity differs by up to about 3 m/s at an impact: with it, 2.2 % of S05 B's static returns
  looked like moving targets and its radar built 53 tracks, 52 of them false. Doppler speeds are projected onto
  the horizontal plane.
- Tracking at 360 deg: returns are clustered in the local Cartesian frame (no azimuth wrap), bearings
  are only reported. TRACK_APPEARED_REAR is new: first azimuth within 5 deg of straight behind.
- Collision segmentation: in the new S06 `a_front_pushed`, A rebounds into B 0.2 s after the impact
  with 0.52 of its peak impulse, pushed backwards both times. The previous single threshold (0.5) would
  have split this rebound. The rule is now three-tier: from 0.75 of the contact's peak a new impact;
  below 0.25 the same contact; in between the recorder's own impact-like velocity jumps decide (reversed
  = new impact from the other side, same direction = rebound), falling back to 0.5 without them.

## 3. Recording

32 runs, 75 recorders, recorded 2026-10-02 12:01-12:23 by the unchanged `scripts/run_scenario.py` on a private
engine (port 3000, idle GPU). Before each run its old directory was deleted. Every logical radar frame was
complete: no queue drop, no missing frame, no incomplete frame. The only failed attempt (S11 stops_safely) was
the known transient `OSError [Errno 22]` while writing the camera metadata on the Desktop; the retry
succeeded.

| Run | Map | Attempts | Wall time | Recorders (radar height) | Sweeps | Returns per sweep | Queue drops / missing / incomplete frames |
|---|---|---:|---:|---|---:|---|---|
| S01/run_0_avoided | Town05 | 1 | 35 s | A 1.78 m, B 1.69 m | 262 | 734, 674 | 0 / 0 / 0 |
| S01/run_0_crash | Town05 | 1 | 23 s | A 1.78 m, B 1.69 m | 240 | 728, 679 | 0 / 0 / 0 |
| S02/run_0_avoided | Town05 | 1 | 30 s | A 1.78 m, B 1.69 m | 304 | 734, 699 | 0 / 0 / 0 |
| S02/run_0_crash | Town05 | 1 | 30 s | A 1.78 m, B 1.69 m | 304 | 801, 772 | 0 / 0 / 0 |
| S02/run_0_critical_before_cut_in | Town05 | 1 | 27 s | A 1.78 m, B 1.69 m | 230 | 833, 831 | 0 / 0 / 0 |
| S03/run_0_crash | Town05 | 1 | 32 s | A 1.78 m, B 1.69 m | 304 | 907, 935 | 0 / 0 / 0 |
| S05/run_0_crash | Town05 | 1 | 29 s | A 1.78 m, B 1.69 m | 290 | 908, 932 | 0 / 0 / 0 |
| S06/run_0_a_front_pushed | Town05 | 1 | 73 s | A 1.78 m, B 1.69 m, C 2.16 m | 600 | 696, 698, 598 | 0 / 0 / 0 |
| S06/run_0_b_rear_first | Town05 | 1 | 41 s | A 1.78 m, B 1.69 m, C 2.16 m | 284 | 733, 714, 610 | 0 / 0 / 0 |
| S07/run_0_full_view | Town05 | 1 | 41 s | A 1.78 m, B 1.69 m, C 2.16 m | 284 | 743, 705, 589 | 0 / 0 / 0 |
| S07/run_0_occluded | Town05 | 1 | 41 s | A 1.78 m, B 1.69 m, C 2.16 m | 284 | 765, 705, 589 | 0 / 0 / 0 |
| S08/run_0_crash | Town05 | 1 | 53 s | A 1.78 m, B 1.69 m, C 2.16 m | 304 | 907, 935, 885 | 0 / 0 / 0 |
| S09/run_0_merge_conflict | Town03_Opt | 1 | 50 s | A 1.78 m, B 1.69 m | 300 | 866, 890 | 0 / 0 / 0 |
| S10/run_0_rolls_through | Town05 | 1 | 32 s | A 1.78 m, B 1.69 m | 320 | 952, 952 | 0 / 0 / 0 |
| S10/run_0_stops_safely | Town05 | 1 | 23 s | A 1.78 m, B 1.69 m | 192 | 945, 947 | 0 / 0 / 0 |
| S10/run_0_stops_then_proceeds | Town05 | 1 | 29 s | A 1.78 m, B 1.69 m | 268 | 948, 959 | 0 / 0 / 0 |
| S11/run_0_rolls_through | Town05 | 1 | 32 s | A 1.78 m, B 1.69 m | 320 | 950, 951 | 0 / 0 / 0 |
| S11/run_0_stops_safely | Town05 | 2 (exit 1) | 41 s | A 1.78 m, B 1.69 m | 192 | 943, 960 | 0 / 0 / 0 |
| S11/run_0_stops_then_proceeds | Town05 | 1 | 29 s | A 1.78 m, B 1.69 m | 268 | 956, 958 | 0 / 0 / 0 |
| S12/run_0_a_arrives_first | Town05 | 1 | 32 s | A 1.78 m, B 1.69 m | 330 | 978, 991 | 0 / 0 / 0 |
| S12/run_0_b_arrives_first | Town05 | 1 | 32 s | A 1.78 m, B 1.69 m | 330 | 968, 980 | 0 / 0 / 0 |
| S12/run_0_b_fails_to_stop | Town05 | 1 | 32 s | A 1.78 m, B 1.69 m | 320 | 965, 981 | 0 / 0 / 0 |
| S12/run_0_near_simultaneous | Town05 | 1 | 29 s | A 1.78 m, B 1.69 m | 300 | 962, 981 | 0 / 0 / 0 |
| S13/run_0_accelerates_into_gap | Town05 | 1 | 23 s | A 1.78 m, B 1.69 m | 200 | 732, 770 | 0 / 0 / 0 |
| S13/run_0_cut_in | Town05 | 1 | 23 s | A 1.78 m, B 1.69 m | 200 | 730, 766 | 0 / 0 / 0 |
| S13/run_0_safe_lane_change | Town05 | 1 | 23 s | A 1.78 m, B 1.69 m | 200 | 760, 813 | 0 / 0 / 0 |
| S15/run_0_b_stops | Town05 | 1 | 41 s | A 1.78 m, B 1.69 m, C 1.69 m | 212 | 952, 951, 943 | 0 / 0 / 0 |
| S15/run_0_deflected_into_c | Town05 | 1 | 53 s | A 1.78 m, B 1.69 m, C 1.69 m | 280 | 948, 946, 948 | 0 / 0 / 0 |
| S15/run_0_single_impact | Town05 | 1 | 50 s | A 1.78 m, B 1.69 m, C 1.69 m | 280 | 948, 946, 967 | 0 / 0 / 0 |
| S16/run_0_avoided | Town05 | 1 | 35 s | A 1.69 m, B 2.16 m, C 2.87 m | 200 | 824, 796, 612 | 0 / 0 / 0 |
| S16/run_0_consequential | Town05 | 1 | 35 s | A 1.69 m, B 2.16 m, C 2.87 m | 200 | 831, 797, 618 | 0 / 0 / 0 |
| S16/run_0_independent | Town05 | 1 | 56 s | A 1.69 m, B 2.16 m, C 2.87 m | 360 | 759, 760, 532 | 0 / 0 / 0 |

## 4. Per-run reconstruction

Transitions are START/END counts over the global graph: BR brake, TL / TR turn left / right, MOV moving, STOP stop,
SPD speed limit exceeded, CLS closing, TTC critical TTC, CUTL / CUTR cut-in from the left / right, STOPSIGN STOP
sign detected, TRACK appeared (F front, R rear, L left, R right) / lost, PATH ego-path entry / exit, COLL
collision nodes. "ok via collision_00x" means aligned through a chain of matched collisions.

| Run | Local nodes:edges | Global nodes:edges | Collision reconstructed | Alignment | Identity associations | Transitions (START/END) |
|---|---|---|---|---|---|---|
| S01/run_0_avoided | A 11:16 B 12:16 | 23:10 | no vehicle-vehicle collision in ground truth | A UNALIGNED B UNALIGNED | none; anonymous 2 (A:track_001, B:track_001) | BR 2/1, MOV 3/2, STOP 2/1, CLS 4/4, TTC 1/1, TRACK 2/0 (F1 R1 L0 R0), PATH 0/0, COLL 0 |
| S01/run_0_crash | A 12:21 B 10:14 | 21:36 | yes (1/1 vehicle contacts) | A ok B ok | A:track_001→B (1.00); B:track_001→A (1.00) | BR 2/0, MOV 2/2, STOP 2/0, CLS 4/3, TTC 1/1, TRACK 2/1 (F1 R1 L0 R0), PATH 0/0, COLL 1 |
| S02/run_0_avoided | A 9:13 B 6:7 | 15:7 | no vehicle-vehicle collision in ground truth | A UNALIGNED B UNALIGNED | none; anonymous 2 (A:track_001, B:track_001) | BR 2/2, MOV 2/0, CLS 2/2, CUTL 1/1, TRACK 2/0 (F0 R0 L1 R1), PATH 1/0, COLL 0 |
| S02/run_0_crash | A 13:22 B 10:15 | 22:39 | yes (1/1 vehicle contacts) | A ok B ok | A:track_001→B (0.95); B:track_001→A (0.99) | BR 3/1, MOV 2/2, STOP 2/0, CLS 2/2, TTC 1/1, CUTL 1/1, TRACK 2/0 (F0 R0 L1 R1), PATH 1/0, COLL 1 |
| S02/run_0_critical_before_cut_in | A 14:26 B 10:13 | 23:45 | yes (1/1 vehicle contacts) | A ok B ok | A:track_001→B (0.91); B:track_001→A (0.97) | BR 4/2, MOV 2/2, STOP 2/0, CLS 2/2, TTC 1/1, CUTL 1/1, TRACK 2/0 (F0 R0 L1 R1), PATH 0/0, COLL 1 |
| S03/run_0_crash | A 9:12 B 11:19 | 19:38 | yes (1/1 vehicle contacts) | A ok B ok | A:track_001→B (0.88); B:track_001→A (0.98) | BR 2/0, MOV 2/2, STOP 2/0, CLS 2/1, TTC 2/1, TRACK 2/1 (F0 R0 L1 R1), PATH 1/0, COLL 1 |
| S05/run_0_crash | A 12:20 B 12:21 | 23:55 | yes (1/1 vehicle contacts) | A ok B ok | A:track_001→B (0.93); B:track_001→A (0.98) | BR 2/0, TL 1/1, MOV 2/2, STOP 2/0, CLS 2/2, TTC 2/2, TRACK 2/0 (F0 R0 L1 R1), PATH 1/1, COLL 1 |
| S06/run_0_a_front_pushed | A 19:37 B 23:37 C 19:30 | 59:121 | yes (2/2 vehicle contacts) | A ok B ok C ok via collision_002 | A:track_001→B (0.66); B:track_001→C (1.00); B:track_002→A (1.00); anonymous 4 | BR 3/1, MOV 4/4, STOP 4/1, SPD 1/1, CLS 12/10, TTC 3/3, TRACK 7/3 (F3 R4 L0 R0), PATH 0/0, COLL 2 |
| S06/run_0_b_rear_first | A 16:27 B 18:31 C 19:30 | 51:102 | yes (2/2 vehicle contacts) | A ok B ok C ok via collision_002 | B:track_001→C (1.00); B:track_002→A (1.00); C:track_002→B (0.99); anonymous 4 | BR 3/0, MOV 3/3, STOP 3/0, SPD 1/1, CLS 11/8, TTC 2/2, TRACK 7/5 (F3 R4 L0 R0), PATH 0/0, COLL 2 |
| S07/run_0_full_view | A 19:33 B 17:28 C 17:23 | 52:72 | yes (1/1 vehicle contacts) | A ok B ok C UNALIGNED | A:track_001→B (1.00); B:track_002→A (1.00); anonymous 5 | BR 3/1, MOV 4/3, STOP 3/1, SPD 1/1, CLS 10/8, TTC 2/2, TRACK 7/5 (F4 R3 L0 R0), PATH 0/0, COLL 1 |
| S07/run_0_occluded | A 19:33 B 17:28 C 17:23 | 52:72 | yes (1/1 vehicle contacts) | A ok B ok C UNALIGNED | A:track_001→B (1.00); B:track_002→A (1.00); anonymous 5 | BR 3/1, MOV 4/3, STOP 3/1, SPD 1/1, CLS 10/8, TTC 2/2, TRACK 7/5 (F4 R3 L0 R0), PATH 0/0, COLL 1 |
| S08/run_0_crash | A 16:27 B 16:32 C 17:34 | 48:78 | yes (1/1 vehicle contacts) | A ok B ok C UNALIGNED | A:track_002→B (0.88); B:track_001→A (0.98); anonymous 4 | BR 3/1, MOV 3/3, STOP 3/0, CLS 6/5, TTC 8/7, TRACK 6/1 (F2 R0 L2 R2), PATH 1/0, COLL 1 |
| S09/run_0_merge_conflict | A 12:16 B 16:26 | 27:51 | yes (1/1 vehicle contacts) | A ok B ok | A:track_001→B (0.85); B:track_001→A (0.99) | BR 2/0, TL 2/2, TR 1/1, MOV 2/2, STOP 2/0, CLS 2/2, TTC 3/3, TRACK 2/0 (F0 R0 L1 R1), PATH 0/0, COLL 1 |
| S10/run_0_rolls_through | A 15:22 B 11:18 | 25:46 | yes (1/1 vehicle contacts) | A ok B ok | A:track_001→B (1.00); B:track_001→A (0.91) | BR 3/1, TL 1/1, MOV 2/2, STOP 2/0, CLS 2/1, TTC 2/1, STOPSIGN 1/1, TRACK 2/1 (F0 R0 L1 R1), PATH 1/0, COLL 1 |
| S10/run_0_stops_safely | A 12:19 B 8:12 | 20:9 | no vehicle-vehicle collision in ground truth | A UNALIGNED B UNALIGNED | none; anonymous 2 (A:track_001, B:track_001) | BR 1/0, MOV 2/1, STOP 1/0, CLS 2/2, TTC 1/1, STOPSIGN 2/2, TRACK 2/1 (F0 R0 L1 R1), PATH 1/1, COLL 0 |
| S10/run_0_stops_then_proceeds | A 17:25 B 9:15 | 26:10 | no vehicle-vehicle collision in ground truth | A UNALIGNED B UNALIGNED | none; anonymous 2 (A:track_001, B:track_001) | BR 1/1, TL 1/1, MOV 3/1, STOP 1/1, CLS 2/2, TTC 1/1, STOPSIGN 2/2, TRACK 2/2 (F0 R0 L1 R1), PATH 1/1, COLL 0 |
| S11/run_0_rolls_through | A 9:12 B 17:25 | 25:43 | yes (1/1 vehicle contacts) | A ok B ok | A:track_001→B (0.97); B:track_001→A (0.98) | BR 3/1, TL 1/1, MOV 2/2, STOP 2/0, CLS 2/1, TTC 2/1, STOPSIGN 1/1, TRACK 2/1 (F0 R0 L1 R1), PATH 1/0, COLL 1 |
| S11/run_0_stops_safely | A 7:12 B 11:17 | 18:9 | no vehicle-vehicle collision in ground truth | A UNALIGNED B UNALIGNED | none; anonymous 2 (A:track_001, B:track_001) | BR 1/0, MOV 2/1, STOP 1/0, CLS 2/2, TTC 1/1, STOPSIGN 1/1, TRACK 2/1 (F0 R0 L1 R1), PATH 1/1, COLL 0 |
| S11/run_0_stops_then_proceeds | A 7:12 B 17:25 | 24:10 | no vehicle-vehicle collision in ground truth | A UNALIGNED B UNALIGNED | none; anonymous 2 (A:track_001, B:track_001) | BR 1/1, TL 1/1, MOV 3/1, STOP 1/1, CLS 2/2, TTC 1/1, STOPSIGN 1/1, TRACK 2/2 (F0 R0 L1 R1), PATH 1/1, COLL 0 |
| S12/run_0_a_arrives_first | A 19:29 B 17:27 | 36:14 | no vehicle-vehicle collision in ground truth | A UNALIGNED B UNALIGNED | none; anonymous 2 (A:track_001, B:track_001) | BR 2/2, TL 1/1, MOV 4/2, STOP 2/2, CLS 3/3, TTC 2/2, STOPSIGN 2/2, TRACK 2/2 (F0 R0 L1 R1), PATH 1/1, COLL 0 |
| S12/run_0_b_arrives_first | A 17:25 B 15:23 | 32:10 | no vehicle-vehicle collision in ground truth | A UNALIGNED B UNALIGNED | none; anonymous 2 (A:track_001, B:track_001) | BR 2/2, TL 1/1, MOV 4/2, STOP 2/2, CLS 3/3, STOPSIGN 2/2, TRACK 2/2 (F0 R0 L1 R1), PATH 1/1, COLL 0 |
| S12/run_0_b_fails_to_stop | A 19:25 B 15:24 | 33:56 | yes (1/1 vehicle contacts) | A ok B ok | A:track_001→B (0.99); B:track_001→A (0.80) | BR 4/2, TL 1/1, MOV 3/3, STOP 3/1, CLS 2/1, TTC 2/1, STOPSIGN 2/2, TRACK 2/1 (F0 R0 L1 R1), PATH 1/0, COLL 1 |
| S12/run_0_near_simultaneous | A 23:36 B 22:39 | 44:101 | yes (1/1 vehicle contacts) | A ok B ok | A:track_001→B (0.98); B:track_001→A (0.91) | BR 4/2, TL 1/1, MOV 4/4, STOP 4/2, CLS 4/4, TTC 2/2, STOPSIGN 3/2, TRACK 2/0 (F0 R0 L1 R1), PATH 1/1, COLL 1 |
| S13/run_0_accelerates_into_gap | A 19:38 B 14:29 | 32:80 | yes (1/1 vehicle contacts) | A ok B ok | A:track_001→B (0.97); B:track_001→A (0.98) | BR 2/0, TR 1/1, MOV 2/2, STOP 2/0, SPD 1/1, CLS 4/4, TTC 3/3, CUTL 1/1, TRACK 2/0 (F0 R0 L1 R1), PATH 1/0, COLL 1 |
| S13/run_0_cut_in | A 13:24 B 10:12 | 22:38 | yes (1/1 vehicle contacts) | A ok B ok | A:track_001→B (0.98); B:track_001→A (0.99) | BR 2/0, TR 1/1, MOV 2/2, STOP 2/0, CLS 2/2, TTC 1/1, CUTL 1/1, TRACK 2/0 (F0 R0 L1 R1), PATH 1/0, COLL 1 |
| S13/run_0_safe_lane_change | A 9:14 B 5:7 | 14:9 | no vehicle-vehicle collision in ground truth | A UNALIGNED B UNALIGNED | none; anonymous 2 (A:track_001, B:track_001) | BR 1/0, MOV 2/0, CLS 4/2, CUTL 1/1, TRACK 2/0 (F0 R0 L1 R1), PATH 1/0, COLL 0 |
| S15/run_0_b_stops | A 13:28 B 26:42 C 10:20 | 49:30 | no vehicle-vehicle collision in ground truth | A UNALIGNED B UNALIGNED C UNALIGNED | none; anonymous 6 | BR 1/0, TL 1/1, MOV 3/1, STOP 1/0, CLS 6/6, TTC 5/5, STOPSIGN 3/2, TRACK 6/4 (F2 R0 L2 R2), PATH 2/2, COLL 0 |
| S15/run_0_deflected_into_c | A 24:43 B 26:51 C 13:25 | 61:130 | yes (2/2 vehicle contacts) | A ok B ok C ok via collision_002 | A:track_001→C (0.96); A:track_002→B (0.91); B:track_002→A (0.95); C:track_001→A (0.97); anonymous 2 (B:track_001, C:track_002) | BR 3/1, TL 2/2, MOV 3/3, STOP 3/0, CLS 6/5, TTC 6/5, STOPSIGN 5/4, TRACK 6/2 (F2 R0 L2 R2), PATH 2/1, COLL 2 |
| S15/run_0_single_impact | A 20:36 B 20:33 C 11:19 | 50:79 | yes (1/1 vehicle contacts) | A ok B ok C UNALIGNED | A:track_002→B (0.91); B:track_001→A (0.95); anonymous 5 | BR 2/1, TL 2/2, MOV 3/2, STOP 2/0, CLS 7/1, TTC 3/1, STOPSIGN 4/3, TRACK 7/2 (F2 R0 L3 R2), PATH 4/3, COLL 1 |
| S16/run_0_avoided | A 10:15 B 14:24 C 9:17 | 32:46 | yes (1/1 vehicle contacts) | A ok B ok C UNALIGNED | A:track_001→B (1.00); B:track_001→A (0.95); anonymous 2 (C:track_001, C:track_002) | BR 2/0, MOV 3/3, STOP 3/0, CLS 6/5, TTC 2/2, TRACK 4/1 (F1 R3 L0 R0), PATH 0/0, COLL 1 |
| S16/run_0_consequential | A 14:18 B 14:24 C 15:25 | 41:83 | yes (2/2 vehicle contacts) | A ok B ok C ok via collision_002 | A:track_001→B (0.99); B:track_001→A (0.94); C:track_001→A (0.84); anonymous 1 (C:track_002) | BR 3/1, TL 1/1, MOV 4/4, STOP 4/1, CLS 6/5, TTC 2/2, TRACK 4/1 (F1 R3 L0 R0), PATH 0/0, COLL 2 |
| S16/run_0_independent | A 22:47 B 17:30 C 21:35 | 58:131 | yes (2/2 vehicle contacts) | A ok B ok via collision_001 C ok | A:track_001→B (1.00); B:track_001→A (0.94); anonymous 5 | BR 3/1, MOV 5/5, STOP 5/2, CLS 8/6, TTC 3/3, STOPSIGN 1/1, TRACK 7/5 (F2 R2 L1 R2), PATH 0/1, COLL 2 |

## 5. Validation

- Metadata: all 75 recorders of the 32 runs have the logical radar at 360 x 30 deg, six physical radars, mount x = y = 0, yaw = pitch = 0, z = own roof + 0.30 m; no deviation.
- Acquisition: queue drops, missing frames and incomplete logical frames are zero in every recorder; returns per sweep 532-991 (median 866); azimuths cover -180.0 .. +180.0 deg.
- Front / side / rear: tracks appeared FRONT 28, REAR 24, LEFT 29, RIGHT 29; track samples (10 Hz) in front (<45 deg) 5778, at the sides 2024, behind (>135 deg) 2906.
- +-180 deg: 25 tracks cross +-180 deg while tracked, each as one track; same-vehicle track splits at the wrap: none.
- Static background (offline, ground-truth boxes): 0 of 64455 returns (0.00%) look like moving targets (>= 1 m/s) while the recorder turns, 0 of 950685 (0.00%) otherwise; tracks on no vehicle: 0 of 110.
- TTC = clearance / closing speed in 4074 of 4074 TRACK_STATE facts with a TTC; the CRITICAL_TTC braking need recomputed from the clearance differs in 0.
- Clearance at contact (the recorder's track lying on its partner, at the last 10 Hz sample at or before the contact, against the true gap between the two boxes then): 51 recorder-contact pairs seen within 0.15 s of the contact; median clearance 0.651 m for a median true gap of 0.0 m; error median 0.529 m, 90th percentile 1.224 m, range 0.0 .. 4.692 m; 1 pair(s) tracked only earlier and 2 not tracked near the contact (section 7).
- Contact window 1 s: 1 track(s) lost 0.5-1.0 s before their contact: S16/run_0_consequential C:track_001 -> ASSOCIATED A (lost 0.75 s before, correct).
- S06 a_front_pushed: COLLISION nodes A+B at +0.00, B+C at +0.15; chains A: collision_001, B: collision_001, C: collision_001 -> collision_002.
- Alignment: every aligned clock has error 0.0 s; clock-shift check (0.73 s): global graph unchanged in every run.
- S04: no configuration, trace, campaign file, metric, test or report table mentions it; `traces/S04` and `configs/scenarios/s04_crossing_braking.yaml` are gone.

## 6. 200-degree front radar vs 360-degree surround radar

Same 32 runs, the former recordings at commit `4d0159e` against the new ones (physics re-run, so small differences in timing are expected).

| | 200 deg | 360 deg |
|---|---:|---:|
| Radar tracks | 263 | 110 |
| Tracks on no vehicle (ghosts) | 187 | 0 |
| (recorder, other vehicle) pairs tracked | 71 | 102 |
| Collision partners tracked | 38 / 54 | 52 / 54 |
| Identity claims correct | 34 / 34 | 49 / 49 |
| Anonymous tracks | 229 | 61 |
| Aligned graphs | 49 | 49 |
| CUT_IN starts | 13 | 6 |
| TRACK_APPEARED_REAR | - | 24 |

| Run | Tracks | Claims correct | Partners tracked | Same collision times | First CRITICAL_TTC shift per pair [s] |
|---|---|---|---|---|---|
| S01/run_0_avoided | 1 -> 2 | 0/0 -> 0/0 | 0 -> 0 / 0 | yes | A->B +0.00 |
| S01/run_0_crash | 1 -> 2 | 1/1 -> 2/2 | 1 -> 2 / 2 | yes | A->B +0.00 |
| S02/run_0_avoided | 1 -> 2 | 0/0 -> 0/0 | 0 -> 0 / 0 | yes | - |
| S02/run_0_crash | 1 -> 2 | 1/1 -> 2/2 | 1 -> 2 / 2 | yes | A->B -0.10 |
| S02/run_0_critical_before_cut_in | 1 -> 2 | 1/1 -> 2/2 | 1 -> 2 / 2 | yes | A->B +0.05 |
| S03/run_0_crash | 2 -> 2 | 2/2 -> 2/2 | 2 -> 2 / 2 | yes | A->B +0.00, B->A +0.00 |
| S05/run_0_crash | 20 -> 2 | 2/2 -> 2/2 | 2 -> 2 / 2 | yes | A->B +0.00, B->A +0.00 |
| S06/run_0_a_front_pushed | 2 -> 7 | 2/2 -> 3/3 | 2 -> 3 / 4 | NO | A->B +0.00, B->C +0.00 |
| S06/run_0_b_rear_first | 2 -> 7 | 1/1 -> 3/3 | 2 -> 4 / 4 | yes | B->C +0.00 |
| S07/run_0_full_view | 2 -> 7 | 1/1 -> 2/2 | 1 -> 2 / 2 | yes | A->B +0.00, B->C +0.00 |
| S07/run_0_occluded | 2 -> 7 | 1/1 -> 2/2 | 1 -> 2 / 2 | yes | A->B +0.00, B->C +0.00 |
| S08/run_0_crash | 6 -> 6 | 2/2 -> 2/2 | 2 -> 2 / 2 | yes | A->C +0.05, A->B +0.00, B->A +0.00, B->C +0.05, C->A +0.00, C->B -0.75 |
| S09/run_0_merge_conflict | 28 -> 2 | 1/1 -> 2/2 | 2 -> 2 / 2 | yes | A->B +0.00, B->A +0.00 |
| S10/run_0_rolls_through | 2 -> 2 | 1/1 -> 2/2 | 2 -> 2 / 2 | yes | A->B -0.05, B->A +0.00 |
| S10/run_0_stops_safely | 2 -> 2 | 0/0 -> 0/0 | 0 -> 0 / 0 | yes | B->A -0.15 |
| S10/run_0_stops_then_proceeds | 16 -> 2 | 0/0 -> 0/0 | 0 -> 0 / 0 | yes | B->A -0.15 |
| S11/run_0_rolls_through | 2 -> 2 | 2/2 -> 2/2 | 2 -> 2 / 2 | yes | A->B -0.05, B->A -0.05 |
| S11/run_0_stops_safely | 2 -> 2 | 0/0 -> 0/0 | 0 -> 0 / 0 | yes | - |
| S11/run_0_stops_then_proceeds | 14 -> 2 | 0/0 -> 0/0 | 0 -> 0 / 0 | yes | - |
| S12/run_0_a_arrives_first | 19 -> 2 | 0/0 -> 0/0 | 0 -> 0 / 0 | yes | A->B -0.15, B->A +0.00 |
| S12/run_0_b_arrives_first | 20 -> 2 | 0/0 -> 0/0 | 0 -> 0 / 0 | yes | - |
| S12/run_0_b_fails_to_stop | 5 -> 2 | 2/2 -> 2/2 | 2 -> 2 / 2 | yes | A->B -0.05, B->A -0.05 |
| S12/run_0_near_simultaneous | 20 -> 2 | 2/2 -> 2/2 | 2 -> 2 / 2 | yes | A->B -0.05, B->A +0.00 |
| S13/run_0_accelerates_into_gap | 44 -> 2 | 1/1 -> 2/2 | 1 -> 2 / 2 | yes | A->B -0.05 |
| S13/run_0_cut_in | 6 -> 2 | 1/1 -> 2/2 | 1 -> 2 / 2 | yes | A->B -0.10 |
| S13/run_0_safe_lane_change | 1 -> 2 | 0/0 -> 0/0 | 0 -> 0 / 0 | yes | - |
| S15/run_0_b_stops | 6 -> 6 | 0/0 -> 0/0 | 0 -> 0 / 0 | yes | A->B +0.10, A->C -0.05, B->A +0.00, C->A -0.05 |
| S15/run_0_deflected_into_c | 12 -> 6 | 4/4 -> 4/4 | 4 -> 4 / 4 | yes | A->B +0.10, A->C -0.05, B->A -0.05, C->A -0.05 |
| S15/run_0_single_impact | 10 -> 7 | 2/2 -> 2/2 | 2 -> 2 / 2 | yes | A->B +0.10, A->C -0.05, B->A -0.05 |
| S16/run_0_avoided | 1 -> 4 | 1/1 -> 2/2 | 1 -> 2 / 2 | yes | B->A +0.00 |
| S16/run_0_consequential | 7 -> 4 | 1/1 -> 3/3 | 2 -> 3 / 4 | yes | B->A +0.00 |
| S16/run_0_independent | 5 -> 7 | 2/2 -> 2/2 | 2 -> 4 / 4 | yes | A->C +0.50, B->A +0.00 |

What the coverage changes:

- Tracking behind and beside. Of the 108 (recorder, other vehicle) pairs the privileged radar audit follows,
  37 never got a confirmed track with the 200-degree radar (28 because the vehicle stayed outside the field of
  view, mostly behind); with 360 degrees 6 remain. All 6 are vehicles standing still or slow, whose returns
  are static by design and cannot start a track. 33 pairs gained a track and 2 lost one: S15 deflected_into_c
  B->C and S16 consequential A->C. The first confirmation comes a median of 0.1 s later: fewer returns per
  target in front at range.
- Rear-end partners are now seen by the vehicle that is struck. Every recorder tracks its partner in 25 of
  the 27 contacts (52 of 54 recorder-contact slots), against 38 of 54. Identity claims rose from 34 to 49, all
  correct. Examples: B identifies A behind it in S01, S02, S06 and S16. TRACK_APPEARED_REAR occurs 24 times.
- No ghost tracks. The 200-degree campaign had 187 tracks lying on no vehicle: static scenery that looked
  like it was moving, mostly after impacts and in stop-and-go. With the radar's own motion taken from its
  displacement there are none, and every one of the 110 tracks lies on a vehicle. Anonymous tracks fall from
  229 to 61, mostly pairs that never collide and so cannot be named. The CUT_IN starts the former ghost
  tracks produced disappear: S10 and S11 stops_then_proceeds, S12 b_arrives_first. The real cut-ins of S02
  and S13 remain.
- New CRITICAL_TTC pairs come from the wider view: in S06 A on C over B's roof, B on A in S13
  accelerates_into_gap. Shared pairs start within +-0.15 s, apart from S08 C->B (-0.75 s) and S16
  independent A->C (+0.5 s). S09 loses its former CUT_IN_FROM_RIGHT on the merging B: when B's lateral
  approach qualifies, its tracked point is already beside A's front, not ahead of its front edge.
- Collision times are unchanged in 31 runs. In S06 a_front_pushed the re-recorded physics differ: B meets C
  at 6.05 s instead of 6.15 s, and A rebounds into B. Alignment stays exact (0.0 s errors) and all 27
  vehicle contacts are reconstructed, as before.

## 7. Anomalies and limitations

- CARLA cannot make one radar 360 degrees wide (section 1.1): the surround sensor is six physical radars
  merged at recording time.
- A single absolute mount height was not usable (roofs 1.39-2.57 m): the mount is 0.30 m above each
  vehicle's own roof (1.69-2.87 m).
- Points per second are 21600, not about 10800 (section 1.2): with the vertical FOV raised to 30 deg,
  10800 left a car 25-40 m away 3-4x fewer returns than the former radar. Radar data grew from 80 MB
  to 226 MB (`traces/` from 153 MB to 290 MB).
- Tall vehicles see low cars close by from far above. The patrol (radar 2.16 m) does not see an audi.tt
  within about 1 m beside it; the Sprinter (2.87 m) does not see low cars within 4 m beside or behind it.
  In S16 the Sprinter C does not track A at A's impact (consequential: last observed 0.75 s before, still
  associated through the 1 s window; independent: not tracked). Their own roofs return 4.5 and 14.5 rays per sweep,
  which are dropped.
- Clearance at contact: the near surface seen from a roof is the target's upper body. The median error at
  the contact is 0.53 m (90 % 1.22 m), against true gaps of about 0. Two chain-collision cases are much
  worse because the radar looks over a low car (audi.tt) onto the taller vehicle touching it, whose returns
  the track follows: S06 b_rear_first A->B 4.75 m (B stands against C), S06 a_front_pushed C->B 3.80 m.
- CARLA physics are not reproducible between recordings. The new S06 a_front_pushed has an A-B rebound with
  0.52 of the first impulse, above the former 0.5 threshold. Collision segmentation therefore became
  three-tier (section 2). It agrees with ground truth in all 15 bursts after a short break in the new
  recordings and in all 13 in the former ones.
- S14 was requested but does not exist: it was removed in `cfb4b87`.
- S07 occluded and full_view now differ only by A's radar range (100 vs 90 m): the former narrow-FOV
  profile also has the surround geometry, as already decided for 200 deg.
- `scripts/validate_observations.py` (radar vs depth camera) now compares a roof-centre radar with a front
  camera. Its agreement figures are not comparable with earlier ones; it is not part of the reconstruction.

## 8. Global event sequences

Aligned runs: global time, 0 = reference collision. Unaligned runs: each recorder's local sequence in its own clock (`*` = already active at the first observation).

**S01/run_0_avoided** (global graph, unaligned nodes: 23)

```
(no reference collision: graphs unaligned; local sequences in each recorder's own clock)
A: 0.00 MOVING_START*; 0.00 TRACK_APPEARED_FRONT(track_001); 0.45 CLOSING_START(track_001); 1.65 CLOSING_END(track_001); 4.20 CLOSING_START(track_001); 5.00 CRITICAL_TTC_START(track_001); 5.05 BRAKE_START; 6.25 CRITICAL_TTC_END(track_001); 6.35 CLOSING_END(track_001); 6.35 MOVING_END; 6.35 STOP_START
B: 0.00 MOVING_START*; 0.00 TRACK_APPEARED_REAR(track_001); 0.50 CLOSING_START(track_001); 1.65 CLOSING_END(track_001); 3.95 BRAKE_START; 4.25 CLOSING_START(track_001); 5.15 MOVING_END; 5.15 STOP_START; 6.40 CLOSING_END(track_001); 11.95 BRAKE_END; 12.35 STOP_END; 12.35 MOVING_START
```

**S01/run_0_crash** (global graph)

```
-6.50 MOVING_START(A); MOVING_START(B); TRACK_APPEARED_FRONT(A,B); TRACK_APPEARED_REAR(B,A)
-6.05 CLOSING_START(A,B)
-6.00 CLOSING_START(B,A)
-4.85 CLOSING_END(A,B); CLOSING_END(B,A)
-2.55 BRAKE_START(B)
-2.30 CLOSING_START(A,B)
-2.25 CLOSING_START(B,A)
-1.50 CRITICAL_TTC_START(A,B)
-1.35 MOVING_END(B); STOP_START(B)
-0.95 BRAKE_START(A)
-0.05 TRACK_LOST(B,A)
+0.00 COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B)
+0.05 MOVING_END(A); STOP_START(A)
```

**S02/run_0_avoided** (global graph, unaligned nodes: 15)

```
(no reference collision: graphs unaligned; local sequences in each recorder's own clock)
A: 0.00 MOVING_START*; 0.00 TRACK_APPEARED_LEFT(track_001); 0.00 CLOSING_START(track_001)*; 2.40 CUT_IN_FROM_LEFT_START(track_001); 2.85 BRAKE_START; 3.30 EGO_PATH_ENTRY(track_001); 4.05 CLOSING_END(track_001); 4.10 BRAKE_END; 5.25 CUT_IN_FROM_LEFT_END(track_001)
B: 0.00 MOVING_START*; 0.00 TRACK_APPEARED_RIGHT(track_001); 0.00 CLOSING_START(track_001)*; 3.15 BRAKE_START; 3.60 BRAKE_END; 4.05 CLOSING_END(track_001)
```

**S02/run_0_crash** (global graph)

```
-4.25 MOVING_START(A); MOVING_START(B); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_RIGHT(B,A); CLOSING_START(A,B); CLOSING_START(B,A)
-1.85 CUT_IN_FROM_LEFT_START(A,B)
-1.15 CRITICAL_TTC_START(A,B)
-1.10 BRAKE_START(B)
-0.90 EGO_PATH_ENTRY(A,B)
-0.65 BRAKE_END(B)
-0.40 BRAKE_START(A)
+0.00 COLLISION(A,B); CLOSING_END(B,A); BRAKE_START(B)
+0.05 CRITICAL_TTC_END(A,B); CLOSING_END(A,B)
+0.60 MOVING_END(A); STOP_START(A)
+0.75 MOVING_END(B); STOP_START(B)
+0.95 CUT_IN_FROM_LEFT_END(A,B)
```

**S02/run_0_critical_before_cut_in** (global graph)

```
-3.90 MOVING_START(A); MOVING_START(B); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_RIGHT(B,A); CLOSING_START(A,B); CLOSING_START(B,A)
-3.10 CRITICAL_TTC_START(A,B)
-2.40 BRAKE_START(B)
-2.25 BRAKE_END(B)
-1.45 BRAKE_START(A)
-1.30 CUT_IN_FROM_LEFT_START(A,B)
-0.70 BRAKE_END(A)
+0.00 COLLISION(A,B); CUT_IN_FROM_LEFT_END(A,B)
+0.05 CRITICAL_TTC_END(A,B); CLOSING_END(A,B); CLOSING_END(B,A); BRAKE_START(A); BRAKE_START(B)
+0.50 MOVING_END(B); STOP_START(B)
+0.55 MOVING_END(A); STOP_START(A)
```

**S03/run_0_crash** (global graph)

```
-4.25 MOVING_START(A); MOVING_START(B)
-3.00 TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B)
-2.95 TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A)
-1.90 CRITICAL_TTC_START(B,A)
-1.80 CRITICAL_TTC_START(A,B)
-0.05 TRACK_LOST(A,B)
+0.00 COLLISION(A,B); EGO_PATH_ENTRY(B,A)
+0.05 BRAKE_START(A); BRAKE_START(B)
+0.25 CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
+0.30 MOVING_END(B); STOP_START(B)
+0.65 MOVING_END(A); STOP_START(A)
```

**S05/run_0_crash** (global graph)

```
-3.70 MOVING_START(A); MOVING_START(B)
-3.15 TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A)
-3.00 TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B)
-2.05 CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A)
-0.25 EGO_PATH_ENTRY(A,B)
+0.00 COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B); TURN_LEFT_START(B)
+0.05 CRITICAL_TTC_END(B,A); CLOSING_END(B,A); BRAKE_START(A); BRAKE_START(B)
+0.10 EGO_PATH_EXIT(A,B)
+0.55 TURN_LEFT_END(B)
+0.60 MOVING_END(B); STOP_START(B)
+0.85 MOVING_END(A); STOP_START(A)
```

**S06/run_0_a_front_pushed** (global graph)

```
-5.90 MOVING_START(A); MOVING_START(B); MOVING_START(C); TRACK_APPEARED_FRONT(A,B); TRACK_APPEARED_FRONT(B,C); TRACK_APPEARED_REAR(B,A); TRACK_APPEARED_REAR(C,C:track_001); TRACK_APPEARED_REAR(C,C:track_002)
-5.45 CLOSING_START(A,B)
-5.40 CLOSING_START(B,A)
-5.10 CLOSING_START(C,C:track_001)
-4.90 TRACK_APPEARED_FRONT(A,A:track_002); CLOSING_START(A,A:track_002)
-4.85 CLOSING_START(B,C); CLOSING_START(C,C:track_002)
-4.25 CLOSING_END(A,B); CLOSING_END(B,A)
-3.95 CLOSING_END(A,A:track_002); CLOSING_END(C,C:track_001)
-3.85 CLOSING_END(B,C); CLOSING_END(C,C:track_002)
-3.50 SPEED_LIMIT_EXCEEDED_START(C)
-2.95 BRAKE_START(C)
-2.90 TRACK_LOST(C,C:track_001)
-2.85 SPEED_LIMIT_EXCEEDED_END(C)
-2.70 CLOSING_START(B,C)
-2.65 CLOSING_START(A,A:track_002)
-2.60 CLOSING_START(C,C:track_002)
-2.20 BRAKE_START(B)
-2.15 CRITICAL_TTC_START(B,C)
-1.95 CLOSING_START(B,A)
-1.90 CLOSING_START(A,B)
-1.85 MOVING_END(C); STOP_START(C)
-1.75 CRITICAL_TTC_START(A,A:track_002)
-1.30 TRACK_APPEARED_REAR(C,C:track_003); CLOSING_START(C,C:track_003)
-1.20 CRITICAL_TTC_START(A,B)
-1.00 CRITICAL_TTC_END(B,C); CLOSING_END(B,C); CLOSING_END(C,C:track_002); MOVING_END(B); STOP_START(B)
-0.35 BRAKE_START(A)
-0.20 BRAKE_END(B)
-0.05 TRACK_LOST(B,A); TRACK_LOST(C,C:track_003)
+0.00 COLLISION(A,B); STOP_END(B); MOVING_START(B)
+0.15 COLLISION(B,C)
+0.20 CRITICAL_TTC_END(A,A:track_002); CRITICAL_TTC_END(A,B); CLOSING_END(A,A:track_002); CLOSING_END(A,B)
+0.25 MOVING_END(A); MOVING_END(B); STOP_START(A); STOP_START(B)
```

**S06/run_0_b_rear_first** (global graph)

```
-6.00 MOVING_START(A); MOVING_START(B); MOVING_START(C); TRACK_APPEARED_FRONT(A,A:track_001); TRACK_APPEARED_FRONT(B,C); TRACK_APPEARED_REAR(B,A); TRACK_APPEARED_REAR(C,B); TRACK_APPEARED_REAR(C,C:track_001)
-5.55 CLOSING_START(A,A:track_001)
-5.50 CLOSING_START(B,A)
-5.20 CLOSING_START(C,C:track_001)
-4.95 CLOSING_START(C,B)
-4.90 CLOSING_START(B,C)
-4.85 TRACK_APPEARED_FRONT(A,A:track_002); CLOSING_START(A,A:track_002)
-4.35 CLOSING_END(A,A:track_001); CLOSING_END(B,A)
-4.00 CLOSING_END(A,A:track_002); CLOSING_END(C,C:track_001)
-3.95 CLOSING_END(C,B)
-3.90 CLOSING_END(B,C)
-3.60 SPEED_LIMIT_EXCEEDED_START(C)
-3.05 BRAKE_START(C); TRACK_LOST(C,C:track_001)
-2.95 SPEED_LIMIT_EXCEEDED_END(C)
-2.80 CLOSING_START(B,C)
-2.75 CLOSING_START(A,A:track_002); CLOSING_START(C,B)
-2.25 CRITICAL_TTC_START(B,C)
-1.95 MOVING_END(C); STOP_START(C)
-1.85 CRITICAL_TTC_START(A,A:track_002)
-1.45 TRACK_LOST(A,A:track_001); TRACK_LOST(C,B)
-1.40 COLLISION(B,C); CRITICAL_TTC_END(B,C); CLOSING_END(B,C); CLOSING_START(B,A)
-1.35 BRAKE_START(B)
-1.25 MOVING_END(B); STOP_START(B)
-0.80 TRACK_APPEARED_REAR(C,C:track_003); CLOSING_START(C,C:track_003)
-0.05 TRACK_LOST(B,A); TRACK_LOST(C,C:track_003)
+0.00 COLLISION(A,B); CRITICAL_TTC_END(A,A:track_002); CLOSING_END(A,A:track_002)
+0.05 BRAKE_START(A)
+0.20 MOVING_END(A); STOP_START(A)
```

**S07/run_0_full_view** (global graph, unaligned nodes: 17)

```
-5.70 MOVING_START(A); MOVING_START(B); TRACK_APPEARED_FRONT(A,B); TRACK_APPEARED_FRONT(B,B:track_001); TRACK_APPEARED_REAR(B,A)
-5.25 CLOSING_START(A,B)
-5.20 CLOSING_START(B,A)
-4.65 TRACK_APPEARED_FRONT(A,A:track_002); CLOSING_START(A,A:track_002)
-4.60 CLOSING_START(B,B:track_001)
-4.05 CLOSING_END(A,B); CLOSING_END(B,A)
-3.70 CLOSING_END(A,A:track_002)
-3.60 CLOSING_END(B,B:track_001)
-2.50 CLOSING_START(B,B:track_001)
-2.45 CLOSING_START(A,A:track_002)
-2.15 TRACK_LOST(A,A:track_002)
-2.05 BRAKE_START(B)
-1.80 CLOSING_START(A,B); CLOSING_START(B,A)
-1.75 CRITICAL_TTC_START(B,B:track_001)
-1.10 CRITICAL_TTC_END(B,B:track_001); CRITICAL_TTC_START(A,B)
-0.85 CLOSING_END(B,B:track_001); MOVING_END(B); STOP_START(B)
-0.05 TRACK_LOST(B,A)
+0.00 COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B)
+0.05 BRAKE_START(A)
+0.15 MOVING_END(A); STOP_START(A)
+8.05 TRACK_APPEARED_FRONT(A,A:track_003)
+8.40 TRACK_LOST(A,A:track_003)
```

**S07/run_0_occluded** (global graph, unaligned nodes: 17)

```
-5.70 MOVING_START(A); MOVING_START(B); TRACK_APPEARED_FRONT(A,B); TRACK_APPEARED_FRONT(B,B:track_001); TRACK_APPEARED_REAR(B,A)
-5.25 CLOSING_START(A,B)
-5.20 CLOSING_START(B,A)
-4.65 TRACK_APPEARED_FRONT(A,A:track_002); CLOSING_START(A,A:track_002)
-4.60 CLOSING_START(B,B:track_001)
-4.05 CLOSING_END(A,B); CLOSING_END(B,A)
-3.70 CLOSING_END(A,A:track_002)
-3.60 CLOSING_END(B,B:track_001)
-2.50 CLOSING_START(B,B:track_001)
-2.45 CLOSING_START(A,A:track_002)
-2.15 TRACK_LOST(A,A:track_002)
-2.05 BRAKE_START(B)
-1.80 CLOSING_START(A,B); CLOSING_START(B,A)
-1.75 CRITICAL_TTC_START(B,B:track_001)
-1.10 CRITICAL_TTC_END(B,B:track_001); CRITICAL_TTC_START(A,B)
-0.85 CLOSING_END(B,B:track_001); MOVING_END(B); STOP_START(B)
-0.05 TRACK_LOST(B,A)
+0.00 COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B)
+0.05 BRAKE_START(A)
+0.15 MOVING_END(A); STOP_START(A)
+8.05 TRACK_APPEARED_FRONT(A,A:track_003)
+8.40 TRACK_LOST(A,A:track_003)
```

**S08/run_0_crash** (global graph, unaligned nodes: 17)

```
-4.25 MOVING_START(A); MOVING_START(B)
-4.20 TRACK_APPEARED_FRONT(A,A:track_001); CLOSING_START(A,A:track_001)
-3.00 TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B)
-2.95 TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A)
-2.10 TRACK_APPEARED_RIGHT(B,B:track_002); CLOSING_START(B,B:track_002)
-2.05 CRITICAL_TTC_START(A,A:track_001)
-1.90 CRITICAL_TTC_START(B,A)
-1.80 CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,B:track_002)
-1.50 CRITICAL_TTC_END(A,A:track_001)
-0.75 CRITICAL_TTC_START(A,A:track_001)
-0.05 TRACK_LOST(A,B)
+0.00 COLLISION(A,B); CRITICAL_TTC_END(B,B:track_002); EGO_PATH_ENTRY(B,A)
+0.05 BRAKE_START(A); BRAKE_START(B)
+0.25 CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
+0.30 CLOSING_END(B,B:track_002); MOVING_END(B); STOP_START(B)
+0.50 CRITICAL_TTC_END(A,A:track_001)
+0.65 CLOSING_END(A,A:track_001); MOVING_END(A); STOP_START(A)
```

**S09/run_0_merge_conflict** (global graph)

```
-1.80 MOVING_START(A); MOVING_START(B); TURN_LEFT_START(A); TURN_RIGHT_START(B); TRACK_APPEARED_LEFT(B,A); TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B); CLOSING_START(B,A); CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A)
-0.95 CRITICAL_TTC_END(B,A)
-0.60 TURN_RIGHT_END(B)
-0.35 CRITICAL_TTC_START(B,A)
-0.15 CRITICAL_TTC_END(A,B)
+0.00 COLLISION(A,B); CRITICAL_TTC_END(B,A); CLOSING_END(A,B); CLOSING_END(B,A)
+0.05 BRAKE_START(A); BRAKE_START(B); TURN_LEFT_START(B)
+0.65 TURN_LEFT_END(A)
+0.70 TURN_LEFT_END(B); MOVING_END(A); STOP_START(A)
+0.75 MOVING_END(B); STOP_START(B)
```

**S10/run_0_rolls_through** (global graph)

```
-5.25 MOVING_START(A); MOVING_START(B)
-3.40 STOP_SIGN_DETECTED_START(A,A:sign-0)
-3.30 BRAKE_START(A)
-3.10 STOP_SIGN_DETECTED_END(A,A:sign-0)
-2.55 TURN_LEFT_START(A); TRACK_APPEARED_RIGHT(B,A); CLOSING_START(B,A)
-2.50 TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B)
-1.70 CRITICAL_TTC_START(B,A)
-1.45 BRAKE_END(A); CRITICAL_TTC_START(A,B)
-0.30 EGO_PATH_ENTRY(B,A)
-0.05 TRACK_LOST(A,B)
+0.00 COLLISION(A,B)
+0.05 TURN_LEFT_END(A); BRAKE_START(A); BRAKE_START(B)
+0.10 MOVING_END(B); STOP_START(B)
+0.15 CRITICAL_TTC_END(B,A); CLOSING_END(B,A); MOVING_END(A); STOP_START(A)
```

**S10/run_0_stops_safely** (global graph, unaligned nodes: 20)

```
(no reference collision: graphs unaligned; local sequences in each recorder's own clock)
A: 0.00 MOVING_START*; 1.85 STOP_SIGN_DETECTED_START(sign-0); 2.15 STOP_SIGN_DETECTED_END(sign-0); 2.55 BRAKE_START; 2.65 TRACK_APPEARED_LEFT(track_001); 2.65 CLOSING_START(track_001)*; 3.35 MOVING_END; 3.35 STOP_START; 5.80 EGO_PATH_ENTRY(track_001); 6.15 CLOSING_END(track_001); 6.25 EGO_PATH_EXIT(track_001); 9.45 TRACK_LOST(track_001)
B: 0.00 MOVING_START*; 2.60 TRACK_APPEARED_RIGHT(track_001); 2.60 CLOSING_START(track_001)*; 4.25 CRITICAL_TTC_START(track_001); 5.95 CRITICAL_TTC_END(track_001); 6.15 CLOSING_END(track_001); 7.60 STOP_SIGN_DETECTED_START(sign-0); 7.80 STOP_SIGN_DETECTED_END(sign-0)
```

**S10/run_0_stops_then_proceeds** (global graph, unaligned nodes: 26)

```
(no reference collision: graphs unaligned; local sequences in each recorder's own clock)
A: 0.00 MOVING_START*; 1.85 STOP_SIGN_DETECTED_START(sign-0); 2.15 STOP_SIGN_DETECTED_END(sign-0); 2.55 BRAKE_START; 2.65 TRACK_APPEARED_LEFT(track_001); 2.65 CLOSING_START(track_001)*; 3.35 MOVING_END; 3.35 STOP_START; 5.80 EGO_PATH_ENTRY(track_001); 6.15 CLOSING_END(track_001); 6.25 EGO_PATH_EXIT(track_001); 6.75 BRAKE_END; 7.10 STOP_END; 7.10 MOVING_START; 7.65 TURN_LEFT_START; 10.30 TURN_LEFT_END; 11.60 TRACK_LOST(track_001)
B: 0.00 MOVING_START*; 2.60 TRACK_APPEARED_RIGHT(track_001); 2.60 CLOSING_START(track_001)*; 4.25 CRITICAL_TTC_START(track_001); 5.95 CRITICAL_TTC_END(track_001); 6.15 CLOSING_END(track_001); 7.70 STOP_SIGN_DETECTED_START(sign-0); 7.70 STOP_SIGN_DETECTED_END(sign-0); 11.95 TRACK_LOST(track_001)
```

**S11/run_0_rolls_through** (global graph)

```
-5.50 MOVING_START(A); MOVING_START(B)
-3.55 BRAKE_START(B)
-3.40 STOP_SIGN_DETECTED_START(B,B:sign-1)
-3.00 STOP_SIGN_DETECTED_END(B,B:sign-1)
-2.85 BRAKE_END(B)
-2.55 TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B)
-2.50 TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A)
-1.75 CRITICAL_TTC_START(A,B)
-1.70 TURN_LEFT_START(B)
-1.45 CRITICAL_TTC_START(B,A)
-0.15 EGO_PATH_ENTRY(B,A)
-0.05 TRACK_LOST(A,B)
+0.00 COLLISION(A,B); TURN_LEFT_END(B)
+0.05 BRAKE_START(A); BRAKE_START(B)
+0.20 MOVING_END(B); STOP_START(B)
+0.40 CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
+0.55 MOVING_END(A); STOP_START(A)
```

**S11/run_0_stops_safely** (global graph, unaligned nodes: 18)

```
(no reference collision: graphs unaligned; local sequences in each recorder's own clock)
A: 0.00 MOVING_START*; 2.65 TRACK_APPEARED_RIGHT(track_001); 2.65 CLOSING_START(track_001)*; 4.40 CRITICAL_TTC_START(track_001); 5.65 CRITICAL_TTC_END(track_001); 6.05 CLOSING_END(track_001); 9.50 TRACK_LOST(track_001)
B: 0.00 MOVING_START*; 2.00 STOP_SIGN_DETECTED_START(sign-1); 2.40 STOP_SIGN_DETECTED_END(sign-1); 2.55 BRAKE_START; 2.75 TRACK_APPEARED_LEFT(track_001); 2.75 CLOSING_START(track_001)*; 3.25 MOVING_END; 3.25 STOP_START; 5.80 EGO_PATH_ENTRY(track_001); 6.10 CLOSING_END(track_001); 6.20 EGO_PATH_EXIT(track_001)
```

**S11/run_0_stops_then_proceeds** (global graph, unaligned nodes: 24)

```
(no reference collision: graphs unaligned; local sequences in each recorder's own clock)
A: 0.00 MOVING_START*; 2.65 TRACK_APPEARED_RIGHT(track_001); 2.65 CLOSING_START(track_001)*; 4.40 CRITICAL_TTC_START(track_001); 5.65 CRITICAL_TTC_END(track_001); 6.10 CLOSING_END(track_001); 12.10 TRACK_LOST(track_001)
B: 0.00 MOVING_START*; 2.00 STOP_SIGN_DETECTED_START(sign-1); 2.35 STOP_SIGN_DETECTED_END(sign-1); 2.55 BRAKE_START; 2.75 TRACK_APPEARED_LEFT(track_001); 2.75 CLOSING_START(track_001)*; 3.25 MOVING_END; 3.25 STOP_START; 5.80 EGO_PATH_ENTRY(track_001); 6.10 CLOSING_END(track_001); 6.20 EGO_PATH_EXIT(track_001); 6.75 BRAKE_END; 7.20 STOP_END; 7.20 MOVING_START; 7.95 TURN_LEFT_START; 10.70 TURN_LEFT_END; 12.05 TRACK_LOST(track_001)
```

**S12/run_0_a_arrives_first** (global graph, unaligned nodes: 36)

```
(no reference collision: graphs unaligned; local sequences in each recorder's own clock)
A: 0.00 MOVING_START*; 0.65 STOP_SIGN_DETECTED_START(sign-0); 2.25 STOP_SIGN_DETECTED_END(sign-0); 2.65 BRAKE_START; 3.20 TRACK_APPEARED_LEFT(track_001); 3.20 CLOSING_START(track_001)*; 3.40 MOVING_END; 3.40 STOP_START; 4.70 CLOSING_END(track_001); 6.45 BRAKE_END; 6.80 STOP_END; 6.80 MOVING_START; 6.95 CLOSING_START(track_001); 7.80 TURN_LEFT_START; 9.60 CRITICAL_TTC_START(track_001); 11.05 TURN_LEFT_END; 11.10 CRITICAL_TTC_END(track_001); 11.25 CLOSING_END(track_001); 15.55 TRACK_LOST(track_001)
B: 0.00 MOVING_START*; 2.10 STOP_SIGN_DETECTED_START(sign-0); 4.00 STOP_SIGN_DETECTED_END(sign-0); 4.35 BRAKE_START; 4.70 MOVING_END; 4.70 STOP_START; 6.95 TRACK_APPEARED_RIGHT(track_001); 6.95 CLOSING_START(track_001)*; 8.50 EGO_PATH_ENTRY(track_001); 9.05 EGO_PATH_EXIT(track_001); 10.45 BRAKE_END; 10.55 CRITICAL_TTC_START(track_001); 10.85 STOP_END; 10.85 MOVING_START; 11.10 CRITICAL_TTC_END(track_001); 11.30 CLOSING_END(track_001); 16.20 TRACK_LOST(track_001)
```

**S12/run_0_b_arrives_first** (global graph, unaligned nodes: 32)

```
(no reference collision: graphs unaligned; local sequences in each recorder's own clock)
A: 0.00 MOVING_START*; 0.95 STOP_SIGN_DETECTED_START(sign-0); 3.55 STOP_SIGN_DETECTED_END(sign-0); 4.35 BRAKE_START; 4.75 MOVING_END; 4.75 STOP_START; 6.90 TRACK_APPEARED_LEFT(track_001); 6.90 CLOSING_START(track_001)*; 9.75 EGO_PATH_ENTRY(track_001); 9.90 CLOSING_END(track_001); 10.20 EGO_PATH_EXIT(track_001); 10.45 BRAKE_END; 10.80 STOP_END; 10.80 MOVING_START; 12.10 TURN_LEFT_START; 15.30 TURN_LEFT_END; 16.20 TRACK_LOST(track_001)
B: 0.00 MOVING_START*; 1.80 STOP_SIGN_DETECTED_START(sign-0); 2.60 STOP_SIGN_DETECTED_END(sign-0); 2.65 BRAKE_START; 3.35 TRACK_APPEARED_RIGHT(track_001); 3.35 CLOSING_START(track_001)*; 3.40 MOVING_END; 3.40 STOP_START; 4.70 CLOSING_END(track_001); 6.45 BRAKE_END; 6.85 STOP_END; 6.85 MOVING_START; 6.90 CLOSING_START(track_001); 9.85 CLOSING_END(track_001); 15.85 TRACK_LOST(track_001)
```

**S12/run_0_b_fails_to_stop** (global graph)

```
-9.70 MOVING_START(A); MOVING_START(B)
-9.05 STOP_SIGN_DETECTED_START(A,A:sign-0)
-7.75 BRAKE_START(B)
-7.45 STOP_SIGN_DETECTED_END(A,A:sign-0)
-7.05 BRAKE_END(B); BRAKE_START(A)
-6.30 MOVING_END(A); STOP_START(A)
-6.20 STOP_SIGN_DETECTED_START(B,B:sign-1)
-5.45 TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B)
-4.40 STOP_SIGN_DETECTED_END(B,B:sign-1)
-1.95 BRAKE_END(A)
-1.60 STOP_END(A); MOVING_START(A)
-1.55 TRACK_APPEARED_RIGHT(B,A); CLOSING_START(B,A)
-1.10 CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A)
-0.60 TURN_LEFT_START(A)
-0.05 TRACK_LOST(A,B)
+0.00 COLLISION(A,B)
+0.05 BRAKE_START(A); BRAKE_START(B)
+0.10 TURN_LEFT_END(A)
+0.35 CRITICAL_TTC_END(B,A); MOVING_END(B); STOP_START(B)
+0.45 CLOSING_END(B,A); EGO_PATH_ENTRY(B,A)
+0.50 MOVING_END(A); STOP_START(A)
```

**S12/run_0_near_simultaneous** (global graph)

```
-9.50 MOVING_START(A); MOVING_START(B)
-8.85 STOP_SIGN_DETECTED_START(A,A:sign-0)
-7.70 STOP_SIGN_DETECTED_START(B,B:sign-0)
-7.25 STOP_SIGN_DETECTED_END(A,A:sign-0)
-6.90 STOP_SIGN_DETECTED_END(B,B:sign-0); TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B)
-6.85 BRAKE_START(A)
-6.75 BRAKE_START(B)
-6.70 TRACK_APPEARED_RIGHT(B,A); CLOSING_START(B,A)
-6.10 MOVING_END(A); STOP_START(A)
-6.05 CLOSING_END(B,A)
-6.00 CLOSING_END(A,B); MOVING_END(B); STOP_START(B)
-2.55 BRAKE_END(A); BRAKE_END(B)
-2.20 STOP_END(A); MOVING_START(A); CLOSING_START(A,B); CLOSING_START(B,A)
-2.15 STOP_END(B); MOVING_START(B)
-1.25 CRITICAL_TTC_START(A,B)
-1.20 TURN_LEFT_START(A); CRITICAL_TTC_START(B,A)
-0.55 EGO_PATH_ENTRY(B,A)
+0.00 COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B); EGO_PATH_EXIT(B,A)
+0.05 CRITICAL_TTC_END(B,A); CLOSING_END(B,A); BRAKE_START(A); BRAKE_START(B)
+0.45 MOVING_END(B); STOP_START(B)
+0.50 TURN_LEFT_END(A); MOVING_END(A); STOP_START(A)
+1.45 STOP_SIGN_DETECTED_START(A,A:sign-1)
```

**S13/run_0_accelerates_into_gap** (global graph)

```
-5.65 MOVING_START(A); MOVING_START(B)
-4.85 BRAKE_START(B)
-2.90 SPEED_LIMIT_EXCEEDED_START(A); TRACK_APPEARED_RIGHT(B,A); CLOSING_START(B,A)
-2.25 TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B)
-1.70 CRITICAL_TTC_START(A,B)
-1.50 CUT_IN_FROM_LEFT_START(A,B)
-0.20 EGO_PATH_ENTRY(A,B)
+0.00 COLLISION(A,B); CLOSING_END(B,A); SPEED_LIMIT_EXCEEDED_END(A)
+0.05 BRAKE_START(A)
+0.10 TURN_RIGHT_START(B)
+0.15 CRITICAL_TTC_END(A,B); CLOSING_END(A,B)
+0.90 CLOSING_START(A,B); CLOSING_START(B,A); CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A)
+1.20 CRITICAL_TTC_END(A,B); CLOSING_END(A,B)
+1.25 CRITICAL_TTC_END(B,A); TURN_RIGHT_END(B); MOVING_END(B); STOP_START(B)
+1.30 CLOSING_END(B,A); MOVING_END(A); STOP_START(A)
+1.40 CUT_IN_FROM_LEFT_END(A,B)
```

**S13/run_0_cut_in** (global graph)

```
-5.25 MOVING_START(A); MOVING_START(B); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_RIGHT(B,A); CLOSING_START(A,B); CLOSING_START(B,A)
-4.45 BRAKE_START(B)
-2.40 BRAKE_START(A)
-1.40 CRITICAL_TTC_START(A,B)
-1.25 CUT_IN_FROM_LEFT_START(A,B)
-0.25 EGO_PATH_ENTRY(A,B)
+0.00 COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B); CLOSING_END(B,A)
+0.20 TURN_RIGHT_START(B)
+1.15 TURN_RIGHT_END(B); MOVING_END(A); STOP_START(A)
+1.20 MOVING_END(B); STOP_START(B)
+1.60 CUT_IN_FROM_LEFT_END(A,B)
```

**S13/run_0_safe_lane_change** (global graph, unaligned nodes: 14)

```
(no reference collision: graphs unaligned; local sequences in each recorder's own clock)
A: 0.00 MOVING_START*; 0.00 TRACK_APPEARED_LEFT(track_001); 0.00 CLOSING_START(track_001)*; 1.50 CLOSING_END(track_001); 2.35 CLOSING_START(track_001); 2.85 BRAKE_START; 4.25 CUT_IN_FROM_LEFT_START(track_001); 5.45 EGO_PATH_ENTRY(track_001); 7.90 CUT_IN_FROM_LEFT_END(track_001)
B: 0.00 MOVING_START*; 0.00 TRACK_APPEARED_RIGHT(track_001); 0.00 CLOSING_START(track_001)*; 1.35 CLOSING_END(track_001); 2.60 CLOSING_START(track_001)
```

**S15/run_0_b_stops** (global graph, unaligned nodes: 49)

```
(no reference collision: graphs unaligned; local sequences in each recorder's own clock)
A: 0.00 MOVING_START*; 0.20 TRACK_APPEARED_FRONT(track_001); 0.20 CLOSING_START(track_001)*; 2.10 TRACK_APPEARED_RIGHT(track_002); 2.10 CLOSING_START(track_002)*; 2.10 CRITICAL_TTC_START(track_002)*; 2.50 CRITICAL_TTC_START(track_001); 4.20 CRITICAL_TTC_END(track_002); 4.25 CLOSING_END(track_002); 4.65 CRITICAL_TTC_END(track_001); 4.65 CLOSING_END(track_001); 9.55 TRACK_LOST(track_001); 10.40 TRACK_LOST(track_002)
B: 0.00 MOVING_START*; 1.45 STOP_SIGN_DETECTED_START(sign-0); 1.75 TRACK_APPEARED_RIGHT(track_001); 1.75 CLOSING_START(track_001)*; 2.05 STOP_SIGN_DETECTED_END(sign-0); 2.10 TRACK_APPEARED_LEFT(track_002); 2.10 CLOSING_START(track_002)*; 2.10 CRITICAL_TTC_START(track_002)*; 2.25 TURN_LEFT_START; 2.40 CRITICAL_TTC_START(track_001); 2.55 BRAKE_START; 2.80 CRITICAL_TTC_END(track_001); 3.35 TURN_LEFT_END; 3.40 MOVING_END; 3.40 STOP_START; 3.55 CRITICAL_TTC_END(track_002); 3.90 EGO_PATH_ENTRY(track_002); 4.00 STOP_SIGN_DETECTED_START(sign-1); 4.30 CLOSING_END(track_002); 4.35 EGO_PATH_EXIT(track_002); 5.25 CLOSING_END(track_001); 5.75 EGO_PATH_ENTRY(track_001); 6.40 EGO_PATH_EXIT(track_001); 7.90 STOP_SIGN_DETECTED_END(sign-1); 9.25 STOP_SIGN_DETECTED_START(sign-1); 9.85 TRACK_LOST(track_002)
C: 0.00 MOVING_START*; 0.05 TRACK_APPEARED_FRONT(track_001); 0.05 CLOSING_START(track_001)*; 0.35 TRACK_APPEARED_LEFT(track_002); 0.35 CLOSING_START(track_002)*; 2.85 CRITICAL_TTC_START(track_001); 4.70 CRITICAL_TTC_END(track_001); 4.70 CLOSING_END(track_001); 5.20 CLOSING_END(track_002); 10.20 TRACK_LOST(track_001)
```

**S15/run_0_deflected_into_c** (global graph)

```
-3.80 MOVING_START(A); MOVING_START(B); MOVING_START(C)
-3.75 TRACK_APPEARED_FRONT(C,A); CLOSING_START(C,A)
-3.60 TRACK_APPEARED_FRONT(A,C); CLOSING_START(A,C)
-3.45 TRACK_APPEARED_LEFT(C,C:track_002); CLOSING_START(C,C:track_002)
-2.05 TRACK_APPEARED_RIGHT(B,B:track_001); CLOSING_START(B,B:track_001)
-2.00 STOP_SIGN_DETECTED_START(B,B:sign-0)
-1.75 STOP_SIGN_DETECTED_END(B,B:sign-0)
-1.70 TRACK_APPEARED_LEFT(B,A); TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B); CLOSING_START(B,A); CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A)
-1.55 TURN_LEFT_START(B); CRITICAL_TTC_START(B,B:track_001)
-1.30 CRITICAL_TTC_START(A,C)
-0.95 CRITICAL_TTC_START(C,A)
-0.85 BRAKE_START(B)
-0.70 CRITICAL_TTC_END(B,B:track_001)
-0.30 BRAKE_END(B)
-0.15 EGO_PATH_ENTRY(B,A)
-0.05 TRACK_LOST(A,B)
+0.00 COLLISION(A,B); TURN_LEFT_END(B); TURN_LEFT_START(A)
+0.05 BRAKE_START(B); CRITICAL_TTC_START(B,B:track_001)
+0.20 MOVING_END(B); STOP_START(B)
+0.35 CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
+0.65 CRITICAL_TTC_END(B,B:track_001)
+0.75 STOP_SIGN_DETECTED_START(A,A:sign-0); STOP_SIGN_DETECTED_END(A,A:sign-0)
+0.85 EGO_PATH_ENTRY(A,C)
+0.90 EGO_PATH_EXIT(B,A)
+0.95 COLLISION(A,C)
+1.00 CLOSING_END(C,C:track_002); BRAKE_START(C)
+1.10 CLOSING_END(B,B:track_001)
+1.15 CRITICAL_TTC_END(C,A); CLOSING_END(C,A); TURN_LEFT_END(A)
+1.20 CRITICAL_TTC_END(A,C); CLOSING_END(A,C)
+1.25 MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C)
+1.45 STOP_SIGN_DETECTED_START(A,A:sign-2)
+3.00 TRACK_LOST(B,A)
+3.95 STOP_SIGN_DETECTED_END(A,A:sign-2)
+4.85 STOP_SIGN_DETECTED_START(A,A:sign-2); STOP_SIGN_DETECTED_END(A,A:sign-2)
+5.85 STOP_SIGN_DETECTED_START(A,A:sign-2)
```

**S15/run_0_single_impact** (global graph, unaligned nodes: 11)

```
-3.80 MOVING_START(A); MOVING_START(B)
-2.55 TRACK_APPEARED_FRONT(A,A:track_001); CLOSING_START(A,A:track_001)
-2.05 STOP_SIGN_DETECTED_START(B,B:sign-0)
-1.75 STOP_SIGN_DETECTED_END(B,B:sign-0)
-1.70 TRACK_APPEARED_LEFT(B,A); TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B); CLOSING_START(B,A); CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A)
-1.55 TURN_LEFT_START(B)
-0.90 TRACK_APPEARED_RIGHT(B,B:track_002)
-0.85 BRAKE_START(B)
-0.30 BRAKE_END(B)
-0.15 EGO_PATH_ENTRY(B,A)
-0.05 TRACK_LOST(A,B)
+0.00 COLLISION(A,B); TURN_LEFT_END(B); TURN_LEFT_START(A); EGO_PATH_ENTRY(A,A:track_001); CLOSING_START(B,B:track_002)
+0.05 EGO_PATH_EXIT(A,A:track_001); BRAKE_START(B)
+0.20 MOVING_END(B); STOP_START(B)
+0.25 EGO_PATH_ENTRY(A,A:track_001)
+0.35 CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
+0.50 EGO_PATH_EXIT(A,A:track_001)
+0.75 STOP_SIGN_DETECTED_START(A,A:sign-0)
+0.85 EGO_PATH_EXIT(B,A)
+1.25 STOP_SIGN_DETECTED_END(A,A:sign-0)
+1.40 TURN_LEFT_END(A)
+6.75 STOP_SIGN_DETECTED_START(A,A:sign-1)
+7.75 MOVING_END(A); STOP_START(A)
+9.60 CRITICAL_TTC_START(A,A:track_001)
```

**S16/run_0_avoided** (global graph, unaligned nodes: 9)

```
-5.15 MOVING_START(A); MOVING_START(B); TRACK_APPEARED_FRONT(B,A); TRACK_APPEARED_REAR(A,B)
-4.50 CLOSING_START(B,A)
-4.45 CLOSING_START(A,B)
-4.40 CRITICAL_TTC_START(B,A)
-3.75 CRITICAL_TTC_END(B,A); CLOSING_END(A,B); CLOSING_END(B,A)
-1.20 BRAKE_START(A)
-0.95 CLOSING_START(A,B)
-0.90 CLOSING_START(B,A)
-0.75 CRITICAL_TTC_START(B,A)
-0.40 BRAKE_START(B)
+0.00 COLLISION(A,B); CLOSING_END(A,B)
+0.05 CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
+0.45 MOVING_END(B); STOP_START(B)
+0.60 MOVING_END(A); STOP_START(A)
```

**S16/run_0_consequential** (global graph)

```
-5.15 MOVING_START(A); MOVING_START(B); MOVING_START(C); TRACK_APPEARED_FRONT(B,A); TRACK_APPEARED_REAR(A,B); TRACK_APPEARED_REAR(C,A); CLOSING_START(C,A)
-5.00 TRACK_APPEARED_REAR(C,C:track_002); CLOSING_START(C,C:track_002)
-4.85 MOVING_END(C); STOP_START(C)
-4.50 CLOSING_START(B,A)
-4.45 CLOSING_START(A,B)
-4.40 CRITICAL_TTC_START(B,A)
-3.75 CRITICAL_TTC_END(B,A); CLOSING_END(A,B); CLOSING_END(B,A)
-1.20 BRAKE_START(A)
-0.95 CLOSING_START(A,B)
-0.90 CLOSING_START(B,A)
-0.75 CRITICAL_TTC_START(B,A)
-0.40 BRAKE_START(B)
+0.00 COLLISION(A,B); CLOSING_END(A,B); TRACK_LOST(C,A)
+0.05 CRITICAL_TTC_END(B,A); CLOSING_END(B,A); BRAKE_END(A)
+0.25 TURN_LEFT_START(A)
+0.45 CLOSING_END(C,C:track_002); MOVING_END(B); STOP_START(B)
+0.75 COLLISION(A,C); STOP_END(C); MOVING_START(C)
+0.80 BRAKE_START(C)
+0.85 TURN_LEFT_END(A)
+0.90 MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C)
```

**S16/run_0_independent** (global graph)

```
-14.10 MOVING_START(A); MOVING_START(B); MOVING_START(C); TRACK_APPEARED_FRONT(B,A); TRACK_APPEARED_REAR(A,B)
-13.60 MOVING_END(C); STOP_START(C)
-13.45 CLOSING_START(B,A)
-13.40 CLOSING_START(A,B)
-13.35 CRITICAL_TTC_START(B,A)
-12.70 CRITICAL_TTC_END(B,A); CLOSING_END(A,B); CLOSING_END(B,A)
-10.65 TRACK_APPEARED_REAR(C,C:track_001); CLOSING_START(C,C:track_001)
-10.15 BRAKE_START(A)
-9.90 TRACK_APPEARED_RIGHT(C,C:track_002); CLOSING_START(A,B); CLOSING_START(B,A); CLOSING_START(C,C:track_002)
-9.70 CRITICAL_TTC_START(B,A)
-9.35 BRAKE_START(B)
-8.95 COLLISION(A,B); CLOSING_END(A,B)
-8.90 CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
-8.85 TRACK_LOST(C,C:track_002)
-8.50 CLOSING_END(C,C:track_001); MOVING_END(B); STOP_START(B)
-8.30 MOVING_END(A); STOP_START(A)
-3.15 BRAKE_END(A)
-2.70 STOP_END(A); MOVING_START(A)
-2.60 TRACK_APPEARED_RIGHT(C,C:track_003)
-2.35 CLOSING_START(C,C:track_003)
-2.15 STOP_END(C); MOVING_START(C); TRACK_APPEARED_LEFT(B,B:track_002)
-1.85 TRACK_LOST(C,C:track_003)
-0.95 TRACK_APPEARED_FRONT(A,A:track_002); CLOSING_START(A,A:track_002); CRITICAL_TTC_START(A,A:track_002)
-0.70 EGO_PATH_EXIT(B,A); STOP_SIGN_DETECTED_START(C,C:sign-3)
-0.50 STOP_SIGN_DETECTED_END(C,C:sign-3)
-0.05 TRACK_LOST(B,A); TRACK_LOST(C,C:track_001)
+0.00 COLLISION(A,C); CRITICAL_TTC_END(A,A:track_002); CLOSING_END(A,A:track_002); BRAKE_START(C)
+0.55 MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C)
+3.70 TRACK_LOST(A,B)
```
