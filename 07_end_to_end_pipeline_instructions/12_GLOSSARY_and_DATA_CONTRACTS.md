# 12 · Glossary and data contracts

**Part 1** defines the terms used across the pipeline. **Part 2** lists the data contracts field by field, read directly from the code (`04_video_engine/implementation_v2/src/examleaf/contracts.py`, `interfaces.py`, `pipeline.py`, `budget.py`; `05_narration_system/narration_system_v1/src/examleaf_narration/contracts.py`, `timeline.py`, `compiler.py`, `qa.py`; the JSON schemas in `04_video_engine/implementation_v2/schemas/` and `05_narration_system/narration_system_v1/configs/narration.schema.json`), with the stage that writes and the stages that read each. Proposed records that are not yet code are marked [PROPOSED].

---

# Part 1 · Glossary

> **Aside: coefficient vs subscript (the worked example used throughout the sources).** In `2H₂O` the **coefficient** `2` counts complete molecules: two water molecules, so 4 H atoms and 2 O atoms. The **subscript** `₂` in `H₂O` is part of the substance's identity: changing it changes the substance (H₂O → H₂O₂ is hydrogen peroxide). Balancing changes coefficients only; changing a formula to make counts match is "a very efficient way to answer a different question". Analogy card `CHEM-COEFF-SANDWICH-01`: number of sandwiches ↔ coefficient; ingredients per sandwich ↔ atoms per molecular copy; limit: "Molecules are not sandwiches … does not establish reaction conditions or feasibility."

