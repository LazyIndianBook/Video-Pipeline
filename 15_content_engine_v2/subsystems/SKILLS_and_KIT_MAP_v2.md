# Skills and Kit Map v2 (Content Engine v2 subsystem)

**Status.** Subsystem specification, 15 Oct 2026. Nothing here has run. Like every skill in the library, all 72 existing skills are drafted and **not agent-evaluated** (06 README).

**Machine-readable companion.** `skills_map_v2.csv` (~~87 rows: 72 existing + 15 new~~ ~~89 rows: 72 existing + 17 new, adding `packaging-export` and `kit-verify`; corrected 15 Oct 2026~~ 91 rows: 72 existing + 19 new, adding `curriculum-ingest` (level-1, CE-111) and `print-render` (level-3+, CE-119); updated 15 Oct 2026). Columns: `name, pack, status_v2, stage_v2, output_owned, registry_validated, slot_types_owned, slot_types_extended, maintainer, activation_trigger, exec_mode`. `stage_v2` holds only `;`-separated values from {S1..S14, GR, admission, migration, post-release, all}; it is empty for retired skills. `slot_types_extended` lists slots a skill writes for, extends or checks without owning the visual. An empty `maintainer` means none is assigned yet (06 assigns none). New skills carry the `examleaf-` prefix in the CSV like every installed skill (changed 15 Oct 2026).

**Inputs.** This map reads:
- `../ARCHITECTURE_content_engine_v2.md` §4 (stage owners), §5.2 (slot vocabulary) and §10 (06 row: the new skills; "skills for no active cell stay dormant");
- `06_skills_library/README.md`, `SKILLS_PIPELINE_STAGE_MAP.md` and `OVERLAP_and_DEDUPLICATION.md` (with addenda), and `SKILLS_MATRIX.csv`;
- 13 §2.2–§2.4, §3.2, §4.1 and §5–§6 (Kit, archetypes, cascade, verifiers);
- `QA_PROFILES_REGISTRY.md` (check IDs).

**Tags.** [Recommendation] marks a design choice made here. [Hypothesis] marks a value a pilot must confirm. The prefix `examleaf-` is omitted in the tables.

**Stage ids.** S1–S14 are the v2 stage ids of Architecture §4. They do not equal 07/03's S0–S16 numbers (07 S5 is the script; v2 S5 is format derivation). §8.1 gives the crosswalk (added 15 Oct 2026).

**Packs.** ST = Super Teacher (10), VE = Video Engine (32), NA = Narration (15), AN = Advanced Animation (15).

---

## 1. Status vocabulary and totals

| Status | Meaning in v2 | Count |
|---|---|---|
| **reuse** | Runs unchanged. Its contract is format- and level-agnostic. | ~~8~~ 6 |
| **extend** | Kept as the owner, author, extender or lens. It must now read the EPP or Format Plan instead of hard-coded class, subject or aspect. | ~~51~~ 53 |
| **dormant** | Installed but not activated until a cell needs it. The trigger is named. Admission still needs `skills-security`. | 6 |
| **retire** | No longer fires in the engine. Its distinctive rules are folded into the named owner's checklist. The folder stays in 06 as history (ST skills stay usable as a standalone script kit outside the engine). | 7 |

Counts corrected 15 Oct 2026: audio-production-engineer (programme mix, `audio_described.m4a`) and speech-animation-synchronizer (`ad.vtt`, transcript) move from reuse to extend (§6 rule 6). ~~The 17 skills~~ The 19 skills in §3 have status **new** (curriculum-ingest and print-render added 15 Oct 2026).

Every extension follows the same pattern:
- Replace `class_level ∈ {10,11,12}` with `level_ref`.
- Replace "one kind per subject" (RD-35, retired) with routing by slot type.
- Replace the vertical-only rule with the EPP aspect.
- Take persona, pacing, safety and thresholds from the EPP and the QA Profile, never from the skill's own text.

---

## 2. The 72 existing skills in v2

### 2.1 Super Teacher (ST)

