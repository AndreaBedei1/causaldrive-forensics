"""Raw-evidence continuity, conservative reacquisition and the two S02 orders."""
import unittest
from pathlib import Path

import numpy as np

from src.cdf.common.config import load_run_config
from src.cdf.simulation.scenario_base import ScenarioSpec

from src.cdf.reconstruction.anonymous import CommonView
from src.cdf.reconstruction.identity import RelativePose, link_to_recorders_corrected
from src.cdf.reconstruction.common_frame import RecorderBody, RecordedPoseSource
from src.cdf.reconstruction.config import ReconstructionConfig, TrackingConfig
from src.cdf.reconstruction.local import reconstruct_vehicle
from src.cdf.reconstruction.pipeline import read_incident_context
from src.cdf.reconstruction.tracking import EgoFootprint, RadarSweep, TrackMeasurement, associate_returns, filter_and_smooth
from test_road_user_fusion import track, straight, following

ROOT = Path(__file__).resolve().parents[1]


class RawCompetitionTests(unittest.TestCase):
    def test_coherent_rival_returns_are_not_consumed_by_older_track(self):
        sweeps = []
        for i in range(80):
            t = i * .05
            y = max(3.0 - max(i - 15, 0) * .04, 1.5)
            vy = -.8 if 15 < i < 53 else 0.0
            groups = [np.column_stack([np.linspace(30+10*t-.2, 30+10*t+.2, 11),
                                        np.linspace(side*y-.65, side*y+.65, 11)]) for side in (-1,1)]
            points = np.concatenate(groups)
            lines = points / np.linalg.norm(points, axis=1)[:,None]
            velocities = np.concatenate([np.tile([10, side*vy], (11,1)) for side in (-1,1)])
            sweeps.append(RadarSweep(t, points, np.zeros_like(points), np.zeros(22, dtype=int),
                                    np.sum(lines*velocities,axis=1),np.linalg.norm(points,axis=1),
                                    np.linalg.norm(points,axis=1),radars=('front',)))
        tracks = associate_returns(sweeps, TrackingConfig())
        self.assertEqual(len(tracks),2)
        self.assertEqual([round(t.last_update_t,2) for t in tracks],[3.95,3.95])
        for tr, sign in zip(tracks,(-1,1)):
            for m in tr.measurements:
                if m.points is not None:
                    self.assertTrue(np.all(m.points[:,1]*sign>0), (tr.track_id,m.t_local,m.points))

    def test_unexpected_doppler_cannot_bend_the_earlier_trajectory(self):
        measurements=[]
        for i in range(70):
            t=i*.05
            x=10*t if i<40 else 20+2*(t-2)
            y=0 if i<40 else 4*(t-2)
            v=10 if i<40 else 2
            measurements.append(TrackMeasurement(t,np.array([x,y]),[(np.array([1.,0.]),v)],n_returns=10,
                                                 competing=(35 <= i <= 40)))
        smoothed,_,_=filter_and_smooth(measurements,TrackingConfig())
        self.assertLess(np.max(np.abs(smoothed[:40,1])),1e-6)
        self.assertLess(np.max(np.abs(smoothed[:40,3])),1e-6)
        self.assertGreater(smoothed[-1,1],4)


def link_to_recorders(view, cfg):
    links, _ = link_to_recorders_corrected(view, cfg, RelativePose({name: b.poses for name, b in view.bodies.items()}))
    return links


class ReacquisitionTests(unittest.TestCase):
    """A segment born after its candidate recorder's contact with a third body gets no recorder link from the
    radar geometry: identity is never inherited across that contamination boundary."""

    def view(self, rival_y=8.0):
        cfg=ReconstructionConfig()
        def body(name,y):
            rows=[dict(timestamp=i*.05,x=30+10*i*.05,y=y,yaw_deg=0,velocity=dict(x=10,y=0)) for i in range(80)]
            return RecorderBody(name,RecordedPoseSource(rows,0),EgoFootprint(-2.3,2.3,-.95,.95),0,
                                ((1.0,('R',)),) if name=='Q' else ())
        before=track('O','old#segment_1',[i*.05 for i in range(16)],straight(30,0,10),following(0,0,10))
        after=track('O','old#segment_3',[1.3+i*.05 for i in range(35)],straight(30,0,10),following(0,0,10))
        before.parent_track=after.parent_track='old'
        bodies={'O':body('O',-10),'Q':body('Q',0),'R':body('R',rival_y)}
        return CommonView([before,after],bodies),cfg

    def test_the_segment_before_the_boundary_is_linked_and_the_one_after_is_not(self):
        view,cfg=self.view()
        links=link_to_recorders(view,cfg)
        self.assertEqual([(l.track.split('#')[1],l.recorder) for l in links],[('segment_1','Q')])

    def test_indistinguishable_rival_prevents_reacquisition(self):
        view,cfg=self.view(rival_y=0)
        self.assertFalse([l for l in link_to_recorders(view,cfg) if l.track.endswith('segment_3')])

    def test_ambiguous_or_contaminated_prefix_cannot_inherit_identity(self):
        view,cfg=self.view()
        view.tracks[-1].identity_ambiguous=True
        self.assertFalse([l for l in link_to_recorders(view,cfg) if l.track.endswith('segment_3')])
        view.tracks[-1].identity_ambiguous=False
        for sample in view.tracks[-1].samples[:10]:
            sample.point[1]=8
        self.assertFalse([l for l in link_to_recorders(view,cfg) if l.track.endswith('segment_3')])


class S02OrderTests(unittest.TestCase):
    def events(self,variant):
        run=ROOT/'traces/S02'/('run_0_'+variant)
        if not (run/'vehicles/A/ego.jsonl').exists():self.skipTest('canonical trace not present')
        local=reconstruct_vehicle(run/'vehicles/A',ReconstructionConfig(),context=read_incident_context(run))
        return {kind:next(n.t_local for n in local.graph.nodes if n.event_type==kind)
                for kind in ['CUT_IN_FROM_LEFT_START','CRITICAL_TTC_START','COLLISION']}

    def test_s02_crash_cutin_before_critical(self):
        events=self.events('crash')
        self.assertGreaterEqual(events['CRITICAL_TTC_START']-events['CUT_IN_FROM_LEFT_START'],.2-1e-6)
        self.assertLess(events['CRITICAL_TTC_START'],events['COLLISION'])
