# Voice and Persona Registry (Content Engine v2 subsystem)

Status: specification, not a build; nothing here has run. Date: 15 Oct 2026. Owners: academic lead (personas), founder (voices), native-language editors and the child-development reviewer where named.
Machine contracts: `schemas/persona.schema.json`, `schemas/voice_asset.schema.json` (draft-07; parse, meta-validation, commercial-term lint and positive/negative instance checks passed 15 Oct 2026). Templates: `templates/persona.template.md`, `templates/voice_asset.template.md`.
Generalises, does not replace: the 03 Super Teacher core, the 05 VoiceIdentity/NarrationPlan/lexicon/compiler/QA/mastering stack, the 11 Path A/B playbook, the 07/04 locale gate and the 07/07 consent rules.

**Citation keys.** [CE-N#] = 15 `SOURCES_and_claims.md`; [11-N#] = 11 PLAYBOOK evidence; [11-S#] = 11 REPORT evidence. Documents by section: [05-VIG] voice identity guide, [05-TTS] provider comparison, [05-NP] narration pipeline, [03-ST] Super Teacher authoring, [07/04], [07/07], [Arch], [LP] Level Profiles, [FR] Format Registry. **[Recommendation]** = design choice; **[Hypothesis]** = pilot must confirm; "verify" = not established in project documents.

---

## 1. Place in the architecture

- **Registries.** `persona/` and `voice/` exist in Arch §3.1. This document adds two supporting id prefixes **[Recommendation]**: `lex/` for pronunciation lexicons (referenced by the Locale Profile `lexicon_ref`) and `gs/` for golden sets. Both need a CE decision row before M1.
- **Resolver.** R1 fixes the path; R8 gives the persona the lowest precedence, so it never sets a number; R9 lets a locale change surface only (lexicon, script, register, voice); R11 takes the persona from the level, lets an overlay add a register and never relaxes safety or retired-expression rules.
- **EPP pins.** `persona@version#variant`, `voice@version` (or the performer/target pair), `lex@version`, ~~`gs@version`,~~ and the R1 conditions that fired. Narration audio is stored by hash and replayed (CE-38). *(Corrected 15 Oct 2026.)* The golden set is not an EPP pin. It is recorded on the voice entry (voice_asset `golden_set.golden_set_ref` and `golden_set_sha256`), so it reaches an artefact only through the voice pin. A voice re-versioned after a GL-voice re-run follows the "New model, voice id or settings" row of §3.10.
- **Gates.** VOICE (S9), GL-voice and GL-glossary (locale), DISCLOSURE, GF/GS, and the child-development co-sign for AC0.

**Voice selection** ~~(inside S9, after R1)~~ (in the Resolver at S5, rule R13; corrected 15 Oct 2026) **[Recommendation]**:
1. Candidates: `admitted`, same locale, persona listed, format/level/safety/family allowed, unexpired, and a matching role (Path A: `A_direct_release`, or performer `A_performance_source` + brand `A_conversion_target`; Path B: `B_tts`). A performer/target pair is refused unless the target's `provider.model_id` is listed in the performer's `rights.consent.models_permitted` (XF-5, §4.1; added 15 Oct 2026).
2. ~~One stable lead voice per course and locale [05-VIG §1]: series members reuse the first member's voice; otherwise the Locale Profile's first admitted voice.~~ *(Corrected 15 Oct 2026: under CE-L2 and R1 a later Path B member cannot reuse a Path A member's conversion target.)* One brand voice identity per course and locale [05-VIG §1]. A series pins the `voice_identity.identity_id` of its first member. Every later member selects only entries with that `identity_id`: an `A_conversion_target` for Path A, a `B_tts` entry for Path B. GR assigns one `identity_id` only to entries that render the same brand voice, for example one provider voice used for both STS and TTS. If no admitted entry of that identity exists for the member's path, rule 3 applies. `A_direct_release` series (as-IN) pin the `performer_ref` instead. A standalone artefact takes the Locale Profile's first admitted voice of the required role. When the pinned voice is superseded, later members pin its `superseded_by` successor (the change is recorded on the series); released members keep their stored audio (CE-38). The Resolver and RELEASE-CHECK enforce this as XF-3 (§4.1). R1 (CE-24) is unchanged.
3. No candidate means a compile error, never a substitute: "a fallback must be an approved voice/model combination, or the job should wait" [05-TTS §7].

---

## 2. Persona registry

### 2.1 The shared core (`persona/super-teacher`, kind `root`)

Identity: "warm toward the student, exacting about the science, and playful about the problem" [03-ST Step 1]. Priority: scientific correctness → independent capability → accessibility → warmth → humour [03-ST Step 1]. Intelligence shows through explanation, warmth through repair, confidence through a check [05-VIG §2].

**Shared never-do rules** (the fifteen `core_rules`; the schema requires all of them in every persona; personas may add, never remove).

| Rule id | Meaning | Source |
|---|---|---|
| `no_fake_sensing` | A prerecorded voice never claims it heard or saw the learner | [05-VIG §2, §6]; [03-ST Step 7] |
| `no_invented_biography` | No invented classroom memories, degrees or experience | [03-ST Step 9] |
| `no_impersonation` | No imitation of Professor Dave, Sal Khan, a celebrity or a real teacher | [05-VIG §1] |
| `no_unconditional_praise` | Praise is conditional on a demonstrated action | [03-ST Step 9]; [11 addendum 4] |
| `no_ease_or_marks_guarantees` | No "this is easy", "guaranteed full marks", "only geniuses" | [05-VIG §2] |
| `no_ridicule_or_sarcasm_at_learner` | No mocking of intelligence, marks, accent, caste, gender or money | [03-ST Step 8] |
| `no_fake_disfluency_or_laughter` | No added ums, breaths or laughs as a proxy for being human | [05-VIG §2]; [03-ST Step 2] |
| `no_intention_as_cause` | Molecules, enzymes and evolution do not "want" anything | [05-VIG §7] |
| `no_pressure_fear_or_urgency` | No fear, urgency, peer comparison or streak pressure | [LP §2] |
| `no_data_solicitation` | Never asks for names, schools, photos, comments or voice | [LP §2]; CE-20 |
| `no_claims_outside_closure` | Every assertive sentence maps to approved nodes | CE-12 |
| `no_stage_tags_in_spoken_text` | Direction lives outside canonical spoken text | [05-VIG §3] |
| `no_speeding_science_to_fit_time` | Shorten words or split chapters; never rush a formula | [05-VIG §5.2] |
| `humour_ceiling_not_quota` | Zero jokes is acceptable; 3–5 per 10 minutes is a ceiling to test | [03-ST Step 8] |
| `answer_hidden_until_window_ends` | No reveal, caption or preview inside a response window | [05-NP §7.2] |

**Retired expressions** (persona-lint seed, all personas): "Let's dive into the fascinating world of…", "Prepare to have your mind blown!", "This is super easy!", "Boom! You have mastered the chapter!", "Even a child can understand this." [03-ST Step 2]; "I heard you", "You all got it", "Got it? Beautiful" [05-VIG §2, §6]; an unconditional "You've got this" [11 addendum 4].

### 2.2 Resolution: level to persona variant

The architecture names nine personas (Arch §6). This registry keeps the five ids in the build brief and carries the architecture names as **variants**, so every name resolves and nothing is lost.

| Level | Safety | Persona id | Variant | Architecture name |
|---|---|---|---|---|
| l1_2, l3_5 | ac0 | `persona/super-teacher-junior` | `junior` | Super Teacher Junior |
| l6_8 | ac1 | `persona/super-teacher-junior` | `coach` | Super Teacher Coach |
| l9_10 | ac1 | `persona/super-teacher` | `core` | Super Teacher |
| l11_12 | ac1 | `persona/super-teacher` | `mentor` | Super Teacher Mentor |
| ug, adult_prof | ac1 / ac2 | `persona/lecturer` | `lecturer` | Lecturer |
| pg | ac2 | `persona/lecturer` | `seminar-lead` | Seminar Lead |
| educator | ac2 | `persona/lecturer` | `colleague` | Colleague |
| voc | ac1 | `persona/skills-instructor` | `instructor` | Skills Instructor |
| any base level + overlay (not jnvst) | inherits | `persona/exam-coach` (register overlay) | `strategist` | Exam Strategist |

The `overlay/jnvst` overlay on l3_5 never activates `persona/exam-coach` (AC0: no strategy, time pressure or marks framing [LP §5]); the schema forces every register overlay to exclude `safety/ac0`.

### 2.3 Persona entries

**`persona/super-teacher`** (root; variants `core`, `mentor`). *Identity:* warm toward the learner, precise about the science, occasionally amused by the problem; interested, not constantly excited [05-VIG §1]. Reveals decisions and hands them over: "Watch how I choose the step" → "You choose the next step" → "Now choose the method without my help" [03-ST Step 2]. *Mentor (l11_12):* exam-aware, deeper derivations, fewer hooks [LP §3.5]; returns every result to exam notation and units. *Register:* board terms with glossary (core), discipline register (mentor); humour concept-linked.

**`persona/super-teacher-junior`** (derived; variants `junior`, `coach`). *Identity (junior, Classes 1–5):* the same teacher at the child's eye level: warmer, slower, shorter sentences, concrete objects, one idea per sentence, play-safe humour (silly objects, gentle surprises, never people), no sarcasm, read-along cadence on text. Narration carries all meaning for pre-readers [LP §3.1]; interaction is say-aloud, point, move, draw and sing [CE-N10] with real pauses; never frames the child as wrong (CE-42); one language per lesson unless the child-development reviewer approves a code-mix (Arch §8). *Coach (Classes 6–8):* inquiry questions, "what would happen if…", experiment framing; less performative than junior, more Socratic than the current Super Teacher [LP §3.3]. *Additional never (junior):* like/subscribe/share prompts, brand names, urgency, "wrong!", asking a name or school, any non-household-safe activity [LP §2]; *(coach)* fear or comparison under junior overlays [LP §5].

**`persona/lecturer`** (derived; variants `lecturer`, `seminar-lead`, `colleague`). *Identity:* an academic addressing a junior colleague: fewer interjections, explicit notation and definitions, talking-head inserts at transitions [CE-N4], drawn derivations [CE-N5] [LP §3.6]. Rigour markers are spoken ("under the assumption that", "we have not yet shown"); derivations run one justified line at a time. *Seminar lead (PG):* cites sources on screen, models critique, states uncertainty [LP §3.7]. *Colleague (educator):* teacher-to-teacher, F26. *Additional never:* "we'll make it easy", "don't worry about the maths", "obvious" steps, certainty about contested claims.

**`persona/exam-coach`** (register overlay; variant `strategist`; overlays jee, neet, cuet, olympiad_junior, olympiad_senior, nmms, upsc, state_psc, ca_cs). *Identity:* a calm strategist; credibility before motivation ("Precise and credible, not promotional" [05-VIG §3]). Time management is a plan the candidate owns, never a countdown; calm under pressure means naming the next small action. Pattern statements are cited, time-bound `exam_pattern` claims with as-of dates [FR F9]. *Additional never:* "this will come" without evidence [FR F9]; fear, urgency or comparison [LP §2]; marks promises or marks on original items (CE-31).

**`persona/skills-instructor`** (derived; variant `instructor`; level/voc). *Identity:* a trade practitioner: procedural, safety-first, demonstration-led [LP §3.9]. One imperative step per sentence; the safety cue precedes the action at deliberate pace and is never shortened; names the check that proves a step was done right. *Additional never:* hazard jokes, unsafe shortcuts even as a gag, a rushed or skipped `activity.safety_cue`, safety implied without a safety claim.

### 2.4 Delivery modes

The narration schema allows exactly six modes; 03 defines five and 05 adds `focused` (RD-12: until the engine `Cue.voice` contract merges `focused`, engine cues map it to `deliberate`).

| Mode | Definition [05-VIG §3] | Best use [03-ST Step 10] | Personas |
|---|---|---|---|
| `curious` | A real question; slight anticipation; no horror-trailer suspense | Opening, prediction | all |
| `steady` (default) | Most explanations; causal words carry emphasis | Most teaching | all |
| `deliberate` | Units, signs, conditions, formulas; separate related terms | Conditions, units, misconceptions, safety cues | all |
| `light` | One dry, concept-linked observation; no forced laugh | A brief relevant observation | junior and coach (play-safe), core, mentor; rare for lecturer and exam-coach; never for skills-instructor in a safety beat |
| `reassuring` | Specific correction; no pity or fake intimacy | Feedback and repair | all |
| `focused` | Exam strategy and final checks; credibility before motivation | Strategy, checks | core, mentor, lecturer, exam-coach, skills-instructor; not junior |

**Candidate addition `cadenced`** **[Recommendation]**: the steady, rhythmic, one-word-at-a-time delivery used for Read-Along (F23) highlighting and chants. Adding it is a contract change to the 05 narration schema and the engine `Cue.voice` enum with an ADR. Until then, use `steady` with a `notes` direction ("even rhythm; one word per highlight").

### 2.5 Pacing bands per level and locale

Personas own **no** numbers (CE-16, R8); these are the Level Profile values, quoted for directors.

| Level | Ordinary (wpm) | Dense / new symbolic | Recap | Think window | Source and tag |
|---|---|---|---|---|---|
| l1_2 | calibrate | calibrate | calibrate | RD-11 floor (5–8 s, default 6 s); may be lengthened | [LP §3.1]: Path A teacher sets natural pace; no adult WPM imported [Hypothesis, owner child-development reviewer] |
| l3_5 | calibrate | calibrate | calibrate | as l1_2 | [LP §3.2] [Hypothesis, owner child-development reviewer] |
| l6_8 | 130–155 | 105–125 (02 §G2 text: ~90–120; §6) | 145–165 | RD-11 | [LP §3.3]: 02 §G2 bands as [Hypothesis, owner academic lead, A/B] |
| l9_10, l11_12 | 130–155 | 105–125 | 145–165 | RD-11 | [LP §3.4–3.5] Inherited; recap from [05-VIG §5.1] |
| ug, pg, adult_prof | 130–155 | 105–125 | 145–165 | RD-11 | [LP §3.6–3.7] Inherited defaults; faster bands only as [Hypothesis] under A/B |
| voc | calibrate | calibrate | calibrate | RD-11 | [LP §3.9] [Hypothesis, owner trade instructor] |
| educator | not set in LP | not set | not set | RD-11 | gap; calibrate |

**Locales.** hi-IN, Hinglish and as-IN have **no** wpm values: "Never translate these exact rates blindly across languages" [05-VIG §5.2]; "Do not transfer English word-rate targets to other languages" [07/04 §3]. Each locale's band is measured by its native editor in GL-voice or the first Path A pilot [Hypothesis, owner native-language editor, pilot GL-voice-1]; an overrun is a compile error (R5), never a speed-up. **Within a band**, `deliberate` runs slowest and `light`/`curious` fastest; for l9_10 the 11 starting values are steady 140–150, deliberate 130, light/curious 150–155 [11 §5, Recommendation].

### 2.6 Emotional-direction map per beat and persona

Beats map to slot types: hook (`hook.*`), prerequisite (`check.predict` diagnostic, repair rungs), core (`explain.*`), worked (`worked.step`), guided (`worked.faded_twin`, `check.interpolated`), independent (`check.retrieval`, practice items), misconception (`misconception.*`), recap (`recap.*`), CTA (`close.next_step`). "CTA" always means a **learning** next step, never a platform call to action. Cells give mode and intent [Recommendation; derived from 05-VIG §4 and 02 §G4 "curious opening → steady explanation → deliberate emphasis → quiet attempt → precise feedback → calm conclusion"].

| Beat | junior (ac0) | coach (l6_8) | core (l9_10) | mentor (l11_12) | lecturer / seminar (ug, pg) | exam-coach (overlay) | skills-instructor (voc) |
|---|---|---|---|---|---|---|---|
| hook | curious: a small wonder, no suspense | curious: "what would happen if…" | curious: real question, modest anticipation | curious: a question with stakes, no hype | steady: motivating problem stated precisely | focused: name the trap calmly | curious: what we will make; safety named |
| prerequisite | reassuring: "let's remember together" | steady: quick check, no labelling | steady: "Need the symbol-reading version? Start here." | steady: assumed knowledge stated | deliberate: definitions and notation fixed | focused: the minimum you need | deliberate: tools, protection, conditions |
| core | steady: one idea, one object | steady: reasoning aloud | steady: causal words emphasised | deliberate: each relation justified | deliberate: assumptions spoken | steady: method, never a trick | steady: one step per sentence |
| worked | steady: count or do with objects | steady: "watch how I choose" | deliberate: decision behind each step | deliberate: every step justified | deliberate: each line derived; notation read exactly | deliberate: set up first, then arithmetic | deliberate: demonstrate, name the check |
| guided | reassuring: "let's try together" | curious: "you choose the next step" | reassuring: specific, repairable | reassuring: conditional feedback | curious: "pause and complete the line" | focused: your set-up, then check | reassuring: do-along, check your set-up |
| independent | curious: say-aloud or point, then silence | curious: predict, explain, check | focused: fresh question, no example | focused: transfer item | curious: interpolated question or critique | focused: self-paced attempt with your own time plan | focused: procedure check |
| misconception | light: gentle surprise, never "wrong" | curious: predict, then evidence | deliberate: tempting idea visibly retired | deliberate: contrast with the condition | deliberate: where the model fails | deliberate: common strategic error, blamed on the method | deliberate: unsafe shortcut named and refused |
| recap | steady (or sung `story.song_chant`): same words as the story | steady: retrieval first | steady: retrieval before statement | focused: formula plus condition | steady: results and assumptions | focused: the rule to carry into the paper | focused: steps in order; safety last |
| cta | reassuring: next story; "with a grown-up" where relevant | steady: one thing to try | focused: one fresh question without reopening | focused: delayed-practice action | steady: next segment or reading | focused: next practice set | focused: practise under supervision |

**Per level.** AC0: more warmth, less energy, never suspense or a clock, a real pause after every invitation. l6_8: more curiosity. l11_12: fewer hooks. UG: fewer interjections; PG: uncertainty stated.

### 2.7 Persona lint (Q-PERSONA)

Q-PERSONA runs report-only first, then blocks (Arch §9.1). It runs on scripts at S7 and on **performed or synthesised transcripts** at S9 (ASR text), because a Path A performer can ad-lib. Checks: retired expressions per persona; fake-sensing patterns ("I heard you say", "I can see you got", "you have definitely mastered" [03-ST Step 15]); persona bans ("we'll make it easy", "this will come in the exam", "wrong!" at AC0, "tell me your name"); unconditional praise. Stage tags in spoken text are blocked by the narration contract, not by the linter.

---

## 3. Voice asset registry

### 3.1 Kinds, fields and admission

| Kind | Path role | What it is |
|---|---|---|
| `human_performer` | `A_direct_release` | The performer's own recorded voice is released (the as-IN route) |
| `human_performer` | `A_performance_source` | The performance is converted by speech-to-speech |
| `sts_target_voice` | `A_conversion_target` | Licensed or consented brand voice that STS converts into |
| `tts_voice` | `B_tts` | Directed TTS voice (provider, model and voice id) |

**Fields** (full contract in the schema): id, version, kind, path role, personas, locale; `performer` (pseudonymous, adult, never a student); `provider` (exact `model_id`, voice ref, verified live contract, 07/07 admission, lifecycle dates); `rights` (05 `rights_status` enum, consent scope, counsel review O-6); verification; `gl_voice`; `native_review`; `golden_set` hash; lexicons; `allowed` formats, levels, safety classes and families; disclosure; expiry and renewal; `voice_identity` (compiles to the 05 `VoiceIdentity`); revocation. Names, contracts, amounts and audio stay in the private store; git holds only `private://` pointers [07/07 §7].

**Schema-enforced admission.** `admitted` needs cleared rights (`licensed-stock`/`consented-custom`) and a passed native review; provider voices add a verified live contract and a passed golden set; TTS adds GL-voice. `B_tts` never lists `safety/ac0`. An STS source must consent to conversion and name a processor. as-IN admits only `A_direct_release`. Disclosure must match the path role. "REPLACE" voice ids fail [05-TTS §7].

*Added 15 Oct 2026.* Every STS target and TTS voice declares `target_origin`: `designed_synthetic`, `performer_clone` or `provider_stock`. A `performer_clone` names the `performer` and needs `consented-custom` rights, consent uses including both `identity_reference` and `voice_clone`, at least one named processor, counsel review (O-6) and the provider's verification record [07/07 §7; 11 Step 4]. A consented-custom synthetic voice (STS target or TTS) carries the structured consent (uses including `identity_reference` or `voice_clone`, languages, territories, platforms, term, revocation), counsel review (O-6) and the provider's verification record. Consent that allows conversion, cloning or an identity reference lists `models_permitted`; every consent records `raw_audio_retention_until` and `removal_sla_days` [07/07 §7; 05-NP §15; 11 §7.4]. A golden-set result of pass or fail names `tested_model_id`, `tested_provider_voice_ref` and `last_run_date`; an admitted provider voice also records the golden-set `reviewer_ids` and the accepted-audio manifest hash. as-IN requires `performer.native_speaker_of_locale: true`. A `superseded` entry names `superseded_by`. A `consent_withdrawn` revocation under `withdraw_published` records each processor's deletion confirmation and `replay_store_purged: true`. Comparisons between two fields (tested model equals current model, consent language covers the locale, expiry within provider and consent dates) are beyond draft-07 and run as the cross-field checks XF-1 to XF-5 (§4.1).

### 3.2 Path A vs Path B by format and level (CE-L2, R1)

R1 forces A if the format default is A, `series_position = first`, `flagship`, `demo_kind = real`, `safety/ac0`, level floor A, or no GL-voice-passed TTS voice in the locale (CE-24). **Today every artefact resolves to Path A**: no GL-voice pass is recorded (CE-41, O-12).

A = Path A by format default or AC0 floor; B = Path B unless R1 fires; — = not offered (LP §6). F2 and F18 at adult_prof are B since 15 Oct 2026 (LP §6).

| Format | l1_2 | l3_5 | l6_8 | l9_10 | l11_12 | ug | pg | adult_prof | voc | educator |
|---|---|---|---|---|---|---|---|---|---|---|
| F1 detailed | A | A | A | A | A | A | A | A | A | — |
| F2 simplified | — | A | B | B | B | B | — | B | B | — |
| F3 recap | A | A | B | B | B | B | B | B | B | — |
| F4 question_analysis | — | A | B | B | B | B | B | B | B | — |
| F5 short | A | A | B | B | B | B | B | B | B | B |
| F6 worked_example | — | A | B | B | B | B | B | B | B | — |
| F7 misconception_fix | A | A | B | B | B | B | B | B | B | — |
| F8 concept_intro | A | A | B | B | B | B | B | B | B | — |
| F9 exam_strategy | — | — | B* | B | B | B | — | B | — | — |
| F10 revision_sheet | — | — | B | B | B | B | B | B | B | — |
| F11 flashcard_reel | A | A | B | B | B | B | B | B | B | — |
| F12 lab_demo | A | A | B/A† | B/A† | B/A† | B/A† | B/A† | B/A† | B/A† | — |
| F13 comparison | — | — | B | B | B | B | B | B | B | — |
| F14 story_history | A | A | B | B | B | B | B | B | B | — |
| F15 qa_doubt | — | — | B | B | B | B | B | B | B | — |
| F16 series | members; bridges A | members; bridges A | members; bridges B | … | … | … | … | … | … | members |
| F17 practice_set | — | A | B | B | B | B | B | B | B | — |
| F18 prerequisite_repair | — | A | B | B | B | B | B | B | B | — |
| F19 derivation_proof | — | — | — | — | A | A | A | — | — | — |
| F20 lecture_segment | — | — | — | — | — | A | A | A | — | — |
| F21 source_analysis | — | — | B | B | B | B | B | B | — | — |
| F22 perspectives | — | — | — | B | B | B | B | B | — | — |
| F23 read_along | A | A | A | — | — | — | — | — | — | — |
| F24 concept_map | — | — | B | B | B | B | B | B | B | — |
| F25 viva_prep | — | — | — | — | B | B | B | — | — | — |
| F26 teacher_explainer | — | — | — | — | — | — | — | — | — | B |

\* only with olympiad_junior or nmms. † A when `demo_kind = real`. For as-IN and other Indic locales, every cell is A, delivered as `A_direct_release` for as-IN (§3.5).

**No mixing inside one artefact** **[Recommendation]**: Path A pickups go back to the performer, not TTS; mixed paths exist only in F16 compositions, with the mixed disclosure (§3.9).

### 3.3 Performance-capture protocol

**Common protocol (every persona)** **[Recommendation; built on 11 Step 3 and 05-NP §15]:**
1. **Preconditions.** GA-Δ approved the script bundle (hash on the session sheet); consent covers this locale, use, platform and every processor; the performer is not this artefact's GF approver (Arch §3.2).
2. **Recording sheet** from the NarrationPlan: spoken text after `{{token}}` expansion, mode, emphasis, pause kind and task (inserted in the edit, **not performed**), critical phrases, take number [05-NP §8]; plus the lexicon card.
3. **Room.** Quiet room, close mic, 48 kHz/24-bit WAV, 30 s room tone per session [11 Step 3].
4. **Direction.** Brief the learner, not the line; one rehearsal, two keeper takes per beat; wording fixes are re-approved **before** recording; real breaths, never fake sensing or new claims [11 Step 3].
5. **STS takes** under 5 min and 50 MB [11-N15][11-N16], lossless [11-N21], heads and tails trimmed [11-N71].
6. **After.** ASR diff of every keeper take against the approved script (`qa.transcript_check`, tokenised by 05 `normalized_words()`: NFC + casefold; word = run of Unicode L/M/N; ZWJ/ZWNJ transparent; maths symbols single tokens; 05 CHANGES.md 2026-10-15; a surface diff only, so native review is still required) and Q-PERSONA on the transcript; any change returns to GA on a new bundle hash, else re-record [11 addendum 2].

| Persona / variant | Learner to brief | Direction specifics |
|---|---|---|
| junior: Class 2 story | "One six-year-old sitting beside you, holding the torch." | Smile in the voice; slower; one idea per breath. The performer gives the invitation ("Say it out loud!") and **stops**; the pause is room tone inserted in the edit (RD-11). No pretend replies. Owned songs only. The child-development reviewer approves the direction sheet and the keeper takes **[Recommendation]**. No child voices in `voice/` (a child voice is a MED asset with a guardian release, CE-54; never a student). |
| junior: read-along | "A child following each word with a finger." | `cadenced` direction via `steady` + notes; record line by line so highlights align; every word fully voiced; the native editor checks phonics and vowel length. |
| coach (l6_8) | "A curious twelve-year-old who keeps asking 'what if?'" | Inquiry tone; real questions; predict-explain-check rhythm. |
| core (l9_10) | "A Class 10 student in Jorhat who has got this numerical wrong for the third time." [11 Step 3] | Explain it to one person, not to a room; let causal words land. |
| lecturer: UG / Masters derivation | "A first-year (or Masters) student copying each line from the board." | One derivation step per take, in sync with the drawn board (16:9 head inserts need an on-camera release). Notation read per the lexicon register variant; pause-video for long steps; assumptions at `deliberate`; PG states uncertainty. |
| exam-coach | "A candidate a week before the exam, steady but short of time." | `focused`, calm, clear; no countdown voice; pattern lines read exactly as cited, with as-of date. |
| skills-instructor: real demo | "A trainee standing at the bench beside you." | Sync sound with the demo; the safety cue is its own beat, re-recorded in quiet if machine noise masks it (never shouted); one step per take; noise isolation on recorded input only [11-N69]. |

### 3.4 Speech-to-speech rules and consent

- **Where it matters most:** a dry joke, a difficult multilingual transition, a careful contrast, subtle reassurance [05-TTS §2.5]. Under CE-L2 whole artefacts are Path A, so this steers rehearsal effort, not path.
- **STS fixes nothing academic** ("does not automatically fix wrong science, missing words, or an incorrect pronunciation" [05-TTS §2.5]); the wording diff and critical-term listening run on the source take **and** the converted output.
- **Documented model facts.** ElevenLabs' English STS is English-only; multilingual STS is used for Hindi/Hinglish [11-N20][11-N51, contested]; multilingual v2 covers 29 languages but Hindi is not named [11-N19]: verify Hindi STS. **Verified 16 Oct 2026 in the live docs: `eleven_multilingual_sts_v2` lists Hindi (hi) among its 29 languages, so Hindi conversion is documented; admission (07/07) and the native gate still apply. See `05_narration_system/ELEVENLABS_SETUP_2026-10-16.md`.**
- **Admission.** Every STS processor (ElevenLabs Voice Changer, a reseller or other) passes 07/07 admission and is **named in the performer's consent** before any recording reaches it [11 addendum 5; 07/07 §4].
- **Consent is specific.** A performance reference is not an identity reference; the latter needs specific permission and the provider's verification. Consent to record a lesson is not consent to a reusable synthetic identity [07/07 §7]. The record covers uses, languages, territory, term, platforms, revocation and deletion; compensation exists in the contract, never as amounts here (CE-L1). The voice is never used for content the performer has not seen [11 Step 3]. The brand voice is the performer's own or a designed (non-real-person) voice; never convert into a non-consenting real person [11 Step 4].
- **Never** student recordings ("Avoid collecting student recordings for voice cloning" [07/07 §7]); never convert an `audition-only` flag into fictional consent [05-NP §15].

### 3.5 Provider matrix per locale (facts from 05-TTS; Sarvam from 11-REPORT and 07/04)

"Admitted" = the 05 compiler accepts the locale (`compiler.LANGUAGES`); it is **not** approval [05-TTS §3]. No row has a GL-voice pass.

| Provider / model | en-IN | Hinglish | hi-IN | as-IN | Other Indic | Notes |
|---|---|---|---|---|---|---|
| ElevenLabs `eleven_v4` | admitted | verify (no Hinglish locale in the compiler; test code-switching) | admitted; documented | admitted and documented, **not used** (RD-42) | verify | Primary expressive candidate; no SSML or legacy speed/style controls; text-to-dialogue route [05-TTS §2.1] |
| ElevenLabs `eleven_v3` | admitted | verify | admitted | admitted, not used | verify | Reference profile |
| ElevenLabs `eleven_multilingual_v2` | admitted | verify | admitted | rejected (tested) | verify | No mode tags |
| Gemini `gemini-3.8-flash-tts` / `-flash-lite-tts` | admitted | verify | admitted; documented | documented, not used | verify | Spoken text separate from `speech_metadata.style`; custom voice storage and expiry need a renewal policy; never live-synthesised here [05-TTS §2.3] |
| Cartesia `sonic-3.5-2026-05-04` (snapshot; 3.6 marketed, untested) | admitted | verify (worth testing) | admitted | **not admitted** | verify | Compile fails without a verified `api_version`; speed is a heuristic [05-TTS §2.2] |
| OpenAI legacy fixture | blocked for production | — | blocked | not admitted | — | Legacy snapshots shut down 6 Jan 2027; replacement `gpt-realtime-2.1-mini` needs a new tested adapter [05-TTS §2.4] |
| Sarvam Bulbul v3 / v4-flash | listed [11-S15] | code-mixed text supported [11-S15] | listed [11-S15] | **not listed** [11-S15, contested]; marketing/API discrepancy blocks commitment [07/04 §18] | 11 languages incl. bn, ta, te, od [11-S1][11-S15] | No emotion parameter [11-S16, contested]; persona styles incl. "kids" [11-S17]; **no 05 compiler profile: verify** |
| Self-hosted (Chatterbox, Indic Parler, Kokoro …) | verify | verify | Chatterbox multilingual documents Hindi | Indic Parler documents Assamese; **not used** (RD-42) | verify | None run locally; F5 weights non-commercial, Fish research licence [05-TTS §4] |
| Human performer | depends on performer | native performer | native performer | **only route** | native performer | "Native performer offers the clearest control route" [05-TTS §3] |

*Live-docs check, 16 Oct 2026 (`05_narration_system/ELEVENLABS_SETUP_2026-10-16.md`):* `eleven_v4` is served only by the Text to Dialogue route (≤2,000 characters per request across `inputs[].text`; `model_id` defaults to `eleven_v3`, so it must be sent explicitly); PCM/WAV output needs the Pro plan; `seed` is best-effort only (CE-38 stands); up to three pronunciation-dictionary locators per request; the v4 family lists 90+ languages including hi, as, bn, or, ta, te. The hosted ElevenLabs MCP is registered in Claude Code at `https://api.us.elevenlabs.io/v1/mcp` (user scope) and awaits the founder's OAuth. A live `eleven_v4` dialogue request succeeded on the founder's Free-plan account later that day (request-id 7qe6fO79BCXq0CjsP1Jq, 114 characters, premade English voice): the route and request shape are verified; no voice is admitted. The account's `eleven_multilingual_sts_v2` offers Hindi but not Assamese or Bengali conversion.

**Assamese human-voice rule.** as-IN is Path A by `A_direct_release`: a native adult performer's own voice, no TTS, no STS (RD-42, CE-L5, P7; schema-enforced). A TTS route needs a decision revisiting RD-42 **and** a GL-voice pass. Never substitute Bengali or infer support from script similarity [07/04 §18]. Other Indic locales take the same human route until a TTS passes GL-voice (CE-L5); no decision blocks STS for them.

### 3.6 Pronunciation lexicon registry (family × locale)

Lexicons are versioned files `lex/<family>.<locale>@x.y.z`, plus `lex/core.<locale>` for numerals, units, dates and currency **[Recommendation]**. A lesson lexicon is compiled as `core ∪ family`; the same key with two spoken forms is a compile error. Each entry carries the 05 fields plus the gap fields 05 already specifies [05-NP §9.2]: `key`, `family`, `subject`, `meaning`, `display`, and per locale `spoken`, `caption`, `allowed_variants`, **`register_variants`** (per persona variant; see §5c), `model_overrides`, `editorially_checked`, `acoustic_approved` **per voice@version**, `accepted_audio_sha256`, `reviewer_id`. VOC nodes link through `lexicon_key` (Arch §2.3).

**Ownership, versioning and contracts** (added 15 Oct 2026) **[Recommendation]**. Owner: the native-language editor of the locale; family entries are co-signed by the family's subject reviewer. Major = a spoken form changes; minor = an entry is added; patch = a non-spoken field changes. Changes go through GR. Machine contracts to add: `schemas/lex_entry.schema.json` (lexicon header `lexicon_id`, `version`, `owner`; entries `key`, `family`, `subject`, `meaning`, `display`, `locales{<tag>: spoken, caption, allowed_variants, register_variants, model_overrides, editorially_checked, acoustic_approved{<voice@version>: bool}, accepted_audio_sha256, reviewer_id}`) and `schemas/golden_set.schema.json` (`gs_id`, `version`, `locale`, `family`, `passages[]` with `sha256` and `features[]`, `human_reference_audio_sha256`, `owner`). ~~Until they exist, `lex/` and `gs/` entries are prose only and cannot pass P1-04 instance tests.~~ Both schemas were added on 15 Oct 2026 as `subsystems/schemas/lex_entry.schema.json` and `subsystems/schemas/golden_set.schema.json` (draft-07, `additionalProperties: false`, meta-validated); `lex/` and `gs/` entries now need only their P1-04 fixtures.

| Family | Seed content | Critical distinctions |
|---|---|---|
| stem_fixture | The shipped 40 en-IN entries (all `editorially_checked: true`, `acoustic_approved: false`) [05-NP §9.4] | milli vs mega; molarity vs molality; inverse vs reciprocal sine; minus signs, charges and exponents; 5′ vs 3′; mitosis vs meiosis [05-NP §9.2] |
| quant_social | New: currency, Indian digit grouping (lakh, crore), percentages vs percentage points, fiscal-year labels, debit/credit | Units of account; ranges; negative balances |
| humanities_citation | New: names of people, places and dynasties; dates and eras | Native-script source spellings; ISO 15919 reference once registered (S-13) |
| languages_literature | New: phonics, word meanings, poetic metre | Native reader only; TXT rights |
| vocational | New: tool and process names, safety signal words | Hazard words never abbreviated |

**Rules.** Explicit `{{token}}` identifiers, never raw-symbol search [05-NP §9.1]; a spoken alias is the portable baseline, provider phonemes only after an acoustic test [05-NP §9.3]; ElevenLabs phoneme tags only on `eleven_flash_v2` [11-N6]; Sarvam dictionaries hold 100 words, one per request, matching `language_code` only [11-N60–N62]; captions come from the script, never the respelling; no English phonetic spelling as the final Hindi or Assamese form and no fabricated Assamese pronunciation [05-NP §9.4]; a version bump must match the plan's `lexicon_version`, and only segments using the entry regenerate.

### 3.7 The native-speaker gate (GL-voice) per locale

GL-voice is "a blind native-speaker review of a TTS voice against the human reference, recorded in the ledger" (Arch §8). Protocol **[Recommendation; generalised from 05 study A, 07/04 §17–§18]**:

1. **Preconditions.** A successful live request in the locale [07/04 §18]; provider admission [05-TTS §7]; rights cleared; native-approved locale lexicon.
2. **Golden set** `gs/<locale>-<family>`: the 05 casting corpus (40 term mappings, 12 connected passages) generalised to ≥3 connected passages per activated family. Each covers negation, a decimal, an exponent, a condition, code-switches (Hinglish is its own locale, RD-42), a question, a correction, a joke and a quiet calculation [05-NP §16]; a native adult performer records the human reference.
3. **Blind listening.** Names hidden, order rotated, level normalised, two generations of hard passages, three voices per locale where available, phone speaker and earphones, quiet and moderate noise, 10-minute continuity after short-listing [05-NP §16].
4. **Raters.** A native-language subject teacher (any meaning-changing defect blocks), a native language editor (accent, intelligibility and naturalness without imposing a stereotype) and a production reviewer. Students rate usability only, with guardian consent and no surveillance, and never decide the gate; no weighted scoring "that lets delightful acting compensate for wrong science" [05-NP §16].
5. **Pass** (criteria made measurable 15 Oct 2026). Pass = all of: (a) 0 defects of class M (meaning-changing: wrong term, number, sign, unit, negation or condition; a word substituted or omitted; a stress that changes meaning) flagged by any rater and confirmed by the subject teacher; (b) for each critical term in the golden set, the subject teacher marks "correct" on both generations; (c) the native editor signs "approve" on accent and intelligibility; (d) continuity: in the 10-minute listen, the production reviewer records 0 speaker-identity changes and 0 class-M defects. A disagreement goes to a second native subject teacher, and any confirmed class-M defect fails. No numeric naturalness threshold applies until a pilot sets one [Hypothesis, owner native-language editor, pilot GL-voice-1]. ASR and alignment are triage only: "Zero word error rate and a successful alignment do not prove correct STEM pronunciation" [05-NP §10].
6. **Record and scope.** A ledger row (voice@version, model id, golden-set hash, audio hashes, reviewers, families); the Locale Profile `voices[].gl_voice_passed` changes through GR. Valid only for that voice@version × model × locale × families; a new family needs a supplement run. `lapsed` is set automatically when `provider.model_id`, `provider_voice_ref`, the `gs@version` or a lex major version changes (added 15 Oct 2026).
7. **Conversion targets (STS)** (added 15 Oct 2026). An `A_conversion_target` is admitted in a locale only after `gs/<locale>-<family>` is run through it. The native adult human-reference takes of step 2 are converted by the pinned STS model and rated against the unconverted takes by the step-4 raters under the step-3 conditions. Any meaning-changing defect introduced by conversion fails (step 5). The result is recorded in `golden_set` and `native_review`. It qualifies the STS route only and is never a GL-voice pass.

### 3.8 Voice QA layers

05 layers [05-NP §12] plus v2 rows.

| Layer | Automated | Human | Blocks |
|---|---|---|---|
| Admission | `compile_plan(production=True)` gates (deprecated model, rights, live contract, placeholder id), lexicon version, voice `admitted` and in scope | — | Yes |
| Text | Unresolved tokens, stage tags in spoken text | Meaning, natural teaching | Yes |
| Path A wording | ASR diff of takes and converted output vs the approved script | GA re-approval on change | Yes |
| Persona | Q-PERSONA on the script and the transcript | Reviewer judgement | Report-only, then yes |
| Transcript | Added or omitted words, critical numbers and phrases | Ambiguous pronunciation | Yes for critical mismatches |
| Pronunciation | Lexicon hit-rate | Teacher hears every critical term | Yes |
| Signal | Clipping, DC offset, unexpected silence (protected intervals supplied) | Joins, fatigue | Yes |
| Consistency | Rate, level or speaker-change flags (not implemented in 05 today) | Acceptable variation | Report-only |
| Alignment, interaction, captions | Hashes, monotonic words, "Premature answer"; captions from the approved script with zero mismatches (CE-22) | Anchors, readability | Yes |
| Mastering | −16 LUFS ±1, true peak ≤ −1 dBTP (pass ≤ −0.9), re-measured after mux [05-NP §13] | — | Yes |
| Disclosure | Q-DISC: variant matches path; `ai_voice_disclosure` and `performer_credit` non-empty (RD-45); string matched against the 07/06 §6.4 template after placeholder substitution | DISCLOSURE gate | Yes |
| Final | — | GF/GS full watch; child-development co-sign for AC0; native editor per locale | Yes |

### 3.9 Disclosure variants

Release blocker (RD-45). Path A and Path B wording is fixed and is the 07/06 §6.4 template (aligned 15 Oct 2026; the earlier 11 PB Step 14 wording is retired here); other rows are **[Recommendation]** pending counsel (O-5) and, for AC0, the child-development reviewer. Locale text is drafted by the native editor (Locale Profile `disclosure_text_ref`).

| Variant | Description line | Notes |
|---|---|---|
| Path A (converted) | "Performed by [Teacher]; voice converted with AI tools; reviewed by [Reviewer]." | RD-45; 07/06 §6.4 (enforced by the packaging_profile pattern and Q-DISC.script). Short form (PD-20): this line is neither spoken nor shown in the video; it stays in the description and `ai_voice_disclosure`, with the platform AI-content label set at upload |
| Path A (direct, as-IN) | "Narrated by [Performer]; no AI voice processing; reviewed by [Reviewer]." (the description line and `ai_voice_disclosure` are this single string) | The field may not be empty (RD-45); RD-42; counsel confirms the wording (O-5). Short form (PD-20): neither spoken nor shown in the video; description and `ai_voice_disclosure` only |
| Path B | "AI-generated narration; script by [Teacher/author, or the Professor Diki Simplified team]; reviewed by [Reviewer]." | RD-45; 07/06 §6.4 (enforced by the packaging_profile pattern and Q-DISC.script). Never Path A wording; no teacher cutaway over Path B audio unless the label says the voice is synthetic [11 Step 14]. Short form (PD-20): neither spoken nor shown in the video; description and `ai_voice_disclosure` only |
| Mixed (F16 only) | "Chapters [list]: performed by [Teacher]; voice converted with AI tools. Other chapters: AI-generated narration; script by [author, or the Professor Diki Simplified team]. Reviewed by [Reviewer]." | One line per path, in chapter order |
| AC0, for parents (description) | "For parents and teachers: [Teacher] performed this lesson and the voice was changed with AI tools. Reviewed by [Reviewer] and a child-development reviewer." | Parent-facing; no links or calls to action (AC0) |
| AC0, for children (spoken end card, optional) | "Teacher [Name] told this story. A computer helped with the voice." | Age-appropriate; one sentence; no data request |

For `path_a_direct`, 07/06 §6.4 items 1 and 4 apply unchanged. Items 2 (YouTube altered/synthetic toggle) and 3 (Meta AI label) are recorded `not_applicable_no_ai_voice` unless another realistic synthetic element is present, in which case they are set (RD-45 "where applicable"). Labelling a human voice as AI-altered would be a false disclosure (added 15 Oct 2026).

Platform duties stay as 11 records them: the YouTube altered/synthetic toggle where applicable [11-N40, contested]; C2PA metadata never stripped [11-N45]; Meta and India IT Rules labelling pending counsel (O-5).

### 3.10 Voice change and invalidation

| Change | Class (Arch §3.6) | Automated re-QA | Human gates | Published artefacts |
|---|---|---|---|---|
| New disclosure text or credit | Narration/disclosure | Q-DISC, re-mux sidecar and end card | DISCLOSURE | Stale |
| New model, voice id or settings | Narration | Golden set and GL-voice re-run **before new synthesis**; old audio replayed by hash | VOICE + GF/GS where audio regenerates | Stale, then re-affirmed |
| Lexicon entry change | Locale/narration | Regenerate only the segments that use it; critical-term ASR | VOICE, GF/GS for those artefacts | Stale |
| Persona register change | Pedagogical | Q-PERSONA; scripts regenerate only on request | GA-Δ, GF/GS if scripts regenerate | Stale |
| Golden-set content change | Narration | Re-run for every admitted voice in the locale | Native editor | Unaffected |
| GL-voice lapse or fail | Locale | R1 forces Path A for new requests | Critical-term re-listen of released Path B artefacts | Valid unless a defect is found (cf. Arch §3.2) |
| Consent scope narrowed (language, platform, processor) | Revocation (scoped) | — | Re-voice the affected scope | Blocked within the scope only |
| Consent or licence revoked or expired | Revocation | — | Re-voice, VOICE, GF/GS, DISCLOSURE; for `consent_withdrawn` with `withdraw_published`: delete raw takes and reference audio from the private store, purge the CE-38 stored narration audio of the withdrawn artefacts (hashes stay in the ledger as records), and obtain each named processor's deletion confirmation within `removal_sla_days` | Blocked and withdrawn unless consent says `future_only` |
| Provider shutdown or voice expiry | Production | No new synthesis; retained approved output kept [05-NP §6.3] | Audition and admit a successor through GR, recorded as `superseded_by`; never switch silently | Unaffected while licence allows |

*Retention and deletion (level-1, 15 Oct 2026, CE-114).* Raw takes, reference audio and narration audio are blobs in the content-addressed store (`content/blobs/sha256/<aa>/<hash>`, Architecture §9.5), each with a `retention_class`: Path A raw takes are `raw_take`; performer consent records and consent-scoped reference audio are `consent_bound`; approved narration audio in a released closure is `artefact_permanent` unless the consent row above withdraws it. "Delete" and "purge" in the rows above mean crypto-shredding of the key for that retention class *and* that data subject (Architecture §9.5; lead ruling 15 Oct 2026, CE-123: one performer's or guardian's withdrawal shreds only their data), so the daily cross-region backups honour a withdrawal too. A purged narration file cannot be re-rendered byte-identically; the artefact is withdrawn and re-voiced, never silently re-synthesised.

### 3.11 Accessibility profiles that touch voice and on-screen people (level-3+, 15 Oct 2026, CE-120)

The `a11y/` profiles are data (Architecture §3.1 addendum); none can be frozen before O-24 registers the Rights of Persons with Disabilities Act 2016 and the Ministry of Education guidelines on e-content for children with disabilities (2021) as sources (status: to verify, no quote).

- **`a11y/isl` (Indian Sign Language inset) is Path A only.** The interpreter is an adult human performer recorded with consent like any Path A performer (§3.1, §3.4: use, platforms, processors, term), never a generated or cloned signer. `voice_asset.schema.json` has no sign-language field (consent `languages` holds locale ids), so the interpreter's entry and consent record need a schema change before the first `a11y/isl` request [Recommendation]. The inset sits in its safe-zone token and is never covered by captions or overlays. A request naming `a11y/isl` resolves to Path A whatever the format cell says in §3.2 [Recommendation; adding `a11y_isl` to the R1 force-A reasons is a lead decision under CE-120, see QA_PROFILES §11 item 11]. A qualified ISL reviewer, recorded as a qualification on a `reviewer/` entry, approves the interpretation at GF (Q-A11Y.isl, critical, not waivable). Until such a reviewer is registered, an `a11y/isl` request is refused at S5, as a request with no admitted voice is. O-18's trigger is now "the first `a11y/isl` request or a pilot with a special-education partner". **Resolved 15 Oct 2026 (CE-123, CE-124): `a11y_isl` is an R1 Path A reason code in Architecture §3.4, `epp.schema.json` and `qa_profile.schema.json`; the ISL reviewer role id and the interpreter consent field wait for the P1-11 reviewer schema and the first `a11y/isl` request.**
- **`a11y/cognitive`** narrows the pacing band in §2.5 below the level's band and allows one idea per beat; the Path A performer is directed to that slower band. The amount is a profile token [Hypothesis until piloted]; no wpm figure is set here.
- **`a11y/low_vision`** and **`a11y/dyslexia`** change visual tokens only; they change nothing in this registry.

---

## 4. Negative tests

Each fails closed. "Schema" = rejected by the subsystem schemas (proven by instance checks).

| # | Input | Expected | Enforced by |
|---|---|---|---|
| V1 | Path B voice allowed for `safety/ac0` | Rejected | Schema; R1 |
| V2 | Voice `audition-only` marked `admitted` | Rejected; compile says "Production voice rights not cleared" | Schema; 05 compiler |
| V3 | as-IN TTS or STS voice | Rejected | Schema (RD-42) |
| V4 | Performer with `is_student: true` or `adult: false` | Rejected | Schema |
| V5 | STS source with no named processor | Rejected | Schema; 07/07 |
| V6 | Path A take adds a sentence not in the approved script | Blocked; GA re-approval on a new bundle hash | Wording diff |
| V7 | Performed transcript says "Yes! I heard you say four!" | Q-PERSONA fail | Persona lint |
| V8 | Provider fails; job retries with a different voice | Refused; the job waits | Selection rule 3 |
| V9 | Hinglish request with a voice that passed GL-voice only for hi-IN | Path A forced | R1; RD-42 |
| V10 | Path B artefact with Path A wording | Q-DISC fail | Q-DISC |
| V11 | Empty `ai_voice_disclosure` or `performer_credit` | Release fails | RD-45 |
| V12 | New `model_id` on an admitted voice, golden set not re-run | Synthesis refused | CI XF-1 (draft-07 cannot compare two fields); §3.10 |
| V13 | exam-coach register on l3_5 + jnvst | Resolver refuses | Schema (`excluded_safety_classes`); R11 |
| V14 | Junior script: "Wrong! Tell me your name" | Q-SAFE and Q-PERSONA fail | Safety lint; persona lint |
| V15 | Path A performer signs GF for their own artefact | Refused | Approval service (Arch §3.2) |
| V16 | Bengali voice offered for as-IN | Refused | Schema (native_speaker_of_locale) + CI XF-2; [07/04 §18] |
| V17 | Persona entry with a wpm field | Rejected | Schema |
| V18 | STS target cloned from a performer (`target_origin: performer_clone`) with no `voice_clone` consent | Rejected | Schema (added 15 Oct 2026) |
| V19 | Admitted consented-custom STS target voice without a consent block | Rejected | Schema (added 15 Oct 2026) |
| V20 | AC0 persona variant with `focused` mode | Rejected | Schema (added 15 Oct 2026) |
| V21 | Path B member of a series whose first member used identity A, pinned to a `B_tts` of identity B | Rejected | XF-3 (added 15 Oct 2026) |
| V22 | Request naming `a11y/isl` resolving to Path B, or with a generated signer in the inset (level-3+, 15 Oct 2026) | Refused | Resolver (§3.11); Q-A11Y.isl |
| V23 | `a11y/isl` artefact at GF with no ISL-qualified reviewer approval (level-3+, 15 Oct 2026) | Release fails | Q-A11Y.isl (critical, not waivable); RELEASE-CHECK |

### 4.1 Cross-field checks (CI and Resolver)

Added 15 Oct 2026. draft-07 cannot compare two fields, so these run in CI (P1-04) on every `voice/` entry, and XF-3 and XF-5 also run in the Resolver and RELEASE-CHECK.

| # | Applies to | Check |
|---|---|---|
| XF-1 | `status: admitted` provider voices | `golden_set.tested_model_id` = `provider.model_id`; `golden_set.tested_provider_voice_ref` = `provider.provider_voice_ref`; for `tts_voice` also `gl_voice.tested_model_id` = `provider.model_id` and `allowed.families` ⊆ `gl_voice.families_covered` |
| XF-2 | every `human_performer` and every `performer_clone` | `locale` appears in `rights.consent.languages` |
| XF-3 | every series, per `series_id` and locale | every member's voice pin carries the same `voice_identity.identity_id` (or `performer_ref` for `A_direct_release`), following the `superseded_by` chain |
| XF-4 | every entry | `expiry.expires_on` ≤ `provider.lifecycle.shutdown_date` and ≤ `provider.lifecycle.custom_voice_storage_expiry` when present, and ≤ `rights.consent.term_end` when consent is present |
| XF-5 | every performer/target pair | the target's `provider.model_id` is in the performer's `rights.consent.models_permitted` |

---

## 5. Worked example: one Ohm's-law hook, four personas

Source: the M1 pilot hook "Does twice the voltage always mean twice the current?" (02 Ohm's-law blueprint, 00:00–00:10). Node ids are illustrative (the closure check fails if the M1 graph lacks them). Tags are direction, never spoken. Hindi is a draft for native review.

**(a) super-teacher / core: l9_10, en-IN, `format/detailed` Ch1 (Path A).**
```
[BEAT h1 | slot hook.question_reveal | mode curious | pace l9_10 ordinary | emphasis "always" | nodes CLM-ohm-proportional, CLM-ohm-condition]
"Here's a ten-ohm resistor with two volts across it. Now we make it four volts. Does twice the voltage always mean twice the current?"
[pause think 6 s | task "Predict the current at four volts, and decide whether 'always' is safe." | answer hidden]
[BEAT h2 | slot explain.ladder_step | mode steady | answers_after h1]
"Hold your prediction. We'll test it, and we'll find the one condition that makes the rule work."
```

**(b) super-teacher-junior / junior: l3_5, hi-IN, `format/story_history` (AC0, Path A performer).** Ohm's law is not taught at l3_5; the compiler can select only a SIM permitted at the level (CE-11), here `SIM-more-cells-brighter` ("with the same small bulb, two cells make it glow brighter than one"; `what_is_lost`: proportionality, conditions, a filament is not ohmic).
```
[BEAT s1 | slot story.beat | mode curious (gentle) | pace l3_5 band (calibrate; performer's natural pace) | nodes STY-mini-torch.b1 → SIM-more-cells-brighter]
"यह मिनी है। मिनी की टॉर्च में एक सेल है, और बल्ब हल्का-हल्का जलता है।"
(This is Mini. Mini's torch has one cell, and the bulb glows softly.)
[BEAT s2 | slot story.beat → check (say-aloud) | mode curious | pause think 6 s (RD-11; child-development reviewer may lengthen) | answer hidden]
"नानी के साथ मिनी एक और सेल लगाती है। अब बल्ब का क्या होगा? ज़ोर से बोलो!"
(With Grandma, Mini puts in one more cell. What will the bulb do now? Say it out loud!)
[BEAT s3 | slot story.beat | mode reassuring (warm) | answers_after s2]
"अगर तुमने सोचा कि बल्ब ज़्यादा चमकेगा, तो चलो देखते हैं... देखो! अब बल्ब ज़्यादा चमक रहा है।"
(If you thought the bulb would glow more, let's look... See! Now the bulb is shining brighter.)
```
Grown-up modelled (Grandma); conditional feedback; no "wrong", nothing personal asked.

**(c) lecturer: ug, en-IN, `format/lecture_segment` 16:9 (Path A).**
```
[BEAT L1 | slot chapter.title → explain.definition | mode steady | pace ug band | talking-head insert [CE-N4] | nodes CLM-ohm-statement, CLM-ohm-condition]
"Does twice the voltage always mean twice the current? Stated carefully: for an ohmic conductor held at constant temperature, the current is proportional to the potential difference, and the resistance does not depend on the voltage."
[BEAT L2 | slot check.interpolated | mode curious | pause think 6 s | task "Which assumption fails for a filament lamp as it heats?" | answer hidden]
"Before we derive the microscopic form, which assumption in that statement fails for a filament lamp as it warms up?"
```
The `{{ohm_law}}` lexicon `register_variants` gives the lecturer "V equals I R"; l9_10 keeps "voltage equals current multiplied by resistance".

**(d) exam-coach register on super-teacher / mentor: l11_12 + `overlay/jee`, en-IN, `format/question_analysis` (Path B only after GL-voice; Path A today).**
```
[BEAT E1 | slot hook.question_reveal | mode focused | nodes ASM-ohm-practice-01 (original: true → "Original practice question", no marks) | question stays on screen]
"Original practice question. Twice the voltage, twice the current: true or false? The answer depends on one condition, and the question may not print it."
[BEAT E2 | slot check.predict | mode focused | pause think 6 s | task "Name the condition before you answer." | answer hidden]
"Name that condition first. Then decide."
[BEAT E3 | slot misconception.confront | mode deliberate | answers_after E2 | nodes MIS-ohm-universal, CLM-ohm-condition]
"True only while the resistance stays constant, for example a resistor at constant temperature. If the component heats or is non-ohmic, doubling the voltage does not double the current. Set up the condition, then calculate."
```
No pattern claim ("this always comes"), no countdown, no marks on an original item.

---

## 6. Inconsistencies found (for the lead)

1. **Persona ids.** The five brief ids differ from the nine Arch §6/LP names; the names are kept as variants (Coach, Mentor, Seminar Lead, Colleague, Exam Strategist = `exam-coach`). LP `persona:` fields must use these ids. Educator had no brief persona (`colleague` added). **Resolved 15 Oct 2026 (CE-64):** `LEVEL_PROFILES.md` §3.11, Architecture §6 and `TEMPLATES.md` now use `persona/<id>#<variant>`, and the level, persona, voice and packaging schemas accept the `#variant` suffix.
2. **Dense pacing.** 02 §G2 says about 90–120 wpm; LP and 03 say 105–125 while citing 02 §G2.
3. **Hinglish** is missing from the 05 `VoiceIdentity` locale enum and `compiler.LANGUAGES`. **Recorded 15 Oct 2026:** mapped in `CROSSWALK_cue_names_and_locales.md` §4 (tag `hi-Latn-IN`); the code change is P1 item P1-CW-2.
4. **Assamese Path A.** Arch defines Path A as performance → STS; RD-42 commits no STS for as-IN (resolved as `A_direct_release`).
5. **Revocation.** 11 §7.4 says future content only; Arch §3.6 says withdraw (resolved per consent, default withdraw).
6. **Sarvam** appears in 11-REPORT and 07/04 only, not in 05-TTS or its compiler.
7. `lex/` and `gs/` are new prefixes; the LP `lexicon_ref` (controlled vocabulary) shares a name with the Locale Profile's pronunciation `lexicon_ref`. **Resolved 15 Oct 2026 (CE-63)** for the prefixes (Architecture §3.1 addendum); the shared name `lexicon_ref` is recorded as P1.
