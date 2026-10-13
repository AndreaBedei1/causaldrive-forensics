"""General body, target-manoeuvre, entity union and impact continuity rules."""
import dataclasses
import json
import math
import tempfile
import unittest
from pathlib import Path
import numpy as np
from src.cdf.reconstruction.anonymous import CommonView, collision_continuity_links
from src.cdf.reconstruction.common_frame import RecorderBody, RecordedPoseSource
from src.cdf.reconstruction.config import ReconstructionConfig, SemanticsConfig
from src.cdf.reconstruction.conflict import body_in_corridor, box_corners, target_box
from src.cdf.reconstruction.fusion import aggregate_entity_events
from src.cdf.reconstruction.local import track_events
from src.cdf.reconstruction.models import Alignment, Association, GraphClock, GlobalNode, Observation
from src.cdf.reconstruction.tracking import EgoFootprint, EgoState, EgoTrajectory, LocalTrack, TrackSample
from src.cdf.robustness.perturb import GnssProfile, PerturbedPoseSource
from test_road_user_fusion import track, straight, following


def sample(t,x,y,vx,vy,box=None):
    return TrackSample(t,x,y,vx,vy,math.hypot(vx,vy),.05,.05,math.hypot(x,y),math.degrees(math.atan2(y,x)),
                       x,y,0,None,True,10,body_estimate=box)


class BodyEvents(unittest.TestCase):
    def events(self,ys,turn=False,target_moves=True):
        samples=[];states=[]
        for i,y in enumerate(ys):
            t=i*.1;heading=-min(t*.15,.3) if turn else 0
            own=EgoState(t,10*t,0,heading,10,0);states.append(own)
            world_y=y if target_moves else 4
            vy=-1 if target_moves else 0
            x=20+10*t
            s=sample(t,x,world_y,10,vy,(x,world_y,0,4.6,1.9))
            dx=x-own.x;s.longitudinal_m=math.cos(heading)*dx+math.sin(heading)*world_y
            s.lateral_m=-math.sin(heading)*dx+math.cos(heading)*world_y
            samples.append(s)
        return track_events('O',LocalTrack('T',samples),samples[-1].t_local,SemanticsConfig(),EgoTrajectory(states)),samples

    def test_body_enters_before_its_representative_point(self):
        events,_=self.events(np.linspace(4,0,41))
        entry=next(e.t_local for e in events if e.type=='EGO_PATH_ENTRY')
        self.assertLess(entry,2.5) # point reaches the 1.5 m corridor at 2.5 s

    def test_first_seen_body_already_inside_does_not_invent_entry(self):
        events,_=self.events(np.linspace(2,0,21))
        self.assertFalse([e for e in events if e.type=='EGO_PATH_ENTRY'])

    def test_forward_body_edge_can_enter_while_point_is_behind_front(self):
        body=box_corners(np.array([1.,0.]),np.array([1.,0.]),(2.3,.95))
        self.assertTrue(body_in_corridor(body,2.3,1.5))
        self.assertFalse(body_in_corridor(body,3.4,1.5))

    def test_rotated_corner_bounding_rectangle_is_not_enough(self):
        body=box_corners(np.array([0.,3.]),np.array([math.sqrt(.5),math.sqrt(.5)]),(2.,.2))
        self.assertFalse(body_in_corridor(body,1.,1.5))

    def test_ego_turn_alone_cannot_create_target_cut_in(self):
        events,_=self.events(np.full(41,4.),turn=True,target_moves=False)
        self.assertFalse([e for e in events if e.type.startswith('CUT_IN')])

    def test_real_body_cut_in_is_detected(self):
        events,_=self.events(np.linspace(4,0,41))
        self.assertTrue([e for e in events if e.type=='CUT_IN_FROM_RIGHT_START'])

    def test_body_heading_does_not_replace_its_translation_velocity(self):
        from src.cdf.reconstruction.conflict import _Prediction
        s=sample(1,20,4,10,-2,(20,4,0,4.6,1.9))
        p=_Prediction(s,EgoState(1,0,0,0,12,0),None,SemanticsConfig())
        self.assertEqual(float(p.target_unit[1]),0)
        self.assertLess(float(p.target_motion_unit[1]),0)


