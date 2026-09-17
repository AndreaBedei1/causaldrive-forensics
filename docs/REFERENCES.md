# References

These works informed the design vocabulary and the methodological choices of
this project. This is **not** a related-work section and makes no claim to
survey the field; no literature search was performed. Each entry records why it
was relevant to a decision made here.

1. **Dosovitskiy, Ros, Codevilla, Lopez, Koltun.** *CARLA: An Open Urban Driving
   Simulator.* CoRL 2017. arXiv:1711.03938.
   The simulator this project runs on. Its synchronous fixed-step mode is what
   makes the experiments deterministic and replayable.

2. **Mansy, Ehab, Elmougy.** *Towards Accountable Self-Driving Cars: A Framework
   for Identifying the Cause of Autonomous Traffic Collisions.* IEEE World Forum
   on Internet of Things, 2023. DOI 10.1109/WF-IoT58464.2023.10539453.
   Applies causal reasoning to vehicle readings, velocity and steering for
   collision-cause identification — the same evidence classes this project
   restricts its local layer to.

3. **Wang, Xue, Jiang, Jia.** *Responsibility Attribution for Autonomous Vehicle
   Crashes Based on Causal Inference: Case Study in California, USA.*
   Transportation Research Record, 2026. DOI 10.1177/03611981261438023.
   Recent crash responsibility-attribution work. Deliberately not reproduced
   here: this project attributes *causal contribution* from onboard evidence
   rather than responsibility from crash reports.

4. **Aryan, Chockler, Mousavi.** *Causal Liability in Autonomous Systems.* FASE
   2026, LNCS 16504. DOI 10.1007/978-3-032-22774-4_15.
   Structural causal models and logical specifications for causal contribution.
   The `cdf.causal.scm` abstraction and the insistence that interventional
   claims be backed by an actual intervention follow this line of thinking.

5. **Pinter, Szalay, Vida.** *Road Accident Reconstruction Using On-board Data,
   Especially Focusing on the Applicability in Case of Autonomous Vehicles.*
   Periodica Polytechnica Transportation Engineering, 2020. DOI 10.3311/PPTR.13469.
   What onboard data are actually required for reconstruction. Motivates the
   telemetry + controls + radar evidence set.

6. **Đorđević, Mitić.** *The possibility of traffic accident reconstruction using
   event data recorders: A review.* Industrija, 2021. DOI 10.5937/industrija49-35974.
   Central motivation for this project: classical EDR data supports simple
   longitudinal crashes far better than multi-participant crashes and pre-crash
   manoeuvres. That gap is what the distributed fusion layer targets.

7. **Strandberg, Nowdehi, Olovsson.** *A Systematic Literature Review on
   Automotive Digital Forensics: Challenges, Technical Solutions and Data
   Collection.* IEEE Transactions on Intelligent Vehicles.
   DOI 10.1109/TIV.2022.3188340.
   Trustworthy automotive forensic evidence. Informs the provenance and
   integrity design: schema versioning, evidence references on every event and
   edge, and SHA-256 digests in `evidence_manifest.json`.

8. **Xiang et al.** *Multi-Sensor Fusion and Cooperative Perception for
   Autonomous Driving: A Review.* IEEE Intelligent Transportation Systems
   Magazine, 2023. DOI 10.1109/MITS.2023.3283864.
   Multi-agent information fusion. Note the difference in setting: this project
   performs *post-event* fusion of exchanged evidence, not online cooperative
   perception, and requires no V2X link.

9. **Wang, Xu, Tan.** *InterCoop: Spatio-Temporal Interaction Aware Cooperative
   Perception for Networked Vehicles.* ICRA 2024. DOI 10.1109/ICRA57147.2024.10610188.
   Spatio-temporal interaction-aware fusion among vehicles. The temporal
   alignment and event identity-resolution stages address the same problems
   offline.

10. **Zhao, Yurtsever, Paulson, Rizzoni.** *Formal Certification Methods for
    Automated Vehicle Safety Assessment.* IEEE Transactions on Intelligent
    Vehicles. DOI 10.1109/TIV.2022.3170517.
    Formal safety methods for automated vehicles. Context for the finite-trace
    monitoring layer — and for the care taken not to overclaim it as
    verification of the simulator.

11. **Shea-Blymyer, Abbas.** *A Deontic Logic Analysis of Autonomous Systems'
    Safety.* HSCC 2020. DOI 10.1145/3365365.3382203.
    Logical reasoning about driving obligations. Informs the shape of the safety
    properties (obligation-to-respond rather than mere threshold crossing) in
    `cdf.checking.properties`.

12. **Goyal, Griggio, Kimblad, Tonetta.** *Automatic Generation of Scenarios for
    System-level Simulation-based Verification of Autonomous Driving Systems.*
    EPTCS, 2023. DOI 10.4204/EPTCS.395.8.
    Scenario generation for simulation-based V&V. Supports the declarative,
    parameterised scenario specification and its explicit validation criteria.

13. **Building causal models for finding actual causes of unmanned aerial
    vehicle failures.** Frontiers in Robotics and AI, 2024.
    DOI 10.3389/frobt.2024.1123762.
    Not automotive, but methodologically close: building causal models and
    reasoning about *actual* causes of a specific incident rather than average
    effects — which is exactly the question asked of a single crash here.
