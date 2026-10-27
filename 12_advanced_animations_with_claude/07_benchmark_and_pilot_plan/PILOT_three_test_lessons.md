# Pilot: three test lessons and a Reel from each

**Status: plan only. Nothing here has been produced.** Companions: `BENCHMARK_hyperframes_vs_remotion.md` (engine choice, same three lessons), `record_sheets.md` (blank tables), `../04_harness_contract/` (contract, lint, hash check, cue-sheet validator, safe-zone tokens). Citations `[N#]`, `[V#]` are in `../01_research/RESEARCH_REPORT_advanced_animations_with_claude.md`. Labels: **[Recommendation]**, **[Hypothesis]**, **verify**. Paths that begin with a number and underscore (for example `10_pilots_and_examples/…`) are relative to the project ROOT, `ExamLeaf_Video_EdTech_Pipeline/`.

**What this pilot is.** A bounded run of the whole "Advanced Animations with Claude" section on three real fixtures (one physics, one chemistry, one biology): freeze the science, build cue sheets, write scenes against the contract, render, test determinism, QA, derive a Reel from each, record every cost and defect. It proves the section's tooling and routines.

**What it is not.**
- It is **not** the four 600-second pilot lessons of `10_pilots_and_examples/INSTRUCTIONS_running_the_four_pilots.md`. Those need full scripts, narration, alignment and two human approvals. The fixtures used here are 30 s `technical_preview` scenes whose `board_mapping_status` is "pending current syllabus and ExamLeaf source review" and whose Physics RC syllabus relevance is unconfirmed.
- It does **not** produce releasable video. Every output stays `blocked_pending_audio_and_expert_review`; the engine's `release-check` must still block. Do not fabricate reviewer identities or approvals.
- It does not evaluate learning. The four-measure learning study (immediate, fresh question, delayed, confidence calibration) belongs to the 600 s pilots.

**Engine.** If the benchmark has chosen an engine, use it. If not, use HyperFrames (the default [Recommendation, report section 2.6]) and label every result "provisional: engine not yet benchmarked". The contract keeps scenes engine-agnostic.

---

## 1. Inputs

All three fixtures are in `../../04_video_engine/implementation_v2/examples/`. Each is 30 s, authored at 24 fps; the pilot renders at **30 fps, 1080 × 1920, 900 frames** (contract section 7: cue times are in seconds, so fps is free).

| ID | Fixture | Title | Class context (fixture) | Assumptions (fixture) |
|---|---|---|---|---|
| **P-PHY** | `physics_rc.json`; R = 10000 Ω, C = 0.0001 F, V_s = 10 V | "Charging takes time" | "Class 12 circuit-model technical benchmark; board coverage is not yet approved." | Ideal linear resistor and capacitor; constant 10 V source. Capacitor initially uncharged. Model time is shown as t/(RC), not a footage timestamp. |
| **P-CHE** | `chemistry_balance.json`; coefficients [2, 1, 2] | "Same atoms. New counts." | "Class 10 chemistry / Class 12 prerequisite repair; not a Class 12 chapter pilot." | Correct starting and product formulas are supplied. Counts are conserved for each element. Discrete schematic states are not a reaction mechanism or lab demonstration. |
| **P-BIO** | `biology_genetics.json`; Aa × Aa | "A ratio is not a promise." | "Class 12 inheritance technical benchmark." | One Mendelian locus with two alleles and equal gamete probabilities. Random gamete union; complete dominance for phenotype mapping. Probabilities are not guaranteed counts in four offspring. |

Also frozen and hashed before any scene is written (same rules as the benchmark, section 3.2 and 3.3 of `BENCHMARK_hyperframes_vs_remotion.md`): the **state export** per lesson (signed by the academic reviewer), the cue sheet, a placeholder 48 kHz audio bed labelled NOT SPEECH, pinned local fonts, the brief, and the clip(s) from the other producers with manifests (`../04_harness_contract/import_clip_notes.md`).

---

## 2. The three lesson scenes

Each lesson is one scene of 30 s built from five beats that follow the fixture's five cues. Route tags follow the report's storyboard routing (section 9, step 3): `typographic`, `data-bound`, `illustrative`.

