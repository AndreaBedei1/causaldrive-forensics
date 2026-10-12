# Final validation

The final offline analysis is prepared to run from one clean analysis freeze.
Quantitative execution records and the exact freeze commit are filled after that
execution; this source-checkout document does not certify a future result.

## Reconstruction changes

S12 collision continuity requires a short segment with the same parent, two strongly
named flanking segments, a matched contact, consistent body geometry across measured
samples, and no compatible local rival or competing recorder. Impact-disturbed velocity
alone no longer creates a new road user. Motion ambiguity remains internal; a real
identity switch cannot inherit the name through incompatible geometry.

PATH ENTRY/EXIT, CUT_IN and CRITICAL_TTC share estimated body geometry. PATH tests the
body's intersection with the forward corridor, with hysteresis and no invented first-seen
entry. CUT_IN additionally requires persistent absolute target lateral motion in a
straight path frame fixed at first observation; ego yaw and translation alone cannot
create the manoeuvre. This removes the S16 C cut-in, preserving true S02 and S17 cut-ins.
The reference oracle uses true oriented body geometry only within privileged evaluation.

Global events union source-track state intervals per observer/entity/state, preserving
source local nodes and source tracks. Sampling cells join adjoining handoffs. Appearance
is unique while any source supports the entity; loss waits for the last source. Silent
initial path states remain silent even when another source subsequently enters.
Replay reads those persisted entity events for its displayed timeline, while the original
local events remain available for diagnosis. Headless state labels also union source labels.
New geometric evidence uses declared decimal precision; differences below 1e-13 m/s between
NumPy versions cannot invalidate the byte comparison proving independence from privileged files.

## Evaluation and assumptions

The historical fusion medians are decomposed on identical physical instants in
[fusion_accuracy_regression](audit/fusion_accuracy_regression.md). The single-track
comparator now has one median source error per fused entity/instant, avoiding unequal
weighting with source count. Fused-state errors exclude mixed-identity source instants;
identity mistakes and fragmentation are always reported separately.

GNSS common fractions 0.5, 0.9 and 1.0 are sensitivity assumptions, supported only as
parametric exploration of slow common errors. Independent white noise, heading and
velocity remain. Absolute and simultaneous pairwise position errors are separate;
common translation can preserve relative identity but displace absolute fused centres.
The empirical relative-error reliability boundary is conditional, not a universal claim.

Combined pose/10% impulse robustness includes all canonical runs; wrong pairings are
counted separately from unpaired singleton callbacks and unmatched true contacts.
All semantic thresholds retain their documented values; no recall target tuning.

## Preservation and cleanup

Initial tree: 2,352 tracked files, 333.53 MiB. All 9,097 raw/manifest SHA-256 hashes
checked unchanged before freeze. Superseded audit image sets, intermediate diagnoses,
old verdicts and generated LLM outputs were removed after fusion regression diagnosis.
The classification is in [final_tree_inventory](audit/final_tree_inventory.json).
Unique recording/calibration details and the verified bibliography were preserved.

The final quantitative evidence will name the clean execution commit and hashes of all
current tables and figures. Historical recording objects are never relabelled.
