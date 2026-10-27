# Animation QA rubric

**Scope.** The animation-specific checks owned by `examleaf-anim-qa`, layered on `examleaf-visual-qa` and `examleaf-audio-caption-qa`. Project-wide gates live in `07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md`. This rubric adds to them and never relaxes them.

## 1. Severity classes

| Class | Meaning | Release effect | Waiver |
|---|---|---|---|
| **critical** | Wrong, hidden or untraceable science, an early answer reveal, a broken determinism contract, any full-frame flash or a seizure-risk flash pattern, tofu | Blocks | **Never** waivable. Fix and re-run |
| **major** | Likely to mislead or exclude: text under platform UI, short holds, off-cue reveals (other than early answers), a flashing tile, loudness off target, broken conjuncts, camera motion during labels | Blocks | A named human reviewer, with a reason, recorded in the report |
| **minor** | Polish: zone membership, small layout drift inside the safe rect | Logged | n/a |
| **incomplete** | A required check has no evidence | Blocks | Produce the evidence |

The status is `pass` only when there are no critical findings, every major finding has a waiver, and nothing is incomplete.

## 2. Checks, evidence and owners

| # | Check | Evidence file | Tool | Default severity | Owner of the fix |
|---|---|---|---|---|---|
| Q1 | Determinism: double-render frame hashes equal (#17) | harness checker output | `04_harness_contract/determinism_hash_check.py` | critical | examleaf-motion-harness / scene author |
| Q2 | Canvas bounds: non-decor elements inside 1080×1920 | `safe_zone_report.json` | `safe_zone_check.py` | critical | scene author |
| Q3 | Safe rect: text-like roles inside the union of platform insets, side ≥ `zones.side_margin_min_px` (96 px, 15 Oct 2026) (#51) | same | same | critical for label/equation/critical; major otherwise | examleaf-vertical-adapt |
| Q4 | Headline hold ≥ 1.2 s [N60] (× 1.5 for hi/as/bn [Recommendation]) (#50) | same | same | major | examleaf-cue-sheet / scene author |
| Q5 | Equation visible until narration reading end + 0.5 s (report §7.5) (#50) | same | same | major | same |
| Q6 | Reveal within one frame of its cue (#63) | same (`--cues`) | same | major | examleaf-cue-sheet |
| Q6a | Answer never visible before its cue (protected think window; answer cues from `meta.answer_protection` or `answer: true`) — added 15 Oct 2026 | same (`--cues`) | same | **critical** | examleaf-cue-sheet / scene author |
| Q7 | Caption never covers a label or equation while both are visible | same | same | major | examleaf-vertical-adapt |
| Q8 | No camera push-in or shake while a label or equation is visible (#64) | same (`camera` samples) | same | major | scene author / examleaf-procedural-2d |
| Q9 | Flash: no whole-frame flash at all, and never > 3 flashes/s on the whole frame (both critical since 15 Oct 2026); ≤ 3/s per tile (major) (#56) | `flash_report.json` | `flash_check.py` | critical / major | scene author; style guide swaps the transition |
| Q10 | Science text equals the fixture field (DOM) (#12) | `text_diff.json` | `text_fixture_diff.py` | critical | fixture owner or scene author (never edit fixtures to match) |
| Q11 | Display text equals the approved script (#11) | same | same | major | scene author |
| Q12 | No untraceable science-looking text (accuracy invariant, report §9) | same | same | **critical** (15 Oct 2026; was major) | scene author |
| Q13 | No text in raster assets (#54) | intake log + OCR/human | mcp-orchestrator intake | critical if science-like | mcp-orchestrator / selective-generation |
| Q14 | Indic: no missing glyphs; no cluster split at a mark, joiner or virama (#55) | same + coverage log | `text_fixture_diff.py` (+ optional fontTools) | critical (tofu) / major (split) | examleaf-kinetic-typography |
| Q15 | Final-mux loudness −16 LUFS ±1, TP ≤ −1 dBTP (pass at ≤ −0.9) (#39) | `final_audio_qa.json` | narration `cli qa` | major | examleaf-audio-production-engineer |
| Q16 | Phone-size human review with the safe-zone overlay | reviewer note | human | — | — |
| Q17 | Decoration does not contradict the science: no wobble, boil or arrow that changes a taught angle, ratio or direction (report §7.13) | reviewer note | human, with fixture alongside | critical if contradicted | scene author |

Q1, Q2–Q8, Q9, Q10–Q12 and Q14 are **required** for every rendered animation scene. Q15 is required for every muxed output (lesson, Reel). Q13 is required whenever raster MCP assets exist. Q16 and Q17 are required before release.

## 3. Extra tests per check

- **Determinism (Q1).** The harness author defines the procedure (two renders, frame hashes compared) in `04_harness_contract/contract.md`. The benchmark plan uses the same measure: "identical frame hashes across two renders" (report §2.6). Record the render-box ID, because headless WebGL can vary by machine (#65).
- **Font coverage (Q14).** Optional pass in the approved environment:
  ```python
  from fontTools.ttLib import TTFont
  cmap = TTFont(font_path).getBestCmap()
  missing = sorted({f"U+{ord(ch):04X}" for ch in text if not ch.isspace() and ord(ch) not in cmap})
  ```
  Put `missing` into `dom_text.json` items as `missing_glyphs`. This proves code-point coverage, not shaping. Conjunct shaping still needs a native reader on phone-size frames (report §11 item 10).
- **DOM text dump (Q10–Q12).** Use `templates/dom_dump_snippet.js` after each `seek(t)`. Elements carry `data-qa-id`, `data-qa-role` and optionally `data-qa-cue`, `data-qa-lang`, and `data-qa-part` (for animated spans). The fixture-bound elements get their IDs from the scene props, which tie them to fixture fields.

## 4. Things this rubric does not judge

- Teaching quality, pacing pedagogy and humour (ST and NA reviewers).
- Contrast and colour-only encoding: covered by visual-qa ("palette and contrast verified on actual frames at phone size", `06_QA_GATES_and_RELEASE.md`).
- Caption wording and timing: audio-caption-qa.
- Music presence under explanations: the audio stage (policy AD-15). QA notes it if heard.

## 5. Report hygiene

- One report per artefact hash. A changed artefact means a new report; never edit an old one.
- Each defect records `severity`, `edge_case`, `element`, `time_s`, `message`, `owner` and `waiver` (`{by, reason, at}` or null).
- Waivers are recorded by a human in the review flow. The authoring agent cannot add one. A local JSON file is not authentication; production uses the authenticated review identity.
