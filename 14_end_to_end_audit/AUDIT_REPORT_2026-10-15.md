# ExamLeaf Video Pipeline: End-to-End Audit Report

**Date:** 15 Oct 2026. **Project root:** `/Users/chinmoybhuyan/Desktop/Personal/Book/Videos/ExamLeaf_Video_EdTech_Pipeline`
**Lead:** Fable. Seven review lenses: goal alignment, cross-section consistency, factual and arithmetic correctness, completeness against your asks, executability, science-safety non-negotiables, and a sceptic/bloat lens. A second checker tried to refute every finding. Findings marked *(contested)* are ones where one of the two checkers disagreed.

---

## 1. Verdict: PARTIALLY ALIGNED

What has been built points the right way and is mostly correct piece by piece.

- **Science safety.** Science comes only from validated fixtures. Image models never produce text. Agents cannot research facts.
- **Approvals and governance.** Two human approvals are bound to hashes and must come from different reviewers. Ultracode is refused in the shipped code. The platform, not the renderer, enforces entitlement. Minors' data is handled cautiously.
- **Content quality rules.** Fake enthusiasm and fake "I heard you" lines are banned. Learning is measured instead of virality.
- **Correctness.** Every offline selftest passes. About 120 cost figures recompute correctly. Nothing from the ChatGPT source is missing (checked by hash).

The problem is integration. Your later decisions live only in addenda, in proposals, or in section 13:

- vertical-only output
- review at $0 cash
- the storyboard gate before paid generation
- AI-voice disclosure
- the Hindi language scope
- the Production Kit cascade

They never reached the operating documents. The ROOT README sends you to `07/11_MASTER_CHECKLIST.md`. If you follow it today you would:

- render a 16:9 1920×1080 master
- skip the human storyboard gate
- publish with no AI-voice disclosure
- launch English-only
- budget review as the main cash cost

Inside section 13, the cheap-model strategy:

- lets Reels ship on an "inherited" science approval
- puts academic approval *after* rendering

There is also one real code defect: the cue-sheet builder produces sheets that its own harness schema rejects.

No finding survived verification at *critical* severity. Twelve consolidated *major* items would each lead to a wrong or non-compliant video, or a blocked gate, if the documents were followed literally. Almost all of them are edits that carry existing decisions into the runbook, plus one code fix. The direction is right; the paperwork has not caught up with your decisions.

---

## 2. What is confirmed correct and aligned (103 checks passed)

### Core runbook (07) and business model (01)
- **Entitlement.** The platform, not the renderer, enforces entitlement. Activation secrets never appear in videos, QR artwork or metadata. Checked in 07/README principle 4, 07/00 §2.5 and §6, 07/05 principle 6, 07/03 S14 and 07/06 §7. Sections 11–13 never touch activation.
- **Learning over virality.** ROOT principle 7, 07/05 §4 and 07/04 §17 study C all measure learning, not watch time. Shorts deliver the full answer.
- **Two human approvals per lesson.** They are bound to hashes and require different reviewer identities. `release_check` enforces this; agents never write approvals (RD-17/RD-32).
- **Minors' data.** DPDP verifiable parental consent, no behavioural retargeting of children, and no attention surveillance in pilots (07/07 §8, checklist lines 71/75/157).
- **Voice consent and licensing.** Voice consent is in place and student recordings are avoided. The licence ledger correctly flags F5-TTS weights as non-commercial, Fish as research-only, GSAP as not MIT, Remotion as conditional, Blender as GPL (isolated) and fonts as per-font.
- **Release gates fail closed.** Engine exit 1 with 4 reasons; narration exit 2 with 9 blockers.
- **Generated video defaults to 0 s.** Consistent across RD-39, 07/08, 12 AD-08 and 13 D-12.
- **Size.** Runbook ≈51,280 words; RD-01…RD-40 present.

### Source completeness (00)
- All 23 downloads and all 462 extracted files reached the numbered sections, verified by SHA-1. The only exceptions are the zip containers (unpacked by design) and the two narration files deliberately changed by the Indic fix. The pristine copies are still in 00_source.
- All six ChatGPT assistant responses are reproduced in full, including the three the share page hid. The `Pasted text(1).txt` gap is disclosed.

### Narration (05)
- The Indic tokenizer fix is correct and narrowly scoped:
  - category-based L/M/N scanner, with ZWJ/ZWNJ transparent and NFC + casefold
  - 3 new regression tests (Devanagari, Bengali-Assamese, ZWJ, English unchanged)
  - honestly documented in `CHANGES.md` (58 passed + 2 FFmpeg-only failures)
- Loudness of −16 LUFS ±1 / ≤ −1 dBTP is consistent across narration code, runbook, playbook, the 12 docs, the anim-qa rubric and both token files.

