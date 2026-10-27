# 11 · Master checklist

One checkbox list from an empty machine to business launch. Each line points to the document and section that explains it. Copy this file per run (for example `checklists/<date>_master.md`) and tick it there; keep this file as the template.

Legend: **[G]** = a gate; nothing after it starts until it is ticked with evidence attached.

**Updated 15 Oct 2026** after the end-to-end audit (`../14_end_to_end_audit/AUDIT_REPORT_2026-10-15.md`): vertical-only masters (RD-16 SUPERSEDED), storyboard gate H-SB (RD-46), animation setup and A-checks (RD-43), AI-voice disclosure gate (RD-45), review cash $0 (RD-41), launch locales (RD-42), and two open founder decisions (RD-44). Lines added or changed on that date are marked *(15 Oct 2026)*. *(Resolved 15 Oct 2026: out of pipeline scope per RD-49; the pipeline is commercially agnostic and this item lives in the business layer only.)*

---

## A. Setup — [`01_SETUP_new_machine_and_repository.md`](01_SETUP_new_machine_and_repository.md)

- [ ] Read the status banner and governing principles — [README §4](README.md)
- [ ] Decide reference OS (Linux/WSL2) and Python 3.13 — 01 §1, [RD-24], [RD-33]
- [ ] Install Python ≥ 3.11, FFmpeg **and ffprobe**, Cairo, DejaVu Sans, Git — 01 §2.1–§2.4
- [ ] *(15 Oct 2026)* This Mac's blockers cleared: Node **20.19.4** is active (Node **24.6.0** is installed under nvm → `nvm use 24`); **ffmpeg and ffprobe are both missing** (`brew install ffmpeg`); Python **3.14** is the default and there is **no `python` binary** → call `python3`, and create every venv with a pinned `python3.13` (`brew install python@3.13`) or the installed `python3.11` — 01 §2.3
- [ ] macOS only: Homebrew install, font path edit in a copy, `DYLD_FALLBACK_LIBRARY_PATH` if needed — 01 §2.3
- [ ] [G] P-1 prerequisites verified and logged — 01 §2.5
- [ ] Engine proof on a **copy**: install `[chemistry,test]` (RDKit needed for every render) — 01 §3.1
- [ ] `validate` exit 0 → `batch --workers 2` (8 rows; overwrites outputs) → `pytest -q` = **56 passed** (batch before pytest) — 01 §3.1 E3–E5
- [ ] `release-check` **blocks** (exit 1; narration missing, audio missing, academic and production approvals missing); no fabricated approvals — 01 §3.1 E9
- [ ] [G] P-2 engine proof logged — 01 §3.1
- [ ] Narration proof on a **copy**: `build_examples.py` (overwrites configs/examples/outputs) → `pytest -q` = *(15 Oct 2026)* **58 passed + 2 FFmpeg-environment failures** on a machine without FFmpeg, **60 passed** with FFmpeg (`pronunciation.py` and `tests/test_narration.py` intentionally differ from `DELIVERY_MANIFEST.json`, see `05_narration_system/narration_system_v1/CHANGES.md`) → `validate` → `compile` per profile (Cartesia fails until a real `api_version`) → `qa` (deliberate pauses flagged as unplanned silence) → `master` → `release-check` **exit 2** with 9 blockers; never run `build_docs.py` — 01 §3.2
- [ ] [G] P-3 narration proof logged — 01 §3.2
- [ ] Super Teacher linter on a copy: 0 errors; unittest 12 OK — 01 §3.3
- [ ] [G] P-4 linter proof logged — 01 §3.3
- [ ] View the delivered previews via `preview_local.html` (no re-render) — 01 §3.4
- [ ] Create canonical monorepo (`engine/`, `narration/`, `super_teacher_kit/`, `lessons/`, `sources/`, `ledgers/`, …); re-run tests inside it; tag `setup-baseline` — 01 §4, [RD-25]
- [ ] Hashed dependency locks; environment ledger (image digest, FFmpeg build, font hashes); licensed production fonts vendored — 01 §5, [RD-23]
- [ ] Activate only reviewed Skills per package; never both near-name authors; record activations — 01 §6, [RD-08], [RD-09]
- [ ] Trigger tests + functional + negative evals before relying on any Skill — 01 §6.4
- [ ] Worker identities and secret stores created; author identities hold no secrets — 01 §8, 07 §2
- [ ] Providers configured **off**; `PendingAdapter` untouched; budget ledger created with a small limit — 01 §9
- [ ] *(15 Oct 2026; PA-17)* When animation is in scope: **Node 22+ and Chrome/Chromium are required**; follow `12_advanced_animations_with_claude/02_documentation/01_SETUP_environment_harnesses_skills.md` (prerequisites, fonts, harnesses, Claude Code effort settings, job workspaces) — 01 §2.1
- [ ] *(15 Oct 2026; PA-17)* `bash 12_advanced_animations_with_claude/04_harness_contract/preflight.sh` passes; output saved to `logs/preflight.txt`. It checks only node, npx, ffmpeg/ffprobe, python, Chrome, fonts, disk and the skills symlink; ultracode/alias/secret checks come from `examleaf-effort-governor` — 06 §3.1 A2
- [ ] *(15 Oct 2026; PA-17)* [G] **S-ANIM**: V1–V15 pass on the authoring workstation; V1–V5 and V8–V11 on the render box — 12/02/01 §10, 06 §1
- [ ] [G] **S-GATE** — 01 §10