def node(kind,t,track_id):
    return GlobalNode('',kind,'PERCEPTION','O','U1',['O'],t,{'source_track':track_id},'radar',None,
                      [Observation('O',track_id+kind+str(t),t)])


class EntityUnion(unittest.TestCase):
    def test_overlapping_states_have_one_start_and_last_end(self):
        nodes=[node('CLOSING_START',0,'a'),node('CLOSING_END',2,'a'),
               node('CLOSING_START',1,'b'),node('CLOSING_END',3,'b')]
        out=aggregate_entity_events(nodes,{})
        self.assertEqual([(n.event_type,n.t_global) for n in out],[('CLOSING_START',0),('CLOSING_END',3)])
        self.assertEqual(len(out[0].attributes['source_local_nodes']),4)

    def test_duplicate_appearance_and_closing_are_collapsed(self):
        nodes=[node(k,0,t) for k in ['TRACK_APPEARED_RIGHT','CLOSING_START'] for t in ['a','b']]
        out=aggregate_entity_events(nodes,{('O','a'):(2,.05),('O','b'):(3,.05)})
        self.assertEqual(len(out),2)

    def test_loss_waits_for_the_last_source(self):
        nodes=[node('TRACK_APPEARED_RIGHT',0,'a'),node('TRACK_LOST',2,'a'),
               node('TRACK_APPEARED_RIGHT',1,'b'),node('TRACK_LOST',3,'b')]
        out=aggregate_entity_events(nodes,{('O','a'):(2,.05),('O','b'):(3,.05)})
        self.assertEqual([(n.event_type,n.t_global) for n in out],[('TRACK_APPEARED_RIGHT',0),('TRACK_LOST',3)])

    def test_real_loss_reacquisition_remains_visible(self):
        nodes=[node('TRACK_APPEARED_RIGHT',0,'a'),node('TRACK_LOST',1,'a'),
               node('TRACK_APPEARED_RIGHT',2,'b'),node('TRACK_LOST',3,'b')]
        self.assertEqual(len(aggregate_entity_events(nodes,{('O','a'):(1,.05),('O','b'):(3,.05)})),4)

    def test_first_seen_active_path_has_no_invented_entry(self):
        nodes=[node('TRACK_APPEARED_RIGHT',0,'a'),node('EGO_PATH_EXIT',2,'a'),
               node('TRACK_APPEARED_RIGHT',1,'b'),node('EGO_PATH_ENTRY',1.5,'b'),node('EGO_PATH_EXIT',3,'b')]
        out=aggregate_entity_events(nodes,{('O','a'):(4,.05),('O','b'):(4,.05)})
        self.assertFalse([n for n in out if n.event_type=='EGO_PATH_ENTRY'])
        self.assertEqual([n.t_global for n in out if n.event_type=='EGO_PATH_EXIT'],[3])


    def test_initial_path_without_exit_still_suppresses_duplicate_entry(self):
        first=node('TRACK_APPEARED_RIGHT',0,'a')
        first.attributes['initial_in_ego_path']=True
        out=aggregate_entity_events([first,node('EGO_PATH_ENTRY',1,'b'),node('EGO_PATH_EXIT',2,'b')],
                                    {('O','a'):(3,.05),('O','b'):(3,.05)})
        self.assertFalse([n for n in out if n.event_type in ('EGO_PATH_ENTRY','EGO_PATH_EXIT')])

    def test_state_survives_an_adjoining_source_handoff(self):
        out=aggregate_entity_events([node('CLOSING_START',0,'a'),node('CLOSING_START',1.05,'b')],
                                    {('O','a'):(1,.05),('O','b'):(2,.05)})
        self.assertEqual([(n.event_type,n.t_global) for n in out],[('CLOSING_START',0)])

    def test_unaligned_initial_path_keeps_its_original_local_observation(self):
        appeared=node('TRACK_APPEARED_RIGHT',0,'a');appeared.t_global=None
        appeared.attributes['initial_in_ego_path']=True
        out=aggregate_entity_events([appeared],{})
        self.assertEqual(out,[appeared])
        self.assertTrue(out[0].observations)