### Skills library (06)
- 57 + 15 = 72 skills; `SKILLS_MATRIX.csv` parses to 72 rows (32/15/10/15) with no duplicates and every path resolving.
- The copies in 06 are byte-identical to the pack sources.
- Every owner skill named in the overlap addendum exists.

### Human-feel research (11)
- **Your direct questions are answered.**
  - The jingle question: "no, not as a mask; yes, as a crafted owned bed in specific sections", muted during derivations.
  - "Emotion then dub": answered via the speech-to-speech (STS) route.
  - Hindi/Hinglish: covered.
  - Assamese: deferred to a human voice.
- **Citations hold up.** 20 sampled citations all match their sources, and contested items are labelled. Claim counts (39 + 76 = 115) are correct.

### Advanced animation layer (12)
- **Code health.**
  - All 26 executable scripts pass `--selftest` offline (20 Python, 3 JS, `preflight.sh`, `reference_analysis.sh`).
  - The harness tools and the motion-harness skill copies are byte-identical (AD-36).
  - `scene_template.html` passes strict L2 lint.
  - The example cue sheet validates, and production mode correctly rejects it.
- **Skill structure.** All 15 skills are complete (SKILL.md, references, templates, evals, scripts) with valid frontmatter. Internal references resolve.
- **Inputs used.** All five reference videos are captured and used heavily (V1–V5).
- **Edge cases.** All 65 have an owner skill that exists.
- **Accuracy invariant.** Fixture routing, read-only props, the text–fixture QA diff (selftest catches 1.50 vs 1.05 and CO vs Co), and no image-model text.
- **Vertical typography.** Minimums are derived correctly: 88×0.5625→50, 112→63, 104→59, and 50 px ≈ 16.7 px on a phone, which is at least RD-18's 16.5 px.
- **Safe zones.** Safe-zone insets are honestly marked `measured: false`.
- **Effort and ultracode.** The 3-loop authoring cap is consistent everywhere. Ultracode is refused by `effort_policy.py` and NT-01.
- **Paid generation.** It is ledgered, idempotent and capped: unknown price, missing cap and video generation all block.
- **Honesty.** The setup document records this Mac's blockers correctly (Node 20.19.4, no ffmpeg/ffprobe, Python 3.14). Unsourced HyperFrames/Remotion commands are marked "verify".
- **Hygiene.** No secrets anywhere in the repo. Only 6 of 283 relative links are dead, all of them ChatGPT `sandbox:` links.

### Strong-to-cheap strategy (13) and costs (08)
- **Arithmetic.** It is correct throughout §7.3–§7.13:
  - per-call costs (Fable $0.18375, Opus $0.075, Sonnet $0.039, Haiku $0.00195)
  - all scenarios
  - the [V1] scaling (600/79 = 7.59)
  - open-model break-even
  - the floors ($5.96 / $1.96 / $0.59) and every ratio
  - payback (220/297 lessons)
  - capacity: 1,417 h ≈ 8.85 FTE-months per 1,000 lessons
  - the Wilson bounds
- **[V1] figures.** They match the transcript exactly (79 s; ~78K→625K tokens; ~$3→$49; ultracode ≥2.5M tokens / ≥$348, never finished).
- **08 Parts A–E.** They recompute correctly. The arithmetic is right; it is the cash *framing* of review that is now out of date.
- **Non-negotiables kept.** Section 13 keeps both human approvals for lessons, verifier-only advancement, no LLM sign-off on science and no student data to hosted models.
- **Honest status.** Status banners in 07, 12 and 13 honestly say nothing has been agent-evaluated, metered or student-tested.

---

## 3. Confirmed findings, ranked by severity

Duplicates across lenses are merged; the lens IDs are listed so you can trace each one.

### MAJOR

**M1. Vertical-only is not in the operating documents.**
*Source findings:* goal-alignment-1, cross-section-consistency-1, completeness-vs-asks-1, executability-1, sceptic-and-bloat-1, factual-and-arithmetic-correctness-5.

The only record of the decision is the addendum at 07/10 line 62 ("RD-16 … is superseded"). Everything people actually work from still says 16:9:

| File | What it still says |
|---|---|
| 07/11_MASTER_CHECKLIST line 104 | "S12 render 16:9 (1920×1080 @ 30 fps)" (I re-checked this line during this audit) |
| 07/03 line 3 | "ONE long-form lesson (16:9)" |
| 07/03 line 239 | master table "1920×1080 (16:9)" |
| 07/03 line 290 | `--aspect 16:9` |
| 07/06 line 86 | "≈190 px reserve at 1920×1080" |
| 07/00 line 33 | 16:9 at S12 |
| 07/README line 69 | "render (16:9, then recomposed 9:16)" |
| ROOT README pipeline line | "approved 16:9 export … → 9:16 recomposition" |
| 10 pilot step 6 | "Render both 16:9 and 9:16" |

