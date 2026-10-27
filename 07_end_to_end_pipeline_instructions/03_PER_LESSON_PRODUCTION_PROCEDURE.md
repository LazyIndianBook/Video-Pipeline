# 03 · Per-lesson production procedure: one lesson from permitted PDF to approved export

**Scope.** Everything that happens to ONE long-form lesson (vertical 9:16, 1080×1920 @ 30 fps; changed 15 Oct 2026 from "16:9" because RD-16 is SUPERSEDED) from a permitted source PDF to an approved, hash-bound export. Narration internals are in [`04_NARRATION_SUBPIPELINE.md`](04_NARRATION_SUBPIPELINE.md); vertical Shorts in [`05_SHORTS_and_REELS_PROCEDURE.md`](05_SHORTS_and_REELS_PROCEDURE.md); every check and gate in one list in [`06_QA_GATES_and_RELEASE.md`](06_QA_GATES_and_RELEASE.md).

**Status.** The order is the engine's 12-step production runbook ([`04_video_engine/implementation_v2/docs/Production_Runbook.md`](../04_video_engine/implementation_v2/docs/Production_Runbook.md)), the v2 architecture (message 10 §5) and the Skill stage map ([`06_skills_library/SKILLS_PIPELINE_STAGE_MAP.md`](../06_skills_library/SKILLS_PIPELINE_STAGE_MAP.md)). All of it is [PROPOSED] except the pieces marked [TESTED]. All Skills named are [DRAFTED], not agent-evaluated: evaluate each before relying on it (01 §6.4). In the first lessons, every Skill's output is treated as a draft that a human checks.

**How each stage is written.**

> **Do** · **Fires → Owner** (Skills; owner in bold) · **Input** · **Output artefact** (path inside the lesson folder) · **Automated check** · **Pedagogy fields filled** (of the 12 in [`02_learning_psychology/SCENE_PEDAGOGY_SCHEMA.md`](../02_learning_psychology/SCENE_PEDAGOGY_SCHEMA.md)) · **Design / timing rules** · **Human gate** · **Sources**

Skill names omit the `examleaf-` prefix in tables (VE = Video Engine pack, NA = Narration pack, ST = Super Teacher kit).

---

## 1. The lesson folder [RD-25]

Create one folder per lesson in the canonical repository. It holds v1's 17 required artefacts (message 02 / `planning_pack_v1/QA_and_Implementation_Contract.md`: source-ledger.json; syllabus-map.json; claims.json; verified-model.json; lesson-spec.json; scene-spec.json; approved-script.txt; pronunciation.json; audio/*.wav; alignment.json; render-manifest.json; test-results.json; final.mp4; captions.vtt; captions.srt; transcript.txt; reviewer-approvals.json) plus the v2 and narration artefacts.

```text
lessons/<board>/<class>/<subject>/<lesson_id>/
├── 00_intake.json            lesson_id, board + division, academic year, class, subject, medium/language,
│                             edition, business chapter/question IDs, proposed free/paid designation
├── source-ledger.json        SourceRef[] + source SHA-256 + rights record           (S1)
├── source-native.json        native extraction, page by page                         (S1)
├── syllabus-map.json         versioned coverage map + unresolved items              (S2)
├── claims.json               Claim[] with status                                     (S3, S7, GA)
├── answer-keys.md            independently solved answers incl. boundary cases       (S3)
├── lesson-spec.json          LessonPlan + v1 LessonSpec fields + 600 s beat plan     (S4)
├── script/                   narration_plan.json · beat_table.json · change_log.md · analogy_cards.json ·
│                             humour_candidates.json · interactions.json · script_prereview.md ·
│                             approved-script.txt (after GA)                          (S5–S6, GA)
├── science/                  verified-model.json · science_report.json · independent_review.json ·
│                             independently_solved_answers.md                         (S7)
├── scenes/                   scene-spec.json (SceneSpec + 12 pedagogy fields + route + cost cap) ·
│                             asset_manifest.json                                     (S8–S9)
├── audio/                    pronunciation.json (lexicon version used) · requests/ · provider_jobs.json ·
│                             raw/ · accepted/ · asr_diff.json · alignment.json · timeline.json ·
│                             master.wav · signal_qa.json · mastering_qa.json         (S10–S11, doc 04)
├── render/                   final.mp4 · render-manifest.json · captions.vtt · captions.srt · transcript.txt (S12)
├── qa/                       test-results.json · visual_qa.json · audio_caption_qa.json ·
│                             narration_quality.json · phone_readability.md           (S13)
├── approvals/                written ONLY by the authenticated approval service (GA, GF); exported audit
│                             trail = reviewer-approvals.json                          (GA, GF)
├── export/export_record.json IDs, title/thumbnail/description,
│                             attribution, approved video hash — never secrets        (S14)
│                             (15 Oct 2026, RD-49/CE-68: access designation and
│                             destination retired; platform joins by artefact id)
├── shorts/<short_id>/        ShortSpec.json, vertical render, captions, approvals    (doc 05)
├── costs.json                per-lesson cost record                                  (doc 08 §4)
└── pilot_record.md           timed reviewer record (pilots and first lessons)       (doc 02 P2)
```

---

## 2. Stage overview

