# 09 - Research and evidence

**What this section is.** The consolidated evidence base behind the ExamLeaf Video Engine project: every cited research source, research ledger, tool/provider evaluation, public-Skill directory, licensing caution, effect size and "was it actually tested?" status that ChatGPT's six responses and its delivered packs produced, organized so each claim can be traced to its source, its stated limit, and the project sections that use it. Nothing was invented: the five synthesis documents are transcriptions and consolidations of the source text (cell wording is the source's own), and the 46 copied files are byte-identical to `00_source` (SHA-256 checked when this README was generated).

**Where it came from.** Research date of every source: **13 October 2026**. Raw provenance is in `../00_source/` (read-only; not modified):
* `00_source/chatgpt_transcript/messages/` - messages 02 (video engine v1), 04 (learning psychology), 06 (business model), 08 (Super Teacher), 10 (video engine v2), 12 (narration system); the sections used are named in each document's *Source* column.
* `00_source/chatgpt_transcript/cited_source_links.md` - every URL the responses cited.
* `00_source/extracted/<pack>/` - the five delivered packs: Super Teacher Starter Pack, Video Engine Planning Pack, Video Engine Implementation, Narration System, Business Launch Toolkit.
* `00_source/spreadsheets_as_csv/` - workbook sheets exported as CSV (Sources, Public_Directory, Provider_Tariffs, ExistingSkills).

**The one-sentence verdict the sources reach.** The design is well-researched but almost entirely *unverified in practice*: learning-science claims are mostly "strong foundation, implementation-dependent" or explicitly production hypotheses; every public Skill/tool was read, not run; prices are planning inputs; and no narrated, approved, student-tested lesson exists yet (see `VERIFIED_vs_PROPOSED.md`).

---

## 1. The five documents written for this section

| File | What it answers | Size of content |
|---|---|---|
| [`EVIDENCE_REGISTER.md`](EVIDENCE_REGISTER.md) | "Can I rely on this claim, how strong is it as the source puts it, what does the source say it does NOT show, where is the link, which section uses it?" Parts A-E: message 04 s1 table (10), effect sizes (16), message 08 s1.1-1.6 and related (20), message 02 s8 (10), further message 04/12 claims (25). Part F: Super Teacher ledger (29). G: production hypotheses (17). H: planned experiments (20). I: business source ledger (30). J: capability/pricing source ledgers (28). K: gaps and inconsistencies. L: URL cross-check against `cited_source_links.md`. | 205 register rows, plus URL cross-check lists and a 64-row cited-URL index (Part L) |
| [`TECHNOLOGY_DECISION_MATRIX.md`](TECHNOLOGY_DECISION_MATRIX.md) | "Which tool, for what role, with what strength/limit/licence/price, verified to what level, with what caveat?" 12 sections: compositors, subject libraries, ingestion/orchestration/storage, LLM costs, generative media (Runway, Higgsfield, Veo, Seedance, Kling, Pika, Luma), commercial TTS (ElevenLabs v2/v3/v4, Cartesia, Gemini, OpenAI, Sarvam, Chirp), open-source TTS (Kokoro, Chatterbox, Indic Parler, CosyVoice, Qwen3-TTS, Fish Speech, F5-TTS), ASR/alignment/audio, agent platforms, commerce and competitors, conflicting numbers, architecture-level cost options. | 100+ rows |
| [`PUBLIC_SKILLS_AND_INTEGRATIONS.md`](PUBLIC_SKILLS_AND_INTEGRATIONS.md) | "Can I install this public Skill/MCP/CLI/API, and what must I check first?" Merges the video-engine directory (21 rows) and the narration directory (28 rows) into one 49-row table; overlap check; the 6-row ExistingSkills sheet; the stated admission/install protocols. | 49 + 6 rows |
| [`VERIFIED_vs_PROPOSED.md`](VERIFIED_vs_PROPOSED.md) | "Was it actually run?" The explicit status tables of messages 06, 08, 10, 12, the packs' "not implemented" paragraphs, the 32 + 15 custom-Skill statuses, the eight renders, the environment limitations (Runway audio download blocked, browser navigation blocked, Linux font path...) and the promotion gates. | Parts A-G |
| [`cited_source_links.md`](cited_source_links.md) | The raw list of cited URLs (copy of the transcript file). | 64 URLs |

