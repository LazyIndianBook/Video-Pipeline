# Learnings ledger (Kit 0.1.0, 16 Oct 2026)

Shape: `13_strong_to_cheap_model_strategy/DOCUMENTATION_TEMPLATES.md` §4. Evidence is the 16 Oct 2026 pilot: n = 1 build per subject × tier, two subjects judged blind on two lenses (pedagogy D1+D2+D3+D7, visual D4+D5+D6+D7, each /20). With n = 1 no confidence interval is meaningful; every effect below is a single paired observation and the revisit trigger is the first Kit-tier re-run. Run ids are pilot ids (`PILOT-1016-<SUBJ>-<TIER>`; no `experiments/ledger/` yet). A = haiku, B = opus (`16_pilot_builds_2026-10-16/judging/mapping.json`). ADR numbers are to be assigned in `14_DECISIONS_and_OPEN_QUESTIONS.md`.

| Score | Physics A (haiku) | Physics B (opus) | Chemistry A (haiku) | Chemistry B (opus) |
|---|---|---|---|---|
| Pedagogy /20 | 14 | 19 | 13 | 19 |
| Visual /20 | 10 | 15 | 12 | 15 |
| Empty middle-zone seconds | 11 | 5 | 8 | 1 |
| QA A1-A9 | 9 pass | 9 pass | 9 pass | 8 pass, A9 warn |

### L-001: QA green does not mean the video teaches
- Date: 2026-10-16
- Claim: A1-A9 passed on both Haiku builds that the judges scored 3-6 points lower on every lens, with 2-4 blocking defects per lens; the gaps are semantic (state, evidence, emptiness), which the A-suite never looks at.
- Evidence: PILOT-1016-{PHY,CHEM}-{HAIKU,OPUS} QA `report.md` (A1-A9 pass, chem opus A9 warn); verdicts list blocking defects for physics A 2 (pedagogy) and 4 (visual), chemistry A 2 and 4 (one shared with B: no captions).
- Models/efforts affected: Haiku 5.5 (kit tier); Opus less so.
- Alternatives considered and rejected: tightening A3 alone (A3 already passes stale states because each glyph matches some fixture field).
- Promoted to: validator — proposed PK-D01…D12 in `skills/examleaf-fill-concept-intro/SKILL.md` §4.1.
- Revisit trigger: PK-D detectors implemented and run on the six pilot builds; they must flag every judge blocking defect (target: 0 misses).
- Status: adopted
- ADR: ADR-TBD-01

