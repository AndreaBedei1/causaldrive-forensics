# Hardening assumptions

These are general engineering assumptions, not calibrated sensor specifications.

- Impulse: independent relative per-report standard deviation 0.10; combined
  `sigma = 0.10 * hypot(I1,I2)`, gate `abs(I1-I2)/sigma <= 3`. Both settings are
  configurable. No reviewed source establishes the accuracy of a real collision
  impulse sensor. This is an uncertainty budget to test, not a real-world accuracy
  claim. With no body geometry the legacy 10% gate remains. Zero impulses cannot
  identify contact. Body contact and approach trajectories are independent evidence;
  maximum feasible one-to-one report assignments resolve forced edges only.
  Equally supported alternatives stay unmatched. Existing clock consistency and
  merged-burst constraints remain.
- Local identity: transverse 5th–95th percentile return support wider than 2.5 m
  plus the tracker measurement standard deviation is incompatible with the declared
  car/van envelope. At least five wide sweeps within the track-gap window confirm
  an ambiguous bout; the existing 0.5 s gap pads its limits. Segments are smoothed
  independently. This can also detect uncertain heading after a crash; it does not
  prove which physical body was tracked. Data and covariance remain available.
  Hazard, cut-in and path-entry claims are UNKNOWN during the ambiguous segment.
  Its radar points remain visible, but no physical ghost box is asserted.
- Stitching: lateral endpoint displacement must also pass the existing 99% 2-dof
  gate using face/velocity uncertainty, without the isotropic unobserved-acceleration
  allowance. It refuses an unseen lateral identity jump and can fragment a real
  lane change across a gap. No scenario id, true identity or GT state enters it.
  A segment endpoint created by detected identity ambiguity cannot participate
  in a motion-only stitch, even with a different track id. Actual simultaneous
  body observations can still link its stable portions across observers.

The full-sweep before/after audit measures the costs of these choices. Historical
robustness and threshold-sensitivity families retain their original execution
provenance; only baseline/impulse robustness is refreshed for this task.