| Term | Meaning in this pipeline |
|---|---|
| **Academic approval (GA / academic role at GF)** | Human approval of claims, scope, explanations, notation, worked examples, answer keys, model assumptions and scientific visuals; bound to an artefact hash. |
| **Access tier** | `free` / `book_entitlement` / `preview` designation exported with a lesson or Short; enforced by the platform, never by the video. |
| **Activation secret** | A random code (e.g. 128-bit, readable base32) under a scratch panel that grants an entitlement; only its hash is stored; never in videos, QR artwork or export metadata. Distinct from the **public QR**, which is navigation only. |
| **Alignment / forced alignment** | Placing the supplied transcript's words in the accepted audio ("Where does the supplied text fit in this audio?"). Not a pronunciation check. |
| **`answers_after`** | Narration segment field naming the earlier question segment it answers; enforces a protected response window before any reveal. |
| **Approval** | A record of role, reviewer identity, artefact SHA-256, decision, time and (production) full-watch evidence. Locally a pydantic model (policy demo); in production issued only by the authenticated approval service. |
| **ASR (independent)** | Separate speech recognition used to ask "What does another system think was spoken?"; run audio-only, never biased with the expected text. |
| **AssetManifest** | Record of every media/data asset: content hash, origin (deterministic / licensed / generated), licence, attribution, and for generated assets the provider, model and job ID. |
| **`audio_cache_key`** | Narration cache key: compiler version + expanded spoken text + profile + voice + direction + only the lexicon entries the segment uses. Excludes visuals and holds. |
| **Blueprint-only plan** | A `*_600s_plan.json` beat plan with no script, audio or approval (`status: blueprint_only`). |
| **Budget ledger** | SQLite table of cost reservations in integer cents with idempotency keys; refuses overspend; records overruns honestly then blocks. |
| **Cache key (render)** | Hash of the scene, aspect, environment and implementation; production version adds claims, assumptions, data, component version, language, text, voice/model settings, tokens, renderer version, output format. |
| **CAC (incremental / fully loaded)** | Customer acquisition cost. Incremental = paid/referral acquisition per customer (Base ₹120; max DTC ₹118 at the target contribution); fully loaded marketing CAC adds organic creative work (₹186.67 Base 5,000). |
| **Claim** | A source-linked scientific statement with assumptions and status `draft` → `machine_checked` → `expert_approved` (only a human makes it expert-approved). |
| **Claim ledger** | The set of claims for a lesson (`claims.json`), each traceable to `SourceRef`s; owned by `claim-research`. |
| **Compositor** | The engine that assembles scenes, audio and captions into the lesson (HyperFrames candidate, Remotion alternative; native SVG proof as reference). |
| **Confidence calibration** | Whether a learner's confidence matches correctness: accurate confidence, high-confidence errors, correct-but-uncertain. A variant that raises confidence while increasing errors loses. |
| **Contribution (per book)** | Realized revenue minus variable costs per retained book (Base 5,000: ₹118.13); not profit. |
| **Cue (engine)** | Timed caption-level unit with role (explain/question/feedback/recap), voice mode and `answer_visible` (never true on a question). |
| **Cue (narration)** | Semantic animation anchor: phrase + occurrence + edge → action on an element at a sample-exact time. |
| **Delayed unprompted assessment** | The primary learning outcome: unfamiliar but curriculum-aligned items after a delay (initially 7 days). |
| **Deterministic vs domain-validated vs reviewed** | Routing classes: equations/graphs/calculations are deterministic; atom identity/charge/reaction state use approved domain representations; anatomy uses reviewed SVG or licensed models; generated media only for context or branding. |
| **Display text vs spoken text** | The equation as shown (`I = neAv_d`) vs how it is read aloud; kept in separate fields. |
| **Entitlement** | The platform's grant of access to a subject + edition (12 months from activation in the proposed terms), created by atomic redemption or direct purchase. |
| **Export record** | What the engine hands the platform: IDs, access designation, destination, approved title/thumbnail/description, attribution, approved video hash. |
| **Fail closed / PendingAdapter** | Unimplemented remote adapters raise errors rather than pretending to work. |
| **GA / GF / GS** | Runbook gate names: academic approval; full final-video review; Short approval. |
| **Golden fixtures / golden set** | Golden fixtures: the four engine science scenes used to test renderers/compositors. Golden set: difficult narration passages with accepted audio, re-run before any model/voice/provider upgrade. |
| **Hash-bound approval** | An approval valid only for the exact artefact SHA-256 it names; any material change invalidates it. |
| **Interaction loop** | Ask something specific → allow an attempt → explain the answer → identify a repair → ask a related question. |
| **Learner-controlled pause** | `pause-video`: the learner decides when to resume (writing, drawing, multi-step work); in the ExamLeaf player a "Continue to explanation" action. |
| **LessonPlan / LessonSpec** | v2 implemented lesson record (board, year, subject, class, language, objective, prerequisites, sources, claims, target seconds, review states) / v1 proposed superset adding worked problems, retrieval questions, expected answers, exam terminology, narration. |
| **Lexicon / `{{token}}`** | Versioned pronunciation dictionary; STEM terms in scripts are written as explicit `{{identifier}}` tokens that expand to display, spoken and caption forms. |
| **LUFS / dBTP** | Integrated loudness / true peak. Target ≈ −16 LUFS (±1), ≤ −1 dBTP. |
| **NarrationPlan** | The structured narration record: voice identity, lexicon version, ordered segments with spoken text, direction, pauses, cues, critical phrases, answer dependencies. |
| **Occurrence index** | The 1-based count telling which instance of a repeated phrase a cue anchors to. |
| **Performance reference vs identity reference** | A recording demonstrating rhythm and intention vs one used to create or condition a synthetic voice resembling the speaker (needs specific permission and provider verification). |
| **Protected pause** | Exact zero samples inserted for thinking/writing (6 s = 288,000 samples at 48 kHz), never synthesized, never removed by silence trimming. |
| **ProviderJob** | Record of a paid provider operation: idempotency key, provider, model, provider job ID, state, estimated/actual cents, input hash. Unknown state → reconcile, never resubmit. |
| **Qualified visit** | A visit by a relevant learner (right class/board/topic) arriving from content, as opposed to plays or raw reach. |
| **Recent-script ledger** | Per-script record of opening type, analogy domain, interaction forms, joke premise, feedback phrase and ending; checked against ≈ 20 previous scripts. |
| **Release-check** | Local fail-closed policy commands (engine exits 1 when blocked; narration always exits 2); in production a release service makes the decision from authenticated approvals. |
| **Retained sale** | A book sale net of refunds and returns (orders, customers, activations and printed copies are different metrics). |
| **Reflow vs crop** | Re-authoring a layout for 9:16 from the same data vs cutting a region out of 16:9; crop is rejected because it can remove axes or conditions. |
| **Scene pedagogy record** | The 12 fields stored per scene: learning objective, prerequisite, scientific relationship, attention target, representation, learner action, available support, answer visibility, pause mode, feedback, misconception, delayed assessment. |
| **Scene router** | The six routing rules deciding deterministic / domain / reviewed / licensed / generated production per scene. |
| **SceneSpec** | Engine scene record: scientific parameters, assumptions, sources, claims, cues, duration, subject, renderer kind, status. |
| **ScienceReport** | Named pass/fail checks for a scene; passes only if all pass; carries the boundary statement that checks cover only the specified model. |
| **Semantic event** | A visual change tied to meaning (show, highlight, transform, hide, reveal-answer) timed from measured speech. |
| **Sell-through** | Share of printed/shipped copies actually sold to end customers (planned 90%, stressed 75%). |
| **ShortSpec** | Record of a vertical Short: source lesson and claims, 20–60 s, hook, complete payoff, retained conditions, destination, access tier, reflow, approval status. |
| **Skill / MCP / CLI / API / SDK / platform / plugin** | Instructions an agent loads / protocol exposing tools / executable / service contract / client library / hosted product / bundle that may include all of these. None supplies scientific verification. |
| **Strong foundation / context-dependent / production hypothesis** | Message 04's evidence labels for design decisions; numeric specs are production hypotheses to test. |
| **Technical preview** | A silent, unapproved proof render (`release_status: blocked_pending_audio_and_expert_review`). |
| **Timeline** | Narration output: sample rate, fps, total samples, audio hash, clips, pauses, events (sample + frame), captions, `contains_fixture`. |
| **WER** | Word error rate of ASR vs the canonical text; zero WER does not prove correct pronunciation. |