**Style [Recommendation].** Code-only visuals (zero image-generation credits): kinetic typography for the headline and a seeded decorative layer in the doodle/flat style (the cheapest house style, report section 4.2), with the science visuals built from the state export. The decorative layer must not use the data's visual vocabulary (no allele-coloured dots, no point clouds near a graph).

**Per-beat common rules.** Reveals land on or 0.05 s before their word (contract section 8); headline hold at least 1.2 s (`vertical_safe_zones.tokens.json`), longer for Hindi and Assamese captions; no camera effects during a measurement or label reveal; science glyphs only from the state export (`data-fx`); layout inside the (placeholder) safe zones.

### 2.1 P-PHY: RC charging

| Beat | Time (s) | Fixture cue role and text | `answer_visible` | On screen (source of glyphs) | Route |
|---|---|---|---|---|---|
| B1 | 0–6 | explain: "Voltage rises quickly, then approaches the supply more slowly." | false | Kinetic headline "Charging takes time" (fixture `title`); RC circuit; the V_C curve draws on (clip from the model) | typographic + data-bound |
| B2 | 6–11 | explain: "Keep R, C and the supply fixed. Watch the same model drive the graph." | false | R, C and V_s chips with values and units from the state export; counters tied to the curve | data-bound |
| B3 | 11–16.5 | question: "Predict: after one RC, is the capacitor fully charged?" | false | The one-time-constant marker on the t/(RC) axis **without** its value; the answer is absent | data-bound |
| B4 | 16.5–24 | feedback: "No. After one RC, it reaches about 63.2% of the supply." | true | The value (about 63.2 %) reveals on its word; pulse (finite) | data-bound |
| B5 | 24–30 | recap: "The curve approaches 10 V; it does not jump there instantly." | true | Asymptote at the supply voltage; assumption chip from the fixture assumptions | data-bound + typographic |

