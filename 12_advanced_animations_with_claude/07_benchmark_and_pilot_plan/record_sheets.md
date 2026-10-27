# Record sheets: benchmark and pilot runs

Blank tables. Copy this file once per run set (for example `record_sheets_<date>_<arm>.md`) and fill it in. **Record failed attempts too** (`INSTRUCTIONS_running_the_four_pilots.md` section 4, step 9). Do not leave a cell blank when a value exists; write `n/a` where it does not apply and `?` where it is unknown.

Used by `BENCHMARK_hyperframes_vs_remotion.md` (sheets A–H, J) and `PILOT_three_test_lessons.md` (sheets A, C–F, I, J). Sheet letters match those files. Gates G1–G8 (benchmark) and G0–G9 (pilot) are defined there. The two gate lists are separate: label which one a row uses.

**Conventions.** Times in seconds unless stated. Hashes are full SHA-256 (or the first 12 hex characters, said so). "Hashes match" = `determinism_hash_check.py` exit 0. Severity = Critical / Major / Minor (engine `docs/Production_Runbook.md`). Arm H = HyperFrames, Arm R = Remotion. Lesson IDs: L-PHY, L-CHE, L-BIO (benchmark); P-PHY, P-CHE, P-BIO (pilot).

---

## Sheet A: environment, versions, frozen inputs, setup

**A1. Run header**

| Field | Value |
|---|---|
| Run set ID | |
| Date started / finished | |
| Person running | |
| Purpose (benchmark / pilot / both) | |
| Engine decided before this run? (Y/N, which) | |

**A2. Machine**

| Field | Value |
|---|---|
| Model / CPU / physical cores / RAM | |
| GPU / driver | |
| OS and build | |
| Power state, power mode, other load | |
| Free disk at start (GB) | |
| `preflight.sh` output (paste) and exit code | |
| Chrome path and version (`CHROME` set? Y/N) | |
| Node / FFmpeg / ffprobe / Python versions | |
| Concurrency settings frozen: C1 = 1 worker; C2 = W = | |

**A3. Engines and skill packs** (record real versions and digests; never guess)

| Item | Arm H: HyperFrames | Arm R: Remotion |
|---|---|---|
| Package / CLI version | | |
| Skill pack source and commit or digest | | |
| Admission review done (engine §11) date and reviewer | | |
| Browser used by the engine (path, version) | | |
| Cache directories deleted for "cold" (names) | | |
| `window.__hf` shape confirmed? (H only) | | n/a |
| Licence text captured (see Sheet H) | n/a (Apache-2.0 [N14]) | |

**A4. Frozen inputs (identical in both arms)**

| Input | Lesson | Path | SHA-256 | Signed by (state export) |
|---|---|---|---|---|
| Fixture JSON | | | | n/a |
| State export | | | | |
| Cue sheet (validator exit code) | | | | n/a |
| Audio bed (NOT SPEECH?) | | | | n/a |
| Fonts: Latin | | | | n/a |
| Fonts: Devanagari | | | | n/a |
| Fonts: Bengali-Assamese | | | | n/a |
| Brief (shared part) | | | | n/a |
| Brief (engine constraints block) H / R | | | | n/a |
| PNG-sequence clip manifest | | | | n/a |
| Encoder command line | | | | n/a |

**A5. 9:16 configuration (M15 / G3)**

| Arm | Config lines that set 1080 × 1920 (paste) | `ffprobe` width × height | fps | frames | crop or scale step in pipeline? | Pass? |
|---|---|---|---|---|---|---|
| H | | | | | | |
| R | | | | | | |

**A6. Setup log (optional, M18)**

| Arm | Steps from empty directory to first render | Minutes | Errors met and how fixed |
|---|---|---|---|
| H | | | |
| R | | | |

---

## Sheet B: render run log (one row per render, including failures)

| Run ID | Date/time | Lesson | Arm | Aspect | Concurrency (workers) | Run type (cold / warm-up / repeat 1–5 / V2 / V4 / 16:9 smoke) | Render command (verify) | Frames wall (s) | Encode wall (s) | Total wall (s) | Peak RSS, process tree (MB) | CPU mean / peak (%) | GPU use | Frames dir (MB) | MP4 (MB) | N frames | Hashes match vs repeat 1 (Y/N) | First differing frame | Failed? cause | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | |

**B2. Determinism summary** (one row per lesson × arm × concurrency)

| Lesson | Arm | Workers | Repeats compared with repeat 1 (2–6) all identical? | Cold vs repeat 2 identical? (cache transparency) | C1 vs C2 identical? (worker invariance) | G2 |
|---|---|---|---|---|---|---|
| | | | | | | |

**B3. Timing roll-up** (median and range over the five cached repeats)

| Lesson | Arm | Workers | Cold (s) | Cached median (s) | Cached min–max (s) | Peak RSS median (MB) | Frames per second (N / cached median) | File size (MB) |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

**B4. Reliability (M17 / G6)**

| Run ID | What failed or hung | Cause found? | Manual intervention | Counted against G6? |
|---|---|---|---|---|
| | | | | |

