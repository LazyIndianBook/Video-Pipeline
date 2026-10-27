# A5 · Brand identity and playbook alignment (16 Oct 2026)

Read-only audit. Evidence: case-insensitive grep of ROOT (minus `00_source`, `17_`); OCR of all 212 one-fps frames; `timeline.json` word times; STT transcripts; ffmpeg metadata; playbook PDF and CSV. Paths: `16/`=16_pilot_builds_2026-10-16, `sub/`=15_content_engine_v2/subsystems, `11/`=11_human_feel_voice_audio_research, `07/`=07_end_to_end_pipeline_instructions, `12/`=12_advanced_animations_with_claude. Baseline is the lead's PD-02/04/10 and `brand/strings.json`; ⚑ marks my deviations. `16/tooling` line numbers are as found at 18:18; the 18:50–18:54 edits (v2 path, A12 brand check) moved them and are noted where they already cover a point. Findings: `A5_findings.json` (A5-01…15); see also A1-28, A3-01.

**Verdict.** The retired brand is spoken once and shown 2.8–5.9 s in all three Opus videos, because the contract, `pilotlib.py` and `check_script.py` require it. No video points to the exact free lesson; none keeps to one idea. 26 authored audience-facing locations (25 carry the literal; `check_script.py` enforces it): 21 must change, 5 are commerce items to confirm.

## 1. Brand inventory

|#|file:line|string|replacement|
|---|---|---|---|
|1-3|`16/{physics:84,chemistry:88,biology:457}/opus/script.json`|b07 "AI-generated narration; script by ExamLeaf." Spoken 65.9–69.9 / 67.1–71.1 / 61.2–65.1 s (word at 69.2 / 70.1 / 64.3 s); on screen to 71.9 / 73.2 / 67.1 s|beat deleted; end card + spoken "Professor Diki Simplified."|
|4|`16/physics/opus/storyboard.md:11`|caption "…script by ExamLeaf"|end-card spec|
|5|`16/PILOT_CONTRACT.md:62` (79 "nothing else promotional")|"text must be exactly: …ExamLeaf."|slots end `close.next_step`, brand; text from `strings.json`|
|6|`16/tooling/pilotlib.py:13` (now `:23`, v1 only)|`DISCLOSURE`|retire the v1 path; read `strings.json`|
|7|`16/tooling/check_script.py:47-48,72-73` (now `:268-269,301-302`)|v1 path requires that string and a last beat `outro.disclosure`; v2 already rejects ExamLeaf and a spoken disclosure|retire the v1 branch (the three builds are v1)|
|8-14|`sub/SCRIPTING_REGISTRY.md:198,425`; `sub/VOICE_and_PERSONA_REGISTRY.md:415,416`(spoken); `15/FORMAT_REGISTRY.md:109`; `sub/INTERACTION_and_ASSESSMENT_REGISTRY.md:159`; `sub/VISUAL_STYLE_and_ANIMATION_REGISTRY.md:228`|"ExamLeaf practice question"|"Original practice question" (CE-31 intact)|
|15-18|`11/PLAYBOOK…:52`; `11/REPORT…:19,74,185`|"ExamLeaf brand voice", "ExamLeaf voice", "ExamLeaf audio logo"|"Professor Diki Simplified voice"; 0.4–0.8 s end motif|
|19|`sub/MUSIC_and_SOUND_REGISTRY.md:25`|id `music/motif-examleaf`|`music/diki-end-motif`|
|20|`04_video_engine/implementation_v2/src/examleaf/visuals.py:78`|`'EXAMLEAF'` drawn on every frame (8 proof MP4s, 32 SVGs; legacy, not Opus)|lockup text if revived|
|21|playbook C03 script (CSV; PDF p.27)|"ExamLeaf connects the explanation to the practice"|delete; keep the no-guarantee clause|
|⚑22-26|C02 p.26 "an actual ExamLeaf question"; C13 p.30 "see how ExamLeaf works"; title "How One ExamLeaf Question Links to Its Explanation" (`07/05…:92`, `01/REEL_BACKLOG_36.md:164`, `01/FULL_business_model…:369`)|commerce or product-demo copy|ExamLeaf may stay; founder confirms|

**Derived, regenerate, never hand-edit** (per build: VTT:22, `timeline.json`, `beats/b07.align.json:31`, `cues/s05.cues.json`, `_preview/s05.synthetic_cues.json`, `scenes/s05.html`, `qa/transcript.json:2`): 26 lines, 6 beat-audio files, 3 MP4s (+3 copies in `16/deliverables/`). Haiku, `haiku_v2` and `judging/` copies carry the same string (out of scope).

**Credit/CTA slots to rewrite (no literal):** `07/06:205-207`; VOICE §3.9:296-301; PACKAGING §4.4, §7:223-225,466,568; `sub/QA_PROFILES_REGISTRY.md:87`; `11/PLAYBOOK:18,348-349,547`; `12/07_benchmark_and_pilot_plan/PILOT_three_test_lessons.md:92` ("brand and call to action text"); `12/06_prompts_and_templates/negative_tests.md:712` (end card may say where to find the book); Kit `SKILL.md:34`, skeleton `:11`.