## 2. Every file placed in this section

Total placed: **46 copied files** (all under `ledgers/` except `cited_source_links.md`) **+ 4 synthesis documents + this README = 51 files.** Layout:

```
09_research_and_evidence/
  README.md  EVIDENCE_REGISTER.md  TECHNOLOGY_DECISION_MATRIX.md
  PUBLIC_SKILLS_AND_INTEGRATIONS.md  VERIFIED_vs_PROPOSED.md  cited_source_links.md
  ledgers/
    super_teacher_pack/{references, evals, pack_readme}
    video_engine_implementation/{research, docs, status_evidence, pack_readme}
    narration_system/{research, docs, status_evidence, pack_readme} + LICENSING_AND_SECURITY.md
    business_toolkit/    planning_pack/    spreadsheet_sheets_csv/
```

Role column: **Brief** = named in the section brief (ledgers, directories, CSV sheets, the listed docs) - 27 files; **Supporting** = extra copies added because a synthesis document cites them (pack READMEs, status JSONs and test logs, extra docs) - 19 files.

| # | Role | File (under `09_research_and_evidence/`) | Copied from (under project root) | Contents |
|---|---|---|---|---|
| 1 | Brief | `cited_source_links.md` | `00_source/chatgpt_transcript/cited_source_links.md` | All external URLs the ChatGPT responses cited, grouped as rendered on the share page (64 URLs). The citation-token-to-URL mapping is not preserved. |
| 2 | Brief | `ledgers/super_teacher_pack/references/Research_Ledger.md` | `00_source/extracted/ExamLeaf_Super_Teacher_Starter_Pack/ExamLeaf_Super_Teacher/references/Research_Ledger.md` | Super Teacher evidence/capability ledger: 18 research entries P01-P18, 4 OpenStax subject references S01-S04, 7 tool/standard references T01-T07, each with URL and limit. |
| 3 | Brief | `ledgers/super_teacher_pack/references/analogy_card.example.json` | `00_source/extracted/ExamLeaf_Super_Teacher_Starter_Pack/ExamLeaf_Super_Teacher/references/analogy_card.example.json` | Example analogy card (coefficient = sandwich copies) with mapping, non-mapping, return to formal science; status DRAFT_HUMAN_REVIEW_REQUIRED. |
| 4 | Brief | `ledgers/super_teacher_pack/references/authoring_contract.md` | `00_source/extracted/ExamLeaf_Super_Teacher_Starter_Pack/ExamLeaf_Super_Teacher/references/authoring_contract.md` | Authoring contract incl. 'Evidence versus production choices' and release rules. |
| 5 | Brief | `ledgers/super_teacher_pack/evals/local_test_report.txt` | `00_source/extracted/ExamLeaf_Super_Teacher_Starter_Pack/ExamLeaf_Super_Teacher/evals/local_test_report.txt` | Output of the 12 structural linter tests (all OK). |
| 6 | Brief | `ledgers/super_teacher_pack/evals/sample_structural_check.json` | `00_source/extracted/ExamLeaf_Super_Teacher_Starter_Pack/ExamLeaf_Super_Teacher/evals/sample_structural_check.json` | Linter result: STRUCTURE_ONLY, 0 errors, academic_approval false, audio_timing_measured false. |
| 7 | Brief | `ledgers/super_teacher_pack/evals/test_linter.py` | `00_source/extracted/ExamLeaf_Super_Teacher_Starter_Pack/ExamLeaf_Super_Teacher/evals/test_linter.py` | Source of the 12 linter regression tests (copied as a record; not executed here). |
| 8 | Supporting | `ledgers/super_teacher_pack/pack_readme/README.md` | `00_source/extracted/ExamLeaf_Super_Teacher_Starter_Pack/ExamLeaf_Super_Teacher/README.md` | Super Teacher pack README (what it is / is not; research and third-party material). |
| 9 | Brief | `ledgers/video_engine_implementation/research/Public_Skills_Directory.md` | `00_source/extracted/ExamLeaf_Video_Engine_Implementation/ExamLeaf_Video_Engine/research/Public_Skills_Directory.md` | Narrative public Skills/integrations directory, 21 entries, checked 2026-10-13. |
| 10 | Brief | `ledgers/video_engine_implementation/research/public_directory.csv` | `00_source/extracted/ExamLeaf_Video_Engine_Implementation/ExamLeaf_Video_Engine/research/public_directory.csv` | Same 21 entries as CSV (kind, origin, decision, licence, auth, install, security boundary, verification, snapshot). |
| 11 | Brief | `ledgers/video_engine_implementation/research/custom_skills.csv` | `00_source/extracted/ExamLeaf_Video_Engine_Implementation/ExamLeaf_Video_Engine/research/custom_skills.csv` | The 32 custom Skill drafts: purpose, inputs, outputs, steps, acceptance, fallback, cost, priority, status. |
| 12 | Brief | `ledgers/video_engine_implementation/research/subject_libraries.csv` | `00_source/extracted/ExamLeaf_Video_Engine_Implementation/ExamLeaf_Video_Engine/research/subject_libraries.csv` | 17 subject-library rows (module, role, boundary, source). |
| 13 | Brief | `ledgers/video_engine_implementation/research/sources.csv` | `00_source/extracted/ExamLeaf_Video_Engine_Implementation/ExamLeaf_Video_Engine/research/sources.csv` | 14 capability/pricing sources with scope and check date. |
| 14 | Brief | `ledgers/video_engine_implementation/research/cost_scenarios.json` | `00_source/extracted/ExamLeaf_Video_Engine_Implementation/ExamLeaf_Video_Engine/research/cost_scenarios.json` | AI-heavy / Hybrid / Self-hosted cost scenarios (status: planning_estimates_not_benchmarks). |
| 15 | Brief | `ledgers/video_engine_implementation/research/environment_observed.json` | `00_source/extracted/ExamLeaf_Video_Engine_Implementation/ExamLeaf_Video_Engine/research/environment_observed.json` | Observed proof environment (Python 3.13.5, Linux, package versions, font SHA-256). |
| 16 | Brief | `ledgers/video_engine_implementation/docs/Higgsfield_Findings.md` | `00_source/extracted/ExamLeaf_Video_Engine_Implementation/ExamLeaf_Video_Engine/docs/Higgsfield_Findings.md` | What to reuse and what to replace from the Higgsfield workflow. |
| 17 | Brief | `ledgers/video_engine_implementation/docs/Security_and_Installation.md` | `00_source/extracted/ExamLeaf_Video_Engine_Implementation/ExamLeaf_Video_Engine/docs/Security_and_Installation.md` | Public package admission process, runtime separation, Blender MCP, local proof boundary. |
| 18 | Supporting | `ledgers/video_engine_implementation/docs/Four_Pilots.md` | `00_source/extracted/ExamLeaf_Video_Engine_Implementation/ExamLeaf_Video_Engine/docs/Four_Pilots.md` | Eight-render benchmark table, four pilot objectives, acceptance gates (extra: cited by VERIFIED_vs_PROPOSED). |
| 19 | Supporting | `ledgers/video_engine_implementation/status_evidence/delivery_status.json` | `00_source/extracted/ExamLeaf_Video_Engine_Implementation/ExamLeaf_Video_Engine/outputs/delivery_status.json` | Machine-written delivery status (56 tests, 0 narrated lessons, 0 skill evaluations...). |
| 20 | Supporting | `ledgers/video_engine_implementation/status_evidence/live_speech_probe.json` | `00_source/extracted/ExamLeaf_Video_Engine_Implementation/ExamLeaf_Video_Engine/outputs/live_speech_probe.json` | Record of the one Runway speech job (32.18 s, 9 credits; download blocked). |
| 21 | Supporting | `ledgers/video_engine_implementation/status_evidence/browser_smoke.json` | `00_source/extracted/ExamLeaf_Video_Engine_Implementation/ExamLeaf_Video_Engine/outputs/browser_smoke.json` | Playwright attempt blocked by administrator policy (not bypassed). |
| 22 | Supporting | `ledgers/video_engine_implementation/status_evidence/tests.txt` | `00_source/extracted/ExamLeaf_Video_Engine_Implementation/ExamLeaf_Video_Engine/outputs/tests.txt` | pytest output: 56 passed. |
| 23 | Supporting | `ledgers/video_engine_implementation/status_evidence/benchmark.json` | `00_source/extracted/ExamLeaf_Video_Engine_Implementation/ExamLeaf_Video_Engine/outputs/benchmark.json` | Per-render benchmark and science/media QA records for the eight silent MP4s. |
| 24 | Supporting | `ledgers/video_engine_implementation/pack_readme/README.md` | `00_source/extracted/ExamLeaf_Video_Engine_Implementation/ExamLeaf_Video_Engine/README.md` | Video Engine README: 'What is actually implemented' / 'What is not implemented or approved'. |
| 25 | Brief | `ledgers/narration_system/research/Public_Narration_Directory.md` | `00_source/extracted/ExamLeaf_Narration_System/ExamLeaf_Narration_System/research/Public_Narration_Directory.md` | Narrative public narration/audio directory, 28 entries, with install protocol and documentation-drift notes. |
| 26 | Brief | `ledgers/narration_system/research/public_directory.csv` | `00_source/extracted/ExamLeaf_Narration_System/ExamLeaf_Narration_System/research/public_directory.csv` | Same 28 entries as CSV. |
| 27 | Brief | `ledgers/narration_system/research/custom_skills.csv` | `00_source/extracted/ExamLeaf_Narration_System/ExamLeaf_Narration_System/research/custom_skills.csv` | The 15 custom narration Skills with negative tests and status/cost. |
| 28 | Brief | `ledgers/narration_system/docs/Audition_and_Evaluation.md` | `00_source/extracted/ExamLeaf_Narration_System/ExamLeaf_Narration_System/docs/Audition_and_Evaluation.md` | Three-experiment audition design, rating roles, and live Runway connector evidence. |
| 29 | Brief | `ledgers/narration_system/docs/Provider_Lifecycle.md` | `00_source/extracted/ExamLeaf_Narration_System/ExamLeaf_Narration_System/docs/Provider_Lifecycle.md` | OpenAI deprecation, ElevenLabs/Cartesia/Gemini lifecycle facts and the admission checklist. |
| 30 | Supporting | `ledgers/narration_system/docs/Costs_and_Methods.md` | `00_source/extracted/ExamLeaf_Narration_System/ExamLeaf_Narration_System/docs/Costs_and_Methods.md` | Narration-only cost methods and provider comparison (extra: cited by the matrix). |
| 31 | Supporting | `ledgers/narration_system/docs/Voice_Identity_Guide.md` | `00_source/extracted/ExamLeaf_Narration_System/ExamLeaf_Narration_System/docs/Voice_Identity_Guide.md` | Voice identity guide incl. 'Evidence boundaries' (extra: cited by the register). |
| 32 | Supporting | `ledgers/narration_system/docs/Implementation_Roadmap.md` | `00_source/extracted/ExamLeaf_Narration_System/ExamLeaf_Narration_System/docs/Implementation_Roadmap.md` | Six-week narration integration roadmap (extra: cited by VERIFIED_vs_PROPOSED). |
| 33 | Supporting | `ledgers/narration_system/status_evidence/release_blockers.json` | `00_source/extracted/ExamLeaf_Narration_System/ExamLeaf_Narration_System/outputs/release_blockers.json` | Nine release blockers returned by the narration release check. |
| 34 | Supporting | `ledgers/narration_system/status_evidence/environment.json` | `00_source/extracted/ExamLeaf_Narration_System/ExamLeaf_Narration_System/outputs/environment.json` | Observed narration environment; 'no speech model downloaded or executed locally'. |
| 35 | Supporting | `ledgers/narration_system/status_evidence/tests.txt` | `00_source/extracted/ExamLeaf_Narration_System/ExamLeaf_Narration_System/outputs/tests.txt` | pytest output: 57 passed. |
| 36 | Supporting | `ledgers/narration_system/status_evidence/cost_summary.json` | `00_source/extracted/ExamLeaf_Narration_System/ExamLeaf_Narration_System/outputs/cost_summary.json` | Five narration-method cost scenarios (machine-readable). |
| 37 | Supporting | `ledgers/narration_system/LICENSING_AND_SECURITY.md` | `00_source/extracted/ExamLeaf_Narration_System/ExamLeaf_Narration_System/LICENSING_AND_SECURITY.md` | Rights and security boundaries of the narration pack. |
| 38 | Supporting | `ledgers/narration_system/pack_readme/README.md` | `00_source/extracted/ExamLeaf_Narration_System/ExamLeaf_Narration_System/README.md` | Narration README: status 'offline-tested sidecar', deliverables, next steps. |
| 39 | Brief | `ledgers/business_toolkit/Research_Source_Ledger.csv` | `00_source/extracted/ExamLeaf_Business_Launch_Toolkit/Research_Source_Ledger.csv` | Business source ledger: 30 rows (topic, type, URL, support, limit). |
| 40 | Supporting | `ledgers/planning_pack/README.md` | `00_source/extracted/ExamLeaf_Video_Engine_Planning_Pack/ExamLeaf_Video_Engine/README.md` | Planning-pack README: recommendation, scope and limitations, price/capability sources. |
| 41 | Supporting | `ledgers/planning_pack/QA_and_Implementation_Contract.md` | `00_source/extracted/ExamLeaf_Video_Engine_Planning_Pack/ExamLeaf_Video_Engine/QA_and_Implementation_Contract.md` | 'production contract - proposed, not implemented': release gates, negative tests, artifacts. |
| 42 | Brief | `ledgers/spreadsheet_sheets_csv/ExamLeaf_Business_Model__Sources__values.csv` | `00_source/spreadsheets_as_csv/ExamLeaf_Business_Model__Sources__values.csv` | Business model 'Sources' sheet (source ledger + open validation gaps). |
| 43 | Brief | `ledgers/spreadsheet_sheets_csv/ExamLeaf_Narration_Cost_Model__Sources__values.csv` | `00_source/spreadsheets_as_csv/ExamLeaf_Narration_Cost_Model__Sources__values.csv` | Narration cost model 'Sources' sheet (14 rows). |
| 44 | Brief | `ledgers/spreadsheet_sheets_csv/ExamLeaf_Narration_Cost_Model__Provider_Tariffs__values.csv` | `00_source/spreadsheets_as_csv/ExamLeaf_Narration_Cost_Model__Provider_Tariffs__values.csv` | Provider tariff references (12 rows). |
| 45 | Brief | `ledgers/spreadsheet_sheets_csv/ExamLeaf_Cost_and_Skills__ExistingSkills__values.csv` | `00_source/spreadsheets_as_csv/ExamLeaf_Cost_and_Skills__ExistingSkills__values.csv` | Planning-pack 'ExistingSkills' sheet (6 rows). |
| 46 | Brief | `ledgers/spreadsheet_sheets_csv/ExamLeaf_Video_Engine_Cost_Model__Public_Directory__values.csv` | `00_source/spreadsheets_as_csv/ExamLeaf_Video_Engine_Cost_Model__Public_Directory__values.csv` | Video Engine cost model 'Public_Directory' sheet (21 rows). |