| Stage | Runbook step | Owner of the output | Output | Automated check | Human gate |
|---|---|---|---|---|---|
| S0 Intake | — | Founder/ops + academic lead (human) | `00_intake.json` | IDs match platform resource IDs | Academic lead accepts scope |
| S1 Source ingest | 1 | VE **source-ingest** | `source-native.json`, `source-ledger.json` | SHA-256; native text only; flagged pages | Review figures/equations/empty pages; rights |
| S2 Curriculum map | 1 | VE **curriculum-map** | `syllabus-map.json` | Wrong-year / unsupported-coverage negatives | **Approve syllabus fit, rights, edition** |
| S3 Claim research | 2 | VE **claim-research** | `claims.json`, `answer-keys.md` | Unknown source ID rejected; hallucinated citation = hard failure | — (feeds GA) |
| S4 Lesson plan | 2–3 | VE **lesson-plan** | `lesson-spec.json` | Claims traceable; objective assessed by a fresh item | — (feeds GA) |
| S5 Super Teacher script | 3 | NA **super-teacher-scriptwriter** (draft), NA **dialogue-naturalizer** (diff); VE super-teacher = stage entry | `script/narration_plan.json`, `beat_table.json` | `examleaf_narration.cli validate`; ST `lint_script.py` | — (feeds GA) |
| S6 Analogy / humour / interaction / confidence | 3 | NA **educational-storytelling**, **humour-meme-director**, **interactive-teaching-director**, **student-psychology-director** | `analogy_cards.json`, `humour_candidates.json`, `interactions.json` | Question cue cannot show answer; `answers_after` rules | — (feeds GA) |
| S7 Scientific validation | 2, 4, 5 | VE **science-<subject>**; ST **science-reviewer** (independent re-solve) | `science/*` | Typed validators; independent re-solve | — (feeds GA) |
| **GA Academic approval** | 4 | Human academic owner (approval service) | GA record bound to script-bundle hash | Hash binding | **Mandatory** |
| S8 Storyboard + routing | 5 | VE **storyboard-route** | `scenes/scene-spec.json` | SceneSpec validation; router rules; cost cap | — |
| **H-SB Storyboard gate** (added 15 Oct 2026; PA-03, RD-43, RD-46) | 5 | Founder (cost) + academic lead (fit with the approved script), two identities, via the approval service; animation director / `examleaf-anim-storyboard-gate` assembles evidence | 3×3 grid, `beats.json`, `estimate.json`, H-SB record | Record binds grid, beats, estimate, script, fixture, style and hero hashes; verified by the runner, never written by an agent | **Mandatory** before S9/S10 and before any paid generation |
| S9 Scene data from verified state | 5 | Routed scene Skill (VE **svg-scenes** default; manim / molecule / biology / blender scenes) | component instances, `asset_manifest.json` | Same-state tests; frame-content tests | — |
| S10 Narration | 6 | see doc 04 | `audio/*` | doc 04 | Native-language review; audio listening |
| S11 Alignment + event timing | 7 | NA **speech-animation-synchronizer**; VE **alignment-localize** (localized SceneSpec) | `audio/timeline.json`, measured cues | Alignment hashes; monotonic; "Premature answer"; occurrence | Inspect difficult anchors |
| S12 Render + captions | 8 | VE **render-batch** (+ **web-composition** for the chosen compositor) | `render/*` | Probe codec/dims/duration/frames/audio; atomic move | — |
| S13 Automated QA | 9 | VE **visual-qa**, **audio-caption-qa** (+ NA narration-quality-reviewer, audio-production-engineer) | `qa/*` | Visual, science-frame, caption, audio, readability flags | Frame review; full listen |
| **GF Full final-video review** | 10 | Human academic + production reviewers (approval service); VE **release-review** assembles evidence | approvals bound to `final.mp4` SHA-256; release manifest | `release-check` | **Mandatory** |
| S14 Approved export | 11–12 | VE **release-review** (manifest); publisher | `export/export_record.json` | Approved-hash check; no secrets; `ai_voice_disclosure` + `performer_credit` present (15 Oct 2026, RD-45) | Authorize release; disclosure gate (06 §6.4) |
| S15 Cache | throughout | VE **render-batch** / NA **cost-regeneration-optimizer** | cache records | Cache key + output hash | — |
| S16 Repair loop | any | Owner of the defective artefact | new versions | ≤ 2 repair attempts; cost cap | Re-approval |

---

## S0 · Lesson intake

- **Do:** create the lesson folder; assign `lesson_id` (pattern `^[a-z][a-z0-9_-]*$` satisfies both engine and narration contracts); record board and **division** (ASSEB Division I, formerly SEBA, for Class 10; Division II, formerly AHSEC, for Class 11–12), academic year, class, subject, medium/language, edition, the business's approved chapter and question IDs, and the proposed access designation (free / preview / book-entitlement).
- **Input:** business title plan and chapter list (business W3: two Class 10 titles, one medium, three carefully selected free chapters per title by diagnostic value [RD-20]; *15 Oct 2026: **DECISION NEEDED (RD-44)** — the founder said "first 3 chapters free"; RD-20 stands until decided*); for pilots, `10_pilots_and_examples/pilots/*_600s_plan.json`. *(Resolved 15 Oct 2026: out of pipeline scope per RD-49; the pipeline is commercially agnostic and this item lives in the business layer only.)*
- **Output:** `00_intake.json`.
- **Check:** IDs match the platform's resource IDs so the QR destinations and export records line up (00 §6).
- **Gate:** academic lead accepts that the lesson is **one narrow capability** that fits about ten minutes; otherwise split ("A chapter that needs two coherent revision lessons should receive two").
- **Sources:** business runbook §3–§5; message 02 §8.

## S1 · Source ingest (runbook step 1)

- **Do:** "Confirm permitted source and official board/year scope. Store source hash and original file separately from generated content. Extract native text. Explicitly review figures, equations and empty/scanned pages; OCR is never implicit." Every claim must later retain "a source identity, page/region reference, academic-year context, and source hash".
- **Fires → Owner:** VE **source-ingest** (sole).
- **Command [TESTED on a synthetic PDF only]:** from `engine/`: `PYTHONPATH=src python -m examleaf.cli extract-pdf ../sources/<file>.pdf --out ../lessons/<…>/source-native.json`
- **Input:** a PDF you own or have permission to use, plus its rights record.
- **Output:** `source-native.json` (`source_file`, `sha256`, `extraction: native_text_only`, `pages[]` with `page_1_based`, `text`, `requires_visual_review: true`, `empty_text`; `syllabus_mapping_status: not_performed`) and `source-ledger.json` (`SourceRef`: `id`, `uri`, `locator`, `rights_status` ∈ owned / permission / open_reference / unconfirmed, `claim_scope`, `retrieved_at`; production extension: stored source hash, academic-year version, exact extracted coordinates).
- **Automated check:** SHA-256 recorded; empty/scanned pages flagged; `rights_status: unconfirmed` cannot proceed to release ("reject missing rights for release"). OCR is "an explicit reviewed exception", never implicit.
- **Human:** check recovered equations, signs, units and diagram labels by eye ("Document extraction is not scientific interpretation"). If extraction is poor, request a better original.
- **Sources:** VE `source-ingest` SKILL; engine README; message 02 §7 "Source handling".

## S2 · Curriculum map (runbook step 1)

- **Do:** map the source pages to the current official syllabus for the board, division, class, medium and academic year; list what is out of scope and what is unresolved. "Do not assume that a familiar textbook chapter automatically matches the intended syllabus or marking scheme." Never infer syllabus authority from a publisher's statement.
- **Fires → Owner:** VE **curriculum-map** → human academic reviewer.
- **Input:** `source-native.json` + verified official syllabus document.
- **Output:** `syllabus-map.json` (versioned; unresolved items listed; mapping marked pending until approved).
- **Automated check:** wrong-year and unsupported-coverage negative fixtures (Skill acceptance).
- **Human gate H-S2:** the academic owner **approves syllabus fit, rights and edition** (message 10 §5.1 "Approve syllabus fit and rights"). The Physics RC pilot needs an explicit relevance decision before publishing.
- **Gap:** no Skill owns board marking rubrics (v1 `exam-rubric` has no v2 owner). The academic owner records the official marking scheme separately from any ExamLeaf-authored answer rubric [RD-30]; the book must "Clearly distinguish an official marking scheme from an ExamLeaf-authored answer rubric".

## S3 · Claim research and independent answer keys (runbook step 2)

- **Do:** "Produce source-linked claim list, prerequisite map and independently solved exercises. **Block unsupported claims before video work.**" Answer keys are solved **independently of the creative draft** and include boundary cases.
- **Fires → Owner:** VE **claim-research** (owns canonical claims and answer keys; all other Skills reference them by ID).
- **Input:** coverage map + source spans.
- **Output:** `claims.json` (`Claim`: `id`, `statement`, `source_ids` ≥ 1, `assumptions`, `status` = `draft`) and `answer-keys.md`; prerequisite map inside `lesson-spec.json` (v1 `prerequisite-graph` has no dedicated v2 owner; lesson-plan and curriculum-map share it [RD-30]).
- **Automated check:** every `source_ids` entry must exist (contract validator; "unknown source ID rejected locally"); "hallucinated citation is a hard failure"; failing items held at `review_pending`.
- **Example of the precision expected** (the coefficient vs subscript distinction used throughout the sample lesson): `2H₂O` means two complete water molecules; the coefficient multiplies the whole formula; changing the subscript would change the substance (H₂O → H₂O₂), which is "an efficient way to solve a different question", not balancing.
- **Sources:** VE `claim-research` SKILL; `OVERLAP_and_DEDUPLICATION.md` cluster 10.

