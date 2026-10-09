# LLM comparison: S17/run_0_crash

PRIVILEGED evaluation artifact (reconstruction/evaluation/): it may cite the run's ground truth; it is never given to a model.  Every model received the same forensic packet, prompts, vocabulary, grammar and output schemas; each analysis used one model for both stages.  A TRUE formula means the temporal hypothesis is consistent with the reconstructed semantic trace, not that the causal explanation is proven.

## Models

| | gemini-3.5-flash-lite (high) | gpt-6-luna (high) |
|---|---|---|
| provider | gemini | openai |
| exact model id (requested) | gemini-3.5-flash-lite | gpt-6-luna |
| model reported by the API | gemini-3.5-flash-lite | gpt-6-luna |
| reasoning / thinking | {"thinking_level": "high", "max_output_tokens": 32000} | {"reasoning_effort": "high", "max_output_tokens": 32000} |
| forensic packet SHA-256 | 97cb278d7eab664e | 97cb278d7eab664e |
| embedded packet SHA-256 (audit) | c0894ee5ea8c39f8 | c0894ee5ea8c39f8 |
| prompt versions | {"explanation": "accident_abduction_v1", "formalize": "formalize_hypothesis_v1"} | {"explanation": "accident_abduction_v1", "formalize": "formalize_hypothesis_v1"} |
| status | COMPLETED | COMPLETED |

### Analyses that ended without an answer

| analysis | model | status | stage: HTTP status of each request | last error |
|---|---|---|---|---|
| gemini_gemini-3.8-flash_20261008T195647Z | gemini-3.8-flash | FAILED | explanation: 503, 503, 503 | This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later. |
| gemini_gemini-3.8-flash_20261008T195920Z | gemini-3.8-flash | FAILED | explanation: 503, 503, 503 | This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later. |
| gemini_gemini-3.8-flash_20261008T200203Z | gemini-3.8-flash | FAILED | explanation: 503, 503, 503 | This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later. |
| gemini_gemini-3.8-flash_20261008T200442Z | gemini-3.8-flash | FAILED | explanation: 503, 503, 503 | This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later. |
| gemini_gemini-3.8-flash_20261008T202105Z | gemini-3.8-flash | FAILED | explanation: 503, 503, 503 | This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later. |
| gemini_gemini-3.8-flash_20261008T204317Z | gemini-3.8-flash | FAILED | explanation: 503, 503, 503 | This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later. |
| gemini_gemini-3.8-flash_20261008T211403Z | gemini-3.8-flash | QUOTA_EXHAUSTED | explanation: 503, 503, 429 | quota exceeded: GenerateRequestsPerDayPerProjectPerModel-FreeTier (limit 20) |
| gemini_gemini-3.8-flash_20261009T000501Z | gemini-3.8-flash | QUOTA_EXHAUSTED | explanation: 503, 503, 429 | quota exceeded: GenerateRequestsPerDayPerProjectPerModel-FreeTier (limit 20) |

8 analyses, 24 requests, no answer (a failed request generates nothing; on the free tier it still counts against the daily request quota).

## 1. Causal-abductive answer (Stage 1)

| | gemini-3.5-flash-lite (high) | gpt-6-luna (high) |
|---|---|---|
| validation | VALID | VALID |
| responsible actor | A | A |
| attribution kind | RECORDER | RECORDER |
| confidence | 0.9 | 0.78 |
| causal chain steps | 5 | 5 |
| alternative hypotheses | 1 | 2 |
| unresolved entities | A:track_001, B:track_002, B:track_003 | A:track_001, B:track_002, B:track_003 |
| identity hallucinations | none | none |
| cited fact ids / invalid | 19 / 0 | 73 / 0 |

### gemini-3.5-flash-lite (high)

**Primary hypothesis.** Vehicle A steered left into the path of Vehicle B, resulting in a side collision.