---

## Sheet C: authoring log (agent), one row per scene per arm per attempt

| Scene ID | Lesson / Reel | Arm | Attempt | Model ID (full) | Effort (explicit) | Effort justification if above `high` | Session ID / log path | Input tokens | Output tokens | Cache read | Cache write | Wall time (min) | Fix loops used (cap 3) | Cause of each loop | Credits (image/voice/other; expected 0) | Human editing minutes | Reviewer minutes | Ultracode used? (must be N) | Outcome (passed / failed for this arm) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | |

How tokens were read (command or screen, **verify**): ____________________

**C2. Engine review surface (optional, M19):** rating 1–5 per arm per lesson: ____________________

---

## Sheet D: scene QA results (one row per scene per arm; for the pilot also per Reel)

Mark each cell **P**ass, **F**ail, or `n/a`, with a note or the defect ID.

| Scene ID | Arm | Contract level reached (0/1/2) | Lint exit code (errors / warnings) | Cue sheet valid (exit code) | Cue source (path/injected/inline) | Two renders identical (Y/N) | Hashes match all pairs (Y/N) | `data-fx` text diff mismatches (count) | Prediction-gate frame at 16.4 s shows no answer | Safe-zone overlay | Headline hold ≥ token | Equation hold = narration end + 0.5 s | Flash check | Min text sizes met | Indic caption check | Audio 48 kHz | Loudness target applied (which) | Audio length = N / fps | Defect IDs | Overall (pass / fail) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | |

**D2. Human frame check (M1b)** at 0.5, 3.0, 5.9, 6.1, 10.9, 11.1, 16.4, 16.6, 23.9, 24.1, 29.9 s: one row per scene per arm.

| Scene ID | Arm | 0.5 | 3.0 | 5.9 | 6.1 | 10.9 | 11.1 | 16.4 | 16.6 | 23.9 | 24.1 | 29.9 | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | | | |

---

## Sheet E: defect log

