# 02 · Prioritised improvement plan (Professor Diki Simplified, 16 Oct 2026)

Status (16 Oct 2026, 20:30 IST): the 118 findings of `01_VIDEO_AUDIT.md` (11 critical in bold, 73 major, 34 minor) grouped by root cause, each id in one item. "Closes" is what a fix addresses; Status says whether it has landed, citing the file I read. I ran only read-only checks (§4). No human has watched or listened to a v2 render.

## 1. Summary

Five root causes explain the findings. (1) Contract constants and slot grammar (`PILOT_CONTRACT.md` §3): 60–70 s, a fixed 5 s think window, no transfer or close slot, a spoken disclosure. Closed for shorts (`DIKI_CONTRACT.md`, A11/A13/A18). (2) The retired brand string, enforced by our own validator. Closed on the v2 path (A12); the v1 branch is live. (3) A scene-per-beat render that tore the board down. Closed in contract and QA (A17); the runtime is being rebuilt as v2.0.x by another builder, so still open. (4) QA and judging that scored render success and compared Haiku with Opus. Closed by A11–A21 and the absolute scorecard, with three gaps (IP-06). (5) No house identity: decided (PD-08, PD-19), in progress. **Nothing is proven on a narrated render: no v2 short has been narrated or rendered. The physics demo is being rewritten by another builder (files dated 20:23 to 20:28).**

## 2. Items

P0 blocks release, P1 next build, P2 quality, P3 later. IP-01 to IP-05 map to the five content gates of the scorecard, IP-06 is the machinery that enforces them, IP-07 is the upload step. Still open inside P0: IP-04 (runtime), IP-05 (gate, reviews), IP-06 (three gaps), IP-07 (all).

### IP-01 · P0 · Brand and disclosure enforced by our own constants
**Closes:** **A1-28**, **A3-02**, **A4-03**, **A5-01**, A2-15, A5-02, A5-03, A5-04, A5-12, A5-14, A5-15  
**Cause** (tooling, contract, validator): `pilotlib.py:23` DISCLOSURE, `check_script.py` v1 branch, `PILOT_CONTRACT.md` §3/§4 outro, QA A7 certifying the string, registry literals.
**Fix:** one source, `brand/strings.json`; end card = brand line + `Free lesson: <topic>` (PD-20, PD-21).  
**Control:** A12 + `brand_check.py`; `test_examleaf_fails_a12`, `test_examleaf_in_captions_fails_a12`.  
**Owner:** contract, QA. **Status:** done for shorts: `strings.json` 1.1.0, `brand_check.py` (selftest OK), A12, `MIGRATION_LOG.md` (56 locations, 17 files). Planned: retire the v1 branch and constant; A12 never reads pixels (A5-03); no repo-wide guard; MP4 publisher tags unverified (A5-15). **Effort (est.):** 0.5 day v1, 0.5–1 day pixel OCR, 0.5 day repo guard.

### IP-02 · P0 · Time budget, idea budget and pauses
**Closes:** A1-29, A3-01, A3-03, A3-M6, A4-01, A4-02, A5-08, A3-04, A3-05, A3-06, A3-07, A3-08, A4-14  
**Cause** (contract, tooling): `PILOT_CONTRACT.md` §0/§3 ("60–70 s", `think_window_s` 4–6); `check_script.py` omitted lead-in and tail and only printed; `qa.py` A8 warn-only; `narrate.py` lead-in 0.6 s, tail 1.6 s.
**Fix:** PD-01, PD-07, PD-14, PD-16: 60.0 ± 1 s, one claim plus its condition, `pauses[]` with a purpose, lead-in 0.3 s, 0.8 s tail, room tone.  
**Control:** `check_script.py` v2; A11, A13, A19, A20; `test_five_second_think_fails_a13`.  
**Owner:** contract, narration. **Status:** done (`DIKI_CONTRACT.md` §3/§4/§7, `pilotlib.py`, `narrate.py`, `qa.py`). Unproven on real audio: the positive fixture is synthetic, so A13's ±25 % bands are uncalibrated. **Effort (est.):** 0.5 day after the first narrated run.