**Explanation.** Vehicle A and Vehicle B were traveling in adjacent lanes on an urban multi-lane road below the speed limit. Vehicle A initiated a leftward steering maneuver starting around t_global = -1.25s, causing it to drift toward Vehicle B. Vehicle B maintained a straight trajectory with zero steering input. At t_global = 0.0s, a physical collision occurred between the two vehicles. Immediately after impact, at t_global = 0.05s, both drivers ceased acceleration and applied full brakes.

**Responsibility.** A (confidence 0.9): Vehicle A initiated a left steering maneuver that brought it into contact with Vehicle B, which was traveling straight.

Limitations stated: Exact lane markings are not recorded in the sensor data.; Analysis relies solely on telemetry and radar tracks from the two recorders.

Causal chain:

1. [GLOBAL -4.95] Vehicle A and Vehicle B are driving on a multi-lane urban road below the speed limit. (actor A; facts F0001, F0005)
2. [GLOBAL -1.25] Vehicle A initiates a left steering input, deviating from its straight path. (actor A; facts F0298)
3. [GLOBAL -1.25] Vehicle B maintains a straight path with zero steering input. (actor B; facts F0302)
4. [GLOBAL 0] A physical collision occurs between Vehicle A and Vehicle B. (actor A; facts F0401)
5. [GLOBAL 0.05] Both drivers release the accelerator and apply full brakes immediately after the collision. (actor A; facts F0403, F0407)

Alternatives:

- Vehicle B drifted into Vehicle A's lane. (responsible B, plausibility 0.05)

Unresolved entities:

- A:track_001: Surrounding road user or stationary object (Anonymous radar track not associated with any known recorder.)
- B:track_002: Surrounding road user or stationary object (Anonymous radar track not associated with any known recorder.)
- B:track_003: Surrounding road user or stationary object (Anonymous radar track not associated with any known recorder.)

### gpt-6-luna (high)

**Primary hypothesis.** A’s leftward maneuver brought A into B’s path as B was drawing alongside, making A’s movement the most plausible causal contribution to the collision.

**Explanation.** The most plausible account is a sideswipe during A’s leftward maneuver as B was drawing alongside from A’s left-rear. A’s radar shows B’s clearance shrinking while A turns left; B’s independent radar shows A approaching from B’s right, while B’s recorded motion remains nearly straight before contact. Both collision sensors match the contact at t_global_s = 0. A:track_001 was also tracked ahead-right of A and may have been relevant to A’s maneuver, but the recordings do not establish why A turned or that this track caused the collision. Exact lane boundaries and the precise contact points are not recorded.

**Responsibility.** A (confidence 0.78): A’s measured leftward turn and lateral movement are the clearest recorded traffic behaviour that made the contact likely: B was approaching alongside from A’s left, while B’s recorded pre-contact path was nearly straight. This is a causal assessment from the available motion and radar evidence, not a legal finding.

Limitations stated: The packet provides no lane-boundary or roadway-position map, so the exact lane occupancy and right-of-way cannot be established.; The exact contact points and the reason for A’s turn are not recorded.; A:track_001 and the other anonymous tracks are not identified road users; their roles and any influence on A’s behaviour remain uncertain.; The recordings cannot exclude relevant road users or events outside the recorders’ fields of view.; Brake onset is sampled at 0.1-second intervals and is only bracketed around the collision.

Causal chain:

1. [GLOBAL -4.95] At the start of the aligned recordings, both recorders were moving. A tracked B behind and to A’s left, with B gaining longitudinally; B independently tracked A ahead and to B’s right. This establishes the relative approach, not the lane geometry. (actor None; facts F0001, F0004, F0005, F0007)
2. [GLOBAL -1.15] A began a marked leftward turn around -1.15 s. At that time A still tracked B to its left, and B’s own recorded heading and lateral position remained nearly steady. A:track_002 (B) was then close, with about 1.32 m reported clearance from A. (actor A; facts F0305, F0308, F0310, F0311)
3. [GLOBAL -0.05] As A’s leftward turn continued, the two recorders’ independent radar tracks show the separation narrowing: just before contact A reported only 0.14 m clearance to B, and B reported 0.25 m clearance to A. A was still turning left overall; B’s pre-contact motion remained approximately straight. These measurements are consistent with A moving into B’s occupied space, though they do not establish lane markings or exact body contact points. (actor A; facts F0361, F0367, F0396, F0399)
4. [GLOBAL 0] The collision sensors matched a physical contact between A and B at t=0. Neither recorder’s brake pedal was pressed in the last sample before that time; both were first sampled with the brake fully pressed at +0.05 s, so the exact brake-onset time is only bracketed around contact. (actor None; facts F0394, F0398, F0401, F0403, F0407)
5. [GLOBAL 1.1] Both recorders decelerated after the contact and came to a standstill, with B first recorded nearly stopped at +1.05 s and A at +1.15 s. (actor None; facts F0430, F0434, F0484, F0487)