**Checked, nothing audience-facing:** `03_super_teacher_framework` and `05_narration_system` (the persona is named "ExamLeaf Super Teacher" in docs only; no spoken credit, intro or outro line), `12/05_style_guides`, `12/04_harness_contract`.

**Internal, keep:** ≈3,700 identifier-only lines (heuristic regex; skill ids `examleaf-*`, package `examleaf`, folder and file names, schema titles, cost models) and ≈1,500 internal prose lines; engine comments (`scenes/_src/engine.js:3`, `s0N.html:72`); `<title>` in `scene_template.html:6`; token names (`examleaf_light`); persona id `persona/super-teacher`. **Publisher/commerce, keep:** "Published by ExamLeaf.", About page, ExamLeaf player, C07–C23 commerce briefs. MP4 containers carry no tags (encoder only), by CE-38.

**Gate gap (as found; mostly closed at 18:52).** Nothing scanned the brand: `qa.py` A7 diffs STT against the script that holds the string, so "Examleaf" scored as a match. The new A12 (`brand_check.py`, DOM text, VTT, STT transcript) closes most of it. Still open: A12's transcript scan rides on A7, which skips without `ELEVENLABS_API_KEY` or with `--no-stt` and then passes silently; no final-pixel OCR (Tesseract read "ExamLeaf" in 12 of 212 frames); no sidecar scan; no F10 (`\bDiki\b` outside the exact string "Professor Diki Simplified").

## 2. Proposed wording

- **Path B** (description, `ai_voice_disclosure`): `AI-generated narration; script by Professor Diki Simplified; reviewed by {Reviewer}.` "…the Professor Diki Simplified team" is safer: a bare brand reads as one person (persona rule `no_invented_biography`). A pilot with no human review omits "reviewed by". Keep "AI-generated": pure TTS is not "AI-assisted". Not spoken: `07/06 §6.4` requires a description line, YouTube toggle, Meta label and C2PA; PACKAGING §7 adds the end-card line.
- **Path A**: `Performed by {Teacher}; voice converted with AI tools; reviewed by {Reviewer}.` A-direct: `Narrated by {Performer}; no AI voice processing; reviewed by {Reviewer}.` No brand inside; never Path A on Path B audio. End card: "AI-generated narration" / "Performed by {name} · voice converted with AI".
- **Spoken outro** (after the transfer and the open-loop question) ⚑: `Try the free lesson on {topic}. Professor Diki Simplified.` The first sentence is C01's own CTA plus the exact topic. Drop PD-10's "linked below": link placement differs by channel (`07/05` SH8: the YouTube related-video link needs account access; Reels caption links are unverified). The open-loop question must be answered in the named lesson (SCRIPTING §10; no deceptive cliffhanger).
- **End card**: final state of the persistent scene, ≥2.0 s: "Professor Diki Simplified", the disclosure line, "Free lesson: {topic}" (≤26 characters), a 0.7 s motif after the last word. The header's lesson code must equal the `next_step_ref` lesson's code, so the pointer is exact and testable. Never ExamLeaf, URL, QR, handle, price, subscribe, codes or book-finding text.
- ⚑ **"Free" is a claim.** Emit it only if the destination plays without sign-up (`07/06:228`; C16 guard), bind it to the COPY approval, and withdraw the Short if the designation changes (CE-34). PD-10 cuts across RD-49 (founder, 15 Oct: the pipeline "should not care about what is free and what is not"); the alternative is a platform end-screen element.
- **Watermark**: the static header lockup (PD-04) is the only persistent mark: exact string, no animation, non-essential (platform insets unmeasured), never ExamLeaf, never viewer identity (`01 runbook:288`), no corner bug, no logo at the open. ⚑ Store the exact-case string and uppercase it with CSS, so DOM, OCR and screen readers see "Professor Diki Simplified".
- **Titles**: Short `{hook question} (Class {n} {Subject})`, no brand (the channel carries it); long `{Topic}: Full Lesson in {n} Chapters (Class {n} {Subject})`. No "free/unlock/subscribe" (Q-COMM).
- **Description** (PACKAGING §4.4): what_you_get · condition · audience_line · `Next: {lesson title}, full lesson.` · disclosure · `Script: Professor Diki Simplified. Academic review: {Reviewer}. Published by ExamLeaf.` · sources · last_revised. A "Free lesson: {title} {link}" line needs §4.6 ("nothing is added at upload") amended.
- **Channel**: YouTube and Instagram display name exactly "Professor Diki Simplified" (one account set; playlists by class, subject, chapter, language; handle and trademark unchecked). Facebook Page, ad account, Merchant, site, books and checkout stay ExamLeaf. This amends playbook §2.3. The About page names publisher and reviewers (playbook §5.2); "Professor" must not imply a credential.
- ⚑ `strings.json` `publisher.rule` lists MP4 artist/copyright tags: CE-38 strips container metadata (`PACKAGING:243-245`). Put the publisher in the sidecar and C2PA, or tag after hashing.

