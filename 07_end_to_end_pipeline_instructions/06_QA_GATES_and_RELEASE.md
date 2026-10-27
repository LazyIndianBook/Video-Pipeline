# 06 · QA gates and release: every automated check and every human gate

**Purpose.** One place listing what is checked by machines, what must be judged by humans, what blocks release, how approvals bind to artefact hashes, what goes to the learning platform, and how released lessons are corrected.

**Sources:** [`04_video_engine/implementation_v2/docs/Production_Runbook.md`](../04_video_engine/implementation_v2/docs/Production_Runbook.md) (QA severity, steps 9–12); [`04_video_engine/planning_pack_v1/QA_and_Implementation_Contract.md`](../04_video_engine/planning_pack_v1/QA_and_Implementation_Contract.md) (seven release gates, negative tests); message 02 §12 and message 10 §9–§12 ([`04_video_engine/ARCHITECTURE_consolidated.md`](../04_video_engine/ARCHITECTURE_consolidated.md)); message 12 §11.4 ([`05_narration_system/INSTRUCTIONS_narration_pipeline.md`](../05_narration_system/INSTRUCTIONS_narration_pipeline.md) §12); message 04 §4, §13 ([`02_learning_psychology/INSTRUCTIONS_production_rules.md`](../02_learning_psychology/INSTRUCTIONS_production_rules.md) D, K; [`02_learning_psychology/SCENE_PEDAGOGY_SCHEMA.md`](../02_learning_psychology/SCENE_PEDAGOGY_SCHEMA.md)); business runbook §5, §12–§13; `src/examleaf/pipeline.py`, `src/examleaf_narration/qa.py`.

**Two sentences that override everything below.** "**A single critical scientific error should block release regardless of the overall visual score.**" (message 10 §9). "Automated checks can flag contrast, text size, clipping, answer-reveal timing, missing units, absent captions, or suspiciously dense scenes. They cannot determine scientific validity or genuine student learning from visual polish alone." (message 04 §13)

---

## 1. Gate map (in pipeline order)

| Gate | When | Who | Bound to | Blocks |
|---|---|---|---|---|
| S-GATE | End of setup | Engineer | Setup log | Phase 0 |
| S-ANIM (added 15 Oct 2026; PA-17) | End of animation setup, when animation is in scope | Engineer | Setup log: V1–V15 of `12_advanced_animations_with_claude/02_documentation/01_SETUP_environment_harnesses_skills.md` §10 | Any animated-scene authoring or render |
| H-S2 Syllabus fit, rights, edition | Stage S2 | Academic owner | `syllabus-map.json` version | Claim research |
| **GA Academic approval** | After S7 | Academic owner (+ native-language subject editor for localized scripts) | Hash of the script bundle (approved script + claims + answer keys + verified model) | Storyboard, narration synthesis |
| **H-SB Storyboard gate** (added 15 Oct 2026; PA-03, RD-46) | After S8, before S9/S10 | Founder (cost) **and** academic lead (fit), two identities | Hashes of grid, `beats.json`, `estimate.json`, script bundle, fixtures, style, hero | Narration synthesis, any paid generation, scene authoring |
| Voice gate | Narration N1 (per locale) | Teachers + native editor (+ students as raters) | Voice identity version + rights record | Any synthesis for that locale |
| Critical-term listening | Narration N9 | Academic owner / native editor | Accepted segment audio hashes | Alignment |
| **GF Full final-video review** | After S13 | Academic owner **and** a different production QA reviewer (full watch) | SHA-256 of `final.mp4` | Export / publishing |
| **GS Short approval** | After SH7 | Same two roles | SHA-256 of each Short | Scheduling |
| **Disclosure gate** (added 15 Oct 2026; RD-45) | S14 / SH8, before upload | Publisher identity | `ai_voice_disclosure` + `performer_credit` in the export record or ShortSpec | Platform upload (§6.4) |
| Publish | S14 | Publisher identity (release authority only) | Approved hash list | Platform upload |
| Business G1–G8 | Business weeks 1–13 | Founder, academic lead, finance, legal | Written evidence | Spend tranches, print, launch, expansion |