class CollisionContinuity(unittest.TestCase):
    def setup_view(self):
        def body(name,x):
            rows=[dict(timestamp=i*.05,x=x+10*i*.05,y=0,yaw_deg=0,velocity=dict(x=10,y=0)) for i in range(70)]
            return RecorderBody(name,RecordedPoseSource(rows,0),EgoFootprint(-2.3,2.3,-.95,.95),0)
        ts=[[i*.05 for i in range(15)],[.75+i*.05 for i in range(16)],[1.55+i*.05 for i in range(25)]]
        tracks=[track('O','p#'+str(i),times,straight(4.6,0,10),following(0,0,10)) for i,times in enumerate(ts)]
        for tr in tracks:
            tr.parent_track='p'
            for s in tr.samples:s.near=s.point.copy()
        for tr in [tracks[0],tracks[2]]:tr.status='ASSOCIATED';tr.entity='R'
        tracks[1].identity_ambiguous=True
        a=[Association('O',tr.track_id,'R' if tr.status=='ASSOCIATED' else 'O:'+tr.track_id,
                       tr.status,None,[],['O'],candidate='R',collision_event='c') for tr in tracks]
        align=Alignment('c',{'O':GraphClock('O','ALIGNED',offset_to_global=0),
                            'R':GraphClock('R','ALIGNED',offset_to_global=0)},
                        [dict(event_id='c',graphs=['O','R'],t_local={'O':1.,'R':1.})])
        return CommonView(tracks,{'O':body('O',0),'R':body('R',4.6)}),a,align

    def test_short_collision_segment_inherits_only_with_two_strong_flanks(self):
        view,a,align=self.setup_view()
        links=collision_continuity_links(view,a,align,[],ReconstructionConfig())
        self.assertEqual([(l.track,l.recorder) for l in links],[('O:p#1','R')])
        self.assertTrue(view.tracks[1].identity_ambiguous) # uncertain motion remains internal

    def test_real_switch_cannot_inherit_identity(self):
        view,a,align=self.setup_view()
        for s in view.tracks[1].samples:s.point[1]=8;s.near[1]=8
        self.assertFalse(collision_continuity_links(view,a,align,[],ReconstructionConfig()))

    def test_rival_contact_track_prevents_inheritance(self):
        view,a,align=self.setup_view()
        rival=dataclasses.replace(view.tracks[1],track_id='rival',parent_track=None)
        view.tracks.append(rival)
        a.append(dataclasses.replace(a[1],local_track='rival'))
        self.assertFalse(collision_continuity_links(view,a,align,[],ReconstructionConfig()))


