# QA Profiles Registry (Content Engine v2 subsystem)

Status: subsystem specification, 15 Oct 2026. Nothing here has run. Parent: `../ARCHITECTURE_content_engine_v2.md` §3.4 (R6, R7), §3.6, §4 (S7, S11–S13), §9. Schema: `schemas/qa_profile.schema.json`. Template: `templates/qa_profile.template.md`.

Tags: **[Recommendation]** is a design choice made here; **[Hypothesis]** needs a pilot; [N#] cites `../SOURCES_and_claims.md`. Section references such as 07/06 §4 point to `07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md`, 12/10 to `12_advanced_animations_with_claude/02_documentation/10_QA_GATES_anim.md`, 05 §12 to `05_narration_system/INSTRUCTIONS_narration_pipeline.md`, 13 to `13_strong_to_cheap_model_strategy/STRATEGY_strong_to_cheap_models.md`.

Two rules from 07/06 override everything below: a single critical scientific error blocks release whatever the other scores are, and automated checks cannot decide scientific validity or real learning.

---

## 1. What a QA Profile is

A **QA Profile** is the expanded, parameterised list of every check and human gate that one artefact must pass. The `profile-resolver` computes it from the EPP as a pure function:

`qa_profile = qa_resolve(EPP, qa/catalogue@<version>)`

It has six axes, all taken from the EPP: **format** (with variant), **level**, **family**, **locale**, **safety class** and **voice path**. It also reads render target, aspect, overlay and style. The profile is canonicalised (NFC, RFC 8785 JCS, SHA-256; CE-32) as `qa_profile_sha256`. *(Corrected 15 Oct 2026.)* The hash is `sha256(JCS(NFC(profile minus qa_profile_sha256 minus provenance.created_at minus preconditions)))`, so two resolver runs on one EPP and one catalogue pin give the same hash. qa_profile_sha256 is computed with `preconditions` removed (runtime reviewer availability and open-item states), so staffing changes never alter it; `preconditions.reviewers_available` stays in the record because the ac0 branch needs it (15 Oct 2026, resolver-14). Open items are listed by id only; their state is read from the Architecture §12 register at RELEASE-CHECK (§3 rule 8), so closing an item does not change the hash. The catalogue version is a registry pin, so it sits inside the EPP pins and reaches every approval's `closure_hash` only through `epp_hash` (Architecture §3.7 closure manifest M; registry pins are not separate closure keys, and `qa_profile_sha256` is not a closure key; corrected 15 Oct 2026). Changing a check's threshold therefore re-queues exactly the affected artefacts (§6).

[Recommendation] The catalogue lives at `content/registry/qa/catalogue@1.0.0.json`, a new registry kind `qa/`. ~~Its changes use the **Validation** change class (the same row as a subject-family profile in Architecture §3.6). The architecture's registry table has no `qa/` row yet; this is listed as an inconsistency in §11.~~ *(Corrected 15 Oct 2026; Architecture §3.1 addendum, CE-63.)* A `qa/` change is classed by its effect. Tightening (a new check, raised severity, narrowed threshold or wider applicability) is **Validation**. Loosening Q-SAFE, Q-FLASH, Q-A11Y, Q-DISC or Q-RIGHTS is **Safety** (child-development sign-off where `safety/ac0` is in scope; G-COUNSEL re-record where class rules loosen). Other loosening is **Validation** with academic-lead sign-off. Removing a CE-35 day-one check or making it report-only is refused. A new gate or co-sign role is **Structural**. GR rejects a release whose declared class does not match its diff.

The profile is read by:
- every validator, which takes its thresholds from it;
- the runner, which schedules checks by stage;
- `examleaf-release-review`, which assembles the evidence;
- the approval service, which refuses an approval when the evidence for a check in that gate's scope is missing.

A profile is never edited by hand.

### 1.1 Severity and enforcement vocabulary

| Term | Meaning |
|---|---|
| **C** critical | Blocks release. **Never waivable** by anyone (07/06 §4; 12/10 §5). Repair at the owning stage, then re-approve on the new hash. |
| **M** major | ~~Blocks release unless a named reviewer who holds the gate role for that check waives it, with a reason, on the approval record bound to the artefact hash. The author can never waive. At `safety/ac0`, majors in Q-SAFE, Q-FLASH and Q-A11Y cannot be waived [Recommendation].~~ *(Revised 15 Oct 2026: the old text named no waiver role, no record field and no lapse rule.)* Blocks release unless a reviewer holding the check's **waiver role** (§2.12) records a waiver in `approval.waivers[]` (`check_id`, `finding_sha256`, `reason`, `reviewer_id`, `role`, `artefact_sha256`, `catalogue_pin`; Architecture §3.7), bound to the artefact SHA-256 and the catalogue pin. A waiver lapses on any byte change or catalogue version change, and auto re-affirmation (§5 item 3) never carries it. The author never waives. A check with no waiver role is not waivable. At `safety/ac0`, majors in Q-SAFE, Q-FLASH and Q-A11Y cannot be waived. Waived majors are ledger rows, reported per check and gate (§7). No fixed waiver count is set (Maturity Roadmap §1). [Recommendation; extends the examleaf-anim-qa waiver rule (07/06 §4 note) to every catalogue check; needs a CE decision] |
| **m** minor | Logged and tracked. It must not be allowed to accumulate (07/06 §4). |
| **R** report-only | Runs and records evidence, but does not block yet (CE-35). It becomes blocking at the stated trigger. It is never counted as a pass. |
| incomplete | A required check has no evidence, or its tool failed. This blocks exactly like C (examleaf-anim-qa decision rules). |

Mode is one of **auto** (a script; the name is given, or marked [to build]), **human** (a named role from the reviewer registry), or **hybrid** (both are required).

---

## 2. Check catalogue (`qa/catalogue@1.0.0`)

**ID scheme.** Each check uses the architecture's own ID (§9.1 Q-checks; A1–A17 from 12/10) where one exists. A sub-check adds a dotted suffix to its parent, for example `Q-CLOSURE.literals`. There are two new parents, `Q-NARR` and `Q-INT` [Recommendation]. They cover the narration and interaction layers that §9.1 leaves to A9/A10 and 07/06 §2.1. *(Added 15 Oct 2026.)* A third new parent, `Q-AUDIO`, covers the music and sound checks of `MUSIC_and_SOUND_REGISTRY.md` §9 (§2.10). An A-check may also take a dotted suffix (`A9.package`, `A7.brief_subset`), as `packaging_profile.schema.json` already allows. Every check that a sibling registry runs (Packaging §11, Music §9, Scripting §15) has a row in this catalogue, which owns its severity (§10). *(Added 15 Oct 2026, completeness review.)* Two more new parents: `Q-LOC` for meaning equivalence across locales (Q-LOC.meaning, §2.2; level-3+, CE-118) and `Q-REPR` for the corpus-level representation audit (§2.13; level-3+, CE-121). Q-REPR runs over the released corpus, never over one artefact, so `qa_resolve` never puts it in a QA Profile.

**Notation.**
- "All" means every registered format, level and family (currently 26 formats, 10 levels and 10 families including the recommended `family/evs_foundational`), unless the row narrows it. *(Corrected 15 Oct 2026; it said "all nine families".)*
- "Video" means `render_target = video`.
- **Exam content** means: the EPP pins an exam overlay, or format ∈ {F4, F9, F17, F25}, or family = `exam_strategy` (15 Oct 2026).
- **Fixture-bound scene** means a scene with at least one `data-fx` element (15 Oct 2026).
- **Formats with checks** means the Format Plan has a slot of kind `check.*`, `card.*`, `viva.*` or `hook.question_reveal` (15 Oct 2026).
- Each row's owner, defect scope, waiver role and review-minute estimate are in §2.12 (15 Oct 2026).
- Evidence is written to `jobs/<artefact_id>/qa/<check_id>.json`, and each file carries `artefact_sha256` plus its input hashes. Existing report names are kept where they already exist.

### 2.1 Contract and system checks (every artefact)

| ID | Verifies | Mode · implementation | Severity | Applies | Pass criteria | Evidence |
|---|---|---|---|---|---|---|
| Q-SCHEMA | Every record validates against its draft-07 schema. A Script Spec, Interaction Spec or QA Profile carries the level, safety_class, persona, persona_variant and register_overlay of the EPP at its epp_hash; a mismatch is critical. Registry ids are patterns; Q-SCHEMA checks that each id resolves to an entry pinned in the EPP at epp_hash (15 Oct 2026) | auto · CI schema step [to build] | C | All | 0 errors; golden negatives fail; every registry id in a per-artefact record equals the corresponding EPP resolved value and appears in EPP.pins | `qa/Q-SCHEMA.json` |
| Q-COMM | No commercial term in schemas, registries or sidecars (CE-26 regex) | auto · `ci/commercial_lint.py` [to build] | C | All | 0 matches outside the three exempt editorial fields | `qa/Q-COMM.json` |
| Q-HASH | NFC + JCS + SHA-256 canon; Python and Node hashes agree. Writers emit set-valued arrays in canonical order: QA Profile `checks[]` sorted by `check_id` and `gates[]` by `gate` (Architecture §3.5 Set order; 15 Oct 2026) | auto · hash canon pair + golden test [to build] | C | All | Identical hashes on the multi-script fixture set, which includes one YAML registry entry containing an unquoted `no`, a quoted date and a Devanagari string (Python and Node must agree on its hash; Architecture §3.1 Registry entry hash), and the listed set-valued arrays are in canonical order (Architecture §3.5 Set order) | CI log |
| Q-DET | Two renders from one closure on the same `harness/` pin give identical frames and bytes (§9.3; CE-38 bitexact encode). *(Revised 15 Oct 2026: 12/10 A3 step 2 says never compare MP4 bytes; for v2 CE-38's pinned bitexact encode supersedes that, and A3 frame comparison stays the diagnostic.)* | auto · `determinism_hash_check.py` (frames) + MP4 SHA compare [extend] | C; precondition O-16 (the resolver emits `precondition_open_items: ["O-16"]` until the toolchain builds are pinned) | Video, audio_only (bytes) | Frame hashes equal and MP4 SHA-256 equal for two renders on the same `harness/` pin | `qa/determinism.json` |
| Q-META | Neutral metadata only; `audience_class` present | auto · `examleaf-packaging-export` exporter lint [to build] | C | All | Required fields present; no unknown fields | `qa/Q-META.json` |
| Q-META.hash_bind | Master SHA-256 equals the SHA-256 bound in the GF/GS approval. Each delivered variant has its own GF/GS on its SHA-256. Each rendition carries `derived_from_sha256` equal to the approved master and passes its re-checks (Packaging §11). Whether variants and renditions need their own GF/GS stays open under CE-14 (Packaging §15 item 5). (Added 15 Oct 2026) | auto · release service [to build] | C | All | Hashes equal | `qa/Q-META.json` |

### 2.2 Script checks (S7, on the compiled script and sentence-to-node map)

| ID | Verifies | Mode · implementation | Severity | Applies | Pass criteria | Evidence |
|---|---|---|---|---|---|---|
| Q-CLOSURE | Every assertive sentence maps to ≥1 approved CLM, SIM, WRK step or ASM in the Format Plan (CE-12) | auto · `closure-check` [to build] | C | All | 0 unmapped sentences. Every sentence counts as assertive unless a deterministic template marks it non-assertive; the flagger may only add sentences [N43] | `qa/Q-CLOSURE.json` |
| Q-CLOSURE.literals | No new numbers, dates, names or units | auto · `closure-check` | C | All | Every literal appears in a referenced node or fixture output | same |
| Q-CLOSURE.conditions | Cited claims keep their conditions; revisions never drop a negation, direction word, sign, exponent or condition (fed by SCRIPTING SQ-20; added 15 Oct 2026) | hybrid · `closure-check` (assumption tokens, fill-to-fill diff) + GA-Δ reviewer | C | All; core for stem_fixture | 0 missing assumption tokens; 0 dropped items in any revision diff | `qa/Q-CLOSURE.json` |
| Q-CLOSURE.ren_equivalence | A REN preserves its source node's literals (added 15 Oct 2026). *(Level-3+, 15 Oct 2026, CE-118: a REN changes wording only.)* A REN field may not target ANL `mapping` or `non_mapping`, STY `beats[].carries`, WRK numbers or context entities, or ASM keys; a culturally adapted analogy, story or word-problem context is a new ANL, STY or WRK node with `adapted_from` and `locale_scope[]`, reviewed at GA-Graph | auto · `closure-check` [to build], also run as a graph lint before GA-Graph | C | Every REN in the closure | Every REN field key names a string field of the source node at `source_node_sha256`; every number, date, name, unit and symbol token in each REN field equals the source field's tokens after NFC and the locale's numeral and spoken-math normalisation (RD-29) | `qa/Q-CLOSURE.json` |
| Q-LOC.meaning | *(Level-3+, 15 Oct 2026, CE-118.)* Meaning equivalence of each REN against its source node: a model back-translates the REN into the source locale and diffs it against the source node; flagged sentences are routed to a bilingual subject reviewer (an `academic_subject` reviewer qualified in both locales) at GA-Δ. The GL-glossary record lists which terms were transcreated and which were kept in English, following the code-mix policy | hybrid · back-translation by `examleaf-multilingual-director` (back-check) + diff in `closure-check` [to build]; bilingual subject reviewer | R until the level-4 pilot measures its precision; then blocking through a GR change citing that measurement (§10) | Every REN in the closure (every non-source locale) | Every flagged sentence carries the bilingual reviewer's disposition on the GA-Δ record | `qa/Q-LOC.meaning.json` |
| Q-CLOSURE.asm_key | ASM keys are well formed (added 15 Oct 2026): for `item_kind: mcq`, exactly one option has `is_key: true` and `expected_answer` equals that option's `option_id` | auto · `closure-check` [to build], also run as a graph lint before GA-Graph | C | Every ASM in the closure | 0 malformed keys | `qa/Q-CLOSURE.json` |
| Q-CLOSURE.marking_scheme | Step marks are official (added 15 Oct 2026): the `exam_tags.marking_scheme[].marks` values sum to `exam_tags.marks`; each `key_span.source_id` is an SRC with `reliability_class: official_paper_or_key`; the span-hash check (Q-LEDGER.span) runs on each `key_span` | auto · `closure-check` + `span-verify` [to build] | C | Every ASM with `exam_tags.marking_scheme` | Sums equal; every key span official and verified | `qa/Q-CLOSURE.json` |
| Q-CLOSURE.sim_anl | Simplification only via SIM, analogy only via ANL permitted at the level (CE-11) | hybrid · `closure-check` + GA-Δ reviewer | C | All | Each SIM/ANL used has `permitted_levels ∋ level`; no paraphrase of an unsimplified claim; `what_is_lost` and `non_mapping` shown at GA-Δ | GA-Δ surface sheet |
| Q-CLOSURE.recompose | Derived video laid out from nodes, never cut from another render | auto · `format-compiler` invariant | C | F5, F11, every derived format | Format Plan has no source-render reference | Format Plan |
| Q-LEVEL.reading | Reading level: controlled vocabulary (level × locale), sentence length, new terms per scene, on-screen text kind | auto · `level-lint` [to build] | R until the level's pilot (CE-35); then M | All | Within Level Profile values | `qa/Q-LEVEL.json` |
| Q-PERSONA.register | Register matches the resolved persona (Junior, Coach, Super Teacher, Mentor, Lecturer, Seminar Lead, Exam Strategist, Skills Instructor, Colleague) | auto · `persona-lint` rules; optional cheap-model triage | R, then M | All | 0 register violations | `qa/Q-PERSONA.json` |
| Q-PERSONA.forbidden | Forbidden phrases: genius/easy/obvious/guaranteed marks, identity praise, "Mastered" after viewing, retired expressions; humiliating lines | auto · `persona-lint` + `lint_script.py` (03 starter pack) | C for humiliation (07/06 §4 Super Teacher gate); R then M otherwise | All | 0 hits | same |
| Q-PERSONA.fake_sensing | Fabricated awareness of the learner ("I heard you say…", unconditional "you got it right") | auto · `lint_script.py` FAKE_CONTINGENCY (escalated from warning) + `persona-lint` | C (deceptive personal response, 07/06 §4) | All | 0 hits | same |
| Q-PERSONA.fake_enthusiasm | Forced laughter, artificial ums, fake gasps, hype not tied to content | auto · `persona-lint` (NA voice-acting-director negatives) | M | All | 0 hits | same |
| Q-INT.answer_hidden | The script never states an answer before its reveal beat | auto · `closure-check` beat order + `validate_cue_sheet.py` | C | All formats with `check.*`, `card.*`, `viva.*`, `hook.question_reveal` | Answer tokens first appear after the reveal cue | `qa/Q-INT.json` |
| Q-INT.answer_surfaces | No answer token in overlays, end card, next-up preview, title, cover or description before the reveal (07/06 §3: hidden across diagram, captions, overlays and the following preview). (Added 15 Oct 2026) | auto · `safety-lint` OCR + copy lint | C | Formats with checks | 0 answer tokens on any surface before the reveal cue | `qa/Q-INT.json` |
| Q-DISC.script | ~~The disclosure line matches voice path and locale (Path A: "Performed by X; voice converted with AI tools; reviewed by Y."; Path B: "AI-generated narration; script by X; reviewed by Y.")~~ *(Corrected 15 Oct 2026.)* `ai_voice_disclosure` equals, byte for byte after NFC, the text at `disclosure.text_ref` (the pinned `voice/` entry) for `classification.locale` and the safety class (VOICE §3.9 rows, including the ac0 parent and child lines); `disclosure_variant` equals that entry's `disclosure.variant`. Accepted template ids: `path_a` (converted), `path_b`, and the VOICE §3.9 variants `path_a_direct` (Path A direct, as-IN) and `mixed` (F16 only); the `path_a_direct` and `mixed` wording is pending counsel (O-5) | auto · `release_check()` item 11 [to build] | C | All | Exact match; Path A line never on Path B | `qa/Q-DISC.json` |

### 2.3 Science and claim checks (S3, S7, S11), selected by family

| ID | Verifies | Mode · implementation | Severity | Applies | Pass criteria | Evidence |
|---|---|---|---|---|---|---|
| Q-FIX | Fixture diff: every number, intermediate and relationship recomputed; units and significant figures | auto · `examleaf.cli validate` + `examleaf-science-<subject>`; quant_social `ledger_recompute`; health `dosage_fixture`; evs_foundational `fixture_exec` (counting, measuring, calendar) | C | Families whose validators include fixture_exec, unit_dimension, sigfig, ledger_recompute or dosage_fixture (§3.1; today stem_fixture, quant_social, health_medicine, evs_foundational). *(Corrected 15 Oct 2026: evs_foundational added; ~~vocational~~ removed, because vocational declares no fixture validator and its `procedure_completeness` runs under Q-LEDGER.family at C.)* | Every on-screen and narrated number equals a fixture output | `science/science_report.json` |
| Q-FIX.sandbox | Code on screen equals output captured in the sandbox (CE-51) | auto · executable sandbox [to build] | C | stem_fixture (CS) | Byte-equal output; no network; caps respected | sandbox log |
| Q-FIX.answer_key | Answer key verified independently | hybrid · fixture/solver/official scheme (`answer_key_check.method`) + ST `examleaf-science-reviewer` re-solve | C | F4, F6, F9, F17, F25, any ASM, and any family whose validators include answer_key_solver (§3.1) | Keys agree; marks only from `source_paper` or `official_key` (CE-31) | same |
| Q-LEDGER.citation | Citation presence: every CLM has ≥1 source; ≥2 for exceptional or sensitive claims; ≥2 for every claim in high-risk families [N14][N17] | auto · `claim-ledger`; `citation-flag` triage [N41]–[N43] | C | All | 0 unsourced claims; every flag resolved | `qa/Q-LEDGER.json` |
| Q-LEDGER.span | Span verify: `span_sha256` matches the registered copy | auto · `span-verify` [to build] | C | All | All spans found in the SRC copy | same |
| Q-LEDGER.source_policy | No open wiki; no self-published source about a living person; reliability class allowed by the family [N18][N19] | auto · `claim-ledger` | C | All | 0 violations | same |
| Q-LEDGER.contested | Contested-state phrasing: attributed/contested claims carry their holder; no verdict; a Short never states one side as fact; board_vs_scholarship rendered as "the syllabus states…" (CE-29) | hybrid · `closure-check` pattern + GV-claims (2 reviewers) | C | All | Rendered sentence carries the attribution; 2 approvals on contested claims | same + approvals |
| Q-LEDGER.family | Every remaining validator in the family profile (date_name_consistency, map_boundary, statute_edition, jurisdiction_check, pattern_recompute, safety_claim, procedure_completeness, sensitivity_screen, grammar_orthography, rubric_entailment), mapped in §3.1; `params.validators` lists those the family declares. *(15 Oct 2026: quote_rights moved to Q-RIGHTS.)* | auto per validator; sensitivity_screen is hybrid (sensitivity reviewer) | C | Per `family.validators` | All listed validators pass | `qa/Q-LEDGER.family/<validator>.json` |
| Q-EXPIRY | No time-bound claim past `review_by` (CE-30) | auto · `claim-ledger` | C | All | 0 expired claims in the closure | `qa/Q-EXPIRY.json` |
| Q-RIGHTS | TXT/MED licences; owned music and SFX (CE-66, refining CE-54); past-paper ASM stems (`stem_form: verbatim` requires the `exam_tags.source_id` SRC `rights_status` ≠ `consulted_only`, added 15 Oct 2026); quote length; map boundary review (CE-53). *(Corrected 15 Oct 2026: it passed licensed music.)* | hybrid · rights lint [to build] + `music/` pins (MUSIC M6) + academic lead for maps | C | All | Music and SFX: every file is an admitted `music/` entry with origin `commissioned` or `code_composed` (owned only, CE-66; M6). TXT/MED: licensed, public-domain edition or in-house. Voice audio under Q-NARR.voice_pin. Maps reviewed against the registered policy source. *(Level-1, 15 Oct 2026, CE-112, P1-17.)* Every SRC in the closure whose `rights_status` ≠ `consulted_only` carries `rights_basis` {policy_ref `rights/<publisher>@x.y.z`, decided_by, decided_on}; the `rights/` entry it cites is released, not revoked and not expired on the release date; and each verbatim span is within that entry's `quotation_within_policy` limits. A missing `rights_basis` or an expired or revoked policy fails. Until O-23 (Counsel) closes, no `rights/` entry exists, so any verbatim past-paper stem, official-key marking, textbook figure or TXT passage fails; M1's past-paper ASM therefore uses `stem_form: adapted` and shows no marks | asset ledger; `qa/Q-RIGHTS.json` |
| A12a | Science validators re-run on the fixtures the render used | auto · `examleaf.cli validate` | C | Fixture-bound scenes | Fixture hashes equal those in the GA-Graph closure | `science/science_report.json` |
| A12b | Science-frame QA: displayed value, graph state and narration agree at every semantic event | hybrid · `examleaf-visual-qa` + academic owner | C | Fixture-bound scenes | Agreement at every event; and axes, units and stated conditions visible on every sampled frame of every aspect and derived format, a missing one being C (07/06 §4; 12/10 A12; added 15 Oct 2026) | `qa/visual_qa.json` |

### 2.4 Narration checks (S9)

| ID | Verifies | Mode · implementation | Severity | Applies | Pass criteria | Evidence |
|---|---|---|---|---|---|---|
| Q-NARR.text | No stage tags or `{{token}}` errors in spoken text | auto · narration contracts + `expand` | C | All with audio | 0 errors | narration `qa.json` |
| Q-NARR.asr_diff | Independent ASR transcript compared with the approved script (added or omitted words). ASR never certifies pronunciation (05 §10) | auto · `transcript_check` + ASR [to build; ASR not done] | R until an ASR provider is admitted (07/07) and P1-11 lands; then M (C when meaning changes). Q-NARR.critical_terms listening remains the blocking control. *(Revised 15 Oct 2026: a blocking check with no tool made every audio artefact incomplete.)* | All with audio | 0 meaning-changing differences | same |
| Q-NARR.critical_terms | Negations, exponents, units, charges, directions and critical numbers | hybrid · `transcript_check` critical phrases + critical-term listening (academic owner or native editor) | C | All with audio | Counts match; the listener signs | same + VOICE record |
| Q-NARR.pause_protection | Protected think windows intact; no `silenceremove` across them | auto · `signal_report(protected_intervals)` | C if a window shrinks below its `answer_protection` interval; M for unplanned silence ≥ 0.6 s | All with check beats | Windows intact ± 0.05 s | same |
| Q-NARR.signal | Clipping (\|x\| ≥ 0.9999), DC offset, duration | auto · `signal_report` | M | All with audio | Within 07/06 §2.1 limits | same |
| Q-NARR.alignment | Word order, monotonic timestamps, audio/transcript hashes; cue sheet not stale | auto · `validate_alignment` + `validate_cue_sheet.py` | C | All with audio | Hashes equal the accepted audio and approved script | `cue_sheet.json` |
| Q-NARR.voice_pin | Voice identity version, model and settings pinned in the EPP; licence valid and not revoked; Path B voice has a recorded GL-voice pass (CE-41); Path A performer consent (O-6) | auto · `profile-resolver` + release check | C | All with audio | Pins resolve; no revoked pin | EPP + `qa/Q-NARR.json` |
| Q-LOCALE.lexicon | Pronunciation lexicon and spoken-math policy for the locale; no untested critical pronunciation (07/06 §4) | hybrid · `examleaf-stem-pronunciation` corpus + native editor | C | All with audio | Every term resolves to a reviewed entry | lexicon report |
| A9 | Loudness −16 LUFS ± 1; true peak ≤ −1 dBTP (pass ≤ −0.9) on the final mux | auto · `examleaf_narration.cli qa` / `loudness_measure` | C *(raised from M 15 Oct 2026: MUSIC §1 policy 6; 12/10 §5 item 4; Packaging §11)* | All with audio | Within tolerance after mux | `final_audio_qa.json` |
| Q-NARR.mux_conform | Scene and timeline length equal audio length ± 1 frame; the mux refuses a mismatch > 0.05 s (07/06 §2.2; 13 V5). (Added 15 Oct 2026) | auto · `mux_supplied_audio()` | C | All with audio | Lengths within ± 1 frame; no mismatch > 0.05 s | `qa/Q-NARR.json` |
| Q-NARR.voice_consistency | Flags an unusual rate, level or speaker change across the narration (07/06 §2.1; 05 §12). (Added 15 Oct 2026) | hybrid · [to build] + VOICE reviewer | R until built; then M | All with audio | 0 unreviewed flags | `qa/Q-NARR.json` |

*Narration evidence keys (15 Oct 2026).* The 07/06 §6.2 narration evidence keys map to catalogue checks: `academic_listening` → Q-NARR.critical_terms; `voice_rights` → Q-NARR.voice_pin; `native_language_review` → Q-LOCALE.lexicon + the GA-Δ native editor; `caption_review` → Q-A11Y.captions; `sync_review` → A10; `mastering` → A9; approval/audio hash mismatch → Q-NARR.alignment. RELEASE-CHECK refuses when any of them lacks evidence (§3 rule 8; 12/10 §5 item 8).

### 2.5 Visual checks (S10–S11; A-suite from 12/10)

| ID | Verifies | Mode · implementation | Severity | Applies | Pass criteria | Evidence |
|---|---|---|---|---|---|---|
| A1 | Seek-contract lint | auto · `lint_seek_contract.js` | C (blocks render) | Video | 0 violations | `qa/anim_contract.json` |
| A2 | Render-box preflight | auto · `preflight.sh` (secret/ultracode greps not implemented; A17a covers them) | C (blocks render) | Video | Passes | preflight log |
| A3 | Determinism hash: identical PNG frames, including a reverse-order render | auto · `determinism_hash_check.py` | C | Video | All frame hashes equal (2D); 3D tolerance [Hypothesis] | `qa/determinism.json` |
| A4 | Safe zones from the style's token set for the EPP aspect | auto · `safe_zone_check.py --require-measured` | C for essential/science elements and unmeasured tokens at release; M other text | Video | No essential element in UI insets or caption reserve | `qa/safe_zone_report.json` |
| A5 | Hold times (headline ≥ 1.2 s, Indic × 1.5 [Recommendation]; equation ≥ narration end + 0.5 s; 2–4 s after a transform; prediction prompt for the whole think window). Headline hold = m_script × m_level × max(1.2, 0.3 × words); m_level is read from the Level Profile `on_screen.hold_level_multiplier`, times any style `hold_extra_multiplier` (VISUAL_STYLE §2.3; 15 Oct 2026) | auto · `safe_zone_check.py` | M for science text; C when a prediction prompt is gone before its window ends; values for l1_2–l6_8 are Cal [Hypothesis] | Video | All holds met | same |
| A6 | Luminance series per frame and per tile: the measurement step for Q-FLASH.* (§2.9) | auto · `flash_check.py`, extended as `flash-analyser` | see Q-FLASH | Video | — | `qa/flash_report.json` |
| A7 | Fixture-vs-rendered text; no text in generated rasters | auto · `text_fixture_diff.py` (OCR fallback is weaker evidence) | C for a science mismatch, missing or untraceable science text, or raster text; M for display-text drift | Video | Exact match after normalisation | `qa/text_diff.json` |
| A7.brief_subset | On-screen strings are a subset of the brief and approved-script strings; catches leaked reasoning (13 V2). (Added 15 Oct 2026) | auto · `text_fixture_diff.py` [extend] | C | Video | 0 on-screen strings outside the brief and script | `qa/text_diff.json` |
| A8a | Glyph coverage (no tofu) | auto · font coverage pass | C | Video, every locale | 0 missing code points | `qa/glyph_coverage.json` |
| A8b | Indic shaping and cluster integrity; rtl layout | hybrid · `grapheme_clusters.py` + native reader | M for a split cluster; C for unreadable text the native reader rejects | Indic and rtl locales | No split at a mark, joiner or virama; reader signs | `qa/indic_shaping.md` |
| A10 | Caption and reveal sync: reveal at word t0 or ≤ 0.05 s before (± 1 frame), never late; captions equal the approved script | auto · `safe_zone_check.py --cues` + `examleaf-audio-caption-qa` | C for an early answer reveal or a caption change that alters meaning; M for a late reveal > 1 frame | Video | All reveals in window | `qa/audio_caption_qa.json` |
| A11 | Media probe at the **EPP resolution** (1080×1920, or 1920×1080 only where the Format Spec is 16:9), 30 fps, frames = round(duration × fps), h264, yuv420p, audio present | auto · `media_check()` [extend: read resolution from EPP] | C | Video | Exact | `qa/media.json` |
| A13 | Contrast ≥ 4.5:1 text / ≥ 3:1 essential graphics on real frames; 360 px display-width readability | hybrid · `examleaf-visual-qa` + device check at GF/GS | C for contrast (CE-35). C when a `data-fx` element (science value, symbol, unit, exponent, sign) or an answer element fails the 360 px rule (12/10 R3; 07/06 §4 Super Teacher gate "inaccessible essential symbol"). M for other essential text, including non-fixture labels (07/06 §4 Major "unreadable essential label"). *(Corrected 15 Oct 2026: it rated the whole 360 px rule M.)* | Video | Ratios met on sampled frames | `qa/visual_qa.json` |
| A14 | No camera move while a `data-fx` element is revealed or held; no element transform without a declared `data-motion` verb (`qa/motion_log.json`, DOM and SVG only; canvas-internal motion at H-SB and GF) (15 Oct 2026) | auto · `safe_zone_check.py` | M; C at `safety/ac0` (15 Oct 2026) | Video | 0 violations | `qa/anim_visual.json`, `qa/motion_log.json` |
| A15 | No unexpected uniform or black frames; no stalled render | auto · frame statistics in `examleaf-anim-qa` | C (blocks composition) | Video | 0 undeclared blank frames | same |
| A16 | Asset provenance and licence | auto · `examleaf-asset-library` AssetManifest | C | All | Every asset hashed, licensed, attributed | asset ledger |
| A17a | Budget headroom; effort/model audit; no ultracode, no bare alias | auto · `effort_policy.py` | C (blocks authoring) | All | Within caps; full model IDs | `costs.json` |
| A17b | Ledger completeness | auto · `examleaf-effort-governor` | M | All | Every run recorded | `costs.json` |

### 2.6 Interaction checks

| ID | Verifies | Mode · implementation | Severity | Applies | Pass criteria | Evidence |
|---|---|---|---|---|---|---|
| Q-INT.window_length | Think window ≥ the level's `think_window_s.min` and covers the whole prompt hold (RD-11) | auto · `validate_cue_sheet.py` + `level-lint` | C if absent or 0 s; M if below the minimum (R where the level value is Cal) | Formats with checks | Window ≥ the level minimum, or 4 s with `binary_choice: true` (RD-11; 15 Oct 2026) | `qa/Q-INT.json` |
| Q-INT.reveal_order | Question → think window → reveal → conditional feedback; answer cues ordered after their question | auto · `validate_cue_sheet.py` (`meta.answer_protection`) | C | Formats with checks | Order holds for every pair | same |
| Q-INT.interpolated | Each chapter stands alone and ends in a check where the spec requires one [N30] (contested evidence) | auto · `format-compiler` plan check | M | F1, F10, F16, F19, F20, chaptered formats | Every required boundary has `check.interpolated` | Format Plan |
| Q-INT.modes | Response modes allowed by the level (say-aloud, point, move, draw, sing at l1_2/l3_5 [N10]; critique at pg) | auto · `level-lint` | R then M | All | Only allowed modes | same |

### 2.7 Packaging checks (S14)

| ID | Verifies | Mode · implementation | Severity | Applies | Pass criteria | Evidence |
|---|---|---|---|---|---|---|
| Q-META.sidecar_complete | Sidecar holds subject, family, level, format, locale, competency GUIDs, versions, hashes, audience class, a11y tracks, disclosure, and a provenance block (contributors, sources, last revision date [N60]) | auto · sidecar schema [to build] | C | All | All fields present and valid | `export/sidecar.json` |
| Q-META.interactions_sidecar | `export/interactions.json` validates against `packaging_profile.schema.json#/definitions/interaction_sidecar`; every Interaction Spec interaction appears exactly once; prompt_start, window_end and reveal_start equal the measured final timeline (added 15 Oct 2026) | auto · sidecar schema [to build] | C | Formats with interactions | Valid; 1:1 with the Interaction Spec; times match the timeline | `export/interactions.json` |
| Q-COMM.sidecar | Forbidden-field lint on the exported sidecar and titles | auto · `ci/commercial_lint.py` [to build] | C | All | 0 matches | `qa/Q-COMM.json` |
| Q-DISC.placement | Description line uses the matching template; YouTube synthetic toggle set on every upload with AI voice (Path A converted, Path B); for A_direct only when another realistic synthetic element is present; Meta AI label applied; C2PA not stripped (07/06 §6.4); child-variant wording at ac0 | hybrid · export check + publisher identity, per channel after S14; upload refused without a passing record (15 Oct 2026) | C | All | All four confirmed per platform; `made_for_kids_flag` set at ac0 on YouTube; `disclosure.voice_identity` equals the `voice/` pin in `sidecar.pins` and the EPP; `disclosure.voice_path` equals EPP `resolved.voice_path` | `content/packages/PKG-<id>.publish.<channel>.json` (`packaging_profile.schema.json#/definitions/publish_receipt`) |
| Q-META.package_truth | Title, cover text and every description block: assertive sentences map to approved nodes in the artefact's Format Plan; every number, date, name and unit is in a referenced node, a fixture output or a computed field (Packaging §4.1 rule 1); no marks claim without `marks_source`; no answer reveal. *(Revised 15 Oct 2026: it was M and banned every marks claim; Packaging §4.2 allows marks with `marks_source`.)* | hybrid · closure-check on the copy string table + GF/GS reviewer | C | All | 0 untraceable claims or literals | package record |
| Q-COMM.copy | Banned copy phrases in titles, covers and descriptions (Packaging §4.1; CE-70) | auto · `ci/commercial_lint.py` copy mode [to build] | C | All | 0 matches | `qa/Q-COMM.json` |
| Q-META.chapters | Chapter cues equal the Format Plan boundaries | auto · exporter | M | Chaptered formats | Within ± 1 frame | package record |
| Q-META.size | File size within the packaging profile's configured limit (value: verify; Packaging §15 item 6) | auto · exporter | M | Video | Within the configured limit | package record |
| A9.package | A9 on every delivered audio-bearing file, including renditions, the AD mix and audio-only | auto · `loudness_measure` | C | All with audio | −16 LUFS ± 1; true peak ≤ −1 dBTP (pass ≤ −0.9) | `final_audio_qa.json` |
| A11.package | A11 probe of every delivered video file against the EPP resolution and the packaging profile | auto · `media_check()` | C | Video | Exact | `qa/media.json` |
| A4.platform | A4 against the target platform's **measured** insets | auto · `safe_zone_check.py --require-measured` | C at release | Video | No essential element in the measured insets | `qa/safe_zone_report.json` |
| A8a.copy | Glyph coverage on cover text and burned captions (Packaging §11 "A8a.copy") | auto · font coverage pass | C | Video, every locale | 0 missing code points | `qa/glyph_coverage.json` |
| Q-RIGHTS.scope | For every `voice/` and `music/` pin in the closure, on the export date: voice entry admitted and not revoked; export date ≤ voice `expiry.expires_on` and, where consent exists, ≤ `consent.term_end`; package channel in `consent.platforms` and, for music, in `commission.platforms`; artefact locale in `consent.languages`; music `expiry.expires_on` null or ≥ export date (added 15 Oct 2026) | auto · neutral exporter (`examleaf-packaging-export`; reads the pinned `voice/` and `music/` entries) [to build] | C | All with audio | All conditions hold | `qa/Q-RIGHTS.scope.json` |

*Added 15 Oct 2026.* Rows Q-COMM.copy to A8a.copy (and Q-RIGHTS.scope) were defined only in Packaging §11; they are catalogued here, and this catalogue owns their severity. Q-META.hash_bind is in §2.1. Q-A11Y.captions and Q-SAFE.no_external_prompts also run on the S14 packaged surfaces (§2.8, §2.9).

### 2.8 Accessibility checks (`a11y/base`, CE-22)

| ID | Verifies | Mode · implementation | Severity | Applies | Pass criteria | Evidence |
|---|---|---|---|---|---|---|
| Q-A11Y.contrast | Same rule as A13, also run on the reduced-motion variant | auto · `a11y-check` [to build] wraps `examleaf-visual-qa` | C | Video | Ratios met | `qa/Q-A11Y.json` |
| Q-A11Y.cvd | Colour never the only differentiator; deuteranopia, protanopia and tritanopia simulation | auto · `a11y-check` + GF reviewer for F13 and F24 | R until O-20; then C | Video | Distinguishable under all three simulations | same |
| Q-A11Y.captions | Captions equal the approved script text (0 word mismatches); timing within the 05 alignment tolerance; spoken maths captioned in display notation | auto · `a11y-check` + `examleaf-audio-caption-qa` | C | Video, including packaged caption files and burned variants at S14. *(Corrected 15 Oct 2026: was All; an audio_only artefact delivers a transcript, checked by Q-A11Y.transcript.)* | 0 mismatches | same |
| Q-A11Y.transcript | Transcript present with display and spoken forms | auto · `a11y-check` | C | All | Present and hash-bound | same |
| Q-A11Y.reduced_motion | Reduced-motion variant rendered and passes the A-suite | auto · `a11y-check` | C | Video | Variant exists and passes | same |
| Q-A11Y.visual_essential | Every `visual_essential` scene is narrated, or `ad.vtt` + `audio_described.m4a` exist; R10 for audio_only | auto · `a11y-check` | C | All | No unflagged silent visual | same |
| Q-A11Y.caption_lines | Caption line length per level (`short_lines` for l3_5, l6_8) | auto · `a11y-check` | R (Cal) | All | Within the level's rule | same |
| Q-A11Y.asm_labels | *(Level-3+, 15 Oct 2026, CE-120.)* Every option of every ASM in the interaction sidecar (`export/interactions.json`) and the Interaction Spec has a keyboard key and a screen-reader label (`option_labels[]`: mcq options; match, ordering and diagram_label items). Keys are unique within the interaction; labels give the option text and position only and never mark the key (answer protection, Q-INT.answer_hidden) | auto · `a11y-check` reading the Interaction Spec and the sidecar | C | Formats with interactions that present options | One label and one key per option; no label differs in form for the keyed option | `qa/Q-A11Y.json` |
| Q-A11Y.print_structure | *(Level-3+, 15 Oct 2026, CE-119, CE-120.)* For `render_target: print`: the PDF is tagged (PDF/UA) and the HTML twin is semantic; reading order equals the Format Plan order; headings nest; every figure has alt text or is marked as an artefact; table headers are tagged; document language is set per locale; contrast and "colour never the only differentiator" hold on the rendered pages; answers never sit on the same page as their questions (the key is a separate file or a final section) | auto · `a11y-check` (tag-tree and reading-order audit) [to build] + GF reviewer page by page | C | Print | All conditions hold | same |
| Q-A11Y.low_vision | *(Level-3+, 15 Oct 2026, CE-120.)* With `a11y/low_vision` pinned: caption scale and contrast tokens equal the profile's larger and higher-contrast values; no meaning is carried by a line thinner than the profile's minimum stroke token. Values come from the profile's tokens; none is set here | auto · `a11y-check` | C | Artefacts whose EPP pins `a11y/low_vision` | Within the profile's tokens | same |
| Q-A11Y.cognitive | *(Level-3+, 15 Oct 2026, CE-120.)* With `a11y/cognitive` pinned: measured pacing below the level band's lower bound by the profile's margin; one idea per beat (each beat binds at most one new CON or CLM); every SIM used is marked plain-language | hybrid · `a11y-check` + `level-lint` (pacing, beat binding) + academic owner at GA-Δ | M | Artefacts whose EPP pins `a11y/cognitive` | All conditions hold | same |
| Q-A11Y.dyslexia | *(Level-3+, 15 Oct 2026, CE-120.)* With `a11y/dyslexia` pinned: font, letter and line spacing and line-length tokens applied to every on-screen and printed text block. [Hypothesis until piloted] | auto · `a11y-check` | R | Artefacts whose EPP pins `a11y/dyslexia` | Tokens applied | same |
| Q-A11Y.isl | *(Level-3+, 15 Oct 2026, CE-120.)* With `a11y/isl` pinned: the voice path is A (Path A only); an Indian Sign Language interpreter inset is present for every narrated span, inside its safe-zone token, and is never covered by captions or overlays; the interpreter is an adult human performer with consent like any Path A performer, never a generated signer; a reviewer whose `reviewer/` entry records an ISL qualification approves the interpretation at GF. Until such a reviewer is registered, an `a11y/isl` request is refused at S5 (no candidate, as for a missing voice) | hybrid · `a11y-check` (inset presence and safe zone) + qualified ISL reviewer at GF | C; not waivable | Artefacts whose EPP pins `a11y/isl` | All conditions hold | same |

*Accessibility profiles (level-3+, 15 Oct 2026, CE-120).* The rows above Q-A11Y.asm_labels belong to `a11y/base`, which every artefact pins. `a11y/low_vision`, `a11y/cognitive`, `a11y/dyslexia` and `a11y/isl` are registered as data under `a11y/` (Architecture §3.1 addendum); each adds its own row only when a request names it, and none can be frozen before O-24 (Academic lead) registers the Rights of Persons with Disabilities Act 2016 and the Ministry of Education guidelines on e-content for children with disabilities (2021) as sources (status: to verify). Q-A11Y.asm_labels and Q-A11Y.print_structure belong to `a11y/base` from the date their inputs exist (interaction sidecar labels; the `print` render target).

*Producers (15 Oct 2026; SKILLS_and_KIT_MAP_v2 §6 rule 6).* `a11y-check` verifies the accessibility deliverables; it does not make them. The reduced-motion variant (Q-A11Y.reduced_motion) is rendered by `examleaf-render-batch`; `ad.vtt` and the transcript (Q-A11Y.visual_essential, Q-A11Y.transcript) by `examleaf-speech-animation-synchronizer`, from the script's `ad_sentences[]`; `audio_described.m4a` by `examleaf-voice-synthesis` (AD voicing, S9) and `examleaf-audio-production-engineer` (mix, S10).

### 2.9 Flash and child-safety checks (Q-FLASH, Q-SAFE)

| ID | Verifies | Mode · implementation | Severity | Applies | Pass criteria | Evidence |
|---|---|---|---|---|---|---|
| Q-FLASH.full_frame | Any whole-frame flash (house ban) | auto · `flash-analyser` | C | All video | 0 | `qa/flash_report.json` |
| Q-FLASH.wcag | WCAG 2.3.1 general and red flash, three-per-second rule (thresholds verified once O-1 registers S-1) | auto · `flash-analyser` | C | ac1, ac2 | Pass | same |
| Q-FLASH.tile | A tile flashing > 3 per second, where the area condition needs a human | hybrid · `flash-analyser` + production QA | ac0 C · ac1 M · ac2 M | All video | 0 at ac0; reviewed at ac1/ac2 | same |
| Q-FLASH.ac0_zero | CE-21: zero general or red flashes with the area threshold removed; tile grid plus a luminance-change rate | auto · `flash-analyser` | C; **R until O-2** signs the parameters (10×10 grid meanwhile), with AC0 release blocked on O-1 and O-2 | ac0 | 0 qualifying pairs in any tile | same |
| Q-FLASH.pattern | Regular moving or flickering patterns: no stripe, grid or checker pattern with more than five light–dark pairs over more than 25% of the frame may move, flicker, oscillate or reverse; static ones get a human check (VISUAL_STYLE §2.1, added 15 Oct 2026) | hybrid · `flash-analyser` + production QA | R until O-1 (and O-2 for ac0) | All video | 0 | `qa/flash_report.json` |
| Q-SAFE.no_solicitation | No request for names, schools, photos, comments, voice or any learner data (CE-19, CE-20); doubts paraphrased (F15) | hybrid · `safety-lint` + child-development reviewer (ac0) | C | ac0, ac1 | 0 hits | `qa/Q-SAFE.json` |
| Q-SAFE.no_external_prompts | No links, QR codes, URLs, handles, brand names or logos, and no like/subscribe/comment/share prompts, and no "watch next" or "next video" prompts (ac0; PACKAGING §8; 15 Oct 2026). Links only to official board or government sources (ac1) | auto · `safety-lint` (script, string tables, OCR of frames; at S14 also title, cover, description and transcript) | C | ac0; ac1 (links rule) | 0 hits | same |
| Q-SAFE.no_timers | No countdowns, streaks, timed pressure, urgency, fear or peer comparison (02 §H5) | auto · `safety-lint` (script + cue kinds) | C at ac0 and in exam content at ac1 (§2 notation); M otherwise. *(Clarified 15 Oct 2026.)* | All | 0 hits | same |
| Q-SAFE.startle | No sudden loudness jump or sudden whole-frame visual change beyond `motion.max_visual_change_rate` | auto · `flash-analyser` (visual) + audio short-term loudness [to build] | C; R until O-2 (visual) and O-22 (audio) close, with AC0 release blocked meanwhile; the resolver emits `precondition_open_items: ["O-2", "O-22"]` (Cal [Hypothesis]). *(Revised 15 Oct 2026: the audio sign-off had no open-item number.)* | ac0 | Within signed limits | same |
| Q-SAFE.language | One language per lesson unless a code-mix pattern is approved; on-screen text `icons_and_single_words` (l1_2) | auto · `level-lint` | C for the language rule; vocabulary as Q-LEVEL (R until O-17) | Levels with `single_language_per_lesson: true` (l1_2, l3_5; corrected 15 Oct 2026, was ac0) | Rules met | same |
| Q-SAFE.child_likeness | No generated real-looking children; a real child needs a guardian release on the MED node | hybrid · MED schema + GF reviewer | C | All (STY `real_child_likeness: false`) | 0 violations | asset ledger |
| Q-SAFE.activity | Household-safe materials and a "with a grown-up" cue; a non-household-safe ACT is never shown as try-at-home | hybrid · `safety-lint` + safety reviewer | C | ac0; F12 at every level | Rules met | same |
| Q-SAFE.audio_source | Owned audio only (CE-66; MUSIC policy 4): every music, sting, bed, ambience, song-backing and SFX file hash-matches an admitted `music/` entry with origin `commissioned` or `code_composed`; no licensed stock, public-domain recording, library, platform or trend audio. *(Corrected 15 Oct 2026: it passed licensed audio.)* | auto · asset ledger + `music/` pins (MUSIC M6) | C | ac0 (F5 and all formats); other classes through Q-RIGHTS | 0 non-owned or unadmitted music or SFX files | same |
| Q-SAFE.sensitive | Sensitive-topic review (health, body, mental health, safety, caste, religion, family structure, food) | human · sensitivity reviewer (ac0: plus child-development reviewer co-sign) | C if a flagged item is unreviewed | ac0, ac1, ac2. *(Corrected 15 Oct 2026: ac0 was missing.)* | Signed | approval record |

### 2.10 Music and sound checks (`MUSIC_and_SOUND_REGISTRY.md` §9; added 15 Oct 2026)

| ID | Verifies | Mode · implementation | Severity | Applies | Pass criteria | Evidence |
|---|---|---|---|---|---|---|
| Q-AUDIO.music_window | M1: no music, bed or ambience in a teaching window; SFX and stings silent in think, pause-video, equation-reading, inspection and safety-cue windows (12/10 A9 "music absent from core_explanation"; rubric R5) | auto · music-stem RMS per `meta.music_roles` window [to build] | C (MUSIC §1 policy 1 is fixed) | All with audio | Stem RMS below the floor in every forbidden window | `qa/Q-AUDIO.json` |
| Q-AUDIO.placement | M2: each placement's window role (from `meta.music_roles`, never self-declared) is allowed by the entry and not forbidden | auto · cue-sheet check [to build] | M | All with audio | 0 placements outside the entry's roles | same |
| Q-AUDIO.bed_level | M3: measured bed-to-dialogue difference within the entry's range | auto · `examleaf-audio-analysis` | R until T2; then M | All with a bed | Within the entry's range | same |
| Q-AUDIO.sting_budget | M8: sting count | auto · cue-sheet count | M | All with audio | ≤ 2 per lesson, ≤ 1 per Reel (MUSIC §9) | same |
| Q-AUDIO.sample_rate | M10: every file 48 kHz, with a resample-on-import record | auto · media probe | M | All with audio | 48 kHz everywhere | same |
| Q-AUDIO.human_listen | M11: bed with narration at phone volume; tags ok, chiptune, too busy, masks speech, wrong mood, startling | hybrid · listening form + audio lead | M; a "startling" tag at ac0 escalates to Q-SAFE.startle | All with a bed or SFX | Every tag resolved | same |
| Q-AUDIO.provenance_wording | M12: code-composed audio is never credited as human-composed | auto · credit lint against `origin` | C (MUSIC §1 policy 5 is fixed) | All with music | 0 false credits | same |
| Q-AUDIO.voice_stem_clean | M13: no SFX or music tags in TTS text; no music bleed in the voice stem | auto · narration text lint + stem check | M | All with audio | 0 hits | same |
| Q-AUDIO.safety_cue_clean | M14: no bed or SFX overlapping `activity.safety_cue` | auto · cue-sheet overlap check | C | All with a safety cue | 0 overlaps | same |
| Q-AUDIO.ac0_engagement | M15: none of the MUSIC §7 AC0 engagement-audio patterns | auto · cue-sheet and stem check [to build] | C | ac0 | 0 patterns present | same |

The other Music §9 rows fold into existing checks: M4 → A9; M5 → Q-DET; M6 → Q-RIGHTS and Q-SAFE.audio_source; M7 → Q-SAFE.startle; M9 → A12b.

### 2.11 Map from 13 §2.4 validator ladder (added 15 Oct 2026)

| 13 rung | Catalogue checks |
|---|---|
| V0 | Q-SCHEMA |
| V1 | A1 |
| V2 | A7, A7.brief_subset |
| V3 | A3, Q-DET |
| V4 | A4, A5, A8b, A13 |
| V5 | A10, Q-NARR.mux_conform |
| V6 | §6 judge (triage only) |
| V7 | report-only drift flag (no catalogue row; never a pass) |
| V8 | §4 gates |

### 2.12 Owner, defect scope, waiver role and review minutes (added 15 Oct 2026)

The resolver copies these values into each check (`owner`, `defect_scope`, `waiver_roles`, `review_minutes_estimate`) and gate. The **waiver role** defaults to the role of the gate that reviews the check's evidence: S10–S13 checks → GF/GS `production_qa`; S7 script checks → GA-Δ `academic_subject`; S9 narration checks → VOICE (`academic_subject` or `native_language_editor`); S14 packaging checks → GF/GS `academic_subject`. It applies only where a check resolves to M; a C check is never waivable. A-check owners follow 12/10 §1 and §6. Review minutes are not yet measured: auto checks are 0; human and hybrid estimates are "verify" with basis `rd41_baseline` (RD-41: 85 min per lesson, not split per check) until O-14 closes, then `pilot_timed`. Cash cost of review is recorded as 0 (RD-41).

| Checks or gates | Owner | Defect scope | Waiver role (where M) | Est. review min (basis) |
|---|---|---|---|---|
| Q-SCHEMA, Q-HASH, Q-COMM, Q-COMM.sidecar, Q-COMM.copy | founder-engineer (CI) | schema_hash | — | 0 (auto) |
| Q-DET, A1, A3, A15 | `examleaf-motion-harness` (via `examleaf-web-composition` / `examleaf-render-batch`) | determinism | — | 0 (auto) |
| A2, A11, A11.package | `examleaf-render-batch` | determinism (A2); composition (A11) | — | 0 (auto) |
| Q-META, Q-META.sidecar_complete, Q-META.interactions_sidecar, Q-META.chapters, Q-META.size | `examleaf-packaging-export` (S14 exporter; 15 Oct 2026, was `examleaf-thumbnail-package`) | metadata | `academic_subject` (GF/GS) | 0 (auto) |
| Q-META.hash_bind | `examleaf-release-review` | metadata, schema_hash | — | 0 (auto) |
| Q-META.package_truth | `examleaf-thumbnail-package` + `closure-check` | claims_sources | — | verify (rd41_baseline) |
| Q-DISC.script, Q-DISC.placement | `examleaf-release-review` | disclosure | — | verify (rd41_baseline) for placement |
| Q-CLOSURE, Q-CLOSURE.literals, Q-CLOSURE.conditions, Q-CLOSURE.ren_equivalence, Q-CLOSURE.asm_key, Q-CLOSURE.marking_scheme, Q-CLOSURE.sim_anl | `closure-check` | claims_sources; science (literals, sim_anl) | — | verify (rd41_baseline) for sim_anl |
| Q-CLOSURE.recompose | `format-compiler` | composition | — | 0 (auto) |
| Q-LEVEL.reading, Q-INT.modes | `level-lint` | readability; instruction_answer | `academic_subject` (GA-Δ) | 0 (auto) |
| Q-PERSONA.* | `persona-lint` | tone | `academic_subject` (GA-Δ) | 0 (auto) |
| Q-INT.answer_hidden, Q-INT.answer_surfaces, Q-INT.reveal_order, Q-INT.window_length | `closure-check` / `examleaf-cue-sheet` / `safety-lint` | instruction_answer | `production_qa` (GF/GS) for window_length | 0 (auto) |
| Q-INT.interpolated | `format-compiler` | instruction_answer | `academic_subject` (GA-Δ) | 0 (auto) |
| Q-FIX, Q-FIX.sandbox, A12a, A12b | `examleaf-science-<subject>` | science | — | verify (rd41_baseline) for A12b |
| Q-FIX.answer_key | `examleaf-science-reviewer` | science, instruction_answer | — | verify (rd41_baseline) |
| Q-LEDGER.citation, Q-LEDGER.source_policy, Q-LEDGER.contested, Q-LEDGER.family, Q-EXPIRY | `claim-ledger` (triage `citation-flag`) | claims_sources | — | verify (rd41_baseline) for contested and sensitivity_screen |
| Q-LEDGER.span | `span-verify` | claims_sources | — | 0 (auto) |
| Q-RIGHTS, A16 | `examleaf-asset-library` | rights | — | verify (rd41_baseline) for maps |
| Q-NARR.text, Q-NARR.asr_diff, Q-NARR.critical_terms, Q-NARR.voice_consistency | `examleaf-narration-quality-reviewer` | audio; science (critical_terms) | VOICE (`academic_subject` or `native_language_editor`) | verify (rd41_baseline) for critical_terms and voice_consistency |
| Q-NARR.alignment, Q-NARR.mux_conform | `examleaf-alignment-localize` | sync | VOICE | 0 (auto) |
| Q-NARR.voice_pin | `profile-resolver` | rights, disclosure | — | 0 (auto) |
| Q-NARR.pause_protection, Q-NARR.signal, A9, A9.package | `examleaf-audio-caption-qa` (A9 with `examleaf-audio-production-engineer`, 12/10 §1) | audio | VOICE | 0 (auto) |
| Q-LOCALE.lexicon | `examleaf-stem-pronunciation` | audio, science | — | verify (rd41_baseline) |
| A4, A4.platform, A5, A6, A7, A7.brief_subset, A14 | `examleaf-anim-qa` (via `examleaf-visual-qa`) | readability (A4, A5); accessibility_flash (A6); science (A7); craft (A14) | `production_qa` (GF/GS) | 0 (auto) |
| A8a, A8a.copy, A8b | `examleaf-kinetic-typography` | readability | `production_qa` (GF/GS) | verify (rd41_baseline) for A8b native reader |
| A10 | `examleaf-audio-caption-qa` | sync | `production_qa` (GF/GS) | 0 (auto) |
| A13 | `examleaf-visual-qa` | readability, accessibility_flash | `production_qa` (GF/GS) | verify (rd41_baseline) for the device check |
| A17a, A17b | `examleaf-effort-governor` | metadata | `production_qa` (GF/GS) | 0 (auto) |
| Q-A11Y.* | `a11y-check` | accessibility_flash | `production_qa` (GF/GS); not at ac0 | 0 (auto) |
| Q-FLASH.* | `flash-analyser` | accessibility_flash | `production_qa` (GF/GS); not at ac0 | verify (rd41_baseline) for tile |
| Q-SAFE.* | `safety-lint` (startle: `flash-analyser` + audio loudness; child_likeness: `examleaf-asset-library`) | child_safety | `academic_subject` (GA-Δ) where M; not at ac0 | verify (rd41_baseline) for hybrid and human rows |
| Q-AUDIO.* | `examleaf-audio-compose` (audio lead) | audio; child_safety (ac0_engagement, safety_cue_clean) | `production_qa` (GF/GS) | verify (rd41_baseline) for human_listen |
| H-CG | approval service | instruction_answer | — | verify (rd41_baseline) |
| GV-claims, GA-Graph | approval service | claims_sources, science | — | verify (rd41_baseline) |
| GA-Δ | approval service | science, instruction_answer, tone | — | verify (rd41_baseline) |
| H-SB | approval service | composition, craft | — | verify (rd41_baseline) |
| VOICE, GL-voice | approval service | audio, sync | — | verify (rd41_baseline) |
| A-SUITE | runner | every A-check scope | — | 0 (automated) |
| GF / GS | approval service | every rubric scope (R1–R10) | — | verify (rd41_baseline) |
| COPY (15 Oct 2026) | approval service | metadata, claims_sources | — | verify (rd41_baseline) |
| Q-RIGHTS.scope (15 Oct 2026) | `examleaf-packaging-export` | rights | — | 0 (auto) |
| DISCLOSURE, G-COUNSEL | approval service | disclosure; child_safety (G-COUNSEL) | — | verify (rd41_baseline) |
| GL-glossary | approval service | readability, science | — | verify (rd41_baseline) |
| RELEASE-CHECK | approval service | schema_hash, metadata | — | 0 (automated) |
| Q-LOC.meaning (level-3+, 15 Oct 2026) | `examleaf-multilingual-director` (back-translation) + `closure-check` (diff) | claims_sources; readability | — (report-only until the level-4 pilot) | verify (rd41_baseline) for the bilingual reviewer |
| Q-A11Y.asm_labels, Q-A11Y.print_structure, Q-A11Y.low_vision, Q-A11Y.cognitive, Q-A11Y.dyslexia (level-3+, 15 Oct 2026) | `a11y-check` | accessibility_flash | `production_qa` (GF/GS) where M; not at ac0 | 0 (auto); verify (rd41_baseline) for the print page review and Q-A11Y.cognitive |
| Q-A11Y.isl (level-3+, 15 Oct 2026) | `a11y-check` + qualified ISL reviewer | accessibility_flash | — (critical, not waivable) | verify (rd41_baseline) |
| Q-REPR (level-3+, 15 Oct 2026; corpus, §2.13) | academic lead + sensitivity reviewer (policy); corpus query [to build] | — (no artefact defect) | — (never blocks) | verify (rd41_baseline), per quarter, not per artefact |

### 2.13 Corpus checks (added 15 Oct 2026; level-3+, CE-121)

A corpus check runs over the released corpus on a schedule, never over one artefact. It is not in any QA Profile, has no severity and never blocks or reopens an artefact.

| ID | Verifies | Mode · implementation | Severity | Applies | Output | Evidence |
|---|---|---|---|---|---|---|
| Q-REPR | Representation across many artefacts. Reads the optional `depicted_attributes` tags {given_name_origin_region, gender_presented, setting, disability_presented, language} on WRK contexts, STY characters, ASM stems and MED people (generated or drawn only; never real children), and reports their distributions per level × family × locale against reference ranges that the academic lead and the sensitivity reviewer record as registry policy. Untagged items are counted as untagged, never guessed | report · quarterly corpus query [to build] over released artefacts | Report-only; never blocks an artefact | Released artefacts, quarterly (Roadmap §6 quarterly cadence) | Distribution report; it feeds the authoring brief for the next quarter | `qa/corpus/Q-REPR-<yyyy-qn>.json` |

The common rule that no community, caste or religion is used as a marker of ability, wealth or wrongdoing applies to every family, STEM contexts included (`SUBJECT_VALIDATION_PROFILES.md` common rules, CE-121); it is checked per artefact by the existing GA-Graph and sensitivity review, not by Q-REPR.

---

## 3. Composition rules (`qa_resolve`)

1. **Union.** A check applies if any of these declares it: the universal set (Format Registry "QA"), the format's `qa_checks`, the family's `validators` (through the §3.1 map), the level, the safety class, every pinned `a11y/` profile (`a11y/base` always; `a11y/low_vision`, `a11y/cognitive`, `a11y/dyslexia` or `a11y/isl` when the request names one; 15 Oct 2026, CE-120), the locale, the voice path, the render target or the packaging profile's `export_qa` (§3.1 map and `export_qa` added 15 Oct 2026). No input can remove a check. Frame checks do not apply to an `audio_only` artefact because it has no frames; R10 adds Q-A11Y.visual_essential as C. Any video sibling still runs the whole suite.
2. **Severity is the maximum.** Effective severity = max(catalogue base, every contributing declaration). The safety class escalates as in the table below. Nothing lowers a catalogue severity.

| Area | ac2 | ac1 | ac0 |
|---|---|---|---|
| Q-FLASH.tile | M | M | C |
| A14 (15 Oct 2026) | M | M | C |
| Q-SAFE.no_timers | M | C in exam content, else M | C |
| Q-SAFE.sensitive | C | C | C |
| Q-FLASH.ac0_zero, Q-SAFE.startle, Q-SAFE.language | — | — | C (R only until their sign-off, with release blocked) |
| Majors in Q-SAFE, Q-FLASH, Q-A11Y | waivable by the check's waiver role (§2.12) | waivable by the check's waiver role (§2.12) | not waivable |
| Report-only Q-LEVEL / Q-PERSONA findings | logged | logged | the child-development reviewer must acknowledge each one at GA-Δ |

3. **Parameters are the most restrictive.** Minimums take the maximum and maximums take the minimum, each with provenance (R8). An empty feasible set is a compile error, never a clamp. Example: a hold time above the format's duration budget fails at S5.
4. **Enforcement.** ~~A check blocks if any contributor says it blocks, or if it is in the CE-35 day-one set. It is report-only only when all contributors agree and the check is outside that set.~~ *(Revised 15 Oct 2026: the old rule made Q-FLASH.ac0_zero and Q-SAFE.startle blocking while their rows said R.)* A check blocks if any contributor says it blocks, or if it is in the CE-35 day-one set. Exception: a day-one check whose parameters await a named sign-off resolves to `enforcement: report_only`, with `precondition_open_items` naming that item; RELEASE-CHECK refuses while any listed item is open. Otherwise a check is report-only only when all contributors agree and it is outside the day-one set.
5. **Gates add up (R7).** The profile's gates are the union of format, family, level, safety and locale gates. Co-signs attach to existing gates. Nothing removes a gate, and no gate is ever sampled (CE-14).
6. **Voice path.** Path A adds performer consent (O-6), the Path A disclosure line, and the rule that the performer is never the GF approver of their own performance (§3.2). Path B adds the GL-voice pass (CE-41) and the Path B line.
7. **Locale.** Adds A8a and A8b for Indic scripts, an rtl layout test for rtl scripts, Q-LOCALE.lexicon, GL-glossary for the first artefact of each family × locale pair, and a native editor on GA-Δ. Every REN locale also adds Q-LOC.meaning (report-only until the level-4 pilot; 15 Oct 2026, CE-118).
8. **Evidence.** Every applicable check must have evidence bound to the artefact hash. Missing evidence is incomplete, and incomplete blocks. *(15 Oct 2026.)* The profile lists the open items its release waits on by id only. Their state is read from the Architecture §12 register at RELEASE-CHECK, so closing an item does not change `qa_profile_sha256`.
9. **No self-approval.** The identity that authored a node, script or render cannot approve a gate that covers it. An agent identity can never approve (07/06 §6.3). *(Level-1, 15 Oct 2026, CE-113.)* Agent and service identities hold no reviewer role and no signing key, so they cannot produce a valid `signature`; a CI rule also rejects any commit by an agent identity that adds rows to `content/approvals/`.
10. **Review load (15 Oct 2026).** The profile carries `human_minutes_total`, the sum of the `review_minutes_estimate` values of its human and hybrid checks and its human gates (§2.12). The GR impact preview's K = Σ `human_minutes_total` over reopened gates plus the §5 item 4 audit minutes. The capacity ledger (CE-49) records actuals per check and gate, and the estimate basis moves from `rd41_baseline` to `pilot_timed` when O-14 closes. Cash cost of review is recorded as 0 (RD-41).

### 3.1 Validator-to-check map (added 15 Oct 2026)

A family profile declares validator names (`SUBJECT_VALIDATION_PROFILES.md` §2–§13), not catalogue ids. This map is a resolver input; an unmapped validator name is a compile error.

| Family validator | Catalogue check |
|---|---|
| fixture_exec, unit_dimension, sigfig, ledger_recompute, dosage_fixture | Q-FIX |
| executable_sandbox (matrix: sandbox) | Q-FIX.sandbox |
| answer_key_solver | Q-FIX.answer_key |
| claim_flagger | Q-LEDGER.citation |
| span_hash | Q-LEDGER.span |
| source_policy | Q-LEDGER.source_policy |
| expiry_check (matrix: expiry) | Q-EXPIRY |
| lexicon | Q-LOCALE.lexicon |
| quote_rights | Q-RIGHTS |
| date_name_consistency, map_boundary, statute_edition, jurisdiction_check, pattern_recompute, safety_claim, procedure_completeness, sensitivity_screen, grammar_orthography, rubric_entailment (added 15 Oct 2026; SUBJECT_VALIDATION_PROFILES §4, §5) | Q-LEDGER.family, with `params.validators` listing those the family declares and one evidence file per validator at `qa/Q-LEDGER.family/<validator>.json` |

No new ids are needed.

---

## 4. Human-gate map

### 4.1 Gates, roles and binding

| Gate | Roles (registry `reviewer/`) | Bound to | Reopens when |
|---|---|---|---|
| H-CG | Academic owner | `framework_version` + `cg_selection_sha256` (the selected item GUIDs) | Framework change alters the objective set |
| GV-claims | Family-qualified reviewer; two for contested claims | `claim_sha256` per claim | Claim, span or source changes |
| GA-Graph | Academic owner + family-qualified reviewer (+ child-development reviewer for ac0 subtrees) | `graph_subtree_sha256` | Any node in the subtree changes |
| GA-Δ | Academic owner, reading the full script with derived surface highlighted; native editor per locale; child-development co-sign at ac0 | `script_content_sha256` per locale + `interaction_spec_content_sha256` + `format_plan_sha256` + `graph_subtree_sha256`. *(Corrected 15 Oct 2026: ~~artefact SHA-256, EPP hash, subtree hash, closure hash~~, which do not exist at S7 and did not bind the script.)* | `script_content_sha256` or `interaction_spec_content_sha256` changes |
| H-SB | Founder or a named delegate (cost) **and** academic lead (fit): two identities; child-development co-sign at ac0 | `storyboard_sha256` of the record `content/storyboards/SB-<artefact_id>.json` = sha256(JCS(NFC({format_plan_sha256, script_content_sha256, grid, beats, cue_intent, estimate, fixture_output_sha256[], style_ids[] with the hashes of their safe-zone and layout-grid token files, hero_sheet_sha256[]}))) (RD-46). *(Corrected 15 Oct 2026: ~~grid, beats, estimate, script bundle~~; no storyboard record was defined.)* | `storyboard_sha256` changes. Selecting a different style reopens H-SB; a new version of the same style that leaves the grid tokens unchanged keeps it valid (Architecture §3.6) |
| VOICE | Teachers + native editor (voice gate); academic owner or native editor (critical-term listening) | `narration_audio_sha256` + voice pin + `lex/` pins | Audio regenerates, or the voice or lexicon pin changes |
| A-SUITE | Runner, **automated**: every applicable A-check and Q-check evidence present and passing; no human role (H-RV stays director evidence for GF/GS). (Added 15 Oct 2026) | artefact SHA-256 | Any byte change |
| GF / GS | Academic owner **and** a different production QA reviewer, full watch on phones; child-development co-sign at ac0 | `artefact_sha256` of each delivered file (Q-META.hash_bind) | Any byte change |
| COPY (added 15 Oct 2026) | Academic owner and a different production QA reviewer (the GF/GS pair); recorded at S12 alongside GF/GS and verified by RELEASE-CHECK at S13 | `copy_sha256` per locale | Title, cover text, description blocks, hashtags or cover image change |
| DISCLOSURE | ~~Publisher identity~~ *(Rewritten 15 Oct 2026.)* DISCLOSURE (S12, publisher identity) confirms the line text for the resolved voice path and locale, non-empty `ai_voice_disclosure` and `performer_credit`, and the end-card or child-variant line. RELEASE-CHECK requires it to be valid | ~~export record~~ the delivered file SHA-256 (Packaging §14); the record also names the voice pin and the `disclosure_text` SHA-256 | Voice version, locale or wording changes |
| RELEASE-CHECK | Approval service, **automated**. *(Expanded 15 Oct 2026.)* Refuses when: any pin or approval is stale or revoked, or the closure differs (Arch §3.7); Q-META.hash_bind fails; any of 07/06 §6.1 reasons 1 and 7–10 holds (artefact SHA-256 differs from the manifest; no valid academic and production approval exists for this exact SHA-256; the production approval lacks `full_video_watched`; both roles are held by one identity); any listed open item is open in the §12 register; any applicable check lacks evidence (§3 rule 8). No human can override it; refuses unless every gate_requirement in the QA Profile is met (Architecture §3.7; 15 Oct 2026). *(Level-1, 15 Oct 2026, CE-113, P1-16.)* It verifies the `signature` of every approval it relies on with `ssh-keygen -Y verify`, namespace `examleaf-approval`, over JCS(record minus signature), against the key in the `signing_keys[]` of the entry named by `reviewer_pin` whose `valid_from`–`valid_to` window contains the record's `timestamp`. An unsigned or mis-signed row counts as absent, so its gate is unmet; a key revoked through the scoped Revocation class makes every approval it signed absent | `closure_hash` | Every release |
| G-COUNSEL | Counsel, recorded per safety class and export schema version (CE-37). [Recommendation] Also recorded before a high-risk family activates (O-9) and before a new locale's disclosure wording is first used (CE-55, O-5) | counsel record | Law, store policy or schema changes |
| GL-glossary / GL-voice | Native subject editor; blind native-speaker panel | Glossary version (GL-glossary); voice version + `model_id` + `gs/<locale>-<family>` golden-set hash (GL-voice; VOICE §3.7). *(Aligned 15 Oct 2026.)* | Glossary, voice version, `model_id` or golden-set version changes; released artefacts unaffected unless a defect is found (Arch §3.1 addendum) |

H-RV (12/10 §4) remains director evidence for GF/GS, never a substitute for them.

*(15 Oct 2026.)* This table is the one place that lists each gate's bound object; an approval record's `artefact_sha256` holds that object's hash, and its `closure_hash` is the closure of the inputs that exist at the gate's stage (Architecture §3.7). Every record also keeps `epp_hash`, so a registry change marks it stale (CE-L10), and Architecture §3.6 re-affirms it when the bound object's hash is unchanged.

### 4.2 Per-format gate map

Every format passes GV-claims (on its subtree), GA-Δ, H-SB, VOICE, A-SUITE, DISCLOSURE and RELEASE-CHECK. Primary formats also require GA-Graph on their subtree. Derived formats require the consumed subtree's GA-Graph to be `valid`; a stale one blocks compilation. Level co-signs come from §4.1.

| Format | GA-Graph | GF / GS | Extra roles and conditions |
|---|---|---|---|
| F1 detailed, F19 derivation_proof | Yes | GF | F19: specialist at ug/pg |
| F2 simplified, F3 recap, F8 concept_intro, F10 revision_sheet, F13 comparison, F17 practice_set, F18 prerequisite_repair, F24 concept_map, F25 viva_prep | Consumed | GF | F13, F24: GF checks the CVD rule by eye; F18: register of the learner's level |
| F4 question_analysis | Yes | GF | Official key or source paper verified at GV-claims; exam-tag display |
| F5 short, F11 flashcard_reel | Consumed | GS | Each Short gets its own H-SB and GS; no approval is inherited (13 §5.7) |
| F6 worked_example | Yes | GF | Twin enters through S4 |
| F7 misconception_fix | Consumed | GF | Gentle form: child-development co-sign |
| F9 exam_strategy | Yes | GF | Academic lead approves the exam patterns (as-of dates) |
| F12 lab_demo | Yes | GF | Safety reviewer; practitioner at voc |
| F14 story_history | Yes | GF | Music licence; sensitivity reviewer for sensitive-tagged claims |
| F15 qa_doubt | Yes | GF | Safety lint sign-off: doubt paraphrased |
| F16 series | Members' | GF on bridges and the assembled file | Every member approval valid; bridges get GA-Δ |
| F20 lecture_segment | Yes | GF | Blocked until O-19 (16:9 token set) and A11 accepts 1920×1080 |
| F21 source_analysis | Yes | GF | Rights for TXT/MED; jurisdiction for law cases |
| F22 perspectives | Consumed | GF | Two qualified reviewers (family contested policy) |
| F23 read_along | Yes | GF | Native-speaker editor in GA-Δ; text licence; Path A for Indic |
| F26 teacher_explainer | Consumed | GF | Academic lead |

---

## 5. Sampling policy for re-QA after a registry change

CE-L10 and CE-34 apply literally: every affected artefact is queued for re-QA. CE-14 rejects sampling of human gates. Sampling here therefore only changes **order and extra audit**, never coverage.

1. **Automated re-QA covers 100% of affected artefacts** before any of them is re-affirmed. `impact-analyser` computes the set from the dependency index. The GR impact preview shows N approvals, M artefacts and K estimated gate-minutes (§3 rule 10) before merge.
2. **Canary first.** [Recommendation] The runner first re-QAs a stratified canary: at least one artefact per affected cell (format × level × family × locale × voice path), with every ac0 artefact in the canary. ~~If any canary check that passed before now fails, the whole batch halts: nothing is re-affirmed, and the change returns to GR. Failing artefacts follow the change-class table (revoked for safety or revocation classes).~~ *(Revised 15 Oct 2026: a halt stopped a Safety-class tightening from finding the published artefacts it was meant to withdraw.)* For Safety-class changes (including accessibility), Validation and Revocation, the batch never halts. Canary failures are revoked at once; then every remaining affected artefact is re-QA'd in full and every failure is revoked (Arch §3.6). For every other class, a canary check that passed before and now fails halts the batch: nothing is re-affirmed, the change returns to GR, and artefacts already failing follow the change-class table.
3. **Auto re-affirmation** only when re-derivation gives identical bytes and every check passes (CE-34). It is recorded as a re-QA record on the approval.
4. **Human audit of re-affirmations (additive).** [Recommendation] A reviewer with the gate role inspects the re-QA records (not a re-watch) for 5% of re-affirmed artefacts per cell, rounded up. This adapts the 5% shadow rate in 13 §6.7. At ac0 the child-development reviewer inspects 100% of the re-QA records. An audit finding reopens the gate for that artefact.
5. **Never sampled:** any human gate whose bytes changed; any change class that needs human judgement (safety loosening, reviewer-set change, contested escalation); revocations; the render-toolchain class, where every affected artefact is re-rendered from its closure and compared byte for byte.

---

## 6. Judge calibration protocol (VLM judge vs human panel)

The judge is 13's V6: a pinned vision ModelProfile (full model ID and explicit effort in `model/`) that answers **binary** rubric questions on a six-keyframe contact sheet.

1. **Panel.** Two blind raters per item, drawn from the reviewer registry with the relevant role, seeing outputs anonymised and in random order (13 §6.1). For ac0 cells, one rater is the child-development reviewer.
2. **Calibration set.** Stratified by format × level band × style × locale × aspect. It includes the seeded negatives (every negative card plus the 31 must-reject tests, 13 §2.4) and is kept separate from the Kit's sealed holdout.
3. **Admission.** A question is admitted per cell if the Wilson 95% lower bound of judge–panel agreement is ≥ 0.80 [Recommendation; stricter than 13 §6.2's 80% point estimate]. Its miss rate on seeded defects is also reported. A question below the bar is dropped for that cell.
4. **What a judge may do (triage only).** Reorder the review queue, add flags with frame times, pre-fill evidence links, and recommend escalation. A failure on an admitted question blocks until a human resolves it.
5. **What a judge may never do.** Approve, waive, pass a check, lower a severity, close a defect, sign science, or count as one of the two approvals. A judge "pass" has no effect on any gate. The approval service rejects any record whose `reviewer_id` is a model identity.
6. **Audit.** Sonnet 5.5 audits 10% of judged items plus every judge–verifier disagreement (13 §6.2).
7. **Recalibration** happens on any ModelProfile change (production class), on each new cell, quarterly, and when the audit disagreement rate rises above its baseline.
8. **Automation-bias guard.** One known defect is seeded per 10 lessons, and the human catch rate per gate is tracked (13 §6.7).

---

## 7. Escape-rate KPI

**Definition.** An **escape** is a defect of severity ≥ M that is first detected at a stage later than the earliest check or gate whose declared scope covers it. Each catalogue check and gate declares its defect scope (§2.12) from this closed vocabulary *(15 Oct 2026)*: rubric scopes `science` (12/10 R1), `instruction_answer` (R2), `readability` (R3), `sync` (R4), `audio` (R5), `accessibility_flash` (R6), `craft` (R7–R8), `tone` (R9), `composition` (R10); additional scopes `rights`, `disclosure`, `metadata`, `determinism`, `child_safety`, `claims_sources`, `schema_hash`.

| KPI | Formula | Cut by |
|---|---|---|
| Post-release escape rate | Defects ≥ M found after RELEASE-CHECK ÷ approved released minutes × 100 | severity, format, level, family, locale, voice path, safety class |
| Gate escape rate (gate G) | Defects in G's scope found downstream of G ÷ all defects in G's scope found anywhere | gate; GA-Δ escapes found at GF/GS trigger the CE-13 revisit |
| Check escape rate (check X) | Defects in X's scope that X passed ÷ defects in X's scope | check |
| Seeded catch rate | Seeded defects caught at gate G ÷ seeded at G | gate, reviewer role |
| Judge miss rate | Panel-confirmed defects the judge passed ÷ panel-confirmed defects | cell, question |
| Check false-positive rate (15 Oct 2026) | Findings overturned by the adjudicating reviewer ÷ findings raised | check, cell |

**Sources.** Ledger rows (CE-49) and the corrections log (07/06 §8).

**Targets.** Post-release critical escapes = 0 (07/06 §9: "zero unresolved critical errors"). Every other threshold is set from the previous maturity level's baseline and recorded as registry policy; none is invented here (Maturity Roadmap §1).

**Response.** Each escape adds a regression fixture (07/06 §8 step 7) and a catalogue review item.

---

## 8. Worked QA profiles

Universal set **U**: §2.1, Q-CLOSURE.*, Q-INT.answer_hidden / reveal_order / window_length, Q-LEDGER.citation / span / source_policy / contested, Q-EXPIRY, Q-RIGHTS, Q-DISC.*, Q-META.*, Q-COMM.sidecar, Q-COMM.copy, Q-NARR.*, A9 and Q-AUDIO.* (all with audio), A1–A17 (video), Q-A11Y.*, Q-FLASH.full_frame, Q-SAFE (class rows), Q-LEVEL and Q-PERSONA.

### 8.1 Detailed, `level/l9_10`, STEM (M1 CR-1)

- **Axes:** `format/detailed`, `level/l9_10`, subject physics → `family/stem_fixture`, `locale/en-in`, `safety/ac1`, Path A (R1: format default A and `series_position = first`), `style/doodle-handdrawn` (primary illustrative) + `style/whiteboard-science` (science layer; VISUAL §4.2 default for detailed). *(Corrected 15 Oct 2026: ~~`style/editorial-vox`~~ implements none of F1's teaching slots.)* 9:16.
- **Checks added to U:**
  - Q-FIX on every on-screen number (F1 extra), A12a, A12b, Q-FIX.answer_key;
  - Q-INT.interpolated (each chapter ≤ 360 s ends in a check [N3]);
  - Q-FLASH.wcag and Q-FLASH.tile (M);
  - Q-SAFE.no_solicitation, Q-SAFE.no_external_prompts (official links only), Q-SAFE.no_timers (C in exam content), Q-SAFE.sensitive.
- **Report-only:** Q-LEVEL and Q-PERSONA (Super Teacher). [Recommendation] l9_10 values are Inherited, so this level is first in line to make them blocking.
- **Gates:** H-CG → GV-claims → GA-Graph → GL-glossary (stem_fixture × en-in, first pair) → GA-Δ → H-SB → VOICE (Path A performance → STS; performer consent O-6) → GF + COPY → DISCLOSURE (Path A line; S12) → RELEASE-CHECK. *(GL-glossary inserted 15 Oct 2026, matching the Roadmap M1 Preconditions and Step 6.)* G-COUNSEL record for ac1 must exist.

### 8.2 Short (M1 CR-2)

- **Axes:** `format/short` variant `short.misconception`, `level/l9_10`, `family/stem_fixture`, `locale/en-in`, `safety/ac1`. Path B only if an en-IN voice has a recorded GL-voice pass; otherwise R1 gives Path A, and that is recorded (O-12).
- **Checks added to U:**
  - Q-CLOSURE.recompose (C): laid out at 1080×1920 from nodes;
  - Q-LEDGER.contested (C: no contested side stated as fact);
  - A11 at 1080×1920;
  - Q-SAFE.no_solicitation treats a "comment your answer" CTA as data solicitation (C at ac1, CE-20);
  - Q-FIX, Q-FLASH.wcag.
- **Gates:** GA-Δ (new hook or caption wording counts as new script), its own H-SB, VOICE, **GS**, DISCLOSURE (line for the resolved path), RELEASE-CHECK. Nothing is inherited from CR-1.

### 8.3 Story, `level/l3_5` (ac0)

- **Axes:** `format/story_history` (gentle story/song), `level/l3_5`, subject earth_science → `family/stem_fixture`, `locale/hi-in`, `safety/ac0`, Path A (R1: ac0 and level floor A), `style/storybook-junior` (extends `style/paper-collage`; ac0 only; VISUAL §4.2 default for story_history at ac0). *(Corrected 15 Oct 2026: ~~`style/paper-collage`~~ is not selectable at ac0.)*
- **Preconditions:**
  - O-1, O-2, O-3, O-4, O-7 and O-22 closed;
  - G-COUNSEL record for ac0;
  - an active child-development reviewer **and** a backup (no out-of-registry substitute, CE-36);
  - GL-glossary for stem_fixture × hi-in.
- **Checks added to U:**
  - every Q-SAFE row at C, including Q-SAFE.sensitive with the child-development co-sign;
  - Q-FLASH.tile (C) and Q-FLASH.ac0_zero (R until O-2, release blocked);
  - Q-SAFE.startle (R until O-2 and O-22 close, release blocked);
  - Q-SAFE.language (single language, hi-IN only);
  - Q-CLOSURE on every teaching story beat (each carries a CLM or SIM);
  - Q-RIGHTS for `song_chant` (owned audio only, CE-66);
  - A8a and A8b (Devanagari);
  - Q-INT.modes (call-and-response with real pauses [N10]);
  - Q-DISC.placement with child-variant wording.
- **Escalations:** Q-LEVEL and Q-PERSONA (Junior) stay R, but every finding needs the child-development reviewer's acknowledgement. No major in Q-SAFE, Q-FLASH or Q-A11Y can be waived.
- **Gates:** GA-Graph (STY subtree; child-development reviewer on the panel) → GA-Δ + co-sign → H-SB + co-sign → VOICE (teacher performance; the performer is not the GF approver) → GF + co-sign → DISCLOSURE → RELEASE-CHECK.

### 8.4 UG lecture segment

- **Axes:** `format/lecture_segment`, `level/ug`, physics → `family/stem_fixture`, `locale/en-in`, `safety/ac1` (always, CE-18), Path A (format default), 16:9 at 1920×1080. The style must list 16:9 in `aspects_supported`.
- **Preconditions:**
  - the O-19 16:9 safe-zone token set exists;
  - A11 is extended to read the EPP resolution (today 12/10 A11 fails every 16:9 file);
  - a family-qualified reviewer with at least a PG degree is registered.
- **Checks added to U:**
  - A4 against the 16:9 tokens;
  - A13 using Displayed = Source × 360 / 1920;
  - Q-FIX on every derivation step;
  - Q-INT.interpolated per chapter, with segments ≤ 360 s even inside long lectures [N31];
  - Q-PERSONA (Lecturer) R.
- **Gates:** GA-Graph → GA-Δ → H-SB → VOICE → GF → DISCLOSURE → RELEASE-CHECK.

### 8.5 Class 10 humanities Recap

- **Axes:** `format/recap`, `level/l9_10`, subject history → `family/humanities_citation` (active from M4), `locale/hi-in`, `safety/ac1`. Path B only with a GL-voice-passed hi-IN voice, otherwise A.
- **Checks added to U:**
  - Q-LEDGER.family: `date_name_consistency`, `map_boundary` (C if a map MED is used), `sensitivity_screen`;
  - Q-LEDGER.contested at C. [Recommendation] A contested key claim may appear only in attributed form and only when a Perspectives artefact for the topic exists or is in the same series (family rule); otherwise it is a compile error routed to the academic lead;
  - Q-FIX does not apply (no fixture validators in this family);
  - Recap coverage: one key claim per objective;
  - A8a and A8b;
  - GL-glossary for humanities_citation × hi-in on the first artefact of the pair.
- **Gates:** GV-claims (two reviewers for contested claims; sensitivity reviewer for sensitive ones) → consumed GA-Graph → GA-Δ (academic owner + native hi-IN editor) → H-SB → VOICE → GF → DISCLOSURE → RELEASE-CHECK.

---

## 9. Negative tests (each must be refused or blocked; CI fixtures [to build])

| # | Input | Expected |
|---|---|---|
| N-1 | A style or format declaration sets Q-FLASH.full_frame to M | `qa_resolve` error: severity cannot be lowered |
| N-2 | An ac0 render with one opposing luminance pair in a single tile | Q-FLASH.ac0_zero critical; a waiver attempt is refused |
| N-3 | A reviewer records a waiver on any C finding | Approval service refuses: critical is not waivable |
| N-4 | A judge (model identity) writes an approval or a "pass" | Rejected; the gate stays open |
| N-5 | Format Spec bump changes bytes; the runner proposes auto re-affirmation | Refused: bytes differ, so GA-Δ, H-SB and GF/GS reopen fully |
| N-6 | Re-QA plan samples GS for changed Shorts | Refused: human gates are never sampled |
| N-7 | A stem_fixture, quant_social, health_medicine or evs_foundational profile without Q-FIX | Resolver compile error |
| N-8 | The script author's identity approves GA-Δ | Refused (conflict of interest, CE-36) |
| N-9 | A Short states a contested claim without attribution | Q-LEDGER.contested critical |
| N-10 | One caption word differs from the approved script | Q-A11Y.captions critical |
| N-11 | A Path B artefact carries the Path A disclosure line | Q-DISC.script critical |
| N-12 | An ac0 script says "comment below" or shows a QR code | Q-SAFE.no_solicitation / Q-SAFE.no_external_prompts critical |
| N-13 | An ac0 cue sheet contains a countdown cue | Q-SAFE.no_timers critical |
| N-14 | `format/short` rendered at 1920×1080 | A11 critical |
| N-15 | Flash report missing for a video artefact | incomplete, release blocked |
| N-16 | `audio_only` with an unnarrated `visual_essential` scene | R10 compile error / Q-A11Y.visual_essential critical |
| N-17 | Sidecar contains `is_free` | Q-COMM.sidecar critical |
| N-18 | An expired `exam_pattern` claim in an F9 closure | Q-EXPIRY critical |
| N-19 | A report-only Q-LEVEL result counted as a pass in the release evidence | Release check refuses: R is never a pass |
| N-20 | GF approval recorded on SHA-256 X; `final.mp4` is SHA-256 Y | Q-META.hash_bind critical; RELEASE-CHECK refuses |
| N-21 | A `data-fx` exponent falls below the style's minimum displayed size at 360 px width | A13 critical; a waiver attempt is refused |
| N-22 | A Safety-class tightening fails one canary artefact | The batch continues, and every failing published artefact is withdrawn |
| N-23 | An ac0 artefact with both GF approvals but no child_development co-sign on GA_DELTA (15 Oct 2026) | RELEASE-CHECK refuses |
| N-24 | A hi-IN REN of a CLM changes 0.4 A to 4 A (15 Oct 2026) | Q-CLOSURE.ren_equivalence critical |
| N-25 | A GF approval row with no `signature`, or signed by a key outside its `valid_from`–`valid_to` window (level-1, 15 Oct 2026, CE-113) | RELEASE-CHECK counts the row as absent and refuses |
| N-26 | An SRC with `rights_status: licensed` and no `rights_basis`, or citing a `rights/` entry past its expiry, in a released closure (level-1, 15 Oct 2026, CE-112) | Q-RIGHTS critical |
| N-27 | A verbatim past-paper stem while O-23 is open (level-1, 15 Oct 2026) | Q-RIGHTS critical (no `rights/` entry exists) |
| N-28 | An MCQ interaction whose sidecar option C has no screen-reader label, or whose keyed option's label says "correct" (level-3+, 15 Oct 2026, CE-120) | Schema rejects the missing label; Q-A11Y.asm_labels critical for the revealing label |
| N-29 | An hi-IN REN of an ANL rewrites its `non_mapping` for a local analogy (level-3+, 15 Oct 2026, CE-118) | Q-CLOSURE.ren_equivalence critical; the adapted analogy must be a new ANL with `adapted_from` and `locale_scope[]` at GA-Graph |
| N-30 | A print Worksheet whose answer key sits on the question page, or whose figure has no alt text (level-3+, 15 Oct 2026, CE-119) | Q-A11Y.print_structure critical |
| N-31 | An `a11y/isl` request resolving to Path B, or with no ISL-qualified reviewer registered (level-3+, 15 Oct 2026, CE-120) | Resolver refuses at S5 |
| N-32 | A Q-REPR report used as a reason to block an artefact (level-3+, 15 Oct 2026, CE-121) | Refused: Q-REPR is report-only and never in a QA Profile |

---

## 10. Build notes

- The catalogue is data: changing a severity or threshold is a GR change, never a code edit.
- New scripts land behind the skills named above. ~~Ownership is in `SKILLS_and_KIT_MAP_v2.md`.~~ The Owner column of §2.12 is authoritative; `SKILLS_and_KIT_MAP_v2.md` gives each skill's stage and status (15 Oct 2026).
- Every catalogue release must reject ~~N-1 to N-24~~ N-1 to N-32 (15 Oct 2026), plus the 31 must-reject tests (13 §2.4).
- A sibling registry may number its own rows, but every check it marks blocking or report-only maps to a catalogue id (as SCRIPTING §15 Feeds does). An unmapped check is a catalogue review item (15 Oct 2026).
- Every auto or hybrid check has fail fixtures at `content/registry/qa/goldens/<check_id>/fail/`, plus pass fixtures where a false flag is possible, pinned by the catalogue version. A catalogue release must flag every fail fixture. A check moves from R to blocking only through a GR change that cites its measured false-positive rate (§7) and fail-fixture result, which is the CE-35 trigger (15 Oct 2026).

## 11. Inconsistencies found while writing this

1. 12/10 A11 rejects every 1920×1080 file, but CE-46 and F20 allow 16:9. A11 must read the resolution from the EPP before F20 can pass. **Resolved 15 Oct 2026 (CE-69):** `12_advanced_animations_with_claude/02_documentation/10_QA_GATES_anim.md` A11 now requires the resolution to equal the aspect declared by the Format Spec (default 1080×1920; 1920×1080 only when the format declares 16:9 and 16:9 safe-zone tokens exist). Making `media_check()` read the EPP is a P1 build item.
2. The examleaf-anim-qa SKILL.md body still rates any whole-frame flash and untraceable science text as major (Execution steps 4 and 5). Its status note and 07/06 §4 say critical. This profile follows 07/06. **Resolved 15 Oct 2026 (CE-69):** the SKILL.md body (steps 4 and 5, selftest list) and `references/flash_test_method.md` now say critical; the scripts already did.
3. `lint_script.py` reports fake contingency only as a warning. v2 makes it critical.
4. The `reviewer_roles` enums in the level and subject schemas lack `production_qa` and `publisher`, which GF and DISCLOSURE need. `qa_profile.schema.json` adds them.
5. Architecture §9.1 has no narration or interaction rows, and §3.1 has no `qa/` registry or change-class row. This document proposes `Q-NARR`, `Q-INT` and `qa/catalogue` (Validation class). **Resolved 15 Oct 2026 (CE-63):** `qa/` is added to Architecture §3.1 by a dated addendum with the Validation change class.
6. Format Spec `qa_checks` is a free string list, and the template shows lowercase `q-closure`. The linter should enforce catalogue IDs.
7. RELEASE-CHECK is automated, not human. The gate enum has no child-development co-sign gate, so co-signs are modelled as roles.
8. Counsel for new families and locales is an extension (CE-37 covers safety classes and the export schema only).
9. Classes 1–5 EVS / "world around us" is listed in no family, so R3 would refuse those requests. **Resolved 15 Oct 2026 (CE-65):** `family/evs_foundational` is added to `SUBJECT_VALIDATION_PROFILES.md` §13 as a [Recommendation].
10. *(15 Oct 2026, completeness review.)* `qa_profile.schema.json` accepts the new parent `Q-LOC` in its `check_id` pattern but not `Q-REPR`, because a corpus check never appears in a per-artefact profile (§2.13). It also accepts `render_target: print` in `axes`; a print profile has no aspect, resolution, voice path, `voice_path_reasons` or VOICE gate (no narration), and must carry Q-A11Y.print_structure.
11. *(15 Oct 2026.)* Q-A11Y.isl needs an ISL-qualified reviewer, but the gate role enum has no ISL role. This catalogue reads the qualification from the reviewer's `reviewer/` entry; adding a role id, and adding `a11y/isl` to the R1 force-A reasons (`voice_path_reasons` in `epp.schema.json` and `qa_profile.schema.json`), is a lead decision under CE-120. **Resolved 15 Oct 2026 (CE-123, CE-124): `a11y_isl` is an R1 Path A reason code in Architecture §3.4, `epp.schema.json` and `qa_profile.schema.json`; the ISL reviewer role id and the interpreter consent field wait for the P1-11 reviewer schema and the first `a11y/isl` request.**