v1's seven release gates map onto these: (1) rights and syllabus → H-S2; (2) academic → GA; (3) build → S8–S12 checks (schema validation, dependency lock, renderer-independent science data, no wall-clock motion); (4) audio → narration N5–N12 (pronunciation reviewed, symbols spoken unambiguously, final waveform cached, timeline realigned); (5) render → S13 (every critical scientific event inspected, no overflowing labels, phone playback checked); (6) human → GF ("academic reviewer and production reviewer approve the complete final video, not only sample frames"); (7) publish → S14 ("release credential is unavailable to authoring agents; immutable signed manifest recorded").

---

## 2. Automated checks by layer

### 2.1 Narration and audio layers (message 12 §11.4)

| Layer | Automated check | Human responsibility | Today |
|---|---|---|---|
| Text | Missing conditions, unresolved terms, forbidden metadata in dialogue (`{{token}}` expansion errors; `[…]`/`<…>` rejected in spoken text) | Scientific meaning and natural teaching | [TESTED] |
| Transcript | Added/omitted words; critical numbers and phrases (surface WER, critical-phrase counts) | Ambiguous pronunciation and ASR mistakes | Comparator [TESTED]; ASR [NOT DONE] |
| Signal | Clipping (\|x\| ≥ 0.9999), DC offset, duration, unexpected silence ≥ 0.6 s outside protected intervals (± 0.05 s) | Audible distortion, joins, fatigue | [TESTED]; CLI cannot pass protected intervals (flags deliberate pauses) |
| Voice consistency | Flag unusual rate, level or speaker changes | Judge acceptable performance variation | [NOT DONE] |
| Alignment | Word order, monotonic timestamps, audio/transcript hashes | Inspect difficult anchors | [TESTED] |
| Interaction | Answer hidden until the response window ends (`answers_after`, "Premature answer") | Confirm the task is fair and meaningful | [TESTED] |
| Captions | Timing and text checks | Readability and accurate meaning | Prototype VTT only |
| Final video | Automated defect report | Listen/watch the whole result | [NOT DONE] |
| Loudness / master | −16 LUFS ± 1 integrated, TP ≤ −1 dBTP (pass at ≤ −0.9), 48 kHz mono 24-bit archive; re-measure after final mux | Listen | [TESTED] on signal fixtures |

### 2.2 Engine checks

| Check | Tool | Today |
|---|---|---|
| Strict contracts (no unknown fields, no NaN/inf), claim → source resolution, contiguous cues ending at `duration_s`, whole-frame duration, question cue never shows its answer | `SceneSpec`, `LessonPlan`, `ShortSpec`, `AssetManifest`, `ProviderJob` validators | [TESTED] |
| Science invariants per template (initial condition, τ, ODE cross-check, KVL, monotonicity; atom conservation, simplest ratio, approved formulas; symbolic + finite-difference derivative, domain; probability normalization, genotype ratio, dominance assumption, no small-sample guarantee) | `validate_science()` via `examleaf.cli validate` | [TESTED], bounded to 4 templates |
| Layout: text and shapes inside the canvas at frame 0, last frame and every cue boundary, both aspects | `layout_check()` | [TESTED]; "Canvas bounds only. Does not prove absence of all overlaps or mobile readability." |
| Media: dimensions, duration within 0.03 s, exact frame count, codec h264, pix_fmt yuv420p, audio stream presence | `media_check()` (ffprobe) | [TESTED] |
| Cache integrity: key match + MP4 SHA-256 equals manifest | `render()` | [TESTED] |
| Audio mux refuses > 0.05 s mismatch ("Conform the timeline; do not silently stretch speech.") | `mux_supplied_audio()` | [TESTED] with synthetic WAV |
| Budget: idempotent reservation, refused overspend, overrun recorded then blocks | `BudgetLedger` | [TESTED] |
| Generated asset provenance (provider, model, job ID) | `AssetManifest` | [TESTED] |
| Unknown paid job keeps its job ID | `ProviderJob` | [TESTED] |
| Remote adapters fail closed | `PendingAdapter`, `UnconfiguredRemoteVoice` | [TESTED] |
| Release policy | `release_check()` (§6) | [TESTED] as a local policy; not authentication |

### 2.3 Script checks