Alternatives:

- A’s leftward maneuver may have been an evasive response to A:track_001, which A tracked ahead-right and whose relative position and predicted approach changed before the collision. The packet does not establish that this track entered A’s lane or caused A to steer. (responsible UNKNOWN, plausibility 0.24)
- B’s greater speed and closing from A’s left-rear may have contributed to the close interaction, so a contribution from B’s passing path cannot be excluded. The recorded evidence is weaker for this account because B’s own pre-contact motion and steering remain nearly steady. (responsible B, plausibility 0.16)

Unresolved entities:

- A:track_001: Anonymous radar track observed by A ahead and to the right (The packet supplies no identity association; its possible influence on A’s leftward maneuver is not established.)
- B:track_002: Anonymous radar track observed by B ahead (The packet supplies no identity association, and it is not established as a participant in the collision.)
- B:track_003: Anonymous radar track observed by B after the collision (The packet supplies no identity association; its identity and any relation to the other anonymous tracks are unknown.)

## 2. Semantic event hypotheses (scored against the reconstructed semantic trace)

| | gemini-3.5-flash-lite (high) | gpt-6-luna (high) |
|---|---|---|
| hypotheses | 10 | 26 |
| reference_events | 36 | 36 |
| TP | 5 | 15 |
| FP | 5 | 11 |
| FN | 31 | 21 |
| precision | 0.5 | 0.577 |
| recall | 0.139 | 0.417 |
| f1 | 0.217 | 0.484 |
| hallucination_rate | 0.1 | 0.154 |
| identity_hallucination_rate | 0 | 0 |
| mean_abs_time_error_s | 0 | 0.04 |

### gemini-3.5-flash-lite (high): proposed nodes

| event | actor | subject | time | outcome |
|---|---|---|---|---|
| MOVING_START | A | - | GLOBAL -4.95 | FP |
| MOVING_START | B | - | GLOBAL -4.95 | FP |
| THROTTLE_START | A | - | GLOBAL -4.95 | FP |
| THROTTLE_START | B | - | GLOBAL -4.95 | FP |
| TURN_LEFT_START | A | - | GLOBAL -1.25 | FP |
| COLLISION | A | B | GLOBAL 0 | TP (+0.00 s) |
| THROTTLE_END | A | - | GLOBAL 0.05 | TP (+0.00 s) |
| BRAKE_START | A | - | GLOBAL 0.05 | TP (+0.00 s) |
| THROTTLE_END | B | - | GLOBAL 0.05 | TP (+0.00 s) |
| BRAKE_START | B | - | GLOBAL 0.05 | TP (+0.00 s) |

### gpt-6-luna (high): proposed nodes