class CorrelatedGNSS(unittest.TestCase):
    def records(self,start=0):
        return [dict(timestamp=start+i*.1,x=10*i*.1,y=0,yaw_deg=0,velocity=dict(x=10,y=0)) for i in range(50)]

    def test_common_translation_cancels_in_relative_geometry(self):
        profile=GnssProfile('paired',bias_m=2,markov_m=1,common_fraction=1)
        a=PerturbedPoseSource(self.records(),0,profile,7,'A')
        b=PerturbedPoseSource(self.records(),0,profile,7,'B')
        np.testing.assert_allclose(a.x,b.x);np.testing.assert_allclose(a.y,b.y)
        self.assertGreater(float(np.max(np.abs(a.y))),.1)

    def test_fraction_scales_only_independent_slow_error(self):
        profile=GnssProfile('paired',bias_m=2,markov_m=1)
        def diff(p):
            a=PerturbedPoseSource(self.records(),0,p,7,'A');b=PerturbedPoseSource(self.records(),0,p,7,'B')
            return a.x-b.x
        np.testing.assert_allclose(diff(dataclasses.replace(profile,common_fraction=.9)),math.sqrt(.1)*diff(profile),atol=1e-12)

    def test_factory_shares_epochs_with_different_recorder_start_times(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            for n,start in [('A',0.),('B',.2)]:
                (root/n).mkdir();(root/n/'ego.jsonl').write_text('\n'.join(json.dumps(r) for r in self.records(start)),encoding='utf-8')
            make=PerturbedPoseSource.factory(GnssProfile('paired',bias_m=2,markov_m=1,common_fraction=1),7)
            a=make(root/'A',0);b=make(root/'B',.2)
            # At simultaneous epochs subtract each receiver's exact own pose.
            np.testing.assert_allclose(a.x[2:]-np.arange(2,50)*1.,b.x[:48]-np.arange(48)*1.,atol=1e-10)

    def test_invalid_common_fraction_is_rejected(self):
        with self.assertRaises(ValueError):GnssProfile('bad',common_fraction=1.1)


class CanonicalFinalRules(unittest.TestCase):
    def test_s09_has_no_anonymous_recorder_between_parent_segments(self):
        root=Path(__file__).resolve().parents[1]
        rows=json.loads((root/'traces/S09/run_0_near_simultaneous/reconstruction/global/associations.json').read_text(encoding='utf-8'))
        parts=[r for r in rows if r['local_graph']=='B' and r['local_track'].startswith('track_001#')]
        self.assertEqual(len(parts),3)
        self.assertEqual({r['global_entity'] for r in parts},{'A'})

    def test_s11_ego_turn_has_no_target_c_cut_in(self):
        root=Path(__file__).resolve().parents[1]
        graph=json.loads((root/'traces/S11/run_0_consequential/reconstruction/global/global_graph.json').read_text(encoding='utf-8'))
        self.assertFalse([n for n in graph['nodes'] if n['actor_id']=='A' and n['subject_id']=='C'
                          and n['event_type'].startswith('CUT_IN')])

    def test_s13_global_entity_semantics_are_not_duplicated(self):
        root=Path(__file__).resolve().parents[1]
        for variant in ['abreast','platoon','passing']:
            graph=json.loads((root/'traces/S13'/('run_0_'+variant)/'reconstruction/global/global_graph.json').read_text(encoding='utf-8'))
            keys=[(n['actor_id'],n['subject_id'],n['event_type'],n['t_global']) for n in graph['nodes']
                  if n['subject_id'] and n['t_global'] is not None]
            self.assertEqual(len(keys),len(set(keys)),variant)

    def test_combined_gnss_impulse_conservatively_matches_multiple_contacts(self):
        from src.cdf.robustness.perturb import GNSS_PROFILES,CollisionPerturbation,Perturbation,perturbed_copy
        from src.cdf.reconstruction.pipeline import reconstruct_run
        from src.cdf.evaluation.reconstruction import evaluate_run
        root=Path(__file__).resolve().parents[1]
        for name in ['run_0_a_front_pushed','run_0_b_rear_first']:
            with tempfile.TemporaryDirectory() as temp:
                profile=dataclasses.replace(GNSS_PROFILES['consumer'],common_fraction=.9)
                copy=perturbed_copy(root/'traces/S04'/name,Path(temp)/'S04'/name,
                                    Perturbation('combined',gnss=profile,collisions=CollisionPerturbation(impulse_rel_std=.1)),0)
                reconstruct_run(copy,pose_factory=PerturbedPoseSource.factory(profile,0))
                result=evaluate_run(copy,clock_shift_check=False)
                # Singleton callbacks are conservative unmatched reports, not wrong pairings.
                self.assertFalse([c for c in result['extra_collisions'] if len(c['participants'])>1])
                self.assertTrue(all(c['participants_correct'] for c in result['collisions'] if c['reconstructed_as']))

    def test_replay_displays_entity_timeline_and_retains_local_sources(self):
        from src.cdf.replay.model import ReplayRun
        root=Path(__file__).resolve().parents[1]
        for variant in ['abreast','platoon','passing']:
            run=ReplayRun.load(root/'traces/S13'/('run_0_'+variant))
            shown=run.display_events()
            keys=[(e.actor,e.subject,e.event_type,e.time) for e in shown if e.subject]
            self.assertEqual(len(keys),len(set(keys)),variant)
            self.assertGreater(len(run.all_events()),len(shown))