### IP-03 · P0 · Slot grammar: answerable prediction, payoff, transfer, close
**Closes:** **A1-01**, **A1-27**, **A1-M1**, **A5-05**, A1-02, A1-12, A1-20, A1-30, A1-M3, A1-M4, A1-M5, A1-M7, A1-M8, A3-M2, A3-M4, A3-M5, A4-11, A1-10, A1-24  
**Cause** (contract): `PILOT_CONTRACT.md` §3 and `pilotlib.SLOTS` had no transfer, payoff or close slot; `check.retrieval` optional; the disclosure replaced the next-step pointer.
**Fix:** PD-06, PD-14: hook, check.predict, reveal.answer, check.transfer, feedback.transfer, close.next_step, outro.brand in order; givens shown and spoken before the question; reveal within 3 s; `cta_line` from the business layer.  
**Control:** A18; `check_script.py` v2; `check_pd_script.py`; `test_prediction_before_givens_fails_a18`, `test_missing_transfer_fails_a18`.  
**Owner:** contract, script skill. **Status:** done (`DIKI_CONTRACT.md` §3/§5; the demo script passes `check_pd_script.py`). Open: A18 is a heuristic, the answer-hidden detector PK-D09 does not exist, no learner has tried a transfer question. **Effort (est.):** PK-D09 0.5 day.

### IP-04 · P0 · One persistent board
**Closes:** **A2-01**, A1-09, A2-02, A2-03, A2-04, A2-05, A2-12, A2-13, A4-04, A4-05, A6-06, A1-17, A2-14, A2-17, A2-18, A2-19, A3-M3  
**Cause** (render, template): `render.py` concatenates independently built scene MP4s; `PILOT_CONTRACT.md` §4 one HTML per scene; `scene_template.html` hides cued parts until their word.
**Fix:** PD-03: one scene; hero visible at frame 0 and only transforming; no draw-on; recap is the final board; every change has a cause.  
**Control:** A14–A17; `build_scene.py` and `qa_scene.py` gates (W_PERSIST_BROKEN, W_NO_HERO, W_FILL_LOW).  
**Owner:** design system, contract. **Status:** contract and checks done (`DIKI_CONTRACT.md` §1; the three Opus builds fail A17 in `test_regressions.py`). In progress: the v2.0.x runtime (another builder; not assessed). A15 can pass on ambient motion and the cue cross-check is unbuilt (07 §2). **Effort (est.):** cross-check 0.5 day; runtime unknown.

### IP-05 · P0 · Science integrity and brief gate
**Closes:** A1-07, A1-18, A1-22, A4-10, A5-09  
**Cause** (script, lesson graph): no brief gate; SQ-23/24 report-only; "fifty" became "herd" via an out-of-schema node `hook_colour`.
**Fix:** brief declares `question_target`; spoken values `on_chain`; a confront needs a sourced counter-value; lamp qualitative until a reviewed fixture exists (PD-16); academic sign-off for new nodes.  
**Control:** `compute.py` closure asserts; A3, A7; `check_pd_script.py` SQ-23; human GA gate (`06_QA_GATES_and_RELEASE.md`).  
**Owner:** script skill; reviewers sit in the business layer. **Status:** partly done: fixture closure and qualitative lamp in the demo. Planned: `question_target`, `on_chain` and unknown-node rejection do not exist (grep). Awaiting review: SIM-push-flow, ASM-transfer-six-volts, CLM-filament wording; no reviewer is named in the files I read. **Effort (est.):** gate 0.5 day; review capacity unknown.

