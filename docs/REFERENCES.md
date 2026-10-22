# References

Every source the project relies on, in one place:

* **Part A**: the sources of the simulated sensors and of the degradation profiles of the robustness study, with
  the values each one supports and the kind of evidence behind each value;
* **Part B**: the estimation methods the reconstruction implements;
* **Part C**: related work and the regulatory context of the paper (compiled and verified on 2026-10-10, unchanged
  below except for its title).

**Verification.**  Every DOI of Parts A and B was resolved again against the Crossref REST API on 2026-10-23
(`api.crossref.org/works/<DOI>`): title, first author, venue and year match the citation; the check is saved in
`docs/references_crossref_2026-10-23.json`.  Documents without a DOI (data sheets, vendor reports, the CARLA
documentation) are cited by the URL at which they were read on 2026-10-10.  No reference was added from memory
without such a check.

**Keys.**  Keys are unique within a part: in Part A, R1-R11 are radar sources and G/N keys GNSS sources, as `docs/robustness_profiles.md` cites them; in Part C, B1-B69 are publications and R1-R9 regulatory instruments, as `docs/paper_positioning.md` cites them.

**Kinds of evidence** used in Part A (the same labels as `docs/robustness_profiles.md`, which gives every profile
value with its justification):

| label | meaning |
|---|---|
| measured | a value measured on real data in the cited study or dataset |
| specification | a manufacturer's stated accuracy or a sensor specification reported by a study |
| design value | a parameter chosen by the cited authors for their own tracker or simulation, not a measurement |
| derived | computed by us from a cited value (unit conversion, median, Gaussian percentile conversion) |
| engineering assumption | no source supports the value itself; the reason is given in `docs/robustness_profiles.md` |

## Part A. Sensors, simulator and degradation profiles

### A.1 Radar (profiles `nominal`, `severe`, `extreme` of campaign v3; historical `low`, `nominal`, `high`)