| Defect ID | Scene ID | Arm | Severity (Critical / Major / Minor) | Description | Type (science / label / timing / layout / font / audio / render / contract) | Found by (lint / hash / QA / reviewer name) | Found at (fix loop #) | Fixed? | Minutes to fix | Re-reviewed by / date |
|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | |
| | | | | | | | | | | |

Counts per scene and arm: Critical ___ Major ___ Minor ___ (a single Critical blocks release; benchmark gate G1).

---

## Sheet F: Indic shaping card (M14 / G4)

Reviewer names: Hindi reader ____________ Assamese reader ____________ Date ________
Fonts used (file names and hashes in Sheet A4): ____________________

Mark **OK**, or the defect (tofu / broken conjunct / mark misplaced / clipped / word split). Heading size = token heading minimum; label size = token label minimum.

| String | Script group | Arm H: heading static | H: label static | H: per-word animation | Arm R: heading static | R: label static | R: per-word animation | Plain-Chrome reference matches? |
|---|---|---|---|---|---|---|---|---|
| क्षेत्र | Devanagari conjunct | | | | | | | |
| ज्ञान | Devanagari conjunct | | | | | | | |
| प्रकाश | Devanagari conjunct | | | | | | | |
| धर्म | Devanagari reph | | | | | | | |
| विद्युत् धारा | Devanagari virama | | | | | | | |
| द्वितीय | Devanagari conjunct | | | | | | | |
| अपवर्तन | Devanagari marks | | | | | | | |
| ट्रांसफ़ॉर्मर | anusvara, nukta | | | | | | | |
| माँ | chandrabindu | | | | | | | |
| বিজ্ঞান | Bengali-Assamese conjunct | | | | | | | |
| ক্ষেত্ৰ | Assamese RA U+09F0 | | | | | | | |
| প্ৰকাশ | Assamese RA U+09F0 | | | | | | | |
| ৰসায়ন | Assamese letters | | | | | | | |
| ৱাট | Assamese letters | | | | | | | |
| प्रकाश का refraction | mixed script | | | | | | | |
| R = 10000 Ω | Latin, numerals, symbol | | | | | | | |
| H₂O | subscript | | | | | | | |
| বিজ্ঞান 10 | mixed script, numerals | | | | | | | |

Native-reader confirmation that every string is correct text: Hindi ____ Assamese ____
Optional: grapheme-cluster letter animation (segmenter behaviour, **verify**): ____________________
Result: G4 pass / fail per arm: H ____ R ____

---

## Sheet G: video-in-video test (M13 / G5), lesson L-BIO, C1 only

| Variant | Arm | Repeat | Workers | MP4 clips visible | Black frames (count) | Duplicated frames | Skipped frames | Desync between clips | Decoder errors / hangs | Wall (s) | Peak RSS (MB) | Reference (PNG-sequence) comparison method and threshold source | Pass? |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| V2 | H | 1 | 1 | 2 | | | | | | | | | |
| V2 | H | 2 | 1 | 2 | | | | | | | | | |
| V2 | H | 3 | 1 | 2 | | | | | | | | | |
| V4 | H | 1 | 1 | 4 | | | | | | | | | |
| V4 | H | 2 | 1 | 4 | | | | | | | | | |
| V4 | H | 3 | 1 | 4 | | | | | | | | | |
| V2 | R | 1 | 1 | 2 | | | | | | | | | |
| V2 | R | 2 | 1 | 2 | | | | | | | | | |
| V2 | R | 3 | 1 | 2 | | | | | | | | | |
| V4 | R | 1 | 1 | 4 | | | | | | | | | |
| V4 | R | 2 | 1 | 4 | | | | | | | | | |
| V4 | R | 3 | 1 | 4 | | | | | | | | | |

Mitigation used and its documented source: H ____________________ R ____________________
Conditional pass under a PNG-sequence-only policy? (Y/N, written policy attached): ______

---

## Sheet H: licence and cost (M12 / G8)

| Item | Arm H: HyperFrames | Arm R: Remotion |
|---|---|---|
| Licence name and URL | Apache-2.0 [N14] (confirm at the repository: ____) | |
| Date terms captured and by whom | | |
| Pasted text of the terms relevant to commercial use | | |
| Does ExamLeaf's use fall in the free or the paid tier? Reasoning | | |
| Per-render fee? Minimum? Definition of a billable render (vendor-confirmed? Y/N) | none stated [N14] | |
| Assumed billable renders per video | n/a | |
| Cost at 1 / 100 / 1,000 videos per month (currency, per month) | | |
| Other cost (hosting, seats, support) | | |
| G8 pass? | | |

Note: engine §10 step 8 records an unverified claim of "$0.01 per billable render with a $100 monthly minimum when the paid licence applies"; do not use it as a fact until confirmed.

**H2. Machine and human cost per scene** (for the total-cost comparison)

| Scene ID | Arm | Machine time cached median (s) × machine rate | Agent cost (tokens → cost at the plan's rate, **verify**) | Human minutes × rate | Licence share | Total |
|---|---|---|---|---|---|---|
| | | | | | | |

---

## Sheet I: pilot roll-up (per lesson and per Reel)

**I1. Lesson scenes**

| Scene | Engine used (provisional? Y/N) | Gates G0–G9 status (list) | Fix loops | Tokens (in / out / cache) | Credits | Human editing min | Reviewer min | Critical / Major / Minor | Full watch done (Y/N, who, device size) | `release-check` still blocks? (Y/N) |
|---|---|---|---|---|---|---|---|---|---|---|
| P-PHY | | | | | | | | | | |
| P-CHE | | | | | | | | | | |
| P-BIO | | | | | | | | | | |

**I2. Reels** (cut list in the pilot file, section 3)

| Reel | Source scene | Reel plan JSON path and hash | Segments tile 0–23.5 s? | Every `dst` frame maps inside the lesson? | Must-keep lines present? (list) | Assumption chip shown from R2 to R4? | Prediction gate preserved in R2? | Derivation minutes | Tokens | Render wall (s) | Hashes match (Y/N) | Defects | Full watch done |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pilot-phy-rc-reel | P-PHY | | | | | | | | | | | | |
| pilot-chem-balance-reel | P-CHE | | | | | | | | | | | | |
| pilot-bio-cross-reel | P-BIO | | | | | | | | | | | | |

---

## Sheet J: gate matrix and decision

**J1. Benchmark gates (G1–G8)** per arm. Evidence = sheet and row.

| Gate | Arm H result | Evidence | Arm R result | Evidence |
|---|---|---|---|---|
| G1 Correctness | | | | |
| G2 Determinism | | | | |
| G3 Vertical 1080 × 1920 | | | | |
| G4 Indic shaping | | | | |
| G5 Video-in-video | | | | |
| G6 Reliability | | | | |
| G7 Contract | | | | |
| G8 Licence | | | | |
| **All gates passed?** | | | | |

**J2. Comparative metrics** (only if both arms pass; each cell the median across the three lessons)

| Metric | H | R | H ÷ R | Tie? (difference below the cached-repeat range) |
|---|---|---|---|---|
| Peak RSS (MB) | | | | |
| Render cold (s) | | | | |
| Render cached (s) | | | | |
| Agent tokens per scene | | | | |
| Fix loops | | | | |
| Reviewer edit minutes | | | | |
| Repair composite (tokens, loops, minutes, each normalised to H, averaged) | 1.00 | | | |
| Total operating cost per month at 100 videos | | | | |

**J3. Decision** (benchmark section 8)

| Item | Entry |
|---|---|
| Rule applied (1: only one passes / 2: both pass / 3: neither passes, STOP) | |
| Margins used (frozen on date) | |
| Engine chosen | |
| If STOP: remediation round done? Gates re-run? Interim compositor? | |
| Changes to `contract.md` required (new version) | |
| Other arm archived on (date) | |
| Signed off by / date | |

**J4. Pilot decision** (pilot section 8): pass / partial / fail; list of failed gates and proposed fixes: ____________________