| # | Skill | v2 | Stage | Output in v2 → owner role | Change |
|---|---|---|---|---|---|
| 1 | lesson-architect | extend | S4 lens | Review notes on the graph (lens only) | Architecture S4 "review lens". Its "assessment before hook" and "out-of-scope list" rules join graph-author's checklist. It never authors nodes. |
| 2 | conversational-script | retire | — | — | "Alternative openings" and "terminology after plain language" join super-teacher-scriptwriter's checklist |
| 3 | analogy-auditor | extend | S4 lens (ANL) | ANL review card | Its card fields are the ANL schema (`mapping`, `non_mapping`, `likely_misconception`, `formal_return`). It adds a `permitted_levels` judgement. |
| 4 | concept-humour | retire | — | — | `literal_science_risk` and `translation_risk` join humour-meme-director |
| 5 | interaction-designer | retire | — | — | Its prompt schema becomes interactive-teaching-director's output. Near-name hazard with interaction-design. |
| 6 | confidence-editor | extend | S7 lens | Feedback findings → persona-lint rule backlog | Architecture S7. Its error taxonomy feeds student-psychology-director. |
| 7 | voice-director | retire | — | — | "Unknown controls fail" moves to tts-provider-adapter; audition moves to stem-pronunciation. Near-name hazard. |
| 8 | language-editor | retire | — | — | Its rules (no demographic assumptions; translate the humour's function) join multilingual-director |
| 9 | science-reviewer | extend | S7 | Independent re-solve report → Q-FIX.answer_key evidence | Different agent and model from the author. Fixture families only (stem_fixture, quant_social, health dosage) |
| 10 | script-evaluator | extend | S7 pre-review, S14+ | Repetition ledger (owner, closing gap 14); script-stage pre-review; experiment plan → learning-evaluation | Output renamed from `release_review.md` (collision with VE release-review) |

### 2.2 Video Engine (VE)

| # | Skill | v2 | Stage | Output → owner | Change |
|---|---|---|---|---|---|
| 11 | source-ingest | extend | S1 | SRC records (copy hash, locators, `reliability_class`, rights) → **source-ingest** through the Source Registry (CE-48) | Single SRC writer; open-wiki and self-published-about-living checks happen at write time |
| 12 | curriculum-map | extend | S2 | Selected GUIDs + prerequisite edges for a scope → **curriculum-map** | Reads frameworks from cg-import; H-CG follows |
| 13 | claim-research | extend | S3, S4 | CLM node drafts with `source_refs` and spans → **claim-research**; independent answer-key solve → recorded in `ASM.answer_key_check` | claim-ledger validates and promotes the drafts. Answer keys move to `ASM.answer_key_check`: claim-research makes the first solve (method: fixture, solver or official scheme), independent of the creative ASM draft (INTERACTION §8; added 15 Oct 2026) |
| 14 | lesson-plan | retire | — | — | Superseded: graph content → graph-author (S4); 600 s plan and beat schedule → format-compiler (S5, R5) |
| 15 | super-teacher | extend | S6 entry | Stage handoff per Format Plan → **super-teacher** | Persona from the EPP; fills per slot; every sentence carries `node_ids[]` |
| 16 | analogy-humour | extend | S4 (ANL) / S6 (humour) | Stage entry for both | ANL drafting moves into the graph; humour stays at S6 under the persona humour ceiling; no memes at ac0 |
| 17 | interaction-design | extend | S4 (ASM drafts); S6 entry | ASM item drafts → submitted to graph-author; Cue[] with `answer_protection` → **interaction-design** | Windows from the Level Profile; response modes per level. At S6 binds and phrases only ASM nodes present in the Format Plan; a new question is a compile error routed to graph-author (added 15 Oct 2026) |
| 18–21 | science-math, -physics, -chemistry, -biology | extend | S3, S7, S11 | ScienceReport + fixtures → **science-<subject>** | The `stem_fixture` fixture library (the four validated models seed it); Q-FIX, A12a |
| 22 | storyboard-route | extend | S8 | SceneSpec routing per slot instance → **storyboard-route** | Routes by slot type × style × aspect. The "unsupported subject-kind" rule retires with RD-35 |
| 23 | svg-scenes | extend | S10 | Fixture-visual scene media → **svg-scenes** | 9:16 and 16:9 from the EPP; the 720×1280 renderer stays as preview profile and determinism oracle (CE-61) |
| 24 | manim-scenes | dormant | S10 | Equation/geometry inserts | Trigger: an active cell at l11_12+ with an approved Manim template |
| 25 | web-composition | extend | S10 | Composed artefact (chapters, EPP resolution) → **web-composition** | One engine; HyperFrames default (CE-L7) |
| 26 | blender-scenes | dormant | S10 | Spatial inserts | P2, opt-in, isolated |
| 27 | molecule-scenes | dormant | S10 | Structure scenes | Trigger: a chemistry lesson in an active stem_fixture cell (M3) |
| 28 | biology-scenes | dormant | S10 | Process scenes | Trigger: a biology lesson in an active cell (M3) |
| 29 | voice-direction | extend | S9 entry | Spoken segments, editorial tags → **voice-direction** | Locale Profile; persona delivery modes become the cue `voice` enum |
| 30 | voice-synthesis | extend | S9 | Audio assets stored by hash + job manifest → **voice-synthesis**; AD sentences voiced on the artefact's voice path (§6 rule 6) | Path A STS / Path B TTS from R1; refuses a Path B voice without a GL-voice pass; Q-NARR.voice_pin |
| 31 | alignment-localize | extend | S9–S10 | Localised SceneSpec, string tables keyed by node and cue ID → **alignment-localize** | REN nodes; rtl; no text baked into SVG paths (CE-39) |
| 32 | render-batch | extend | S10 | MP4/VTT/manifest → **render-batch**; reduced-motion variant (second render from the same closure with the style's `reduced_motion` tokens; §6 rule 6) | Pinned container, `-threads 1`, bitexact (CE-38); A2, A11 at the EPP resolution |
| 33 | visual-qa | extend | S11 | Frame defects → **visual-qa** | A12b, A13; feeds a11y-check |
| 34 | audio-caption-qa | extend | S11 | Media QA + corrected VTT → **audio-caption-qa** | Captions must equal the approved script (Q-A11Y.captions); cites anim-qa loudness |
| 35 | release-review | extend | S12 | Release evidence pack per QA Profile → **release-review** | Binds the EPP hash and closure hash; **never approves** |
| 36 | reel-repurpose | retire | — | — | Absorbed into format-compiler and `format/short` (Architecture S5; CE-60). "Recompose, never crop" becomes the compiler invariant Q-CLOSURE.recompose |
| 37 | thumbnail-package | extend | S14 | Title, cover, description → **thumbnail-package** | Q-META.package_truth, Q-COMM; neutral metadata |
| 38 | observability-cost | extend | all | Ledger: cost, capacity, provenance and licence rows → **observability-cost** | Cost per approved minute by format × level × family × locale × voice path (§9.2) |
| 39 | skills-security | reuse | admission | Approval record, pinned digest | Unchanged; admits every new skill below |
| 40 | learning-evaluation | extend | post-release | Pilot plan/results → **learning-evaluation**; `signal_proposal` ledger rows → **learning-evaluation** (level-2 interface, level-3+ operation, CE-117; added 15 Oct 2026) | Pre/post items from MIS diagnostic items [N74]; learner data stays in the platform. **Signal intake (15 Oct 2026):** reads aggregate `learning_signal` records (`../schemas/learning_signal.schema.json`; Architecture §9.7) keyed by artefact_sha256, asm_id, option_id or misconception_id and cue_id; rejects any record with a learner identifier or a cell below the O-3 minimum cohort (stricter for ac0 and ac1); treats `doubt_cluster_text` as untrusted data (§2.2). It never edits the graph: each signal becomes a proposal (raise a MIS priority, add a SIM, author a new MIS, queue an F15 doubt) submitted to graph-author at S4 and decided at GA-Graph, and each writes a `signal_proposal` ledger row. Accepted and rejected counts are a KPI from level 3 |
| 41 | asset-library | extend | S4, S10 | AssetManifest + MED nodes' file hashes → **asset-library** | Rights, generator ProviderJob, guardian release, map review link |
| 42 | selective-generation | reuse | S10 (optional) | Generated asset + job → **selective-generation** | "Zero generated seconds is allowed" |

### 2.3 Narration (NA)

| # | Skill | v2 | Stage | Output → owner | Change |
|---|---|---|---|---|---|
| 43 | super-teacher-scriptwriter | extend | S6 | Slot narration draft with `node_ids[]`; `ad_sentences[]` for each `visual_essential` beat whose meaning is not fully spoken (§6 rule 6) → **super-teacher-scriptwriter** | The only script author; register from the EPP persona |
| 44 | dialogue-naturalizer | extend | S6 | Minimal wording diff → **dialogue-naturalizer** | Must keep `node_ids`, literals, negations, direction words, conditions, signs and exponents (07/03 S5; SQ-20; 15 Oct 2026); closure-check re-runs after it |
| 45 | educational-storytelling | extend | S4 | ANL and STY beat drafts → submitted to graph-author | Every draft names `permitted_levels`; return-to-science line = `formal_return` |
| 46 | humour-meme-director | extend | S6 | Removable humour lines → **humour-meme-director** | Persona humour ceiling; no memes or trend audio at ac0 |
| 47 | student-psychology-director | extend | S6 | Feedback and progress text → **student-psychology-director** | Gentle forms for l1_2/l3_5; no unconditional praise |
| 48 | interactive-teaching-director | extend | S4 (ASM drafts); S6 | ASM item drafts (with interaction-design) → submitted to graph-author; Q/A segments, Pause nodes, hidden answers → **interactive-teaching-director** | Adopts the ST prompt schema; response modes per level [N10]. At S6 binds and phrases only ASM nodes present in the Format Plan; a new question is a compile error routed to graph-author (added 15 Oct 2026) |
| 49 | voice-acting-director | extend | S9 | Direction records → **voice-acting-director** | Path A performance direction; persona delivery |
| 50 | pacing-controller | extend | S9 | Measured durations, hold schedule → **pacing-controller** | Pacing from the Level Profile (CE-16); overruns route to the spec owner, never cut |
| 51 | stem-pronunciation | extend | S9 | Spoken/display/caption mappings per locale → **stem-pronunciation** | Locale spoken-math policy; Q-LOCALE.lexicon |
| 52 | multilingual-director | extend | S6 (REN drafts); S9 (locale narration support) | REN node drafts + back-check → submitted to graph-author; approved at GA-Δ for that locale (not GA-Graph; corrected 15 Oct 2026) | GL-glossary; Hinglish transliteration table |
| 53 | tts-provider-adapter | extend | S9 | Provider payloads → **tts-provider-adapter** | Pinned ModelProfile; refuses voices without licence or GL-voice |
| 54 | speech-animation-synchronizer | ~~reuse~~ extend | S9–S10 | Sample-index timeline, captions, `ad.vtt`, transcript (txt and json; display and spoken forms; `node_ids`) → **speech-animation-synchronizer** | Format-agnostic. Adds `ad.vtt` and the transcript from the measured timeline (§6 rule 6; status changed 15 Oct 2026) |
| 55 | audio-production-engineer | ~~reuse~~ extend | S9 (voice master); S10 (programme mix) | Voice master; programme mix (stems with gain automation, SFX bus, sum, normalise to −16 LUFS ±1 / ≤ −1 dBTP); `audio_described.m4a` → **audio-production-engineer** | ~~Unchanged~~ Owns the programme mix and re-master of `music/` stems and SFX (MUSIC §6); the 05 contract covers dialogue only. Mixes `audio_described.m4a` after the programme mix; A9 runs on it (§6 rule 6). Changed 15 Oct 2026 |
| 56 | narration-quality-reviewer | extend | S11 | Severity-ranked issues → **narration-quality-reviewer** | Q-NARR.asr_diff and critical_terms per locale |
| 57 | cost-regeneration-optimizer | reuse | S9 | Narration usage ledger → **cost-regeneration-optimizer** | Unchanged |

### 2.4 Advanced Animation (AN)

| # | Skill | v2 | Stage | Output → owner | Change |
|---|---|---|---|---|---|
| 58 | anim-brief | extend | S10 | brief.md → **anim-brief** | Reads the slot instance, style and aspect from the Format Plan and EPP |
| 59 | anim-qa | extend | S11 | anim_qa_report → **anim-qa** | A11 at the EPP resolution; severity text aligned (QA doc §11); flash thresholds from flash-analyser |
| 60 | anim-storyboard-gate | extend | S8 | Grid, beats, estimate → **anim-storyboard-gate** | Estimate per format × level × voice path; ac0 co-sign; one H-SB per Short |
| 61 | audio-analysis | reuse | S10 | Beat grid | — |
| 62 | audio-compose | extend | S10 | Stems, SFX → **audio-compose** | Child sonic-logo variant; `song_chant` in-house by default (O-7); startle-safe SFX at ac0 |
| 63 | cue-sheet | extend | S10 | cue_sheet.json → **cue-sheet** | `answer_protection` from the Format Plan's check slots; windows from the level |
| 64 | effort-governor | extend | all | Run config, effort log → **effort-governor** | `kit_cascade` family (13 D-16); ModelProfile pins per Kit cell |
| 65 | kinetic-typography | extend | S10 | Text layers → **kinetic-typography** | String tables; locale fonts; rtl; A8a/A8b |
| 66 | mcp-orchestrator | dormant | S8/S10 | Credit sub-ledger | Trigger: a founder-approved MCP provider (AD-34) |
| 67 | motion-harness | reuse | S10–S11 | Lint + determinism evidence | The contract applies to every format (A1, A3) |
| 68 | procedural-2d | extend | S10 | Illustrative scene code → **procedural-2d** | ac0-eligible styles; zero-flash transitions |
| 69 | reference-analyzer | reuse | S10 | Reference measurements | — |
| 70 | style-guides | extend | S8; GR (`style/`) | Style entries → **style-guides** | `aspects_supported`, `safety_classes_allowed`; 16:9 token set (O-19) |
| 71 | threejs-scenes | dormant | S10 | 3D inserts | Trigger: an active cell at l11_12+ with a 3D slot need |
| 72 | vertical-adapt | extend | S10 | Zone rectangles → **vertical-adapt** | Geometry for both aspects from the Format Spec |

---

## 3. New skills named by the architecture

Execution mode **D** is a deterministic script: no model call, so the same inputs give the same output. Mode **M** is model-backed through the Kit cascade (§5), with results stored by hash (CE-38).

| Skill | Stage | Purpose | Inputs → outputs | Output owner · maintainer | Edge cases | Exec mode |
|---|---|---|---|---|---|---|
| cg-import | S2 | Load or hand-author CASE-shaped frameworks [N46]–[N50] | Board syllabus files or a hand-authored YAML → `content/curriculum/<framework_id>.json` | **cg-import** · founder-engineer + academic owner (H-CG) | No board CASE feed (O-13): hand-author with internal GUIDs [N51]. ~~Never reuse a GUID across editions; use a `crosswalk_equivalent` association.~~ *(Corrected 15 Oct 2026, CE-111.)* GUIDs are minted as UUIDv5(UUIDv5(NS_URL, framework_id), human_code), so an item carried into a new edition keeps its GUID and re-ingesting the same syllabus mints no new GUIDs; `crosswalk_equivalent` links items across boards or frameworks. Every framework validates against `../schemas/curriculum_framework.schema.json` (P1-14) and carries `valid_academic_years[]` and, for board frameworks, `exam_windows[]` (CE-116, CE-122). Non-evaluative units [N36]. `nsqf_level` for voc (O-11) | D |
| graph-author | S4; S6 (REN writes only) | Compile approved claims into OBJ/CON/ANL/MIS/WRK/ASM/SIM/ACT/STY/VOC/TXT/MED nodes; the **only writer** of graph documents | Approved CLMs + drafts (ANL/STY from educational-storytelling; ASM from interaction-design and interactive-teaching-director; (S6) REN from multilingual-director) → `content/graphs/LG-<id>.json` + `graph_subtree_sha256` | **graph-author** · academic owner (GA-Graph) | Misconceptions authored first [N73]. ANL without `permitted_levels` is refused. A SIM must state `what_is_lost`. Model provenance (`model_id`, `effort`, `kit_version`) is required. Cross-graph conrefs. `real_child_likeness: false` | M (strong model offline as compiler, CE-L6) + D validation |
| claim-ledger | S3 | Apply ledger rules [N13]–[N19][N39]; move CLM status draft → machine_checked; run Q-LEDGER and Q-EXPIRY | CLM drafts + SRC + family profile → ledger report, status changes | **claim-ledger** · founder-engineer | ≥2 sources for exceptional/sensitive claims and for every claim in high-risk families. Contested needs attribution; board_vs_scholarship needs a recorded decision. Expiry → stale → revoked after grace. Source retraction is a revocation | D |
| citation-flag | S3, S7 | Mark sentences that need a citation [N41]–[N43]. **Only adds flags** (CE-28) | Draft or script sentences → flags with reason codes | **citation-flag** · founder-engineer | Hinglish code-mix and Indic sentences (recall per locale); robustness varies with source quality [N44]; uncertain means flag; recall/precision against reviewers is a KPI | M (cheap rung) |
| span-verify | S3, S7 | Confirm each quoted span exists in the registered copy | CLM `source_refs` + SRC copies → span report | **span-verify** · founder-engineer | NFC before matching; locator drift on a new edition triggers GV-claims; OCR copies flagged; conjunct-heavy Indic spans; `consulted_only` copies kept privately by hash | D |
| profile-resolver | S5, GR | Pure `resolve()` (R1–R12) → EPP; `qa_resolve()` → QA Profile | Content Request + registry snapshot + graph → EPP, QA Profile, or a named error | **profile-resolver** · founder-engineer | Subject in zero or two families (R3). Empty duration intersection. Overlay not allowed. No GL-voice voice means Path A. Every named reviewer unavailable means refuse. audio_only with an unnarrated visual-essential scene. Severity-lowering declarations | D |
| format-compiler | S5 | Select → requirements → grammar → budget → bind → Format Plan; emit v1 contracts; spec linter (CE-08) | EPP + graph → Format Plan (`format_plan_sha256`), LessonPlan/SceneSpec/NarrationPlan/ShortSpec views | **format-compiler** · founder-engineer (format/ registry) | Unmet requirement is a compile error naming the gap. Chapters ≤ 360 s. Determinism (same hash twice). Recompose, never crop. Derived formats add no node types. A locale's narration over budget routes to the spec owner | D |
| closure-check | S7 | CE-12 closure: sentence → node map; literals; SIM/ANL permission; contested phrasing; answer-hidden order | Script + sentence map + Format Plan → `qa/Q-CLOSURE.json` | **closure-check** · founder-engineer | Default-assertive: only deterministic templates mark a sentence non-assertive, and the flagger can only add. Numbers in words vs digits; spoken vs displayed units (RD-29); negations; Indic sentence segmentation; REN sentences map via `rendering_of` | D (flagger input M) |
| level-lint | S7 | Q-LEVEL: vocabulary, sentence length, new terms, on-screen text kind, response modes, think windows | Script + cue sheet + Level Profile → `qa/Q-LEVEL.json` | **level-lint** · academic lead | Cal values are report-only (CE-35). Missing controlled vocabulary lists (O-17). Single language at ac0. Prerequisite Repair uses the learner's own level register (R11) | D |
| persona-lint | S7 | Q-PERSONA: retired expressions, register, fake sensing, fake enthusiasm, humour ceiling | Script + persona entry → `qa/Q-PERSONA.json` | **persona-lint** · academic lead | A forbidden phrase quoted inside `misconception.confront` goes to a human. Exam Strategist register must be fear-free at ac1. Rules are versioned per persona. Optional cheap-model register triage is report-only | D (+ M triage) |
| safety-lint | S7, S11 | Q-SAFE: solicitation, links/QR/brands/CTAs, timers and pressure, activity safety, language at ac0 | Script, string tables, cue kinds, OCR of frames → `qa/Q-SAFE.json` | **safety-lint** · child-development reviewer (ac0 rules) + counsel (G-COUNSEL) | URLs spoken aloud; brand names inside textbook content go to a human; a neutral exam time plan is not a timer; locale CTA phrases (hi-IN, Hinglish, Assamese); "with a grown-up" cue present | D |
| flash-analyser | S11 | Q-FLASH and Q-SAFE.startle (visual), including spatial patterns (Q-FLASH.pattern, 15 Oct 2026); extends `flash_check.py` | Frames (both variants) + safety class + signed parameters → `qa/flash_report.json` | **flash-analyser** · production QA; ac0 parameters signed by the child-development reviewer (O-2) | Area threshold removed at ac0; red flash; tile grid parameter; 16:9 frames; spatial patterns (Q-FLASH.pattern, 15 Oct 2026); thresholds become final only after O-1 | D |
| a11y-check | S11 | Q-A11Y: contrast, CVD simulation, captions = script, transcript, reduced-motion, visual-essential and AD track; *(level-3+, 15 Oct 2026, CE-119, CE-120)* ASM option keys and screen-reader labels, print tag tree and reading order, and the `a11y/low_vision`, `a11y/cognitive`, `a11y/dyslexia` and `a11y/isl` rows when a request names them | Frames, captions, approved script, SceneSpec flags → `qa/Q-A11Y.json` | **a11y-check** · production QA | CVD thresholds pending O-20; locale captions vs REN text; spoken-math display vs spoken; textured backgrounds (paper collage); `ad.vtt` required when a visual is essential | D |
| impact-analyser | GR | Dependency index; affected set; impact preview (N approvals, M artefacts, K gate-minutes); canary selection | Registry diff + dependency index + ledger capacity rows → impact report, re-QA queue | **impact-analyser** · founder-engineer | Invalidation storms (batching); cross-graph conrefs; `legacy/v1` pins; reviewer lapse scoped by date; revocations queued first | D |
| v1-import | migration | CE-47 converter | ~~v1 LessonPlan/SceneSpec/ShortSpec/SourceRef/Claim + approvals → graph nodes (`author_kind: import`), `legacy/v1@1.0.0` pins, legacy approvals~~ v1 LessonPlan/SceneSpec/ShortSpec/SourceRef/Claim + approvals → SRC import records submitted to source-ingest (single SRC writer, CE-48); graph-node import drafts (`author_kind: import`, `import_ref`) submitted to graph-author (deterministic validation path, no model call); `legacy/v1@1.0.0` pin manifest (entries released through GR); a legacy-approval wrap manifest (v1 approval record + artefact sha256 + script bundle hash) submitted to the approval service, which alone writes each legacy approval and its `legacy_closure_hash` (corrected 15 Oct 2026: §6 rules 2 and 3) | **v1-import** (drafts and manifests only) · founder-engineer | Spans without a copy hash become `machine_checked`; idempotent re-import; voice assets without a licence are not admitted; the 54 scene packages become Kit fixtures, never releasable | D |
| packaging-export | S14 | Neutral exporter (Architecture §4 S14): builds the Distribution Package and every channel deliverable from the approved master and runs the export checks (PACKAGING §11). Added 15 Oct 2026 | Approved master + GF/GS records + EPP + `packaging/` profile + approved script, captions, transcript, AD track + thumbnail-package copy → Distribution Package (`content/packages/PKG-<id>.json`), renditions with `derived_from_sha256`, neutral sidecar, captions, transcript, AD track, C2PA sidecar manifest; export QA report (Q-META.hash_bind, sidecar_complete, chapters, size; Q-COMM.sidecar, copy; Q-DISC.placement evidence; Q-A11Y.captions packaged; A9.package; A11.package; A4.platform; A8a copy; Q-SAFE.no_external_prompts copy) | **packaging-export** · founder-engineer + publisher (`packaging/` registry) | A distribution-only change (copy, sidecar, chapters mode) re-exports without reopening the full-watch gate; a bytes change goes back through render (PACKAGING §1). Never strips C2PA; ships the sidecar manifest that references the master hash (PACKAGING §7). Platform insets and size limits are measured or marked verify, never assumed. Q-DISC.placement needs the publisher's per-platform confirmation; the skill records it and never asserts it. Locale captions and transcripts must match the REN text. RELEASE-CHECK stays with the approval service. Never approves | D |
| kit-verify | S10, S11, GR | The Kit verifiers no other skill owns: V0 semantic slot validator, V6 keyframe judge, V7 SSIM against golden frames (13 §2.4); Kit regression; 5% shadow-audit sampling. Added 15 Oct 2026 | Slot JSON + approved script hash + cue IDs (V0); 6-keyframe contact sheets (V6); rendered frames + the archetype's golden frames (V7); frozen eval set + ModelProfile or Kit diff (regression) → V0/V6/V7 verdicts, golden-frame store, Kit regression report, CAPABILITY_LEDGER evidence rows (13) | **kit-verify** · founder-engineer | V1/V3 stay with motion-harness and V2/V4/V5 with anim-qa (06 "Kit verifiers" cluster, amended here). Golden frames are re-baselined only through GR. V6 blocks only on questions calibrated per QA_PROFILES §6 and otherwise flags; Sonnet audits 10% of scenes plus every disagreement. A ModelProfile or Kit bump queues Kit regression for every affected Kit cell (Architecture §3.6; M1 production-class drill). The 54 v1 scene packages are regression fixtures, never releasable. Never approves | D (V0, V7, regression) + M (V6: Haiku vision, Sonnet audit) |
| curriculum-ingest | S1 (candidates); consumed at S2 by cg-import and gated at ⛔ H-CG | Turn a board syllabus PDF into candidate Curriculum Framework items with provenance. Level-1, CE-111; added 15 Oct 2026 | Syllabus PDF registered as an SRC (`reliability_class: official_curriculum`, via source-ingest) → candidate items {human_code, kind, statement, parent, associations, `source_span` {source_id, locator, span_sha256}} with GUIDs minted by the CE-111 rule; validated against `../schemas/curriculum_framework.schema.json`; submitted to cg-import, which alone writes `content/curriculum/<framework_id>.json` after H-CG | **curriculum-ingest** (candidates only) · academic owner (H-CG) + founder-engineer; validates `framework/` | The syllabus text is untrusted data in any model prompt (Architecture §2.2). Re-ingesting the same edition must return the same GUIDs (UUIDv5 over the edition-independent `human_code`); a changed `human_code` is a framework-diff row (Architecture §3.6, CE-116), never a silent re-mint. Every candidate carries a `source_span`; a candidate without one is refused. Scanned PDFs: OCR copies flagged as in span-verify. Indic-script syllabi: NFC before span hashing. Nothing enters `content/curriculum/` until H-CG. Never approves | M (candidate extraction) + D (schema, span hash, GUID mint) |
| print-render | S10 | Render `render_target: print` artefacts: a tagged PDF/UA plus an HTML twin from the same Format Plan through the pinned Chrome print path. Level-3+, CE-119; added 15 Oct 2026 | Format Plan + approved script and string tables + graph nodes in the closure (ASM keys, WRK, MIS, ANL, ACT) + `style/` print tokens + `harness/` Chrome pin + `packaging/print-pdf` `print_variant` → the print PDF, the HTML twin and the answer key as a separate file or final section; `artefact_sha256` per file | **print-render** · founder-engineer | Deterministic: vendored fonts, fixed document metadata, no wall-clock timestamps, so Q-DET applies. Answers never on the question page. Every `visual_essential` element needs a text alternative in the tag tree (the print counterpart of R10). F-GN (AC0): no links, QR codes, data requests or calls to action (Q-SAFE). File-size limit is `verify`. a11y-check runs Q-A11Y.print_structure on the output; GF reviews the PDF page by page. Never approves | D |

The fixture library and the Kit `examleaf-fill-<archetype>` skills remain as 13 proposed them. They are not in the 72, they are not counted here, and they are added only after arm C4 passes (06 README addendum).

---

## 4. Kit slot vocabulary mapping

**Ownership.** Each slot type has one **slot owner**: the scene skill that holds its code module, tests, Kit template and A-check (Architecture §5.2). The **script filler** writes the narration for the beat (except K-rung slots once their text arm passes; see the note under the table). An **alternate renderer** may render a slot instance when routed, but never owns the slot's module, tests, Kit template or A-check (corrected 15 Oct 2026). Extenders add sub-artefacts. The Kit archetype numbers follow 13 §3.2:
1. hook/title card
2. definition/key-term card
3. labelled-fixture reveal
4. formula derivation step-reveal
5. worked numerical
6. graph/plot from fixture data
7. chemical equation balancing
8. recap/quiz pause-and-reveal

Fixture-visual archetypes (3, 6) route to svg-scenes or manim-scenes, never to HyperFrames templates (13 §2.3).

| Slots | Script filler → extenders | Script entry rung (SCRIPTING §16) | Kit archetype | Slot owner (visual; exactly one) | Alternate renderers / extenders | Key checks |
|---|---|---|---|---|---|---|
| hook.realworld, hook.surprise | super-teacher-scriptwriter → dialogue-naturalizer | S | 1 | kinetic-typography | procedural-2d (illustration); asset-library (MED) | A5 headline hold, Q-CLOSURE |
| hook.question_reveal | scriptwriter → interactive-teaching-director | H | 1, 8 | kinetic-typography | — | Q-INT.reveal_order |
| explain.ladder_step | scriptwriter | S | 3, 6 | svg-scenes | procedural-2d (illustrative) | A7, A12b |
| explain.definition | scriptwriter | S | 2 | kinetic-typography | — | A7 display text |
| explain.analogy | scriptwriter (reads the ANL drafted by educational-storytelling) | S | — (proposed 11) | procedural-2d | — | Q-CLOSURE.sim_anl; `non_mapping` spoken |
| explain.derivation_step | scriptwriter | O at l11_12, ug, pg; below l11_12 §16 sets no rung (verify) | 4 | svg-scenes | manim-scenes (alternate adapter when active) | Q-FIX, A7 |
| worked.step, worked.faded_twin | scriptwriter → interactive-teaching-director (pause per step) | H (step); S (faded_twin) | 5, 7 | svg-scenes | manim-scenes (alternate adapter when active) | Q-FIX, Q-INT.window_length |
| check.interpolated, check.predict, check.retrieval | interactive-teaching-director → student-psychology-director | H | 8 | kinetic-typography | — | Q-INT.*, A10 |
| misconception.elicit, misconception.retest | scriptwriter → student-psychology-director (gentle at ac0) | S | 8 | kinetic-typography | — | Q-INT, F7 "ends on correct model" |
| misconception.confront | scriptwriter | S | 3, 6 | svg-scenes | procedural-2d | A12b; wrong model shown by shape and label, not colour alone |
| recap.retrieval, recap.statement | interactive-teaching-director / scriptwriter | H (retrieval); K (statement) | 8, 2 | kinetic-typography | — | Q-INT, Q-CLOSURE |
| card.front, card.back | interactive-teaching-director | H (front); K (back) | 2, 8 | kinetic-typography | — | Q-INT.window_length |
| marking.scheme, exam.pattern, exam.time_plan | scriptwriter (Exam Strategist register) | K (marking.scheme, exam.pattern); H (exam.time_plan) | — (proposed 12) | kinetic-typography | — | Q-FIX.answer_key, Q-EXPIRY, Q-SAFE.no_timers |
| compare.dimension | scriptwriter | H | — (proposed 9) | svg-scenes | — | Q-A11Y.cvd |
| activity.setup, activity.do, activity.observe, activity.safety_cue | scriptwriter → voice-acting-director (Path A real demos) | H (setup, do, observe); S (safety_cue) | — (proposed 13) | kinetic-typography | asset-library (MED footage) | Q-SAFE.activity |
| story.beat, story.song_chant | scriptwriter (Junior) → audio-compose (song) | S (beat); K (song_chant) | — (proposed 11) | procedural-2d | — | Q-CLOSURE (beat carries CLM/SIM), Q-RIGHTS |
| qa.doubt_statement, qa.answer | scriptwriter | K (doubt_statement); S (answer) | 1, 2 | kinetic-typography | — | Q-SAFE.no_solicitation |
| source.show, source.read, source.interpret | scriptwriter → multilingual-director (TXT renderings) → speech-animation-synchronizer (read-along highlight) | K (show, read); S (interpret) | — (proposed 10) | kinetic-typography | — | Q-RIGHTS, Q-LEDGER.contested |
| perspective.position | scriptwriter | O | — (proposed 9/10) | kinetic-typography | — | Q-LEDGER.contested |
| map.node, map.link | scriptwriter (nodes and edges supplied by format-compiler; nothing inferred) | K | — (proposed 14) | svg-scenes | — | Q-CLOSURE, Q-A11Y.cvd |
| viva.prompt, viva.model_answer | interactive-teaching-director / scriptwriter | H (prompt); S (model_answer) | 8 | kinetic-typography | — | Q-INT |
| teach.move | scriptwriter (Colleague) | S | 2, 8 | kinetic-typography | — | Q-CLOSURE |
| chapter.title, bridge.return_link, close.next_step | scriptwriter | K (chapter.title); H (bridge.return_link, close.next_step) | 1 | kinetic-typography | — | Q-CLOSURE |

**Script entry rungs** (columns and note added 15 Oct 2026, from SCRIPTING §16). Any beat on a contested or sensitive claim enters at O whatever its slot. The disclosure line is also K. Until the cell's text arms T0–T3 pass, every slot is Sonnet-authored, Opus-reviewed and Haiku-routed (13 §5.6). After that, K-rung slots are filled at S6 by the slot's Kit template with no model call (`cascade_rung: K`; validators only). The script filler named here never writes or rewrites them, and dialogue-naturalizer does not edit them.

**Proposed archetypes 9–14** [Recommendation]: (9) side-by-side comparison, (10) source-document reveal, (11) illustrative/story beat, (12) table/pattern card, (13) footage-with-labels overlay, (14) map build. Until each one passes the 13 protocol (dev set, sealed holdout, arm C4), its slots are routed as `UNKNOWN`. That means cascade rung 3 through the Kit, or a human-authored template, and never a Haiku fill. Today the eight qualified-to-be archetypes cover only the STEM text-card, symbolic and fixture families. 17 of the 43 slots have no archetype.

---

## 5. Cascade per task type

~~Strong models (Fable 5.1, Opus 5.5) run **offline only**, as compilers, template and rule authors, and judges' rubric designers (CE-L6).~~ Fable 5.1 runs offline only. Opus 5.5 runs offline as compiler, template and rule author and judge-rubric designer, and online only as cascade rung 3, the claim-drafting and REN escalation, and the slot-narration reviewer until T0–T3 pass (CE-L6; 13 §2.2 allows Opus as the third cascade rung; corrected 15 Oct 2026). Ultracode is refused in production; the one attended $50 probe is the only exception (CE-L3). ~~Every call pins the full model ID and an explicit effort.~~ Every call pins the full model ID and an explicit effort from the `model/` ModelProfile for its Kit cell; no call relies on a surface default (Sonnet 5.5 defaults to high on the API and medium in Claude Code, 07/09 §4.1). Scene-fill efforts follow 13 §5.8; Haiku efforts come from the C3 sweep, starting at medium (13 §2.5). (Corrected 15 Oct 2026.) Kit cells are separate per (format family × subject family × level band) (R12, CE-50).

| Task type | Author rung | Reviewer | Escalation | Strong model role | Never |
|---|---|---|---|---|---|
| Citation flagging (S3, S7) | Haiku 5.5 | claim-ledger (D); GV-claims (human) | An uncertain flag stays | Writes and evaluates the flag rubric | Removing a flag; acting as a source |
| Claim drafting (S3) | Sonnet 5.5 via the Kit, with source spans | span-verify, claim-ledger, GV-claims | Opus 5.5 | — | Model knowledge as a source |
| Graph authoring (S4) | Fable 5.1 / Opus 5.5 offline; humans edit | GA-Graph | — | Compiler | Shipping a node without GA-Graph |
| Resolve, compile, lint (S5, S7, S11) | Deterministic code | — | Compile error → spec owner | — | Any model call |
| Slot narration (S6) | ~~Sonnet authors, Opus reviews, Haiku routes, **until** text arms T0–T3 pass; then Haiku authors and Sonnet reviews (13 §5.6)~~ Until T0–T3 pass for the Kit cell: Sonnet authors, Opus reviews, Haiku routes. After: the per-slot entry rung from SCRIPTING §16 (K: Kit deterministic fill, validators only; H: Haiku with Sonnet review; S: Sonnet with Opus review; O: Opus with human review at GA-Δ); see §4 (corrected 15 Oct 2026) | closure-check, persona-lint, level-lint, safety-lint; GA-Δ | Opus 5.5 | Authors slot schemas and negative cards | Free on-screen text (only `text_ref` to the approved script) |
| Locale renderings (REN) | Sonnet 5.5 [Recommendation] | Native editor; GL-glossary | Opus 5.5 | — | Haiku before a locale text arm qualifies |
| Scene slot fill (S10) | Haiku 5.5 → Haiku xhigh → Sonnet 5.5 medium → Opus 5.5 medium/high → human ticket. Caps $0.02 / $0.25 / $0.60 per scene; circuit breaker at > 20% escalation per lesson (13 §5.3, §5.8) | V0–V7, then the A-suite | Triggers in 13 §5.4; `UNKNOWN` goes to cascade rung 3 | Templates, verifier rules; 5% shadow audit | Free animation code; times, colours or fonts |
| Keyframe judge V6 (**kit-verify**) | Haiku 5.5 vision | Sonnet 5.5 audits 10% + every disagreement | Sonnet if image input fails | Calibration rubric | Approving (QA doc §6) |
| Register triage | Haiku 5.5, report-only | persona-lint rules | — | — | Blocking alone |
| Human gates | Humans only | — | — | — | Any model verdict |

---

## 6. Ownership rules

1. **One owner per output** (msg 10 §6). The owner emits `handoff.json`. Extenders write named sub-artefacts only. Lenses write review notes only. Retired skills write nothing in the engine.
2. **graph-author is the only writer of graph documents.** Other skills submit drafts:
   - claim-research → CLM drafts
   - educational-storytelling → ANL and STY drafts
   - multilingual-director → REN drafts
   - interaction-design (+ interactive-teaching-director) → ASM item drafts (item_kind, stem, options, hints, feedback, MIS links) at S4 (added 15 Oct 2026)
   - claim-research → independent answer-key solve recorded in `ASM.answer_key_check` (method: fixture, solver or official scheme) at S3/S4 (added 15 Oct 2026)
   - v1-import → import drafts (SRC to source-ingest; nodes to graph-author) (added 15 Oct 2026)
   source-ingest is the only SRC writer (CE-48).
3. **No skill writes approvals or release decisions.** That is the approval service (07/06 §6.3). Every QA skill runs as the independent-reviewer identity, never the author's. This includes legacy approvals: v1-import emits only the wrap manifest (added 15 Oct 2026).
4. **Registry ownership:**

| Registry | Validating skill | Human owner |
|---|---|---|
| format/ | format-compiler (linter) | founder-engineer |
| slot/ | the slot owner in §4 (+ ADR) | founder-engineer |
| level/ | level-lint | academic lead |
| overlay/ | claim-ledger (expiry) | academic lead |
| safety/ | safety-lint, flash-analyser | child-development reviewer + counsel |
| a11y/ | a11y-check | production QA |
| framework/ (level-1, CE-111; added 15 Oct 2026) | curriculum-ingest (candidates); cg-import (writes after H-CG) | academic owner |
| persona/ | persona-lint | academic lead |
| family/ | claim-ledger + science-* | academic lead |
| locale/ | multilingual-director, stem-pronunciation | native editors |
| style/ | style-guides | founder-engineer |
| voice/ | voice-synthesis | founder (licence evidence) |
| model/, kit/ | effort-governor (reads CAPABILITY_LEDGER, written from kit-verify evidence, to set per-cell model rung and effort) | founder-engineer |
| harness/ | motion-harness, render-batch | founder-engineer |
| reviewer/ | none (approval service) | academic lead |
| ~~qa/ (proposed)~~ qa/ | profile-resolver | founder-engineer |
| music/ | audio-compose (entry validation; deterministic music resolution, MUSIC §2.1) | audio lead (registry, mix) + founder (commissions, licences) + child-development reviewer (AC0 entries) |
| lex/ | stem-pronunciation | native editors + academic owner |
| gs/ | voice-synthesis (GL-voice runner) | native editors + narration lead |
| packaging/ | packaging-export | founder-engineer + publisher |

Rows for `music/`, `lex/`, `gs/` and `packaging/` added and `qa/` confirmed 15 Oct 2026 (Architecture §3.1 addendum, CE-63).

5. **Activate an owner and its extenders together, never an extender alone.** Examples: anim-qa with visual-qa; cue-sheet with speech-animation-synchronizer; a fill skill with its scene owner.
6. **Accessibility deliverables** (added 15 Oct 2026; PACKAGING §10). a11y-check verifies them; these skills produce them:
   - **AD text.** super-teacher-scriptwriter authors `ad_sentences[]` (each with `node_ids[]`) at S6 for every beat with `visual_essential: true` whose meaning is not fully spoken. closure-check covers them at S7 and they are shown at GA-Δ. (Needs the `ad_sentences[]` field in `schemas/script_spec.schema.json`.)
   - **AD audio.** voice-synthesis voices the AD sentences at S9 on the artefact's voice path. audio-production-engineer mixes `audio_described.m4a` at S10 after the programme mix (description clips count as speech for ducking, MUSIC §6), and A9 runs on it.
   - **`ad.vtt` and the transcript** (txt and json, with display and spoken forms and `node_ids`): speech-animation-synchronizer, from the measured timeline, at S9–S10.
   - **Reduced-motion variant.** render-batch at S10 renders a second time from the same closure with the style's `reduced_motion` tokens; motion-harness A1/A3 and the A-suite run on it (Q-A11Y.reduced_motion).

### 6.1 Near-name hazards (added for v2)

| Pair | Risk | Rule |
|---|---|---|
| closure-check / RELEASE-CHECK "closure hash" | "Closure" means derivation closure (CE-12) in one and the approval input closure (§3.7) in the other | closure-check never computes approval hashes. The approval service never maps sentences |
| claim-ledger / claim-research | Two claim writers | research drafts; the ledger validates and promotes |
| cg-import / curriculum-map | Framework vs scope | import builds frameworks; map selects GUIDs for a scope |
| format-compiler / web-composition | "compile" vs "compose" | The compiler writes plans and never renders; composition never selects nodes |
| graph-author / lesson-architect / lesson-plan (retired) | Three planners | Only graph-author writes |
| persona-lint / confidence-editor | Same phrases | The lint blocks; the editor is a lens |
| level-lint / pacing-controller | Pacing | The lint checks planned text; pacing-controller measures audio |
| safety-lint / skills-security | "Security" vs "safety" | Content vs software admission |
| flash-analyser / anim-qa `flash_check.py` | Two flash verdicts | flash-analyser extends the script and owns the Q-FLASH verdict; anim-qa cites it |
| a11y-check / visual-qa / audio-caption-qa | Contrast and captions | a11y-check owns the Q-A11Y verdict and reads their measurements |
| impact-analyser / observability-cost | Ledger reads | impact-analyser owns re-QA queues; observability-cost owns money |
| Existing pairs (06 OVERLAP): interaction-design / interaction-designer, voice-direction / voice-director | Mis-trigger | ST members retired in the engine |

---

## 7. Activation matrix

### 7.1 By maturity level (Maturity Roadmap §1)

● active · R report-only · ○ dormant · ✕ retired in the engine. ST rows corrected and added 15 Oct 2026 (06 OVERLAP: near-name ST skills are never installed beside their VE/NA owners).

| Skill group | L0 | L1 | L2 (M1) | L3 | L4 | L5 |
|---|---|---|---|---|---|---|
| VE/NA/AN in v1 procedures (07/03, 07/05) | ● | ● | ● (now compiled from the graph) | ● | ● | ● |
| lesson-plan, reel-repurpose | ● | ● | ✕ | ✕ | ✕ | ✕ |
| ST conversational-script, concept-humour, interaction-designer, voice-director, language-editor | ~~lens~~ rules in owner checklists; standalone ST kit only (not installed in the engine; 06 installation hazards) | ~~lens~~ same | ✕ | ✕ | ✕ | ✕ |
| ST science-reviewer (independent re-solve), script-evaluator (repetition ledger, pre-review), confidence-editor (S7 lens) | ● | ● | ● | ● | ● | ● |
| ST lesson-architect, analogy-auditor (S4 lenses on graph-author output) | rules in lesson-plan / educational-storytelling checklists (06 §1, §4) | same | ● | ● | ● | ● |
| v1-import, impact-analyser, profile-resolver (registry validation) | ○ | ● | ● | ● | ● | ● |
| cg-import, graph-author, claim-ledger, citation-flag, span-verify, format-compiler, closure-check, packaging-export | ○ | ○ | ● | ● | ● | ● |
| curriculum-ingest (level-1, CE-111; added 15 Oct 2026) | ○ | ○ | ● when a syllabus PDF is ingested (M1 may hand-author through cg-import) | ● | ● | ● |
| print-render (level-3+, CE-119; added 15 Oct 2026) | ○ | ○ | ○ | ● when a request sets `render_target: print` | ● | ● |
| learning-evaluation `signal_proposal` intake (CE-117; added 15 Oct 2026) | ○ | ○ | interface only (schema and ledger row type; no signals yet) | ● | ● | ● |
| kit-verify [Recommendation] | ○ | ○ | ● (Kit regression on the v1 fixtures; V0, V7) | ● (V6 with the Kit fill) | ● | ● |
| level-lint, persona-lint | ○ | ○ | R | R | R → blocking per level after its pilot | same |
| safety-lint (ac1 rules), flash-analyser (WCAG floor), a11y-check | ○ | ○ | ● (CVD R) | ● | ● | ● |
| Kit fill archetypes 1–8 | ○ | ○ | ○ | ● once arm C4 passes | ● | ● |
| molecule-scenes, biology-scenes | ○ | ○ | ○ | ● on route | ● | ● |
| claim-ledger humanities validators; proposed archetypes 10, 12 | ○ | ○ | ○ | ○ | ● | ● |
| multilingual-director at scale (hi-IN, Hinglish REN), GL-glossary | ○ | ○ | ○ | ○ | ● | ● |
| safety-lint ac0 rules, flash-analyser ac0, audio-compose child variant, procedural-2d ac0 styles | ○ | ○ | ○ | ○ | ○ | ● after O-1–O-4, O-7, G-COUNSEL |
| 16:9 vertical-adapt/style-guides tokens, manim-scenes, threejs-scenes | ○ | ○ | ○ | ○ | ○ | ● after O-19 |
| mcp-orchestrator, blender-scenes | ○ | ○ | ○ | ○ | ○ | on approval |

### 7.2 By cell (format family × subject family × level band) [Recommendation]

The architecture names cells but does not define "format family". The working grouping used here is:
- **long:** F1, F6, F12, F14, F19, F20, F21, F23
- **short:** F5, F11
- **derived-mid:** the other derived formats
- **composition:** F16
- **educator:** F26

| Cell | Opens at | Skills added beyond the core |
|---|---|---|
| long × stem_fixture × l9_10–l11_12 | M1 | science-physics (+ math), svg-scenes, Path A STS chain |
| short × stem_fixture × l9_10–l11_12 | M1 | vertical-adapt, anim-storyboard-gate per Short |
| derived-mid × stem_fixture × l9_10–l11_12 | M3 | interactive-teaching-director heavy; archetype 8 |
| long/derived × humanities_citation × l9_10 | M4 | claim-ledger family validators, span-verify on scholarly sources, sensitivity reviewer; archetypes 10, 12 |
| any × stem/humanities × l6_8 | M4 | persona Coach rules in persona-lint |
| long/short × stem_fixture/languages × l1_2–l3_5 (ac0) | M5a | safety-lint ac0, flash-analyser ac0, audio-compose, procedural-2d, archetype 11; F23 adds speech-animation-synchronizer read-along |
| long (16:9) × stem_fixture × ug–pg | M5b | vertical-adapt 16:9, manim-scenes, threejs-scenes |
| assessment × exam_strategy × l9_10–adult_prof | M5b | claim-ledger `pattern_recompute`, expiry |
| long × vocational × voc | M5b (O-11) | procedure fixtures, safety reviewer, archetype 13 |
| educator × any × educator | M5 | persona Colleague |

---

## 8. Firing order v2 (stage map)

Same style as `06_skills_library/SKILLS_PIPELINE_STAGE_MAP.md`. ⛔ marks a human gate. QA skills never approve.

| # | Stage | v2 stage | Fires, in order | Output artifact → **owner** | Basis |
|---|---|---|---|---|---|
| 1 | Ingest | S1 | source-ingest → curriculum-ingest (when a syllabus PDF is ingested; 15 Oct 2026, CE-111) | SRC records → **source-ingest**; candidate framework items → **curriculum-ingest** | Architecture S1, CE-48, CE-111 |
| 2 | Curriculum | S2 | (curriculum-ingest candidates →) cg-import → curriculum-map → ⛔ H-CG | Framework → **cg-import**; scope GUIDs → **curriculum-map** | S2 |
| 3 | Claim ledger | S3 | claim-research → citation-flag → span-verify → claim-ledger → science-<subject> (fixture families) → ⛔ GV-claims | CLM drafts → **claim-research**; ledger state → **claim-ledger**; fixtures → **science-<subject>** | S3 |
| 4 | Lesson Graph | S4 | educational-storytelling (ANL/STY drafts) · interaction-design + interactive-teaching-director (ASM item drafts) · claim-research (independent answer-key solve → `ASM.answer_key_check`) → graph-author · lenses: lesson-architect, analogy-auditor → ⛔ GA-Graph | Graph + subtree hash → **graph-author** | S4 |
| 5 | Format derivation | S5 | profile-resolver → format-compiler | EPP + QA Profile → **profile-resolver**; Format Plan → **format-compiler** | S5 |
| 6 | Script | S6 | super-teacher (entry) → super-teacher-scriptwriter → interactive-teaching-director → student-psychology-director → humour-meme-director (optional) → dialogue-naturalizer · Kit cascade per slot · multilingual-director (REN drafts per locale, including TXT renderings for source.* slots) → graph-author (writes the REN nodes; GA-Graph is not reopened, Architecture §3.6 REN row) → approved per locale by the native editor at GA-Δ | Slot narration + `ad_sentences[]` → **super-teacher-scriptwriter**; Cue[] → **interaction-design**; REN nodes → **graph-author** | S6, mapping |
| 7 | Validation | S7 | closure-check → citation-flag (script) → span-verify → level-lint → persona-lint → safety-lint → science-<subject> re-run → ST science-reviewer (re-solve) · lens: confidence-editor, script-evaluator pre-review → ⛔ GA-Δ (+ child-dev co-sign at ac0; native editor per locale) | `qa/Q-CLOSURE`, `Q-LEVEL`, `Q-PERSONA`, `Q-SAFE` → their linters | S7 |
| 8 | Storyboard | S8 | effort-governor → storyboard-route → style-guides → anim-storyboard-gate → observability-cost reserve → ⛔ H-SB | Routing → **storyboard-route**; grid + estimate → **anim-storyboard-gate** | S8, RD-46 |
| 9 | Narration | S9 | voice-direction (entry) → multilingual-director (locale lexicon and back-check) → voice-acting-director → stem-pronunciation → pacing-controller (estimate) → cost-regeneration-optimizer → voice-synthesis (incl. AD sentences) → tts-provider-adapter → audio-production-engineer (voice master) → pacing-controller (measure) → speech-animation-synchronizer → ⛔ VOICE | Audio by hash → **voice-synthesis**; voice master → **audio-production-engineer**; timeline, `ad.vtt`, transcript → **speech-animation-synchronizer** | S9 |
| 10 | Animation and composition | S10 | ~~cue-sheet → anim-brief → Kit fill (cascade) → svg-scenes / kinetic-typography / procedural-2d (/ manim, molecule, biology, threejs when active) on motion-harness → audio-compose → alignment-localize → web-composition → vertical-adapt → render-batch~~ vertical-adapt (zone rectangles for the EPP aspect) → cue-sheet (requests only the bed roles the format allows, MUSIC §2.1) → audio-compose (beds per resolved `music/`; SFX named in cue sheet `sfx[]`) → audio-analysis (beat grid, if a bed exists; merged into the cue sheet) → anim-brief → Kit fill (cascade; kit-verify V0 per fill) → svg-scenes / kinetic-typography / procedural-2d (/ manim, molecule, biology, threejs when active) on motion-harness → audio-production-engineer (programme mix per MUSIC §6: voice master → stems with gain automation from the narration timeline → SFX bus → sum → normalise to −16 LUFS ±1 / ≤ −1 dBTP; then `audio_described.m4a` when required) → alignment-localize → web-composition → render-batch (mux; A9/M4 re-measured on the final mux; reduced-motion variant from the same closure). Order corrected 15 Oct 2026. *Print branch (`render_target: print`; level-3+, CE-119, 15 Oct 2026):* no narration, cue sheet, music or motion; print-render renders the PDF/UA, HTML twin and answer key from the Format Plan, and S11 runs a11y-check (Q-A11Y.print_structure) and safety-lint on the pages | Scene media → slot owner (§4); programme mix + `audio_described.m4a` → **audio-production-engineer**; artefact → **web-composition**; MP4 + reduced-motion variant → **render-batch** | S10 |
| 11 | QA | S11 | motion-harness (A1, A3) → anim-qa → flash-analyser → visual-qa → a11y-check → safety-lint (frames) → audio-caption-qa → narration-quality-reviewer → ~~V6 judge (triage only)~~ kit-verify V6 (triage only; calibrated per QA_PROFILES §6) and V7 (flags) | Verdicts → each check's owner (QA doc §2) | S11, CE-35 |
| 12 | Approvals | S12 | release-review (evidence pack) → ⛔ GF or GS (+ co-signs) → ⛔ DISCLOSURE | Evidence → **release-review**; approvals → approval service | S12, RD-45 |
| 13 | Release check | S13 | approval service RELEASE-CHECK (automated) | Release manifest → approval service | S13 |
| 14 | Export | S14 | thumbnail-package → ~~neutral exporter~~ packaging-export (PACKAGING §11: Q-META, Q-COMM, Q-DISC, Q-A11Y.captions packaged, A9.package, A11.package, A4.platform) | ~~Sidecar, captions, transcript, AD track → exporter~~ Distribution Package (`content/packages/PKG-<id>.json`), sidecar, captions, transcript, AD track, C2PA sidecar manifest → **packaging-export** | S14 |
| — | Registry change | GR | impact-analyser → profile-resolver re-resolves with the superseded entry replaced by its current version, even when the request named a version (Architecture §3.6 Re-resolution; 15 Oct 2026) → runner re-QA (canary first); kit-verify Kit regression for `model/` and `kit/` changes | Impact report + queue → **impact-analyser** | §3.6, CE-34 |
| — | Throughout | — | observability-cost ⇄ cost-regeneration-optimizer; effort-governor; asset-library; skills-security (admission); learning-evaluation (pilots; `signal_proposal` intake from aggregate `learning_signal` records → graph-author at S4, CE-117); v1-import (migration) | Ledgers → **observability-cost**; `signal_proposal` rows → **learning-evaluation** | §4 cross-cutting |


### 8.1 Stage id crosswalk (v2 → 07/03) (added 15 Oct 2026)

v2 renumbers the stages. 07/03, 07/09 §5 and the other 07 documents keep the old numbers, so a bare "S9" is ambiguous outside this folder. The CSV column is `stage_v2`.

| v2 | 07/03 equivalent |
|---|---|
| S1 | 07 S1 |
| S2 | 07 S2 |
| S3 | 07 S3 (+ claim-level fixture checks from 07 S7) |
| S4 | 07 S4 (+ analogy cards from 07 S6) + new GA-Graph |
| S5 | new (absorbs the 07/05 SH ShortSpec and reel-repurpose) |
| S6 | 07 S5 + S6 |
| S7 | 07 S7 (07 GA becomes GA-Δ) |
| S8 | 07 S8 + H-SB |
| S9 | 07 S10 |
| S10 | 07 S9 + S11 + S12 |
| S11 | 07 S13 |
| S12 | 07 GF (+ 07/05 GS) + DISCLOSURE (07/06 §6.4) |
| S13 | 07/06 §6.3 release check, now a stage |
| S14 | 07 S14 |
| — | 07 S0 → Content Request (Architecture §3.3); 07 S15 and S16 → the cross-cutting cache and repair loop |

Milestone labels (M1, M3, M4, M5a, M5b, M5) in §7.2 and the CSV are defined in `../MATURITY_MODEL_and_ROADMAP.md` §1.

---

## 9. Inconsistencies with the architecture or the library

1. Architecture S7 lists `examleaf-science-reviewer` for every family, but its re-solve applies only to computable content. Claim-ledger families rely on GV-claims instead.
2. Architecture S4 turns lesson-plan into graph-author, but 06 OVERLAP §11 gives the planned 600 s budget to lesson-plan. In v2 that budget belongs to format-compiler (R5).
3. "Format family" in R12 and CE-50 is undefined. §7.2 proposes a grouping.
4. The 8 Kit archetypes cover 26 of the 43 slots. The rest have no qualified archetype (§4).
5. The 8 fill skills are proposed and unbuilt, so the Kit cascade cannot start until `kit_cascade` exists in `effort_policy.py` (13 §5.8).
6. VE skill descriptions are template-generated weak triggers (06 README). Trigger tests are needed before auto-invocation of extended skills.
7. The anim-qa severity text contradiction and the A11 16:9 rejection are carried over from QA doc §11. **Both resolved 15 Oct 2026 (CE-69).**
8. *(15 Oct 2026.)* The critic named the ingestion skill `curriculum-ingest`; the canonical id is `examleaf-curriculum-ingest`, which sits beside the existing `cg-import` (writer of framework files) and `curriculum-map` (scope selection). The three are kept apart by the one-owner rule: curriculum-ingest emits candidates only. `subsystems/README.md` still counts 17 new skills and 89 CSV rows; it should read 19 and 91 (README is outside this map's owner, so the correction is left to its owner). **Resolved 15 Oct 2026: `subsystems/README.md` now reads 91 rows (72 existing, 19 new).**