---

# Part 2 · Data contracts

Conventions: engine models use `extra='forbid'`, no NaN/inf; narration models use `extra="forbid"`, `validate_assignment=True`. "W" = stage that writes; "R" = stages that read (stage IDs from [`03_PER_LESSON_PRODUCTION_PROCEDURE.md`](03_PER_LESSON_PRODUCTION_PROCEDURE.md); N-steps from [`04_NARRATION_SUBPIPELINE.md`](04_NARRATION_SUBPIPELINE.md); SH from [`05_SHORTS_and_REELS_PROCEDURE.md`](05_SHORTS_and_REELS_PROCEDURE.md)).

## 3. Engine contracts [TESTED as schemas]

### 3.1 `SourceRef` (`contracts.py`) — W: S1 · R: S3, S4, S14
| Field | Type / rule |
|---|---|
| `id` | str, ≥ 3 chars |
| `uri` | str (data, never fetched) |
| `locator` | str (page/section) |
| `rights_status` | `owned` · `permission` · `open_reference` · `unconfirmed` |
| `claim_scope` | str |
| `retrieved_at` | str (date) |
| *(production extension, [PROPOSED])* | stored source hash, academic-year version, exact extracted coordinates |

### 3.2 `Claim` — W: S3 (status updated S7, GA) · R: S4–S9, S14, SH
| Field | Type / rule |
|---|---|
| `id` | str |
| `statement` | str |
| `source_ids` | list[str], ≥ 1; each must exist in the containing record's `sources` |
| `assumptions` | list[str] |
| `status` | `draft` (default) · `machine_checked` · `expert_approved` |

### 3.3 `Cue` (engine) — W: S6/S8 (planned), S11 (measured) · R: S12, S13
| Field | Type / rule |
|---|---|
| `start_s` | float ≥ 0 |
| `end_s` | float > 0, > `start_s` |
| `text` | str (single field today; display/spoken split → [RD-29]) |
| `role` | `explain` (default) · `question` · `feedback` · `recap` |
| `voice` | `steady` (default) · `curious` · `deliberate` · `light` · `reassuring` (`focused` to be added, [RD-12]) |
| `answer_visible` | bool, default false; **must be false when `role = question`** |