The RD-16 row itself is not struck through. The engine CLI also defaults to 16:9 and hard-codes 1280×720 / 720×1280 (`pipeline.py:35`, `visuals.py:74`).

**Fix:**
1. Mark the RD-16 row SUPERSEDED.
2. Rewrite 07/03 (scope line, master table, S12), 07/00, 07/06 §3, 07/11 lines 39 and 104, 07/README §3 and the ROOT pipeline line to say 1080×1920 @ 30 fps.
3. Change the pilot benchmark to 9:16, with 16:9 only as an unscored smoke test.
4. Add a P1 build item for a 1080×1920 output mode in the proof renderer.

Related minors:
- *(contested)* executability-8: the addendum implies the renderer can simply be re-run at 1080×1920, but that needs a code change. Reword it to match C13.
- executability-13: the walkthrough B.6 still renders `--aspect 16:9`.
- science-safety-nonnegotiables-13: 12/10 A11 still accepts 1920×1080.
- goal-alignment-13 and cross-section-consistency-13: style tokens and AD-07/Q16/C1 still cite RD-16 as the authority, or as open.

**M2. No AI-voice disclosure gate anywhere in the release path.**
*Source findings:* goal-alignment-2, completeness-vs-asks-7, science-safety-nonnegotiables-2.

`grep -i disclos` over 07 finds only an unrelated table cell and roadmap lines. The S14 export record (07/03 line 317) has no AI-use field. The disclosure exists only as a playbook *recommendation* (Step 14, §9 "Step 14 disclosure tick"). A lesson that follows the runbook ships with no disclosure, which breaks your honest-marketing goal.

**Fix:**
- Add a blocking check to 07/06 §6.1 and to the GF/GS/SH publish steps:
  - a description line
  - the YouTube altered/synthetic toggle
  - the Meta label
  - C2PA not stripped
- Add `ai_voice_disclosure` and `performer_credit` to the S14 export record and the ShortSpec.
- Add the check to 12/10 §5 and 07/11.

Related minor, science-safety-nonnegotiables-3: the suggested wording ("Lesson performed by [Teacher] …") would be false on Path B (pure TTS) Reels and recaps. Provide two templates:
- Path A: performed by X, voice converted with AI.
- Path B: AI-generated narration, script by X.

**M3. Section 13 lets Reels skip their second approval.**
*Source findings:* goal-alignment-7, cross-section-consistency-5, science-safety-nonnegotiables-1.

STRATEGY §5.7, line 608, which I re-checked, says: "The Reel inherits the lesson's science approval and keeps one short human check", and the LLM writes new hook and caption text. This contradicts:
- 07/05 principle 5: each Short is a new hashed artefact needing its own academic and production approvals (gate GS).
- 07/05 line 59: new spoken wording is new script.
- 12 AD-12: the storyboard gate is mandatory for every Reel.

