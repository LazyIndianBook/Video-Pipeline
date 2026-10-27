# 06 · Brand and audio identity: Professor Diki Simplified (v1.0.0)

**Status (16 Oct 2026):** built; both selftests pass; motif measured with FFmpeg; nobody has listened yet. Inputs: digest §1–§3 and §6, PD-01 to PD-09, A3. `audit/A5_brand_playbook.md` did not exist, so §5 comes from my own grep of ROOT (excluding `00_source`).

## 1. Identity principles

1. **Recognised by how it explains, not by logo time.** The identity is one persistent board that changes, colour by meaning, a prediction the learner can get right, a transfer question and a precise, warm voice. The brand takes about 1.5 s of screen attention per video, with no intro and no logo animation.
2. **One name.** On screen and spoken: exactly "Professor Diki Simplified". ExamLeaf is the publisher. It appears only in publisher metadata (channel owner, copyright, sidecar `publisher`, C2PA producer, MP4 artist tag) and in an optional last description line, "Published by ExamLeaf." "Super Teacher" stays an internal persona name.
3. **Trust first.** No brand line makes a claim, a guarantee or an exam promise. Disclosure is honest and visible.
4. **Owned and deterministic.** Assets are text or seeded code. There are no font files, samples, stock music, avatars or celebrities.
5. **Momentum (digest §6).** With no jingle, the first word comes at ≤ 0.6 s. The accents confirm the learner's own success. The end motif resolves "question → answer" right after the learner has solved the transfer. Measured by time-to-first-word, by accents falling only on storyboard `payoff`/`mismatch` events, by the motif following the transfer, and by the D8 judge score (PD-09).

## 2. Visual brand rules

| Element | Asset | Geometry (1080 × 1920) | Colour |
|---|---|---|---|
| Header "PROFESSOR DIKI SIMPLIFIED · <lesson code>" (PD-04) | `brand/header_lockup.svg` | 864 × 56 box at x 96, y 250 (top of the title zone). Brand run 32 px, `textLength` 520. Dot at x 546. Code 28 px at x 566, pattern `^[A-Z]{3}-[A-Z0-9]{2,8}-[0-9]{2}$`. Headline starts at y ≥ 318 | Ink #16263A; dot and code #526173 |
| Wordmark | `brand/wordmark.svg` | 1040 × 96, 64 px, baseline 70, `textLength` 1000. "PROFESSOR DIKI" at weight 800, "SIMPLIFIED" at 500 | Ink on transparent |
| End card | `brand/endcard.svg` | Stacked wordmark at 96 px, baselines 820 and 926, `textLength` 840. Rule at y 988. Disclosure slot at baseline 1086, 44 px. "Free lesson: <topic>" at 1162, 44 px, topic ≤ 26 characters. Shrink to 40 px before wrapping; never truncate | Paper #F5F2EA, ink |

- **Fonts:** `Inter, 'Noto Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif`, by name only. `textLength` fixes the run widths whatever font is used as the fallback. A headless-Chrome render with Helvetica Neue fitted every box. Production renders still need the vendored Inter (RD-23).
- **Placement:** the header is static for the whole video in the persistent scene (PD-03). The end card is that scene's final state, not a cut. End-card lines must be literal text nodes or `data-fx` fixture values; the pilots' runtime-built outro text is invisible to the gate.
- **Hold:** end-card lines visible ≥ 2.0 s (they may appear during the CTA and outro); the 0.8 s tail after the last word holds the motif (A3-07).
- **Never on screen:** ExamLeaf, URLs, QR codes, handles, subscribe/like prompts, prices, scores, logo animation, the Super Teacher name, a science meaning colour used as a brand colour, faces or avatars.

## 3. Audio identity

- **No opening jingle and no logo at the open.** The first word comes at the 0.6 s lead-in.
- **No music under science.** No bed at all in this format (MUSIC §1 policy 1).
- **End motif** `motif/diki_end_motif_v1.wav` (seed 2026): E5 → G5 → C5, onsets 0 / 108.5 / 238.8 ms, short-short-long. A soft mallet tone (12 ms raised-cosine attack), a small three-comb room and an 80 ms release. The rising minor third is the lift of a spoken question; the fall of a fifth onto the tonic is a settled answer. It stays inside one triad at 523–784 Hz, which phone speakers reproduce, with no sub-bass. **Measured:** 0.700 s, sample peak −6.00 dBFS, true peak −6.0 dBTP, −17.2 LUFS. It plays once, 0.1 s after the spoken outro ends, and never under speech.
- **Confirmation accent** `confirm_tick_v1.wav`: C6 with a quiet G6, the answer pitch an octave up. 0.100 s, peak −6.00 dBFS. Plays only on a correct reveal after the learner's attempt.
- **Mismatch accent** `mismatch_v1.wav`: E4 against F4, two near-equal pitches that beat. Low-passed at 1.1 kHz with a soft attack, so it is not a buzzer. 0.140 s, peak −6.00 dBFS. Plays only on `RevealMismatch`.
- **Accent rules:** ≤ 3 per 60 s video (A3-13), each on a storyboard-named event. Never in think, pause, equation-reading or inspection windows. Never within ±250 ms of a spoken number or unit. Never two within 1 s. Level 18–22 dB under the voice (a hypothesis; the mixer owns it).
- **Loudness:** −16 LUFS integrated, true peak ≤ −1.5 dBTP, two-pass linear, re-measured on the final mux. −14 LUFS is only an A/B arm.
- **Voice direction:** a licensed adult Indian-English teacher voice, auditioned on a golden passage (two library voices plus one designed voice; creak is in the rubric; A3-11/12), after the plan upgrade (PD-05, `05_narration_system/ELEVENLABS_SETUP_2026-10-16.md`). Warmth and contrast over volume: stress the word that changes; bright hook, steady mechanism, deliberate formula. No stock phrases (F06–F08). Pauses follow PD-01 (by purpose and difficulty, each labelled).
- **Provenance:** code-composed and owned, never called human-composed; hashes in `motif_meta.json`.