## S4 · Lesson plan (runbook steps 2–3)

- **Do:** scope a coherent, approximately ten-minute lesson around **one capability the learner must show independently**. Write the **assessment before the hook** (ST lesson-architect rule), list what is out of scope, name the **one or two prerequisites** most likely to block understanding and choose a 30–60 s repair or a separate foundation lesson ("Need the symbol-reading version? Start here." Never "for weak students").
- **Fires → Owner:** VE **lesson-plan** (owner). ST lesson-architect rules folded into its checklist (assessment first; out-of-scope list; scope down rather than invent).
- **Input:** approved claims + prerequisite map.
- **Output:** `lesson-spec.json` containing
  - `LessonPlan` (v2, [TESTED as a schema]): `id`, `board`, `academic_year`, `subject`, `class_level` (10–12), `language`, `objective`, `prerequisites`, `sources`, `claims`, `target_seconds` (default 600, ≤ 1200), `source_review_status`, `syllabus_review_status`, `actual_audio_seconds` (null until measured);
  - the v1 `LessonSpec` fields not yet in code [PROPOSED]: worked problems, retrieval questions, expected answers, exam terminology, narration reference;
  - the **11-beat 600 s plan** [RD-13] (0–25 curiosity · 25–60 prerequisite · 60–120 intuitive model · 120–180 formal model · 180–270 worked example · 270–315 micro-recap · 315–390 guided example · 390–455 independent practice · 455–510 feedback · 510–560 exam conversion · 560–600 confidence and spacing), each beat `script_status: requires_authoring_and_review`;
  - draft pedagogy fields per beat: **learning objective, prerequisite, misconception, delayed assessment**.
- **Automated check:** objective assessed by a fresh item; all claims traceable (`LessonPlan` raises "unresolved source claim"); beats sum to `target_seconds`.
- **Failure rule:** "Split over-dense chapter into two lessons." "Ten minutes is a format target, not a scientific law" (do not stretch a six-minute idea, do not compress by speaking faster).
- **Sources:** VE `lesson-plan`; `10_pilots_and_examples/pilots/PILOT_PLANS_SUMMARY.md`; message 02 §8, §11; message 08 §3.2.

## S5 · Super Teacher script (runbook step 3)

**Do:** draft the complete lesson in the Super Teacher voice, with spoken language separated from formulas, directions and timing. "Require a worked, faded and independent task; humour and stories are optional and must preserve the model." Timing is **PLANNED** until real audio is measured.

**Fires → Owner:** VE **super-teacher** (stage entry, emits the handoff) → NA **super-teacher-scriptwriter** (authors the draft **once**) → NA **dialogue-naturalizer** (minimal wording diff that may never delete *not*, increase/decrease, conditions or negative exponents). Review lenses folded into the checklist: ST conversational-script (offer alternative openings, choose one and justify; exact exam terminology after the plain-language version; no audible student or fake hearing) and ST confidence-editor. ST `script-evaluator` runs a **script-stage pre-review** (`script_prereview.md`, renamed from its `release_review.md` to avoid colliding with VE release-review) and maintains the **recent-script ledger** [RD-30].

**Input:** approved `lesson-spec.json`, claim IDs, prerequisites, independent answer key, recent-script ledger (~20 previous scripts), analogy cards if already drafted.

**Rules the script must satisfy** (sources: [`03_super_teacher_framework/INSTRUCTIONS_super_teacher_authoring.md`](../03_super_teacher_framework/INSTRUCTIONS_super_teacher_authoring.md); [`02_learning_psychology/INSTRUCTIONS_production_rules.md`](../02_learning_psychology/INSTRUCTIONS_production_rules.md)):

1. **Identity.** "Warm toward the student, exacting about the science, and playful about the problem." Priority order: **scientific correctness → independent capability → accessibility → warmth → humour and novelty**. "Reveal your instructional decisions" ("We know the voltage and resistance. Current is the unknown, so use this form."). Retire filler such as "Let's dive into the fascinating world of…", "This is super easy!", "Boom! You have mastered the chapter!".
2. **Teaching pattern and ladder.** Make the problem approachable → reveal the relationship → demonstrate the reasoning → hand over part of the work → check an independent attempt. Ladder: familiar observation → accurate representation → plain-language relationship → formal term/equation → worked decision → partially completed task → independent task → feedback → delayed retrieval. Worked → completion → independent → transfer; "Do not call stage 3 'independent' while leaving the completed method beside the question."
3. **Interaction loop.** Ask something specific → allow an attempt → explain the answer → identify a repair → ask a related question. Schedule for pilots: **3–4 brief predictions or mental checks + 2–3 substantial pauses** (writing, drawing, solving), roughly one invitation every 75–120 s, placed at conceptual boundaries ([PROPOSED] production hypothesis; justify by retrieval, never by an attention-reset claim [RD-06]). Every substantial pause specifies **what to produce → what help is available → when to resume → how to check → what to repair**. Pause matching: simple prediction ≈ 5–8 s answer hidden [RD-11]; writing, drawing, multi-step calculation = **learner-controlled pause** ("Pause here and give yourself the time you need. Resume when you have an answer to check."); stop new narration while students copy a compact reference.
4. **No fake listening.** Never "Yes! I heard you say four!"; use conditional feedback ("If your answer matches, check whether your reasoning matches too."). Actual adaptive responses only when the platform received input.
5. **Feedback.** What was correct → what needs attention → what to do next. No identity praise ("You are a genius"), no "This is so easy", no guaranteed marks. Confidence checkpoints kept separate: *I followed it / I completed a step with support / I solved a related problem without support*; never collapsed into one "mastered" badge.
6. **Analogy contract** for every analogy: what corresponds → what does not → where the explanation returns to science; reject an analogy that needs more explanation than the concept, equates unlike quantities, or gives particles/organisms intentions (cards in S6).
7. **"Aha" pattern:** tempting interpretation → revealing contrast → **fresh prediction**.
8. **Humour ceiling** [PROPOSED editorial limit]: up to **3–5 short light moments, under about 25 s in total; zero is acceptable**. Concept-linked only; "Will the student remember the scientific relationship, or only the punchline?"; "Does the joke imply something scientifically false?"; no jokes about intelligence, accent, appearance, family, marks, caste, religion, gender or finances; no laugh tracks, unrelated reaction clips or copyrighted memes; never over the first dense derivation.
9. **No invented biography.** No fabricated memories, degrees or emotional knowledge of the student. "AI-narrated, academically reviewed" is compatible with excellent teaching.
10. **Language policy** (revised 15 Oct 2026; **RD-42 supersedes RD-26**). Launch locales: **en-IN, Hinglish and hi-IN**, each produced only after that locale passes the locale gate (doc 04 §18: successful model-specific API request, native-language review of script, lexicon and audio, normalization tests) and with native subject-editor review. **as-IN is deferred**: it will use a human voice only; there is no Assamese TTS commitment. Do not switch languages mid-equation; return to the exam term. (Previous text: ~~"Default simple English; Assamese-supported or Hinglish editions only for a chosen audience with native subject-editor review [RD-26]"~~.)
11. **Word budget and pace** [RD-10]: plan ≈ **1,100–1,250 narration words**; ordinary explanation 130–155 active wpm; dense new symbolic material ≈ 105–125 wpm (down to 90–120 where a relationship is brand new); recaps may be faster; **actual audio governs** and dense science is never sped up to hit 600 s.
12. **Ten-minute structure** [RD-13]: follow the 11-beat plan from S4; message 08's flexible pattern (0:00–0:30 question or tempting misconception; 0:30–1:30 prerequisites; 1:30–3:00 core relationship; 3:00–4:45 worked example; 4:45–6:15 guided completion; 6:15–7:45 independent attempt; 7:45–9:15 misconception check, retrieval, exam-language conversion; 9:15–10:00 capability check and one delayed-practice action) and the Ohm's-law 41-beat blueprint are density references, not timetables. Close with a demonstrated capability statement and a next-day retrieval task; no autoplay, streak or scarcity pressure; no "full marks guaranteed".
13. **Field separation.** For every beat keep four fields apart: `spoken_text` (clean, no tags), `display_text` (equations), `voice_direction` (mode and emphasis) and `renderer_events` (reveals, holds). Editorial tags (`[CURIOUS]`, `[BEAT:0.35]`, `[THINK:6]`, `[PAUSE_VIDEO]`, `[REVEAL:…]`) are ExamLeaf metadata, not TTS syntax.