### 3.4 `SceneSpec` (`schemas/scene.schema.json`) — W: S8–S9 · R: S11, S12, S13
| Field | Type / rule |
|---|---|
| `schema_version` | `"1.0"` |
| `id` | `^[a-z][a-z0-9_-]{2,70}$` |
| `subject` | `physics` · `chemistry` · `mathematics` · `biology` |
| `kind` | `rc_charge` · `atom_balance` · `chain_rule` · `mendel_cross`; subject ↔ kind fixed 1:1 today ([RD-35]) |
| `title`, `objective`, `class_context` | str |
| `duration_s` | 0 < x ≤ 600; `duration_s × fps` must be a whole number |
| `fps` | 1–60, default 24 (production 30, [RD-16]) |
| `parameters` | dict of number / str / list[int] |
| `assumptions` | list[str], ≥ 1 |
| `sources` | list[`SourceRef`], ≥ 1 |
| `claims` | list[`Claim`], ≥ 1; every source ID resolvable |
| `cues` | list[`Cue`], ≥ 1; contiguous from 0, no gaps, last `end_s` = `duration_s` |
| `status` | `technical_preview` (default) · `review_pending` · `approved` |

### 3.5 `Check` and `ScienceReport` — W: S7, S9 · R: GA, S12 manifest, GF
| Field | Type / rule |
|---|---|
| `Check.name`, `Check.passed`, `Check.detail` | str, bool, str |
| `ScienceReport.scene_id` | str |
| `ScienceReport.checks` | list[`Check`]; `passed` = non-empty and all pass |
| `ScienceReport.boundary` | "Checks cover the specified model only; they do not establish curriculum fit or expert approval." |

### 3.6 `Approval` (no schema file) — W: GA, GF, GS (approval service only) · R: `release-check`, S14
| Field | Type / rule |
|---|---|
| `role` | `academic` · `production` |
| `reviewer_id` | str, ≥ 3 (authenticated identity in production) |
| `artifact_sha256` | 64 lowercase hex |
| `approved` | bool |
| `reviewed_at` | str |
| `full_video_watched` | bool, default false (required true for production approval) |

*(15 Oct 2026, level-1, CE-113 / P1-16)* In Content Engine v2 an approval record also carries `signature` (SSH signature, namespace `examleaf-approval`, over JCS(record minus signature)), checked by RELEASE-CHECK with `ssh-keygen -Y verify` against the reviewer's `signing_keys[]` entry valid at the record's timestamp; an unsigned or mis-signed row counts as absent, and agent identities hold no reviewer role (`15_content_engine_v2/ARCHITECTURE_content_engine_v2.md` §3.2, §3.7).

### 3.7 `LessonPlan` (`interfaces.py`; `schemas/LessonPlan.schema.json`) — W: S4 · R: S5–S14
| Field | Type / rule |
|---|---|
| `schema_version` | `"1.0"` |
| `id`, `board`, `academic_year` | str |
| `subject` | as SceneSpec |
| `class_level` | int 10–12 |
| `language`, `objective` | str |
| `prerequisites` | list[str] |
| `sources` | list[`SourceRef`], ≥ 1 |
| `claims` | list[`Claim`], ≥ 1; unresolved source → error |
| `target_seconds` | int, default 600, ≤ 1200 |
| `source_review_status`, `syllabus_review_status` | `pending` · `approved` |
| `actual_audio_seconds` | float or null (filled at S11) |

### 3.8 `AssetManifest` — W: S9, S10, S12, SH · R: S13, S14, licence ledger
| Field | Type / rule |
|---|---|
| `id` | str |
| `content_sha256` | 64 hex |
| `local_path` | str |
| `kind` | `svg` · `video` · `audio` · `mesh` · `data` |
| `origin` | `deterministic` · `licensed` · `generated` |
| `licence`, `attribution` | str |
| `provider`, `model`, `provider_job_id` | required when `origin = generated` |
| `science_review_status` | `pending` (default) · `approved` · `not_applicable` |