## 4. Disclosure policy (exact strings in `brand/strings.json`)

| Place | Path B (TTS) | Path A (performer + STS) |
|---|---|---|
| End card, slot 1 | "AI-generated narration" | "Performed by <name>; voice converted with AI" |
| Description / `ai_voice_disclosure` | "AI-generated narration; script by <author>; reviewed by <reviewer>." | "Performed by <name>; voice converted with AI tools; reviewed by <reviewer>." |
| Spoken | Only "Professor Diki Simplified." (PD-02) | same |
| Platform | Altered/synthetic toggle, Meta AI label, C2PA kept (07/06 §6.4) | same |

- `<author>` is a named person or "the Professor Diki Simplified team", never ExamLeaf.
- Path A credit stays on the end card and in `performer_credit`.
- Path A wording on Path B audio fails the gate.
- A-direct: end card "Narrated by <name>".
- **Spoken CTA (at most one, after the transfer, before the outro; none at ac0):** "The full free lesson is linked below." · "Try the free lesson linked below." · "The worked example is in the free lesson below."
- **Description:** `{{WHAT_YOU_GET}}` → disclosure sentence → "Free lesson: <title> <link>" → ≤ 3 approved topic hashtags → optional "Published by ExamLeaf."

## 5. Migration list

| File:line | Now → change to |
|---|---|
| `16_pilot_builds_2026-10-16/tooling/pilotlib.py:13` | `DISCLOSURE = "…script by ExamLeaf."` → `OUTRO = "Professor Diki Simplified."`; end-card lines read from `strings.json` |
| `16_pilot_builds_2026-10-16/tooling/check_script.py:40-48, 72-73` | last slot `outro.disclosure` with the exact DISCLOSURE text → `outro.brand` with text == OUTRO |
| `16_pilot_builds_2026-10-16/PILOT_CONTRACT.md:62, 79` | slots end in `outro.disclosure`; "outro shows the disclosure line" → the slots end in an optional CTA, then `outro.brand`; the outro is the static end-card state |
| `15_content_engine_v2/subsystems/SCRIPTING_REGISTRY.md:198, 425` | on screen "ExamLeaf practice question" → "Original practice question" |
| `…/VOICE_and_PERSONA_REGISTRY.md:415-416` | spoken "ExamLeaf practice question." → "Original practice question." |
| `…/VOICE_and_PERSONA_REGISTRY.md:296, 298` | add the §4 end-card variants |
| `…/INTERACTION_and_ASSESSMENT_REGISTRY.md:159`; `15_content_engine_v2/FORMAT_REGISTRY.md:109`; `…/VISUAL_STYLE_and_ANIMATION_REGISTRY.md:228` | "ExamLeaf practice question" → "Original practice question" |
| `…/PACKAGING_and_DISTRIBUTION_REGISTRY.md:237` | the end card carries the voice line → it carries the `strings.json` end-card lines |
| `…/PACKAGING_and_DISTRIBUTION_REGISTRY.md:103, 139` | "free lesson" banned, no URL → founder decision (§7.1) |
| `07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md:205-206` | add: X ≠ ExamLeaf; end-card short line; PD-02 |
| `…/MUSIC_and_SOUND_REGISTRY.md:25, 35, 54, 67` | `music/motif-examleaf`, short logo at the cold open → `music/diki-end-motif`, close only |
| `11_human_feel_voice_audio_research/PLAYBOOK_human_crafted_vertical_video.md:296, 450` | logo at open and close → close only |
| `11_human_feel_voice_audio_research/REPORT_human_crafted_feel_vertical_videos.md:19` | "3-5 s ExamLeaf audio logo" → "0.4–0.8 s Professor Diki Simplified end motif" |
| `04_video_engine/implementation_v2/src/examleaf/visuals.py:78` | `'EXAMLEAF'` header → the lockup text (legacy engine, if revived) |

Internal names (skill ids, schema titles, `<title>` tags) are never rendered and stay. Pilot artefacts are historical evidence and are not edited.

## 6. QA gate

`python3 17_professor_diki_simplified/brand/brand_check.py <build>` is a **blocking** release step, after `check_script.py` and before upload (in v2 it joins Q-COMM/Q-DISC).

- **Fails** on F01–F09 (the reasons are in `strings.json`) in spoken text, on-screen text, fixture strings, title/topic, the MP4 filename or the MP4 title tag.
- **Passes only** if the outro scene shows the brand line, the path's disclosure line and a filled "Free lesson:" line, with no `{{slot}}` left, and the last spoken line is "Professor Diki Simplified.".
- **Selftest:** the positive fixture passes; the negative fixture fails with 7 violations and 4 missing requirements.
- **Current physics pilot:** fails as expected (ExamLeaf spoken in b07; no lockup or end card).

`make_motif.py --selftest` runs in the same suite.

## 7. Open items

1. **"Free lesson" conflicts with PACKAGING §4.1.3, §4.4 and §15.4** (RD-49/CE-68 ban it). The C01 brief and PD-06 require it. Either amend Q-COMM or drop slot 2.
2. **The registry wants a commissioned logo.** Admitting this code-composed motif needs a CE decision row. Until then it is an interim owned sting.
3. **Path A separator:** PD-02 uses "·", the brief uses ";". The gate accepts both; the lead should pick one.
4. **F04 "100%"** has no waiver for a genuine science value.
5. **The ±250 ms SFX-to-number check** belongs in the cue-sheet validator and is not coded yet.
6. **Phone-speaker listen** required before admission.