The four synthesis documents and this README are original text written for this section (not copies); they quote the sources and are not a substitute for them.

---

## 3. How to use this section (step by step)

**A. Check a learning-science claim before it goes into a script, storyboard or marketing line**
1. Open `EVIDENCE_REGISTER.md` and search for the keyword (`grep -n -i "retrieval" EVIDENCE_REGISTER.md`).
2. Read the **Evidence label** column - use the source's own word: *Strong foundation*, *Context-dependent*, *Production hypothesis*, *Not supported*, *Insufficient*, *Not justified*.
3. Read **Does NOT establish** before using the claim. Never write the stronger version (e.g. do not write "retrieval raises marks by 50%"; the register says g = 0.50 "does not mean 50% higher marks").
4. If the row is in Part G, it is an untested starting value - put it in a config, not in a claim. If it is in Part H, the experiment has not been run.
5. Cite the row ID (e.g. `E-A07`) in the lesson's source ledger. If the link cell says **URL not preserved**, do not quote a URL; follow Part K item 1.

**B. Choose or re-check a tool**
1. Open `TECHNOLOGY_DECISION_MATRIX.md`, jump to the section for the layer (compositor, TTS, ASR, ...).
2. Read **Verification level** first - almost every row is "documentation inspected; not installed or executed" or "research-read; not live-tested".
3. Read **Licence / pricing as stated** and the **Caveat** (voice rights, code vs weights, GPL vs output, conditional commercial terms, deprecation dates).
4. If a price matters, check section 11 for conflicting figures, then re-check the provider page - every price is dated 13 October 2026.
5. Do not adopt a tool without a live contract test plus listening/rendering evaluation (the sources' own admission rule).

**C. Install a public Skill, MCP server or CLI**
1. Find the entry in `PUBLIC_SKILLS_AND_INTEGRATIONS.md` Table 1 (49 rows).
2. Follow the **Install approach (after audit)** cell and the admission steps under "Admission and install protocols": resolve official repo -> read scripts/manifests/hooks without executing -> record an exact **commit** (the listed blob SHAs are not commit pins) -> evaluate in a disposable container without production credentials -> copy only selected folders -> re-audit upgrades.
3. Never run `curl | sh` installers or `npx skills add ...` as an audit; never enable auto-install/auto-update in production.

**D. Find out whether something was really tested**
1. Open `VERIFIED_vs_PROPOSED.md`; Part A is a one-page status table, Parts B-E are per-pack (Super Teacher, Video Engine, Narration, Business/cost), Part F lists the environment limitations, Part G the promotion gates.
2. If a status is NOT DONE, the matching evidence file is in `ledgers/*/status_evidence/`.

**E. Add new evidence later**
1. Append a row to the right part of `EVIDENCE_REGISTER.md` (next free ID, same six columns, the source's own wording for label and limit).
2. If you verify or run something, move its row in `VERIFIED_vs_PROPOSED.md` from PROPOSED/RESEARCHED to TESTED and put the receipt (log, hash, date) in a new `ledgers/.../status_evidence/` file.
3. Re-check dated facts (prices, model lifecycles, repository states) on a schedule; the narration directory warns of "documentation drift".

**F. Prove the copies are unchanged**
```sh
cd <project root>
diff 09_research_and_evidence/cited_source_links.md 00_source/chatgpt_transcript/cited_source_links.md
diff 09_research_and_evidence/ledgers/video_engine_implementation/research/public_directory.csv \
     00_source/extracted/ExamLeaf_Video_Engine_Implementation/ExamLeaf_Video_Engine/research/public_directory.csv
```
(The "Copied from" column above gives the origin of every file.) No network access is needed for any step in this section; no URL was fetched while building it.

---

## 4. Cross-references to the other sections

| Section | What this section gives it | What it takes from this section |
|---|---|---|
| [`01_business_model`](../01_business_model/) | Part I of the register (30 market/regulatory/platform rows: ASSEB, ASER, GST, DPDP, Meta, Razorpay, Amazon, Cloudflare...), competitor and commerce rows in the matrix s10, verified-vs-estimated table (`VERIFIED_vs_PROPOSED.md` Part E) | Business source ledger, tariffs, assumptions |
| [`02_learning_psychology`](../02_learning_psychology/) | Evidence register Parts A, B, D, E (labels, effect sizes, limits), G (hypotheses), H (A/B experiments) | The blueprint (message 04) whose claims are being labelled |
| [`03_super_teacher_framework`](../03_super_teacher_framework/) | Register Parts C and F (message 08 s1 + the 29-entry research ledger); starter-pack status (`VERIFIED_vs_PROPOSED.md` Part B) | Framework text, authoring contract, analogy card |
| [`04_video_engine`](../04_video_engine/) | Matrix s1-s3, s5 (compositors, libraries, orchestration, generative media); public Skills rows 1-21; Part C of the status document (what the eight renders and 56 tests prove) | Architecture and prototype descriptions |
| [`05_narration_system`](../05_narration_system/) | Matrix s6-s8 (TTS, open-source TTS, ASR/alignment); narration public-directory rows 22-49; provider lifecycle and audition evidence; Part D of the status document | Voice identity guide, provider recipes |
| [`06_skills_library`](../06_skills_library/) | `PUBLIC_SKILLS_AND_INTEGRATIONS.md` (what public Skills may complement the custom ones, with licence cautions); skill status tables (32 + 15) in `VERIFIED_vs_PROPOSED.md` | The 40/32/15/10 custom Skill definitions |
| [`07_end_to_end_pipeline_instructions`](../07_end_to_end_pipeline_instructions/) | Admission/install protocols, release-gate and QA statements, promotion gates (`VERIFIED_vs_PROPOSED.md` Part G), safe-install steps | Pipeline stages and QA contract |
| [`08_cost_models`](../08_cost_models/) | Every stated price with its verification level and the conflicting-figures table (matrix s4, s6, s11, s12), `Provider_Tariffs` and `Sources` sheets | Workbook formulas and scenarios |
| [`10_pilots_and_examples`](../10_pilots_and_examples/) | Planned experiments (register Part H), `Four_Pilots.md` acceptance gates and the eight-render table | Pilot plans, sample lessons and outputs |

## 5. Known gaps and cautions (what this section does not contain)

1. **Citation-token mapping lost.** The transcript marks citations with opaque tokens; the token-to-URL mapping is not in the export. Register rows for which no listed URL fits say **URL not preserved** (list in `EVIDENCE_REGISTER.md` Part K). Links shown as "(inferred)" were matched by the label in `cited_source_links.md`.
2. **Not researched by the sources:** Flipkart fees (message 06: "Flipkart should be similarly costed using the actual seller-account quotation"); Higgsfield whole-lesson price; Luma price; Eleven v4 tariff ("TBD"); Pika/Luma/Veo/Seedance/Kling side-by-side quality ("No side-by-side scientific-video audition was performed"); local market shelf prices; exact 2026 Assam participation numbers.
3. **Numbers that differ between messages/packs** (pace, word budget, pause lengths, typography, ElevenLabs $0.08 vs $0.10, Anthropic model rates) are shown side by side, not reconciled (`TECHNOLOGY_DECISION_MATRIX.md` s11, `EVIDENCE_REGISTER.md` Part G/K).
4. **The 2026 seductive-details meta-analysis (g = -0.16)** and the segmentation meta-analysis (56/88) cannot be matched to a single listed URL.
5. **Everything is dated 13 October 2026.** Prices, model lifecycles (OpenAI TTS shutdown 2027-01-06; Gemini tariff change 2027-01-01) and repository states move quickly.
6. **No fetching was done.** Nothing in this section was verified against the live web; it records what the sources stated.