### 3.9 `ProviderJob` — W: S9 (generation), N7–N8 · R: ledger, reconciliation, `costs.json`
| Field | Type / rule |
|---|---|
| `idempotency_key` | str, ≥ 8 |
| `provider`, `model` | str |
| `provider_job_id` | str or null; **required** for `submitted` / `running` / `succeeded` / `unknown` |
| `state` | `planned` · `reserved` · `submitted` · `running` · `succeeded` · `failed` · `unknown` |
| `estimated_cents` | int ≥ 0 |
| `actual_cents` | int ≥ 0 or null |
| `input_sha256` | 64 hex |

### 3.10 `GeneratorAdapter` / `PendingAdapter` — W: engineer (P1–P3) · R: provider workers
Protocol `estimate(request) → cents`, `submit(request, idempotency_key) → job_id`, `poll(job_id) → dict`, `fetch(job_id, directory) → AssetManifest`. `PendingAdapter(name)` raises `NotImplementedError` on every method until an authenticated integration is tested.

### 3.11 `ShortSpec` — W: SH2 · R: SH3–SH8, platform export

*(15 Oct 2026, RD-45)* Two fields are required by the runbook but **not yet in the code**: `ai_voice_disclosure` and `performer_credit` (05 SH2; 06 §6.4). `ShortSpec` is a strict model, so add them to `interfaces.py` and the schema before use.
| Field | Type / rule |
|---|---|
| `id`, `source_lesson_id` | str |
| `source_claim_ids` | list[str], ≥ 1 |
| `target_seconds` | int 20–60 |
| `hook`, `complete_payoff` | str |
| `retained_conditions` | list[str] |
| `destination_resource_id` | str *(15 Oct 2026) Retired from the pipeline contract under RD-49 and CE-68: the platform attaches entitlement outside the pipeline; removal from the 04 code is P1-01.* |
| `access_tier` | `free` · `book_entitlement` · `preview` *(15 Oct 2026) Retired from the pipeline contract under RD-49 and CE-68: the platform attaches entitlement outside the pipeline; removal from the 04 code is P1-01.* |
| `layout_strategy` | `reflow` only (crop rejected) |
| `approval_status` | `pending` · `approved` |

### 3.12 Render manifest (`<id>_<aspect>.manifest.json`, `pipeline.render`) — W: S12 · R: S13, GF, S15
`scene_id`, `aspect`, `cache_key`, `cache_hit`, `sha256`, `video`, `render_wall_seconds`, `frames`, `resolution`, `render_status` (`passed`), `release_status` (preview: `blocked_pending_audio_and_expert_review`), `audio_status` (preview: `intentionally_silent_technical_preview`; required for release: `approved_narration`), `science`, `media_qa` (incl. `passed`, `audio_present`), `layout_qa`, `environment`, `invoice_cost_usd`, `billing_note`, `warnings`.

### 3.13 Native extraction output (`extract-pdf`) — W: S1 · R: S2, S3
`source_file`, `sha256`, `extraction: native_text_only`, `pages[]` (`page_1_based`, `text`, `requires_visual_review: true`, `empty_text`), `syllabus_mapping_status: not_performed`.

### 3.14 600-second beat plan (`examples/*_600s_plan.json`) — W: S4 · R: S5, S8
`id`, `status` (`blueprint_only`), `duration_s`, `subject`, `technical_scene`, `objective`, `prerequisites`, `board_mapping_status`, `beats[]` (`start_s`, `duration_s`, `end_s`, `purpose`, `task`, `script_status`), `audio_status`, `mandatory_reviews` (academic, full_render, native_language_when_localized), `success_measures`.

### 3.15 Budget ledger table (`budget.py`) — W: N7, S9, S12 · R: cost dashboard, reconciliation
SQLite `jobs(key PRIMARY KEY, cents, state)`; `reserve(key, cents)`, `settle(key, actual_cents)`; states `reserved`, `settled` (a `released` transition is a build item).