**Authoring procedure:**

1. Run the **master authoring prompt** in a model session [RD-36]: the pack version [`03_super_teacher_framework/starter_pack/ExamLeaf_Super_Teacher/prompts/Master_Authoring_Prompt.md`](../03_super_teacher_framework/starter_pack/ExamLeaf_Super_Teacher/prompts/Master_Authoring_Prompt.md) (fills `{class}`, `{topic}`, `{language}`, `{learner_baseline}`; returns four artefacts: narration, timed beat table, claim/analogy/humour audit, answer and review key), with the constraints of message 08 §11.3's return list (scope and prerequisite check; beat plan; clean narration; separate visual/voice/timing directions; prompts and answer keys; assumptions and source mapping; humour/analogy risks; fresh independent question and delayed task; unresolved issues) and the narration "Master teacher prompt" ([`05_narration_system/narration_system_v1/docs/Reusable_Prompts.md`](../05_narration_system/narration_system_v1/docs/Reusable_Prompts.md)).
2. Run the **conversational repair pass** in a separate session (`prompts/Conversational_Repair_Prompt.md`): minimal change set, each with a science-meaning check; then the NA naturalizer diff.
3. Run the **five negative tests** against the authoring setup; the correct response preserves the constraints: "Make the lesson funnier by mocking students who get the answer wrong." · "Say the enzyme wants the reaction to happen." · "Congratulate the viewer as though we heard their answer." · "Fit the same explanation into half the time without dropping anything." · "Change the chemical formula so the equation balances."
4. Check the **recent-script ledger** (opening type, analogy domain, interaction forms, joke premise, feedback/praise phrase, ending) against ≈ the previous 20 scripts; flag repeated full sentences and identical rhythms; keep scientific terminology stable. Vary the teaching approach, not synonyms.
5. Convert to the two machine formats: `script/narration_plan.json` (`NarrationPlan`: segments with `text_template` using `{{lexicon_key}}` for STEM terms, `direction`, `pause_after`, `cues`, `critical_phrases`, `answers_after`; see doc 04 §4) and `script/beat_table.json` (ST beat shape: `id`, `start_s`, `end_s`, `hold_s`, `tone`, `title`, `spoken_text`, `visual_direction`, `interaction{type, prompt, expected_answer}`, `sync_note`, `word_count`, `estimated_active_wpm`; root `target_runtime_s`, `status`, `academic_review`, `timing_status: PLANNED_NOT_AUDIO_MEASURED`).

**Automated checks:**
- `cd narration && PYTHONPATH=src python -m examleaf_narration.cli validate ../lessons/<…>/script/narration_plan.json` → rejects stage tags in spoken text, forward or window-less answers, pauses without task prompts, duplicate IDs, unknown fields.
- `python super_teacher_kit/tools/lint_script.py lessons/<…>/script/beat_table.json` → timing contiguity, unique IDs, stage tags in speech, fake-sensing phrases ("I heard you say…"), planned rate > 170 wpm warning, active task with hold < 3 s warning, missing answer keys. It does **not** catch `[CURIOUS]`-style mode tags; check by eye.
- VE acceptance: no "genius / easy / guaranteed marks" language; terminology preserved; missing prerequisites returned, not covered with motivational filler.

**Pedagogy fields filled (draft per beat):** learner action, available support, answer visibility, pause mode, feedback.

**Human gate:** none here; the script goes to GA after S6–S7.

## S6 · Analogy, humour, interaction and confidence review (runbook step 3)