**Science traps the animation must not break** (from the fixture's checks and plan): initial condition V_C(0) = 0 (never show an instant jump); one time constant is 1 − e⁻¹ ≈ 63.2 % of the supply; the horizontal axis is model time t/(RC), never labelled as seconds of footage; the counter and the curve must agree; the curve must never be drawn as reaching the supply exactly; no wobble or boil on the curve or axes.

### 2.2 P-CHE: balancing atoms

| Beat | Time (s) | Fixture cue role and text | `answer_visible` | On screen | Route |
|---|---|---|---|---|---|
| B1 | 0–6 | explain: "Balance the quantities without replacing the substances." | false | Headline "Same atoms. New counts."; formula cards for H₂, O₂, H₂O | typographic + data-bound |
| B2 | 6–11 | explain: "Two water molecules fix oxygen—but change the hydrogen total." | false | Coefficient 2 on H₂O; the atom ledger updates to the intermediate state (oxygen matches, hydrogen does not) | data-bound |
| B3 | 11–16.5 | question: "Your turn: how many hydrogen molecules supply four H atoms?" | false | The H₂ coefficient slot is empty (a UI placeholder, not a science glyph); the answer is absent | data-bound |
| B4 | 16.5–24 | feedback: "Two H₂ molecules. Now every element matches on both sides." | true | Coefficient 2 on H₂ reveals; ledger shows equal counts (H 4, O 2 on both sides) | data-bound |
| B5 | 24–30 | recap: "Change coefficients, not the specified chemical formulas." | true | Subscripts highlighted as fixed; assumption chip ("schematic states, not a mechanism") | data-bound + typographic |

**Traps:** formulas and subscripts never change; no animation that implies a reaction mechanism or collision path (the fixture says the states are discrete and schematic: swap or cross-fade states instead of flying atoms); no implication that balance proves the reaction occurs; every ledger state shown comes from the state export.

### 2.3 P-BIO: a ratio is not a promise

| Beat | Time (s) | Fixture cue role and text | `answer_visible` | On screen | Route |
|---|---|---|---|---|---|
| B1 | 0–6 | explain: "Each parent can contribute A or a with equal probability." | false | Headline "A ratio is not a promise."; two parents Aa with gametes A and a at equal weight | typographic + data-bound |
| B2 | 6–11 | explain: "Combine one allele from each parent; keep genotype and trait distinct." | false | The 2 × 2 grid fills (AA, Aa, Aa, aa); a genotype row and a separate trait row, labelled differently | data-bound |
| B3 | 11–16.5 | question: "Under complete dominance, what fraction shows the dominant trait?" | false | Genotypes visible; trait labels and the fraction are hidden | data-bound |
| B4 | 16.5–24 | feedback: "Three quarters: AA and Aa show the dominant trait in this model." | true | Trait labels reveal; the fraction 3/4 reveals on its word | data-bound |
| B5 | 24–30 | recap: "A 3:1 expectation does not guarantee three out of exactly four." | true | The caveat as on-screen text; assumption chip (complete dominance, equal gamete probabilities) | typographic + data-bound |

**Traps:** genotype and phenotype are never conflated or share a label style; complete dominance is stated; no visual that implies a family of four must show 3:1. Any drawn example of four offspring must exist as a reviewed "illustrative outcome" in the state export, otherwise show none; seeded decoration must not resemble offspring or allele dots.

### 2.4 Languages

English is the lesson text (the fixture's own cue text). A Hindi and an Assamese caption line per lesson exist **only** for the Indic shaping check (benchmark section 6.6 and Sheet F). They are unreviewed translations: do not publish them; a native reviewer must approve any such text before use beyond the test.

---

## 3. The Reel derived from each lesson

A 9:16 Reel of about 23.5 s (705 frames at 30 fps), built by **re-seeking sub-ranges of the lesson scene**, not by re-authoring it. Scenes are pure functions of time, so seeking `t_src` inside the lesson gives the correct state, including everything revealed earlier (report section 9, step 10).

### 3.1 Cut list (same for all three lessons)

| Segment | Kind | Source time (s) | Reel time (s) | Length (s) | Content |
|---|---|---|---|---|---|
| R1 | new card | n/a | 0.0–2.5 | 2.5 | Hook card: the fixture `title` as kinetic type. No new science. |
| R2 | range | 11.0–16.5 | 2.5–8.0 | 5.5 | The question beat (B3) |
| R3 | range | 16.5–24.0 | 8.0–15.5 | 7.5 | The feedback beat (B4) |
| R4 | range | 24.0–30.0 | 15.5–21.5 | 6.0 | The recap beat (B5), complete |
| R5 | new card | n/a | 21.5–23.5 | 2.0 | End card (the two `brand/strings.json` lines: "Professor Diki Simplified" and "Free lesson: <topic>"; no disclosure line, URL, QR code, handle or price; not science) |

Mapping: for range segments, `t_src = t_reel − reel_start + src_start`. The Reel's cue sheet is derived from the lesson's by the same mapping (`examleaf-cue-sheet`); times are shifted, never re-aligned by eye.

### 3.2 Reel rules [Recommendation]

1. **Cut only at cue boundaries** and never inside a sentence.
2. **The Reel must not drop a premise or a caveat.** Because B1 and B2 (which state assumptions) are not in the Reel, the **assumption chip from the fixture assumptions is shown during R2** (and stays through R4). Must-keep lines: P-PHY the feedback line and the recap line; P-CHE the feedback line and the recap line; P-BIO the recap caveat ("does not guarantee three out of exactly four").
3. **No new science text.** The hook card uses the fixture title; the end card carries no science.
4. **The prediction gate is preserved.** In R2 the answer is absent; it appears only in R3 on its word.
5. **Reels do not get camera effects** that distort a graph, grid or ledger.
6. Music (a beat-synced bed) is optional and out of scope here; use the same placeholder bed re-cut, and say so in the record.
7. Safe zones: the same placeholder tokens; the Reel's caption lives in the bottom caption zone.

### 3.3 Reel plan record

Keep a small JSON per Reel next to its frames (informal format; the segment list above is the content):

```json
{"reel_id": "pilot-phy-rc-reel", "source_scene": "pilot-phy-rc", "fps": 30, "duration": 23.5,
 "segments": [
   {"kind": "card", "id": "hook", "dst": [0, 2.5], "text_from": "fixture.title"},
   {"kind": "range", "src": [11.0, 16.5], "dst": [2.5, 8.0]},
   {"kind": "range", "src": [16.5, 24.0], "dst": [8.0, 15.5]},
   {"kind": "range", "src": [24.0, 30.0], "dst": [15.5, 21.5]},
   {"kind": "card", "id": "end", "dst": [21.5, 23.5]}]}
```

The check for each Reel: every `dst` frame maps to a `t_src` inside the lesson; the lengths of `src` and `dst` match; segments tile `[0, duration]` with no gap or overlap; all must-keep lines appear.

---

## 4. What to record

All blank tables are in `record_sheets.md`. Per scene (3 lessons and 3 Reels, and every failed attempt):

- **Authoring:** model ID (full, pinned), effort (explicit), tokens (input, output, cache read, cache write), wall time, number of fix loops and the cause of each, credits (expected 0), human editing minutes.
- **Contract and data checks:** lint level and result, cue-sheet validation result, frame-hash determinism (two renders identical Y/N, first differing frame, worker invariance), render times (cold, cached), peak memory, file size.
- **QA:** safe-zone overlay check, hold-time check, flash check, `data-fx` text diff against the state export, prediction-gate frame check, Indic caption check, loudness and peak (placeholder bed), audio and video length match.
- **Defects:** every one with severity (Critical, Major, Minor), where found, fix loop, minutes to fix.
- **Reel:** derivation minutes, mapping check, must-keep-line check.
- **Human:** full watch of every output on a small-phone-size view (sampling frames does not replace watching the whole video), reviewer minutes.

Also keep the render manifest (contract section 11) and frame hash manifest for every render, and the agent session logs.

---

## 5. Sequence

| Step | Do | Output | Gate |
|---|---|---|---|
| P0 | Fix the render box (`preflight.sh`); install and pin the engine after admission review (engine §11) | Sheet A | **G0** preflight exit 0 |
| P1 | Freeze inputs: fixtures, state exports (academic reviewer signs), fonts, placeholder audio, clips with manifests | hashes | **G1** all hashes recorded; state exports signed |
| P2 | Build cue sheets by the deterministic rule in the benchmark section 3.4; add reveal cues from the brief; validate | `*.cue.json` | **G2** `validate_cue_sheet.py` 0 errors (non-production) |
| P3 | Assemble the brief per lesson (style, route tags, required features, contract level, caps, "do not read other folders") | brief | n/a |
| P4 | Author scenes with Claude Code: pinned model, effort `high`, one workspace per lesson, cap 3 fix loops, no ultracode, zero generated-asset credits | scenes | n/a |
| P5 | `lint_seek_contract.js --level 1` (then 2 when ready); double render; `determinism_hash_check.py` | lint and hash reports | **G3** lint 0 errors and frames identical |
| P6 | Compose the lesson on the master timeline, importing the clips; render frames, then encode and mux the placeholder bed (48 kHz) | lesson MP4 and frames | n/a |
| P7 | Run QA (`examleaf-anim-qa`): safe zones, hold times, flash, `data-fx` diff, prediction-gate frames (11.0–16.4 s show no answer), Indic caption check | QA record | **G4** zero Critical, zero fixture mismatches |
| P8 | Audio checks: sample rate 48 kHz, one loudness target applied (−16 LUFS ±1, ≤ −1 dBTP per AD-04; the −14 LUFS Reels variant only as the recorded A/B arm; 15 Oct 2026: no longer "unresolved"), audio length equals N / fps | audio record | **G5** |
| P9 | Derive the three Reels by re-seeking sub-ranges (section 3); render; re-run P5 and P7 on each Reel | Reel MP4s, plans | **G6** mapping check and must-keep lines |
| P10 | Human full-watch of every lesson and Reel on a small-phone-size view; reviewer notes; defects logged with severity | review record | **G7** no unresolved Critical |
| P11 | Apply the release rule; confirm `release-check` still blocks; complete all sheets; write the decision memo | memo | **G8**, **G9** |

### Gates

| Gate | Pass criterion | Tool or reviewer | If it fails |
|---|---|---|---|
| G0 | `preflight.sh` exit 0 | script | fix the box; do not start |
| G1 | all inputs hashed; each state export signed by a named academic reviewer | reviewer | stop; no scene before the science is frozen |
| G2 | cue sheets valid | `validate_cue_sheet.py` | rebuild sheets |
| G3 | lint exit 0 at Level 1; two renders byte-identical | lint, `determinism_hash_check.py` | counts as a fix loop; find the impure code |
| G4 | zero Critical defects; zero text mismatches; prediction gate respected; safe-zone, hold-time and flash checks pass | anim-qa, reviewer | fix loop (max 3) |
| G5 | audio sample rate 48 kHz; loudness target applied; length matches | audio checks | fix |
| G6 | Reel mapping valid; must-keep lines present; no sentence cut | script or reviewer | re-cut |
| G7 | full watch done; no unresolved Critical; Majors repaired and re-reviewed | human | repair and re-review |
| G8 | **a single Critical science error blocks everything** regardless of visual quality (`INSTRUCTIONS_running_the_four_pilots.md` section 8); `release-check` still blocks | reviewer, engine | block; log |
| G9 | all sheets complete including failed attempts | owner | complete before the decision |

Severity classes (engine `docs/Production_Runbook.md`): **Critical** = wrong science, answer or condition, misleading visual, unlicensed asset, missing critical text or audio, unauthorised data or spend (blocks release); **Major** = poor pronunciation, unreadable essential label, distracting pacing, caption error that changes meaning, answer revealed too early (repair and re-review); **Minor** = cosmetic timing or alignment issue without learning impact (track it).

---

## 6. Stop rules and budgets

- **Iteration cap:** 3 fix loops per scene. After that, record "failed", the cause, and move on.
- **Effort:** `high` explicit; `xhigh` only with a written reason; **never ultracode** [V1][N24].
- **Credits:** zero. No Higgsfield or other paid generation (credits have no native cap [N33][N34]).
- **Tokens:** a per-scene cap set at kickoff by `examleaf-effort-governor`; the [V1] range (about 78K to about 625K tokens for one from-scratch 79 s piece) is an upper-bound reference only, and scenes built from the contract and tokens are expected to be far cheaper **[Hypothesis]**: this pilot measures it.
- **Science stop:** any Critical defect stops that lesson until fixed and re-reviewed.
- **No sibling reads:** each authoring session sees only its own workspace ([V3], edge case 9).

---

## 7. Roles

| Role | Does |
|---|---|
| Academic reviewer (physics, chemistry, biology) | signs state exports; reviews every lesson and Reel for science; classifies defects |
| Native Hindi reader and native Assamese reader | check the shaping card and the test caption lines |
| Animation reviewer | checks timing, hold, safe zones, flash, polish; full-watch |
| Pipeline owner | runs gates, keeps the sheets, writes the memo |
| Claude Code (Opus 5.5, high) | writes scenes against the contract; never edits science text |

---

## 8. Exit criteria and what comes next

**Pass:** G0–G9 satisfied for all three lessons and all three Reels, with the measured agent cost, fix-loop counts and human minutes recorded. Then: promote the section's tooling to "pilot-validated"; hand the contract, template and QA routine to the four 600 s pilots; add the mathematics (chain rule) lesson as a fourth, where Manim CE carries the equations and graphs (report section 2.6).

**Partial:** if some gates fail, the memo lists each failure with its cause and a proposed fix; re-run only the failed gates.

**Fail (any Critical not resolved, or determinism unachievable):** do not scale; revisit the contract or the engine decision (`BENCHMARK_hyperframes_vs_remotion.md` section 8, rule 3).

---

## 9. Open items

Syllabus relevance of RC charging for the Assam board; state-export format and who writes it; the loudness target (−14 vs −16 LUFS); safe-zone insets per platform (placeholders only); the 25 % repair margin and other benchmark thresholds; whether the engine's preview surface suits human review; whether approved narration exists by pilot time (otherwise placeholder audio and synthetic cue timings are used and the lessons are silent technical proofs).
