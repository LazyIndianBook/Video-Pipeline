# 10 · Implementation roadmap (Professor Diki Simplified shorts, from 16 Oct 2026)

Status (16 Oct 2026, 20:30 IST): a plan, not a record. Dates are my proposed targets counted from Friday 16 Oct 2026; efforts are my estimates; "done" cites the file that proves it. Every date after Tue 20 Oct moves with the hand-over of the v2.0.x design system (another builder, in progress, date unknown to me). Item ids (IP-nn) refer to `02_IMPROVEMENT_PLAN.md`.

## 1. How an exit is measured

- **QA:** `qa.py <script> --format concept_short_60` shows no fail in A1–A21; every warn is explained in the build notes.
- **Scorecard:** `scorecard.py` shows all six gates pass, none missing, total ≥ 85 (`09_SCORECARD.md`). It scores a machine-only report as full marks and prints `releasable: True` (IP-06), so every exit below also needs blind D1–D8 verdicts from two judges (`JUDGE_RUBRIC_PD.md`) and one human watch and listen, since nothing shows that model judges can hear audio. It cannot see the human gates: GA, GS and the §6.4 upload gate (`06_QA_GATES_and_RELEASE.md`) are kept as records.
- **Brand and tests:** `brand_check.py` exit 0; `tests/run_all.sh` green.
- **Baseline** (machine-only, my run on copies of the Opus reports): all three Opus builds pass science and technical and fail brand, prediction/transfer, persistence and silence/length (`07_PIPELINE_CHANGES.md` §2 lists the A11–A21 failures).

## 2. Phase 0 · This cycle (to Fri 16 Oct 2026)

Done, with proof:
- Audit `01_VIDEO_AUDIT.md`; decisions PD-01 to PD-21 in `DECISIONS_PD.md`.
- Contract and format: `DIKI_CONTRACT.md`, `format/concept_short_60.md`, `NARRATION_DIRECTION_SHEET.md`.
- Pipeline: `qa.py` A11–A21, `render.py` audio extras, `check_script.py` v2, `pilotlib.py` and `narrate.py` (lead-in 0.3 s, room tone, two-pass loudnorm), Kit R-027 to R-038, 12 regression tests.
- Brand: `strings.json` 1.1.0, `brand_check.py`, wordmark, opening-ident and end-card SVGs, end motif and two accents, `MIGRATION_LOG.md`.
- Teaching and scoring: framework `03`, `skills/professor-diki-script/`, `check_pd_script.py`, two exemplar scripts, `09_SCORECARD.md`, `scorecard.py`, `JUDGE_RUBRIC_PD.md`.
- Voice: ElevenLabs key live, smoke test HTTP 200; the library-voice audition was refused (HTTP 402, Free plan).