| key | source | DOI / URL | what it supports here | kind |
|---|---|---|---|---|
| R1 | Continental Engineering Services, "ARS 408-21 Long Range Radar Sensor 77 GHz - Data Sheet", print ID 091018_FS_ARS_408_21_EN_HS (2018, modified 2020) | <https://platformselect.autonomoustuff.com/wp-content/uploads/2020/08/ARS-408-21-whitelabel.pdf> | range accuracy +-0.10 m (near) and +-0.40 m (far); azimuth +-0.1 deg (far), +-1 deg at +-45 deg and +-5 deg at +-60 deg (near); radial velocity +-0.1 km/h; Doppler resolution 0.37 / 0.43 km/h; cycle time | specification |
| R2 | smartmicro, "High Performance Automotive Radar" flyer, UMRR-11 Type 132 and UMRR-96 Type 153 (2020) | <https://levelfivesupplies.com/wp-content/uploads/2019/11/smartmicro-High-Performance-Automotive-Radar-PDF.pdf> | range < 0.25 m (medium range) and < 0.5 m (long-range modes); azimuth <= 0.5 deg; elevation <= 0.5 deg (UMRR-11), <= 2 deg (UMRR-96); radial velocity <= 0.1 m/s (UMRR-11), < 0.2 m/s (UMRR-96) | specification |
| R3 | Bosch Engineering, "Radar off-highway premium" data sheet (2024) | <https://www.bosch-engineering.com/media/industries/construction/bosch_engineering_ohw_premiumradar_datasheet_en_1125.pdf> | range 0.11-0.22 m; azimuth 0.1 deg; elevation 0.2 deg; radial velocity 0.04 m/s; velocity separability 0.17 m/s; up to 1,024 detections per cycle | specification |
| R4 | AUMOVIO (former Continental automotive business), technical data of the ARS540, ARS620, ARS51x and SRR52x | <https://www.aumovio.com/en/solutions/driver-assistance/automated-assisted-driving/radar-technology/ars540.html> (same path: ars620, ars51x, srr52x) | azimuth and elevation +-0.1 deg (ARS540); radial velocity +-0.08 and +-0.07 km/h (ARS620, SRR52x); cycle times | specification |
| R5 | H. Caesar et al., "nuScenes: A Multimodal Dataset for Autonomous Driving," CVPR 2020, pp. 11618-11628 | [10.1109/CVPR42600.2020.01164](https://doi.org/10.1109/CVPR42600.2020.01164) | radar returns per object fall from about 40 at 10 m to 10 at 50 m: motivates the higher miss rate | measured |
| R6 | O. Schumann et al., "RadarScenes: A Real-World Radar Point Cloud Data Set for Automotive Applications," IEEE FUSION 2021, pp. 1-8 | [10.23919/FUSION49465.2021.9627037](https://doi.org/10.23919/FUSION49465.2021.9627037) | azimuth 0.5 deg at boresight (nominal) and 2 deg at the +-60 deg edge of the field of view (severe, extreme); range 0.15 m and radial velocity 0.028 m/s of its sensors | specification reported by the dataset |
| R7 | F. Kraus, N. Scheiner, W. Ritter, K. Dietmayer, "The Radar Ghost Dataset - An Evaluation of Ghost Objects in Automotive Radar Data," IEEE/RSJ IROS 2021, pp. 8570-8577 | [10.1109/IROS51168.2021.9636338](https://doi.org/10.1109/IROS51168.2021.9636338) | about 2.3 ghost points per frame (about 100 k over 42,793 frames), rounded up to 3 false returns per sweep (nominal, severe); 819.91 detections per frame on average; Doppler resolution 0.087 m/s; 100 ms cycle | measured (scenes chosen near reflective surfaces: an upper-end urban rate) |
| R8 | A. Scheel, K. Dietmayer, "Tracking Multiple Vehicles Using a Variational Radar Model," IEEE T-ITS 20(10):3721-3736, 2019 | [10.1109/TITS.2018.2879041](https://doi.org/10.1109/TITS.2018.2879041) | detection probability P_D = 0.8, i.e. a 0.2 miss rate (nominal); Poisson clutter mean 30 per scan (extreme) | design value of a tracker on real data, not measured |
| R9 | P. Gao, S. Zhang, W. Wang, C. X. Lu, "DC-Loc: Accurate Automotive Radar Based Metric Localization with Explicit Doppler Compensation," ICRA 2022, pp. 4128-4134 | [10.1109/ICRA46639.2022.9811561](https://doi.org/10.1109/ICRA46639.2022.9811561) | range 0.25 m, azimuth 0.5 deg and radial velocity 0.1 m/s injected into CARLA radar (nominal) | design value of another simulation study |
| R10 | M. Morales, G. Habibi, "Synthesizing and Identifying Noise Levels in Autonomous Vehicle Camera-Radar Datasets," arXiv:2505.00584, 2025 | <https://arxiv.org/abs/2505.00584> | 0-4 ghost points per frame, context only | preprint, not peer reviewed |
| R11 | CARLA 0.9.15, sensors reference (radar) and source at the tag 0.9.15 | <https://carla.readthedocs.io/en/0.9.15/ref_sensors/#radar-sensor>; <https://github.com/carla-simulator/carla/blob/0.9.15/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Sensor/Radar.cpp> | the simulated radar: ray casting, no measurement noise, no false alarms, no resolution limits; blueprint defaults (30 x 30 deg, 100 m, 1,500 points/s); sign of the radial velocity | software documentation |
| K1 | J. Kopp et al., "Fast Rule-Based Clutter Detection in Automotive Radar Data," IEEE ITSC 2021, pp. 3010-3017 | [10.1109/ITSC48978.2021.9564776](https://doi.org/10.1109/ITSC48978.2021.9564776) | about 90 % clutter among the moving detections of a production mid-range radar in extra-urban traffic: a limitation of the uniform clutter model, not a profile value | measured |
| W1 | S. Hasirlioglu et al., "Test methodology for rain influence on automotive surround sensors," IEEE ITSC 2016 | [10.1109/ITSC.2016.7795918](https://doi.org/10.1109/ITSC.2016.7795918) | not used for any value: weather is not modelled | candidate (DOI verified, full text not read) |
| W2 | F. Norouzian et al., "Rain Attenuation at Millimeter Wave and Low-THz Frequencies," IEEE Trans. Antennas and Propagation 68(1):421-431, 2020 | [10.1109/TAP.2019.2938735](https://doi.org/10.1109/TAP.2019.2938735) | not used for any value: weather is not modelled | candidate (DOI verified, full text not read) |
| W3 | M. Holder et al., "Measurements revealing Challenges in Radar Sensor Modeling for Virtual Validation of Autonomous Driving," IEEE ITSC 2018 | [10.1109/ITSC.2018.8569423](https://doi.org/10.1109/ITSC.2018.8569423) | not used for any value: interference and sensor-model fidelity are not modelled | candidate (DOI verified, full text not read) |

The values that no source supports are engineering assumptions, named as such in `docs/robustness_profiles.md`:
the elevation sigmas of campaign v3 (the cited sensors are 2-D), the severe range and radial-velocity sigmas, the
0.40 miss rate, the share of ghost-like false returns, the 0.1 m range clip and the 1 m minimum false-return range.

### A.2 GNSS/INS (G0 ideal, G1 RTK, G2 degraded; 5G only as the transport of RTK corrections)

| key | source | DOI / URL | what it supports here | kind |
|---|---|---|---|---|
| N1 | M. Volckaert, D. Schellekens, K. Smolders, A. Simsky, B. Bougard, "Integrity of an RTK-INS positioning system using SSR corrections for safety-critical automotive applications," Septentrio technical presentation, 19 September 2019, slides 16 and 18 | <https://gnss-imu.com/down/upload/20240402/1712021876.pdf> | G1: horizontal position P95 4.0 cm (P99 5.3 cm) and horizontal velocity P95 1.6 cm/s (P99 2.9 cm/s) of RTK epochs | measured (technical presentation, not peer reviewed) |
| N2 | SBG Systems, "Automotive Tests in Urban Navigation," EUT#1 RTK + odometer, real-time results | <https://www.sbg-systems.com/test-reports/automotive-tests/> | G1: yaw P95 0.140 deg (2D position P95 0.246 m in that urban test) | measured (vendor test report) |
| N3 | R. Lesjak et al., "Centimeter-Level GNSS Positioning Using C-ITS for Correction Data Delivery: An Experimental Study," Lecture Notes in Mobility, Springer, 2025, pp. 565-571, Table 1 | [10.1007/978-3-032-06763-0_81](https://doi.org/10.1007/978-3-032-06763-0_81) | G2: 2D error P99.5 43.4 cm with C-ITS correction delivery (P95 3.1 cm; 4G: P95 2.4 cm, P99.5 37.9 cm; RTK-fixed 98.9 % and 98.8 %), the evidence that informs the rounded P99.5 = 0.50 m stress target | measured (peer reviewed) |
| N4 | SBG Systems, "Ellipse-D Automotive Test Report / Performance Assessment" | <https://www.sbg-systems.com/wp-content/uploads/SBG-Ellipse-automotive-test-report.pdf> | context for G2: yaw P99.7 0.444 / 0.477 deg and position P99.7 0.600 / 0.838 m (light urban / forest): 0.50 m is not the worst observed error | measured (vendor test report) |
| N5 | O. Elgarhy et al., "Development, Implementation and Field Trial of 5G Integrated GNSS-RTK Positioning in Cross-Border Settings," IEEE Future Networks World Forum 2024 | [10.1109/FNWF63303.2024.11028789](https://doi.org/10.1109/FNWF63303.2024.11028789) | feasibility of RTK corrections over 5G; no profile value | measured (feasibility only) |
| N6 | M. Hoffmann, P. Kryszkiewicz, G. P. Koudouridis, "Modeling of Real Time Kinematics localization error for use in 5G networks," EURASIP J. Wireless Communications and Networking 2020:31 | [10.1186/s13638-020-1641-8](https://doi.org/10.1186/s13638-020-1641-8) | the Gauss-Markov form of the position error (bias + Gauss-Markov + white) | modelling reference |
| N7 | u-blox, "ZED-F9R-02B Data Sheet," UBX-21017486, R06, 3 May 2024 | <https://content.u-blox.com/sites/default/files/ZED-F9R-02B_DataSheet_UBX-21017486.pdf> | velocity accuracy 0.05 m/s and dynamic heading 0.2 deg (68 %): the G2 heading and speed P99.5 targets are stress assumptions above these | specification |
| N8 | C. Marshall et al., "5G Precise Positioning Testbed - Technical Report," FrontierSI, January 2024 | <https://frontiersi.com.au/wp-content/uploads/2023/04/5G-Testbed-Technical-Report.pdf> | transport and integration of OSR/SSR corrections over 5G; no percentile is attributed to it | technical report |
| G7 | US DoD, "GPS Standard Positioning Service Performance Standard," 5th ed., April 2020 | <https://archive.gps.gov/technical/ps/2020-SPS-performance-standard.pdf> | the 1.96 factor between 95 % values and RMS used in the statistic conversions | standard |
| G8 | CAR 2 CAR Communication Consortium, "Vehicle C-ITS station profile," RS_2037, Release 1.6.10, 2026 | <https://www.car-2-car.org/fileadmin/documents/Basic_System_Profile/Release_1.6.10/C2CCC_RS_2037_Profile_R1610.pdf> | city speed confidence 0.6 m/s (95 %) of fused states, against which the independent velocity noise is discussed | specification |

The G1 targets (P95 0.040 m, 0.140 deg, 0.016 m/s) are the measured values of N1 and N2; the G2 targets (P99.5
0.50 m, 0.60 deg, 0.20 m/s) are engineering stress assumptions informed by N3, N4 and N7.  The error model
(stationary bias + Gauss-Markov + white position and heading, white velocity, the component splits and the
correlation times) is an engineering assumption calibrated to these targets (`docs/robustness_profiles.md`, section
"Current GNSS protocol").  5G is the transport of the RTK corrections only (N5, N8): no latency, availability or
radio behaviour is simulated or claimed.

Sources of the historical GNSS profiles (frozen campaign of 2026-10-15, `docs/archive/`), kept for the record:

| key | source | DOI / URL | kind |
|---|---|---|---|
| G1 | u-blox, "NEO-M8 - u-blox M8 concurrent GNSS modules - Data sheet," UBX-15031086, R14, 2025 | <https://content.u-blox.com/sites/default/files/NEO-M8-FW3_DataSheet_UBX-15031086.pdf> | specification |
| G2 | u-blox, "NEO-M9N-00B - Standard precision GNSS module - Data sheet," UBX-19014285, R08, 2025 | <https://content.u-blox.com/sites/default/files/NEO-M9N-00B_DataSheet_UBX-19014285.pdf> | specification |
| G3 | u-blox, "ZED-F9P-04B - High precision GNSS module - Data sheet," UBX-21044850, R05, 2024 | <https://content.u-blox.com/sites/default/files/ZED-F9P-04B_DataSheet_UBX-21044850.pdf> | specification |
| G4 | u-blox, "ZED-F9R-01B - High precision sensor fusion GNSS receiver - Data sheet," UBX-19054459, R06, 2023 | <https://cdn.sparkfun.com/assets/d/4/3/f/4/ZED-F9R-01B_Datasheet_UBX-19054459.pdf> | specification |
| G5 | Septentrio, "mosaic-X5 - Compact, multi-constellation GNSS receiver," brochure, 2019 (third-party mirror) | <https://components101.com/sites/default/files/2020-09/Mosaic-X5-Datasheet.pdf> | specification |
| G6 | OxTS, "RT3000 v4 DATASHEET" (no version or date printed) | <https://positics.fr/wp-content/uploads/2024/02/RT3000-v4-datasheet-1.pdf> | specification |
| G9 | L.-T. Hsu et al., "Hong Kong UrbanNav: An Open-Source Multisensory Dataset for Benchmarking Urban Navigation Algorithms," NAVIGATION 70(4), navi.602, 2023 | [10.33012/navi.602](https://doi.org/10.33012/navi.602) | measured |
| G10 | M. Olynik, M. Petovello, M. Cannon, G. Lachapelle, "Temporal impact of selected GPS errors on point positioning," GPS Solutions 6(1-2):47-57, 2002 | [10.1007/s10291-002-0011-9](https://doi.org/10.1007/s10291-002-0011-9) | measured |
| G11 | X. Niu et al., "Using Allan variance to analyze the error characteristics of GNSS positioning," GPS Solutions 18(2):231-242, 2014 (online 2013) | [10.1007/s10291-013-0324-x](https://doi.org/10.1007/s10291-013-0324-x) | measured |
| G12 | Y. Wang, X. Chen, P. Liu, "Statistical Multipath Model Based on Experimental GNSS Data in Static Urban Canyon Environment," Sensors 18(4):1149, 2018 | [10.3390/s18041149](https://doi.org/10.3390/s18041149) | measured |
| G13 | S. Jada, M. Joerger, "Measurement Error Time-Correlation Modeling for Safety-Critical Navigation," NAVIGATION 72(4), navi.721, 2025 | [10.33012/navi.721](https://doi.org/10.33012/navi.721) | modelling reference |

### A.3 Simulator

| key | source | DOI / URL | what it supports here |
|---|---|---|---|
| B63 | A. Dosovitskiy et al., "CARLA: An Open Urban Driving Simulator," CoRL 2017, PMLR 78:1-16 | <https://proceedings.mlr.press/v78/dosovitskiy17a.html> | the simulator of the 22 scenarios and of the ground truth (version 0.9.15) |
| R11 | CARLA 0.9.15 documentation and source | see A.1 | sensors, synchronous mode, collision sensor |

## Part B. Estimation methods implemented

| key | source | DOI | used in |
|---|---|---|---|
| M1 | R. E. Kalman, "A New Approach to Linear Filtering and Prediction Problems," J. Basic Engineering 82(1):35-45, 1960 | [10.1115/1.3662552](https://doi.org/10.1115/1.3662552) | the constant-velocity Kalman filter of each local radar track (`cdf.reconstruction.tracking`) |
| M2 | H. E. Rauch, F. Tung, C. T. Striebel, "Maximum likelihood estimates of linear dynamic systems," AIAA Journal 3(8):1445-1450, 1965 | [10.2514/3.3166](https://doi.org/10.2514/3.3166) | the backward Rauch-Tung-Striebel smoother of each track (offline reconstruction) |
| B35 | Y. Bar-Shalom, X.-R. Li, T. Kirubarajan, *Estimation with Applications to Tracking and Navigation*, Wiley, 2001 | [10.1002/0471221279](https://doi.org/10.1002/0471221279) | motion models, gating and filter consistency (Part C, [B35]) |
| B36 | S. J. Julier, J. K. Uhlmann, "A non-divergent estimation algorithm in the presence of unknown correlations," ACC 1997, 4:2369-2373 | [10.1109/ACC.1997.609105](https://doi.org/10.1109/ACC.1997.609105) | covariance intersection of several recorders' estimates of one road user (`cdf.reconstruction.anonymous`; Part C, [B36]) |
| B65 | J. C. Hayward, "Near-Miss Determination Through Use of a Scale of Danger," Highway Research Record 384:24-34, 1972 | <https://onlinepubs.trb.org/Onlinepubs/hrr/1972/384/384-004.pdf> | time to collision, the quantity behind CRITICAL_TTC (Part C, [B65]) |

# Part C. Related work and regulatory context

Paper: multi-vehicle accident reconstruction from partial onboard recordings (collision-anchored temporal alignment, identity association between recorders, cross-observer reconstruction of non-recording road users, global semantic event trace, replay from the reconstruction, per-vehicle perceivability/reaction event graphs as input to expert avoidability analysis; no liability determination). Target style: IEEE T-ITS.

Compiled and verified on 2026-10-10.

## C: How this list was verified

- **DOIs.** Every DOI below was resolved against the Crossref REST API (`api.crossref.org/works/<DOI>`). Title, authors, venue, year, volume/issue and pages were taken from the returned record. When I had recalled a DOI wrongly, Crossref returned a different paper. Four such cases were caught and corrected; see the notes at the end.
- **arXiv, PMLR and NeurIPS items.** These were checked with the arXiv API (`export.arxiv.org`) and on the official PMLR and NeurIPS proceedings pages (citation metadata).
- **Regulatory texts.** The full texts were downloaded from EUR-Lex (Official Journal HTML) and read locally. Other official sources:
  - UN Treaty Collection: adoption and entry-into-force dates.
  - UN ODS: ECE/TRANS/WP.29/2022/59/Rev.1, the R157 01 series, read as PDF.
  - Cornell LII: mirror of eCFR 49 CFR 563.
  - govinfo: the Federal Register final rule.
  - ntsb.gov, onlinepubs.trb.org and etsi.org: PDFs.
- **Relevance notes** are based on the abstracts, retrieved from Crossref/OpenAlex/Semantic Scholar/arXiv, or on the official text. Where no abstract was available, the note sticks to what the title and venue establish and says so.
- **Tags.** "Verified: Crossref" means the DOI record matches. "Verified: official PDF/page" means there is no DOI, but the document was opened at its publisher or authority. "[!]" marks a residual uncertainty, explained inline.
- **How it was compiled.** Outside the code: no LLM API was called from code; only bibliographic metadata APIs were queried.  Copied into the repository unchanged otherwise (then `docs/bibliography.md`, now Part C of `docs/REFERENCES.md`); the sources of the robustness profiles are in Part A.

## C: Counts

| # | Topic | Main entries | Verified alternates (Appendix A) |
|---|---|---|---|
| 1 | Traffic accident reconstruction | 9 | 7 |
| 2 | Avoidability, perception-reaction time | 8 | 4 |
| 3 | EDR / DSSAD (literature and standards) | 5, plus 9 regulatory instruments R1-R9 | 1 |
| 4 | Cooperative perception | 10 | 6 |
| 5 | MOT, track-to-track association and fusion | 10 | 6 |
| 6 | Decentralized/common-frame fusion, relative pose | 6 | 2 |
| 7 | Time synchronization from events, vehicle clocks | 8 | 5 |
| 8 | Digital twins, onboard data logging | 6 | 2 |
| 9 | R157 time gap, CARLA, TTC / safe distance | 7, plus the R157 table in the Regulatory facts | 3 |
| | **Total** | **69 (+9 regulatory)** | **36** |

---

## C.1 Traffic accident reconstruction (classical, EDR-based, video/data-based, simulation-based)

**[B1]** Steffan, H. & Moser, A., "The Collision and Trajectory Models of PC-CRASH," *SAE Technical Paper* 960886, 1996. DOI: [10.4271/960886](https://doi.org/10.4271/960886). Verified: Crossref.
*Relevance:* Describes the restitution/momentum impact model and the time-forward multi-vehicle dynamics simulation behind PC-Crash, the de-facto forensic simulation tool. It represents classical simulation-based reconstruction, which infers pre-crash motion from scene evidence instead of from onboard recordings.

**[B2]** Brach, R. M. & Brach, M. (R. Matthew), *Vehicle Accident Analysis and Reconstruction Methods*, 2nd ed., SAE International (R-397), 2011. DOI: [10.4271/R-397](https://doi.org/10.4271/R-397). Verified: Crossref. A 3rd edition exists (2022, DOI [10.4271/9781468603453](https://doi.org/10.4271/9781468603453)); Crossref lists J. Mason, R. M. Brach and M. Brach as its authors.
*Relevance:* Standard reference for physics-based reconstruction: impact mechanics, crush energy and uncertainty analysis. These are the classical methods our recorder-based reconstruction complements.

**[B3]** Burg, H. & Moser, A. (Eds.), *Handbuch Verkehrsunfallrekonstruktion*, 3rd ed., Springer Vieweg (ATZ/MTZ-Fachbuch), Wiesbaden, 2017. DOI: [10.1007/978-3-658-16143-9](https://doi.org/10.1007/978-3-658-16143-9). Verified: Crossref and SpringerLink (edition 3, chapter list).
*Relevance:* Practitioner handbook for accident experts, with a dedicated avoidability chapter ("A8 Vermeidbarkeitsbetrachtungen"). Our per-vehicle event graphs are designed to feed exactly this kind of expert analysis.

**[B4]** Gabler, H. C. et al., "Crash Severity: A Comparison of Event Data Recorder Measurements with Accident Reconstruction Estimates," *SAE Technical Paper* 2004-01-1194, 2004. DOI: [10.4271/2004-01-1194](https://doi.org/10.4271/2004-01-1194). Verified: Crossref.
*Relevance:* Compares EDR-recorded delta-V with reconstruction-code estimates (CRASH3/WinSMASH) on more than 500 NASS/CDS cases. It is early evidence that onboard recordings can replace or check reconstruction estimates, and of their limits.

**[B5]** Young, C.-P. et al., "Highway Vehicle Accident Reconstruction Using Cooperative Collision Warning Based Motor Vehicle Event Data Recorder," *Proc. IEEE Intelligent Vehicles Symposium (IV)*, pp. 1131-1136, 2009. DOI: [10.1109/IVS.2009.5164441](https://doi.org/10.1109/IVS.2009.5164441). Verified: Crossref; abstract via OpenAlex.
*Relevance:* The closest early precedent. An EDR also stores neighbours' states received over V2V cooperative collision warning, so that host and neighbour trajectories can be rebuilt. Our setting differs: neighbours are reconstructed post hoc from each recorder's own radar perception, without V2V.

**[B6]** Han, I., "Car speed estimation based on cross-ratio using video data of car-mounted camera (black box)," *Forensic Science International*, vol. 269, pp. 89-96, 2016. DOI: [10.1016/j.forsciint.2016.11.014](https://doi.org/10.1016/j.forsciint.2016.11.014). Verified: Crossref.
*Relevance:* Representative video/dashcam-based forensic reconstruction: speed from onboard video geometry. It is a single-observer, camera-only counterpart to our multi-observer radar-based reconstruction.

**[B7]** Bashetty, S. K. et al., "DeepCrashTest: Turning Dashcam Videos into Virtual Crash Tests for Automated Driving Systems," *Proc. IEEE ICRA*, pp. 11353-11360, 2020. DOI: [10.1109/ICRA40945.2020.9197053](https://doi.org/10.1109/ICRA40945.2020.9197053). Verified: Crossref.
*Relevance:* Extracts 3D vehicle trajectories from uncalibrated monocular crash videos and recreates the crashes in a simulator (video, then reconstruction, then simulation). It is related to our replay built only from the reconstruction.

**[B8]** Scanlon, J. M. et al., "Waymo simulated driving behavior in reconstructed fatal crashes within an autonomous vehicle operating domain," *Accident Analysis & Prevention*, vol. 163, 106454, 2021. DOI: [10.1016/j.aap.2021.106454](https://doi.org/10.1016/j.aap.2021.106454). Verified: Crossref.
*Relevance:* Reconstructs 72 real fatal crashes and re-simulates them counterfactually, replacing the initiator or the responder with an ADS. It is a reference for simulation-based reconstruction and for the initiator/responder framing of avoidability.

**[B9]** National Transportation Safety Board, "Collision Between Vehicle Controlled by Developmental Automated Driving System and Pedestrian, Tempe, Arizona, March 18, 2018," Highway Accident Report NTSB/HAR-19/03 (PB2019-101402), adopted 19 Nov 2019. No DOI. URL: <https://www.ntsb.gov/investigations/AccidentReports/Reports/HAR1903.pdf>. Verified: official PDF.
*Relevance:* A landmark investigation that used the ADS's own perception record. The ADS detected the pedestrian 5.6 s before impact. It tracked her until the crash without ever classifying her correctly. By the time it determined that a collision was imminent, the situation exceeded the response specifications of the ADS braking system. This is the "perceivable versus reacted" timeline that our event graphs make explicit.

## C.2 Avoidability analysis and perception-reaction time

**[B10]** Johansson, G. & Rumar, K., "Drivers' Brake Reaction Times," *Human Factors*, vol. 13, no. 1, pp. 23-27, 1971. DOI: [10.1177/001872087101300104](https://doi.org/10.1177/001872087101300104). Verified: Crossref.
*Relevance:* Classic on-road brake reaction-time distribution (321 drivers; surprise-corrected median about 0.9 s, 25 % above 1.2 s). It is a standard source for the reaction-time assumptions used in avoidability analysis.

**[B11]** Olson, P. L. & Sivak, M., "Perception-Response Time to Unexpected Roadway Hazards," *Human Factors*, vol. 28, no. 1, pp. 91-96, 1986. DOI: [10.1177/001872088602800110](https://doi.org/10.1177/001872088602800110). Verified: Crossref.
*Relevance:* Measures perception-response time from the first sighting of an unexpected obstacle (95th percentile about 1.6 s). It supports separating "hazard became perceivable" from "response began", as our event graphs do.

**[B12]** Green, M., "'How Long Does It Take to Stop?' Methodological Analysis of Driver Perception-Brake Times," *Transportation Human Factors*, vol. 2, no. 3, pp. 195-216, 2000. DOI: [10.1207/STHF0203_1](https://doi.org/10.1207/STHF0203_1). Verified: Crossref.
*Relevance:* Meta-analysis showing that driver expectation dominates perception-brake time: about 0.70-0.75 s when expected, about 1.25 s for unexpected but common signals, about 1.5 s for surprise. These are the ranges an expert would apply to our perceivability timestamps.

**[B13]** Markkula, G. et al., "A farewell to brake reaction times? Kinematics-dependent brake response in naturalistic rear-end emergencies," *Accident Analysis & Prevention*, vol. 95, pp. 209-226, 2016. DOI: [10.1016/j.aap.2016.07.007](https://doi.org/10.1016/j.aap.2016.07.007). Verified: Crossref.
*Relevance:* Shows that braking onset tracks kinematic urgency (visual looming) rather than a fixed reaction time after a "hazard onset". This argues for reporting perceivability and reaction as separate, kinematically contextualised events.

**[B14]** Engström, J. et al., "Modeling road user response timing in naturalistic traffic conflicts: A surprise-based framework," *Accident Analysis & Prevention*, vol. 198, 107460, 2024. DOI: [10.1016/j.aap.2024.107460](https://doi.org/10.1016/j.aap.2024.107460). Verified: Crossref.
*Relevance:* Tackles the stimulus-definition problem of response time in naturalistic conflicts: responses are relative to violated expectations. This bears directly on how we define when a hazard "became perceivable".

**[B15]** Kusano, K. D. & Gabler, H. C., "Safety Benefits of Forward Collision Warning, Brake Assist, and Autonomous Braking Systems in Rear-End Collisions," *IEEE Trans. Intelligent Transportation Systems*, vol. 13, no. 4, pp. 1546-1555, 2012. DOI: [10.1109/TITS.2012.2191542](https://doi.org/10.1109/TITS.2012.2191542). Verified: Crossref.
*Relevance:* Counterfactual re-simulation of 1,396 real rear-end crashes with a probabilistic driver-reaction model. It is a T-ITS precedent for "what-if" avoidability reasoning on reconstructed kinematics.

**[B16]** Mattas, K. et al., "Driver models for the definition of safety requirements of automated vehicles in international regulations. Application to motorway driving conditions," *Accident Analysis & Prevention*, vol. 174, 106743, 2022. DOI: [10.1016/j.aap.2022.106743](https://doi.org/10.1016/j.aap.2022.106743). Verified: Crossref.
*Relevance:* Compares the UN R157 preventable/unpreventable driver models with RSS and the Fuzzy Safety Model (FSM). The FSM was proposed for the R157 amendment and is now "Performance model 2" in the 01-series Annex 3 (see the Regulatory facts).

**[B17]** Scanlon, J. M. et al., "Collision Avoidance Effectiveness of an Automated Driving System Using a Human Driver Behavior Reference Model in Reconstructed Fatal Collisions," *SAE Technical Paper* 2026-01-0520, 2026. DOI: [10.4271/2026-01-0520](https://doi.org/10.4271/2026-01-0520). Verified: Crossref.
*Relevance:* Benchmarks an ADS against a "non-impaired, eyes on conflict" (NIEON) human reference model in reconstructed crashes. It is a formalised avoidability reference that could consume our perceivability and reaction timestamps.

## C.3 Event data recorders and DSSAD (literature and industry standards; the regulations are in the Regulatory facts)

**[B18]** Kowalick, T. M., *Fatal Exit: The Automotive Black Box Debate*, Wiley, 2004 (Crossref date; often cited as 2005). DOI: [10.1002/0471715964](https://doi.org/10.1002/0471715964). Verified: Crossref.
*Relevance:* Book-length account of the automotive black-box (EDR) debate. It is background for why regulated EDR content is deliberately narrow.

**[B19]** Böhm, K. et al., "New developments on EDR (Event Data Recorder) for automated vehicles," *Open Engineering*, vol. 10, no. 1, pp. 140-146, 2020. DOI: [10.1515/eng-2020-0007](https://doi.org/10.1515/eng-2020-0007). Verified: Crossref.
*Relevance:* Argues from real-accident reconstructions and crash tests that automated vehicles need a data basis broader than 49 CFR 563: the AHEAD data model, including object data and camera feeds. It directly supports our assumption of perception logging beyond today's EDR.

**[B20]** Yao, Y. & Atkins, E., "The Smart Black Box: A Value-Driven High-Bandwidth Automotive Event Data Recorder," *IEEE Trans. Intelligent Transportation Systems*, vol. 22, no. 3, pp. 1484-1496, 2021. DOI: [10.1109/TITS.2020.2971385](https://doi.org/10.1109/TITS.2020.2971385). Verified: Crossref.
*Relevance:* Value-driven buffering and compression for high-bandwidth AV sensor recording under finite storage. It is a design point for the onboard perception recorders our method consumes.

**[B21]** SAE International, Event Data Recorder Committee, "Automated Driving System Data Logger," SAE **J3197** (Recommended Practice), issued 2020-04, revised 2021-07. DOI: [10.4271/J3197_202107](https://doi.org/10.4271/J3197_202107) (2020 issue: [10.4271/J3197_202004](https://doi.org/10.4271/J3197_202004)). Verified: Crossref. [!] Scope taken from the SAE Mobilus abstract; the full text is paywalled and was not read.
*Relevance:* Industry recommended practice for ADS-specific data elements (SAE Level 3-5 features) that supplement the SAE J1698 EDR record for post-crash analysis. It sits between the regulated EDR and full perception logging.

**[B22]** IEEE, "IEEE Standard for Data Storage Systems for Automated Driving," IEEE Std **1616.1-2023**. DOI: [10.1109/IEEESTD.2023.10205988](https://doi.org/10.1109/IEEESTD.2023.10205988). Verified: Crossref (title and DOI). [!] The standard number and scope come from standards-retailer listings; the full text was not read.
*Relevance:* Voluntary standard defining DSSAD functions, metrics and data elements, including an EDR/DSSAD element compendium for M1/N1 vehicles with automated driving.

## C.4 Cooperative perception (V2V/V2X datasets and methods)

**[B23]** Xu, R. et al., "OPV2V: An Open Benchmark Dataset and Fusion Pipeline for Perception with Vehicle-to-Vehicle Communication," *Proc. IEEE ICRA*, pp. 2583-2589, 2022. DOI: [10.1109/ICRA46639.2022.9812038](https://doi.org/10.1109/ICRA46639.2022.9812038). Verified: Crossref and arXiv:2109.07644.
*Relevance:* CARLA-based V2V perception benchmark comparing early, late and intermediate fusion. It is the closest public setting (CARLA, several equipped vehicles), and our track-level fusion belongs to its late-fusion family.

**[B24]** Li, Y. et al., "V2X-Sim: Multi-Agent Collaborative Perception Dataset and Benchmark for Autonomous Driving," *IEEE Robotics and Automation Letters*, vol. 7, no. 4, pp. 10914-10921, 2022. DOI: [10.1109/LRA.2022.3192802](https://doi.org/10.1109/LRA.2022.3192802). Verified: Crossref.
*Relevance:* Simulated multi-agent recordings (vehicles plus roadside unit) with ground truth for detection, tracking and segmentation. It is a reference multi-observer dataset design.

**[B25]** Yu, H. et al., "DAIR-V2X: A Large-Scale Dataset for Vehicle-Infrastructure Cooperative 3D Object Detection," *Proc. IEEE/CVF CVPR*, pp. 21329-21338, 2022. DOI: [10.1109/CVPR52688.2022.02067](https://doi.org/10.1109/CVPR52688.2022.02067). Verified: Crossref and arXiv:2204.05575.
*Relevance:* A real-world dataset that explicitly raises temporal asynchrony between vehicle and infrastructure sensors and proposes Time Compensation Late Fusion. Our collision anchoring addresses the same timing issue, post hoc and across recorders.

**[B26]** Xu, R. et al., "V2X-ViT: Vehicle-to-Everything Cooperative Perception with Vision Transformer," in *Computer Vision - ECCV 2022*, LNCS, Springer, pp. 107-124, 2022. DOI: [10.1007/978-3-031-19842-7_7](https://doi.org/10.1007/978-3-031-19842-7_7). Verified: Crossref and arXiv:2203.10638.
*Relevance:* Intermediate-fusion transformer designed for asynchronous sharing, pose errors and heterogeneous agents (dataset built with CARLA/OpenCDA). It represents learned online fusion, in contrast to our offline forensic track fusion.

**[B27]** Hu, Y. et al., "Where2comm: Communication-Efficient Collaborative Perception via Spatial Confidence Maps," *Advances in Neural Information Processing Systems 35 (NeurIPS 2022)*, pp. 4874-4886, 2022. DOI: [10.52202/068431-0352](https://doi.org/10.52202/068431-0352); arXiv:2209.12836. Verified: Crossref and NeurIPS proceedings page.
*Relevance:* Bandwidth-aware collaborative perception that shares only perceptually critical regions. It contrasts with our offline setting, where all recordings are available after the crash.

**[B28]** Xu, R. et al., "CoBEVT: Cooperative Bird's Eye View Semantic Segmentation with Sparse Transformers," *Proc. Conference on Robot Learning (CoRL 2022)*, PMLR vol. 205, pp. 989-1000 (published 2023). No DOI. URL: <https://proceedings.mlr.press/v205/xu23a.html>; arXiv:2207.02202. Verified: PMLR page and arXiv.
*Relevance:* Multi-agent multi-camera BEV fusion (evaluated on OPV2V). It completes the intermediate-fusion family for the related-work section.

**[B29]** Rauch, A. et al., "Car2X-based perception in a high-level fusion architecture for cooperative perception systems," *Proc. IEEE IV*, pp. 270-275, 2012. DOI: [10.1109/IVS.2012.6232130](https://doi.org/10.1109/IVS.2012.6232130). Verified: Crossref; abstract via OpenAlex.
*Relevance:* Models received object data as a virtual sensor in a high-level (track) fusion architecture. Temporal alignment uses CTRA prediction; spatial alignment transforms the data with its uncertainty via an unscented transform. It is the closest classical analogue to our common-frame cross-observer fusion.

**[B30]** Allig, C. & Wanielik, G., "Alignment of Perception Information for Cooperative Perception," *Proc. IEEE IV*, pp. 1849-1854, 2019. DOI: [10.1109/IVS.2019.8814108](https://doi.org/10.1109/IVS.2019.8814108). Verified: Crossref.
*Relevance:* Reviews and evaluates temporal and spatial alignment of shared track-level objects (sender-motion compensation versus non-predicted sender state). This is directly relevant to transforming one recorder's tracks into another's frame or into a common frame.

**[B31]** Chiu, H.-K. et al., "Probabilistic 3D Multi-Object Cooperative Tracking for Autonomous Driving via Differentiable Multi-Sensor Kalman Filter," *Proc. IEEE ICRA*, pp. 18458-18464, 2024. DOI: [10.1109/ICRA57147.2024.10610487](https://doi.org/10.1109/ICRA57147.2024.10610487). Verified: Crossref.
*Relevance:* Cooperative multi-object tracking with learned per-detection measurement uncertainty, evaluated on V2V4Real. It is a recent tracking-level counterpart to our cross-observer fusion.

**[B32]** ETSI, "Intelligent Transport System (ITS); Vehicular Communications; Basic Set of Applications; Collective Perception Service; Release 2," ETSI TS 103 324 V2.1.1 (2023-06). No DOI. URL: <https://www.etsi.org/deliver/etsi_ts/103300_103399/103324/02.01.01_60/ts_103324v020101p.pdf>. Verified: official PDF (title page).
*Relevance:* Standardised sharing of perceived objects (collective perception) between ITS stations. It shows the object/track-list abstraction that our recorders' tracked radar output resembles.

## C.5 Multi-object tracking, track-to-track association and fusion

**[B33]** Bar-Shalom, Y., "On the track-to-track correlation problem," *IEEE Trans. Automatic Control*, vol. 26, no. 2, pp. 571-572, 1981. DOI: [10.1109/TAC.1981.1102635](https://doi.org/10.1109/TAC.1981.1102635). Verified: Crossref.
*Relevance:* Hypothesis test for whether two tracks represent the same target, accounting for the correlation between the track estimates. It is the basic T2T association test across observers.

**[B34]** Bar-Shalom, Y. & Campo, L., "The Effect of the Common Process Noise on the Two-Sensor Fused-Track Covariance," *IEEE Trans. Aerospace and Electronic Systems*, vol. AES-22, no. 6, pp. 803-805, 1986. DOI: [10.1109/TAES.1986.310815](https://doi.org/10.1109/TAES.1986.310815). Verified: Crossref.
*Relevance:* Quantifies the cross-covariance that common process noise induces when fusing two sensors' tracks. It justifies correlation-aware (or covariance-intersection) fusion of observer tracks.

**[B35]** Bar-Shalom, Y. et al. (with X.-R. Li and T. Kirubarajan), *Estimation with Applications to Tracking and Navigation*, Wiley, 2001. Crossref lists the online date as 2002. DOI: [10.1002/0471221279](https://doi.org/10.1002/0471221279). Verified: Crossref.
*Relevance:* Textbook reference for Kalman filtering, motion models and filter-consistency tests, as used in per-recorder tracking and smoothing.

**[B36]** Julier, S. J. & Uhlmann, J. K., "A non-divergent estimation algorithm in the presence of unknown correlations," *Proc. American Control Conference*, vol. 4, pp. 2369-2373, 1997. DOI: [10.1109/ACC.1997.609105](https://doi.org/10.1109/ACC.1997.609105). Verified: Crossref.
*Relevance:* Covariance intersection: consistent fusion when the cross-correlations between estimates are unknown, as for tracks from independent vehicles.

**[B37]** Chong, C.-Y. et al. (with S. Mori, W. H. Barker and K.-C. Chang), "Architectures and algorithms for track association and fusion," *IEEE Aerospace and Electronic Systems Magazine*, vol. 15, no. 1, pp. 5-13, 2000. DOI: [10.1109/62.821657](https://doi.org/10.1109/62.821657). Verified: Crossref.
*Relevance:* Sensor-to-sensor versus sensor-to-system track fusion, with association and fusion that account for correlated track errors. It is the architectural frame for our observer-to-global-trace fusion.

**[B38]** Granström, K. et al. (with M. Baum and S. Reuter), "Extended Object Tracking: Introduction, Overview and Applications," *Journal of Advances in Information Fusion*, vol. 12, no. 2, pp. 139-174, 2017. No DOI. arXiv:1604.00970. Verified: arXiv (journal reference) and Chalmers research record. [!] The arXiv journal-ref says "December 2016"; Chalmers lists 2017.
*Relevance:* Survey of extended-object tracking (multiple detections per object, shape estimation). It grounds the handling of observers that see different faces of the same vehicle.

**[B39]** Kuhn, H. W., "The Hungarian method for the assignment problem," *Naval Research Logistics Quarterly*, vol. 2, no. 1-2, pp. 83-97, 1955. DOI: [10.1002/nav.3800020109](https://doi.org/10.1002/nav.3800020109). Verified: Crossref.
*Relevance:* Optimal one-to-one assignment, used for track-to-track and recorder-identity association.

**[B40]** Aeberhard, M. et al., "Track-to-Track Fusion With Asynchronous Sensors Using Information Matrix Fusion for Surround Environment Perception," *IEEE Trans. Intelligent Transportation Systems*, vol. 13, no. 4, pp. 1717-1726, 2012. DOI: [10.1109/TITS.2012.2202229](https://doi.org/10.1109/TITS.2012.2202229). Verified: Crossref; abstract via OpenAlex.
*Relevance:* Automotive high-level T2T fusion of asynchronous sensors via information matrix fusion, keeping global tracks across fields of view. It is the automotive precedent for fusing asynchronous track lists.

**[B41]** Hammarstrand, L. et al., "Extended Object Tracking using a Radar Resolution Model," *IEEE Trans. Aerospace and Electronic Systems*, vol. 48, no. 3, pp. 2371-2386, 2012. DOI: [10.1109/TAES.2012.6237597](https://doi.org/10.1109/TAES.2012.6237597). Verified: Crossref.
*Relevance:* Radar model for vehicles with multiple resolved reflection centres. It explains why radar tracks from different viewpoints refer to different points on the same vehicle.

**[B42]** Bernardin, K. & Stiefelhagen, R., "Evaluating Multiple Object Tracking Performance: The CLEAR MOT Metrics," *EURASIP Journal on Image and Video Processing*, vol. 2008, 246309, 2008. DOI: [10.1155/2008/246309](https://doi.org/10.1155/2008/246309). Verified: Crossref.
*Relevance:* MOTA/MOTP metrics for evaluating the reconstructed tracks of non-recording road users against simulator ground truth.

## C.6 Decentralized / common-frame fusion and relative pose between vehicles

**[B43]** Umeyama, S., "Least-squares estimation of transformation parameters between two point patterns," *IEEE Trans. Pattern Analysis and Machine Intelligence*, vol. 13, no. 4, pp. 376-380, 1991. DOI: [10.1109/34.88573](https://doi.org/10.1109/34.88573). Verified: Crossref.
*Relevance:* Closed-form rigid/similarity transform between corresponding point sets, for example estimating a recorder-to-common-frame transform from matched trajectories.

**[B44]** Besl, P. J. & McKay, N. D., "A method for registration of 3-D shapes," *IEEE Trans. Pattern Analysis and Machine Intelligence*, vol. 14, no. 2, pp. 239-256, 1992. DOI: [10.1109/34.121791](https://doi.org/10.1109/34.121791). Verified: Crossref.
*Relevance:* ICP, the baseline registration method when correspondences between observers are unknown.

**[B45]** Grime, S. & Durrant-Whyte, H. F., "Data fusion in decentralized sensor networks," *Control Engineering Practice*, vol. 2, no. 5, pp. 849-863, 1994. DOI: [10.1016/0967-0661(94)90349-2](https://doi.org/10.1016/0967-0661%2894%2990349-2). Verified: Crossref.
*Relevance:* Foundational decentralized data-fusion architecture with no central fusion node. It is the conceptual basis for fusing estimates produced independently by each vehicle.

**[B46]** Alam, N. et al., "Relative Positioning Enhancement in VANETs: A Tight Integration Approach," *IEEE Trans. Intelligent Transportation Systems*, vol. 14, no. 1, pp. 47-55, 2013. DOI: [10.1109/TITS.2012.2205381](https://doi.org/10.1109/TITS.2012.2205381). Verified: Crossref; abstract via OpenAlex.
*Relevance:* Improves vehicle-to-vehicle relative positioning by fusing shared low-level GPS data, outperforming DGPS without radio ranging. It is relevant to GNSS-based alignment of the recorders' frames.

**[B47]** Héry, E. et al., "Consistent decentralized cooperative localization for autonomous vehicles using LiDAR, GNSS, and HD maps," *Journal of Field Robotics*, vol. 38, no. 4, pp. 552-571, 2021. DOI: [10.1002/rob.22004](https://doi.org/10.1002/rob.22004). Verified: Crossref.
*Relevance:* Consistent decentralized fusion under unknown correlations, combined with LiDAR/ICP relative pose estimation between vehicles and GNSS bias correction. It is close to our common-frame problem.

**[B48]** Vadivelu, N. et al., "Learning to Communicate and Correct Pose Errors," *Proc. Conference on Robot Learning (CoRL 2020)*, PMLR vol. 155, pp. 1195-1210 (published 2021). No DOI. URL: <https://proceedings.mlr.press/v155/vadivelu21a.html>; arXiv:2011.05289. Verified: PMLR page and arXiv.
*Relevance:* Learns to detect and correct relative pose noise between communicating vehicles before fusion. It shows how sensitive multi-vehicle fusion is to frame misalignment.

## C.7 Time synchronization (event-based alignment, sensor and vehicle clocks)

**[B49]** Elson, J. et al., "Fine-grained network time synchronization using reference broadcasts," *ACM SIGOPS Operating Systems Review*, vol. 36 (SI, OSDI 2002), pp. 147-163, 2002. DOI: [10.1145/844128.844143](https://doi.org/10.1145/844128.844143). Verified: Crossref; abstract via OpenAlex.
*Relevance:* Reference-Broadcast Synchronization: receivers align their clocks using the arrival time of a common event rather than sender timestamps. This is the same principle as anchoring recorders on a shared collision.

**[B50]** IEEE, "IEEE Standard for a Precision Clock Synchronization Protocol for Networked Measurement and Control Systems," IEEE Std 1588-2019 (published 2020). DOI: [10.1109/IEEESTD.2020.9120376](https://doi.org/10.1109/IEEESTD.2020.9120376). Verified: Crossref.
*Relevance:* PTP, the clock-synchronization protocol family. It shows what synchronised recorders would require, which independent vehicles do not share.

**[B51]** IEEE, "IEEE Standard for Local and Metropolitan Area Networks - Timing and Synchronization for Time-Sensitive Applications," IEEE Std 802.1AS-2020. DOI: [10.1109/IEEESTD.2020.9121845](https://doi.org/10.1109/IEEESTD.2020.9121845). Verified: Crossref.
*Relevance:* gPTP, the time-synchronization basis of TSN and in-vehicle Ethernet. It provides intra-vehicle time only, not a common time base across vehicles.

**[B52]** Westenberger, A. et al., "Temporal synchronization in multi-sensor fusion for future driver assistance systems," *Proc. IEEE ISPCS*, pp. 93-98, 2011. DOI: [10.1109/ISPCS.2011.6070146](https://doi.org/10.1109/ISPCS.2011.6070146). Verified: Crossref; abstract via OpenAlex.
*Relevance:* Recovers millisecond-accurate measurement timestamps for automotive sensors that lack them, handling clock drift and frame drops. It is the intra-vehicle precursor of inter-recorder alignment.

**[B53]** Olson, E., "A passive solution to the sensor synchronization problem," *Proc. IEEE/RSJ IROS*, pp. 1059-1064, 2010. DOI: [10.1109/IROS.2010.5650579](https://doi.org/10.1109/IROS.2010.5650579). Verified: Crossref.
*Relevance:* Estimates the sensor-to-host clock mapping passively from arrival timestamps. It is a reference for offset/skew estimation without cooperation from the clock source.

**[B54]** Caspi, Y. & Irani, M., "Spatio-temporal alignment of sequences," *IEEE Trans. Pattern Analysis and Machine Intelligence*, vol. 24, no. 11, pp. 1409-1424, 2002. DOI: [10.1109/TPAMI.2002.1046148](https://doi.org/10.1109/TPAMI.2002.1046148). Verified: Crossref.
*Relevance:* Jointly aligns, in time and space, unsynchronised recordings of the same dynamic scene by exploiting the scene dynamics. This is analogous to aligning vehicle recordings through events that several of them observed.

**[B55]** Shrestha, P. et al., "Synchronization of multiple video recordings based on still camera flashes," *Proc. ACM Multimedia*, pp. 137-140, 2006. DOI: [10.1145/1180639.1180679](https://doi.org/10.1145/1180639.1180679). Verified: Crossref; abstract via OpenAlex.
*Relevance:* Recovers time offsets between independent recorders by matching sharp shared events (flashes). It is a direct analogue of collision-anchored alignment.

**[B56]** Bannach, D. et al., "Automatic Event-Based Synchronization of Multimodal Data Streams from Wearable and Ambient Sensors," in *Smart Sensing and Context (EuroSSC 2009)*, LNCS, Springer, pp. 135-148, 2009. DOI: [10.1007/978-3-642-04471-7_11](https://doi.org/10.1007/978-3-642-04471-7_11). Verified: Crossref. [!] No abstract in the indexes used; the note relies on the title.
*Relevance:* Event-based synchronization of independently clocked multimodal sensor streams. It is a methodological precedent for cross-modal event matching, for example collision sensor against odometry or IMU.

## C.8 Vehicle digital twins and onboard perception/data logging

**[B57]** Grieves, M. & Vickers, J., "Digital Twin: Mitigating Unpredictable, Undesirable Emergent Behavior in Complex Systems," in *Transdisciplinary Perspectives on Complex Systems*, Springer, pp. 85-113, 2017. DOI: [10.1007/978-3-319-38756-7_4](https://doi.org/10.1007/978-3-319-38756-7_4). Verified: Crossref.
*Relevance:* Widely cited origin of the digital-twin concept. It frames our replay as a post-hoc twin of the accident built only from recorded data.

**[B58]** Schwarz, C. & Wang, Z., "The Role of Digital Twins in Connected and Automated Vehicles," *IEEE Intelligent Transportation Systems Magazine*, vol. 14, no. 6, pp. 41-51, 2022. DOI: [10.1109/MITS.2021.3129524](https://doi.org/10.1109/MITS.2021.3129524). Verified: Crossref.
*Relevance:* Review of vehicular digital twins and their defining data link between the physical system and the model. It positions reconstruction-driven replay among CAV twin applications.

**[B59]** Wang, Z. et al., "Mobility Digital Twin: Concept, Architecture, Case Study, and Future Challenges," *IEEE Internet of Things Journal*, vol. 9, no. 18, pp. 17452-17467, 2022. DOI: [10.1109/JIOT.2022.3156028](https://doi.org/10.1109/JIOT.2022.3156028). Verified: Crossref.
*Relevance:* Human/vehicle/traffic digital-twin framework. It contextualises vehicle-level twins built from onboard data.

**[B60]** Klitzke, L. et al., "Real-world Test Drive Vehicle Data Management System for Validation of Automated Driving Systems," *Proc. VEHITS 2019*, SciTePress, pp. 171-180, 2019. DOI: [10.5220/0007720501710180](https://doi.org/10.5220/0007720501710180). Verified: Crossref.
*Relevance:* Management of recorded vehicle sensor data, aggregated into time series of scenes for scenario mining. It covers the logging and analysis side of the data our method ingests.

**[B61]** Caesar, H. et al., "nuScenes: A Multimodal Dataset for Autonomous Driving," *Proc. IEEE/CVF CVPR*, pp. 11618-11628, 2020. DOI: [10.1109/CVPR42600.2020.01164](https://doi.org/10.1109/CVPR42600.2020.01164). Verified: Crossref.
*Relevance:* A widely used per-vehicle multimodal log that includes automotive radar. It is an example of what raw onboard perception logs contain.

**[B62]** Schumann, O. et al., "RadarScenes: A Real-World Radar Point Cloud Data Set for Automotive Applications," *Proc. IEEE FUSION*, pp. 1-8, 2021. DOI: [10.23919/FUSION49465.2021.9627037](https://doi.org/10.23919/FUSION49465.2021.9627037). Verified: Crossref.
*Relevance:* Series-production radar detections (four sensors) with point-wise annotations of moving road users. It is a realistic reference for the raw radar data our recorders store.

## C.9 UN R157 following distance, CARLA, time-to-collision and safe distance

The UN R157 minimum time-gap table, transcribed from the official text, is in the Regulatory facts, section F.

**[B63]** Dosovitskiy, A. et al., "CARLA: An Open Urban Driving Simulator," *Proc. 1st Conference on Robot Learning (CoRL 2017)*, PMLR vol. 78, pp. 1-16, 2017. No DOI. URL: <https://proceedings.mlr.press/v78/dosovitskiy17a.html>; arXiv:1711.03938. Verified: PMLR page and arXiv.
*Relevance:* The simulator used to generate the multi-vehicle accident recordings and the ground truth.

**[B64]** Shalev-Shwartz, S. et al., "On a Formal Model of Safe and Scalable Self-driving Cars," arXiv:1708.06374, 2017. No DOI. URL: <https://arxiv.org/abs/1708.06374>. Verified: arXiv.
*Relevance:* Responsibility-Sensitive Safety (RSS): safe longitudinal and lateral distances with an explicit response time. It is an alternative safe-distance criterion to the R157 time-gap table.

**[B65]** Hayward, J. C., "Near-Miss Determination Through Use of a Scale of Danger," *Highway Research Record* 384, Highway Research Board, pp. 24-34, 1972. No DOI. URL: <https://onlinepubs.trb.org/Onlinepubs/hrr/1972/384/384-004.pdf>. Verified: official TRB PDF.
*Relevance:* Origin of time-to-collision as a measurable "scale of danger" for traffic conflicts.

**[B66]** Minderhoud, M. M. & Bovy, P. H. L., "Extended time-to-collision measures for road traffic safety assessment," *Accident Analysis & Prevention*, vol. 33, no. 1, pp. 89-97, 2001. DOI: [10.1016/S0001-4575(00)00019-1](https://doi.org/10.1016/S0001-4575%2800%2900019-1). Verified: Crossref.
*Relevance:* Time-exposed and time-integrated TTC (TET/TIT). These aggregate TTC indicators can summarise criticality per vehicle.

**[B67]** Vogel, K., "A comparison of headway and time to collision as safety indicators," *Accident Analysis & Prevention*, vol. 35, no. 3, pp. 427-433, 2003. DOI: [10.1016/S0001-4575(02)00022-2](https://doi.org/10.1016/S0001-4575%2802%2900022-2). Verified: Crossref.
*Relevance:* Distinguishes headway/time gap (the R157-style following distance) from TTC as safety indicators. Both kinds of predicate appear in our event semantics.

**[B68]** Westhofen, L. et al., "Criticality Metrics for Automated Driving: A Review and Suitability Analysis of the State of the Art," *Archives of Computational Methods in Engineering*, vol. 30, no. 1, pp. 1-35, 2023. DOI: [10.1007/s11831-022-09788-7](https://doi.org/10.1007/s11831-022-09788-7). Verified: Crossref.
*Relevance:* Comprehensive review of TTC, headway, RSS-type and other criticality metrics, with a suitability analysis. It supports the choice and definition of our event predicates.

**[B69]** Mattas, K. et al., "Fuzzy Surrogate Safety Metrics for real-time assessment of rear-end collision risk. A study based on empirical observations," *Accident Analysis & Prevention*, vol. 148, 105794, 2020. DOI: [10.1016/j.aap.2020.105794](https://doi.org/10.1016/j.aap.2020.105794). Verified: Crossref.
*Relevance:* Defines the PFS and CFS fuzzy surrogate safety metrics and compares them with RSS distance and TTC. They underpin "Performance model 2" in the R157 01-series Annex 3.

---

## C: Regulatory facts (EDR / DSSAD / GSR)

All article, paragraph and annex numbers below were read in the official texts listed in R1-R9. Short quotes are verbatim.

### R. Instruments (cite these)

| ID | Instrument | Date / publication | Status / URL |
|---|---|---|---|
| R1 | **Regulation (EU) 2019/2144** (General Safety Regulation, GSR) | 27 Nov 2019; OJ L 325, 16.12.2019, p. 1-40 | Applies from 6 Jul 2022 (Art. 19). <https://eur-lex.europa.eu/eli/reg/2019/2144/oj> |
| R2 | **Commission Delegated Regulation (EU) 2022/545**: EDR type-approval for M1/N1 and as a separate technical unit; amends GSR Annexes I and II | 26 Jan 2022; OJ L 107, 6.4.2022, p. 18-23 | Applies from 6 Jul 2022 (Art. 8). <https://eur-lex.europa.eu/eli/reg_del/2022/545/oj> |
| R3 | **Commission Delegated Regulation (EU) 2024/2220**: EDR type-approval for heavy-duty M2/M3/N2/N3 | 26 Jul 2024; OJ L, 2024/2220, 2.10.2024 | Applies from 7 Jan 2026 (Art. 7). <https://eur-lex.europa.eu/eli/reg_del/2024/2220/oj> |
| R4 | **Commission Implementing Regulation (EU) 2022/1426**: type-approval of the ADS of fully automated vehicles | 5 Aug 2022; OJ L 221, 26.8.2022, p. 1 | In force on the 20th day after publication (Art. 4). <https://eur-lex.europa.eu/eli/reg_impl/2022/1426/oj> |
| R5 | **UN Regulation No. 160**: Event Data Recorder (M1, N1) | Original: OJ L 221, 21.6.2021, p. 15 (as cited in R2). Draft notified 30 Mar 2021 (C.N.111.2021, doc. ECE/TRANS/WP.29/2020/123/Rev.1). Entry into force **30 Sep 2021** (UN Treaty Collection). **01 series**: OJ L 265, 26.7.2021, p. 3 [2021/1215], authentic text ECE/TRANS/WP.29/2021/58 | [!] The OJ gives the 01-series entry into force as "TBC". <https://eur-lex.europa.eu/eli/reg/2021/1215/oj> |
| R6 | **UN Regulation No. 169**: EDR for heavy-duty vehicles (M2, M3, N2, N3) | OJ L, 2024/1218, 23.5.2024; entry into force **19 Jun 2024**; authentic text ECE/TRANS/WP.29/2023/134/Rev.1 | <https://eur-lex.europa.eu/eli/reg/2024/1218/oj> |
| R7 | **UN Regulation No. 157**: Automated Lane Keeping Systems, original version | Adopted 24 Jun 2020 (UN Treaty Collection); entry into force **22 Jan 2021**; OJ L 82, 9.3.2021, p. 75 [2021/389]; authentic text ECE/TRANS/WP.29/2020/81 | <https://eur-lex.europa.eu/eli/reg/2021/389/oj> |
| R8 | **UN R157, 01 series of amendments**: ECE/TRANS/WP.29/2022/59/Rev.1 (30 May 2022), considered at WP.29 187th session (21-24 Jun 2022) | Entry into force **4 Jan 2023** | [!] Date from GlobalAutoRegs, a secondary source; confirm in UNECE TRANS/WP.29/343. Text read from UN ODS: <https://documents.un.org/api/symbol/access?s=ECE/TRANS/WP.29/2022/59/Rev.1&l=en&t=pdf> |
| R9 | **US 49 CFR Part 563**: Event Data Recorders. Final rule **89 FR 102810-102834** (18 Dec 2024; docket NHTSA-2024-0084; RIN 2127-AM12; effective 17 Jan 2025), amended at 91 FR 28440 (18 May 2026) | See section E | <https://www.govinfo.gov/content/pkg/FR-2024-12-18/html/2024-29862.htm> |

### A. EU General Safety Regulation (R1): what it mandates

- **Art. 3(13): definition.** An EDR is "a system with the only purpose of recording and storing critical crash-related parameters and information shortly before, during and immediately after a collision".
- **Art. 6(1)(g): obligation.** Motor vehicles shall be equipped with an "event data recorder". It is one of seven advanced vehicle systems listed in Art. 6(1)(a)-(g).
- **Art. 6(4)(a): content.** Data recorded "shortly before, during and immediately after a collision" shall include:
  - the vehicle's speed, braking, and position and tilt on the road;
  - the state and rate of activation of all its safety systems;
  - the 112-based eCall system;
  - brake activation and the relevant input parameters of the onboard active safety and accident-avoidance systems;
  - all of this "with high level of accuracy and ensured survivability of data".
- **Art. 6(4)(b)-(d): operation and access.**
  - The EDR cannot be deactivated.
  - It operates as a closed loop.
  - Its data are anonymised and protected against manipulation and misuse.
  - The data allow the exact vehicle type, variant and version, and the fitted active safety systems, to be identified.
  - The data can be made available to national authorities only for accident research and analysis (including type-approval), in compliance with the GDPR, over a standardised interface.
- **Art. 6(5): no identification.** The EDR shall not be able to record the last four digits of the VIN's vehicle indicator section, or any other information that could identify the vehicle, its owner or its holder.
- **Art. 11(1): automated vehicles.** Automated and fully automated vehicles shall comply with implementing acts on:
  - (a) systems replacing driver control;
  - (b) real-time information on the state of the vehicle and its surroundings;
  - (c) driver availability monitoring;
  - **(d) "event data recorders for automated vehicles"**;
  - (e) data exchange for platooning;
  - (f) safety information to other road users.
- **Art. 19.** The regulation applies from **6 Jul 2022**.
- **Annex II, Part E, row E5 "Event Data Recorder"** (columns M1 M2 M3 N1 N2 N3 ... STU; replaced by R2 and then by R3):
  - **M1 and N1 are code B.** EU type-approval is refused from **6 Jul 2022**. Registration, market placement and entry into service are prohibited from **7 Jul 2024**. The regulatory acts are R2 and UN R160.
  - **M2, M3, N2 and N3 are code D.** Type-approval is refused from **7 Jan 2026**. Registration is prohibited from **7 Jan 2029**. The regulatory acts are R3 and UN R169.
  - The separate technical unit (STU) is code B.
  - [!] Art. 6(2) of R2 sets the M1/N1 registration date as "6 July 2024", whereas GSR code B says 7 Jul 2024.
- **Annex II rows E4, E6, E7 and E9** (driver availability monitoring, replacement of driver control, information on vehicle state and surroundings, safety information to other road users) are code "B (5)", where footnote 5 reads "Compliance is required in case of automated vehicles". The consolidated GSR (version of 7 Jul 2024) cites **UN R157** for E4, E6 and E7. Annex I lists UN R157 (original version, OJ L 82, 9.3.2021, p. 75) for M1.

### B. EDR technical content: UN R160 (light vehicles) and UN R169 (heavy vehicles), and the EU additions

**EU additions in R2/R3 (same structure in both acts):**
- Art. 2: compliance with UN R160 (01 series, R2 recital 6 and Art. 6) or UN R169 (R3).
- Art. 3: protection against manipulation via UN R155, and secured software updates.
- Art. 4(1): retrieval through the serial data port of the standardised data link connector (OBD), or by direct connection if that port no longer works after the collision.
- Art. 4(3): event reports carry all mandatory elements plus the precise type, variant and version.
- Art. 4(4): **no retrieval over interfaces accessible without unlocking the vehicle or using tools, and none over wireless vehicle interfaces**.
- Art. 4(5): machine-readable format, and no information relating the data to a natural person.
- Art. 5: checks at periodic roadworthiness tests.
- R2 Art. 6 (transitional): non-EU approvals to the original R160 are accepted until 1 Jul 2024 for type-approval and until 1 Jul 2026 for registration.

**UN R160 (01 series text in OJ L 265):**
- **Scope:** M1 and N1 (§1.1).
- **Excluded from scope (§1.3):** "VIN, associated vehicle details, location/positioning data, information of the driver, and date and time of an event".
- **Definition (§2.11):** event data "does not include audio and video data".
- **Time zero (§2.45, §5.3.3):** "Time zero is the time reference for the EDR data timestamps of an event". It is set at whichever comes first:
  - wake-up of the restraint control algorithm;
  - the first point where the cumulative longitudinal delta-V exceeds 0.8 km/h within 20 ms (lateral: 0.8 km/h within 5 ms);
  - deployment of a non-reversible restraint or VRU system.
- **Triggers (§5.3.1):**
  - change in longitudinal or lateral velocity of more than 8 km/h within 150 ms or less;
  - activation of a non-reversible restraint;
  - activation of a VRU secondary safety system.
- **Locking (§5.3.2):** on deployment of a non-reversible restraint; or, in a frontal impact without a non-reversible frontal restraint, when the x-axis velocity change exceeds 25 km/h within 150 ms or less; or on activation of a VRU secondary safety system.
- **Storage:** at least **3 events** (§5.3). A multi-event crash is two or more events, the first and last no more than 5 s apart (§2.21). The EDR cannot be deactivated (§5.5).
- **Annex 4, Table 1, pre-crash elements, −5.0 to 0 s at 2 Hz:**
  - indicated speed, accelerator, service brake, engine rpm;
  - ABS and stability control;
  - steering input;
  - longitudinal and lateral acceleration, yaw rate;
  - AEBS status, cruise control and ACC status;
  - LDW status, corrective (CSF) and emergency (ESF) steering function status, ACSF category A-E status.
- **Annex 4, Table 1, crash elements:** delta-V at 100 Hz over 0-250 ms (or to end of event + 30 ms).
- **Footnote 3:** "Pre-crash data and crash data are asynchronous". The pre-crash sample-time accuracy is **−0.1 to 1.0 s**.
- **What is absent:** no data element describes other road users or the environment. There are no object lists and no sensor data.

**UN R169 (heavy-duty):**
- **Scope:** M2, M3, N2 and N3. Contracting parties "may but are not required to" make it mandatory (§0.4).
- **Exclusions (§1.3):** the same as R160, including location/positioning data and date and time.
- **Triggers (§5.3.1):**
  - "Sudden Deceleration" above 3.25 m/s², persisting at least 0.7 s;
  - "Last Stop";
  - activation of the supplemental restraint system, ABS, AEB or vehicle stability function.
- **Storage:** at least **5 events** (§5.3). Time zero is the trigger occurrence (§5.3.3).
- **Annex 4 recording window:** −20 to +10 s. Vehicle speed at 4 Hz; service brake and accelerator at 10 Hz. The same asynchronous pre-crash/crash timing footnote applies.

### C. DSSAD under UN R157 (ALKS): occurrence log, not a sensor log

- **Original R157 (R7).**
  - **Scope and speed:** the ALKS operates up to 60 km/h (§5.2.3.1). The EU listing (GSR Annex I) is for M1.
  - **Fitment:** "Each vehicle equipped with ALKS ... shall be fitted with a DSSAD" (§8.1). The DSSAD "enables the determination of interactions between the ALKS and the human driver" (§2.15).
  - **Recorded occurrences (§8.2.1 (a)-(k)):**
    - activation and deactivation (dedicated means, or override by steering, accelerator or brake);
    - transition demand (planned, unplanned, driver unavailable or unbuckled, system failure, override);
    - reduction or suppression of driver input;
    - start and end of an emergency manoeuvre;
    - **EDR trigger input**;
    - **involvement in a detected collision**;
    - minimum risk manoeuvre engagement;
    - severe ALKS failure and severe vehicle failure.
  - **Data elements (§8.3.1):** the occurrence flag; its reason; the date (yyyy/mm/dd); and a **timestamp hh:mm:ss with time zone, accuracy ±1.0 s**. Plus the software identification R157SWIN (§8.3.2).
  - **Availability and protection:**
    - access is subject to national or regional law (§8.4.1);
    - first-in, first-out overwrite (§8.4.2);
    - retrievable after an R94/R95/R137-level impact and without main power (§8.4.3);
    - readable via the OBD port (§8.4.4);
    - anti-tampering (§8.5).
- **01 series (R8).**
  - **Scope:** speed up to **130 km/h** (§5.2.3.1). The text explicitly covers M2/M3/N2/N3 as well as M1/N1 (heavy-vehicle time-gap column; DSSAD retrievability §8.4.3.2).
  - **New occurrences:** (l)-(p), covering the start, end and abortion of a lane-change procedure and the start and end of intentional lane crossing, plus (c)(viii), manual activation of the direction indicator.
  - **Lane-change flags** are stored only if they occur within 30 s before an emergency manoeuvre, a collision, an aborted lane change or an EDR trigger (§8.2.2).
  - **§8.4.5, retrieval with the R160 EDR:** the DSSAD elements for **at least the last 30 s before the last "EDR trigger input" flag** must be retrievable with the EDR data. Where national or regional law requires it, the date and timestamp are dropped and **replaced by the time difference to the EDR-trigger flag** (§8.4.5.3).
  - **Annex 6 §7.1, test-only data channels:** during **type-approval public-road testing only**, data channels including distance to the leading vehicle, relative speed, following-vehicle distance, and positions and velocities of vehicles in the adjacent lane must be logged.
- **Fully automated vehicles (R4, Annex II §9).**
  - **Scope:** use cases "predefined area", "hub-to-hub" and "automated valet parking".
  - **Occurrences (9.1.1-9.1.17):** activation; deactivation; remote-operator requests and inputs; start and end of emergency operation; detected collision; EDR trigger; minimal risk manoeuvre and minimal risk condition; ADS and vehicle failures; lane-change and lane-crossing events.
  - **Data elements:** flag, reason, date, **position (GPS coordinates)**, and timestamp with ±1.0 s accuracy (9.3); RXSWIN (9.4).
  - **With an EDR (9.7):** the last 30 s before the EDR trigger are retrievable through the OBD port. **The timestamp is replaced by the time difference to the EDR-trigger flag** (9.7.3).

### D. EDR vs DSSAD vs raw perception logging

| | EDR (GSR Art. 6 + R160/R169) | DSSAD (R157 §8; R4 Annex II §9) | Raw / tracked perception logging (radar detections, object tracks) |
|---|---|---|---|
| Purpose | Crash-related ego-vehicle parameters | Interactions between system and driver (ALKS); ADS occurrence log (fully automated vehicles) | Development and validation, research; our recorders |
| Trigger / time base | Triggered. Timestamps are relative to **time zero** at the crash; pre-crash window −5 to 0 s at 2 Hz (R160) or −20 to +10 s (R169); pre-crash timing accuracy −0.1/+1.0 s | Occurrence-driven. Absolute date and time at **±1.0 s**; when read together with the EDR, time is relative to the EDR trigger (R157 01 series §8.4.5.3; R4 9.7.3) | Continuous, at sensor rate, on the vehicle clock (no common inter-vehicle clock) |
| Position | **Excluded** (R160/R169 §1.3) | Not in R157; **GPS position in R4** | Pose and GNSS usually logged |
| Other road users | **None** | **None** (only the flags "involved in detected collision" and "EDR trigger input") | Yes |
| Mandatory for | M1/N1: new types from 6 Jul 2022, all new vehicles from 7 Jul 2024. M2/M3/N2/N3: new types from 7 Jan 2026, all new vehicles from 7 Jan 2029 (GSR Annex II E5). US: only if fitted (49 CFR 563.3) | Only for vehicles approved with ALKS (R157) or with an ADS under R4. Fitting an ALKS or ADS is itself optional | **Not mandated** by any instrument above |

### E. US comparison (R9; LII mirror of eCFR, current text)

- **§563.3:** Part 563 applies to vehicles up to 3,855 kg (8,500 lb) GVWR manufactured on or after 1 Sep 2012 **"if they are equipped with an event data recorder"**. An EDR is therefore not mandated in the US.
- **§563.5:** the EDR definition excludes audio and video.
- **Table I, current text:** speed, accelerator and service brake are recorded over **−20 to 0 s at 10 Hz**. Until the phase-in completes, **−5.0 to 0 s at 2 Hz** remains required.
- **Phase-in:** 25 % of EDR-equipped production from 1 Sep 2028, 50 % from 1 Sep 2029, 75 % from 1 Sep 2030, and all from 1 Sep 2031. Later dates apply to small-volume and multi-stage manufacturers. The 2024 final rule had originally set a single compliance date of 1 Sep 2027.

### F. UN R157 minimum following distance (time-gap) table

**Original (R7, §5.2.3.3).** d_min = v_ALKS · t_front (v in m/s). Linear interpolation applies between table values. For present speeds **below 2 m/s, d_min is never less than 2 m**.

| Speed (km/h) | (m/s) | t_front (s) | d_min (m) |
|---|---|---|---|
| 7.2 | 2.0 | 1.0 | 2.0 |
| 10 | 2.78 | 1.1 | 3.1 |
| 20 | 5.56 | 1.2 | 6.7 |
| 30 | 8.33 | 1.3 | 10.8 |
| 40 | 11.11 | 1.4 | 15.6 |
| 50 | 13.89 | 1.5 | 20.8 |
| 60 | 16.67 | 1.6 | 26.7 |

**01 series (R8, §5.2.3.3).**
- The **M1/N1 column is unchanged** (values above).
- A heavy-vehicle column (M2/M3/N2/N3) is added: 1.2 / 1.4 / 1.6 / 1.8 / 2.0 / 2.2 / 2.4 s, giving 2.4 / 3.9 / 8.9 / 15.0 / 22.2 / 30.6 / 40.0 m.
- The table applies **up to 60 km/h only**. Above 60 km/h the system must respect the minimum following distances of the country of operation (§5.1.2).
- The floor below 2 m/s is 2 m for M1/N1 and 2.4 m for heavy vehicles.
- **Correction:** there is no 70-130 km/h row in the official table.
- This matches the project's d_min = max(v · t_front, 2 m) for M1.

**Related provisions useful for event semantics and avoidability:**
- **Emergency manoeuvre (§5.3.1.1, original):** any longitudinal deceleration demand above 5.0 m/s² counts as an emergency manoeuvre.
- **Cut-in (§5.2.5.2):** a collision must be avoided only if all of the following hold:
  - the cutting-in vehicle is slower than the ALKS vehicle;
  - its lateral movement has been **visible for at least 0.72 s** before the TTC_LaneIntrusion reference point;
  - TTC_LaneIntrusion > v_rel/(2·6 m/s²) + 0.35 s, as written in the 01 series. TTC_LaneIntrusion is taken when the intruding wheel crosses a line 0.3 m beyond the outer edge of the lane marking.
  - [!] In the original's EUR-Lex HTML the equation is an image and was not checked.
- **Preventable vs unpreventable scenarios** (original: Annex 4, Appendix 3; 01 series: Annex 3). These are guidance for type approval, not a liability rule.
  - **Performance model 1:**
    - risk perception point: the vehicle centre deviates more than 0.375 m from the lane centre (cut-in/out), or the leading vehicle's deceleration exceeds 5 m/s²;
    - risk evaluation (perception) time: **0.4 s**;
    - **0.75 s** from the end of perception to the start of deceleration;
    - **0.6 s** jerk to 0.774 g (0.85 g after full wrap, derived from UN R152);
    - TTC 2.0 s for cut-in; THW 2.0 s for cut-out and deceleration.
  - **Performance model 2 (01 series §3.4)** uses the fuzzy surrogate safety metrics PFS and CFS ([B69], [B16]).

### G. What is NOT required (state explicitly in the paper)

1. No EU, UNECE or US instrument above requires series vehicles to log **raw sensor data or perception outputs** (detections, object lists, tracks, classifications) for accident analysis.
2. EDR data contain **no location, no absolute date or time, no VIN, no audio or video, and nothing about other road users**. The pre-crash window is short (5 s for R160; 20 s for R169 and US after phase-in), and the 2 Hz pre-crash samples have a −0.1/+1.0 s timing tolerance.
3. DSSAD records only discrete occurrences with ±1 s timestamps (plus GPS position under R4). It is mandatory only where an ALKS or a fully-automated ADS is approved, and access depends on national law.
4. R157's richer data channels exist **only for type-approval testing** (Annex 6).
5. Data-retrieval tools and methods are outside the scope of R160/R169 (§0.2 / §0.1). EU retrieval is wired-only (R2/R3 Art. 4(4)).

**Implication for the paper:**
- The recorder assumptions go beyond current regulatory minima: per-vehicle pose, controls, collision sensor, and raw or tracked radar with independent clocks. They should be stated as such, aligned with proposals like [B19], [B21] and [B22].
- The regulations themselves anchor DSSAD and ADS data to the EDR trigger by a relative time difference (R157 01 §8.4.5.3; R4 §9.7.3). This is a regulatory precedent for collision-anchored alignment.

---

## C: Appendix A: Additional verified candidates (Crossref-verified unless noted; not counted above)

| Topic | Reference | DOI / URL |
|---|---|---|
| 1 | Campbell, K. L., "Energy Basis for Collision Severity," SAE TP 740565, 1974 | [10.4271/740565](https://doi.org/10.4271/740565) |
| 1 | Brach, R. M., "Uncertainty in Accident Reconstruction Calculations," SAE TP 940722, 1994 | [10.4271/940722](https://doi.org/10.4271/940722) |
| 1 | Wach, W. & Unarski, J., "Uncertainty of calculation results in vehicle collision analysis," Forensic Sci. Int. 167(2-3):181-188, 2007 | [10.1016/j.forsciint.2006.06.061](https://doi.org/10.1016/j.forsciint.2006.06.061) |
| 1 | Struble, D. E. & Struble, J. D., *Automotive Accident Reconstruction*, CRC Press, 2020 (1st ed. 2013: 10.1201/b15542) | [10.1201/9781003008972](https://doi.org/10.1201/9781003008972) |
| 1 | Bortles, W. et al., "A Compendium of Passenger Vehicle Event Data Recorder Literature and Analysis of Validation Studies," SAE TP 2016-01-1497, 2016 | [10.4271/2016-01-1497](https://doi.org/10.4271/2016-01-1497) |
| 1 | Gambi, A. et al., "Generating effective test cases for self-driving cars from police reports," ESEC/FSE 2019, pp. 257-267 | [10.1145/3338906.3338942](https://doi.org/10.1145/3338906.3338942) |
| 1 | Rosenbluth, W., *Black Box Data from Accident Vehicles: Methods of Retrieval, Translation, and Interpretation*, ASTM monograph, 2009 | [10.1520/MONO5-EB](https://doi.org/10.1520/MONO5-EB) |
| 2 | Summala, H., "Brake Reaction Times and Driver Behavior Analysis," Transp. Human Factors 2(3):217-226, 2000 | [10.1207/STHF0203_2](https://doi.org/10.1207/STHF0203_2) |
| 2 | Dozza, M., "What factors influence drivers' response time for evasive maneuvers in real traffic?" AAP 58:299-308, 2013 | [10.1016/j.aap.2012.06.003](https://doi.org/10.1016/j.aap.2012.06.003) |
| 2 | Bärgman, J. et al., "Counterfactual simulations applied to SHRP2 crashes ...," AAP 102:165-180, 2017 | [10.1016/j.aap.2017.03.003](https://doi.org/10.1016/j.aap.2017.03.003) |
| 2 | Lee, D. N., "A Theory of Visual Control of Braking Based on Information about Time-to-Collision," Perception 5(4):437-459, 1976 | [10.1068/p050437](https://doi.org/10.1068/p050437) |
| 3 | Guo, H. et al., "Blockchain-inspired Event Recording System for Autonomous Vehicles," IEEE HotICN 2018, pp. 218-222 | [10.1109/HOTICN.2018.8606016](https://doi.org/10.1109/HOTICN.2018.8606016) |
| 4 | Wang, T.-H. et al., "V2VNet: Vehicle-to-Vehicle Communication for Joint Perception and Prediction," ECCV 2020, pp. 605-621 | [10.1007/978-3-030-58536-5_36](https://doi.org/10.1007/978-3-030-58536-5_36) |
| 4 | Xu, R. et al., "V2V4Real: A Real-World Large-Scale Dataset for Vehicle-to-Vehicle Cooperative Perception," CVPR 2023, pp. 13712-13722 | [10.1109/CVPR52729.2023.01318](https://doi.org/10.1109/CVPR52729.2023.01318) |
| 4 | Lu, Y. et al., "Robust Collaborative 3D Object Detection in Presence of Pose Errors" (CoAlign), ICRA 2023, pp. 4812-4818 | [10.1109/ICRA48891.2023.10160546](https://doi.org/10.1109/ICRA48891.2023.10160546) |
| 4 | Han, Y. et al., "Collaborative Perception in Autonomous Driving: Methods, Datasets, and Challenges," IEEE ITS Mag. 15(6):131-151, 2023 | [10.1109/MITS.2023.3298534](https://doi.org/10.1109/MITS.2023.3298534) |
| 4 | Yu, H. et al., "V2X-Seq: A Large-Scale Sequential Dataset for Vehicle-Infrastructure Cooperative Perception and Forecasting," CVPR 2023, pp. 5486-5495 | [10.1109/CVPR52729.2023.00531](https://doi.org/10.1109/CVPR52729.2023.00531) |
| 4 | ETSI TR 103 562 V2.1.1 (2019-12), "Analysis of the Collective Perception Service (CPS); Release 2" (official PDF) | <https://www.etsi.org/deliver/etsi_tr/103500_103599/103562/02.01.01_60/tr_103562v020101p.pdf> |
| 5 | Mori, S. et al., "Track association and track fusion with nondeterministic target dynamics," IEEE TAES 38(2):659-668, 2002 | [10.1109/TAES.2002.1008994](https://doi.org/10.1109/TAES.2002.1008994) |
| 5 | Uhlmann, J. K., "Covariance consistency methods for fault-tolerant distributed data fusion," Information Fusion 4(3):201-215, 2003 | [10.1016/S1566-2535(03)00036-8](https://doi.org/10.1016/S1566-2535%2803%2900036-8) |
| 5 | Scheel, A. & Dietmayer, K., "Tracking Multiple Vehicles Using a Variational Radar Model," IEEE T-ITS 20(10):3721-3736, 2019 | [10.1109/TITS.2018.2879041](https://doi.org/10.1109/TITS.2018.2879041) |
| 5 | Weng, X. et al., "3D Multi-Object Tracking: A Baseline and New Evaluation Metrics" (AB3DMOT), IROS 2020, pp. 10359-10366 | [10.1109/IROS45743.2020.9341164](https://doi.org/10.1109/IROS45743.2020.9341164) |
| 5 | Matzka, S. & Altendorfer, R., "A comparison of track-to-track fusion algorithms for automotive sensor fusion," IEEE MFI 2008, pp. 189-194 | [10.1109/MFI.2008.4648063](https://doi.org/10.1109/MFI.2008.4648063) |
| 5 | Reid, D., "An algorithm for tracking multiple targets," IEEE TAC 24(6):843-854, 1979 | [10.1109/TAC.1979.1102177](https://doi.org/10.1109/TAC.1979.1102177) |
| 6 | Horn, B. K. P., "Closed-form solution of absolute orientation using unit quaternions," JOSA A 4(4):629, 1987 | [10.1364/JOSAA.4.000629](https://doi.org/10.1364/JOSAA.4.000629) |
| 6 | Segal, A. et al., "Generalized-ICP," Robotics: Science and Systems V, 2009 | [10.15607/RSS.2009.V.021](https://doi.org/10.15607/RSS.2009.V.021) |
| 7 | Lim, H.-T. et al., "IEEE 802.1AS time synchronization in a switched Ethernet based in-car network," IEEE VNC 2011, pp. 147-154 | [10.1109/VNC.2011.6117136](https://doi.org/10.1109/VNC.2011.6117136) |
| 7 | Huck, T. et al., "Precise timestamping and temporal synchronization in multi-sensor fusion," IEEE IV 2011, pp. 242-247 | [10.1109/IVS.2011.5940472](https://doi.org/10.1109/IVS.2011.5940472) |
| 7 | Furgale, P. et al., "Unified temporal and spatial calibration for multi-sensor systems," IROS 2013, pp. 1280-1286 | [10.1109/IROS.2013.6696514](https://doi.org/10.1109/IROS.2013.6696514) |
| 7 | Shrestha, P. et al., "Synchronization of Multiple Camera Videos Using Audio-Visual Features," IEEE TMM 12(1):79-92, 2010 | [10.1109/TMM.2009.2036285](https://doi.org/10.1109/TMM.2009.2036285) |
| 7 | Mills, D. L., "Internet time synchronization: the network time protocol," IEEE Trans. Commun. 39(10):1482-1493, 1991 | [10.1109/26.103043](https://doi.org/10.1109/26.103043) |
| 8 | Tao, F. et al., "Digital Twin in Industry: State-of-the-Art," IEEE TII 15(4):2405-2415, 2019 | [10.1109/TII.2018.2873186](https://doi.org/10.1109/TII.2018.2873186) |
| 8 | Sun, P. et al., "Scalability in Perception for Autonomous Driving: Waymo Open Dataset," CVPR 2020, pp. 2443-2451 | [10.1109/CVPR42600.2020.00252](https://doi.org/10.1109/CVPR42600.2020.00252) |
| 9 | Laureshyn, A. et al., "Evaluation of traffic safety, based on micro-level behavioural data ...," AAP 42(6):1637-1646, 2010 | [10.1016/j.aap.2010.03.021](https://doi.org/10.1016/j.aap.2010.03.021) |
| 9 | Ward, J. R. et al., "Extending Time to Collision for probabilistic reasoning in general traffic scenarios," TR-C 51:66-82, 2015 | [10.1016/j.trc.2014.11.002](https://doi.org/10.1016/j.trc.2014.11.002) |
| 9 | Hillenbrand, J. et al., "A Multilevel Collision Mitigation Approach - Its Situation Assessment, Decision Making, and Performance Tradeoffs," IEEE T-ITS 7(4):528-540, 2006 | [10.1109/TITS.2006.883115](https://doi.org/10.1109/TITS.2006.883115) |

## C: Appendix B: Verification notes and residual uncertainties

- **DOIs I had recalled wrongly, caught and corrected through Crossref.** Each wrong DOI resolved to an unrelated paper (or, for the Guo et al. DOI, did not resolve), so it was replaced:

  | Paper | Wrong DOI | Correct DOI |
  |---|---|---|
  | Hammarstrand et al. 2012 | 10.1109/TAES.2012.6237604 | **6237597** |
  | Mori et al. 2002 | 10.1109/TAES.2002.1008984 | **1008994** |
  | Lim et al. 2011 | 10.1109/VNC.2011.6117106 | **6117136** |
  | Westenberger et al. 2011 | 10.1109/ISPCS.2011.6070153 | **6070146** |
  | Guo et al. 2018 | 8606022 (did not resolve) | **8606016** |
  | Kowalick | 0471698954 (did not resolve) | **0471715964** |

  Cite only the DOIs given in this file.
- **No DOI exists** (verified on official pages): CARLA [B63], CoBEVT [B28], Vadivelu et al. [B48], RSS [B64], Hayward [B65], Granström et al. [B38], NTSB [B9], ETSI [B32].
- **Year ambiguities:**
  - Granström et al.: 2017 (Chalmers) vs "Dec. 2016" (arXiv journal-ref).
  - Bar-Shalom/Li/Kirubarajan: 2001 print vs 2002 Crossref.
  - Kowalick: 2004 Crossref vs a frequently cited 2005.
- **Content not read in full:** SAE J3197 [B21] and IEEE 1616.1 [B22] are paywalled; their scope comes from publisher and retailer abstracts. Bannach et al. [B56] had no abstract available.
- **Regulatory dates that rest on secondary or incomplete sources:**
  - Entry into force of the R157 01 series (4 Jan 2023): GlobalAutoRegs only.
  - Entry into force of the R160 01 series: "TBC" in the OJ.
  - The 6 vs 7 July 2024 M1/N1 registration date in R2 vs the GSR.
  - Confirm all three against UNECE TRANS/WP.29/343 (blocked to automated access during this check) before submission.
- **Material corrected during verification:** the R157 table has **no** rows above 60 km/h. The 01 series instead refers to national following-distance rules above 60 km/h.
