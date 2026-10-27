# ExamLeaf Human-Crafted Vertical Video Playbook (voice, emotion, pacing, music, visuals)

**Scope:** ~10-minute STEM revision lessons and 20-60 s Reels/Shorts for ASSEB Class 10-12 Physics, Chemistry, Maths and Biology. All vertical 9:16. Languages now: Indian English, Hinglish, Hindi. Assamese comes later, through a human voice.
**Research date:** 14 Oct 2026.

**How to read the citations**
- **[P-S#]** is a claim from the earlier verified register (`11_human_feel_voice_audio_research/SOURCES_and_claims.md`).
- **[N#]** is new verified evidence from this pass. "(contested)" means not every verifier confirmed it. Re-check those before you rely on them.
- **[Recommendation]** and **[Hypothesis]** mark ExamLeaf design judgement, not sourced fact.
- Any number with no citation and no label is not allowed in this document. Where a number is a starting value for testing, it says so.

> **Lead's note (coverage limits of this pass).** (1) The search deliberately targeted YouTube tutorials, Reddit threads and creator blogs, and 84 sources were found, but the fetch tooling cannot read YouTube video transcripts, so creator *videos* contributed titles and descriptions only; the verified tricks below come from vendor docs, engineering blogs, a sound-designer interview, a research paper and a policy page (12 sources carried all 76 surviving claims). Treat any hack seen in a creator video as untested until you try it. (2) The EQ and compression figures in Step 9 and the catalog ([N22]–[N27], [N72]–[N76]) come from two articles about processing AI *singing* vocals; they are sensible starting points for narration, not narration-specific measurements. (3) For ElevenLabs, Gemini and Cartesia language coverage (Assamese and Hindi listed for ElevenLabs' newer models and for Gemini 3.8 TTS; Cartesia does not admit Assamese) and for the music-and-learning evidence (seductive-details meta-analysis, g = −0.16), see `../05_narration_system/TTS_PROVIDER_COMPARISON.md` and `../02_learning_psychology/FULL_learning_psychology_blueprint.md` §1 and §5.5; those were verified on 13 Oct 2026 in the earlier research and are not repeated here.


> **Correction addendum (15 Oct 2026; source: `14_end_to_end_audit/AUDIT_REPORT_2026-10-15.md` M2, M9 and the "Safety minors" and "Other" findings; runbook rows RD-11, RD-41, RD-45 in `07_end_to_end_pipeline_instructions/10_DECISIONS_and_CONFLICT_RESOLUTIONS.md`).** The changes below are made in place, each marked *15 Oct 2026*; the original wording is kept struck through or quoted where it matters.
> 1. **Pauses.** The 3 s cap applies **only to TTS break tags** (the engine limit [N1]). **Protected think windows follow RD-11**: 5–8 s for a simple prediction (4 s only for a binary choice), **default 6 s**, answer hidden, inserted as **room tone** in the edit; writing, drawing or multi-step work uses **pause-video** (learner-controlled). The playbook's 1.2–2.0 s "THINK" beat hold is a short emphasis hold, not the protected window.
> 2. **Path A wording check.** Run ASR on every keeper take and diff it against the **approved script** (narration comparator `qa.transcript_check`, Indic-safe since 15 Oct 2026). Any wording change, ad-lib claim or fake-sensing line goes back to **academic approval (GA) on a new script-bundle hash** before conversion or release.
> 3. **Disclosure** is a release blocker (RD-45) with **two templates**: Path A "Performed by [Teacher]; voice converted with AI." and Path B "AI-generated narration; script by [Teacher/author, or the Professor Diki Simplified team]." Never use Path A wording on Path B content.
> 4. **Confidence lines are conditional** (Super Teacher rules, `03_super_teacher_framework/INSTRUCTIONS_super_teacher_authoring.md` Step 9: praise a demonstrated action conditionally; confidence tied to a visible capability). "You've got this" is replaced by lines such as "If you can count the atoms on both sides without the animation, you can balance the next one" or "Any step you could not do tells you exactly what to practise next."
> 5. **Third-party speech-to-speech processors** (ElevenLabs Voice Changer, Segmind or any other) must pass the **07/07 admission process** (`07_end_to_end_pipeline_instructions/07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md` §2 scoped worker key and approved outbound domain, §4 admission chain) and must be **named in the performer's consent** (§7) before any teacher recording is sent to them.
> 6. **Reels:** 1–3 **recomposed complete units** per lesson (more only after the GS gate holds), not "3–5 cut". **Renderer:** HyperFrames is the default master timeline (Remotion is the benchmark only; Manim for maths inserts), per `12_advanced_animations_with_claude` AD-01.
> 7. **Music policy** (aligned with 12 AD-15/AD-37): **muted under teaching** (a spoken recap is teaching); an **owned sonic logo, commissioned** from a contracted composer; **code-generated beds** (seeded, `examleaf-audio-compose`) are owned and may be used for Reel hooks/CTA, transitions, SFX/stings, intros/outros and prototypes, but are never described as human-composed. Bed levels are starting values to test: 20–24 dB under voice in every allowed placement and in the T2 A/B arm that tests a bed under teaching (12 AD-15 addendum; AD-37 as corrected 15 Oct 2026).
> 8. **Cost note:** the lean-floor cost cases elsewhere (`13_strong_to_cheap_model_strategy` §7.13, `08_cost_models` README §3.1) assume Gemini-class TTS at ≈ $0.14 per lesson, which **doubles to ≈ $0.28 on 1 Jan 2027**; and they assume Path B (TTS). Path A full lessons add performer time plus STS conversion.

---

## 0. Executive answer (12 bullets)

1. **Direct answer: can a low-volume jingle or music bed hide AI artefacts? No, not as a mask. Yes, as a crafted, owned, brand bed in specific sections.**
   - What listeners notice in synthetic narration lives inside the voice: wrong stress, a flat question, a mispronounced "stoichiometry", a rushed pause. The voice sits *on top of* any bed, so a quiet bed leaves all of these audible. [Hypothesis]
   - To actually cover them, the music would have to compete with the words. On a phone speaker that costs intelligibility first, because phones lose the low end and everything crowds into the mid band where speech lives [N31]. [Hypothesis]
   - So the "hide" frame fails on its own terms. It also does nothing to disclosure duties (bullet 9).

2. **Learning-cost evidence on music under narration:**
   - Neither this pass nor the earlier one found verified evidence on how background music under narration affects STEM learning. The earlier register lists it as an open gap.
   - The only verified data point on music and value is a warning. The cited paper reports a retail case where background music *reduced* perceived value by 7.7% [N39].
   - Treat "music helps retention" as unproven. Test it (Section 8) before adopting it. [Recommendation]

3. **When a bed is acceptable** [Recommendation]:
   - Places it can play: the sonic logo, the 2-4 s hook entry of a Reel, chapter transitions, the outro/end card, and wordless visual-only moments. *(15 Oct 2026: was "the recap or 'you've got this' outro"; a spoken recap is teaching and stays muted (12 AD-15), and confidence lines are conditional, see the correction addendum item 4.)*
   - Places it is muted: during derivations, numericals, definitions and any "watch this step" beat.
   - Starting level to test [Hypothesis, unsourced]: under speech, the bed sits roughly 20-24 dB below the dialogue level, with sidechain ducking. Between phrases it may rise to about 12 dB below dialogue. *(15 Oct 2026: 20–24 dB applies to every allowed placement and to the T2 arm, per 12 AD-15 addendum and AD-37 as corrected.)*
   - Validate these values with the Section 8 A/B test and the multi-device check [N32]. They are not established figures.

4. **The right frame is "craft + disclose", not "hide".**
   - In a 1,326-listener study [P-S20], first-clip appeal was 60% for the human voice and 61% for the AI voice [P-S21]. Listeners largely could not tell the difference.
   - The headline of that study is that listeners also do not *trust* AI voice. iHeartMedia's internal figure (internal, not independent) is that 90% of consumers want human-made media [P-S22].
   - So the risk is not detection. The risk is **discovery**: a student or parent finding out later. Hiding raises the cost of discovery. Disclosing it, together with visible real human craft, removes it. [Recommendation]

5. **Make the performance genuinely human (Path A, preferred for hero lessons).**
   - A real teacher performs the lesson.
   - Speech-to-speech then converts the performance into the consistent Professor Diki Simplified voice. This "preserves the original delivery" [N51 (contested)].
   - Use the multilingual STS model for Hindi and Hinglish. The English STS model is English-only [N20], [N68 (contested)].
   - *15 Oct 2026:* the performed take is diffed (ASR) against the approved script; any wording change returns to GA on a new bundle hash (Step 3). The STS processor must pass 07/07 admission and be named in the performer's consent (Step 4).

6. **Path B (directed TTS) is for volume: Reels, recaps and re-takes.** Constraints by engine:
   - **ElevenLabs v3/v4:** no SSML break tags [N2]. Speed is limited to 0.7-1.2 [N3], [N4]. Inline audio tags are used sparingly [N54].
   - **Sarvam Bulbul:** no emotion parameter. Temperature is the nearest control, and higher values are more artefact-prone [P-S16]. Style comes from the persona choice [P-S17].

7. **Pronunciation is the single highest-impact "human" fix** [Hypothesis].
   - Write numbers and units as spoken words, because normalisation is on by default [N7].
   - ElevenLabs phoneme tags work only on `eleven_flash_v2` [N6].
   - Sarvam dictionaries are plain-JSON respellings [N63]:
     - 100 words per dictionary [N61]
     - one dictionary per request [N62]
     - only the block matching `language_code` is applied [N60]
   - Build one dictionary per subject (Physics, Chemistry, Maths, Biology), each with a separate `hi-IN` block.

8. **Post-production makes synthetic or converted voice sit like a recorded human** (all [N] blog-sourced):
   - high-pass at 80-100 Hz [N22]
   - gentle 2-5 kHz presence lift [N23]
   - +1-2 dB air shelf [N24]
   - compression starting at 2:1 and never above 4:1 [N72], [N73]
   - attack about 20 ms [N74]
   - release 100-300 ms [N75]
   - optional quiet 6:1 parallel bus [N76]
   - Then add real room tone and keep natural breaths. [Recommendation]

9. **Disclosure is required regardless of music.**
   - YouTube requires disclosure of realistic altered or synthetic content [N40 (contested)]. Persistent non-disclosure can lead to labels, removal or YouTube Partner Program suspension [N46].
   - YouTube may also auto-label, including from C2PA metadata [N45], [P-S11 (contested)]. Labelled videos are reportedly not demoted [P-S12 (contested)].
   - Cloning *one's own* voice for voice-overs is listed as exempt [N43]. Animated or non-realistic content may get only a description label [N42], [N44].
   - Instagram and Indian rules were not verified in this pass. See Section 10.
   - *15 Oct 2026:* disclosure is now a release blocker (RD-45) with two wording templates, Path A and Path B (Step 14).

10. **A sonic logo is a sound investment, separate from any "mask" idea.**
    - The cited paper reports:
      - audio assets on average 3.44 times more effective than visual assets [N35 (contested)]
      - about a 5% perceived-value lift for recognisable sonic identities [N36]
      - 20% of young adults more inclined to buy from brands with one [N37]
      - one case with +38% recall and +70% appeal [N38]
    - Commission a short owned audio logo. Never use platform-library songs for brand Reels: the Zee v. Nykaa suit sought about Rs 2 crore over 12 Reels [P-S29], [P-S30], and library availability does not confer brand rights [P-S34].

11. **Borrow sound craft from vertical microdrama, not its scale claims.** The craft lessons:
    - Use silence before a reveal [N30].
    - Use texture rather than bass on phones [N31].
    - Save attention-grabbing sounds for "irreversible turns", which here means one or two key moments per lesson [N33].
    - Use off-screen ambience to widen the narrow frame [N34].
    - Use templated sessions so that batch production is feasible [N29].
    - The market is large: Lumikai projects $1.5 bn by end-2026 [P-S6], and KukuTV has 100 M+ downloads [P-S7]. Per-episode view claims are contested [N28].

12. **Order of adoption** [Recommendation]:
    1. Pronunciation lexicon and spoken-form scripts.
    2. Path A pilot with one consenting teacher, Hindi and English.
    3. Humanisation chain and multi-device QC [N32].
    4. Sonic logo pilot with A/B [N38], [N39].
    5. Disclosure checklist in the publish SOP [N46]. *(15 Oct 2026: now a release blocker, RD-45.)*
    6. Then automate with vetted skills (Section 9) [N47].

---

## 1. The human-feel model

### 1.1 What listeners actually detect (evidence)

- **Blind appeal is roughly at parity.** In the 1,326-listener study [P-S20], first-clip appeal was 60% human vs 61% AI [P-S21]. A clean modern synthetic voice does not lose on first impression.
- **Trust is the problem, not detection.** The study's framing is that listeners cannot detect AI voice but do not trust it either [P-S20]. Industry-internal data says 90% want human-made media [P-S22] (internal research, so treat as directional).
- **Platforms detect what people cannot.** YouTube auto-labels significant photorealistic AI content [P-S11 (contested)], [N45]. Auto-labelling can also trigger from C2PA metadata or YouTube's own AI tools [N45].
- **What students will notice in STEM specifically** [Hypothesis, to be tested in Section 8]:
  1. mispronounced technical terms and symbols (Δ, μ, "mole", "sin θ")
  2. emphasis on the wrong word in a definition
  3. no "thinking pause" before the step that matters
  4. uniform pitch across a question and its answer
  5. a voice that sounds pleased about everything (fake enthusiasm)
  6. room-less, breath-less audio that sounds "pasted on"

### 1.2 The five levers

| Lever | What it controls | Primary evidence | Where in SOP |
|---|---|---|---|
| **1. Direction** | Beat intent and mode (curious / steady / deliberate / light / reassuring), where pauses go, what is emphasised | Pause and speed limits [N1]–[N5]; audio tags [N54] | Step 1 |
| **2. Performance** | Who actually "acts" the line: a human (Path A) or a directed model (Path B) | STS preserves delivery [N51 (contested)]; Sarvam has no emotion parameter [P-S16] | Steps 3–6 |
| **3. Pronunciation** | Terms, symbols, numbers, units, Hindi/English code-mixing | [N6], [N7], [N60]–[N66], [P-S15] | Steps 2, 7 |
| **4. Post-production** | Room, breath, EQ, dynamics, pauses, music, loudness | [N22]–[N27], [N30]–[N34], [N72]–[N76] | Steps 8–10 |
| **5. Visuals** | Hands, handwriting, real teacher presence, imperfection, captions | Labelling of non-realistic content [N42], [N44]; narrow frame [N34] | Steps 11–12 |

**[Recommendation] Rule of thumb:** a lesson feels human when at least two levers carry real human input. Performance (Path A) or a human director for Path B is one. A visible human in the visuals (hands or a teacher cutaway) is the other. Post-production polish alone does not create the feeling of a human.

---

## 2. End-to-end production SOP: one vertical lesson (English master, then Hindi/Hinglish)

Each step lists **Input / Output / Tools / Settings / Check**.

### Step 1: Script with beat direction tags

- **Input:** syllabus topic (ASSEB chapter), the 3–5 learning outcomes, and common exam mistakes.
- **Output:** an English master script split into beats. A beat is one idea, roughly 10–40 s. Each beat carries a header:

  `[BEAT 04 | mode: deliberate | wpm: 130 | pause-after: 1.5s THINK | emphasis: "net force" | sting: no]`

- **Settings** [Recommendation]:
  - Modes come from the Super Teacher persona.
  - wpm bands come from the existing plan (130–155).
  - Mark every "protected thinking pause" explicitly. ~~Scripted pauses are capped at 3 s~~ *(15 Oct 2026, scoped)* **TTS break tags** are capped at 3 s, because break tags support pauses only up to 3 s [N1]. **Protected think windows are not break tags:** they follow RD-11 (5–8 s for a simple prediction, 4 s only for a binary choice, **default 6 s**, answer hidden), inserted as room tone in the edit (Step 8), or `pause-video` (learner-controlled) for writing, drawing or multi-step work. Inside a Reel, keep non-task pauses short, since longer dead air fights the Reel's attention curve [Hypothesis]; a Reel that asks a question still gets the RD-11 window or does not ask it.
  - *15 Oct 2026:* confidence lines are conditional and tied to a visible capability (Super Teacher rules, `03_super_teacher_framework/INSTRUCTIONS_super_teacher_authoring.md` Step 9). Write "If you can count the atoms on both sides without the animation, you can balance the next one", not "You've got this".
  - Write numbers, units and symbols in spoken form. Write "nine point eight metres per second squared", not "9.8 m/s²", because normalisation is on by default and you should not leave reading to it [N7].
- **Check:** read the script aloud at the target wpm with a stopwatch. Any beat that overruns by more than about 10% gets cut, not sped up. [Recommendation]

### Step 2: Pronunciation lexicon

- **Input:** the term list extracted from the script.
- **Output:** a versioned lexicon file per subject and per language.
- **Tools and settings:**
  - **Sarvam:**
    - Dictionaries are plain JSON with respellings and no phoneme markup [N63].
    - 100 words per dictionary [N61], one `dict_id` per request [N62], and only the block matching `language_code` (for example `hi-IN`) applies [N60].
    - So create four subject dictionaries, each with `en-IN` and `hi-IN` blocks. [Recommendation]
    - Upload with curl, appending `;type=application/json` to the file field [N64].
    - Update in place so the `dict_id` survives [N65]. The same id works across REST, HTTP Stream and WebSocket [N66].
    - Dictionaries are supported on v3/v4-flash [P-S18].
  - **ElevenLabs:** phoneme tags only on `eleven_flash_v2` [N6]. For v3/v4, use respelling in the text itself, applied by a script pre-processor from the same lexicon. [Recommendation]
- **Check:** the 100-word cap forces prioritisation. Rank terms by frequency across the chapter set and by how badly the default reading fails. [Recommendation]

### Step 3: Path A, human performance capture (preferred for full lessons)

- **Input:** the beat-tagged script and the lexicon card printed for the teacher.
- **Output:** WAV or FLAC takes, each under 5 minutes and under 50 MB [N15], [N16], [N21].
- **Recording setup** [Recommendation; gear specifics unverified in this pass]:
  - Quiet, soft-furnished room. Close-miked (USB or XLR dynamic or condenser). Phone mic only as a fallback.
  - Record 48 kHz / 24-bit WAV (matches the video master; the 48 kHz choice is a Recommendation).
  - Record 30 s of room tone at the start of every session.
- **How to direct a teacher** [Recommendation]:
  - Brief the *student*, not the line: "A Class 10 student in Jorhat has just got this numerical wrong for the third time."
  - Run each beat in its mode. Ask for "explain it to one person", not "present it".
  - Do one rehearsal pass, then two keeper takes per beat. Recording itself costs no ElevenLabs credits [N18], so rehearse freely.
  - Let the teacher fix script wording that sounds unnatural to them. Real phrasing is part of the value. *(15 Oct 2026: wording fixes are proposed before recording and re-approved; see the check below.)*
  - Keep real reactions: a small laugh at a silly mnemonic, a breath before the key step. Reactions must not be fake sensing ("Yes, exactly!", "I heard you say…") or new claims.
- **Consent and contract** [Recommendation; legal review required]:
  - Written consent covering voice recording, voice conversion, any cloning (an Instant Voice Clone needs only about 10 s of audio [N56], so consent must be explicit), languages, term, territory, revocation and payment.
  - A named credit ("Performed by …") in descriptions.
  - *15 Oct 2026:* name every third-party processor the takes will be sent to (for example the STS vendor, Step 4); the consent does not cover an unnamed processor.
  - No use of the teacher's voice for content they have not seen.
- **Check:**
  - Trim leading and trailing silence before conversion. Silence is billed as output on Segmind [N71] (and duration-billed generally [N17]).
  - Split anything over 5 min or 50 MB [N15], [N16].
  - **Wording diff against the approved script (15 Oct 2026, mandatory for Path A):** transcribe every keeper take with ASR and diff it against the GA-approved script using the narration comparator (`qa.transcript_check`, critical phrases included; Indic-safe since 15 Oct 2026). Run the script linter's fake-sensing checks on the performed transcript. **Any wording change, added claim or fake-sensing line returns the script to academic approval (GA) on a new script-bundle hash** before conversion, alignment or release; otherwise re-record the beat to the approved wording.

### Step 4: Voice conversion to the brand voice (Path A continued)

- **Input:** trimmed takes.
- **Output:** brand-voice takes with the teacher's timing, emphasis and emotion.
- **Tools and settings:**
  - **ElevenLabs Voice Changer (speech-to-speech):**
    - Use `eleven_multilingual_sts_v2` for Hindi and Hinglish [N51 (contested)], [N20]. Multilingual v2 covers 29 languages [N19]. Hindi is not named in the quoted evidence, so verify it.
    - Accepted inputs: MP3, M4A, FLAC, OGA, OGG, WAV [N21].
    - Turn on the noise-isolation option for home recordings [N69].
    - Cost: 1,000 characters per minute [N17], so a 10-minute lesson costs about 10,000 characters per pass.
  - **Via Segmind** (third party): about $0.00375 per output second, roughly $0.225/min [N67]. Latency was observed under 7 s (author observation) [N70].
  - *15 Oct 2026:* any third-party STS processor (ElevenLabs Voice Changer, Segmind or another reseller) must pass the **07/07 admission process** (`07_end_to_end_pipeline_instructions/07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md` §2 scoped worker key and approved outbound domain; §4 admission chain; §7 voice consent) and be named in the performer's consent before any teacher recording is sent to it.
  - **Alternatives** (RVC, Seed-VC, OpenVoice, Chatterbox): not verified in this pass (Section 4).
- **Brand-voice choice** [Recommendation]:
  - **Option 1:** the teacher's *own* voice as the brand voice, with no conversion, or a consented own-voice clone. This is closest to YouTube's exemption for own-voice clones [N43].
  - **Option 2:** a designed (non-real-person) brand voice. Never convert into the voice of a real person who did not consent [N41].
- **Check:** compare original and converted side by side on a phone speaker. Reject any take where conversion smears consonants in technical terms. Re-record those beats rather than patching them. [Recommendation]

### Step 5: Path B, directed TTS (Reels, recaps, re-takes, volume)

- **Input:** a beat-tagged script that has been lexicon-preprocessed.
- **ElevenLabs v4/v3:**
  - Break tags are not supported [N2]. Get pauses from punctuation, from line breaks between generations, or by inserting room tone in the edit (Step 8).
  - Speed: default 1.0 [N5]. Deliberate mode 0.85–0.95, with a hard floor of 0.7 [N3]. Reel hooks up to 1.05–1.1, with a hard ceiling of 1.2 [N4]. The in-range values are Recommendations; the limits are sourced.
  - Inline tags: v4 supports delivery and sound tags such as `[laughs]` or `[light rain]` [N54]. Use at most one delivery tag per beat and no sound-effect tags in the voice track, because SFX belong in the edit [Recommendation].
  - Stability and style values were not sourced in this pass. Tune by listening test.
  - v4 claims about 75% blind preference over competitors [N57]. That is a vendor claim, so run your own test.
  - v4 lists 90+ languages, but the page does not name Hindi [N55]. Run a native-speaker Hindi test before committing.
- **Sarvam Bulbul:**
  - v3 has 11 languages and 30+ voices [N8], [P-S1]. v4-flash has 200+ personas whose names encode style (narration, expressive/warm and so on) [P-S17], [P-S35].
  - There is no emotion parameter. Temperature runs 0.01–1.0 (default 0.6), and higher values are more expressive but artefact-prone [P-S16]. Start at the default and move down for steady or deliberate beats. [Recommendation]
  - Pace runs 0.5–2.0 [P-S18].
  - REST is capped at 2,500 characters per request [P-S36]; HTTP streaming at 3,500 [P-S37].
  - Request `wav` [N9] at 48 kHz (REST supports up to 48 kHz) [P-S19], [P-S38].
  - Code-mixed text is supported [P-S15].
- **Gemini 3.8 TTS / Cartesia Sonic:** remain candidates. Their controls, Hindi quality and pricing are unverified in this pass. *(15 Oct 2026 cost note: the lean-floor cost cases in `13_strong_to_cheap_model_strategy` §7.13 and `08_cost_models` README §3.1 assume Gemini-class TTS at ≈ $0.14 per lesson from the narration research; that tariff doubles on 1 Jan 2027, to ≈ $0.28 per lesson (`08_cost_models/CONSOLIDATED_COST_SCENARIOS.md` E.6). The lean floor is a Path B figure; Path A lessons add performer time and STS conversion.)*
- **Output:** one audio file per beat (never one 10-minute render). [Recommendation]

### Step 6: Per-beat generation and re-roll policy [Recommendation]

1. Generate each beat 3 times (Path B) or convert 2 takes (Path A).
2. A human picks the best by ear on a phone speaker, using a 4-item checklist:
   - Is every term pronounced right?
   - Does emphasis land on the tagged word?
   - Does the mode match the tag?
   - Are there no artefacts (warble, clipped consonant, odd breath)?
3. If all 3 fail, change the *input*: respell, re-punctuate or split the sentence. Do not keep re-rolling. After 6 total failures the beat goes to Path A (a human records it).
4. Log every failure term into the lexicon backlog (Step 2).

### Step 7: Hindi and Hinglish adaptation (rewrite, don't translate)

- **Input:** the locked English master plus the beat map.
- **Output:** a Hindi or Hinglish script with the *same beat map*, so visuals and timings carry over.
- **Rules** [Recommendation]:
  - **Rewrite for how an Assam Class 10 student hears Hindi STEM.** Keep English technical terms where textbooks and coaching use them ("force", "velocity", "mole", "equation"). Use Hindi for the connective and emotional language ("dekho", "ab socho", "yahi trick hai").
  - **Script form:**
    - For Sarvam, test both Devanagari with English terms in Latin script, and full Devanagari. Code-mixed input is supported [P-S15].
    - For ElevenLabs, test Devanagari against romanised Hinglish on the same beat.
    - Pick per engine by listening test [Hypothesis]. No source in this pass settles this.
  - **Numbers and units:** write them out in the target language's spoken form. Normalisation is on by default [N7], and Hindi number reading is a common failure point [Hypothesis].
  - **Lexicon:** the separate `hi-IN` dictionary block applies only when `language_code=hi-IN` [N60].
  - **Length:** Hindi often runs longer than English [Hypothesis]. Re-time beats; do not speed up past the persona band.
  - **Reviewer:** a native Hindi-speaking STEM teacher signs off every script and every final audio.
- **Assamese, later:** human voice only. Sarvam Vision OCR supports 23 languages (22 Indian + English) [N13], which is useful for extracting Assamese-medium textbook text. Confirm Assamese is among them. Bulbul does not list `as-IN` [P-S15].

### Step 8: Forced alignment and protected pauses

- **Input:** chosen beat takes and the script.
- **Tools:**
  - Sarvam speech-to-text: the REST endpoint takes clips up to 30 s; use the Batch API for longer audio [N10].
  - ElevenLabs transcription skill: speaker IDs and paragraph-start timestamps [N49 (contested)]. Realtime `scribe_v2_realtime` gives word-level timestamps [N50 (contested)].
  - WhisperX and similar aligners are unverified in this pass.
- **Process** [Recommendation]:
  1. Align words to time.
  2. Insert protected pauses as *room tone*, never digital silence, at the tagged points: 0.6–1.0 s "light", 1.2–2.0 s "THINK" (emphasis hold), ~~up to 3 s maximum (consistent with [N1])~~. *(15 Oct 2026: the 3 s limit applies only to TTS break tags [N1]. Protected think windows where the student predicts or answers follow **RD-11**: room-tone insert, **default 6 s**, 5–8 s range (4 s only for a binary choice), answer hidden until the window ends; or `pause-video` for writing, drawing or multi-step work.)*
  3. Trim AI-generated over-long gaps.
  4. Keep one natural breath before the key line of each beat.
- **Check:** the caption timing file comes from the same alignment, so it stays in sync.

### Step 9: Post-production humanisation (voice chain)

Order and settings:

1. **Clean:** noise isolation on recorded input [N69]. iZotope RX, Adobe Podcast and Auphonic are optional, not verified here.
2. **High-pass** at 80–100 Hz [N22].
3. **De-ess:** gentle, by ear. Settings not sourced.
4. **EQ:** gentle presence lift in the 2–5 kHz region [N23], then a +1–2 dB high shelf above 8 kHz for air. Back it off if sibilance rises [N24].
5. **Compressor:** ratio starting at 2:1 [N72], up to 3:1–4:1 if needed [N26], never above 4:1 [N73]. Attack about 20 ms (sources give 10–30 [N25] and 15–30 [N74]). Release 100–300 ms [N27], [N75].
6. **Parallel bus (optional):** a 6:1+ compressed copy blended low under the dry signal [N76].
7. **Saturation:** subtle tape or tube colour to add harmonic "body" [Hypothesis; unsourced, test by ear].
8. **Room:** lay a continuous room-tone bed under the entire voice track, from the teacher's own room tone or a recorded classroom or study room. Use a very short, dark room reverb only if the voice sounds "in your skull" [Recommendation].
9. **Micro-variation:** when Path B joins beats, avoid identical breath samples and identical pause lengths. Vary pauses ±10–20% within the mode band [Hypothesis].

### Step 10: Music, sonic logo and ducking

- **Default stays "music off" under teaching** (the existing plan, reinforced by [N39] and the lack of learning evidence). A spoken recap counts as teaching. *(15 Oct 2026, aligned with 12 AD-15/AD-37.)*
- **Allowed placements** [Recommendation]:
  - end motif at close only (0.6–0.75 s, `music/diki-end-motif`; no logo at the open, PD-04)
  - a short transition sting between chapters
  - a bed under the Reel hook and the outro CTA
  - an optional very low ambience: classroom or lab hum suggesting the "world beyond the frame" [N34]
- **Ducking:** sidechain the bed from the voice. Starting values [Hypothesis, unsourced]: a fast attack (a few ms), a release of a few hundred ms, and 8–12 dB of gain reduction when voice is present.
- **Tension tools:** use an ambience drop just before the key reveal [N30]. Use texture and rhythm, not sub-bass [N31]. Allow at most 1–2 stings per lesson [N33].
- **Licensing:** commissioned or owned music only. Log every asset (Section 6). Platform libraries do not confer brand rights [P-S33], [P-S34].
- **Music policy (15 Oct 2026, aligned with 12 AD-15/AD-37):** the **sonic logo is owned and commissioned** from a contracted composer. **Code-generated beds** (seeded, in-house, `examleaf-audio-compose`) are owned and may be used for Reel hooks/CTA, transitions, SFX/stings, intros/outros and prototypes; never describe them as human-composed. Starting bed level 20–24 dB under voice in those placements (12 AD-37 as corrected 15 Oct 2026); muted under teaching.

### Step 11: Loudness and export

- **Existing plan:** master to -16 LUFS integrated. Platform-specific normalisation targets for YouTube, Shorts and Reels are **unverified** (an open gap in the earlier register). Keep -16 LUFS as the house standard until you measure what each platform does to an upload. [Recommendation]
- **True peak:** set a limiter ceiling. -1 dBTP is a commonly used conservative ceiling [Recommendation, unverified in this pass].
- **Exports:** a 48 kHz WAV stem master (voice, music, SFX separate), then delivery AAC in MP4. Check the exported files for C2PA metadata before upload [N45].

### Step 12: Captions and visual human signals

- **Captions** [Recommendation; platform safe-zone specs unverified]:
  - Large, high-contrast, 1–2 lines.
  - Keep them out of the bottom UI band and the right-side action rail; check against the current platform templates.
  - Highlight one keyword per caption, using the beat's emphasis word.
  - Hindi captions in Devanagari, technical terms in Latin script.
  - Timing comes from Step 8.
- **Visual human signals** [Recommendation]:
  - real hands writing on paper or a whiteboard, filmed top-down in 9:16
  - the teacher's handwriting, including a crossed-out mistake that gets corrected
  - 1–3 short real teacher cutaways per lesson (face or upper body, reacting)
  - real lab or object shots where possible
  - small imperfections left in: a paper rustle, a pen tap
- **Disclosure interaction:** stylised or animated visuals may need only a description label [N42], [N44]. A real teacher on camera with a synthetic voice is the case that most needs honest disclosure.
- **Avatar tools** (HeyGen, Hedra, Veo): unverified here. Avoid photoreal synthetic teachers [Recommendation].

### Step 13: QA listening panel

- **Panel** [Recommendation]: 1 subject teacher, 1 native Hindi speaker, and 3 target-age students (with consent and guardian consent where needed).
- **Devices:** studio monitors or headphones, earbuds, and a phone speaker [N32].
- **Score each lesson on:**
  - pronunciation errors (count)
  - "felt like a real teacher" (1–5)
  - listening effort (1–5)
  - any moment that "sounded robotic" (timestamp)
- **Gate:** zero pronunciation errors on key terms. Any robotic-moment timestamp goes back to Step 6. *(15 Oct 2026: for Path A, also the Step 3 ASR wording diff shows no unapproved change, or GA has re-approved the new bundle hash.)*

### Step 14: Disclosure and labelling

- **YouTube:**
  - Tick the AI-use disclosure under Attributes when content is realistic altered or synthetic [N40 (contested)].
  - Making a real person appear to say something they did not is always disclosable [N41].
  - Own-voice clones for voice-overs are listed exempt [N43].
  - Non-realistic AI content does not need disclosure [N42].
  - YouTube may auto-label regardless [N45], [P-S11]. Repeated non-disclosure can lead to penalties [N46].
- **ExamLeaf house rule** ~~[Recommendation]~~ *(15 Oct 2026: now a release blocker, RD-45)*: disclose voice processing in every description whether or not it is strictly required. ~~Suggested wording: "Lesson performed by [Teacher], voice processed with AI tools. Reviewed by [Teacher]."~~ This is the "craft + disclose" frame. **Two templates (15 Oct 2026):**
  - **Path A** (human performance + speech-to-speech): "Performed by [Teacher]; voice converted with AI. Reviewed by [Reviewer]."
  - **Path B** (pure TTS: Reels, recaps, re-takes): "AI-generated narration; script by [Teacher/author, or the Professor Diki Simplified team]. Reviewed by [Reviewer]."
  - Never use Path A wording on Path B content, and never place a real-teacher cutaway over Path B audio unless the label states plainly that the voice is synthetic. Fill the export fields `ai_voice_disclosure` and `performer_credit` (empty = release fails). Also: the YouTube altered/synthetic toggle where applicable, the Meta AI label, C2PA not stripped.
- **Instagram/Meta and Indian synthetic-media rules:** unverified in this pass. Get legal review before scale-up (Section 10). The EU AI Act transparency obligations (Aug 2026) [P-S13 (contested)] matter only if you distribute there.

### Step 15: Publish cadence [Recommendation]

- Per lesson: 1 full lesson plus ~~3–5 Reels/Shorts cut from its strongest beats~~ **1–3 recomposed complete units** (Reels/Shorts that each teach one complete idea; recompose, don't crop; more only after the GS gate holds) *(15 Oct 2026, aligned with 07/05 principles 1–2)*.
- Microdrama platforms show that daily cadence is achievable at scale (one regional title daily [P-S27]), but only with templated sound sessions [N29].
- Start at 2–3 lessons per week and scale after the QA gate holds for four consecutive weeks.

---

## 3. Tricks, tips and hacks catalog

| # | Trick | What it fixes | Exactly how (settings) | Source | Risk / when it backfires |
|---|---|---|---|---|---|
| 1 | Cap **TTS break-tag** pauses at 3 s *(15 Oct 2026: scoped; protected think windows follow RD-11, default 6 s room-tone insert or pause-video)* | Over-long dead air | Break tags up to 3 s on supported models | [N1] | v3/v4 ignore break tags [N2] |
| 2 | Edit-inserted pauses for v3/v4 | Rushed delivery with no thinking time | Generate per beat; insert room tone at THINK marks | [N2] + Rec | Digital silence sounds dead; always use room tone |
| 3 | Slow deliberate mode via speed | Derivations too fast | Speed 0.85–0.95; floor 0.7 | [N3], [N5] | Near 0.7 can sound drawn-out; prefer rewriting shorter |
| 4 | Reel speed cap | "Chipmunk" hooks | ≤1.1 typical; hard max 1.2 | [N4] | Speed-up raises artefacts; cut words instead |
| 5 | Spoken-form numbers and units | Misread "m/s²", "10⁻³", "H₂SO₄" | Write "ten to the power minus three" etc. | [N7] | Makes scripts longer; keep the on-screen text symbolic |
| 6 | Phoneme tags only on flash_v2 | Ignored IPA on other models | Use `eleven_flash_v2` for phoneme-tagged lines | [N6] | Model mismatch within one lesson changes timbre |
| 7 | Respelling lexicon | Term mispronunciation on v3/v4 and Sarvam | Pre-processor replaces terms with respellings | [N63] + Rec | Respelling can leak into captions; caption from the original script |
| 8 | Language-specific dictionary blocks | English rule applied to Hindi or vice versa | Separate `hi-IN` and `en-IN` blocks | [N60] | Wrong `language_code` silently skips the block |
| 9 | Top-100 term prioritisation | Dictionary cap | Rank by frequency × failure severity | [N61] | Long-tail terms still fail; catch in QA |
| 10 | Per-subject dictionaries | One `dict_id` per request | Physics/Chem/Maths/Bio dicts | [N62] | Cross-subject lessons need a merged dictionary |
| 11 | Content-type suffix on upload | Failed curl uploads | `-F "file=@phy.json;type=application/json"` | [N64] | — |
| 12 | Update the dictionary in place | Broken integrations after edits | Update keeps the same `dict_id` | [N65] | Version the JSON in git; edits are live everywhere [N66] |
| 13 | Human performance → STS | Robotic prosody | Teacher records; convert with multilingual STS | [N51 (contested)], [N20] | Conversion may smear consonants; QA every term |
| 14 | Scene-sized takes | Upload rejections | <5 min, <50 MB per take | [N15], [N16] | Splitting mid-sentence causes seams; split at beat boundaries |
| 15 | Lossless input | Conversion artefacts from lossy input | Record WAV/FLAC | [N21] | Larger files; watch the 50 MB cap |
| 16 | Free rehearsal | Credit waste | Rehearse in-tool; generate only keepers | [N18] | — |
| 17 | Trim silence before converting | Paying for silence | Trim heads and tails | [N71], [N17] | Over-trim clips breaths; leave about 150 ms [Rec] |
| 18 | Noise isolation flag | Home-recording noise | Enable isolation before conversion | [N69] | Can thin the voice; A/B it |
| 19 | High-pass filter | Rumble, plosive mud | 80–100 Hz | [N22] | Too high thins a male voice |
| 20 | Presence lift | Low intelligibility on phones | Gentle boost 2–5 kHz | [N23] | Harshness; A/B on a phone |
| 21 | Air shelf | Dull, "boxed" AI tone | +1–2 dB above 8 kHz | [N24] | Sibilance; de-ess first |
| 22 | Gentle compression | Flat, lifeless AI voice | Start 2:1; max 4:1 | [N72], [N26], [N73] | Over 4:1 flattens emotion [N73] |
| 23 | Slow-ish attack | Squashed consonants | ~20 ms (range 10–30) | [N25], [N74] | Too slow lets peaks through; the limiter catches them |
| 24 | Rhythmic release | Pumping | 100–300 ms | [N27], [N75] | — |
| 25 | Parallel compression | Thin voice on phone speakers | 6:1+ bus blended low | [N76] | Too loud a blend sounds "radio-ad" |
| 26 | Silence before the reveal | Key insight lands flat | Drop ambience/bed 0.5–1 s before the reveal | [N30] | Overuse becomes predictable |
| 27 | Texture, not sub-bass | Emphasis lost on phones | Use mid-range textures and rhythm | [N31] | Laptop/headphone listeners hear a thinner mix |
| 28 | Sting rationing | Fatigue, "YouTuber" cheapness | 1–2 stings per lesson at true turning points | [N33] | — |
| 29 | Off-screen ambience | Narrow frame feels sterile | Low classroom or lab hum | [N34] | Hum competes with speech if too loud |
| 30 | Multi-device QC | Mix fine in studio, bad on phone | Check monitors, earbuds, phone | [N32] | — |
| 31 | Templated sessions | Batch production slows quality | DAW template with chain, buses, logo, ambiences | [N29] | Templates breed sameness; vary ambience per subject |
| 32 | Sparing inline audio tags | Monotone delivery | ≤1 delivery tag per beat (e.g. `[laughs]`) | [N54] | Tags can over-act; can add fake enthusiasm |
| 33 | Lower Sarvam temperature for steady beats | Artefacts | Default 0.6, step down for deliberate | [P-S16] | Too low sounds monotone |
| 34 | Persona choice as emotion control (Sarvam) | No emotion parameter | Choose a narration or warm persona | [P-S17] | Persona names are not a guarantee; listen |
| 35 | Chunk to the character cap | Failed or truncated renders | ≤2,500 chars REST; ≤3,500 HTTP stream | [P-S36], [P-S37] | Chunk at beat boundaries only |
| 36 | Batch STT for lessons | 30 s REST limit | Sarvam Batch API for 10-min audio | [N10] | — |
| 37 | C2PA check before upload | Surprise auto-labels | Inspect metadata on export | [N45] | Stripping metadata to evade labels conflicts with the disclosure ethic; don't |
| 38 | Owned sonic logo | Brand anonymity | Commissioned 2–3 s logo, consistent | [N35]–[N38] | Mismatched music lowers value [N39] |
| 39 | Never use platform-library songs in brand Reels | Copyright suits | Owned or commissioned music only | [P-S29]–[P-S34] | — |
| 40 | OCR Assamese textbooks | Manual retyping | Sarvam Vision (23 languages) | [N13] | Verify Assamese accuracy on a sample |
| 41 | Multi-language document translation as a first draft only | Speed | Up to 12 targets per job | [N14] | Output is a translation, not a rewrite; a human must rewrite (Step 7) |

---

## 4. Tools and settings table

| Tool | Role | Hindi support | Cost (if sourced) | Key settings | Caveat |
|---|---|---|---|---|---|
| ElevenLabs Eleven v4 / v4 Turbo | Directed TTS (Path B) | 90+ languages; Hindi not named on page [N55] | Not on page [N59] | Speed 0.7–1.2 [N3], [N4]; inline tags [N54]; no break tags [N2] | 75% preference is a vendor claim [N57]; PVC support [N58] |
| ElevenLabs Eleven v3 | Directed TTS | Not verified | Not sourced | No break tags [N2] | — |
| ElevenLabs eleven_flash_v2 | Lines needing phoneme tags | Not verified | Not sourced | Phoneme tags only here [N6] | Timbre may differ from v4 |
| ElevenLabs Voice Changer (STS) | Path A conversion | Multilingual v2 STS, 29 languages [N19] | 1,000 chars per minute [N17]; recording free [N18] | <5 min, <50 MB, WAV/FLAC [N15], [N16], [N21]; noise isolation [N69] | English STS is English-only [N20]; multilingual model name contested [N51] |
| Segmind (ElevenLabs STS) | Hosted STS API | As above | ~$0.00375/s (~$0.225/min) [N67] | Trim silence [N71] | Latency under 7 s is the author's observation [N70]. *15 Oct 2026: third-party processor; admit through 07/07 and name in performer consent first* |
| ElevenLabs IVC / PVC | Voice cloning (own or consented voice) | Not verified | Not sourced | ~10 s audio for IVC [N56]; PVC on v4 [N58] | Written consent mandatory [Rec] |
| ElevenLabs skills + MCP | Automation | n/a | n/a | `npx skills add elevenlabs/skills` [N47]; hosted MCP via OAuth [N53] | Skill details contested [N49]–[N52] |
| Sarvam Bulbul v3 | Hindi/English TTS | Yes, hi-IN [P-S15]; 11 languages, 30+ voices [N8] | Not sourced | Pace 0.5–2.0 [P-S18]; temperature [P-S16]; wav [N9]; 48 kHz REST [P-S38] | No emotion parameter [P-S16]; no Assamese [P-S15] |
| Sarvam Bulbul v4-flash | Persona TTS | Yes [P-S15] | Not sourced | 200+ personas [P-S35]; style via persona [P-S17] | Model status contested [P-S14] |
| Sarvam pronunciation dictionary | Lexicon | hi-IN block [N60] | Not sourced | 100 words, 1 per request, JSON [N61]–[N63] | Only the matching block applies [N60] |
| Sarvam STT (REST / Batch / Streaming) | Transcripts, alignment, captions | Yes (Indian languages) | Not sourced | REST ≤30 s; Batch for longer [N10]; streaming WAV/PCM only [N11]; 8 kHz flag rules [N12] | — |
| Sarvam Vision | OCR of textbooks | 23 languages [N13] | Not sourced | — | Confirm Assamese quality |
| Sarvam document translation | First-draft translation | Yes | Not sourced | Up to 12 targets per job [N14] | Not a substitute for a rewrite |
| Gemini 3.8 TTS | TTS candidate (style prompts) | Unverified | Unverified | Unverified | Needs its own test |
| Cartesia Sonic | TTS candidate | Unverified | Unverified | Unverified | Needs its own test |
| RVC / Seed-VC / OpenVoice / Chatterbox | Open-source voice conversion or TTS | Unverified | Self-hosted (compute only) | Unverified | Licence, consent and quality not verified this pass |
| Adobe Podcast (Enhance) | Speech cleanup | Unverified | Unverified | — | Can over-process; A/B |
| Auphonic | Leveling and loudness automation | n/a | Unverified | Target -16 LUFS (house) | Platform targets unverified |
| iZotope RX | Repair (de-click, de-noise, de-ess) | n/a | Unverified | — | — |
| Audacity / FFmpeg | Editing, batch processing, loudness | n/a | Free (open source) | FFmpeg loudnorm for -16 LUFS [Rec] | Settings unverified here |
| WhisperX | Word-level alignment | Unverified | Open source | — | Hindi alignment quality unverified |
| HyperFrames (default master timeline); Remotion (benchmark only); Manim (maths inserts) *(15 Oct 2026: was "Remotion / manim-voiceover"; per 12 AD-01)* | Programmatic video and maths animation synced to audio | n/a | Unverified | Drive from the Step 8 alignment JSON via the cue sheet [Rec] | — |
| HeyGen / Hedra / Veo | Avatars, generated video | Unverified | Unverified | — | Photoreal output triggers disclosure [N40], [N45]; avoid synthetic teachers [Rec] |
| Caption tools (CapCut, Submagic etc.) | Burned-in captions | Unverified | Unverified | One-keyword highlight [Rec] | Check Devanagari rendering |

---

## 5. Audio spec sheet: ExamLeaf vertical video

| Parameter | Full lesson (~10 min) | Reel / Short (20–60 s) | Basis |
|---|---|---|---|
| Integrated loudness | -16 LUFS | -16 LUFS | Existing plan; platform targets unverified |
| True peak ceiling | -1 dBTP | -1 dBTP | [Recommendation, unverified] |
| Music under speech | Off (teaching, including spoken recaps); bed only in intro/transition/outro | Bed allowed under hook and CTA | [N39], [Recommendation]; 12 AD-15 (15 Oct 2026) |
| Bed level under voice | ~20–24 dB below dialogue in intro/transition/outro and in the T2 A/B arm (*15 Oct 2026, 12 AD-37 as corrected*) | ~20–24 dB below dialogue (*15 Oct 2026: 18–22 and 15–20 superseded, 12 AD-15 addendum*) | [Hypothesis, unsourced; test in Section 8] |
| Ducking | Sidechain, 8–12 dB reduction | Same | [Hypothesis] |
| Stings | 1–2 per lesson | 0–1 | [N33] |
| Sonic logo (end motif) | Close only, 0.6–0.75 s (no logo at the open, PD-04) | Close only, 0.6–0.75 s | [Recommendation] |
| Speech rate | Steady 140–150; deliberate 130; light/curious 150–155 wpm | Hook 150–155; body 145 | Existing plan (130–155) |
| Light pause | 0.6–1.0 s | 0.4–0.8 s | [Recommendation] |
| THINK pause (emphasis hold) | 1.2–2.0 s | 0.8–1.2 s | [Recommendation] |
| Protected think window (*15 Oct 2026*) | RD-11: 5–8 s, **default 6 s**, answer hidden, room-tone insert; or pause-video | Same when the Reel asks a question | RD-11 |
| Maximum **TTS break-tag** pause (*15 Oct 2026: scoped*) | 3.0 s | 1.5 s | [N1], [Recommendation] |
| Engine speed (ElevenLabs) | 0.85–1.0 | 1.0–1.1 (max 1.2) | [N3]–[N5] |
| Voice chain | HPF 80–100 Hz; +2–5 kHz presence; +1–2 dB >8 kHz; comp 2:1–4:1, ~20 ms attack, 100–300 ms release | Same | [N22]–[N27], [N72]–[N76] |
| Low end in mix | No sub-bass emphasis | Same | [N31] |
| Recording format | 48 kHz / 24-bit WAV (or FLAC) | Same | [N21], [Recommendation] |
| TTS request format | wav, 48 kHz (Sarvam REST) | Same | [N9], [P-S38] |
| STS take limit | <5 min, <50 MB | n/a | [N15], [N16] |
| Master deliverable | Stems (voice / music / SFX / ambience) WAV 48 kHz + mixed WAV | Same | [Recommendation] |
| Upload deliverable | MP4 H.264 + AAC (bitrate unverified) | Same | [Recommendation] |
| QC devices | Monitors, headphones, earbuds, phone speaker | Same | [N32] |

---

## 6. Sonic branding plan

### 6.1 Evidence

The cited Oxford-hosted paper reports:
- Audio assets were on average 3.44 times more effective than visual assets in creative effectiveness (Ipsos) [N35 (contested)].
- Recognisable sonic identities are associated with about a 5% higher perceived value [N36].
- 20% of young adults were more inclined to buy from brands with a sonic identity (YouGov) [N37].
- One campaign measured +38% recall and +70% appeal (Veritonic context) [N38].
- **Counter-evidence:** background music in retail reduced perceived value by 7.7% [N39].

**Reading** [Recommendation]: a *short, consistent, owned* signature is supported. A *continuous* bed is not supported and can backfire. None of this evidence is about learning outcomes, so measure recall and retention yourself.

### 6.2 Audio logo design brief [Recommendation]

- **Length:** 1.5–3 s. A 4–6 s extended version for full-lesson intros only.
- **Character:** warm, curious, precise, like the Super Teacher. Not hype or EDM. A "lightbulb" resolution, from a question to an answer in 2–4 notes.
- **Palette:** mid-range melodic instruments that survive phone speakers [N31]. Avoid sub-bass hits. A subtle Northeast Indian or Assamese timbral nod is optional and should be tested with students (for example a light bamboo flute or *gogona*-like texture). Keep it non-stereotyped [Hypothesis].
- **Variants to commission:**
  1. full logo
  2. short logo
  3. a "correct answer" micro-sting from the same motif
  4. a transition swoosh from the same motif
  5. a 30 s and a 60 s loopable bed from the same motif, for intros and outros only
  6. a stems package
- **Deliverables:** WAV 48 kHz/24-bit, stems, loudness-matched versions, and written full buyout or exclusive licence.

### 6.3 Usage map

| Placement | Logo | Bed | Stings | Ambience |
|---|---|---|---|---|
| Lesson cold open (0–5 s) | None (no logo at the open, PD-04) | Bed under first line, ducked | — | — |
| Teaching beats (definitions, derivations, numericals) | — | **Muted** | — | Optional very low room/lab hum [N34] |
| Key reveal or "aha" | — | — | 1 sting max, after a silence drop [N30], [N33] | Dropped just before [N30] |
| Chapter transitions | — | 2–4 s bed swell | Transition sting | — |
| Recap (spoken; teaching) *(15 Oct 2026: was "Recap / 'you've got this'"; conditional confidence lines only)* | — | **Muted** | — | — |
| Outro / CTA | End motif (`music/diki-end-motif`, once, after the last word) | Bed | — | — |
| Reel hook | (Test arm) | Bed under hook | — | — |
| Reel body | — | Muted or very low (test) | Correct-answer sting allowed | — |
| Reel end | End motif (`music/diki-end-motif`) | — | — | — |

### 6.4 Commissioning and cost pointers

- Commission from an independent composer, ideally from the Northeast or India, through a written agreement. Prefer a full buyout or exclusive perpetual licence covering all platforms and paid ads. [Recommendation]
- Market prices for audio-logo commissions were **not verified** in this pass. Get three quotes.
- **Never** use songs from the Instagram/YouTube libraries in brand content. Zee's Meta licence covers only non-commercial individual use [P-S33], and library availability does not confer rights [P-S34]. The Zee v. Nykaa claim was about Rs 2 crore [P-S29].

### 6.5 Licensing log (template fields)

`asset_id | title | composer | licence type | territory | term | platforms | paid-ads allowed | contract file | date | stems location | used in (video IDs)`

### 6.6 Indian examples

Specific Indian sonic-branding case studies were not verified in this pass. Research recognisable Indian edtech and consumer audio signatures before briefing the composer, and verify each example independently. [Recommendation]

---

## 7. The "Real humans, real emotions" operating rules

### 7.1 Must be genuinely human
1. **Performance of every full lesson (Path A)** once the pilot passes. The teacher's timing, emphasis and feeling are the product.
2. **Direction of every Path B render:** a human chooses mode, pauses and emphasis, and picks takes.
3. **Script rewriting** for Hindi/Hinglish: a native speaker, never raw machine translation [N14].
4. **Subject accuracy review:** a qualified teacher signs off every lesson.
5. **QA listening panel** (Step 13), including students.
6. **Visible human presence:** real hands and handwriting in every lesson, plus at least one real teacher cutaway.
7. **The sonic logo** is composed by a person ExamLeaf contracts (owned, commissioned). *(15 Oct 2026: was "The sonic logo and music"; code-generated beds and SFX are allowed per Step 10 but are never called human-composed.)*
8. **Comment replies** to students come from humans.

### 7.2 May be synthetic (with disclosure where required)
- Voice conversion of a consented teacher performance into the brand voice [N51].
- Directed TTS for Reels, recaps and pickups.
- Transcription, alignment, caption timing [N10], [N49].
- OCR and first-draft translation [N13], [N14].
- Stylised or animated visuals and diagrams. These are non-realistic, so they need no disclosure by themselves [N42] and may get description-only labels [N44].

### 7.3 How to disclose [Recommendation]
- YouTube: use the Studio AI-use toggle whenever the content is realistic and altered or synthetic [N40]. When in doubt, tick it. Labelled videos are reportedly not demoted [P-S12 (contested)].
- In every description, name the human performer and reviewer and state the AI processing. *(15 Oct 2026: use the Path A or Path B template in Step 14; a Path B piece has no performer, so name the script author instead.)*
- A pinned comment, for example "Real teacher, real lesson, AI-assisted voice." *(Path A only; Path B comments name the author as in Step 14)*. In shorts it is not an end-card line: the end card carries the brand line and "Free lesson: <topic>" only (PD-20; `brand/strings.json`).
- Do not strip C2PA metadata to avoid labels [N45].

### 7.4 Consent rules
- Written, specific, revocable consent from every voice performer covering recording, conversion, cloning (IVC needs only about 10 s [N56]), languages and term.
- Guardian consent for any minor on camera or in audio tests.
- A credit line for the performer.
- *15 Oct 2026:* the consent names every third-party processor (for example the STS vendor) that will receive the recordings; that processor must have passed 07/07 admission.
- Revocation process: a removal SLA for future content.

### 7.5 Never do
- Never clone or convert into the voice of a real person without consent. It is disclosable [N41] and unethical.
- Never present a synthetic person as a real teacher.
- Never use music beds to hide errors. Fix the take.
- Never use platform-library commercial music in brand content [P-S34].
- Never claim "100% human" in marketing while using AI processing.
- Never skip disclosure "because nobody can tell". Platforms may detect it anyway [N45], [P-S11], and penalties apply [N46].

---

## 8. A/B test plan

**Design** [Recommendation]: within-subject where possible (each student hears multiple arms in counterbalanced order), with 2–3 STEM topics of comparable difficulty. Sample sizes are **directional**: roughly 30–50 students per arm for a pilot is enough to see large effects only. Expand before deciding anything subtle [Hypothesis].

### 8.1 Arms

| Test | Arm A | Arm B | Arm C (optional) |
|---|---|---|---|
| T1 Voice path | Path A: teacher performance → brand voice (STS) | Path B: directed TTS (ElevenLabs v4) | Path B: Sarvam Bulbul (Hindi) |
| T2 Music | No music under teaching | Low ducked bed under teaching (level per Section 5) | Bed only in intro/transitions/outro |
| T3 Sonic logo | No logo | Logo open+close | — |
| T4 Disclosure | Disclosure line visible | Disclosure in description only | — |
| T5 Hindi form | Devanagari + Latin terms | Romanised Hinglish | — |
| T6 Visuals | Animation only | Animation + real hands + teacher cutaway | — |

### 8.2 Metrics
1. **Appreciation:** a 1–7 "I liked learning from this" rating, and "would watch the next one".
2. **Listening effort:** a 1–7 "how hard was it to follow". This is the key metric for T2.
3. **Immediate comprehension:** a 5-item quiz right after viewing.
4. **Recall at 24–72 h:** the same quiz with item order shuffled, plus a free recall ("what were the three steps?").
5. **AI perception:** "Was this narrated by a person or AI?" plus confidence (1–5). Mirrors [P-S20].
6. **Trust:** "I trust this teacher's explanation" (1–7). Measured before *and after* the disclosure reveal, for T4.
7. **Brand recall** (T3): unprompted "which channel was this?" at 72 h. Compare to [N38]'s direction, not its magnitude.
8. **Platform metrics** (live tests): average view duration, % viewed for Reels, replays, saves, shares, and comment sentiment mentioning "AI" or "robot".

### 8.3 Decision rules [Recommendation]
- **T2 music:** adopt a bed under teaching only if listening effort and 72 h recall are *not worse* *and* appreciation improves. Otherwise keep music off (default).
- **T1 voice path:** if Path A beats Path B on trust or appreciation with equal recall, make Path A the standard for full lessons.
- **T4 disclosure:** expect a small trust dip at reveal. Measure whether the "real teacher" framing removes it.

---

## 9. Skills and automation stack

The pipeline maps to automation as follows, adopted in this order [Recommendation]:

| Order | Pipeline stage | Skill / tool | Evidence | Admission caveat |
|---|---|---|---|---|
| 1 | Lexicon management | Git-versioned JSON + scripted Sarvam dictionary upload/update | [N63]–[N66] | In-house script; no third-party skill needed |
| 2 | Script pre-processor (spoken forms, respellings, beat tags → API params) | In-house | [N7], [N6] | Small script; one test per subject |
| 3 | TTS and STS generation | ElevenLabs official skills, installed with `npx skills add elevenlabs/skills` [N47]. They follow the Agent Skills spec [N48] | [N47], [N48], [N51] | *15 Oct 2026: the skill and the STS processor itself go through the 07/07 admission process (§2, §4, §7).* **Admission review before install:** read every skill's files, pin a commit, run in a sandboxed repo, keep API keys in env vars (never in prompts). The voice changer skill's details are contested [N51] |
| 4 | Transcription and alignment | ElevenLabs speech-to-text skill (speaker IDs + timestamps) [N49 (contested)]; realtime `scribe_v2_realtime` [N50 (contested)]; or Sarvam Batch STT [N10] | [N10], [N49], [N50] | Contested capabilities: verify word-level timestamp output on a Hindi sample before relying on it |
| 5 | Account and agent management | Hosted ElevenLabs MCP (OAuth, no local install) [N53] | [N53] | Grants account access to an assistant; least privilege, and the founder approves the OAuth grant personally |
| 6 | Voice agent ("ask the Super Teacher") | Speech Engine skill [N52 (contested)] | [N52] | Out of scope for video; park it |
| 7 | Render | HyperFrames master timeline (Remotion benchmark only; Manim inserts) driven by the alignment JSON via the cue sheet *(15 Oct 2026: was "Remotion / manim-voiceover"; 12 AD-01)* | Unverified | Pilot on one lesson |

**Human gates that automation must not bypass:** Step 6 take selection, Step 13 QA panel, Step 14 disclosure tick, and the consent check before any voice conversion. *(15 Oct 2026: add the Path A wording diff and GA re-approval when wording changed (Step 3); the disclosure tick is a release blocker, RD-45.)*

---

## 10. Open questions, unverified items, vendor questions

### 10.1 Unverified in this pass (do not rely on yet)
- **Effect of background music under narration on STEM learning.** No verified study. This is the core uncertainty behind the founder's question.
- **Platform loudness targets and true-peak handling** for YouTube, Shorts and Instagram Reels.
- **Caption safe zones** for Reels and Shorts.
- **Instagram/Meta AI-label rules and India's synthetic-media labelling rules** (MeitY/IT Rules). Get legal review.
- **Gemini 3.8 TTS and Cartesia Sonic:** controls, Hindi quality, pricing.
- **Open-source voice conversion** (RVC, Seed-VC, OpenVoice, Chatterbox): quality on Hindi, licence terms.
- **Adobe Podcast, Auphonic, iZotope RX, WhisperX, Remotion, manim-voiceover, HeyGen, Hedra, Veo:** settings and costs.
- **YouTube tutorials and creator "hacks":** this pass verified documentation and blogs. Creator videos were not systematically reviewed. Any hack from them needs testing before adoption.
- **Prosody preservation in speech-to-speech for Indian languages, for any vendor** (gap carried over from the earlier register).
- **Indian sonic-branding case studies** and commission price ranges.

### 10.2 Contested items to re-check
[N28], [N35], [N40], [N49]–[N52], [N68]; and [P-S2]–[P-S5], [P-S8], [P-S10]–[P-S18], [P-S25], [P-S26].

### 10.3 Vendor questions

**ElevenLabs**
1. Is Hindi (and Hinglish code-mixed input) officially supported and evaluated on v4, v4 Turbo and `eleven_multilingual_sts_v2`?
2. What are the recommended stability, style and similarity settings for teaching narration on v4?
3. How does STS handle Hindi retroflex consonants and English technical terms within Hindi?
4. Does exported audio carry C2PA or other provenance metadata?
5. What are the commercial terms for an own-teacher PVC, and do they include revocation?
6. Is there a pronunciation-dictionary equivalent for v4?

**Sarvam**
1. What is Bulbul v4-flash's production status and roadmap, including Assamese?
2. Will the dictionary cap above 100 words be raised?
3. Are expressive or emotion controls planned?
4. Is Assamese OCR accuracy published for Sarvam Vision?
5. Is there pricing for Batch STT on 10-minute lessons?

**Google / Cartesia:** Hindi voice list, style-prompt controls, pricing, and data-retention terms.

**Legal counsel:**
1. A template voice-performer consent and licence (including conversion and cloning).
2. Indian synthetic-media labelling duties.
3. Music commission buyout terms.
4. Whether converting a consented teacher into a *designed* brand voice changes YouTube disclosure status.

### 10.4 Internal questions
- Who are the 1–2 pilot teachers (Hindi and English), and what will they be paid?
- What budget is there for the sonic logo commission?
- Is there a student panel and guardian-consent process for the A/B tests?

---

## Sources

### Prior register (earlier pass)
Full table: `/Users/chinmoybhuyan/Desktop/Personal/Book/Videos/ExamLeaf_Video_EdTech_Pipeline/11_human_feel_voice_audio_research/SOURCES_and_claims.md`
- [P-S1]–[P-S5]: https://docs.sarvam.ai/api-reference-docs/getting-started/models/bulbul
- [P-S6]–[P-S10]: https://www.hollywoodreporterindia.com/features/insight/indias-microdrama-boom-how-data-desire-and-aritifical-intelligence-are-reshaping-entertainment
- [P-S11]–[P-S13]: https://thenextweb.com/news/youtube-will-now-automatically-label-ai-generated-videos-whether-creators-disclose-them-or-not
- [P-S14]–[P-S19]: https://docs.sarvam.ai/api-reference/text-to-speech/convert.md
- [P-S20]–[P-S22]: https://radioink.com/2026/07/07/radio-listeners-cant-detect-ai-voice-but-dont-trust-it-either/
- [P-S23]–[P-S28]: https://www.afaqs.com/news/ott-streaming/kuku-fm-launches-vertical-microdrama-ott-platform-kuku-tv-8718086
- [P-S29]–[P-S34]: https://www.medianama.com/2026/05/223-zee-nykaa-delhi-high-court-copyrighted-songs-instagram-reels
- [P-S35]–[P-S39]: https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/overview.md

### New evidence (this pass)
- [N1]–[N7]: https://elevenlabs.io/docs/best-practices/prompting
- [N8]–[N14]: https://docs.sarvam.ai/api/getting-started/building-for-india
- [N15]–[N21]: https://elevenlabs.io/docs/product-guides/playground/voice-changer
- [N22]–[N27]: https://www.sonarworks.com/blog/learn/mastering-ai-vocals-eq-and-compression-tips
- [N28]–[N34]: https://www.music-news.com/news/Underground/190732/Minjia-Du-talks-subtle-sound-design-for-booming-vertical-drama-industry
- [N35]–[N39]: https://ora.ox.ac.uk/objects/uuid:a3db49b9-75e6-41c9-b31e-586b4f76b605/files/rt148fj539
- [N40]–[N46]: https://support.google.com/youtube/answer/14328491
- [N47]–[N53]: https://elevenlabs.io/docs/eleven-api/resources/agent-tooling
- [N54]–[N59]: https://elevenlabs.io/blog/eleven-v4
- [N60]–[N66]: https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/pronunciation-dictionary
- [N67]–[N71]: https://blog.segmind.com/elevenlabs-voice-changer-how-to-convert-voices-in-2026/
- [N72]–[N76]: https://www.sonarworks.com/blog/learn/compression-strategies-for-ai-generated-backing-vocals