In progress: design system v2.0.x and the `demo/physics_v2` rewrite under PD-17 to PD-21 (both by another builder; the demo's static checks pass at 20:30; no narration, render, QA or judging yet).

**Exit E0:** `tests/run_all.sh` green after the last edit (07 reports 12 of 12; not re-run since); `brand_check.py --selftest` OK (I ran it today). The document sync (IP-11) moves to Phase 1.

## 3. Phase 1 · Mon 19 Oct to Fri 30 Oct 2026

| Work | Target | Exit measure |
|---|---|---|
| Fix `scorecard.py` (judge presence), sync documents (IP-11), install the skill; the founder names the academic owner | Mon 19 – Tue 20 Oct | `releasable: false` with no verdicts; no AI line on an end card outside `strings.json`; skill present in `~/.claude/skills` |
| Finish the v2 design system | Tue 20 Oct (assumed) | `build_scene.py` exit 0 and `qa_scene.py` ok on the example; `05_DESIGN_SYSTEM.md` rewritten |
| Finish the physics demo on v2 (under way) | Wed 21 Oct | `check_script.py`, `check_pd_script.py`, `brand_check.py`, `build_scene.py`, `qa_scene.py` all clean |
| Academic review of SIM-push-flow, ASM-transfer-six-volts, CLM-filament | Fri 23 Oct | GA record with the reviewer's identity |
| Narrate (about 743 characters, stock voice, PD-05; confirm with `narrate.py --dry-run`) and render | Mon 26 Oct | A1–A21 no fail; 60.0 ± 1.0 s; silence ≤ 15 %; A9 byte-identical re-render (no pixel double-render hash test has run on the design system, 05 §10) |
| Blind judging (`prepare_judging.py` needs a path option for `17_…/demo/`), a human watch and listen, then the before/after scorecard | Tue 27 and Wed 28 Oct | six gates pass, total ≥ 85, D8 judged, listening notes on D5 and D8; table of the 07 §2 baseline against the after build |
| Chemistry and biology example lessons on v2 | Mon 26 – Fri 30 Oct | static checks as above; `narrate.py --dry-run` plans 60 ± 1 s; narrated only if the plan decision (§7) is made |
| Haiku re-run with Kit v0.2.0 | Fri 30 Oct | only if the physics exit holds and the founder agrees (digest §5: other tiers wait for Opus quality); A1–A21 against the Haiku v2 baseline, where all eleven new checks fail today (07 §2); no tier claim |

**Exit E1:** the physics after-build meets every measure; chemistry and biology pass their static checks; the before/after report exists. If it scores below 85 or a gate fails, fix at the lowest rung that holds, re-run, and hold dependent Phase 2 work.

## 4. Phase 2 · Mon 2 Nov to Mon 30 Nov 2026

| Work | Target | Exit measure |
|---|---|---|
| Plan upgrade (founder) and Indian-English audition: 12 prepared requests, about 2,100 characters, re-scoped to en-IN voices | audition by Fri 6 Nov | three candidates rated; native gate passed for en-IN; `voice_id` resolves to an admitted en-IN entry; a tag is admitted only with a measured shift (+1 st or +1 dB, A3-09) |
| Re-narrate physics, chemistry, biology on the chosen voice | Fri 27 Nov | A1–A21 no fail on all three; A13, A19, A21 re-run; scorecard ≥ 85 with verdicts |
| Fonts vendored | Fri 6 Nov | tokens resolve to local files with recorded hashes; licences checked; no system fallback |
| Platform insets measured on real devices | Fri 13 Nov | tokens no longer say PLACEHOLDER; A16 re-run on all builds |
| Academic review of chemistry and biology nodes; correction ledger opened | Fri 6 Nov | GA record per short |
| Remaining components: graph/axes, ray-optics bench, particle field, units ledger | Mon 9 – Mon 30 Nov | each passes `qa_scene.py` on an example with seek purity; cross-video identity gate added and green |
| Captions decision (burn-in, sidecar or both) and chunker fix | decision Mon 9 Nov | VTT cues ≤ 42 characters by 2 lines, 1.8 s for six words; A12 still 0 hits |
| Student sessions (12–20 students, `09_SCORECARD.md` §4) | Mon 16 – Fri 27 Nov | results logged; no learning claim published |
| Upload gate dry run on an unlisted post | Fri 27 Nov | all four §6.4 confirmations recorded |

**Exit E2:** three subjects pass A1–A21 and score ≥ 85 on the chosen voice; identity gate green; fonts and insets closed; captions decision recorded; GA and GS records exist for each short; the dry run is complete.

## 5. Phase 3 · Tue 1 Dec 2026 to Fri 15 Jan 2027

| Work | Target | Exit measure |
|---|---|---|
| First public posts, only with the narration licence, name clearance, O-5 answer and approvals in place | from Tue 1 Dec | the first 10 posts set baselines for the 04 §8 hypotheses (hook rate, watch-through, shares, saves, follows) |
| Two human approvals: GS by the academic owner and a different production QA reviewer, bound to the MP4 SHA-256, plus the §6.4 gate | every post | a record per post; a post without one is logged as a process failure |
| Playbook cadence: parent lessons first; stage two titles (2 × 354 = 708 accepted minutes, about 5.9 weeks at 120 a week; playbook pp. 13–14); a short ships only after its parent lesson is approved | fixed in writing Fri 18 Dec | releases per week never exceed approvals per week, set from reviewer minutes per short (unknown today) |
| Scorecard gating in CI: tests, `qa.py`, `scorecard.py` on every contract, template, token, brand or script change | Fri 18 Dec | broken fixtures (ExamLeaf in a caption, a 5 s think window, an AI line on the end card) fail the pipeline; the default interpreter moves off `/private/tmp`; cross-machine byte identity confirmed or tolerance documented |
| Recent-script ledger (SQ-18) | Fri 18 Dec | no two consecutive shorts share opening type and beat order |
| Hindi, Assamese, Bengali options | Mon 7 Dec – Fri 15 Jan | per locale: native-reviewed golden-set pass; glyph check on the as-IN smoke strings; Latin brand string unchanged |

**Exit E3:** every released short has A1–A21 with no fail and a scorecard ≥ 85 with six gates passing; no publish without records; CI blocks the broken fixtures; the cadence is written down; each locale pilot is passed or deferred by decision.

## 6. Dependencies and risks

| Item | Effect | Mitigation and owner |
|---|---|---|
| Narration quota: Free plan 10,000 characters a month, about 2,285 left; three scripts the size of the physics demo (743 characters) use 2,229 | no retake budget; Free plan listed non-commercial; library voices need a paid plan | founder picks Starter ($6 a month, first month $1), Creator ($22), Pro ($99), pay-as-you-go ($0.08 per 1,000 characters) or the Startup grant (list prices read 16 Oct; verify); cached beats cost nothing |
| Determinism: verified on this Mac only (Chrome 155, `--disable-gpu`, serial renders); narration seed is best effort | CI may differ; re-narration can shift timings | pin the CI image; keep the beat cache; recalibrate A13 with evidence |
| Review capacity: no reviewer named; team throughput 120 accepted minutes a week (playbook); a scientific error is a quarantine event | the queue caps the cadence | founder names the academic owner and a second reviewer |
| AI declaration at upload: PD-20 removed the only visible one; counsel's O-5 (is a visible label required for Path B?) is open; the §6.4 gate is human and no code checks the sidecar | a missed toggle; an O-5 ruling would reopen PD-20 (edits to `brand_check.py`, `check_script.py`, the end-card fixture) | counsel answers O-5 before the first post; publisher identity runs the gate; sidecar validator (IP-07) |
| A13, A15, A16 thresholds were calibrated on pre-v2 renders | false pass or fail on the collage | recalibrate on the first v2 render |
| Name clearance and "Diki" pronunciation unverified | a rename after launch is costly | founder and counsel; lexicon entry plus an ASR check |
| Scope rule: other tiers wait for Opus quality | the Haiku re-run may be cancelled | founder go/no-go Fri 30 Oct |
| Scorecard weights are house policy; 04 §8 targets are hypotheses | a score is not evidence of learning | no learning claim until measured |
| Design-system hand-over date and font licences unknown | Phase 1 slips; other faces | track with the other builder; check licences first |

## 7. Who decides what

| Decision | Decider | Needed by |
|---|---|---|
| Narration plan or grant | founder | Fri 23 Oct to narrate all three in Phase 1, else Mon 2 Nov |
| Academic owner and production QA reviewer (GA, GS) | founder | Tue 20 Oct |
| Haiku re-run go or no-go | founder | Fri 30 Oct |
| Hero fill: 45 % of the frame or of the lane (07 §5); thresholds | lead | Mon 19 Oct |
| Captions: burn-in, sidecar or both | lead with founder | Mon 9 Nov |
| "Free lesson" wording waiver (Q-COMM); commerce scope C02, C13, C19 | founder | Mon 9 Nov |
| Student sessions: consent and child-data design | founder | Fri 6 Nov |
| Voice choice, after the native gate | founder | Fri 20 Nov |
| Name clearance, channel split, handles; counsel's O-5 answer and the IT Rules note | founder and counsel | before the first post |
| Locale order and Bengali scope | founder | Mon 7 Dec |
| Publish (release authority) | publisher identity | every post |

**Added 17 Oct 2026 (PD-26).** The external kit `Professor_Diki_Simplified_Production_Kit.zip` (editorial profile PDS-60-Editorial-1.0, Opus generation and review prompts, an offline reviewer contract and Python checker) was received; its editorial direction is adopted as `11_SIXTY_SECOND_EXPLAINER_METHOD.md`. Its reviewer contract and checker are a Phase 2 candidate adapter (map one script to the contract, inject the audited failures, confirm they block) alongside our QA A1–A21 and blind judges; its 2.5-second thinking gap is not adopted in shorts (PD-24). The Ohm's law method short (`demo/physics_v4_method/`) is built and checked now and narrated after the ElevenLabs quota reset on 15 Nov 2026 or on the paid plan.
