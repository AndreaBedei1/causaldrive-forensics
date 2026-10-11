import json
import unittest
from pathlib import Path

import numpy as np

from src.cdf.reconstruction.alignment import match_collisions, impulse_z
from src.cdf.reconstruction.config import FusionConfig, TrackingConfig, SemanticsConfig
from src.cdf.reconstruction.models import GraphNode, LocalGraph
from src.cdf.reconstruction.tracking import TrackMeasurement, identity_segments, LocalTrack, TrackSample
from src.cdf.reconstruction.local import track_events
from src.cdf.evaluation.provenance import commit_code_hash, verify_equivalence


def graph(owner, reports):
    return LocalGraph(owner, [GraphNode(owner+':'+str(i),'COLLISION','OUTCOME',owner,None,t,
                                       {'peak_impulse':v},'collision_sensor',1.0)
                              for i,(t,v) in enumerate(reports)])


class CollisionUncertaintyTests(unittest.TestCase):
    def test_independent_uncertainty_requires_geometry(self):
        graphs=[graph('A',[(10,800)]),graph('B',[(20,1200)])]
        self.assertEqual(match_collisions(graphs,FusionConfig())[0],[])
        found,_=match_collisions(graphs,FusionConfig(),lambda *args:(0,1))
        self.assertEqual(len(found),1)
        self.assertLess(found[0]['impulse_z'],3)

    def test_geometry_rejects_equal_impulses_at_separate_contacts(self):
        graphs=[graph('A',[(10,1000)]),graph('B',[(20,1000)])]
        found,rejected=match_collisions(graphs,FusionConfig(),lambda *args:(50,1))
        self.assertFalse(found)
        self.assertIn('apart',rejected[0]['reason'])

    def test_two_equally_supported_partners_are_unmatched(self):
        graphs=[graph('A',[(10,1000)]),graph('B',[(20,900)]),graph('C',[(30,1100)])]
        def contacts(a,ta,b,tb):return (50,1) if {a,b}=={'B','C'} else (0,1)
        found,_=match_collisions(graphs,FusionConfig(),contacts)
        self.assertFalse(found)

    def test_chain_assignment_uses_coverage_without_impulse_tie_break(self):
        graphs=[graph('A',[(10,900)]),graph('B',[(20,1000),(22,1100)]),graph('C',[(30,1000)])]
        def contacts(a,ta,b,tb):
            return (50,1) if {a,b}=={'A','C'} or ({a,b}=={'A','B'} and max(ta,tb)==20) else (0,1)
        found,_=match_collisions(graphs,FusionConfig(),contacts)
        self.assertEqual({tuple(e['graphs']) for e in found},{('A','B'),('B','C')})

    def test_zero_impulses_do_not_provide_identity(self):
        self.assertFalse(match_collisions([graph('A',[(0,0)]),graph('B',[(0,0)])],FusionConfig(),lambda *args:(0,1))[0])


class IdentitySegmentTests(unittest.TestCase):
    def measurements(self, widths):
        return [TrackMeasurement(i*.05,xy=np.array([i*.5,0]),points=np.column_stack([np.zeros(20)+i*.5,
                                                                                 np.linspace(-w/2,w/2,20)]))
                for i,w in enumerate(widths)]

    def test_persistent_two_body_support_splits_without_smoothing_across_it(self):
        widths=[1.9]*15+[5]*10+[1.9]*15
        states=np.array([[i*.5,0,10,0] for i in range(len(widths))])
        segments=identity_segments(self.measurements(widths),states,TrackingConfig())
        self.assertEqual([s[2] for s in segments],[False,True,False])

    def test_single_outlier_and_a_single_body_do_not_fragment(self):
        widths=[1.9]*15+[5]+[1.9]*15
        states=np.array([[i*.5,0,10,0] for i in range(len(widths))])
        self.assertEqual(identity_segments(self.measurements(widths),states,TrackingConfig()),[(0,len(widths),False)])

    def test_ambiguous_body_cannot_generate_a_path_entry_or_hazard(self):
        samples=[TrackSample(i*.1,10,3-i*.3,10,0,10,.1,.1,10,0,10,3-i*.3,2,5,True,10,
                             identity_ambiguous=True) for i in range(20)]
        track=LocalTrack('track_001#segment_2',samples,identity_ambiguous=True)
        events=track_events('A',track,3,SemanticsConfig())
        self.assertFalse([e for e in events if e.type in ('EGO_PATH_ENTRY','CRITICAL_TTC_START') or e.type.startswith('CUT_IN')])


class HistoricalProvenanceTests(unittest.TestCase):
    def test_equivalence_is_proved_without_rewriting_execution(self):
        old={'git_commit':'c80eab4','git_dirty':True,'code_sha256':commit_code_hash('11dbc6d')}
        new=verify_equivalence(old,['11dbc6d'])
        self.assertEqual(new['git_commit'],'c80eab4')
        self.assertTrue(new['git_dirty'])
        self.assertTrue(new['equivalent_clean_commit'].startswith('11dbc6d'))

    def test_unverified_equivalence_is_not_asserted(self):
        record={'git_commit':'c80eab4','git_dirty':True,'code_sha256':'wrong'}
        self.assertNotIn('equivalent_clean_commit',verify_equivalence(record,['11dbc6d']))

    def test_independent_checker_never_imports_event_implementation(self):
        source=(Path(__file__).resolve().parents[1]/'scripts/event_oracle_independent_check.py').read_text()
        import ast
        tree=ast.parse(source)
        imports=[n.module or '' for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)]
        self.assertFalse([n for n in imports if n.startswith('cdf')])