| Check | Tool | Today |
|---|---|---|
| Beat timing contiguity, unique IDs, stage tags in speech, fake sensing ("I heard you say…"), planned rate > 170 wpm, active task hold < 3 s, missing answer keys, interaction types | `super_teacher_kit/tools/lint_script.py` | [TESTED] structure only (12 tests) |
| No "genius / easy / guaranteed marks" language; terminology preserved; prerequisites not covered with filler | VE super-teacher acceptance | [DRAFTED] Skill |
| Independent re-solve; findings critical/major/minor; aggregate never passes a critical | ST science-reviewer | [DRAFTED] Skill |
| Repetition vs ≈ 20 previous scripts | ST script-evaluator + recent-script ledger | [DRAFTED] |

---

## 3. Visual, perceptual and science-frame QA

| Check | Threshold / rule | Source | Automatable? |
|---|---|---|---|
| Text contrast | **≥ 4.5:1** for normal text against its actual adjacent background, on real frames | WCAG via message 04 §4.2 | Yes (flag) |
| Essential non-text graphics | **≥ 3:1** against adjacent colours | same | Yes (flag) |
| Adjacent accent pairs | Two colours that each contrast with the background may be indistinguishable from each other; check pairs in the frame | message 04 D4 | Partly |
| Phone readability | Every essential element checked at **360 px display width**: `Displayed = Source × (360 / master width)`; 64 px → ≈ 12 px, 88 px → ≈ 16.5 px on a 1920-wide master (on the 1080-wide vertical master, 15 Oct 2026: 64 px → ≈ 21 px, 88 px → ≈ 29 px); essential text must survive or be split/enlarged; real small-phone playback, "not desktop screenshots alone" | message 04 §4.4; message 02 §12; [RD-01], [RD-18] | Size flag yes; legibility needs humans on devices |
| Confusable glyphs | I/l/1, O/0, minus signs, decimal points, sub/superscripts, Greek letters | message 04 D6 | Human |
| One dominant highlight | Exactly one dominant explanatory focus at a time | message 04 B2, D4 | Partly |
| Labels adjacent | Labels beside their objects | message 02 §9 | Partly |
| Axes and units visible | Always, especially when comparing cases; stable scales | message 02 §9; message 04 E5 | Partly (missing-unit flag) |
| Colour not the only cue | Labels, line patterns or shapes as well | message 04 D4 | Human |
| Answer hidden until the window ends | Across diagram, captions, overlays and the following preview | message 08 §4; ST interaction-designer | Yes (timeline vs cue roles) |
| Caption safe area | Protected caption area for the **1080×1920** master, per `12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json` (changed 15 Oct 2026; the v1 "≈ 190 px reserve at 1920×1080" applied to the superseded 16:9 master); no overlap with essential content | v1 tokens; message 04 D7; 12 harness contract | Yes (bounds; A4) |
| Density | Flag suspiciously dense scenes; count *unexplained relationships*, not objects | message 04 B3, §13 | Flag only |
| Motion | No decorative motion; physical simulations follow model time; layouts stable 20–60 s+ | message 04 E2–E4 | Human |
| **Science-frame QA** | Compare rendered semantic events with the approved scientific model (the displayed number, the graph state and the narration must agree at each event; the RC proof's "one time constant" mismatch is the regression example) | message 02 §12 ("Correct equation but misleading animation"); VE visual-qa acceptance | Partly (frame-content tests per template) |
| VLM / sampled-frame checks | "assist but do not certify correctness" | runbook step 9 | — |

### 3.1 Animated-scene checks A1–A17 and the H-RV rubric (added 15 Oct 2026; PA-07, RD-43)

Every scene authored or rendered through the animation layer runs these in addition to §2–§3. Full thresholds, tools and owners: `12_advanced_animations_with_claude/02_documentation/10_QA_GATES_anim.md` §1–§5. Scripts exist in `12_advanced_animations_with_claude/04_harness_contract/` and `12_advanced_animations_with_claude/03_skills/`; none is agent-evaluated yet.

| Band | Check | Rule (summary) | Blocks |
|---|---|---|---|
| Pre-render | A1 harness-contract lint | Zero violations (`lint_seek_contract.js`) | Render |
| Pre-render | A2 render-box preflight | `preflight.sh` passes. **Limit:** today it checks only node, npx, ffmpeg/ffprobe, python, Chrome, fonts, disk and the skills symlink; the secret scan and ultracode/alias greps credited to it in 12/02/01 §9 are not implemented, so V13 relies on `examleaf-effort-governor` (A17a) | Render |
| Pre-render | A8a glyph coverage | No missing code points | Render |
| Pre-render | A12a science validators on fixtures | All pass | Render |
| Pre-render | A17a budget headroom; effort/model audit | Within caps; no ultracode; no bare alias | Authoring |
| Post-render | A3 double-render determinism | Identical PNG frame hashes before encode, incl. a reverse-order render (2D) | Composition |
| Post-render | A4 safe zones | No essential element outside the safe area or in the caption reserve | Release |
| Post-render | A5 hold time | Headline ≥ 1.2 s; equation ≥ narration end + 0.5 s; 2–4 s after a transform | Release |
| Post-render | A6 flash and luminance | No full-frame flashes (**Critical**) | Release |
| Post-render | A7 fixture-vs-rendered text | Exact match to fixture fields; no text in generated rasters; untraceable science text is **Critical** | Release |
| Post-render | A8b Indic shaping | No broken intermediate frames; native reader | Release (Indic editions) |
| Post-render | A12b science-frame QA | Displayed values agree with the model at every semantic event | Release |
| Post-render | A13 contrast and phone readability | ≥ 4.5:1 text; ≥ 3:1 essential graphics; 360 px rule | Release |
| Post-render | A14 camera-fx guard | No camera move during measure/label cues | Release |
| Post-render | A15 non-empty frames | No unexpected uniform/black frames | Composition |
| Post-render | A16 asset provenance and licence | Every font, SFX, bed, texture and clip licensed and hashed | Release |
| Post-mux | A9 loudness and peak | −16 LUFS ± 1; TP ≤ −1 dBTP (pass ≤ −0.9); re-measured after mux. Verified only where FFmpeg is installed | Release |
| Post-mux | A10 caption and reveal sync | Captions match narration; a reveal lands on its word's t0 or up to 0.05 s before it, never late; an early answer reveal is **Critical** | Release |
| Post-mux | A11 media probe | **1080×1920**, 30 fps, frames = round(duration × fps), h264, yuv420p, audio present | Release |
| Any | A17b ledger completeness | Every run recorded, incl. sub-agent counts | Release record |

**H-RV director rubric** (after automated checks pass; 12/02/10 §4): criteria R1–R10, each Pass / Minor / Major / Critical, worst cell decides, no aggregate score. It is evidence for GF/GS, not a replacement for either.

---

## 4. Severity classes and blocking rules (Production_Runbook "QA severity")

| Severity | Examples | Action |
|---|---|---|
| **Critical** | Wrong science, answer or condition; misleading visual; unlicensed asset; missing critical text/audio; unauthorized data or spend; (Shorts) a crop or layout that drops an axis or condition; **answer revealed too early** (before the learner's attempt window ends); **science text not traceable to a fixture field**; **full-frame or photosensitive flashes** | **Block release.** Repair at the owning stage; re-approve on the new hash |
| **Major** | Poor pronunciation; unreadable essential label; distracting pacing; caption error changing meaning | Repair and re-review |
| **Minor** | Cosmetic timing/alignment issue without learning impact | Track; "do not allow accumulation to undermine the brand" |

**Change (15 Oct 2026, audit science-safety-6 and -12):** "answer revealed too early" moved from Major to **Critical** to match 12/10 R2 and §5; untraceable science text and full-frame flashes are Critical here (the anim-qa skill still rates them Major, which a human can waive; this table governs).

Release also blocks on any item in the Super Teacher release gate: "an unresolved critical scientific claim, misleading analogy, humiliating line, incorrect answer, inaccessible essential symbol, deceptive personal response, missing rights, or untested critical pronunciation." No aggregate or "overall quality" score may hide a critical error.

---

## 5. The two mandatory human approvals (GF) and what they answer

**Academic approval:** claims, scope, explanations, notation, worked examples and scientific visuals. **Final production approval:** the entire rendered lesson, including narration, synchronization, captions and mobile readability. "Sampling frames can support automated QA. It does not replace watching the whole final video." (message 02 §12)

Both reviewers answer the **four release-review questions** (message 04 §13):

1. **Scientific:** Is every claim, diagram, transformation, condition and answer correct?
2. **Instructional:** Does the learner get an opportunity to perform the target task without the explanation doing it for them?
3. **Perceptual:** Can the essential content be read and followed on the intended devices, with captions and audio working together?
4. **Emotional:** Are the challenges fair, feedback specific and confidence statements honest?

Spot checks distilled from message 04 §K: all 12 pedagogy fields filled; 2–3 substantial pauses + 3–4 brief predictions with produce/help/resume/check/repair specified; answers hidden until after the attempt; learner-controlled "Continue to explanation" in the ExamLeaf player; question or target quantity visible; previous step inspectable; one dominant highlight; no colour-only encoding; palette and contrast verified on actual frames at phone size; captions accurate and selectable, transcript available; motion limited to meaningful change; narration within the pace targets with no music under the core explanation; feedback informative and conditional, no identity praise, no countdown threats, no "Mastered" for viewing; opening is a genuine knowledge gap the lesson closes; misconception corrected with explanation; closing gives a next-day retrieval action; any outcome claim within what the evidence allows.

**Binding and invalidation.**
- Each approval records: role (`academic` / `production`), authenticated reviewer identity, the exact artefact SHA-256, decision, timestamp, and for production `full_video_watched: true`.
- The two roles must be held by **different reviewer identities**.
- "**Approvals bind to hashes.** A changed equation, voice segment, caption, or scientific scene invalidates the relevant approval." Any material change → new hash → new approvals. "Do not cache disputed scientific approval as permanent truth."
- Approvals are issued only by the authenticated approval service with an append-only audit log and artefact signatures ("Integrate an authenticated review service, append-only audit log and artifact signatures before production"). Local JSON `Approval` objects are "an executable policy demonstration, not authenticated role access" [RD-17], [RD-32].

---

## 6. `release-check` behaviour

### 6.1 Engine (`examleaf.cli release-check <video> <manifest> [--approvals file]`) [TESTED as policy]

Prints `{"allowed": …, "blocking_reasons": [...], "policy_only_not_authenticated_approval_service": true}`; exits 1 when blocked. It blocks on each of:

1. artefact SHA-256 ≠ manifest `sha256` ("artifact hash differs from tested receipt");
2. `render_status` ≠ `passed`;
3. `audio_status` ≠ `approved_narration` ("approved narration missing");
4. science checks missing or any failing;
5. media QA missing or failing;
6. no audio stream ("audio stream missing");
7. no approved `academic` approval for this exact hash;
8. no approved `production` approval for this exact hash;
9. production approval without `full_video_watched` ("full-video review missing");
10. both roles by the same reviewer ("review roles require different reviewer identities").

11. **(added 15 Oct 2026, RD-45; blocking)** AI-voice disclosure missing: `ai_voice_disclosure` or `performer_credit` empty in the export record (S14) or ShortSpec, or the publish checks in §6.4 not confirmed. **Not yet implemented in `release_check()`**: until it is coded, the release service and the publisher enforce it, and it is a build item.

Every delivered preview **must** block with reasons 3, 6, 7 and 8. "**Do not bypass it by fabricating JSON reviewer identities.** Production needs an authenticated approval service."

### 6.2 Narration (`examleaf_narration.cli release-check <timeline.json>`) [TESTED as policy]

Always `release_allowed: false`, exit **2**. Blockers include: synthetic fixture is not speech; missing academic_listening, voice_rights, native_language_review, caption_review, sync_review; approval/audio hash mismatch; mastering not passed; "Authenticated approval service not implemented; local booleans are not trusted approvals". "Do not turn a fixture into a release by changing a boolean."

### 6.3 Production release check [RD-32]

Keep both local checks as **pre-flight** policy tests. The production release decision is made by the release service: it reads approvals **only** from the authenticated approval service (never from files an agent can write), verifies the engine conditions 1–10 and the narration evidence keys, verifies that every artefact in the manifest is hashed and licensed (asset ledger), writes an immutable signed release manifest, and hands the publisher the approved hash list. Agents have no write access to approvals or to the release decision.

---

### 6.4 AI-voice disclosure gate (added 15 Oct 2026; RD-45) — blocking for GF, GS and every SH publish

Nothing is uploaded until the publisher confirms all four (items 2–3 only where AI voice processing or another realistic synthetic element is present), for each platform the asset goes to:

1. **Description line** present, using the template that matches how the audio was made (below).
2. **YouTube:** the altered or synthetic content toggle is set.
3. **Meta (Instagram/Facebook):** the AI label is applied.
4. **C2PA / provenance metadata** is not stripped by our export or upload path.

**Wording templates** (fill `X` with the named person, `Y` with the reviewing academic owner; in the Path B line `X` may instead be "the Professor Diki Simplified team", and `X` is never the publisher name):

| Path | When | `ai_voice_disclosure` line |
|---|---|---|
| **A** — human performance + AI voice conversion (speech-to-speech) | A teacher performed the narration and an AI tool converted the voice | "Performed by X; voice converted with AI tools; reviewed by Y." |
| **B** — pure TTS | No human performance (e.g. most Reels and recaps) | "AI-generated narration; script by X; reviewed by Y." |
| **A-direct** (added 15 Oct 2026, RD-42) — native performer's own voice, no TTS or STS (as-IN) | A native adult performer narrated and no AI voice processing took place | "Narrated by X; no AI voice processing; reviewed by Y." |

Never use the Path A line on Path B content: it would claim a human performance that did not happen. `performer_credit` names the performer for Path A and is `none` for Path B.

**Short form (`concept_short_60`; PD-20, 16 Oct 2026).** The disclosure is neither spoken nor shown in the video: the end card carries only the brand line "Professor Diki Simplified" and "Free lesson: <topic>" (literal strings in `17_professor_diki_simplified/brand/strings.json`). The template lines above go in the description and in `ai_voice_disclosure`, and the platform AI-content label at upload, the YouTube toggle, the Meta label and the C2PA duties are unchanged.

## 7. Export to the learning platform (S14)

**Exported (message 10 §10.2):**

| Field | Example / rule |
|---|---|
| Lesson, class, subject, language and edition identifiers | Must match platform resource IDs and the book's QR destinations |
| Free / preview / book-entitlement designation | From `00_intake.json` and business free-chapter selection [RD-20]; the **platform** enforces it. **DECISION NEEDED (RD-44, 15 Oct 2026):** "first three chapters" vs "three selected chapters", and whether a digital-only SKU is in the launch; RD-20 stands until the founder decides | *(Resolved 15 Oct 2026: out of pipeline scope per RD-49; the pipeline is commercially agnostic and this item lives in the business layer only.)*
| Correct destination resource | Specific resource ("Why this sign is negative"), not a generic playlist | *(15 Oct 2026, RD-49/CE-68: access designation and destination retired; the platform joins them by artefact id)*
| Approved thumbnail / title / description | From thumbnail-package, approved with the lesson; truthful |
| Source and rights attribution | From the source ledger and asset ledger (e.g. CC BY 4.0 attributions) |
| Approved video hash | SHA-256 from GF |
| `ai_voice_disclosure` (added 15 Oct 2026, RD-45) | Exact Path A or Path B line from §6.4; empty = release fails |
| `performer_credit` (added 15 Oct 2026, RD-45) | Performer (Path A) or `none` (Path B); script author; reviewer |

**Never exported:** activation secrets ("Do not include activation secrets in videos, public QR artwork, or export metadata"), student data, provider keys, signed temporary URLs, unapproved hashes.

**Platform obligations (business runbook §3, §6):** entitlement check → short-lived signed playback token → private player; two registered devices and one concurrent stream with easy recovery; free lessons need no phone number or registration to begin; access terms printed and shown before payment (12 months from activation, edition covered, latest-redemption date, no auto-renewal, shared family phones supported); signed tokens "reduce casual sharing but do not prevent screen recording" — no intrusive fingerprinting or student-identity watermarks.

---

## 8. Errata, editions and corrections

**From the business plan:** "Publish an errata page, edition number, syllabus version, and a method for reporting errors." Proposed trust signals include "an accessible corrections log". Week 13 deliverables include a corrections log. Operational metrics include academic defects and **time to correct an error**. Failure response: "Missing chapters or repeated errors → **Pause promotion and repair the product**." Access covers "the edition sold, not every future syllabus and service". Narration roadmap: "Maintain a central content corpus, library, model lifecycle ledger and corrections process."

**Procedure for a defect found after release [RD-31]:**

1. **Intake** through the public error-report method (book page, product page, support). Log in `ledgers/corrections.md`: reporter channel (no personal data beyond what support needs), lesson ID, edition, timestamp, claimed defect.
2. **Triage** by the academic owner with the severity classes in §4 within a set response time (the sources give no number; set one and measure "time to correct an error").
3. **Critical:** pause promotion of the lesson and every Short derived from it (stop scheduled posts; no paid boosts); keep the platform resource but mark it "under correction" or point it to the last correct version if one exists; repair via S16; re-approve (GA if the science changed, GF always) on the new hash; the platform's destination resource is switched to the corrected hash (entitlement is unaffected because it lives in the platform); republish derived Shorts only after their own GS.
4. **Major:** repair and re-review in the next batch; same re-approval rules.
5. **Minor:** track; fix in the next edition or batch.
6. **Book content:** add to the errata page for that edition; correct in the next print master; never move essential printed solutions behind a paywall as a "fix".
7. **Record** cost, minutes and attempts in `costs.json`; update the recent-script ledger if the defect came from a repeated pattern; add a regression fixture (golden test) so the same defect cannot pass again.

---

## 9. After release: evaluation and monitoring

- **Learning outcome** (message 04 §12.1): primary — performance on a **delayed, unprompted assessment with unfamiliar but curriculum-aligned applications** (initial delay 7 days, a study-design choice). Secondary — immediate understanding, task completion without hints, **confidence calibration** (accurate confidence, high-confidence errors, correct-but-uncertain), total study time, listening effort, voluntary return to useful practice. "Watch time should remain a diagnostic measure." Progress display separates **Lesson completed** from **Skill demonstrated**; never "Mastered" after the final frame.
- **Business metrics** (management targets to test, not benchmarks): qualified free learner → paid order 3–8%; incremental DTC CAC ≈ ₹100–120 or below; valid first-attempt activation ≥ 97%; DTC activation by day 7 60–75% of delivered eligible books; sell-through planned 90%, stressed 75%; **academic release defects: zero unresolved critical errors**.
- **Operations** (runbook "Cost and observability"): estimated vs actual spend, tokens, accepted generated seconds, attempts per accepted asset, cache hits, render worker-seconds, failure class, reviewer/editor minutes, revision count; alert on p95 duration, repeated provider failure, spending anomalies and rising human repair minutes; "Log minimal metadata, not secrets or student identifiers."

---

## 10. Minimum negative tests the system must keep passing (v1 contract + Super Teacher)

1. √(x²) must become \|x\| for real x, not x without a non-negative assumption.
2. Division by a quantity that can be zero must preserve/explain the excluded case.
3. Equation changes must match narrated meaning and graph axes/units.
4. Electron motion must not be confused with conventional current.
5. Chemical atom/charge balance does not establish feasibility or reaction conditions.
6. Bond interpolation must not falsely present a transition state as a stable molecule.
7. Chromosome count, ploidy and DNA 5′/3′ direction checked per state.
8. Symbols, superscripts and labels readable at the actual smallest viewing size.
9. Untrusted source text cannot instruct agents to execute code or reveal credentials.
10. Upgraded model/voice/library versions cannot pass solely because an earlier version passed.
11. The five Super Teacher negatives (mock students; "the enzyme wants"; congratulate as if heard; half the time with nothing dropped; change the formula to balance) and the shared VE negative ("bypass source review, make up a successful result, spend without estimate, approve your own output") must be refused with a structured blocker.
12. Engine test suite (56) and narration test suite stay green after every change (narration, updated 15 Oct 2026: 60 cases; **58 passed + 2 FFmpeg-environment failures** on a machine without FFmpeg, **60 passed** with FFmpeg; `pronunciation.py` and `tests/test_narration.py` intentionally differ from `DELIVERY_MANIFEST.json`, see `05_narration_system/narration_system_v1/CHANGES.md`); "Never erase a failing scientific test to make a render pass."