### 3.16 Release-check output (`release_check`) — W: GF pre-flight · R: release service
`{"allowed": bool, "blocking_reasons": [...], "policy_only_not_authenticated_approval_service": true}` (conditions in [`06_QA_GATES_and_RELEASE.md`](06_QA_GATES_and_RELEASE.md) §6.1).

## 4. Narration contracts [TESTED as schemas]

### 4.1 `VoiceIdentity` — W: N1 · R: N3–N8, release evidence
| Field | Type / rule |
|---|---|
| `identity_id`, `version`, `brief` | str, non-empty |
| `locale` | `en-IN` · `hi-IN` · `as-IN` |
| `rights_status` | `audition-only` · `licensed-stock` · `consented-custom` · `unverified` (production requires licensed-stock or consented-custom) |
| `rights_record` | str, non-empty |
| `reference_audio_sha256` | str or null |

### 4.2 `Direction` — W: N4 · R: N6
`mode` (`curious` · `steady` default · `deliberate` · `light` · `reassuring` · `focused`); `target_wpm` int 80–185 (default 140); `emphasis` list[str]; `notes` str.

### 4.3 `Cue` (narration) — W: S6, N3 · R: N11 → engine S11
`cue_id` (`^[a-z][a-z0-9_-]*$`); `phrase` (non-empty); `occurrence` int ≥ 1 (default 1); `edge` `start` (default) · `end`; `action` `show` · `highlight` · `transform` · `hide` · `reveal-answer`; `element_id` (non-empty).

### 4.4 `Pause` — W: S5–S6, N3 · R: N11
`kind` `none` (default) · `beat` · `think` · `pause-video`; `seconds` 0–30; `prompt` str. `none` must have 0 s; `think`/`pause-video` require a prompt.

### 4.5 `Segment` — W: S5–S6, N3 · R: N4–N11
`segment_id` (`^[a-z][a-z0-9_-]*$`); `objective_id`; `claim_ids` (≥ 1); `text_template` (1–6,000 chars; no `[…]` or `<…>`; `{{tokens}}` for STEM terms); `direction`; `pause_after`; `cues`; `expected_visuals`; `critical_phrases`; `answers_after` (earlier question segment ID or null).

