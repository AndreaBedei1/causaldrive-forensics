"""The controller reacts to a collision at a tick fixed by the collision frame, not by callback arrival."""

import unittest

from cdf.simulation.vehicle_agent import RawVehicleAgent


class _Controller:
    def __init__(self):
        self.impacted = False
        self.notified_at = None

    def notify_impact(self):
        self.impacted = True


class _Collisions:
    def __init__(self):
        self.pending = []

    def drain_vehicle(self):
        out, self.pending = self.pending, []
        return out


def _agent(reaction_ticks=1):
    agent = RawVehicleAgent.__new__(RawVehicleAgent)
    agent.controller, agent.collision_sensor, agent.logger = _Controller(), _Collisions(), None
    agent.impact_reaction_ticks = reaction_ticks
    agent._first_impact_frame, agent.late_impact_notifications = None, 0
    return agent


class ImpactReactionTests(unittest.TestCase):
    def _run(self, arrival_frame, collision_frame=100, frames=range(98, 106)):
        agent = _agent()
        reacted = None
        for frame in frames:
            if frame == arrival_frame:
                agent.collision_sensor.pending.append({"frame": collision_frame, "timestamp": 0.0, "impulse": 1.0})
            agent._receive_impacts(frame)
            if agent.controller.impacted and reacted is None:
                reacted = frame
        return reacted, agent.late_impact_notifications

    def test_reaction_tick_does_not_depend_on_arrival(self):
        # Arriving with its own frame or one frame later gives the same reaction tick.
        self.assertEqual(self._run(arrival_frame=100), (101, 0))
        self.assertEqual(self._run(arrival_frame=101), (101, 0))

    def test_a_callback_too_late_is_counted(self):
        reacted, late = self._run(arrival_frame=103)
        self.assertEqual((reacted, late), (103, 1))

    def test_an_earlier_frame_arriving_later_moves_nothing_once_reacted(self):
        agent = _agent()
        agent.collision_sensor.pending.append({"frame": 100, "timestamp": 0.0, "impulse": 1.0})
        agent._receive_impacts(101)
        self.assertTrue(agent.controller.impacted)
        agent.collision_sensor.pending.append({"frame": 99, "timestamp": 0.0, "impulse": 1.0})
        agent._receive_impacts(102)
        self.assertEqual(agent.late_impact_notifications, 0)


if __name__ == "__main__":
    unittest.main()