| event | actor | subject | time | outcome |
|---|---|---|---|---|
| MOVING_START | A | - | GLOBAL -4.95 | FP |
| MOVING_START | B | - | GLOBAL -4.95 | FP |
| TRACK_APPEARED_FRONT | A | A:track_001 | GLOBAL -4.95 | FP |
| TRACK_APPEARED_LEFT | A | B | GLOBAL -4.95 | TP (+0.00 s) |
| TRACK_APPEARED_RIGHT | B | A | GLOBAL -4.95 | TP (+0.00 s) |
| TRACK_APPEARED_FRONT | B | B:track_002 | GLOBAL -4.95 | FP |
| CLOSING_START | A | B | GLOBAL -4.95 | FP |
| CLOSING_START | B | A | GLOBAL -4.95 | FP |
| TURN_LEFT_START | A | - | GLOBAL -1.15 | FP |
| TURN_LEFT_END | A | - | GLOBAL -0.25 | FP |
| CRITICAL_TTC_START | A | B | GLOBAL -0.25 | FP |
| CRITICAL_TTC_START | B | A | GLOBAL -0.15 | FP |
| CRITICAL_TTC_END | A | B | GLOBAL 0 | TP (+0.00 s) |
| CRITICAL_TTC_END | B | A | GLOBAL 0 | TP (-0.05 s) |
| COLLISION | A | B | GLOBAL 0 | TP (+0.00 s) |
| COLLISION | B | A | GLOBAL 0 | FP |
| THROTTLE_END | A | - | GLOBAL 0 | TP (+0.05 s) |
| THROTTLE_END | B | - | GLOBAL 0 | TP (+0.05 s) |
| BRAKE_START | A | - | GLOBAL 0.05 | TP (+0.00 s) |
| BRAKE_START | B | - | GLOBAL 0.05 | TP (+0.00 s) |
| CLOSING_END | B | A | GLOBAL 0.05 | TP (-0.05 s) |
| CLOSING_END | A | B | GLOBAL 0.2 | TP (-0.20 s) |
| MOVING_END | B | - | GLOBAL 1.05 | TP (-0.05 s) |
| STOP_START | B | - | GLOBAL 1.05 | TP (-0.05 s) |
| MOVING_END | A | - | GLOBAL 1.15 | TP (-0.05 s) |
| STOP_START | A | - | GLOBAL 1.15 | TP (-0.05 s) |

## 3. Formulas (Stage 2) and verification

| | gemini-3.5-flash-lite (high) | gpt-6-luna (high) |
|---|---|---|
| Stage-2 validation | VALID | VALID |
| formulas | 12 | 31 |
| valid / invalid | 12 / 0 | 31 / 0 |
| untestable claims | 3 | 9 |
| verifier TRUE | 10 | 19 |
| verifier FALSE | 2 | 12 |
| verifier UNKNOWN | 0 | 0 |
| verifier INVALID | 0 | 0 |

### gemini-3.5-flash-lite (high): formulas

| id | claim | formula | result |
|---|---|---|---|
| f_cc1 | causal_chain[1] | `F[-1.3,-1.2] event(TURN_LEFT_START,A)` | FALSE |
| f_cc3 | causal_chain[3] | `F[-0.1,0.1] event(COLLISION,A,B)` | TRUE |
| f_sh0 | semantic_hypotheses[0] | `F[-5.0,-4.9] event(MOVING_START,A)` | TRUE |
| f_sh1 | semantic_hypotheses[1] | `F[-5.0,-4.9] event(MOVING_START,B)` | TRUE |
| f_sh2 | semantic_hypotheses[2] | `F[-5.0,-4.9] event(THROTTLE_START,A)` | TRUE |
| f_sh3 | semantic_hypotheses[3] | `F[-5.0,-4.9] event(THROTTLE_START,B)` | TRUE |
| f_sh4 | semantic_hypotheses[4] | `F[-1.3,-1.2] event(TURN_LEFT_START,A)` | FALSE |
| f_sh5 | semantic_hypotheses[5] | `F[-0.1,0.1] event(COLLISION,A,B)` | TRUE |
| f_sh6 | semantic_hypotheses[6] | `F[0.0,0.1] event(THROTTLE_END,A)` | TRUE |
| f_sh7 | semantic_hypotheses[7] | `F[0.0,0.1] event(BRAKE_START,A)` | TRUE |
| f_sh8 | semantic_hypotheses[8] | `F[0.0,0.1] event(THROTTLE_END,B)` | TRUE |
| f_sh9 | semantic_hypotheses[9] | `F[0.0,0.1] event(BRAKE_START,B)` | TRUE |

