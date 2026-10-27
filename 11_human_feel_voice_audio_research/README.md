# 11 · Research: making vertical AI-made lessons feel human-crafted (voice, dubbing, pacing, music)

**Question researched (14 October 2026):** how to make ExamLeaf's vertical (9:16, mobile-only) lessons and
Reels, audio above all, feel human-crafted rather than AI-made so students appreciate them. Specific concerns:
emotional voice-over in Indian languages (English → Hindi / Assamese), "generate with emotion, then dub via
Sarvam" while preserving emotion and speed, what microdramas do with pacing and why fast speech hides AI
artefacts, and whether a background tune or jingle can hold attention and build brand recognition.

## Files

| File | What it is |
|---|---|
| **`PLAYBOOK_human_crafted_vertical_video.md`** (pass 2, start here) | The end-to-end playbook (~8,500 words): direct answer on low-volume music beds, the human-feel model, a 15-step production SOP (English master → Hindi/Hinglish), a 41-row tricks/tips/hacks catalog with settings, tools-and-settings table, audio spec sheet, sonic branding plan, "real humans, real emotions" operating rules, A/B test plan, skills/automation stack, open questions, sources |
| `SOURCES_and_claims_pass2.md` | Every [N#] claim behind the playbook with quote, URL, source kind and verification status |
| `REPORT_human_crafted_feel_vertical_videos.md` (pass 1) | The first, narrower report: Sarvam capabilities, listener-perception evidence, microdrama market facts, music licensing case, YouTube labelling; provider table; A/B plan |
| `SOURCES_and_claims.md` (pass 1) | Every [S#] claim behind the first report (cited as [P-S#] inside the playbook) |

## How it was produced

Two deep-research workflow runs (fan-out → fetch → adversarial verify → synthesize), run by Fable 5.1 as lead, Sonnet 5.5 for search/fetch/verify, Opus 5.5 for synthesis.

**Pass 1 (report):** 5 angles (emotional Indic TTS and dubbing; human-vs-AI voice perception; microdrama conventions; music, jingles and sonic branding; vertical craft and AI labelling).

| Phase | Agents | Result |
|---|---|---|
| Search | 5 | 41 unique sources |
| Fetch + claim extraction | 5 | 15 sources read, 66 claims, 48 unique after dedup/cap |
| Adversarial verification, two lenses per claim (source-support; currency-and-contradiction); killed only when both refute | 12 | 39 survived, 9 killed |
| Synthesis | 1 | Report |

**Pass 2 (playbook), after the user widened scope to Hindi and asked for every practitioner trick, tutorial, skill and tool:** 8 angles (TTS humanizing tutorials; Hindi/Hinglish AI voice; performance capture and voice conversion; audio post-production humanization; measured microdrama and short-form craft; sonic branding and music-while-learning; visual human signals and AI labelling; skills and automation stacks). Searches deliberately included YouTube tutorials, Reddit/forum threads, creator blogs, GitHub repos and vendor docs.

| Phase | Agents | Result |
|---|---|---|
| Search | 8 | 84 unique sources |
| Fetch + claim extraction | 8 | 24 sources read, 152 claims, 80 unique after dedup/cap |
| Adversarial verification, two lenses per claim | 16 | 76 survived, 4 killed |
| Synthesis (also folds in the 39 pass-1 claims) | 1 | Playbook |

Caveats: a single research pass on one day; only the top 15 of 41 sources were read in full; "contested" claims
had one of two verifiers refuse to confirm them and should be re-checked before relying on them; vendor
capabilities (especially Sarvam, ElevenLabs, Gemini TTS) change quickly, so re-verify against current docs
before buying. Nothing was auditioned or tested with students.

## How this connects to the rest of the project

- Voice pipeline and provider decisions feed `05_narration_system/` and the narration sub-pipeline in
  `07_end_to_end_pipeline_instructions/04_NARRATION_SUBPIPELINE.md`.
- Pacing conclusions sit on top of the Super Teacher targets in `03_super_teacher_framework/`.
- Music and sonic-branding decisions change the "music off by default" rule in `02_learning_psychology/`
  only where this report says the evidence supports it.
- Vertical-only output and AI-disclosure obligations affect `07_end_to_end_pipeline_instructions/05_SHORTS_and_REELS_PROCEDURE.md`
  and `06_QA_GATES_and_RELEASE.md`; record any change as a new Runbook decision in
  `07_end_to_end_pipeline_instructions/10_DECISIONS_and_CONFLICT_RESOLUTIONS.md`.

## Corrections applied 15 Oct 2026 (end-to-end audit)

`14_end_to_end_audit/AUDIT_REPORT_2026-10-15.md` found that parts of the playbook conflicted with the runbook. The playbook was corrected in place (each change marked *15 Oct 2026*, with a summary addendum under its lead's note). The research findings and citations are unchanged; [Recommendation]/[Hypothesis] labels are kept.

| Topic | Was | Now | Basis |
|---|---|---|---|
| Pause cap (audit M9) | "Scripted pauses are capped at 3 s"; Step 8 "up to 3 s maximum" | 3 s applies only to **TTS break tags**. Protected think windows follow **RD-11**: room-tone insert, **default 6 s**, 5–8 s range (4 s for a binary choice), answer hidden; or `pause-video` | RD-11 |
| Path A wording | Teacher may change wording; no check | ASR diff of every keeper take against the **approved script** (`qa.transcript_check`); any change returns to **GA** on a new bundle hash | 07/03 GA, 07/06 §5 |
| Disclosure (audit M2) | One "performed by" wording, a recommendation | Release blocker (RD-45) with two templates: **Path A** "Performed by [Teacher]; voice converted with AI." **Path B** "AI-generated narration; script by [Teacher/author, or the Professor Diki Simplified team]." | RD-45 |
| Reels per lesson | "3–5 Reels/Shorts cut" | **1–3 recomposed complete units** (more only after the GS gate holds) | 07/05 principles 1–2 |
| Renderer | "Remotion / manim-voiceover" | **HyperFrames** default master timeline; Remotion benchmark only; Manim inserts | 12 AD-01 |
| Confidence line | "you've got this" outro | Conditional confidence tied to a visible capability | 03 Super Teacher rules (Step 9) |
| STS processor | Segmind "third party", no admission | Any third-party STS processor passes **07/07 admission** and is named in the performer's consent | 07/07 §2, §4, §7 |
| Music | "Sonic logo and music composed by a person"; beds 20–24 dB under speech; recap bed | **Muted under teaching** (spoken recap included); **owned sonic logo, commissioned**; **code-generated beds** for Reel hooks/CTA, transitions, SFX, intros/outros and prototypes, never called human-composed; 15–20 dB in those placements, 20–24 dB only for a T2 A/B arm | 12 AD-15, AD-37 |
| TTS cost | not discussed | Lean-floor cost cases assume Gemini-class TTS ≈ $0.14/lesson, **≈ $0.28 from 1 Jan 2027**; lean floor is Path B only | 08 E.6; 13 §7.13 |

Status is unchanged: everything in this section is researched or proposed; nothing was auditioned, dubbed, mixed or tested with students (`09_research_and_evidence/VERIFIED_vs_PROPOSED.md` Part H).