### L-002: Empty middle zone is the largest visual gap between tiers
- Date: 2026-10-16
- Claim: The cheap tier leaves the hero zone empty while science is spoken; a hard 0.5 s ceiling plus "hide containers until content" closes most of it.
- Evidence: empty seconds physics 11 vs 5, chemistry 8 vs 1 (`judging/*/verdict_visual.json`); physics A empty circle 4.6 s and empty card 5.8 s during the rule (pedagogy blocking); visual A 10 vs B 15, 12 vs 15.
- Models/efforts affected: Haiku; Opus partly (5 s in physics, empty board 0-3.0 s).
- Alternatives considered and rejected: a 1.5 s ceiling (judge's pedagogy suggestion) — the visual judge measured 0.5 s and it is the stricter rule.
- Promoted to: template + validator — R-001, R-017; skeleton §1; PK-D01, PK-D11.
- Revisit trigger: PK-D01 false positives on decoration-only-but-intentional frames > 1 per video.
- Status: adopted
- ADR: ADR-TBD-02

### L-003: Spoken conditions must be drawn, twice
- Date: 2026-10-16
- Claim: A condition or relationship that is only spoken is lost; it must be a fixture display string on its word and again in the recap.
- Evidence: physics A never showed "constant temperature" or V = I × R (pedagogy blocking); B showed both and repeated them in recap ticks; pedagogy 14 vs 19, D2 3 vs 5 (`judging/physics/verdict_pedagogy.json`).
- Models/efforts affected: Haiku.
- Alternatives considered and rejected: relying on SQ-20 (it checks the condition is spoken, not shown).
- Promoted to: validator + script check — R-002; PK-D02; SCRIPTING_REGISTRY §15 SQ-22.
- Revisit trigger: next physics or maths brief with a stated condition.
- Status: adopted
- ADR: ADR-TBD-03

### L-004: A confrontation needs evidence in the same setup
- Date: 2026-10-16
- Claim: "Name the misconception plus an icon" does not confront it; the counter-example must sit in the worked setup with a change glyph and the struck shortcut, and answer the predict prompt.
- Evidence: physics A s04 bare bulb, no circuit (blocking, both lenses); B lamp in the same loop with "R ↑" and struck ×2; D2 3 vs 5, visual D5 2 vs 3. Chemistry A's confront was rated better than B's (counts-match tally for H2O2) — the evidence half matters in both directions.
- Models/efforts affected: Haiku (physics); Opus (chemistry, weaker evidence).
- Alternatives considered and rejected: a dedicated misconception template with a red cross (style guides ban red crosses).
- Promoted to: template + script check — R-003; skill §3 confront row; PK-D05; SQ-23.
- Revisit trigger: a confront beat whose setup cannot be reused (e.g. history topic) → escalate and add a variant.
- Status: adopted
- ADR: ADR-TBD-04

### L-005: Worked steps need fixture intermediate states, not prose
- Date: 2026-10-16
- Claim: The cheap tier announces the final coefficients; giving the fixture a named state per step (`unbalanced → step1 → balanced`) and binding state switches to cues makes the recount, and removes stale tallies.
- Evidence: chemistry A one-sentence answer and stale tally (blocking, both lenses); B recounts from `coefficients.step1`/`counts.step1`; pedagogy 13 vs 19, D2 3 vs 4 (`judging/chemistry/verdict_pedagogy.json`).
- Models/efforts affected: Haiku.
- Alternatives considered and rejected: letting scene code compute counts (breaks "every glyph is a fixture field").
- Promoted to: schema + validator — R-004, R-005, R-015; skeleton §4 state table; PK-D03, PK-D06; SQ-24.
- Revisit trigger: a brief with more than 3 states (currently escalated).
- Status: adopted
- ADR: ADR-TBD-05

### L-006: Formula typography must be structural
- Date: 2026-10-16
- Claim: Unicode subscript digits depend on the font; only `parts[].sub` spans give lowered subscripts on every machine.
- Evidence: chemistry A baseline subscripts in every formula (blocking, both lenses), visual D4 2 vs 4; the brief itself suggested Unicode ₂ (`chemistry/brief.md`).
- Models/efforts affected: Haiku; the brief template affects all tiers.
- Alternatives considered and rejected: lining figures in Georgia (Haiku tried it; still on the baseline).
- Promoted to: schema + validator — R-006; PK-D04; `editorial-vox.md` §5 glyph test (promotion target).
- Revisit trigger: fonts vendored (COMPARISON L-09); re-run the glyph test.
- Status: adopted
- ADR: ADR-TBD-06

### L-007: Style depth must be pre-built, not described
- Date: 2026-10-16
- Claim: Prose depth rules are skipped by the cheap tier; a skeleton with the style's layers already present is the only reliable carrier.
- Evidence: visual D4 A 2 vs B 4 in both subjects; physics A "no L1/L2/L4 depth layers", headline ~60 px sans; Haiku physics notes "Depth only partly met".
- Models/efforts affected: Haiku.
- Alternatives considered and rejected: longer style-guide digests (Haiku read the guides and still missed it).
- Promoted to: template — written skeleton `templates/concept_intro_scene_skeleton.md` §2; R-009; PK-D08. A coded skeleton is still missing.
- Revisit trigger: a coded skeleton exists; then re-run EV-CI-01/02 and compare D4.
- Status: watch (the written skeleton is rung 5; it becomes adopted at rung 1)
- ADR: n/a until adopted

### L-008: Determinism is "identical procedure", serial, opacity-only
- Date: 2026-10-16
- Claim: Chrome rasters transformed layers history-dependently; determinism holds only for the identical capture procedure, one render at a time, with opacity-only reveals.
- Evidence: COMPARISON §1 L-01 (PSNR ≈ 45 dB across orders; byte-identical MP4 over three identical runs), L-02 (2/831 frames mismatched under concurrent renders; chemistry opus A9 warn); Haiku chemistry 10/11 reverse seeks differed until transforms were removed.
- Models/efforts affected: all tiers (template default).
- Alternatives considered and rejected: Chrome flags (`--disable-gpu`, `--disable-lcd-text`, font flags) — none fixed it.
- Promoted to: validator + lint — R-011, R-012, R-013; A9; lint W03 → error (proposed).
- Revisit trigger: Chrome version change, or any A9 mismatch on a serial render.
- Status: adopted
- ADR: ADR-TBD-07

### L-009: Shared pipeline defects hide inside tier comparisons
- Date: 2026-10-16
- Claim: The 0.6 s lead-in drop hit all four judged builds equally; QA must check video length against the timeline before judging, or judges score sync for a pipeline fault.
- Evidence: MP4 vs timeline 73.27/73.87, 71.33/71.93, 72.73/73.33, 72.60/73.20 s (`judging/*/verdict_visual.json`); A1-A9 missed it.
- Models/efforts affected: none (pipeline).
- Alternatives considered and rejected: shifting cues by −0.6 s (would hide the root cause).
- Promoted to: validator — A10 in `tooling/qa.py`; fix in `tooling/narrate.py`; R-010.
- Revisit trigger: first re-render; A10 must pass on all six.
- Status: adopted
- ADR: ADR-TBD-08

### L-010: Fixture asserts and the hook rule transfer to the cheap tier
- Date: 2026-10-16
- Claim: Hard, checkable rules transfer: Haiku caught the brief's wrong oxygen count with an assert and cut the hook's answer leak, as Opus did.
- Evidence: PILOT-1016-BIO-HAIKU and BIO-OPUS build notes (O 18/18 vs the brief's 24/24; "Not mainly from the soil" removed); `biology/brief.md` corrected.
- Models/efforts affected: Haiku and Opus equally.
- Alternatives considered and rejected: none.
- Promoted to: validator — R-019, R-007; SQ-02, SQ-04.
- Revisit trigger: a brief error that passes both tiers.
- Status: adopted
- ADR: ADR-TBD-09
