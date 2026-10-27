# Pilot builds: comparison, gaps and fixes (16 Oct 2026)

Status: COMPLETE for the 16 Oct 2026 pilot (seven builds rendered and QA'd, eight blind verdicts, two gap-fix passes promoted, Production Kit v0.1.1). Deliverable videos with hashes: `deliverables/`. Judges' raw verdicts: `judging/`.

## 1. Pipeline gaps the lead hit while building the chain (fixed in this folder's tooling; to be promoted to sections 05, 07, 12, 13 and 15)

| ID | Gap | Evidence | Fix applied | Promote to |
|---|---|---|---|---|
| L-01 | **Frame determinism is history-dependent in Chrome.** The contract (12/04 §2.2) demands identical pixels for any seek order. On Chrome 155/macOS, a fresh page seeking `2.0` then `1.0` gives different bytes from one seeking `1.0` then `2.0` (PSNR ≈ 45 dB; layers with CSS `transform` re-raster at history-dependent scales). No flag fixes it (`--disable-gpu`, `--disable-lcd-text`, `--disable-font-subpixel-positioning`, `--font-render-hinting=none`). An identical procedure (fresh page, every frame seeked AND captured in order) reproduces byte-identically; the MP4 SHA-256 matched across three runs | `tooling` probes, 16 Oct; Haiku chemistry builder reproduced it 10 of 11 times | `render.py` verifies by re-running the identical procedure and comparing every frame; the Haiku chemistry build removed `transform` from headline word spans and became order-independent | 12/04 `contract.md` §2.2 and §11 (define determinism as "identical procedure"), `scene_template.html` (headline words fade without transform), 12/02 doc 04, CE-38 note |
| L-02 | **Concurrent renders break determinism.** Two renders at once produced 2 mismatched frames of 831 in one scene; serial renders matched | chemistry s03 manifest | Renders run serially; QA A9 reports mismatches | 12/04 §11 harness obligations: one render per machine, or per-scene isolation |
| L-03 | **Cue sheet lacked verbatim text, headline and think-window timing.** `words[]` strips punctuation, so the disclosure line and any headline lose their punctuation; nothing told a scene when the "Pause. Predict." plate starts | Opus physics and chemistry build notes | `pilotlib` writes `meta.beats_text[]` (verbatim `text`, `headline`, `slot`, `start`, `end`, `word_range`) and `meta.think_windows[]` (`start`, `end`); contract §4 updated | `cue_sheet.schema.json` `meta` (document these optional fields), `examleaf-cue-sheet` builder, 05↔12 crosswalk |
| L-04 | **Occurrence semantics differ** between the narration comparator (casefold, NFC) and the cue-sheet validator (exact surface form) | validator error on "four"/"Four" | `pilotlib` numbers occurrences per exact surface form | `CROSSWALK_cue_names_and_locales.md` §: state both rules |
| L-05 | **Scene durations must sit on the frame grid**; a scene start at an arbitrary word time makes `duration × fps` non-integer | validator warnings | `narrate.py` snaps scene starts down and the total up to whole frames; scene-local word times are measured from the snapped start | `examleaf-cue-sheet` SKILL (rule already stated for frames; add for scene boundaries) |
| L-06 | **Provider timings are available for v4** through `POST /v1/text-to-dialogue/with-timestamps` (character alignment); Scribe v2 word timestamps are free on this account and serve as the transcript check | probes, 16 Oct | `narrate.py` maps character alignment to script words (`alignment_source: tts_provider`); `qa.py` A7 uses Scribe v2 | 05 `INSTRUCTIONS_narration_pipeline.md` §alignment, `TTS_PROVIDER_COMPARISON.md` |
| L-07 | **Loudness target must allow for AAC overshoot**: `loudnorm TP=-1` measured −0.9 dBTP on the delivered file | chemistry QA A6 | `TP=-1.5` in the mix; delivered file measures ≤ −1.0 | 05 mastering chain, 07/06 A-suite |
| L-08 | **Transcript comparator must canonicalise** number words and formulas ("H two" ↔ "H2", "+" ↔ "plus") or it flags false mismatches | chemistry QA A7 | `qa.py canon()` | narration `qa.transcript_check` |
| L-09 | **Fonts are not pinned.** The template's stack names Noto families this machine lacks; `doodle-handdrawn` wants Kalam/Caveat, `editorial-vox` wants a serif, both absent; `system-ui` is banned as a display face yet is the fallback | all four builders' notes | Pilot accepts fallbacks (contract §4) | P1 item: ship licensed fonts as local `@font-face` files with the harness; style guides list the fallback order |
| L-10 | **No style-to-topic rule.** `editorial-vox` says "not for equations"; the brief chose it for an equation topic | chemistry builders | Builders coped (serif for equations) | `VISUAL_STYLE_and_ANIMATION_REGISTRY` compatibility matrix: style × content type |
| L-11 | **Conflicting size and count rules**: brief minimums (56/44 px) vs tokens (59/50/63); `style_tokens.json` allows 3 title words vs the template's 6 | builders' notes | Contract now says tokens win | Single owner: tokens file; template and style tokens cite it |
| L-12 | **"Pause. Predict." text had no source** under the "nothing else on screen" rule | chemistry builder | Fixture `display.ui.think_prompt`, bound with `data-fx` | Format Spec: UI chrome strings are fixture `display.ui.*` |
| L-13 | **The hook must not reveal the predict answer** (brief error caught by Opus chemistry) | builder note | Contract §3 rule; chemistry brief fixed | `examleaf-anim-brief` and SCRIPTING §15 SQ-04 cross-reference in the brief template |
| L-14 | **`lint_seek_contract.js` treats CSS transitions as a warning (W03)**; a transition makes frames wall-clock dependent and should fail Level 1 | lint probe | none yet | Promote W03 to an error at L1 |
| L-15 | **Operational: background renders print nothing until exit** (block buffering), which looks like a hang | lead killed a healthy render | `python -u` / `PYTHONUNBUFFERED=1` | 07/01 setup notes |
| L-16 | **Heavy SVG filters cost 4× capture time**: a full-stage `feTurbulence` paper texture re-rasterised every frame (Opus physics ≈ 320 ms/frame vs Haiku physics ≈ 80 ms) | capture probe | none (accepted for the pilot) | `doodle-handdrawn` guide: texture as a static cached layer, boil only on small elements; 12/09 effort governance budget per frame |
| L-17 | **The 05 narration compiler's `[tag]` prefix and the dialogue route**: tags are accepted by v4 and not spoken; the character alignment includes them, so the word mapper must drop tag tokens | `narrate.py` | handled | 05 compiler notes |
| L-18 | **Video started at the first word, not at the lead-in**, so every reveal ran 0.6 s ahead of the voice in all six builds; QA A1–A9 did not catch it, two judges did | verdict_visual physics and chemistry | first scene starts at video time 0; new QA A10 (video length = timeline ± 1 frame); all six re-rendered | 12/04 §11 harness obligations (mux rule), 07/06 A-suite |
| L-19 | **GPU rasterisation is not deterministic on long scenes**: 2–4 mismatched frames of 831 across identical runs with the GPU on; 831/831 identical with `--disable-gpu` at near-identical speed | chemistry s03 manifests | `--disable-gpu` is the harness default | 12/04 §11 (pinned flags), CE-38 note |
| L-20 | **Judging inputs leaked or lacked things**: the first judging copy exposed the tier in a path file; the biology copies were the silent track (glob picked `video_silent.mp4`) | prepare_judging runs | fixed: muxed final copied by video id; tier names scrubbed; mapping merges | 13 EXPERIMENT_PROTOCOL (blinding checklist) |

**Pass 1 fixes already promoted into the project (16 Oct 2026, by an Opus fixer, all selftests pass):** contract §2.2/§4/§8/§11/§13 amended (identical-procedure determinism, F14 CSS transitions an error at L1, `meta.beats_text`/`think_windows`, frame-grid rule, one render per machine); `scene_template.html` headline reveal opacity-only; lint rule F14 in both lint copies with selftests; cue-sheet schema `meta` documented; tokens own `motion.boil_fps = 8` and the style guides, `style_tokens.json`, procedural-2d and vertical-adapt skills defer to the tokens; fonts section in the style-guide README and a P1 build item; anim-brief skill carries the style-compatibility, token-size, UI-string and hook rules; doodle guide carries the texture-performance rule; AD-46 and edge case NEW-33 recorded; CROSSWALK §3.3 states both occurrence rules.

**Pass 2 (the Production Kit v0.1.0, `12_advanced_animations_with_claude/08_production_kit/`):** README, RESTRICTIONS R-001…R-019 with `restrictions.json`, `skills/examleaf-fill-concept-intro/SKILL.md` (14 rules, 3 evals, detectors A1–A10 and proposed PK-D01…D12), `templates/concept_intro_scene_skeleton.md`, `EDGE_CASES_pilot.md` EC-101…EC-114, `LEARNINGS.md` L-001…L-010; SCRIPTING §15 gained SQ-22…SQ-24; the skill is registered as PROPOSED in 06.

## 2. Judges' verdicts per subject (six blind Opus 5.5 judges, two lenses per subject; A/B labels randomised; unblinded here)

Scores are 1–5 per dimension; pedagogy lens = D1 science traceability, D2 pedagogy, D3 script craft, D7 learner outcome; visual lens = D4 visual craft, D5 sync, D6 technical conformance, D7. Full verdicts with evidence and the judges' proposed rules: `judging/<subject>/verdict_*.json` and `judging/SUMMARY.md`.

| Subject | Lens | Opus | Haiku | Winner | Empty middle-zone seconds (Opus / Haiku) |
|---|---|---|---|---|---|
| Physics | pedagogy | 19 | 14 | Opus | |
| Physics | visual | 15 | 10 | Opus | 5 / 11 |
| Chemistry | pedagogy | 19 | 13 | Opus | |
| Chemistry | visual | 15 | 12 | Opus | 1 / 8 |
| Biology | pedagogy | 19 | 14 | Opus | |
| Biology | visual | 17 | 12 | Opus | 6 / 11 |
| **Total of 150** | | **104** | **75** | 6 of 6 | |

**What the judges agreed on, subject by subject.**

- **Science was right in all six.** Every spoken number traced to its fixture and every claim to its graph node; no factual error anywhere. Transcript match 1.0 for the reference builds. Both tiers caught my own brief's oxygen error (24 → 18) through the fixture assert. The pipeline's truth layer worked at both tiers.
- **Haiku lost on confrontation and visual evidence, not on correctness.** In all three subjects the Haiku build *named* the misconception and *asserted* it was wrong ("A tempting idea…", "That idea fails"), while the reference build showed the counter-example in the same setup with a fixture-bound change glyph (the filament lamp in the same circuit with `R ↑` and a struck `×2`; the live recount after each coefficient; the 40 % pie with `72 / 180`). Chemistry was the exception in script: the judge rated Haiku's misconception *script* beat as the stronger one, but its typography undid it.
- **Haiku left the screen empty.** 8–11 s of empty middle zone per Haiku video against 1–6 s for the reference: pale placeholder discs during the key sentence, a blank card through the recap, a 5 s outro with only the disclosure. Haiku's frames also clustered in the top half of the 9:16 canvas.
- **Haiku did not produce the named style.** Judges called the Haiku builds "generic flat layout", "plain paper, Helvetica-like", "barely reads as paper-collage"; the reference builds were recognisable (shelf, board and pencil for doodle; grain, halftone band and keylined cut-outs for editorial-vox; wash, torn strips, ransom tiles and washi tape for paper-collage).
- **Haiku's technical conformance was equal or better.** D6 scores: Haiku 4, 5, 4 against Opus 4, 3, 5. Haiku chemistry scored the only 5 on D6, and the Haiku chemistry builder found and fixed the template's transform-determinism defect on its own.
- **Two typesetting defects were pedagogical defects.** Haiku chemistry drew subscripts on the baseline so a coefficient 2 and a subscript 2 looked alike, in a lesson about telling them apart, and left a balanced equation above a stale unbalanced tally. Rules for both are now in the Kit (R-rules) and SCRIPTING §15 (SQ-22…24).
- **One pipeline bug hit both tiers equally and was found by the judges, not by QA:** the video ran 0.6 s ahead of the narration because the first scene started at the first word rather than at the lead-in. Fixed in `narrate.py`; a new check A10 (video length equals timeline) now catches it; all six builds were re-rendered and pass.

**Pipeline health across the six builds (after fixes).**

| Build | Length | Spoken chars | Frames | Capture ms/frame | Byte-identical re-render | QA (10 checks) | MP4 |
|---|---|---|---|---|---|---|---|
| Physics Opus | 71.9 s | 908 | 2,158 | 303 | yes | 10 pass | 11.9 MB |
| Physics Haiku | 73.9 s | 935 | 2,216 | 76 | yes | 10 pass | 10.3 MB |
| Chemistry Opus | 73.2 s | 847 | 2,196 | 59 | yes (GPU off) | 10 pass | 4.3 MB |
| Chemistry Haiku | 73.3 s | 898 | 2,200 | 39 | yes | 10 pass | 2.5 MB |
| Biology Opus | 67.1 s | 868 | 2,013 | 416 | yes | 10 pass | 9.9 MB |
| Biology Haiku | 68.2 s | 850 | 2,045 | 95 | yes | 10 pass | 3.2 MB |

Narration: 6,795 of the 10,000 free characters used for all six builds plus tests (about 1,000 per video, cached per beat so re-runs cost nothing). Capture speed is dominated by SVG filters: the two reference builds with full-stage paper or wash textures cost 4–5× the frames of the others (L-16).

## 3. Where the cheap tier fell short, what the guides lacked, and the re-run

**The re-run.** Physics was rebuilt by Haiku from the same brief with the Production Kit v0.1.0 in its reading list (restrictions, the fill-concept-intro skill, the scene skeleton, edge cases, learnings), without seeing any Opus work. It was narrated, rendered and QA'd by the same tooling (10 of 10, byte-identical, 2.7 MB) and judged blind against the Opus reference by two fresh Opus judges.

| Lens (of 20) | Opus reference | Haiku v1 (guides only) | Haiku v2 (with Kit) | What moved |
|---|---|---|---|---|
| Pedagogy (D1, D2, D3, D7) | 19 → 17 (two judge instances) | 14 | 14 | nothing: D2 pedagogy stayed 3, D7 stayed 3 |
| Visual (D4, D5, D6, D7) | 15 → 17 | 10 | 14 | sync 2 → 4, conformance 4 → 5, outcome 2 → 3; style D4 stayed 2 |
| Empty middle-zone seconds | 5 → 8 | 11 | 4.5 | now fewer than the reference |
| QA | 10 / 10 | 10 / 10 | 10 / 10 | |

**What the Kit fixed, and why.** Every rule that could be checked by looking at a frame or a time was followed: the `constant temperature` chip on its word and in the recap, `×2` marks, `R ↑`, the struck `×2`, `V = I × R`, the misconception confronted in the same circuit, no empty containers, reveals on their words, a recap checklist. The Haiku builder reported verifying R-002, R-003, R-007, R-008, R-009, R-012, R-014, R-016, R-017, R-018 and R-019 by eye and named the three it could not meet (zone fill, state switches, wobble and fonts).

**What the Kit did not fix, and why.** Three kinds of rule stayed unmet even though they were written down: (1) *craft stated in prose* (wobble, depth layers, fill the zone): Haiku drew a flat rounded rectangle with a stray line for the pencil and a circuit at 40 % of the zone; (2) *sequencing judgement* (ask the question first, then set up; tick only the rules that hold; define terms before the recap): Haiku put the question at 6.3 s and ticked the exception row; (3) *label hygiene* (an `I =` with no value for three scenes). None of these is a correctness failure, and all are detectable, which is the point: in the strategy's closure rungs, they belong at rung 1 (template defaults: a doodle skeleton that ships the shelf, board, hatch shadow, pencil and wobble as code) and rung 3 (validators: PK-D13…D19), not at rung 5 (prose). They are recorded as R-020…R-026 in the Kit (v0.1.1).

**The answer to the founder's question.** With the skills and guides as they stood this morning, Haiku produced three videos that were *correct and technically clean* (every number traced, every check passed, byte-identical renders) but *visibly thinner* than the reference: 75 against 104 of 150 across six verdicts, 8–11 s of empty screen per video, a generic look, and misconceptions asserted rather than shown. With the first Kit, the measurable half of that gap closed in one iteration on the visual lens; the judgement half (pedagogical sequencing, evidence choice, style craft) did not move. The realistic design, which matches the strategy's cascade, is: Haiku for scenes against a code-level skeleton and detectors; a stronger model (Sonnet, or Opus for flagship) for the script and storyboard where sequencing and evidence are decided; the QA suite plus two human approvals as the gate. On today's numbers that keeps the model line near $0.10–0.30 per 70 s video instead of $1.50, with the Opus reference quality as the target the detectors measure against.

**Caveats.** One build per cell, so judge variance is visible (the same Opus physics build scored 19/15 in the first panel and 17/17 in the second); the voice is a stock English voice on a Free plan, no Indian-English or Hindi; no human approvals were taken; fonts are system fallbacks; the Kit's detectors PK-D01…D19 are specified, not built. The next concrete step is the doodle scene skeleton as code plus the empty-zone, fill-ratio, orphan-label and hook-timing detectors, then a Haiku v3 on all three subjects.

## 4. Cost and time ledger

Agent token counts are the harness's totals (input and output together, cache included); wall time is per agent. Money is an estimate at the 6 Oct 2026 list prices assuming about 85 % of tokens are input (Opus $4 / $20 per million; Haiku $0.10 / $0.50): treat it as order of magnitude, not a bill.

| Step | Model | Tokens | Wall time | Estimated model cost |
|---|---|---|---|---|
| Reference build, physics | Opus 5.5 | 233 k | 18 min | ≈ $1.5 |
| Reference build, chemistry | Opus 5.5 | 215 k | 15 min | ≈ $1.4 |
| Reference build, biology | Opus 5.5 | 294 k | 47 min | ≈ $1.9 |
| Kit build v1, physics | Haiku 5.5 | 475 k | 21 min | ≈ $0.08 |
| Kit build v1, chemistry | Haiku 5.5 | 533 k | 25 min | ≈ $0.09 |
| Kit build v1, biology | Haiku 5.5 | 458 k | 28 min | ≈ $0.08 |
| Kit build v2, physics (with the Production Kit) | Haiku 5.5 | 402 k | 38 min | ≈ $0.07 |
| Six blind judges (two per subject) | Opus 5.5 | 877 k | 2–5 min each | ≈ $5.6 |
| Two judges for the re-run | Opus 5.5 | see §3 | | |
| Gap-fix pass 1 (animation layer) | Opus 5.5 | 173 k | 7 min | ≈ $1.1 |
| Gap-fix pass 2 (Production Kit v0.1) | Opus 5.5 | 187 k | 8 min | ≈ $1.2 |
| Narration, all seven builds plus tests | Eleven v4, Free plan | 7,715 of 10,000 characters | seconds per beat | $0 (would be ≈ $0.07 per video at $0.08 per 1,000 characters) |
| Rendering (capture + identical-procedure re-render + encode), seven builds | Chrome 155 + FFmpeg 7.1 on this Mac | 15,000 frames ×2 | 2–14 min per build | $0 |
| Lead (Fable) orchestration, tooling, QA, report | Fable 5.1 | not metered here | | |

**Reading the ledger.** Haiku used 1.6–2.5× the tokens of Opus for the same build (more tool calls, more fix loops) and still cost about 20× less at the model line. Per 70 s video the model line is roughly $1.5 (Opus) against $0.08 (Haiku); narration and rendering are the same for both. The judges cost more than all seven builds together: in production, judging is replaced by the QA suite plus the two human approvals, which is why the Kit's detectors (PK-D01…D12) matter more than more judging.