## B. Build phases — [`02_PHASED_BUILD_ROADMAP.md`](02_PHASED_BUILD_ROADMAP.md)

- [ ] P0: academic owner per subject assigned — 02 §2 P0
- [ ] P0: syllabus/rights evidence (ASSEB division, year, class, medium, edition); source ledger with hashes — 02 §2 P0
- [ ] P0: scaffold reviewed; unsupported assumptions rejected — 02 §2 P0
- [ ] P0: contracts frozen (LessonSpec fields, 12 pedagogy fields, display/spoken separation, `focused` mode, approval record) — [RD-12], [RD-29]
- [ ] P0: production design tokens (typography, holds, **1080×1920 @ 30 fps vertical-only** *(15 Oct 2026; ~~1920×1080~~ removed, RD-16 SUPERSEDED)*, phone rule, fonts, light theme) — [RD-01], [RD-02], [RD-18], [RD-23], [RD-27]
- [ ] P0: v1 minimum negative tests as fixtures — 06 §10
- [ ] P0: launch locales *(15 Oct 2026)* **en-IN, Hinglish, hi-IN**, each behind the locale gate; **as-IN deferred, human voice only, no Assamese TTS commitment** — RD-42 (supersedes RD-26), 04 §18
- [ ] [G] P0: "Academic owners agree on the definition of correctness" (signed) — 02 §2 P0
- [ ] Narration week 1: corpus (12 passages + 40 terms), 3 voices per locale audited, rights records — 04 §2
- [ ] [G] Narration week 1: approved primary voice per required locale — 04 §2
- [ ] P1: HyperFrames (and optionally Remotion) admitted in isolation; auto-install disabled — 07 §4
- [ ] P1: four golden fixtures ported without rewriting science; ≥ 5 repeats; cold/cached; RSS, wall time, repairs, visual diffs, human repair cost — 02 §2 P1
- [ ] P1: one compositor selected; core components with negative tests; still-frame fix; allowed kinds per subject — [RD-07], [RD-34], [RD-35]
- [ ] *(15 Oct 2026)* P1: **1080×1920 @ 30 fps output mode** added to the proof renderer (today the CLI renders only 1280×720 / 720×1280 and the fixtures use 24 fps); benchmark scored on 9:16, 16:9 only as an unscored smoke test — 02 P1, 03 S12
- [ ] [G] P1: same correct scientific states across layouts and repeated builds — 02 §2 P1
- [ ] Narration week 2: one live transport (Eleven v4 or Gemini 3.8) in the provider worker; usage records; limits; recovery; Eleven v4 quote obtained — 04 §8–§9, [RD-03]
- [ ] [G] Narration week 2: successful controlled synthesis and failure tests — 02 §2 P1
- [ ] Narration week 3: independent ASR; real forced alignment verified on an annotated sample; per-language normalization tests; critical terms listened — 04 §10–§11
- [ ] [G] Narration week 3: manually verified timing and pronunciation samples — 02 §4
- [ ] P2: TTS lifecycle (estimate/submit/cache/poll/fetch); timeline events into compositor adapters; manifest fields added — 02 §2 P2
- [ ] P2: minimum authenticated approval service with append-only audit log — [RD-17]
- [ ] P2: four complete pilots through every stage with timed records — 02 §2 P2; 03
- [ ] [G] P2: Four_Pilots acceptance gates all met; compositor confirmed after human-repair cost comparison — 02 §2 P2
- [ ] P2b: six Class 10 free lessons with pilot-grade records — [RD-05]
- [ ] P3: Prefect/Postgres/object storage, separate CPU and provider queues, secret isolation, retry/cancel/resume, staging failure injection, reviewer workflow — [RD-22]
- [ ] P3: 20–30-lesson controlled batch with measured cost, defects, retake fraction, human minutes — [RD-14]
- [ ] [G] P3: failure/repair/cost targets demonstrated; predictable accepted-output cost and defect rate — 02 §2 P3
- [ ] P4: scale only with queue/CPU/storage observations; new languages only after locale gate — 02 §2 P4
- [ ] PG: learning evaluation designed (delayed unprompted assessment, calibration); A/B priority 1 planned — 02 §2 PG