**Fix:** Rewrite §5.7.
- An LLM-drafted hook or CTA is new script and goes to GA.
- Each Reel gets the full A-suite and GS (two identities, bound to the Reel's hash).
- A deterministic cut-down may *shorten* review because approved claim IDs carry over, but it does not remove a gate.

**M4. Section 13's kit pipeline puts academic approval after rendering and has no storyboard gate.**
*Source findings:* science-safety-nonnegotiables-8, sceptic-and-bloat-3.

The §2.1 diagram (line 218) runs: render ×2 → QA report → "HUMAN GATE 1 (academic: script, fixtures, storyboard)". §5.5 runs GA → TTS, with no H-SB step. The required order (12/05 §1) is GA → storyboard gate → narration and paid assets.

**Fix:** Redraw the diagram and rewrite §5.5 as: GA (bundle hash) → H-SB → TTS → cascade → A-suite → GF, with GS for Reels.

**M5. The animation layer, the storyboard gate and the ultracode ban are not in the runbook.**
*Source findings:* executability-2, sceptic-and-bloat-2, completeness-vs-asks-2, goal-alignment-3.

All 18 amendments (PA-01…PA-18, 12/02/11 §7) are still proposals ("do not edit ROOT/07"). A grep of 07 for `H-SB|storyboard gate|ultracode|cue sheet|S-ANIM|preflight` finds nothing. As a result:
- S8 has no human gate.
- 07/01 still calls Node 22+ "optional, benchmark only".
- The checklist has no preflight, no S-ANIM and no animation-authoring cost line.

**Fix:**
1. Record the accepted PAs as RD rows.
2. Apply at minimum:
   - PA-03: H-SB between S8 and S9/S10 in 07/00, 07/03 and 07/11.
   - PA-07: A-checks in 07/06.
   - PA-11: animation-authoring line in 07/08.
   - PA-12: the effort/ultracode rule in 07/09 §4 and 07/08.
   - PA-17: checklist Section A (12/02/01 setup, `preflight.sh`, S-ANIM).
3. Make Node 22+ and Chrome required in 07/01 whenever animation is in scope.

**M6. The "$0 review" decision never reached the runbook or the cost docs.**
*Source findings:* goal-alignment-6, cross-section-consistency-2, factual-and-arithmetic-correctness-6, completeness-vs-asks-3, sceptic-and-bloat-4.

It exists only in 13 §7.13 and the ROOT README. Everything else still treats review as paid:

| File | What it still says |
|---|---|
| 07/README line 75 | "human review is the dominant cost" |
| 07/README line 98 | "Human review, not AI, is the cost driver" |
| RD-15 | budgets $26.67 for review |
| 07/08 line 24 | "45 min × $20/h = $15.00" |
| 08 README / CONSOLIDATED Part E.7 | "88% / 78%" review share |
| Business plan | Rs 3,000 per reviewed video |
| 13 §9.1 risk 1 | "review is about 78%" (contradicts §7.13 in the same document) |

**Fix:**
- Add a new RD row (e.g. RD-41): review cash is $0, and 85 min per lesson is kept as a *capacity* metric (≈1,417 h per 1,000 lessons).
- Add dated addenda to 07/README §3/§4, 07/08 §1/§4/§9, the 08 README and CONSOLIDATED Part E, giving the review-free totals and pointing to 13 §7.13.
- Reword the principle to "review minutes, not AI, are the throughput constraint".
- Relabel the business Rs 3,000 line as opportunity cost.

**M7. The cue-sheet builder's output fails the harness schema.**
*Source finding:* completeness-vs-asks-4.

The `sheet = {...}` dict in `12/03_skills/examleaf-cue-sheet/scripts/build_cue_sheet.py` (line 203) emits `scene_id, fps, duration, words, beats, cues, sfx`. `04_harness_contract/cue_sheet.schema.json` line 8 *requires* `schema_version`, `language`, `narration_audio_sha256` and `script_sha256`. I re-checked both files during this audit. Every built sheet will be rejected; the selftests pass only because none of them runs the builder output through the schema.

**Fix:** Emit the four fields from the spec and provenance hashes. Add a selftest that runs builder output through `04_harness_contract/validate_cue_sheet.py --production`.

**M8. The runbook's language scope contradicts your decision.**
*Source finding:* goal-alignment-4.

- RD-26 says "en-IN only".
- 07/03 line 152 offers "Assamese-supported or Hinglish editions" and does not name Hindi.
- 07/04 §18 routes Assamese through TTS providers.

Your scope is Indian English, Hinglish and Hindi now, with Assamese later through a human voice.

**Fix:**
- Add a row superseding RD-26.
- Set launch locales to en-IN, Hinglish and hi-IN, each behind the existing locale gate.
- Mark as-IN as deferred and human-voiced, with no Assamese TTS commitment.
- Update 07/03 S5 rule 10 and 07/04 §18.

**M9. The playbook's 3 s pause cap cuts the student's think window short.**
*Source finding:* science-safety-nonnegotiables-4.

- PLAYBOOK Step 1 says "Scripted pauses are capped at 3 s".
- Step 8 says "up to 3 s maximum".
- RD-11 and the brief template require a 5–8 s prediction window (default 6 s) with the answer hidden.
- The 07/10 addendum wrongly says nothing in the playbook is contradicted.

**Fix:** Scope the 3 s limit to TTS break tags only. Protected think windows follow RD-11 (room-tone insert, default 6 s) or pause-video. Correct the addendum.

**M10. The storyboard approval record can be forged and has only one role.**
*Source finding:* science-safety-nonnegotiables-9.

- The `templates/approval_record.json` used by the skill and brief has one `"role": "production"` and one `reviewer_id`.
- It binds the estimate, beats, grid and script, but not fixtures, style or hero.
- `estimate_and_gate.py verify()` checks only that `reviewer_id` is at least 3 characters plus a hash the agent computes itself.
- The file sits in the agent's workspace, and `storyboard/**` is not in the deny list.
- Doc 05 §5.1 specifies two approvers (founder for cost, academic lead for science fit) and fixture/style/hero hashes.

**Fix:**
- Align the template with doc 05.
- Have the runner, not the agent, verify the approval against the authenticated service.
- Add `Edit(./storyboard/**)` to the deny list.

**M11. `preflight.sh` is credited with checks it does not perform.**
*Source finding:* executability-6.

12/02/01 §9 and §6.5 credit preflight with a secret scan, ultracode/alias greps, model pinning, a Manim variant check and repository weight. V13 relies on this. The script checks only:
- node, npx, ffmpeg/ffprobe, python
- Chrome
- fonts
- disk
- the skills symlink

**Fix:** Add at least the secret scan and ultracode greps (reusing `effort_policy.py`), or relabel the §9 table as implemented vs proposed and point V13 at the effort governor only.

**M12. Section 13's verifier stack duplicates checks that exist, contradicts the timing rule and drops required checks.**
*Source findings:* cross-section-consistency-6, science-safety-nonnegotiables-7, sceptic-and-bloat-6.

- **Duplicates.** V2 (fixture/text diff) and V4 (layout/safe zone) are marked "New". `examleaf-anim-qa/scripts/text_fixture_diff.py` and `safe_zone_check.py` already exist and pass selftest.
- **Timing conflict.** V5 uses ±150 ms. The contract says a reveal lands on its word's t0 or up to 0.05 s before it, never late.
- **Determinism.** V3 drops the reverse-order render that AD-21 requires.
- **Missing checks.** Nothing mentions the A1–A17 suite, the answer-hidden window, flash checks, licences, loudness or caption fidelity.

**Fix:**
- Make V2 and V4 *point to* anim-qa.
- Set V5 to the contract rule (late = fail), with ±150 ms as a quality metric only.
- Add reverse-order rendering to V3.
- State that V0–V8 are *in addition to* 12/10 and 07/06.
- Route fixture-visual archetypes to the existing SVG/Manim adapters.

### MINOR

**Stale test counts and integrity claims.**
*Source findings:* goal-alignment-9, factual-and-arithmetic-correctness-3, completeness-vs-asks-6, executability-3, science-safety-nonnegotiables-17, sceptic-and-bloat-8, executability-9, cross-section-consistency-12.

- Gate P-3, the S-GATE row, checklist line 20, 07/06 §10, the 05 README and INSTRUCTIONS, and the ROOT README all say "57 passed".
- The suite is now 52 test functions / 60 cases: 58 pass plus 2 FFmpeg failures here, and 60 pass with FFmpeg installed.
- `DELIVERY_MANIFEST.json` now shows a diff for `pronunciation.py` and `tests/test_narration.py`. The ROOT "byte-identical" provenance sentence and the 05 "English-only comparator" description are now untrue.
- **Fix:** Update every gate. Note in 07/01 and 05 that the two files differ from the manifest on purpose (see `CHANGES.md`). Mark the loudness gate as verified only where FFmpeg is installed.

**Section 13 cost framing overstates the savings.**

- factual-and-arithmetic-correctness-1: "40–100× at the lean floor" is not reached by its own table (maximum ≈7× against an Opus Kit, 14–27× against bespoke generation). It appears only against [V1]-max.
- factual-and-arithmetic-correctness-2, cross-section-consistency-8, sceptic-and-bloat-5: the "Today" baseline ($1.716) is priced at 4.6-era tariffs while the Kit rows use the verified 5.5 prices. On one price basis, today = $7.17 and the cascade saves about 2%.
- factual-and-arithmetic-correctness-4: the lean-floor TTS price ($0.14) doubles on 1 Jan 2027 to $0.28. The ratios become ≈6.2× and 12–23×.
- cross-section-consistency-9: the "today" baseline still includes $4 of generated clips, which the runbook already set to 0.
- factual-and-arithmetic-correctness-7: "open models save <1%" is stale; it is 5–33% now that review is $0.
- factual-and-arithmetic-correctness-8: the "upper bound" is actually a floor.
- factual-and-arithmetic-correctness-9: the batched cascade is ≈$0.71–0.80, not $0.60–0.70.
- factual-and-arithmetic-correctness-10 and completeness-vs-asks-12: the S-arm budget is $385 vs $435; the $2,317 figure uses the $1,000 cap.
- factual-and-arithmetic-correctness-14: cache reads are 2.5–10% of input price, not 10%.
- factual-and-arithmetic-correctness-15: several approximations are off.
- factual-and-arithmetic-correctness-17: the rater table assumes 20 shadow pairs; the design produces 10.
- factual-and-arithmetic-correctness-18: the word count is ≈13,500.
- goal-alignment-8 and sceptic-and-bloat-12: the floors assume TTS, but the playbook requires a teacher performance + STS for every full lesson, plus cutaways and Higgsfield credits. Add a Path A row and performer and storyboard-review minutes, or state that the lean floor applies only to Path B content.

**Effort and ultracode conflicts.**
*Source findings:* cross-section-consistency-4, cross-section-consistency-15, completeness-vs-asks-5, science-safety-nonnegotiables-14, goal-alignment-11, cross-section-consistency-16.

- Section 13's cascade (Haiku authors scene code, up to about 10 calls per scene) contradicts AD-02/AD-11/AD-24, and the shipped governor would refuse it.
- The $50 S5 "Ultra" probe has no exception path in the governor (which refuses ultracode even in sandbox mode). It relies on a billed-usage cap that 12 says is not a hard limit.
- The edge-case table #3 allows ultracode in a sandbox.
- Sections 12 and 13 disagree on Sonnet 5.5's default effort (Claude Code vs API surface).
- **Fix:**
  - Record a new AD that scopes AD-02/11/24 to the strong-model phase, and add a `kit_cascade` family with its own caps to `effort_policy.py`.
  - Either drop S5, or make it a founder-approved, attended-only exception with a provider-side spend limit, which can never enable ultracode in production.
  - State the per-surface effort defaults in one place.

**Safe-zone geometry disagrees in three ways.**
*Source finding:* cross-section-consistency-3.

| Source | Zone split | Side margin |
|---|---|---|
| `layout_zones.py` | 0.18/0.57/0.25 | 90 px |
| tokens and template | 0.22/0.54/0.24 | 60 px inset |
| `style_tokens` | — | 96 px |
| stale note | 0.20/0.58/0.22 | — |

**Fix:** Make `vertical_safe_zones.tokens.json` the only owner, and have the scripts read from it.

**Loudness and music records.**
*Source findings:* goal-alignment-14, cross-section-consistency-10, completeness-vs-asks-10, cross-section-consistency-11, science-safety-nonnegotiables-11.

- AD-37 writes "−1.5 dBTP" for a value that is actually a sample-peak dBFS figure. `import_clip_notes` §6.3 still says "unresolved" and points to a token key that no longer exists.
- AD-15 says music is off under teaching, but AD-37 and the tokens set a "teaching bed" level. The allowed-placement lists differ on recaps.
- The playbook says music is "genuinely human-composed" while audio-compose generates beds in code. The ducking ranges also differ (15–20 vs 20–24 dB).
- **Fix:** Pick one policy for each of these.

**Free-chapter policy drift.**
*Source finding:* goal-alignment-5.

RD-20 defaults to "three carefully selected" chapters and the business plan adds an optional INR 299 digital-only edition. You said "first 3 chapters free". This needs your decision, recorded as an RD row.

**Section 13 is not registered.**
*Source finding:* cross-section-consistency-7.

There is no 07/10 addendum, no 07/README row and no 06 owner for the eight `examleaf-fill-<archetype>` skills or the templates.

**Two cue-sheet validators.**
*Source findings:* completeness-vs-asks-11, executability-11, sceptic-and-bloat-7.

- They have different CLIs (positional vs `--sheet`) and tolerances (1e-6 vs 1e-3).
- The skill copy skips `$ref`, `pattern` and `maximum`, and accepts `alignment_source: "example"`, which the harness validator rejects in production mode.
- The builder keeps ZWJ/ZWNJ inside tokens, while the narration comparator now drops them.
- **Fix:** Delete the skill copy and call the harness validator.

**Setup executability.**

- executability-4: 07/01 omits that ffmpeg (not only ffprobe) is missing and that Node is 20. Node 24.6.0 is already installed under nvm (`nvm use 24`).
- executability-5: venv commands do not pin 3.13. This Mac has 3.14 and 3.11, and no `python` binary.
- executability-7: no frame-render command exists for the V10/V11 determinism gate.
- executability-10: the canonical skills location disagrees between 06 and 07/01, and there is no `animation/` package in the repo tree.

**Safety minors.**

- science-safety-nonnegotiables-5: Path A performers may change approved wording with no ASR diff and no GA re-approval.
- science-safety-nonnegotiables-6: anim-qa rates untraceable science text and full-frame flashes as *major*, which a human can waive. Make them critical.
- science-safety-nonnegotiables-10: the deny list `Read(../**)` blocks the style and contract files the brief tells the agent to read. Stage hashed copies into the workspace.
- science-safety-nonnegotiables-12: an early answer reveal is Major in 07/06 but Critical in 12/10. Make it Critical.
- science-safety-nonnegotiables-15: student-panel consent is hedged "where needed". Require guardian consent for every participant under 18, collect anonymous ratings only and gate the panel on G3.
- science-safety-nonnegotiables-16: the "31 of 31" negative tests do not apply to the no-chat slot-fill path. Add NTs for disclosure removal, fake sensing and activation secrets.
- science-safety-nonnegotiables-18: "you've got this" is an unconditional confidence statement, and the third-party STS processor is not admitted under 07/07.

**Navigation and counts.**

- goal-alignment-10 and completeness-vs-asks-13: the ROOT "Start here" table has no rows for sections 11–13. It and the install guide still say "57 Skills".
- 09 VERIFIED_vs_PROPOSED does not reference sections 11–13.
- factual-and-arithmetic-correctness-11, factual-and-arithmetic-correctness-12, factual-and-arithmetic-correctness-13: wrong counts (72 skills; 34 sheets, not 35; 15 source URLs, not 12).
- completeness-vs-asks-14: stray `__pycache__` folders; 05 has 131 files and 12 has 224 (excluding `__pycache__`).
- *(contested)* executability-12: the documented selftest commands should use `python3 -B -I`.
- *(contested)* executability-14: add a note at the top of each FULL_ transcript mapping its `sandbox:/mnt/data/...` links to the `00_source/extracted` equivalents.

**Other.**

- goal-alignment-12: the playbook says "3–5 Reels cut" and "Remotion/manim-voiceover". It should say 1–3 recomposed complete units, with HyperFrames as the default.
- cross-section-consistency-14: two token notes still say the typography conflict is "unresolved"; RD-01 resolved it.
- factual-and-arithmetic-correctness-16: three research-report statements are cited to [N#] quotes that do not support them (N28, N49, N36).
- completeness-vs-asks-9: edge cases #53 and #62 have nominal owners that never mention them.
- completeness-vs-asks-8: the "YouTube tricks/tutorials" part of your ask is thin, because creator videos were never transcript-reviewed. Microdrama speech rate is still an unmeasured hypothesis.
- *(contested)* cross-section-consistency-17: pilot sets drift apart. Maths is dropped from the 12/13 pilots, and the Ohm's-law item is blocked on an `iv_graph` kind that does not exist yet.
- *(contested)* cross-section-consistency-18: the scene-count models are incompatible (7 vs 30 scenes per lesson).

---

## 4. Drift from the goals

| Goal | Status | Where it drifts |
|---|---|---|
| Vertical 9:16 only | Decided, not applied | 07 body, checklist, ROOT README, engine defaults (M1) |
| Super Teacher persona, human feel | Aligned | Pause cap undercuts the think window (M9); unconditional confidence line |
| Science only from fixtures | Aligned in 07/12 | 13 verifier stack omits the A-suite (M12); anim-qa waivable majors |
| Two human approvals | Aligned for lessons | Reels lose GS in 13 (M3); storyboard approval is single-role and forgeable (M10) |
| Book-linked funnel, platform enforces | Aligned on enforcement | "First 3" became "curated"; digital-only SKU added without your decision |
| Honest marketing, AI-voice disclosure | **Not enforced** | No gate or field (M2); Path B wording would be false |
| Languages en/Hinglish/Hindi, Assamese later by human | **Contradicted** | RD-26 en-only; Assamese routed through TTS (M8) |
| Minors' data caution | Aligned | Panel consent is hedged |
| Strict cost control | Aligned in 12 code | Storyboard gate and ultracode ban missing from runbook (M5); $0 review not in cost docs (M6); 13 headline savings overstated |
| Animation layer, strong→cheap Kit | Sound design | Not wired into 07; 13 cascade conflicts with the governor; nothing agent-evaluated; machine cannot render yet |
| Documented end to end with verified/proposed status | Mostly | Sections 11–13 missing from the start-here table and the verified/proposed register |
| Nothing omitted from ChatGPT | **Met** (hash-verified) | none |

The pattern is the same everywhere. Each new section respected "do not edit 07", so the runbook stayed frozen while the decisions moved on.

---

## 5. What to cut, merge or defer (sceptic lens, verified items only)

- **Merge the duplicate cue-sheet validator.** Delete the skill copy and call `04_harness_contract/validate_cue_sheet.py --production`. Add it to the AD-36 `cmp` drift check.
- **Delete `reference_analysis.sh`.** AD-35 already names the Python analyser as canonical. Also delete the `__pycache__` folders.
- **Do not build new V2/V4 verifiers in 13.** Extend `text_fixture_diff.py` and `safe_zone_check.py`. Route symbolic and fixture-visual archetypes to the existing SVG/Manim adapters.
- **Use one pilot plan and one benchmark.** Vertical only, 4 subjects (keep Maths) with one Reel each, using 12's benchmark document. Mark the 10 four-pilot instructions as superseded where they conflict.
- **Shrink the 13 campaign** *(contested)*. About 20 arms and ≈185 engineering hours is not realistic beside the 07 roadmap. Phase 1: 3 archetypes, arms P-low, C3-medium and C4, and one integration lesson. Defer S3/S4/S5, the C1/C2 variants, O1/O2, T3/T4 and the V6/V7 judges until one lesson ships. Have someone who never authors templates own the "sealed" holdout, or drop the claim.
- **Merge extender skills into their owners** *(contested)*. All 15 new skills are extenders that must load with an owner. Merging them into references/ files cuts about 10 skills. Do not add the 8 fill-skills until the archetypes pass C4.
- **One canonical copy per contract** *(contested)*. Make `contract.md` canonical and reduce doc 04 to a pointer. Keep 2 house styles (paper-collage-vertical, kinetic-type) for the pilot and move the other 3 to a backlog folder. Label 12/02_documentation as reference for Kit authors, not operating documents.
- **One ledger** *(contested)*. Use a single append-only `ledger.jsonl` with `{unit: usd|credit|ktok, stage, run_id}`, reported by examleaf-observability-cost.
- **Gate on scene-level counts** *(contested)*. The 5 samples per scene are correlated. Treat the 85-minute review baseline as a hypothesis until it has been timed.

---

## 6. Do this next (in order)

1. **Decide and record three founder rows in 07/10.**
   - RD-16 superseded (vertical 1080×1920 @ 30 fps).
   - Review cash $0, tracked as capacity.
   - Languages en-IN / Hinglish / hi-IN now, Assamese later by human voice.

   Also decide: first-3 vs curated free chapters, and whether the digital-only SKU is in the launch.
2. **Apply vertical-only in place** across 07/00, 03, 06, 11, 07/README, the ROOT README, the 10 pilots, 12/10 A11 and the walkthrough B.6 (M1).
3. **Add the AI-voice disclosure gate.** Export fields plus a release blocker, with Path A and Path B wording templates (M2).
4. **Fix section 13's gate order and Reels approvals.** GA → H-SB → TTS → cascade → A-suite → GF, with full GS per Reel (M3, M4). Align the V0–V8 stack with anim-qa and the timing contract (M12).
5. **Apply PA-03, PA-07, PA-11, PA-12 and PA-17 into 07.** That covers the H-SB gate, A-checks, the animation cost line, the effort/ultracode rule, and setup plus S-ANIM in the checklist (M5).
6. **Fix the cue-sheet builder.** Emit the 4 required fields, add a builder→harness-validator selftest and delete the duplicate validator (M7).
7. **Harden the storyboard approval.** Two roles plus fixture/style/hero hashes, verified by the runner, with `storyboard/**` denied (M10). Make untraceable science text and full-frame flashes critical in anim-qa.
8. **Fix the playbook.** Limit the 3 s pause cap to TTS break tags (6 s think window protected), add the Path A ASR diff against the approved script, and use 1–3 recomposed Reels.
9. **Refresh the numbers.**
   - Narration gates: 60 / 58+2.
   - Skills: 72.
   - Re-price "Today" at 5.5 tariffs.
   - Correct the 40–100× claim.
   - TTS price at $0.28 from 2027.
   - Add the $0-review addenda to 07/08 and 08.
   - Add Start-here rows for sections 11–13.
   - Reconcile `preflight.sh` with its documentation.
10. **Unblock this Mac and ship one vertical lesson end to end.**
    - Install ffmpeg/ffprobe, run `nvm use 24` and create a Python 3.13 (or 3.11) venv.
    - Add a minimal frame-capture command for the determinism gate.
    - Produce one 1080×1920 lesson plus one Reel through both human gates before writing more documentation.

---

## 7. Audit method and limits

**Method.** Seven lenses ran in parallel over the whole project tree. Each lens produced findings with file and line evidence. A second, adversarial checker then tried to refute each one; findings one checker refuted are marked *(contested)*. The checks included:

- recomputing about 120 cost figures by hand
- matching sampled claims against SOURCES quotes (about 37 in 11 and 12)
- SHA-1 matching of all 462 extracted files and 23 downloads against sections 01–13
- running every offline `--selftest` (26 scripts)
- `cmp` and `diff -rq` on skill and harness copies
- parsing `SKILLS_MATRIX.csv` and the skill frontmatter
- walking 283 relative markdown links
- a regex secret scan
- live checks of this Mac's toolchain

For this report I re-checked four headline findings directly:
- checklist line 104 (16:9)
- the cue-sheet schema's required fields against the builder dict
- 13 §5.7 line 608 ("inherits the lesson's science approval")
- ffmpeg absent and Node v20.19.4

**Limits.**
- Nothing was rendered: FFmpeg is absent, Node is 20 and HyperFrames is not installed. Determinism, loudness and visual quality are verified only by design and selftests.
- No skill has been agent-evaluated. The evals are authored, not executed.
- No cost figure has been metered. All Kit and cascade inputs are hypotheses until the week 1–4 measurements.
- Platform-side behaviour (YouTube/Meta AI labels, entitlement service) was checked against the documentation only.
- Prices were checked against the project's SOURCES files, not live pricing pages, on this audit pass.
- The release gates were read, not executed, per the brief.
- Reviewer selftest runs left two `__pycache__` directories in 12/03_skills. They are safe to delete.
- Contested findings are lower-confidence. Each needs a judgement call rather than a mechanical fix.
