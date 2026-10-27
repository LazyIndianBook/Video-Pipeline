# 08 · ExamLeaf Production Kit, v0.1.0 (16 Oct 2026)

**What it is.** The Kit is the set of rules, skills, templates and records that let a cheap model (Haiku-class) build a vertical ExamLeaf lesson that matches what the strong model builds. It is the artefact described in `13_strong_to_cheap_model_strategy/STRATEGY_strong_to_cheap_models.md` §4, written in the shapes of `13_strong_to_cheap_model_strategy/DOCUMENTATION_TEMPLATES.md`. Version 0.1.0 covers one format: `concept_intro` (60-70 s, 1080×1920, five scenes).

**Status: PROPOSED.** Nothing here has been re-run on the cheap tier yet. Each rule says how it is enforced; rules whose detector is only "proposed" are checked by the pre-submit checklist and the judge until the detector exists.

## Provenance

- **Six pilot builds** on 16 Oct 2026 (`16_pilot_builds_2026-10-16/`): physics (Ohm's law, doodle-handdrawn), chemistry (balancing H₂ + O₂, editorial-vox) and biology (photosynthesis, paper-collage-vertical), each built by Opus 5.5 (reference tier) and Haiku 5.5 (kit tier) from `PILOT_CONTRACT.md`.
- **Four blind verdicts** (`16_pilot_builds_2026-10-16/judging/{physics,chemistry}/verdict_{pedagogy,visual}.json`; A = haiku, B = opus per `judging/mapping.json`). Opus won all four: pedagogy 19 vs 14 (physics) and 19 vs 13 (chemistry); visual 15 vs 10 and 15 vs 12. Biology is rendered but not judged.
- The six build notes (Opus Kit cards; Haiku guide-failure lists), the QA reports (`<subject>/<tier>/qa/report.md`, A1-A9) and the lead's gap table (`COMPARISON_and_GAPS.md` §1, L-01…L-17).
- No `experiments/ledger/` exists yet. Evidence is cited by verdict file, QA id and pilot run id `PILOT-1016-<SUBJ>-<TIER>`, n = 1 per cell.

## Files

| File | What it holds |
|---|---|
| `RESTRICTIONS.md` + `restrictions.json` | 19 rules R-001…R-019 (§2 shape), each with enforcement and a negative test id |
| `skills/examleaf-fill-concept-intro/SKILL.md` | The per-archetype guide (§1 shape): slot table per scene archetype, default path and escape hatch, 14 rules with detectors, checklist, 3 evals, and the proposed detectors PK-D01…D12 |
| `templates/concept_intro_scene_skeleton.md` | What every scene contains per zone, the mandatory layers of the three styles, the cue-naming convention and the state-table rule |
| `EDGE_CASES_pilot.md` | 14 pilot defects EC-101…EC-114 (§3 shape) |
| `LEARNINGS.md` | 10 entries L-001…L-010 (§4 shape) with the score evidence |

## How a cheap model uses it (read order)

1. The lesson brief, then `PILOT_CONTRACT.md` (or its production successor) for schemas and tooling.
2. `skills/examleaf-fill-concept-intro/SKILL.md` §1-§3: check the route, take the default path, fill the slot table for each scene.
3. `templates/concept_intro_scene_skeleton.md`: build each scene zone by zone; write the state table before any markup.
4. `RESTRICTIONS.md`: the hard rules; read the statement column only.
5. The named style guide's Digest (`05_style_guides/<style>.md`), only for colours and shapes the skeleton leaves open.
6. Before submitting: the skill's §5 checklist and §7 verification. `EDGE_CASES_pilot.md` and `LEARNINGS.md` are for the lead and for Kit maintenance, not for the build prompt.

## Still missing (before 0.2.0)

- **Detectors:** PK-D01…D12 are specified, not implemented (target: `03_skills/examleaf-anim-qa/scripts/`); A10 exists in `tooling/qa.py` but no report has run it yet.
- **Negative tests** NT-101…NT-119 are named, not written into `06_prompts_and_templates/negative_tests.md`.
- **A coded skeleton** (`templates/concept_intro/component.js`, `params.schema.json`, `TEMPLATE.md`, golden hashes; strategy §4.6). The written skeleton is the stop-gap.
- **Exemplar cards:** golden cards from physics/opus and chemistry/opus and negative cards from the Haiku builds (strategy §4.5); none carded.
- **The Kit-tier re-run** of the three briefs (skill §10 evals), and the biology judging.
- **Vendored fonts** (`05_style_guides/README.md` §12); every face named here is a pilot fallback.
- **Capability ledger, model profiles, verifier spec** (strategy §4.7-§4.9): not started.
- **Promotion** of the pilot fixes into the contract, template and style guides (COMPARISON §1 "Promote to" column) and the ADRs for L-001…L-010.
- **Open conflict:** burned-in narration captions (production rule D7) versus the contract's "nothing else on screen" (EC-114).

**v0.1.1 (16 Oct 2026, after the Haiku re-run).** R-020…R-026 added from `16_pilot_builds_2026-10-16/judging/physics_v2/`. Measured effect of v0.1.0 on the Haiku physics build: visual lens 10 → 14 of 20 (sync 2 → 4, conformance 4 → 5), empty middle-zone seconds 11 → 4.5; pedagogy lens unchanged at 14 of 20; style recognisability unchanged at 2 of 5. Prose rules the cheap tier skipped are now scheduled as template defaults and detectors (PK-D13…D19), per the closure-rung rule.