## C. Business gates and weeks — [`01_business_model/INSTRUCTIONS_business_launch_runbook.md`](../01_business_model/INSTRUCTIONS_business_launch_runbook.md)

- [ ] W1: interviews (15 students, 5 parents, 5 teachers, 4 shops); competing books; medium and board/year — 02 §3
- [ ] W2: two private prototype previews; price cards; three like-for-like print quotes (incl. lead time); tax/privacy review started; spend ≤ ₹60,000 — [RD-38]
- [ ] [G] G1 real paid demand — 02 §3
- [ ] W3: two Class 10 titles + one medium locked; syllabus map signed; free chapters per title chosen — [RD-20], RD-42. *(15 Oct 2026)* **DECISION NEEDED (RD-44):** "first three chapters" vs "three selected chapters" (or launch first-three and test selected) — founder records the choice in 10 before W3 *(Resolved 15 Oct 2026: out of pipeline scope per RD-49; the pipeline is commercially agnostic and this item lives in the business layer only.)*
- [ ] W4: reusable visuals; Reels and free lesson 1 **only if GF/GS-approved** — [RD-38]
- [ ] W5: checkout, entitlement DB, refunds/coupons, guardian flow; webhook test; free viewing without registration; no behavioural pixels — 07 §8
- [ ] W6: six free lessons; low-cost phone tests; partner specimens — 02 §2 P2b
- [ ] [G] G2 academic quality and teacher approval — 02 §3
- [ ] W7: blind review of papers and solutions; print proofs; tax/invoicing/access terms approved — 02 §3
- [ ] [G] G3 written GST, DPDP/minors and CCPA reviews — 07 §8
- [ ] W8: paid catalogue promised at launch complete (or honest schedule shown); print masters; scratch-code and two-device recovery tests; duplicate redemption and refund tests — 02 §5 M2
- [ ] [G] G6 payment + activation + refund tests — 02 §3
- [ ] W9: first short print batch only against paid demand; urban/rural dispatch test — 02 §5 M3
- [ ] [G] G4 print proof and quotes; [G] G5 delivery test — 02 §3
- [ ] W10: fulfil; repair activation friction; voluntary learning feedback; seed 10–20 outlets — 02 §3
- [ ] W11: referral pilot (one reward path); digital-only vs bundle — 02 §3. *(15 Oct 2026)* **DECISION NEEDED (RD-44):** whether a ₹299 digital-only SKU is in the launch at all, or deferred *(Resolved 15 Oct 2026: out of pipeline scope per RD-49; the pipeline is commercially agnostic and this item lives in the business layer only.)*
- [ ] W12: reconcile channels, stock, receivables; reprint by SKU demand and lead time — 02 §3
- [ ] [G] G7 reprint rule — 02 §3
- [ ] W13: continue / revise / stop; corrections log; source and customer-data audits — 02 §3
- [ ] [G] G8 day-90 decision (positive contribution, dependable delivery, evidence of learning) — 02 §5 M5