## 3. Playbook alignment of the three scripts

- **Exact-lesson CTA: fail ×3.** Last words are the credit; no `next_step_ref`; the v1 `SLOTS` lack the `close.next_step` that F8 requires and F5 allows (V2_SLOTS now has it; nothing checks a `next_step_ref`).
- **Forbidden claims: none** (no success %, guarantee, fear, urgency, "full marks"). Unsourced: biology "can weigh more than a herd of elephants" (`HK-banyan-herd`, no source) and "Many think a plant is built from soil".
- **One idea: fail.** Distinct claim nodes: physics 4, chemistry 5, biology 8; 67–73 s against the 20–60 s cap (RD-19).
- **Privacy: pass** (no data, name, comment, link or code). **Free-learning promise:** nothing gates or sells; nothing delivers it either. C01's "academic review required": none recorded, correct for a pilot.
- **Language:** English with terms and symbols visible: pass. But playbook §4.2 is Assamese-first (Hindi "a future test"); CE-L5 launches en/Hinglish/hi and leaves Assamese to level 5; the render box has no Noto fonts (`PILOT_CONTRACT:71`); `qa.py` has no glyph check.

**Physics vs C01.**

|C01 intent|Opus physics|
|---|---|
|Hook "Double the voltage. Does current always double?"|question at 0.6 s, but the beat runs 10 s; board empty ~3 s|
|One circuit|drawn s01, s02, s04; absent s03, s05|
|Constant conditions stated first|first at 34.4 s, as "temperature" (b04, b06); b05 says "constant resistance"|
|Finish with one question; CTA "Try the free lesson"|predict at 11–22 s only; ends on recap and credit|
|2 Ω: 1 A, 2 A; 45–60 s|10 Ω: 0.2, 0.4 A (the lead's sample keeps 10 Ω); 71.9 s; adds resistance definition, V = I × R, filament lamp|

## 4. The 24 briefs

|ID|Format|Design-system demand|
|---|---|---|
|C01|concept short|persistent circuit, fixture-bound readouts, condition badge, ×2 arrow, transfer question, end card|
|C03|definition→diagram→answer|three stacked panels, verbatim definition card, leader-line callouts, answer skeleton; no marking-scheme chips|
|C04|progressive labels, retrieval pause|part-id diagram, label reveal/hide, collision-free ≥50 px labels, pause plate scaled to part count, rights-cleared art|
|C05|reaction change|structure renderer, atom-map highlight, conditions on arrow, "model only" chip, no invented mechanism|
|C06|two methods|two stacked lanes ≤4 steps, equation ≥63 px, same-result badge|
|C14|three difficulty levels|three cards, neutral level chips (no rank colours), "editorial classification" note|
|C15|review cycle|cycle diagram, paper and video id chips from the catalogue, only existing explanations|
|C16|mistake notebook|handwritten 3-column card, 4-card layout, print render target|
|C18|Assamese variant|locale-swappable layers, Bengali-Assamese fonts (ৰ ৱ), 1.8 s Indic holds, bilingual term chip, human voice, Latin brand|
|C24|14-day plan|14-cell planner, "planning tool, not a promise" chip, no countdown or urgency colour|

All ten also need fixture-bound text, one persistent board (PD-03), literal end-card strings (PD-13), colour by meaning, labelled think plates (PD-01). Hybrid (teaching core only; the commerce wrapper keeps ExamLeaf): C02, C13, C19. Not pipeline: C07–C12, C17, C20–C23.

## 5. Catalogue shape and the 60 s job

Per title: 12×10 + 24×6 + 90 = 354 accepted minutes; six titles = 2,124 minutes at ₹120 = ₹2,54,880 (pp.13–14). Shorts sit outside it: ₹500–1,600 production each (₹11,700 for the ten primary briefs) inside a ₹25,000 envelope that funds "a small creative wave using existing approved assets". So a Short is a recomposed unit of an approved lesson, with `parent_lesson_id` and one fixture shared with that lesson (C01's text says 2 Ω, the pilot and the sample use 10 Ω: fix the brief or the fixture, never one side), one idea plus its condition and one check, measured by qualified lesson starts. It is the entry point, not a chapter replacement: a 10-minute lesson holds about three chapters. Destinations differ: lesson (C01, C04), question explanation (C05, C06), paper unit (C15). Shorts are Path B, lessons Path A (RD-47): both need one brand voice; the pilot used a stock voice.

## 6. Decisions needed

1. "Free" in the master vs platform-added (RD-49 vs PD-10). 2. Channel split vs playbook §2.3. 3. Scope of the five commerce items. 4. Name clearance for "Professor Diki Simplified" and the pronunciation of "Diki": unverified (no synthesis run; add a lexicon entry and an ASR check).
