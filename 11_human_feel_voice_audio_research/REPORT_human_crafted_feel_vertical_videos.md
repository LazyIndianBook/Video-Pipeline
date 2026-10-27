# Making ExamLeaf Vertical Videos Feel Human-Crafted: Voice, Pacing, Music, Signals

Research date: 14 Oct 2026. Scope: 9:16 mobile-only videos. That means 10-minute ASSEB Class 10-12 STEM revision lessons and 20-60 s Reels/Shorts in Indian English, Hinglish, Hindi and Assamese.
Evidence rule: every factual claim cites [S#]. Claims marked "(contested)" were not confirmed by every verifier. Lines marked **[Recommendation]** or **[Hypothesis]** are design judgement, not sourced fact. Where the evidence is thin, the report says so.

> **Lead's note (read together with the rest of the project).** This run verified Sarvam from its own docs but did not re-fetch ElevenLabs, Gemini or Cartesia pages, so Section 2's table marks them "unverified". The project already holds doc-checked facts on them (research date 13 Oct 2026) in `../05_narration_system/TTS_PROVIDER_COMPARISON.md` and `../05_narration_system/FULL_narration_system.md` §2: ElevenLabs' newer model families list **Assamese and Hindi**, and ElevenLabs offers **speech-to-speech** (performance transfer into a licensed target voice), **forced alignment** and dubbing; Gemini 3.8 Flash TTS and Flash-Lite list **Assamese and Hindi** and separate spoken text from `speech_metadata.style` direction; Cartesia Sonic does **not** admit Assamese. That is the practical route for the founder's "perform with emotion, then carry it into Indian languages" idea: a human (or directed) performance → ElevenLabs speech-to-speech into the brand voice, with native-speaker review as a hard gate, rather than text-only Sarvam dubbing. Likewise, Section 4's "no study on music under narration" refers to this run only: `../02_learning_psychology/FULL_learning_psychology_blueprint.md` §1 and §5.5 carry the seductive-details meta-analysis (g = −0.16, 50 studies, March 2026) and the coherence principle that justify the music-off default. Nothing in either place was auditioned; all vendor claims still need the hands-on test in Section 7.

---

## Executive answer: the 10 decisions

1. **Detection is not the main problem. Trust is.** In a 1,326-listener study, appeal was 60% for a human voice and 61% for an AI voice on the first clip [S20][S21]. Listeners mostly cannot tell the difference. Industry players still claim audiences *want* human-made media, though that figure comes from iHeartMedia's internal research, not an independent study [S22]. The goal is therefore "human-*directed*, honestly made" rather than "undetectable AI".
2. **Keep the human in the performance, not only in the script.** For flagship lessons, a real teacher records a guide or reference performance. AI then cleans it, converts it or matches it. Pure text-to-speech stays the fallback for volume content and Reels.
3. **"Generate with emotion, then dub with Sarvam" does not work as stated.** Sarvam Bulbul is a text-to-speech engine. It has no explicit emotion parameter [S5][S16] (contested). The nearest levers are persona choice [S17], temperature [S16] and pace 0.5-2.0x [S3][S18]. Emotion is not carried over from a source track. It has to be *re-directed* per sentence in each language.
4. **Assamese is the gap.** Sarvam's documented language codes do not include Assamese (as-IN) [S15] (contested). KUKU TV, the reference microdrama platform, also launched without Assamese [S24]. **[Recommendation]** Plan a human Assamese voice (a teacher or artist) as the anchor. Treat any AI Assamese voice as a pilot until listening tests pass.
5. **Do not copy microdrama speech speed into lessons.** Fast delivery may mask artefacts, but that is the founder's hypothesis. No source here measures it. Lessons keep the Super Teacher target of 130-155 wpm with protected thinking pauses. Reels may run hotter only in the first 2-3 s hook.
6. **Chunk by beat, not by character limit.** Sarvam caps REST requests at 2,500 characters [S2][S18][S36] and HTTP streaming at 3,500 [S37]. Generating one teaching beat (1-3 sentences) per request gives per-beat control of emotion and pace, which is the main human-feel lever.
7. **Render at 48 kHz.** Sarvam REST supports 44.1 and 48 kHz output [S19][S38]. Streaming tops out at 24 kHz [S4] (contested). Use REST for final renders and avoid resampling artefacts.
8. **Music: an original sonic logo, yes. Wall-to-wall music under teaching, no.** Build a 0.6–0.75 s Professor Diki Simplified end motif (PD-04) and an owned or commissioned bed. Under explanations, duck the music hard or mute it. Never use platform-library film songs on a brand account: the Zee v. Nykaa suit (about Rs 2 crore over 12 Reels) shows the exposure [S29][S30][S33][S34].
9. **Expect labelling and disclose voluntarily.** YouTube began auto-labelling significant photorealistic AI content in May 2026. It says labelled videos are not demoted or demonetised [S11][S12] (contested). Disclosure costs little reach. Being "caught" costs trust.
10. **Decide by A/B test, not by taste.** Measure appreciation, listening effort and delayed recall (24-72 h) for each voice pipeline and each music setting before locking the defaults (Section 7).

---

## 1. Why AI voice-overs sound flat, and what humans do differently

**What the evidence says**

- **Listeners rate AI and human voices about the same on first exposure.** Overall appeal was 60% (human) vs 61% (AI) on the first clip in a 1,326-listener study [S20][S21]. "Flatness" is therefore not mainly a raw voice-quality problem. Modern TTS sounds good on short clips.
- **Audiences say they prefer human-made media,** per iHeartMedia's internal (not independent) research [S22]. Treat this as a directional signal, not a measured effect size.
- **Vendors claim expressiveness but expose few controls.** Sarvam says its voices have "natural intonation and emotional expression" [S5], yet it documents no emotion parameter. Expressiveness comes from persona selection and a temperature knob that trades expressiveness for artefacts [S16][S17] (contested).

**Why a 10-minute lesson still feels "AI"** (practitioner reasoning, not sourced; mark as **[Hypothesis]**)

- **Uniform prosody across long durations.** TTS chooses intonation sentence by sentence and does not "know" where the lesson's emotional arc sits. Over 10 minutes, the repetition of the same contour pattern is what students notice, not any single sentence.
- **No intent behind the pause.** A human teacher pauses *because* they expect the student to think. TTS pauses happen at punctuation.
- **No reaction.** Humans audibly react to their own content ("that's the trick here"), shift register for a common mistake, and slow down on a key equation. Default TTS does none of this.
- **Over-perfect articulation and an identical breath pattern.**
- **Mispronounced domain terms.** Examples are "mole", "ohm", "sin θ", and Assamese/Hindi technical vocabulary. One wrong term breaks the illusion faster than flat prosody does. This is why the existing pronunciation lexicon matters; Sarvam supports `dict_id` dictionaries on v3/v4-flash [S18] (contested).

**Implication.** Human feel comes from *direction* (beat-level intent, pace and pause choices) and *correctness* (pronunciation, register). The base voice model matters less.

---

## 2. Recommended voice pipeline for ExamLeaf

### Pipeline overview

```
Script (EN master) -> direction tags per beat -> [Path A: human guide take] or [Path B: directed TTS]
  -> per-language adaptation (rewrite, not literal translate) -> per-beat generation with mapped pace/persona
  -> lexicon + forced alignment -> timing match to visuals -> QA listening panel -> -16 LUFS master
```

### (a) Direction-tagged expressive generation

**[Recommendation]**
- **Tag every beat in the script** with one of the existing Super Teacher modes (curious / steady / deliberate / light / reassuring), a target wpm inside 130-155, and pause slots (for example `[PAUSE-THINK 1.2s]` after a question and `[PAUSE-WRITE]` while an equation draws).
- **Map each mode to concrete engine parameters.** On Sarvam these are persona, `pace` and `temperature` [S16][S17][S18] (contested). For example:
  - **Deliberate:** pace ~0.9, temperature ~0.4, a steady narration persona.
  - **Curious:** pace ~1.0, temperature ~0.6-0.7, a warm or expressive persona.
  - **Reassuring:** pace ~0.9, a warm persona.

  These values are starting points to tune, not sourced numbers.
- **Generate per beat, not per lesson.** The 2,500-character REST cap [S36] makes this natural anyway. Insert real silence for pauses in the edit, not via TTS punctuation, so that pause lengths are exact and protected.
- **Keep higher temperatures for short beats only,** because higher values are "more expressive but may introduce artifacts or errors" [S16]. Re-roll a beat 2-3 times and pick the best take, the way a director would.
- **Ask for warm or expressive personas by name** on v4-flash, for example `ishita_enhi_customer_expressive` for code-mixed English/Hindi [S17]. Code-mixed text is supported [S15], which matters for Hinglish. Persona names and availability are contested: verify them against the live persona list.

### (b) Human performance reference and performance capture (strongest human-feel option)

**[Recommendation]**
- **Path A (flagship lessons, first 2-3 chapters per subject).** A real teacher records the lesson's guide track in their natural language, scrappy is fine. That track is used either:
  1. **directly,** cleaned with denoise/de-ess and edited; or
  2. **as a performance source for speech-to-speech voice conversion** into the consistent "Professor Diki Simplified voice". This keeps the human's timing, emphasis and pauses while unifying timbre; or
  3. **as a timing and prosody template.** Forced alignment extracts word timings and pause lengths, and the TTS beats are then paced to match.
- **Path B (Reels, long-tail chapters).** Directed TTS as in (a).
- **Consent and contract.** Any teacher whose voice is cloned or converted needs written consent covering scope, languages, duration and revocation. Make this a hard gate.
- **Evidence gap.** No source in this evidence set verifies a specific vendor's speech-to-speech prosody-preservation quality for Indian languages. Test before committing.

### (c) Emotion-preserving dubbing and voice conversion: what is actually supported

**What Sarvam does (as documented, 14 Oct 2026)**

- **Models:** Bulbul v4-flash (latest, recommended, 200+ personas), v3 (default, 30+ voices) and legacy v2 [S14][S35] (contested for S14).
- **Languages:** 11 (10 Indian + English) [S1]. Listed codes include hi-IN, en-IN, bn-IN, ta-IN, te-IN and od-IN, plus code-mixed text. **No as-IN listed** [S15] (contested).
- **Controls:**
  - **Pace:** 0.5-2.0x [S3][S18].
  - **Temperature:** 0.01-1.0, default 0.6 [S16].
  - **Persona styles** encoded in names: news, kids, narration, devotional, expressive/warm [S17].
  - **Pronunciation dictionaries** via `dict_id` [S18].
  - **No explicit emotion parameter** [S5][S16] (contested).
- **Limits:** 2,500 characters per REST request [S2][S36], 3,500 per HTTP stream [S37], and 2,500 per WebSocket message with under 500 recommended [S39].
- **Output:** up to 48 kHz on REST [S19][S38]. Streaming runs 8-24 kHz [S4] (contested). The default is 22,050 Hz base64 WAV [S19].

**What this means for "generate with emotion, then dub with Sarvam"**

Sarvam's documented TTS does **not** take an emotional source *audio* track and carry its emotion across. It takes *text*. The workable version of the founder's idea is:

1. Produce the emotional master in Indian English, with a human guide or directed TTS.
2. Extract per-beat **mode tag + duration + pause map** via forced alignment.
3. Adapt the script into Hindi or Hinglish. Rewrite it rather than translating literally, keeping the same beat boundaries.
4. Generate each beat in Sarvam with the mapped persona, temperature and **pace computed to hit the source beat duration**, clamped to a natural range.
5. Re-insert the source pause map as real silence.

This preserves **speed and structure** deterministically. **Emotion is approximated** through persona and temperature, not transferred.

**Provider comparison**

| Provider / path | Emotion controls | Indic incl. Assamese | Dubbing / speech-to-speech | Pricing | Caveats |
|---|---|---|---|---|---|
| **Sarvam Bulbul v4-flash / v3** | No emotion param. Persona style names, temperature, pace [S16][S17][S18] (contested) | 11 languages; Assamese **not listed** [S1][S15] (contested); code-mixed supported [S15] | Not documented in evidence (TTS only) | Not in evidence: get a quote | 2,500-char REST cap; temperature artefacts; persona list changes |
| **ElevenLabs (v4 candidate)** | **Unverified in this evidence set** | **Unverified** (confirm Assamese explicitly) | Dubbing and voice-changer products exist per general knowledge; **not verified here** | Not in evidence | Test Indic pronunciation and code-mixing |
| **Gemini 3.8 TTS** | **Unverified** (prompt-style direction expected) | **Unverified** | **Unverified** | Not in evidence | Already a project candidate; run the same listening test |
| **Cartesia Sonic** | **Unverified** | **Unverified** | **Unverified** | Not in evidence | Same |
| **Human voice artist / teacher** | Full | Any, including Assamese | N/A; is the source | Not in evidence (get local quotes) | Scheduling; consistency across sessions; consent paperwork |
| **Hybrid: human guide + voice conversion** | Inherits the human performance | Depends on the converter's language robustness (**unverified**) | Yes, by design | Not in evidence | Consent; artefacts on Assamese phonemes untested |

**Bottom line.** Only Sarvam's capabilities are verified here, and only from its own docs. Everything else in the table must be verified with a hands-on test and a written vendor answer (Section 8).

### (d) QA and listening tests

**[Recommendation]**
- **Automated:**
  - Lexicon hit-rate (every technical term in the dictionary).
  - ASR back-transcription word error rate per language, to catch mispronunciations.
  - Forced-alignment check that pauses are at least their protected length.
  - Measured wpm per beat inside 130-155.
  - Loudness at -16 LUFS integrated.
- **Human panel per language:** 5-8 students from the target board plus 1 subject teacher. Each rates a blind 60-90 s clip on a 1-5 scale for "sounds like a real teacher", "easy to follow" and "any word wrong?". Assamese gets a native-speaker gate before *any* AI Assamese ships.
- **Re-roll policy.** Any beat flagged twice gets regenerated or replaced with a human pickup.

---

## 3. Pacing: what microdramas do, what to adopt and what to reject

**What the evidence says about microdramas**

- **Big, fast-growing format.** The Indian microdrama market is projected at $1.5 bn by end-2026 [S6]. KukuTV has 100 M+ downloads [S7]. StoryTV reports 3.5 M+ paid subscribers [S8] (contested).
- **Very short episodes in long series.** Episodes run up to 2 minutes, with 50+ episodes per series [S23]. One regional title is released daily [S27].
- **Vertical is the default.** 90% of Indians consume vertical video on social media, per one article's assertion [S28].
- **Costs are falling with AI.** Production runs about Rs 20,000-30,000 per minute [S9], and AI is claimed to cut this to about a tenth [S10] (contested).
- **Evidence gap.** None of the sources measures microdrama **speech rate, hook timing or cut frequency**. The claim that "fast speech hides AI" is a plausible hypothesis, not sourced.

**Adopt (for Reels, and for lesson openings)**

- **Hook inside the first ~2-3 s:** a question, a surprising result, or a common-mistake reveal. **[Recommendation]**
- **Open loops:** end each lesson segment or Reel with the next question ("but why does the bulb dim?"). This mirrors the series-with-50-episodes logic [S23].
- **Visual change every few seconds** (zoom, new line written, cutaway) instead of faster talking.
- **Episodic packaging:** split a chapter into a numbered series of Reels, published on a fixed cadence (compare the daily release in [S27]).

**Reject for lessons**

- **Fast speech as camouflage.** Learning needs processing time. Keep 130-155 wpm with protected thinking pauses. Speeding up to hide artefacts trades comprehension for concealment. Fix the artefacts instead (Section 2).
- **Melodramatic tone and constant cliffhangers.** These clash with the "no fake enthusiasm" Super Teacher rule.

**Practical rules**

| Segment | wpm target | Pauses | Notes |
|---|---|---|---|
| Reel hook (0-3 s) | top of range (~150-155), punchy | none | One sentence, on-screen text backs it up |
| Reel body | 140-155 | short (0.3-0.6 s) | One idea only |
| Lesson explanation | 130-145 | protected 0.8-1.5 s thinking pauses | Slow down on equations; let the writing animation lead |
| Common mistake / exam tip | 135-150, "light" or "reassuring" mode | pause before the reveal | |

The pause lengths above are design defaults, not sourced values. Tune them with the A/B test.

---

## 4. Background music and sonic branding

**Evidence status.** This evidence set contains **no study** on music under narration and learning outcomes. Multimedia-learning guidance (the "coherence" idea that extraneous sound can hurt learning) is widely cited but was **not re-verified in this run**. The project's existing "music off by default" setting is the safe baseline until the A/B test (Section 7) shows otherwise.

**When to use, duck or mute** **[Recommendation]**

| Moment | Music |
|---|---|
| End motif (close only) | Full level, 0.6–0.75 s |
| Reel hook and transitions | Light bed, ducked ~15-20 dB under voice, or none |
| Concept explanation, derivations, numericals | **Muted** |
| Recap / "you've got this" outro | Light bed allowed |
| Thinking pauses | **Silence**, so the pause reads as intentional |

**Loudness.** Keep the project target of -16 LUFS integrated for the final mix. Speech should dominate. If a bed is used, keep it far enough under the voice that captions-off listening stays effortless. Platform normalisation targets for Reels and Shorts are **not verified in this evidence set**, so check them per platform before finalising.

**Professor Diki Simplified end motif plan (0.6–0.75 s)** **[Recommendation]**
1. **A motif of 3-5 notes,** playable as a sting (logo), a soft bed variant, and a "correct answer" chime. One motif, many uses, is what builds recognition.
2. **Instrumentation with a regional nod** (for example a soft dhol/khol pulse or a pepa-like timbre for the Assamese identity) over a clean modern synth. Test whether students in Hindi markets accept it.
3. **Placement:** once, after the last word of a lesson or Reel; no logo at the open (PD-04), so viewers never wait through a logo before the hook.
4. **Ownership:** commission or compose it with a written assignment of copyright. Register it as part of the brand kit.

**Licensing rules for Reels and Shorts**

- **Zee sued Nykaa** (filed 3 April) over **12 Instagram Reels** using its music, seeking about **Rs 2 crore** [S29][S30]. All 12 were taken down [S31], and the matter was listed for 26 May [S32].
- **Zee's argument:** its Meta licence covers **non-commercial** individual use only, so brand accounts are exposed [S33]. A song being available in the platform music library does **not** by itself grant brands the right to use it [S34].
- **Rule for ExamLeaf (an edtech brand, i.e. commercial):** use only original, commissioned or properly licensed music. No trending film songs, even from in-app libraries. Keep a licence log per asset.

---

## 5. Visual "human-made" signals for 9:16, and AI labelling

**Signals that read as human-crafted** (design practice, **[Recommendation]**; not sourced)
- **Hands and handwriting:** real or realistic stylus writing of equations, synced to the narration via forced alignment. The hand "arrives" slightly before the word.
- **Purposeful imperfection:** a crossed-out wrong step for the common-mistake beat, or a circled answer. Do not add random glitches.
- **Lead note (15 Oct 2026):** a real teacher on camera over Path B (pure TTS) audio must not imply the teacher spoke; use the Path B disclosure template ("AI-generated narration; script by X") or reserve cutaways for Path A lessons. See the PLAYBOOK Step 14 and RD-45.
- **Teacher cutaways:** 1-3 s of a real teacher's face or hands per segment, even in an otherwise AI-voiced lesson. This anchors the "human made this" impression.
- **Local context:** examples from Assam (Brahmaputra, tea gardens, local prices) and ASSEB question-paper styling.
- **Captions sized for phones:** large, high-contrast, burned-in captions in the safe zone (clear of platform UI at the top and bottom). Highlight one key word per line, not karaoke-style on every word.
- **Signature presence:** the same teacher name, sign-off line and sonic logo on every video.

**Labelling obligations and practice**

- **YouTube:** began gradually rolling out automatic labels in May 2026 for videos with significant **photorealistic** AI-generated content, regardless of creator disclosure [S11]. It states that labelled videos will not be demoted or lose monetisation, and that creators can correct mislabels [S12] (contested). Whether an AI *voice* over hand-drawn or animated visuals triggers the label is **not established** by this evidence.
- **EU AI Act:** transparency obligations take effect in August 2026 [S13] (contested). This is relevant only if ExamLeaf distributes in the EU.
- **India-specific synthetic-media rules** are **not covered in this evidence set**. Get a legal check.
- **[Recommendation]** Add a short honest credit, for example "Taught by [Teacher]. Voice produced with AI tools". Combined with real teacher presence, this keeps trust if the content is ever auto-labelled.

---

## 6. Advanced AI tricks that work, and ones that backfire

**Work (or are low-risk to pilot)** **[Recommendation]**
1. **Per-beat generation with mode-mapped parameters** (persona, pace, temperature) plus best-of-N re-rolls [S16][S17][S18].
2. **Pronunciation dictionaries** for every STEM term in every language [S18].
3. **Human guide track, then forced alignment to steal timing and pauses** for the TTS. This is cheap and gives a large human-feel gain.
4. **Human performance, then voice conversion** for consistent brand timbre with human prosody. Quality on Indian languages is unverified, so test it.
5. **Code-mixed Hinglish scripts** written the way teachers actually talk, which Sarvam supports [S15].
6. **Render at 48 kHz** via REST and master once [S38].
7. **Edit-level humanisation:** real silence for pauses, light room tone, occasional natural breath kept in, and a slight speed change on emphasis words.

**Backfire**
1. **Fast speech to hide artefacts.** It hurts comprehension (Section 3).
2. **Maximum temperature for "more emotion".** The vendor itself warns of artefacts and errors [S16].
3. **Cloning a real teacher without written consent,** or implying a human recorded what AI generated.
4. **Trending film music on brand Reels** [S29][S33][S34].
5. **Literal translation followed by TTS.** The rhythm breaks. Rewrite per language at beat level instead.
6. **Fake enthusiasm** ("Amazing! Let's go!"). It violates the persona and is the cliché students associate with AI.
7. **Photorealistic AI "teacher" avatars.** These are the most likely to trigger auto-labels [S11] and the uncanny reaction.

---

## 7. A/B test plan

**Arms (one chapter, for example Class 10 Light, ~10 min, plus 3 Reels)**
- **A:** human teacher voice, as the reference.
- **B:** directed TTS (per-beat modes, lexicon, protected pauses).
- **C:** human guide performance with voice conversion or timing-matched TTS.
- **D:** B plus a light music bed (ducked) and the sonic logo.
- **Languages:** run Hindi/Hinglish first. Assamese runs A vs C only until an AI Assamese voice passes QA.

**Measures**

| Metric | How |
|---|---|
| Appreciation | 1-5 ratings: "feels made by a real teacher", "would watch the next one"; likes, saves and shares per view on Reels |
| Listening effort | 1-5 "how hard was it to follow"; replays and scrub-backs per minute |
| Delayed recall | 5-item quiz at 24-72 h (concept + numerical + common-mistake item) |
| Retention | Average view duration; % reaching the recap; Reel 3-s hold rate |
| AI perception | After rating: "Do you think the voice was AI?", plus whether disclosure changes the appreciation rating |

**Design.** Within-subject where possible, with counterbalanced order. There should be at least ~30 students per arm for directional signals. The evidence gives no power calculation, so treat early results as directional. Ship a default only if B or C is within striking distance of A on recall and effort. Note that the radio study found little first-impression appeal gap [S21], so differences may show up in effort and recall rather than "liking".

---

## 8. Open questions, unverified items and what to ask vendors

**Unverified or contested in this evidence set**
- Assamese support in Sarvam (not listed [S15]), ElevenLabs, Gemini and Cartesia.
- Whether any vendor offers emotion or prosody *transfer* from source audio for Indian languages.
- The exact current persona list and style coverage on Bulbul v4-flash [S14][S17].
- Pricing for every provider (none is in the evidence).
- Whether AI voice over non-photorealistic visuals triggers YouTube or Instagram AI labels [S11].
- India synthetic-media disclosure rules.
- Microdrama speech rates, cut rates and hook timings (no measured data).
- The effect of music beds on STEM learning for this audience.

**Questions to put to vendors in writing**
1. Do you support Assamese (as-IN) TTS today? Which voices? Please send a sample of a STEM paragraph.
2. Is there an explicit emotion or style control, or prompt-based direction? Which languages does it work in?
3. Do you offer speech-to-speech or voice conversion that preserves the source timing, emphasis and pauses for Hindi and Assamese?
4. What are the per-character or per-minute price, commercial-use rights and attribution requirements?
5. What are the character limits, maximum sample rate and support for pronunciation dictionaries and SSML-like pause control?
6. What are your consent requirements and data retention for cloned or converted voices?
7. Are the persona names and voices stable across model versions, so the brand voice will not change silently?

---

## Sources

- [S1]-[S5] Sarvam Bulbul model page: https://docs.sarvam.ai/api-reference-docs/getting-started/models/bulbul
- [S6]-[S10] Hollywood Reporter India, microdrama boom: https://www.hollywoodreporterindia.com/features/insight/indias-microdrama-boom-how-data-desire-and-aritifical-intelligence-are-reshaping-entertainment
- [S11]-[S13] The Next Web, YouTube auto-labelling: https://thenextweb.com/news/youtube-will-now-automatically-label-ai-generated-videos-whether-creators-disclose-them-or-not
- [S14]-[S19] Sarvam TTS convert API reference: https://docs.sarvam.ai/api-reference/text-to-speech/convert.md
- [S20]-[S22] Radio Ink, listeners and AI voice: https://radioink.com/2026/07/07/radio-listeners-cant-detect-ai-voice-but-dont-trust-it-either/
- [S23]-[S28] afaqs!, KUKU TV launch: https://www.afaqs.com/news/ott-streaming/kuku-fm-launches-vertical-microdrama-ott-platform-kuku-tv-8718086
- [S29]-[S34] MediaNama, Zee v. Nykaa: https://www.medianama.com/2026/05/223-zee-nykaa-delhi-high-court-copyrighted-songs-instagram-reels
- [S35]-[S39] Sarvam TTS overview guide: https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/overview.md

The full claim list with quotes and verification status is in `SOURCES_and_claims.md`.