### IP-06 · P0 · QA and review loop
**Closes:** **A4-12**, A4-13, A3-14, A3-15  
**Cause** (QA, review loop): `qa.py` A1–A10 checked render success; `JUDGE_RUBRIC.md` compared A with B; the Kit skill `examleaf-fill-concept-intro` §9 named the Opus builds golden.
**Fix:** A11–A21; frozen Opus negatives; absolute scorecard with D8 and hard gates; two-pass loudnorm; word-edge cue placement.  
**Control:** `tests/run_all.sh`; `scorecard.py`; `JUDGE_RUBRIC_PD.md`.  
**Owner:** QA. **Status:** done: `qa.py` A11–A21, 12 regression tests (07 reports 12 of 12; not re-run), `09_SCORECARD.md`, `scorecard.py`, `narrate.py` loudnorm and word-edge placement (unrun on v2). Gaps: (a) `scorecard.py` prints 100.0 and `releasable: True` for an all-pass machine report with no judge verdicts (reproduced in scratch; **fixed the same evening**: `releasable` now also requires at least one judge verdict, reported as `judge_verdicts`) and omits 09 §1's judge D1 ≥ 4 clause; (b) `restrictions_lint.py` is unbuilt and that Kit §9 still says "Golden (candidates)"; (c) `prepare_judging.py` reads only the pilot tree's `<subject>/<tier>` folders (the demo is linked in as `physics/diki_v2` for this cycle), and whether model judges can hear audio is unconfirmed. **Effort (est.):** 1 day.

### IP-07 · P0 · Release obligations that moved off screen
**Closes:** A5-06, A5-13  
**Cause** (business layer against pipeline): playbook §2.3 makes ExamLeaf the audience channel; Q-COMM bans "free lesson" copy; PD-20 moved the AI declaration to upload.
**Fix:** run the upload gate on every post (`06_QA_GATES_and_RELEASE.md` §6.4: description line, YouTube toggle, Meta label, C2PA kept); educational accounts Professor Diki Simplified, commerce accounts ExamLeaf; clear the name; confirm commercial use of the narration plan; `Try the free lesson on <topic>` (PD-14).  
**Control:** human disclosure gate plus GS (two identities); the packaging schema requires `ai_voice_disclosure`. I found no code that writes or checks the sidecar for `concept_short_60` (grep of *.py).  
**Owner:** business layer. **Status:** planned; founder pending: name clearance and "Diki" pronunciation (A5 §6); channel split; Q-COMM waiver (`MIGRATION_LOG.md` §4); `strings.json` `cta_options` still offer "…free lesson below"; Free plan listed non-commercial (`ELEVENLABS_SETUP_2026-10-16.md` §4.1); counsel's O-5 (does Path B need a visible label?) is open and PD-20 was decided ahead of it. **Effort (est.):** decisions unknown; sidecar validator 1 day.

### IP-08 · P1 · Proof run: the first positive build
**Closes:** no finding; supplies the evidence for IP-02 to IP-06.  
**Cause:** no positive fixture exists; 07 §5 names the demo as the real positive test.  
**Fix:** finish `demo/physics_v2` on v2.0.x under PD-17 to PD-21, narrate, render, run A1–A21, blind-judge against the original, run `scorecard.py`.  
**Control:** every check named above, A9 double render, `scorecard.py`.  
**Owner:** QA. **Status:** in progress: another builder rewrote the script, fixture and scene (fixture now has only the two end-card lines); the three static checks pass (§4); `build_notes.md` (19:27) still describes the PD-01 to PD-16 build; no narration, render, QA or judging folder. **Effort (est.):** about 2 days after the design system lands.