## D. Per-lesson stages — [`03_PER_LESSON_PRODUCTION_PROCEDURE.md`](03_PER_LESSON_PRODUCTION_PROCEDURE.md)

- [ ] S0 lesson folder and `00_intake.json` (IDs match platform resources; one narrow capability) — 03 S0
- [ ] S1 `extract-pdf` native text; source hash; rights record; figures/equations/empty pages reviewed; OCR only as a reviewed exception — 03 S1
- [ ] S2 syllabus map; [G] H-S2 academic owner approves syllabus fit, rights, edition — 03 S2
- [ ] S3 claims with sources; independent answer keys incl. boundary cases; unsupported claims blocked — 03 S3
- [ ] S4 `LessonPlan` + 11-beat plan; assessment before hook; prerequisites and repair route; over-dense → split — 03 S4, [RD-13]
- [ ] S5 script via pack master prompt; repair pass; five negatives; recent-script ledger; `validate` + `lint_script.py` pass — 03 S5, [RD-36]
- [ ] S5 rules: ladder; interaction loop; conditional feedback; humour ceiling; analogy contract; no fake listening; no invented biography; 1,100–1,250 words — 03 S5, [RD-10], [RD-11]
- [ ] S6 analogy cards, humour candidates (incl. none), interaction prompts with hidden answers; `answers_after` valid — 03 S6
- [ ] S7 typed validators + independent re-solve by a different agent/model; ScienceReport — 03 S7
- [ ] [G] **GA** academic approval bound to the script-bundle hash — 03 GA
- [ ] S8 SceneSpecs with 12 pedagogy fields, route (rules 1–6), cost cap; generated video 0 s by default — 03 S8, [RD-39]
- [ ] S8 design tokens and visual rules applied (palette, typography, one highlight, labels adjacent, axes/units, no colour-only) — 03 S8
- [ ] *(15 Oct 2026; PA-03)* [G] **H-SB** storyboard gate: 3×3 grid + `beats.json` + `estimate.json`; founder (cost) and academic lead (fit), two identities, via the approval service, bound to grid/beats/estimate/script/fixture/style/hero hashes; **no TTS, paid asset or scene code before it** — 03 H-SB, RD-46
- [ ] S9 typed state first; same-state rule; AssetManifest with provenance; new components versioned with negative tests — 03 S9
- [ ] S10 narration complete (section E) — 04
- [ ] S11 alignment validated; events from measured audio; protected pauses; no premature answers; `contains_fixture: false` — 03 S11
- [ ] *(15 Oct 2026; PA-17)* Animated scenes: one cue sheet per scene projected from `timeline.json`, rebuilt on any audio time change, validated with `12_advanced_animations_with_claude/04_harness_contract/validate_cue_sheet.py --production` (the builder's output currently fails that schema, audit M7: fix before relying on it) — 12/02/06
- [ ] S12 render **9:16 (1080×1920 @ 30 fps)** *(15 Oct 2026; was "16:9 (1920×1080)", RD-16 SUPERSEDED)*; atomic; probed; audio muxed within 0.05 s; VTT + SRT + transcript — 03 S12
- [ ] S13 automated QA complete; no open Critical; Majors repaired — 03 S13, 06 §2–§4
- [ ] *(15 Oct 2026; PA-07)* Animated scenes: A1–A17 pass (no failed hard check); H-RV rubric recorded; early answer reveal, untraceable science text and full-frame flashes are Critical — 06 §3.1, §4
- [ ] [G] **GF** academic + different production reviewer, full watch incl. small phones, four questions answered, bound to `final.mp4` hash; `release-check` passes in the release service — 03 GF, 06 §5–§6
- [ ] S14 export record (IDs, approved title/thumbnail/description, attribution, hash, *(15 Oct 2026)* `ai_voice_disclosure` + `performer_credit`; no secrets); immutable signed manifest; 17 artefacts present — 03 S14, 06 §7 *(15 Oct 2026, RD-49/CE-68: access designation and destination retired; the platform joins them by artefact id)*
- [ ] *(15 Oct 2026; RD-45)* [G] **Disclosure gate** before upload: description line (Path A "Performed by X; voice converted with AI tools; reviewed by Y." or Path B "AI-generated narration; script by X; reviewed by Y."); YouTube altered/synthetic toggle; Meta AI label; C2PA not stripped — 06 §6.4
- [ ] S15 cache keys and invalidation reasons recorded — 03 S15
- [ ] S16 repairs within limits (≤ 2 attempts; cost cap); approvals re-issued on new hashes — 03 S16
- [ ] `costs.json` and (pilots) `pilot_record.md` completed — 08 §3

## E. Narration — [`04_NARRATION_SUBPIPELINE.md`](04_NARRATION_SUBPIPELINE.md)

- [ ] N1 voice brief; approved voice per locale; rights record (licensed-stock or consented-custom); performance reference corpus; no student recordings — 04 §2
- [ ] N2 (non-English) localized script by multilingual-director; native editor approval — 04 §3
- [ ] N3 `NarrationPlan` valid (`validate`); segments 15–35 s; questions split from answers; think pauses with prompts — 04 §4
- [ ] N4 one mode per segment; emphasis on logical words; pace targets; no speeding — 04 §5, [RD-12]
- [ ] N5 lexicon entries for every `{{token}}`; versions match; critical distinctions tested; overrides only after acoustic test — 04 §6
- [ ] N6 compile per provider; unsupported direction kept in `editorial_style`; production gates pass; caps respected — 04 §7, [RD-28]
- [ ] N7 provider admission record; ledger reservation; ProviderJob — 04 §8
- [ ] N8 synthesis per segment in the provider worker; job IDs persisted; unknown jobs reconciled — 04 §9
- [ ] N9 independent ASR diff; critical terms listened; take accepted or segment repaired — 04 §10
- [ ] N10 forced alignment imported and validated against an annotated sample — 04 §11
- [ ] N11 timeline composed (sample-exact pauses, occurrences, frames, captions) — 04 §12
- [ ] N12 master −16 LUFS ± 1, ≤ −1 dBTP, 48 kHz mono 24-bit; re-measured after final mux; music off — 04 §13
- [ ] Audio release evidence: academic listening, voice rights, native review, caption review, sync review, hash match, mastering — 04 §15
- [ ] Golden set re-run before any model/voice/provider upgrade — 04 §16

## F. Shorts and Reels — [`05_SHORTS_and_REELS_PROCEDURE.md`](05_SHORTS_and_REELS_PROCEDURE.md)

- [ ] SH1 1–3 complete units selected (misconception → prediction → payoff → one CTA) — 05 §2
- [ ] SH2 `ShortSpec` valid (20–60 s, reflow, claims, conditions, *(15 Oct 2026)* `ai_voice_disclosure`, `performer_credit`) — 05 §2, [RD-19] *(15 Oct 2026, RD-49/CE-68: access designation and destination retired; the platform joins them by artefact id)*
- [ ] *(15 Oct 2026)* [G] H-SB for the Reel before any paid generation — 05 SH7, RD-46
- [ ] SH3 1–3 complete units recomposed from the approved vertical scenes (same verified state; never cropped); axes/conditions kept; phone rule — 05 §2, [RD-18]
- [ ] SH4 narration reused or new wording approved — 05 §2
- [ ] SH5 0–3 / 3–8 / 8–30 s / final-CTA structure — 05 §2
- [ ] SH6 truthful title and cover; caption = audience + promise + condition + one CTA — 05 §2
- [ ] [G] **GS** QA re-run (incl. A1–A17 for animated Reels); two approvals on the Short's hash — 05 §2
- [ ] SH8 auditable content record row; *(15 Oct 2026)* disclosure gate passed (06 §6.4); publish only approved hashes; 4–5 reviewed Reels/week; Class 12 CTAs wait for products — 05 §2–§3

## G. QA and release — [`06_QA_GATES_and_RELEASE.md`](06_QA_GATES_and_RELEASE.md)

- [ ] Every layer check run or explicitly marked not yet implemented — 06 §2
- [ ] Contrast ≥ 4.5:1 text, ≥ 3:1 graphics on actual frames; phone test at 360 px — 06 §3
- [ ] Science-frame QA (rendered events vs approved model); answer hidden until the window ends — 06 §3
- [ ] Severity applied; single critical error blocks — 06 §4
- [ ] *(15 Oct 2026)* A1–A17 run or explicitly marked not applicable for every animated scene; H-RV rubric attached to GF/GS evidence — 06 §3.1
- [ ] *(15 Oct 2026)* Disclosure gate wired into the release service (`release_check()` reason 11 is a build item) — 06 §6.1, §6.4
- [ ] Approvals only from the authenticated service; different reviewers; full watch — 06 §5, [RD-17], [RD-32]
- [ ] Errata page, edition, syllabus version, error-report method live; corrections log — 06 §8, [RD-31]

## H. Security — [`07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md`](07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md)

- [ ] Untrusted content never authorizes actions; permissions enforced in runner/containers/release service — 07 §1
- [ ] Narrow secrets and budgets per worker; renderer offline after staging — 07 §2
- [ ] Every public Skill/MCP/CLI admitted with a pinned commit; no curl|sh; no auto-install — 07 §4
- [ ] Licence ledger complete (GSAP, Blender, Remotion, FFmpeg, Anthropic doc Skills, F5-TTS weights, Fish Audio, fonts, voices, assets) — 07 §5
- [ ] Blender MCP isolated with `DISABLE_TELEMETRY=true`; MCP only for supervised auditions; SDK/API workers for bulk — 07 §6
- [ ] Voice consent records; performance vs identity reference separated — 07 §7
- [ ] Minors: guardian-mediated consent where required; OTP ≠ adult verification; no behavioural retargeting of children; WhatsApp permissions — 07 §8
- [ ] "What to avoid" list reviewed with the team — 07 §9
- [ ] Go-live security checklist — 07 §10

## I. Costs — [`08_COST_TRACKING_and_BUDGETS.md`](08_COST_TRACKING_and_BUDGETS.md)

- [ ] Per-stage caps loaded; over-cap approvals recorded — 08 §1, [RD-40]
- [ ] Ledger reservations, idempotency keys, job reconciliation running — 08 §2
- [ ] Per-lesson cost records complete — 08 §3
- [ ] *(15 Oct 2026; PA-11)* Animation-authoring line capped (provisional ≈ 78K tokens per non-template scene until pilot p90) and run ledger filled (model ID, requested/effective effort, tokens incl. cache, rounds, outcome) — 08 §1, §3
- [ ] *(15 Oct 2026; PA-12)* Effort explicit on every run, full model IDs pinned, no ultracode, caps 3 rounds + 2 repairs — 08 §8, 09 §4.1
- [ ] *(15 Oct 2026; RD-41)* Review recorded as timed minutes (capacity); review cash $0 — 08 §1 addendum
- [ ] Workbooks combined with the overlap recipe (floor/ceiling decided in writing) — 08 §6, [RD-15], [RD-21]
- [ ] Quotes obtained for every item in 08 §7 before committing money — 08 §7
- [ ] Model names and tariffs re-checked and re-dated at this gate — 08 §8, [RD-04]

## J. Launch milestones — [`02_PHASED_BUILD_ROADMAP.md`](02_PHASED_BUILD_ROADMAP.md) §5

- [ ] [G] M0 first pilot render with real speech
- [ ] [G] M1 first public free lesson or Short (GF/GS via the approval service)
- [ ] [G] M2 first paid lesson behind entitlement (G6 passed; access terms shown)
- [ ] [G] M3 before first book print (stable specific QR destinations; activation secrets hashed; edition/errata printed; G3, G4)
- [ ] [G] M4 public launch / sales (G5; support; corrections process; privacy controls)
- [ ] [G] M5 day-90 decision
- [ ] [G] M6 scale / Class 12 / new language