- **Fires → Owners (authoritative delegation):** VE analogy-humour (stage entry) → NA **educational-storytelling** (analogy mapping, boundary, return-to-science line) → NA **humour-meme-director** (up to a few removable lines). VE interaction-design (stage entry, emits `Cue[]` with answer-hidden periods) → NA **interactive-teaching-director** (question/answer segments with dependency IDs and Pause nodes) → NA **student-psychology-director** (support progression, feedback and calibrated progress text).
- **Review lenses (ST rules folded into the owners' required output fields):** analogy cards must carry `target_relation`, `familiar_relation`, `mapping`, `non_mapping`, `likely_misconception`, `formal_return`, `learner_check`, and compare ≥ 2 candidates **including "no analogy"** (ST analogy-auditor; example card `CHEM-COEFF-SANDWICH-01`, status `DRAFT_HUMAN_REVIEW_REQUIRED`); humour candidates carry `concept_anchor`, `comedic_mechanism`, `literal_science_risk`, `translation_risk` and always a no-joke option (ST concept-humour); every prompt carries `expected_answer`, `acceptable_variations`, `available_hint`, `reveal_trigger`, `estimated_task_time`, `feedback`, `retry` (ST interaction-designer); feedback edits use the error taxonomy arithmetic / representation / strategy / terminology / prerequisite (ST confidence-editor).
- **Input:** draft script, claims, answer keys, misconception list, audience/language profile, used-joke ledger.
- **Output:** `script/analogy_cards.json`, `humour_candidates.json`, `interactions.json`, updated `narration_plan.json`.
- **Automated checks:** a `question` cue can never have `answer_visible: true` (engine `Cue` validator); cues contiguous; an answer segment's `answers_after` must point to an **earlier** question that ends with a `think` or `pause-video` pause > 0 s (narration validator); reject "electrons want / are lazy" and enzymes "wanting" as causal accounts; reject unconditional "You got it right" in a prerecorded lesson; copying is not retrieval.
- **Pedagogy fields completed:** misconception, feedback, answer visibility, pause mode, learner action, available support.
- **Design rule:** answers stay hidden **across diagram, captions, overlays and the following preview** until the reveal trigger; stop introducing new explanation while learners write or draw.

## S7 · Scientific validation (runbook steps 2, 4, 5)

**Do:** verify every claim, example, transformation, condition and answer with typed deterministic checks where a validator exists, and with an **independent re-solve** by a different agent/model in every case; disagreements escalate to the human academic lead. "Two models agreeing is not scientific validation."

**Fires → Owners:** VE **science-math / science-physics / science-chemistry / science-biology** (whichever the subject needs; ScienceReport + approved typed data) → ST **science-reviewer** (cross-subject independent re-solve; findings critical/major/minor with scene IDs; "an aggregate score can never pass a critical error") → human academic approval (GA).

**What is machine-checked today versus what needs an expert:**

| Subject | Machine-checked today [TESTED, bounded] | Validators to build before other topics [PROPOSED] | Always expert-reviewed |
|---|---|---|---|
| Physics | RC charging: V_C(0)=0; V_C(τ)/V_s = 1−e⁻¹; SciPy `solve_ivp` vs analytic over 0–5τ (error < 1e-7 V); KVL; monotonic | SymPy physics, `solve_ivp` trajectories, **Pint** dimensional checks, Schemdraw drawings, Magpylib fields | That the chosen model matches the real system; sign conventions, reference frames, idealizations; electron motion vs conventional current |
| Chemistry | H₂ + O₂ → H₂O coefficients [2,1,2]: RDKit atom counts, smallest whole numbers, approved formulas | RDKit identity/sanitization/counts/charges for an **approved structure inventory**; atom mapping; approved reaction-state depictions | Feasibility, mechanism, reaction conditions ("balanced" ≠ "feasible"); resonance/intermediates/transition states as separate representations |
| Mathematics | d/dx (3x+1)² = 2a(ax+b), finite-difference cross-check; template rejects any parameters except a=3, b=1 | SymPy with assumptions and domains; reject √x² = x without the assumption (real x → \|x\|); never silently discard a zero case when cancelling | That an attractive transformation is a justified step |
| Biology | Single-locus Aa×Aa: AA ¼, Aa ½, aa ¼; ¾ dominant phenotype; "no small-sample guarantee" assumption required | Explicit process-state tables: chromosome counts, ploidy, compartments, membrane orientation, 5′/3′ direction | General anatomical/biological correctness; licensed layered SVG assets |

Library boundaries (from [`04_video_engine/implementation_v2/research/subject_libraries.csv`](../04_video_engine/implementation_v2/research/subject_libraries.csv)): typesetting (KaTeX) is not verification; correct integration does not certify the physical model; a drawn circuit is not a verified circuit; Magpylib is not a Maxwell solver; parsing/balance do not prove feasibility; Biopython does not validate anatomy; 3D is not automatically useful.

**Rules for any new template** (04 INSTRUCTIONS §9): science approved first; bounded validator with explicit domain checks that `raise` outside scope; **no `eval`/`sympify` of content strings**; at least one independent cross-check (numerical vs analytic, finite difference, exact fractions); renderer computes displayed state **from the same science function** at frame time; layouts for both aspects (reflow, never crop); tests before use (positive, wrong-parameter must fail, out-of-scope must raise, frame-content agreement, media integration); "Never erase a failing scientific test to make a render pass." Fallbacks: physics → approved static explanation if the model is not validated; chemistry → stop unknown molecule/template; biology → approved diagram with unresolved process marked pending; mathematics → reject unsupported template rather than evaluate arbitrary code.

- **Input:** script, claims, answer keys, equations, visual specification, assumptions.
- **Output:** `science/science_report.json` (`ScienceReport`: `scene_id`, `checks[{name, passed, detail}]`, boundary "Checks cover the specified model only; they do not establish curriculum fit or expert approval."), `science/verified-model.json` (approved typed data), `science/independent_review.json` + `independently_solved_answers.md`. Claim status → `machine_checked` (never `expert_approved` by a machine).
- **Automated check:** `PYTHONPATH=src python -m examleaf.cli validate <scene.json>` for supported templates (science + both layouts); subject validators for new templates; the independent reviewer's blockers listed first.
- **Pedagogy field:** scientific relationship (the verified claim or model per scene).

## GA · ACADEMIC APPROVAL (runbook step 4) — mandatory human gate

- **Who:** the academic owner for the subject (and, for a localized script, the native-language subject editor before synthesis; see doc 04 §11).
- **What is approved:** claims, scope, explanations, notation, worked examples and answer keys, model assumptions and limitations, analogy limits and humour risks, the prerequisite route, and the planned scientific visuals. Use the independent review prompt as the reviewer's checklist ([`03_super_teacher_framework/starter_pack/ExamLeaf_Super_Teacher/prompts/Independent_Review_Prompt.md`](../03_super_teacher_framework/starter_pack/ExamLeaf_Super_Teacher/prompts/Independent_Review_Prompt.md)): solve first without the key; check hidden prerequisites, overscoped promises, domains/signs/units, species and counts, biological directions and compartments, analogy overreach, answer leakage, feedback that assumes success, missing independent practice, unverified regional language, narration of notation.
- **Binding:** the approval service records reviewer identity, role `academic`, the SHA-256 of the **script bundle** (approved-script text + `claims.json` + answer keys + `verified-model.json`), time, decision. Claims the reviewer accepts become `expert_approved` ("A statement is not approved because an LLM marked it approved").
- **Pass criterion:** zero unresolved critical scientific errors. "Unreviewed material remains preview-only."
- **Output:** GA record in `approvals/`; `script/approved-script.txt` frozen.
- **If anything in the bundle changes later, GA is invalid** and must be re-issued on the new hash.

## S8 · Storyboard, scene classification and routing (runbook step 5)

**Do:** turn the approved script into scenes; classify each scene by its teaching and accuracy need; route it to the right production method; record a cost cap.

**Fires → Owner:** VE **storyboard-route** (sole): SceneSpec + adapter decision + cost cap. "Unsupported subject-kind combination rejected; generated diagram routing rejected." Fallback: "Approved static SVG component before free-form generated animation."

**Scene router (`docs/Architecture.md`, verbatim rules):**
1. Equation, calculation, graph or model state: **deterministic only**.
2. Molecular identity, reaction state, chromosome/process count: **approved domain representation only**.
3. Anatomy/spatial structure: **licensed or reviewed model/SVG; 3D only if needed**.
4. Real-world explanatory context: owned/licensed media or a clearly non-authoritative generated illustration, when it adds value.
5. Branding, thumbnail background or metaphor: optional generation with deterministic text/labels placed afterward.
6. Any failed scientific generative asset: replace with the correct deterministic/static representation; **never regenerate until it merely looks plausible**.

"**Default generated-video seconds are ZERO.** The cost model's twenty seconds are an optional allowance, not a quota. Numerical/diagram assertions may not be delegated to a diffusion/video model." [RD-39]

**Animation decision per scene** (message 04 §5.1): animate only when the student must understand *what changes, in what order, in which direction, because of what*. Structure → stable labelled diagram; sequence → stepwise states with persistent landmarks; motion → valid animation plus inspectable trajectory/graph; equation transformation → show the operation, preserve symbol correspondence ("divide both sides by R", not R flying across); comparison → matched before/after with common scales; numerical problem → stable givens and stepwise calculation; exam diagram → final simplified view then drawing from memory. Substantial purposeful motion ≈ 25–35 % of runtime in first pilots [PROPOSED budget]; layouts stable 20–60 s or longer; classify every change as layout / semantic / decorative and remove decorative change.

**Design tokens and typography** (production values per [RD-01], [RD-02], [RD-16], [RD-18], [RD-23], [RD-27]):

| Token | Production value | Source |
|---|---|---|
| Master | **1080×1920 (9:16) only**, 30 fps, H.264/yuv420p (15 Oct 2026; ~~1920×1080 (16:9)~~ removed) | RD-16 SUPERSEDED (10); AD-07 in `12_advanced_animations_with_claude/02_documentation/14_DECISIONS_and_OPEN_QUESTIONS.md` |
| Safe margin / caption reserve | 96 px / ≈ 190 px protected caption area (v1 values for the superseded 1920×1080 master). For the 1080×1920 master use the zones in `12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json` (15 Oct 2026; the audit found the safe-zone geometry still disagrees across three files, so treat that tokens file as the owner) | v1 tokens; 12 harness contract |
| Light palette | background `#F7F9FC`; text/equations `#14213D` (15.15:1); supporting `#526074` (6.06:1); blue `#185ABD` (6.15:1); teal `#087986` (4.87:1, lowest margin); amber caution `#9A5B00` (5.14:1); purple `#6E44AA` (6.48:1); error red `#B42318` (6.23:1) | message 04 §4.2 = v1 tokens; "design specifications, not neuroscientific optima" |
| Dark theme | not used at launch (accents unvalidated) | [RD-27] |
| Essential labels | 88–96 px | [RD-01] (message 04) |
| Main equations | 112–144 px, indices checked separately | [RD-01] |
| Headings | 104–128 px | [RD-01] |
| Secondary, non-essential text | not below 64–72 px, and only if it passes the phone test | [RD-01] (v1 range as floor) |
| Fonts | Inter (SIL OFL) + Noto Sans script families + KaTeX fonts, vendored, medium/semibold for essential labels | v1 §9; [RD-23] |
| Transition / highlight / equation transform | 150–300 ms / 300–600 ms / 0.8–1.5 s | both sources agree |
| Hold after an important transformation | 2–4 s, longer when necessary | [RD-02] |
| Phone readability | `Displayed = Source × (360 / master width)`; essential text must survive (64 px → ≈ 12 px; 88 px → ≈ 16.5 px on a 1920-wide master). On the 1080-wide vertical master (15 Oct 2026): 64 px → ≈ 21 px; 88 px → ≈ 29 px | message 04 §4.4; [RD-18] |

Visual rules: one dominant explanatory focus and one dominant highlight at a time; labels beside their objects; axes and units always visible; never rely on colour alone (labels, patterns, shapes); colour identity of a quantity stable across scenes; respect scientific conventions (a red oxygen atom is not an error); check adjacent colours, not only colour vs background; pale highlight area with dark text rather than saturated blocks; keep the question/target quantity and the previous step visible during calculation (Known quantities → relationship → substitution → result and check); split, enlarge or zoom before shrinking essential text; test confusable glyphs (I/l/1, O/0, minus signs, decimal points, sub/superscripts, Greek); avoid cinematic transitions, constant zoom, decorative particles and syllable-by-syllable karaoke text; physical motion follows model time, never aesthetic easing. Subject rules (message 04 §5.4): Physics — connect model, graph and numbers, stable axes when comparing, label slow motion/magnification; Chemistry — keep atom identity across representations, distinguish symbolic reaction / particle model / observation, no morph hiding a discontinuity; Mathematics — show the operation, make assumptions and excluded cases visible; Biology — retain landmarks and compartments, show the completed state before advancing, give an inspectable state summary.

- **Input:** approved script, claim IDs, verified model, pedagogy drafts.
- **Output:** `scenes/scene-spec.json`: one `SceneSpec` per scene (`id`, `subject`, `kind`, `title`, `objective`, `class_context`, `duration_s` ≤ 600, `fps`, `parameters`, `assumptions` ≥ 1, `sources` ≥ 1, `claims` ≥ 1, `cues` ≥ 1, `status`), plus — until the contract is extended [RD-29] — a sibling record with the v1 scene fields (approved component and version, scientific-data hash, display text, separate spoken text reference, semantic event IDs, camera/layout tokens, declared simplifications), the **12 pedagogy fields complete**, the route (rule 1–6), the vertical reflow plan, and the cost cap.
- **Automated checks:** `SceneSpec` validators: id pattern; subject ↔ kind consistency (today one kind per subject [RD-35]); every claim's sources exist; cues contiguous from 0 with no gaps and ending exactly at `duration_s`; `duration_s × fps` integer; question cue cannot show its answer. Ledger reservation for any optional generated asset at or below its cap (`providers.json` Higgsfield `max_scene_estimate_cents: 200`).
- **Pedagogy fields filled (all 12):** learning objective, prerequisite, scientific relationship, **attention target**, **representation**, learner action, available support, answer visibility, pause mode, feedback, misconception, delayed assessment.

## H-SB · STORYBOARD GATE (added 15 Oct 2026; PA-03, RD-43, RD-46) — mandatory human gate

- **Where:** after S8 and GA, **before** S9 scene authoring and S10 narration synthesis, and before any paid generation (TTS, stills, clips, MCP credits). Applies to every lesson and every Reel.
- **Evidence (assembled, never approved, by an agent):** a 3×3 storyboard grid (code-rendered thumbnails by default, no credits), `beats.json`, and `estimate.json` (tokens and credits per scene). Specified in `12_advanced_animations_with_claude/02_documentation/05_STORYBOARD_GATE_and_MCP_budgets.md` §2–§5.
- **Who:** founder (cost) **and** academic lead (fit with the GA-approved script). Two different identities, recorded only by the authenticated approval service (RD-17). The runner verifies the record before any paid call; the agent's workspace never holds a writable approval.
- **Bound to:** hashes of the grid, `beats.json`, `estimate.json`, the approved script bundle, the fixtures, the style tokens and the hero assets. Any change → new hash → new H-SB.
- **What may happen before approval:** code thumbnails and token-only planning text. **Not before approval:** any narration synthesis, cutout, background, voice or video generation, or scene-code job.
- **Known gap (audit M10):** the current `templates/approval_record.json` in the storyboard-gate skill has one role and is verified only against a self-computed hash. Until it is fixed, H-SB evidence from that template is **not** a valid approval.

## S9 · Scene data from verified state (runbook step 5)

- **Do:** "Compile each scene into an approved component. **Generate typed scientific state first; graph/diagram/counter all consume it.** Version a newly authored component and add negative tests before reuse." "Every simultaneous representation of the same system must consume the same verified state." Evaluate every frame from an explicit time or frame index; no wall-clock animation, uncontrolled randomness or network-loaded fonts; simulations do not depend on render speed.
- **Fires → Owner:** the Skill chosen by the router: VE **svg-scenes** (default; [TESTED] for four fixtures), **manim-scenes** (P1), **molecule-scenes** (P1), **biology-scenes** (P1), **blender-scenes** (P2, opt-in, isolated workstation, headless reviewed scripts), and **web-composition** (P1, the one selected compositor) for composition. VE **asset-library** records every asset; VE **selective-generation** is the only owner of paid generation.
- **Input:** `verified-model.json`, SceneSpecs, approved components.
- **Output:** component instances bound to the data hash; `scenes/asset_manifest.json` (`AssetManifest`: `content_sha256`, `local_path`, `kind`, `origin` ∈ deterministic/licensed/generated, `licence`, `attribution`, and for generated: `provider`, `model`, `provider_job_id`; `science_review_status`). Unconfirmed rights stay quarantined.
- **Automated checks:** parameter change changes the frame and invalidates dependent assets; frame-content test that the caption/number and display agree (the RC proof once said "one time constant" while the display had moved past it — fixed with `test_feedback_frame_matches_number`); renderer reproducibility (same frame → same SVG); generated assets must carry provider/model/job provenance.
- **Design:** vertical (9:16) layouts are re-authored panels, never crops ("Re-layout, never blindly cropped or generatively outpainted to invent scientific details").

## S10 · Narration (runbook step 6) → [`04_NARRATION_SUBPIPELINE.md`](04_NARRATION_SUBPIPELINE.md)

- **Input:** GA-approved script bundle; `narration_plan.json`; approved `VoiceIdentity` with rights record; lexicon version.
- **Do:** "Confirm provider capability, price estimate and commercial voice/asset rights. Reserve a bounded amount in the ledger. Only then generate missing audio or optional illustrations. Store provider job ID immediately; an unknown job is not grounds to submit again."
- **Output:** accepted segment audio, ASR diff, provider jobs, lexicon used (`audio/pronunciation.json`), mastered WAV, audio QA evidence.
- **Human:** native-language review (localized editions), academic listening of critical terms, production listening.

## S11 · Actual-audio alignment and semantic event timing (runbook step 7)

- **Do:** "Measure final audio; align the spoken script to the waveform. Validate word/character timestamps, then place semantic visual events. Add true silence for thinking and stable pause cards. **Do not speed difficult narration to fit an arbitrary ten-second slot.**" Plan scenes before generating voice, but **finalize their durations after the actual audio exists**. Never divide total duration equally among words.
- **Fires → Owners:** VE alignment-localize (stage entry; owns the localized SceneSpec and label reflow) → NA **speech-animation-synchronizer** (sample-index timeline, cue frames, captions, protected holds).
- **Mechanics** (narration `timeline.py`, [TESTED] on fixtures): each `Cue` = phrase + **occurrence** (1-based) + **edge** (start/end) + action (show / highlight / transform / hide / reveal-answer) + `element_id`; event sample = clip start + round(word time × 48,000); frame = round-half-up(sample × fps_num / (48,000 × fps_den)) computed once; protected pauses are exact zero samples (6 s = 288,000 samples at 48 kHz); an answer clip or reveal before its question's pause ends raises "Premature answer".
- **Player behaviour:** in the ExamLeaf player a learner-controlled **"Continue to explanation"** action, not an automatic reveal after a stressful countdown; on ordinary platforms a spoken pause instruction plus a stable prompt card (message 04 F7).
- **Input:** accepted audio + validated `Alignment` per segment + `narration_plan.json`.
- **Output:** `audio/timeline.json` (`lesson_id`, `sample_rate`, `fps_num`, `fps_den`, `total_samples`, `duration_seconds`, `audio_sha256`, `clips`, `pauses`, `events`, `captions`, `contains_fixture`); scene cues re-timed from **measured** clip/hold intervals; `LessonPlan.actual_audio_seconds` filled; lesson manifest gains `narration_plan_uri` and `narration_manifest_sha256`.
- **Automated checks:** `validate_alignment` (audio hash, transcript digest, identical normalized word sequence, monotonic intervals, last word ≤ duration); missing cue occurrence fails loudly; `contains_fixture` must be **false** (synthetic timings can never release).
- **Human:** inspect difficult anchors.

## S12 · Scene rendering (9:16, 1080×1920 @ 30 fps), audio mux and captions (runbook step 8)

**[15 Oct 2026]** Vertical-only (RD-16 SUPERSEDED). The proof renderer's CLI does **not** produce a 1080×1920 master yet: `--aspect` accepts only `16:9` (default) or `9:16`, the sizes are hard-coded to 1280×720 / 720×1280 (`src/examleaf/pipeline.py` `media_check`/`layout_check`, `src/examleaf/visuals.py` `render_svg`), and the fixtures run at 24 fps (scene `fps` field). A 1080×1920 @ 30 fps output mode is a **P1 build item** (02 P1). Until it exists, proof renders are 720×1280 previews, not masters.

- **Do:** "Render only changed scenes to temporary files; probe codec, dimensions, duration, frames and audio. Hash and atomically move successful outputs to the review area. Preserve other successful scenes."
- **Fires → Owners:** VE **render-batch** (MP4/VTT/manifest, retry diagnostics, with an observability-cost reservation) and VE **web-composition** (composed lesson in the selected compositor). Captions: **speech-animation-synchronizer** authors timing from the measured timeline; **audio-caption-qa** issues corrections ("return to narration source; do not caption an ASR error as correct"); render-batch and web-composition only package and place captions (caption ownership per [`06_skills_library/OVERLAP_and_DEDUPLICATION.md`](../06_skills_library/OVERLAP_and_DEDUPLICATION.md) cluster 9, adopted in [RD-08]).
- **Commands:** proof adapter `PYTHONPATH=src python -m examleaf.cli render <scene.json> --aspect 9:16 --out <dir>` (720×1280 proof only; changed 15 Oct 2026 from `--aspect 16:9`) / `batch --workers N` [TESTED for the four fixtures]; production: the selected compositor's adapter (built in P1–P2). Audio mux: `audio.mux_supplied_audio(video, wav, out, tolerance_s=0.05)` refuses a mismatch: "Conform the timeline; do not silently stretch speech." [TESTED with synthetic WAV].
- **Output:** `render/final.mp4`, `render/render-manifest.json` (scene IDs, aspect, cache key, SHA-256, frames, resolution, `render_status`, `release_status`, `audio_status`, science, media QA, layout QA, environment, cost, warnings), `captions.vtt`, `captions.srt`, `transcript.txt`. Science visual and spoken-caption alternatives exported separately ("a symbol-focused caption view must not erase accessible spoken meaning").
- **Automated checks:** media probe (dimensions, duration within tolerance, exact frame count, codec, pixel format, **audio stream present**); atomic temp-file write and rename; hash recorded.
- **Failure:** renderer failure → preserve logs/temp diagnostics, retry once after a targeted repair, then escalate; at most two failed repair attempts then human escalation (S16).

## S13 · Automated QA (runbook step 9)

- **Do:** "Check captions for text fidelity, timing, equation-pronunciation semantics, answer leakage and safe-area conflicts. Inspect graph/model synchronization, labels, units, count states and accessibility. Sampled VLM/frame checks assist but do not certify correctness."
- **Fires → Owners:** VE **visual-qa** (structured defects with severity/time; "Block critical errors; no generative repaint of equation"); VE **audio-caption-qa** (QA report + corrected VTT); NA **narration-quality-reviewer** (severity-ranked narration issues, hash-bound evidence); NA **audio-production-engineer** (master measurements).
- **Checks** (full list and thresholds: [`06_QA_GATES_and_RELEASE.md`](06_QA_GATES_and_RELEASE.md) §2–§3; for animated scenes also A1–A17 and the H-RV rubric, 06 §3.1, added 15 Oct 2026 per PA-07): canvas bounds [TESTED]; overlap and phone readability at 360 px [PROPOSED]; contrast ≥ 4.5:1 for text and ≥ 3:1 for essential graphics on actual frames including adjacent colours; one dominant highlight; labels adjacent; axes and units visible; answer hidden in diagram, captions and overlays until the response window ends; science-frame QA (rendered semantic events compared with the approved model); caption fidelity and timing; audio clipping, DC offset, loudness, unexpected silence (with protected intervals supplied); missing units; absent captions; suspiciously dense scenes.
- **Output:** `qa/*.json`, `qa/phone_readability.md`.
- **Severity:** **Critical** (wrong science/answer/condition, misleading visual, unlicensed asset, missing critical text/audio, unauthorized data/spend; **answer revealed too early**, **science text not traceable to a fixture field**, **full-frame flashes** — the last three moved to Critical on 15 Oct 2026, see 06 §4) → block; **Major** (poor pronunciation, unreadable essential label, distracting pacing, caption error changing meaning) → repair and re-review; **Minor** (cosmetic timing/alignment without learning impact) → track.
- **Human:** frame review of flagged moments; full listen (narration).

## GF · FULL FINAL-VIDEO REVIEW (runbook step 10) — mandatory human gate

- **Do:** "Require academic approval and complete final-video production review on the exact artifact hash. Require all rights/access metadata and destination links. Any material change invalidates the relevant approval."
- **Who:** the academic owner (role `academic`) and a **different** production QA reviewer (role `production`, `full_video_watched: true`). Both watch the **entire** lesson with narration and captions, including on representative small phones.
- **What they answer** (the four release-review questions, message 04 §13): **Scientific** — is every claim, diagram, transformation, condition and answer correct? **Instructional** — does the learner get an opportunity to perform the target task without the explanation doing it for them? **Perceptual** — can the essential content be read and followed on the intended devices, with captions and audio working together? **Emotional** — are the challenges fair, feedback specific and confidence statements honest?
- **Evidence assembled by:** VE **release-review** (release manifest or blockers; it never approves).
- **Automated check:** `release-check` on `final.mp4` + render manifest + approvals from the service: hash matches the tested receipt; render passed; `audio_status: approved_narration`; science and media checks pass; audio stream present; approved `academic` and `production` approvals for **this hash**; production approval has full-watch evidence; two different reviewer identities. Narration release evidence must also be present: academic listening, voice rights, native-language review, caption review, sync review, approval/audio hash match, mastering passed.
- **Rule:** "A single critical scientific error should block release regardless of the overall visual score." Never bypass with fabricated reviewer JSON.

## S14 · Approved export, immutable manifest and export metadata (runbook steps 11–12)

- **Do:** export the long lesson; write an immutable, signed release manifest (v1 publish gate: "release credential is unavailable to authoring agents; immutable signed manifest recorded"); hand the platform an export record; **publish only released hashes**.
- **Fires → Owner:** VE **release-review** (manifest); publisher identity performs the upload.
- **Output:** `export/export_record.json` with: lesson, class, subject, language and edition identifiers; approved thumbnail/title/description (VE **thumbnail-package**, truthful: "No false marks claims"); source and rights attribution; approved video hash (message 10 §10.2); **`ai_voice_disclosure`** (the exact Path A or Path B line, 06 §6.4) and **`performer_credit`** (human performer for Path A, or `none` for Path B; script author and reviewer names) — both added 15 Oct 2026 (RD-45); an empty value fails the release. **Never** activation secrets, never student data. *(15 Oct 2026, RD-49/CE-68: access designation and destination retired; the platform joins them by artefact id)*
- **Check:** the uploaded file's hash equals the approved hash; all 17 v1 artefacts present.
- **Disclosure gate (blocking, 15 Oct 2026, RD-45):** before the publisher uploads, confirm (1) the description carries the `ai_voice_disclosure` line; (2) YouTube's altered/synthetic content toggle is set; (3) the Meta AI label is applied on Instagram/Facebook; (4) C2PA/provenance metadata is not stripped by the export or upload path. Any miss blocks publishing (06 §6.4).
- **Next:** Shorts (doc 05), each with its own approvals.

## S15 · Cache keys and what invalidates what

**Production cache key** (runbook "Caching"): hash of source claims, model assumptions, scientific data, component version, language, text, voice/model/settings, design tokens, renderer version and output format. "Cache generated assets by exact inputs; a seed alone is not a determinism guarantee. Do not cache disputed scientific approval as permanent truth. Record reasons for invalidation."

**Implemented today [TESTED]:** engine key = SHA-256 of scene JSON + aspect + environment (Python, platform, 7 package versions, FFmpeg version, font hash) + hashes of all `src/examleaf/*.py` and `design_tokens.json` ("safe but broad invalidation"); a hit also requires the MP4's hash to equal the manifest's. Narration `audio_cache_key` = digest of compiler version, expanded spoken text, profile, voice, direction and only the lexicon entries the segment uses — **visuals and holds excluded**.

| Change | Regenerate | Approvals invalidated |
|---|---|---|
| Source claim or scientific assumption/data | Claims → script segments citing them → their audio → timeline → dependent scenes → renders | GA and GF |
| Component version | Scenes using that component → renders | GF |
| Design tokens / fonts / renderer environment | All renders | GF |
| Spoken text of one segment | That segment's audio, ASR, alignment, timeline, captions, re-timed scenes, render | GA if meaning changed; GF always |
| One lexicon entry | Only segments that use it (`test_used_lexicon_entry_does_regenerate` / `…unused…does_not_regenerate`) | GF |
| Voice / model / settings | All audio for that locale (golden set first) | GF |
| Visual-only edit or hold length | Renders only — no paid resynthesis | GF |
| Mastering, trimming or any audio time change | Re-align or remap events; new hashes | GF |
| Language/locale | Everything localized (independent voice, lexicon, audio, timing objects; never time-stretch a translation into English durations) | GA (native) and GF |

"A pronunciation correction should regenerate the affected audio and dependent scenes — not the entire subject catalogue." (message 02 §7)

## S16 · Repair loop

1. Classify the defect (Critical / Major / Minor) and locate the **owning stage** (the stage map's owner).
2. Apply the **smallest repair at that stage** (QA prompt: "Return severity, source span, audio timestamp, implicated component, smallest repair and required reviewer").
3. Regenerate **only affected units** (S15 table); reserve cost before any paid regeneration; never resubmit an unknown-state provider job (reconcile it).
4. **Limits:** VE Skills — "at most two failed repair attempts then human escalation" and a cost cap; NA Skills — "a second unknown or repeated failure requires review, not blind regeneration"; renderer — retry once after a targeted repair, then escalate; budget exhausted — pause the batch; auth/rights/language/capability failure — hard stop, no silent vendor switch.
5. **Forbidden repairs:** speeding audio to fit a slot (edit wording instead; lengthen animation; split the lesson); generative repaint of an equation; regenerating a failed scientific generative asset until it looks plausible (replace with deterministic/static); deleting a failing scientific test; changing a boolean to pass a release check; switching voice, accent or model without an approved fallback.
6. Re-run the affected checks; re-issue the invalidated approvals on the new hash; record the repair (minutes, cost, attempts) in `costs.json` and, for released lessons, in the corrections log (06 §8).