Untestable claims:

- causal_chain[0]: Vehicle A and Vehicle B are driving on a multi-lane urban road below the speed limit. (Contains quantities (speed limit value) and environmental descriptions that the temporal logic grammar cannot express.)
- causal_chain[2]: Vehicle B maintains a straight path with zero steering input. (Contains numerical quantities (zero steering input value) which the temporal logic grammar cannot express.)
- causal_chain[4]: Both drivers release the accelerator and apply full brakes immediately after the collision. (Contains quantities (full brakes pedal value) which the temporal logic grammar cannot express.)

### gpt-6-luna (high): formulas

| id | claim | formula | result |
|---|---|---|---|
| cf0 | causal_chain[0] | `F[-4.95,-4.95] (event(MOVING_START,A) AND event(MOVING_START,B) AND event(TRACK_APPEARED_LEFT,A,B) AND event(TRACK_APPEARED_RIGHT,B,A))` | TRUE |
| cf1 | causal_chain[1] | `F[-1.25,-1.15] event(TURN_LEFT_START,A)` | FALSE |
| cf2 | causal_chain[2] | `BEFORE(event(TURN_LEFT_START,A),event(COLLISION,A,B))` | FALSE |
| cf3 | causal_chain[3] | `F[0,0] event(COLLISION,A,B) AND F[0,0] event(COLLISION,B,A) AND F[-0.05,-0.05] (NOT state(BRAKE,A)) AND F[-0.05,-0.05] (NOT state(BRAKE,B)) AND F[-0.05,0.05] event(BRAKE_START,A) AND F[-0.05,0.05] event(BRAKE_START,B)` | TRUE |
| cf4 | causal_chain[4] | `F[0.95,1.05] (event(MOVING_END,B) AND event(STOP_START,B)) AND F[1.05,1.15] (event(MOVING_END,A) AND event(STOP_START,A))` | TRUE |
| sh0 | semantic_hypotheses[0] | `F[-4.95,-4.95] event(MOVING_START,A)` | TRUE |
| sh1 | semantic_hypotheses[1] | `F[-4.95,-4.95] event(MOVING_START,B)` | TRUE |
| sh2 | semantic_hypotheses[2] | `F[-4.95,-4.95] event(TRACK_APPEARED_FRONT,A,A:track_001)` | FALSE |
| sh3 | semantic_hypotheses[3] | `F[-4.95,-4.95] event(TRACK_APPEARED_LEFT,A,B)` | TRUE |
| sh4 | semantic_hypotheses[4] | `F[-4.95,-4.95] event(TRACK_APPEARED_RIGHT,B,A)` | TRUE |
| sh5 | semantic_hypotheses[5] | `F[-4.95,-4.95] event(TRACK_APPEARED_FRONT,B,B:track_002)` | FALSE |
| sh6 | semantic_hypotheses[6] | `F[-4.95,-4.95] event(CLOSING_START,A,B)` | FALSE |
| sh7 | semantic_hypotheses[7] | `F[-4.95,-4.95] event(CLOSING_START,B,A)` | FALSE |
| sh8 | semantic_hypotheses[8] | `F[-1.25,-1.15] event(TURN_LEFT_START,A)` | FALSE |
| sh9 | semantic_hypotheses[9] | `F[-0.35,-0.25] event(TURN_LEFT_END,A)` | FALSE |
| sh10 | semantic_hypotheses[10] | `F[-0.25,-0.15] event(CRITICAL_TTC_START,A,B)` | FALSE |
| sh11 | semantic_hypotheses[11] | `F[-0.25,-0.15] event(CRITICAL_TTC_START,B,A)` | FALSE |
| sh12 | semantic_hypotheses[12] | `F[0,0] event(CRITICAL_TTC_END,A,B)` | TRUE |
| sh13 | semantic_hypotheses[13] | `F[0,0] event(CRITICAL_TTC_END,B,A)` | FALSE |
| sh14 | semantic_hypotheses[14] | `F[0,0] event(COLLISION,A,B)` | TRUE |
| sh15 | semantic_hypotheses[15] | `F[0,0] event(COLLISION,B,A)` | TRUE |
| sh16 | semantic_hypotheses[16] | `F[-0.05,0.05] event(THROTTLE_END,A)` | TRUE |
| sh17 | semantic_hypotheses[17] | `F[-0.05,0.05] event(THROTTLE_END,B)` | TRUE |
| sh18 | semantic_hypotheses[18] | `F[-0.05,0.05] event(BRAKE_START,A)` | TRUE |
| sh19 | semantic_hypotheses[19] | `F[-0.05,0.05] event(BRAKE_START,B)` | TRUE |
| sh20 | semantic_hypotheses[20] | `F[-0.05,0.05] event(CLOSING_END,B,A)` | TRUE |
| sh21 | semantic_hypotheses[21] | `F[0.15,0.25] event(CLOSING_END,A,B)` | FALSE |
| sh22 | semantic_hypotheses[22] | `F[0.95,1.05] event(MOVING_END,B)` | TRUE |
| sh23 | semantic_hypotheses[23] | `F[0.95,1.05] event(STOP_START,B)` | TRUE |
| sh24 | semantic_hypotheses[24] | `F[1.05,1.15] event(MOVING_END,A)` | TRUE |
| sh25 | semantic_hypotheses[25] | `F[1.05,1.15] event(STOP_START,A)` | TRUE |