### IP-09 · P1 · House identity, colour roles, size, type
**Closes:** **A2-10**, A2-06, A2-07, A2-08, A2-09, A2-16, A4-08, A6-07, A2-11, A4-06, A4-07  
**Cause** (design system): briefs assigned a style per video and `05_style_guides` chose per scene; placeholder insets; unpinned fonts; template `backOut` and word-by-word headlines.
**Fix:** PD-08 one system, then PD-19 collage; colour by meaning; true subscripts; whole headlines; a card lane for tables and definitions (PD-18).  
**Control:** `build_scene.py` structural bans (CSS transitions, elastic easing, Unicode subscripts); `qa_scene.py` (W_CARD_* per PD-18); A16. Planned: a cross-video identity gate (A4's A19 is not in `qa.py`).  
**Owner:** design system. **Status:** in progress: v2.0.x rebuild by another builder; not assessed; A2-11 and part of A2-16 are closed by decision (§3). Open (`05_DESIGN_SYSTEM.md` §10, tokens): fonts not vendored, insets still placeholder, no pixel double-render hash test, headline chips can still carry role hues; four components unbuilt (roadmap Phase 2). **Effort (est.):** hand-over unknown; fonts 0.5 day; insets 0.5 day plus phones; identity gate 0.5–1 day; components 1–2 days each.

### IP-10 · P1 · Teaching craft
**Closes:** A1-03, A1-04, A1-05, A1-06, A1-08, A1-13, A1-14, A1-15, A1-19, A1-21, A1-23, A1-25, A1-31, A1-32, A1-M6, A4-09, A6-01, A6-02, A1-11, A1-16, A1-26, A1-33, A6-03, A6-08  
**Cause** (script): the slots had no intuition or analogy rung; closure pushed NCERT sentences (SCRIPTING §14); four tags; the "subset of narration" rule forced "Pause and predict".
**Fix:** `03_PROFESSOR_DIKI_SCRIPT_FRAMEWORK.md`: creator's flow over seven obligations, pin before turn, faded step, plain-meaning terms, one analogy with its non-mapping, banned phrases.  
**Control:** `check_pd_script.py`; skill checklist; exemplars.  
**Owner:** script skill. **Status:** done on paper: framework v1.0.0, `skills/professor-diki-script/`, two exemplar scripts, demo script OK. Planned: the skill is not installed under `~/.claude/skills` or registered in `12_` or `15_`; ANL appears in `concept_short_60.md` but no graph schema validates it (the demo uses SIM); no biology exemplar; no learner has seen any of it. **Effort (est.):** install 2 h; ANL schema 0.5 day; biology exemplar 1 day.

### IP-11 · P1 · Contract, doc and decision-record sync
**Closes:** no finding; keeps IP-01 closed.  
**Cause:** PD-17 to PD-21 landed after the documents.  
**Found by grep:** an AI line on the end card in `DIKI_CONTRACT.md` §6, `04_SIXTY_SECOND_FORMAT.md`, `concept_short_60.md`, `03_PROFESSOR_DIKI_SCRIPT_FRAMEWORK.md`, `professor-diki-script/SKILL.md`, `09_SCORECARD.md`, `06_BRAND_and_AUDIO_IDENTITY.md`, RESTRICTIONS R-030; the decoration ban in `DIKI_CONTRACT.md` §2/§11 against PD-19. PD-01 to PD-21 are missing from `10_DECISIONS_and_CONFLICT_RESOLUTIONS.md` and `DECISIONS_CE.md`.  
**Fix:** edit each; record the decisions. **Control:** `tests/run_all.sh`; a planned lint that no end-card definition lists a disclosure line.  
**Owner:** contract. **Status:** planned. **Effort (est.):** 3 h.

### IP-12 · P2 · Voice, energy arc, audio identity
**Closes:** A1-M2, A3-09, A3-12, A3-M1, A3-10, A3-11, A3-13  
**Cause** (narration): stock British voice George; four tags; no energy target; no emphasis control; no audio identity.
**Fix:** `NARRATION_DIRECTION_SHEET.md` (tags per beat, energy marks, `emphasis_words`); end motif PD-11 and two accents; an Indian-English voice after a plan upgrade.  
**Control:** A19, A21, listening; planned: `voice_id` must resolve to an admitted en-IN registry entry.  
**Owner:** narration. **Status:** partly done: direction sheet, A21, `render.py` audio extras, `brand/motif/` (selftest OK); nobody has listened. The audition was refused with HTTP 402 on the Free plan; its 12 requests are saved in `manifest.json`; tag candidates stay unadmitted until measured. **Effort (est.):** audition 0.5 day after upgrade; native gate unknown.

### IP-13 · P2 · Captions and muted viewing
**Closes:** A6-04, A6-05  
**Cause** (contract, tooling): `PILOT_CONTRACT.md` §3 "nothing else on screen"; `narrate.py` (L240–246) writes one VTT cue per beat.
**Fix:** decide burn-in (`captioned` layout, `caption.js`) or sidecar; chunk at 42 characters by 2 lines, 1.8 s for six words.  
**Control:** planned caption lint.  
**Owner:** design system, narration. **Status:** planned. **Effort (est.):** 1 day.

### IP-14 · P2 · Short-to-lesson linkage and brief conformance
**Closes:** A5-07, A5-10  
**Cause** (business layer, contract): no `parent_lesson_id`; briefs not machine-checked (C01 says 2 Ω, the pilots use 10 Ω); PD-21 moved the lesson code off screen, so A5's "header code equals next_step_ref" test lost its home.
**Fix:** `parent_lesson_id` required, one fixture shared with the lesson, a machine-readable row per C0x brief, pointer check on metadata.  
**Control:** planned schema rule and `brief_conformance` check; neither exists.  
**Owner:** business layer, contract. **Status:** planned; the 2 Ω or 10 Ω choice is open. **Effort (est.):** 1 day.

### IP-15 · P3 · Locale
**Closes:** A5-11  
**Cause:** CE-L5 launches en-IN, Hinglish and hi-IN and puts Assamese at maturity level 5; no Bengali-Assamese font stack or glyph check.  
**Fix:** en-IN, then as-IN with a human voice (RD-42), Hindi later; glyph check; Latin brand inside as-IN.  
**Control:** planned `qa.py` glyph check; native gate per locale.  
**Owner:** narration, business layer. **Status:** planned; v4 lists hi, as, bn; speech-to-speech covers Hindi, not Assamese or Bengali (`ELEVENLABS_SETUP_2026-10-16.md` §1.1). **Effort (est.):** unknown (native reviewers).

## 3. Reversed or amended by founder decision

Do not re-open these. Where a fix is voided, the finding stays in `01_VIDEO_AUDIT.md` as history.

- **PD-15** (vivid, colour by meaning) overrules the external audit's restrained tokens (paper #F5F2EA, ink #16263A), A2 §10 "ink and paper by default" and A4 §3.1 item 7 (`professor-diki@1.0`). Stands: one hue per role, red for mismatch only, contrast ≥ 4.5:1.
- **PD-17** (light vivid, no dark backgrounds) overrules the audit's single cream paper (#F5F2EA) and reverses PD-15's own dark backgrounds. Stands: no dark or deep background audience-facing; saturation, semantics, contrast.
- **PD-19** (paper cut-out collage, every subject) overrules A2-11 and A2 §10's drop list (washi, polaroids, ransom tiles, grain, pencil), A2-16's single type family, A2-10's illustration-skin rule, A4-08's look, and PD-17's "white panels on a pastel page" reading. Stands: one persistent board, nothing empty, labels ≥ 52 px, whole headlines, every string from the fixture. `DIKI_CONTRACT.md` §2/§11 still carry the old ban (IP-11).
- **PD-20** (no AI line on screen or spoken) overrules the disclosure fixes of A1-28, A3-02, A2-15, A4 §3.1 item 3, A5-04 and PD-02. Stands: platform label plus `ai_voice_disclosure` at upload (IP-07). Its note on India's 2026 IT Rules is unverified by me; counsel's O-5 is open (`SOURCES_and_claims.md` S-6).
- **PD-21** (brand at start and end card only) overrules PD-04's persistent header, which A5 adopted as "the only persistent mark", and A5's lesson-code exactness test. Stands: opening ident (frame 0 to 2.5 s), end-card wordmark, lesson code in metadata.

## 4. Checks I ran (read-only, 16 Oct) and what is unknown

- `brand_check.py --selftest`, `make_motif.py --selftest`: OK.
- Demo script (`demo/physics_v2`): `check_script.py` exited 1 at about 20:00 (on-screen disclosure in b14) and exits 0 when re-run just before this file was written; plan 60.63 s, 125 words, 13.5 % silence. `check_pd_script.py` and `brand_check.py`: pass.
- `scorecard.py` on copies of the Opus reports (scratch): science and technical pass; brand, prediction/transfer, persistence, silence/length fail; machine-only totals 32.2, 32.2, 39.7.
- Not run: `tests/run_all.sh`, `qa.py` (they rewrite pilot files).
- Unknown: v2.0.x hand-over date; reviewer names and capacity; font licences; Free-plan quota reset date; counsel's answer to O-5.