### 4.6 `NarrationPlan` (`configs/narration.schema.json`) — W: S5 (draft), N3 · R: N4–N12, engine manifest (`narration_plan_uri`)
`schema_version` `"1.0"`; `lesson_id` (`^[a-z][a-z0-9_-]*$`); `academic_edition`; `source_claim_manifest`; `voice` (`VoiceIdentity`); `lexicon_version` (must equal the lexicon's `version` at compile); `segments` (≥ 1; unique segment IDs; unique cue IDs; `answers_after` must reference an earlier segment ending with `think`/`pause-video` > 0 s).

### 4.7 `ProviderProfile` (`configs/<profile>.json`) — W: N6 (engineer/narration lead) · R: compiler, provider worker
`provider` (`elevenlabs` · `cartesia` · `gemini` · `openai`); `model`; `voice_id`; `api_version` (required by Cartesia); `live_contract_verified` bool (default false; production requires true).

### 4.8 `AlignedWord` and `Alignment` — W: N10 · R: N11
`AlignedWord`: `text`, `start` ≥ 0, `end` > `start`. `Alignment`: `segment_id`; `audio_sha256` and `transcript_sha256` (64 hex; transcript hash = digest of the expanded spoken text); `method` (`provider-timestamps` · `forced-aligner` · `human` · `synthetic-fixture`); `engine_version`; `words` (monotonic; overlap tolerance 1 ms). `synthetic-fixture` sets `contains_fixture: true` (release blocked).

### 4.9 Lexicon entry (`configs/pronunciation.json`) — W: N5 · R: N6 (compile), captions
Top level: `version`, `review_scope`, `entries`. Entry: `display`, `meaning`, `locales: {<locale>: {spoken, caption, editorially_checked, acoustic_approved}}`. [PROPOSED additions per message 12 §10.2]: `subject`, `allowed_variants`, `model_overrides` (per provider/model/voice, only after acoustic test), `reviewer`, `accepted_audio_sha256`.

### 4.10 Compiled request file (`outputs/<profile>_requests.json`) — W: N6 · R: provider worker (N8), reviewer
`status` (`offline-request-compilation-not-live-integration`), `lesson_id`, `requests[]`, `network_operations: 0`. Each request: `segment_id`, `method`, `url`, `headers_template` (`ENV:` placeholders), `body`, `canonical_spoken`, `caption_text`, `audio_cache_key`, `editorial_style`, `warnings`.

### 4.11 Timeline (`timeline.json`) — W: N11 · R: engine S11–S13
`lesson_id`, `sample_rate` (48,000), `fps_num`, `fps_den`, `total_samples`, `duration_seconds`, `audio_sha256`, `clips[]` (`segment_id`, `start_sample`, `end_sample`, `audio_sha256`, `alignment_method`), `pauses[]` (`segment_id`, `start_sample`, `end_sample`, `kind`, `prompt`), `events[]` (`cue_id`, `sample`, `frame`, `action`, `element_id`, `segment_id`), `captions[]`, `contains_fixture`.

### 4.12 Narration QA and release records — W: N9, N12, GF pre-flight · R: GF
`transcript_check` → `surface_word_error_rate`, `edit_count`, `critical_mismatches`, `needs_human_check`, `limitation`. `signal_report` → duration, rate, channels, sample peak, RMS, clipped samples, DC offset, silences (planned flag), `not_measured`. `master` → `before`, `after`, `target`, `within_target`. `release_report` → `release_allowed` (always false locally), `blockers[]`; evidence keys `academic_listening`, `voice_rights`, `native_language_review`, `caption_review`, `sync_review`, hash match, mastering.

## 5. Proposed records (not yet code) [PROPOSED]

| Record | Fields | W | R | Source |
|---|---|---|---|---|
| v1 `LessonSpec` additions | worked problems, retrieval questions, expected answers, exam terminology, narration reference | S4 | S5–S8 | message 02 §7 |
| v1 scene contract additions | approved component (+ version), scientific-data hash, display text, separate spoken text, semantic event IDs, actual audio offsets, camera/layout tokens, declared simplifications, output hash | S8–S12 | S12–GF | `QA_and_Implementation_Contract.md` |
| Scene pedagogy record | the 12 fields (Part 1) | S4 (draft), S8 (complete) | S5–S13, GF | message 04 §13 |
| ST beat record (`beat_table.json`) | `id`, `start_s`, `end_s`, `hold_s`, `tone`, `title`, `spoken_text`, `visual_direction`, `interaction{type ∈ prediction/guided_pause/independent_pause/retrieval_pause/feedback/none, prompt, expected_answer}`, `sync_note`, `word_count`, `estimated_active_wpm`; root `schema_version`, `title`, `language`, `target_runtime_s`, `status`, `academic_review`, `timing_status`, `audience`, `scope`, `sources`, `beats` | S5 | linter, S6, S8 | ST `examples/sample_lesson.json` |
| Analogy card | `id`, `target_relation`, `familiar_relation`, `mapping`, `non_mapping`, `likely_misconception`, `formal_return`, `learner_check`/`student_check`, `status` | S6 | GA | ST `references/analogy_card.example.json` |
| Humour candidate | `concept_anchor`, `comedic_mechanism`, `literal_science_risk`, `translation_risk` (+ no-joke option) | S6 | GA | ST concept-humour |
| Interaction prompt | `expected_answer`, `acceptable_variations`, `available_hint`, `reveal_trigger`, `estimated_task_time`, `feedback`, `retry` | S6 | S8, S11 | ST interaction-designer |
| Recent-script ledger row | `script_id`, opening type, analogy domain, interaction form(s), joke premise, feedback/praise phrase, ending | S5 (ST script-evaluator) | S5 | message 08 §11.4 |
| Export record | lesson/class/subject/language/edition IDs, access designation, destination resource, approved thumbnail/title/description, source and rights attribution, approved video hash; *(15 Oct 2026, RD-45)* `ai_voice_disclosure`, `performer_credit` | S14 | platform | message 10 §10.2; 06 §6.4 |
| Activation code record (platform) | hash of secret, serial, SKU, edition, print batch, issuing status (`generated → printed → issued → redeemed`; `suspended`, `revoked`, `expired`), redemption deadline, audit history | platform (M3) | platform | business runbook §6 |
| Auditable Reel content record | chapter ID, claim source, science approval, script, 9:16 scene, caption, target class/medium, CTA destination, experiment ID, release status | SH8 | growth, audit | Execution Runbook §5 |
| Per-pilot record | academic defects (C/M/m), reviewer minutes, editing minutes, pronunciation repairs, render time cold/cached, peak memory, accepted-asset generation attempts, total cost, fresh-question performance immediate/delayed, calibration counts, full listen Y/N, mobile review Y/N, approvals with hashes | P2 pilots | P2 gate | message 10 §9; `INSTRUCTIONS_running_the_four_pilots.md` §5.1 |
| `costs.json` | fields in [`08_COST_TRACKING_and_BUDGETS.md`](08_COST_TRACKING_and_BUDGETS.md) §3 | all stages | founder, P3 gate | runbook "Cost and observability" |
| Provider admission record | provider, API version, model ID, lifecycle dates, voice rights, voice ID, locale, permitted controls, audio format, rate/concurrency limits, estimate/actual usage, sample hashes, reviewer approvals | N7 | provider worker | `Provider_Lifecycle.md` |
| Skill activation record | Skill name, source pack, source folder hash, date, client, model, eval result | 01 §6 | all agent sessions | 06 INSTRUCTIONS §2 |

*(15 Oct 2026)* Records added to the v2 specification by the completeness critic (RD-53) are specified in `15_content_engine_v2/`, not here: the Curriculum Framework (`schemas/curriculum_framework.schema.json`, level-1, CE-111), SRC `rights_basis` (level-1, CE-112), blob `retention_class` and `backup` ledger rows (level-1, CE-114), `export/withdrawals.jsonl` and `incident` ledger rows (level-2, CE-115), and the aggregate `learning_signal` record (`schemas/learning_signal.schema.json`, level-2, CE-117).

## 6. Write/read matrix (summary)

| Artefact | Written at | Read at |
|---|---|---|
| `source-native.json`, `source-ledger.json` | S1 | S2, S3, S14 |
| `syllabus-map.json` | S2 | S3, S4, GA |
| `claims.json`, `answer-keys.md` | S3 (S7, GA update status) | S4–S9, GA, SH |
| `lesson-spec.json` (LessonPlan + beats + pedagogy drafts) | S4 | S5–S14 |
| `script/narration_plan.json` | S5, S6, N3 | N4–N12, engine manifest |
| `script/beat_table.json` | S5 | linter, S6, S8 |
| `science/*` (ScienceReport, verified model, independent review) | S7 | GA, S8, S9, GF |
| GA approval | GA (service) | S8 onward; invalidated by bundle change |
| `scenes/scene-spec.json`, `asset_manifest.json` | S8, S9 | S11–S13, S14 |
| `audio/*` (lexicon version, requests, jobs, raw, accepted, ASR diff, alignment) | N5–N10 | N11, GF evidence |
| `audio/timeline.json`, master, QA | N11–N12 | S11–S13, GF |
| `render/*` (final.mp4, manifest, VTT, SRT, transcript) | S12 | S13, GF, S14 |
| `qa/*` | S13 | GF |
| GF approvals; release manifest | GF (service), S14 | publisher, platform |
| `export/export_record.json` | S14 | platform |
| `shorts/<id>/*` | SH1–SH8 | GS, platform, scheduler |
| `costs.json`, `pilot_record.md` | all stages | founder, phase gates |