Untestable claims:

- causal_chain[0]: B was gaining longitudinally on A. (The grammar cannot express relative speed or changes in longitudinal separation; these are quantitative motion claims.)
- causal_chain[0]: The relative approach does not establish lane geometry. (Lane geometry and spatial relationships beyond the event labels are not expressible in this temporal logic.)
- causal_chain[1]: B remained tracked by A at the turn time, B's heading and lateral position remained nearly steady, and the reported clearance was about 1.32 m. (The grammar cannot express continuous radar-track observation, heading, lateral position, or numerical clearance.)
- causal_chain[1]: A may have turned in response to A:track_001, or that track caused A to steer. (A possible motive or causal influence is not represented by temporal event/state formulas; the track's identity and role are also unresolved.)
- causal_chain[2]: The radar measurements show separation narrowing, with clearances of 0.14 m and 0.25 m just before contact; B's path was approximately straight and A moved into B's occupied space. (The grammar cannot express numerical distances, path geometry, or approximate motion. The claim that A moved into B's space is a spatial and causal interpretation.)
- causal_chain[2]: A's leftward maneuver made the collision likely or was a causal contribution to it. (Temporal logic satisfaction can establish temporal consistency, not causation, likelihood, or responsibility.)
- causal_chain[2]: The exact lane occupancy, lane markings, and precise body contact points are not established. (The grammar has no representation for lane boundaries, occupancy, or contact-point geometry.)
- causal_chain[3]: Both brake pedals were fully pressed in the first sample at +0.05 s. (The grammar can express a brake state or event, but not pedal magnitude, sampling status, or a sampled value of 1.0.)
- causal_chain[4]: Both recorders decelerated after contact. (Deceleration is a quantitative motion claim and is not expressible in the grammar.)

## 4. Security

| | gemini-3.5-flash-lite (high) | gpt-6-luna (high) |
|---|---|---|
| leak guard | PASS (packet and prompts checked before each request; the analysis ran) | PASS (packet and prompts checked before each request; the analysis ran) |
| pre-send payload audit | PASS, PASS | PASS, PASS |
| identity hallucination rate | 0 | 0 |

## 5. Usage and cost

| | gemini-3.5-flash-lite (high) | gpt-6-luna (high) |
|---|---|---|
| input_tokens (both stages) | 143855 | 121423 |
| cached_input_tokens (both stages) | 0 | 0 |
| output_tokens (both stages) | 4267 | 28562 |
| reasoning_tokens (both stages) | 10341 | 18171 |
| total_tokens (both stages) | 158463 | 149985 |
| latency_s (both stages) | 32.854 | 255.643 |
| explanation: in / out / reasoning, s | 70698 / 2022 / 2280, 10.609 | 58713 / 15918 / 13110, 163.209 |
| explanation: response id | 3_XHauavBaGExN8P6vndkQ0 | resp_0884d30b68d6b8c1016ac7f640bc7887d29bf12bf13fb0c2e6 |
| formalize: in / out / reasoning, s | 73157 / 2245 / 8061, 22.245 | 62710 / 12644 / 5061, 92.434 |
| formalize: response id | 6fXHas6eLLOuvdIPvZTz6A0 | resp_02bebb321e3fa1ff016ac7f6e35c3487d29beaa1b14a49b64f |
| cost (USD) | not stated (no published price in the configuration; free tier) | 0.0264 |

Cost basis: returned usage x published list price (https://developers.openai.com/api/docs/models/gpt-6-luna, as of 2026-10-08); output tokens include reasoning tokens.

Gemini token counts: output tokens exclude the thinking tokens (thoughtsTokenCount, shown as reasoning); OpenAI: output tokens include the reasoning tokens.

## 6. Analyst assessment (written after reading the answers; not computed)

**Gemini 3.8 Flash (G38): no answer, so the mandatory G38 vs G35L comparison could not be made.**

- **Attempts.** 8 analyses with 24 requests in total: from 2026-10-08 19:56Z to 21:14Z, and once more at 2026-10-09 00:05Z.
  - 22 requests got HTTP 503 UNAVAILABLE ("This model is currently experiencing high demand").
  - 2 requests got 429 RESOURCE_EXHAUSTED `GenerateRequestsPerDayPerProjectPerModel-FreeTier`, limit 20.
- **Quota.** Failed requests count against the free tier: the first 20 503s used up the quota for 2026-10-08.
- **After the reset.** Following the 00:00 UTC reset, the quota was reported exhausted again after only two more 503s, with "retry in 23 h 48 min". Either other traffic shares the project's quota, or overloaded requests are counted more than once. https://ai.dev/rate-limit shows the project's usage.
- **What exists.** No 3.8 token was generated and no Stage 1 exists. Nothing was completed with 3.5 Flash-Lite. Every 3.8 request body passed the payload audit with the same packet as the other models.
- **Rerun.** G38 can be rerun unchanged with `--provider gemini --model gemini-3.8-flash` once 3.8 is reachable.
- **Open questions.** It remains open where 3.8 and 3.5 Flash-Lite agree or diverge, which of the two reconstructs S17 better, and whether Lite loses information against 3.8. The comparison below is between G35L and GPT-6 Luna.

**Privileged reference** (ground_truth/, never given to a model). C (`record: false`) exists in the packet only as three anonymous radar tracks: A:track_001, B:track_002 and B:track_003. The packet does not say they are one road user. C cuts in from the right ahead of A. The corridor-clearance trigger fires at t_global −1.65 s, with a front clearance of 2.48 m. A reacts at −1.30 s by swerving left: 2.7 m of lateral departure, yaw rate up to −18 °/s and a heading change of only −11°. B is overtaking on A's left at 13 m/s against A's 12 m/s, and the A–B sideswipe happens at t_global 0 (1577 N·s). The counterfactuals give the causal structure. Without C there is no collision. With the swerve disabled, A hits C at +1.0 s. The conflict is therefore initiated by the unrecorded road user's close cut-in, A's swerve is an evasive reaction, and B is the party that gets hit.

The packet holds enough to infer this. Between −2.55 s and −0.95 s, A:track_001 (bearing 29° → 9°, 4–6 m ahead) moves its lateral offset from 3.2 m to 0.7 m. Its relative lateral speed reaches −2.35 m/s and its clearance shrinks to about 1.9 m. A's yaw onset follows at −1.25 s (F0297). The best answer the packet allows is:

- the initiating cause is A:track_001, an anonymous road user that cut in from the right just ahead of A;
- A's left move was evasive, and B was hit while overtaking;
- optionally, A:track_001 and B:track_002 might be the same road user, offered as uncertain.

**1. Causal-abductive quality: neither model recovers the cause.** Both make A responsible: G35L with confidence 0.90 and GPT-6 Luna with 0.78. A did move left into B, but the initiating cause is the cut-in, which neither primary hypothesis contains.

- **GPT-6 Luna is clearly closer.** Its first alternative (responsible UNKNOWN, plausibility 0.24) is that A's leftward manoeuvre may have been an evasive response to A:track_001, which A tracked ahead-right with a changing relative position and predicted approach. Its limitations state that the reason for A's turn is not recorded. It describes B correctly: overtaking from the left-rear on a near-straight path. It also keeps all three anonymous tracks unresolved without merging them. It found the right lead but ranked it below the visible proximate cause.
- **G35L never considers the anonymous tracks.** It calls them "Surrounding road user or stationary object", gives one alternative only (B drifting, 0.05) and is the more confident of the two. Its narrative is temporally right but causally shallow.

**2. Semantic hypotheses.**

| | GPT-6 Luna | G35L |
|---|---|---|
| Hypotheses | 26 | 10 |
| TP / FP / FN | 15 / 11 / 21 | 5 / 5 / 31 |
| Precision | 0.58 | 0.50 |
| Recall | 0.42 | 0.14 |
| F1 | 0.48 | 0.22 |

- **Both miss the events that carry the causal story:** CUT_IN_FROM_RIGHT_START (A and B), EGO_PATH_ENTRY of A:track_001 into A's corridor, and A's CRITICAL_TTC_START on A:track_001.
- **G35L's true positives** are only the collision and the post-impact pedal events.
- **Some false positives are not invented events.** Four of G35L's five FPs and two of GPT-6 Luna's are states already active at the first observation. The scorer leaves those out of the reference by design, and the verifier finds them TRUE.
- **GPT-6 Luna's other FPs fall into three groups:**
  - Sector and threshold mismatches: TRACK_APPEARED_FRONT where the reconstruction says RIGHT (FRONT means a bearing within ±5°; the tracks were at 19° and 18°), and TURN_LEFT_START / END (see 3).
  - Mistimed CLOSING_START and CRITICAL_TTC_START events.
  - A duplicate COLLISION(B, A).

**3. Formula consistency: TRUE is not "correct".**

| | G35L | GPT-6 Luna |
|---|---|---|
| Formulas | 12 | 31 |
| TRUE | 10 (83 %) | 19 (61 %) |
| FALSE | 2 | 12 |

G35L asserts few things, most of them trivially checkable: initial states, the collision and the post-impact pedals. It has the higher TRUE ratio and the worse causal account, which is the "temporally consistent but causally worse" case.

Both models' TURN_LEFT formulas are FALSE because of how the reconstruction defines a turn:

- The reconstruction emits TURN_LEFT only for at least 15° of heading change at 10 °/s or more.
- A's swerve reached 18 °/s but changed the heading by only 11°, so the reconstructed trace has no TURN_LEFT for A.
- The vocabulary text the models receive ("starts turning to the left") does not state these thresholds.

So these FALSEs are a granularity mismatch. A did steer left. The same applies to the FRONT / RIGHT sector.

**4. Identity hallucinations: none.** Neither model named C or any id outside the packet. Neither claimed the anonymous tracks are one road user. The leak guard and the pre-send payload audit passed on every request.

**Cost and latency.**

| | GPT-6 Luna | G35L |
|---|---|---|
| Total tokens | 150k (18k reasoning) | 158k (10k thinking) |
| Latency | 256 s | 33 s |
| Cost | US$ 0.026 (list price) | Free tier |

**What G35L shows on its own.** Its answer is valid and fast, with no identity hallucination. It loses everything about the anonymous tracks:
- no role for them;
- no hypothesis that A's swerve was evasive;
- recall 0.14.

GPT-6 Luna keeps that line of reasoning as an alternative. Whether this is a Lite limitation or a Gemini-family one can only be settled by G38.
