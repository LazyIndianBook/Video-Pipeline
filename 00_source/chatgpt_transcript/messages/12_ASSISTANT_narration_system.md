<!-- source: ChatGPT share 6acf03ec-b480-83ee-a000-3701059934d9 | message ef490fbf-33df-4096-bbce-8080977095a4 | ef490fbf-33df-4096-bbce-8080977095a4 role=assistant content_type=text create_time=1791910794.693964 chars=45047 -->

# ExamLeaf Narration System  
## Research, voice direction, production architecture, and implementation starter

**Build narration as a dedicated production system—not as the last step of video generation.**

The recommended approach is:

> **Approved academic explanation → conversational teaching script → performance direction → context-aware pronunciation → segmented speech generation → independent transcription and listening checks → alignment → animation timing → mastering → final approval.**

For ExamLeaf, I recommend **one consistent lead voice per language**, premium commercial speech generation initially, and **selective human-performed reference passages** for difficult humour, emotional transitions, or particularly important explanations.

Do not make every lesson a two-character conversation. The student’s thinking should provide the interaction; a second synthetic character is usually unnecessary.

### Deliverables created

[**Download the narration implementation, 15 custom Skills, templates, pronunciation library, and tests**](sandbox:/mnt/data/ExamLeaf_Narration_System.zip)

[**Download the editable narration cost model**](sandbox:/mnt/data/ExamLeaf_Narration_Cost_Model.xlsx)

[**Read the Super Teacher Voice Identity Guide**](sandbox:/mnt/data/ExamLeaf_Narration_System/docs/Voice_Identity_Guide.md)

[**Read the Public Narration Skills and Tools Directory**](sandbox:/mnt/data/ExamLeaf_Narration_System/research/Public_Narration_Directory.md)

### What was actually implemented and tested

| Item | Status |
|---|---|
| Structured narration contracts and provider-request compiler | Implemented locally |
| Fifteen dedicated ExamLeaf narration Skills | Written, with evaluation cases; **not agent-evaluated** |
| Forty explicit English STEM pronunciation mappings | Included; **not acoustically approved** |
| Sample-accurate timeline, protected thinking pauses, and animation markers | Implemented and tested |
| Cache invalidation, transcript comparison, signal analysis, and two-pass mastering | Implemented within the starter |
| Local tests | **57 passed** |
| Actual voice demonstrations | **Two speech auditions generated through your connected Runway account**, using 18 workspace credits |
| Local processing of those generated voices | Not completed; the audio assets were not transferred into this runtime |
| Local speech-quality or pronunciation benchmark | **Not performed** |
| Local audio fixtures | Real WAV test files, explicitly labelled **NOT SPEECH** |
| Complete production service | Not yet: authenticated synthesis transport, actual ASR/alignment execution, and authenticated approval remain to be integrated |

The two generated auditions compare textbook-style wording with a more interactive teaching rendition using the same requested voice, model, and speed. **They differ in wording, length, and expressive instructions, so they are demonstrations—not a controlled A/B experiment.**

Research was checked on **13 October 2026**. Pricing, model lifecycle, documented capabilities, original design recommendations, and local test results are distinguished below.

---

# 1. The decisive technology recommendation

## Recommended launch stack

| Layer | Recommended choice | Why |
|---|---|---|
| Script and teaching direction | Custom ExamLeaf Skills through Claude Code/Codex | Your personality, scientific constraints, and teaching progression should remain provider-independent |
| Primary expressive TTS candidate | **Eleven v4** | Strong candidate for directed, expressive narration and a consistent voice identity |
| Main alternative to audition | **Gemini 3.8 Flash TTS** | Explicit separation of spoken text and performance metadata; broad language coverage and attractive published pricing |
| Additional challenger | **Cartesia Sonic 3.6** | Particularly worth testing for conversational Indian English/Hindi and production efficiency |
| Human-performance path | Consented human recording, optionally converted to a licensed target voice | Preserves a deliberately performed rhythm where text prompting is insufficient |
| Independent transcription | A separately evaluated ASR model/provider | Helps detect omissions, additions, wrong numbers, and substituted terms |
| Alignment | ElevenLabs alignment initially; WhisperX/MFA where language resources are suitable | Align accepted speech with the approved transcript |
| Audio processing | FFmpeg + SoundFile + NumPy/SciPy | Reproducible audio assembly, measurement, mastering, and export |
| Playback timing | Sample-index narration timeline passed to existing scene adapters | Animations follow actual speech instead of forcing speech into rigid scenes |
| Release | Academic/native-language listening plus full-video review | Automated checks cannot certify teacher quality or every pronunciation |

**This is a ranked implementation recommendation, not a claim that I have listened to and benchmarked all three commercial models.**

The choice of final voice should follow a controlled audition. A marginally cheaper API is not a saving when it produces substantially more pronunciation repairs or reviewer work.

---

# 2. Current commercial voice technologies

## 2.1 ElevenLabs: first production candidate, with model-specific controls

Eleven v4 is the current expressive candidate. Current documentation also lists Assamese and Hindi coverage in the relevant newer model families. That resolves an important uncertainty from earlier generic language-support discussions, but **documented support is not proof of native-quality pronunciation for your curriculum**. citeturn569163search0turn391053search7turn391053search12

For ExamLeaf:

**Use TTS** for most approved script segments.

**Use speech-to-speech** when a performer can deliver a passage more effectively than a text instruction can.

**Use voice isolation** only when a recording genuinely needs cleanup.

**Use dubbing cautiously** for exploratory localization. Final Hindi or Assamese lessons should retain explicit control over scientific wording, conditions, notation, and timing.

### Important control changes

Do not copy old ElevenLabs settings into a new model blindly. The inspected v4 guidance differs from older models: **SSML and legacy speed/style controls are not interchangeable across the family**. Dictionary phoneme support likewise does not imply universal SSML support. citeturn569163search0turn145960search0

The starter therefore uses an explicit model-specific request recipe rather than a generic payload containing every setting.

**Keep the original teaching direction even when a provider cannot represent it exactly.** The adapter should report that limitation, not silently discard it.

## 2.2 Cartesia Sonic: strong challenger, not automatically the cheapest accepted audio

Cartesia has an official Skills repository covering its raw APIs, SDKs, and optional MCP tooling. Its `cartesia-api` Skill is relevant here; `line-voice-agent` is primarily aimed at interactive voice-agent applications rather than prerecorded lessons. citeturn676449view1

Sonic 3.6 is the current marketed generation, including multilingual/code-switching use cases. However, the request contract I could directly inspect in detail used a documented Sonic 3.5 snapshot. **The bundled recipe is labelled accordingly; I did not rename it “3.6” and imply that it was tested.** citeturn901218search3turn637231view2

Recommended role:

> Audition Sonic against the other shortlisted engines using identical Indian-English and Hindi passages, then compare **accepted output cost**, not advertised latency alone.

Assamese is **not admitted by the Cartesia contract in this starter**. Do not substitute Bengali or assume that a broad multilingual claim covers the intended language.

## 2.3 Gemini TTS: particularly promising for directed multilingual narration

The current Gemini 3.8 TTS interface separates **verbatim spoken text** from turn-level delivery instructions in `speech_metadata.style`. It also supports point-in-time vocal events. This maps well to an ExamLeaf narration format with separate dialogue and directing metadata. citeturn280214search0

Both Gemini 3.8 Flash TTS and Flash-Lite list **Assamese and Hindi**. Native review is still mandatory, particularly for scientific names, numbers, borrowed terminology, and code-switch boundaries. citeturn280214search7

### Two implementation details that matter

**Audio format:** current unary output is a complete WAV file; streaming output commonly uses raw PCM. Do not prepend a second WAV header or concatenate complete WAV containers as though they were raw samples.

**Voice lifecycle:** custom voice identifiers have documented storage and expiry limits. A brand voice needs a renewal/version policy, not just a voice ID stored indefinitely. citeturn280214search0

**Recommended role:** main commercial alternative, especially for multilingual expansion and cost-sensitive bulk production.

## 2.4 OpenAI speech: a migration issue must be handled now

The current official deprecation notice schedules `tts-1`, `tts-1-hd`, and the listed `gpt-4o-mini-tts` snapshots for removal on **6 January 2027**. It names **`gpt-realtime-2.1-mini`** as the recommended replacement. Older guides and public Skills still contain legacy examples. citeturn280214search1

Therefore:

**Do not start a new ExamLeaf catalogue on an old TTS snapshot merely because a Skill still uses it.**

The replacement is a realtime model with a different integration context. Its documentation lists text and audio pricing, but it should not be treated as a proven drop-in prerecorded-narration replacement without an exact-script audition and endpoint test. citeturn391053search0

The supplied OpenAI recipe is consequently an **offline migration fixture**. The code blocks it for new production.

## 2.5 Language support versus voice suitability

| Candidate | English/Indian-English assessment | Hindi/Hinglish | Assamese |
|---|---|---|---|
| Eleven v4 | Audition the actual voice, not just the model | Documented language support; test code-switching | Documented; native audition required |
| Gemini 3.8 TTS | Explicit style/accent direction available; test outcome | Documented | Documented |
| Cartesia Sonic | Worth auditioning for conversational delivery | Worth testing; model-specific controls matter | Not verified/admitted here |
| OpenAI replacement route | Requires new exact-script benchmark | Requires locale-specific testing | Not admitted by this starter |
| Human narration | Depends on the actual performer | Native/competent performer available | Native performer offers the clearest control route |

The documentation supports the language coverage, **not the comparative naturalness ranking**. citeturn391053search12turn280214search7turn901218search3

---

# 3. Open-source and self-hosted options

“Open-source TTS” is not one category. Code, pretrained weights, voice references, and commercial permissions must be checked separately.

| Project | Recommended ExamLeaf role | Important boundary |
|---|---|---|
| **Chatterbox** | First self-hosted expressive English/Hindi challenger | MIT project; select the correct multilingual model rather than assuming every variant has identical language support |
| **Indic Parler TTS** | Important self-hosted Assamese/Hindi audition candidate | Model card explicitly covers Indian languages, including Assamese; native quality still needs testing |
| **Kokoro 82M** | Lightweight preview or cost experiment | Apache-2.0 model; do not assume the exact release covers every requested Indian language |
| **CosyVoice** | Secondary research candidate | Inspected language coverage does not make it an automatic Hindi/Assamese solution |
| **Qwen3-TTS** | Additional expressive/voice-control candidate | Verify the exact release’s language coverage and weight licence |
| **Fish Speech** | Research or separately licensed commercial candidate | Current repository uses a **FISH AUDIO RESEARCH LICENSE**; do not treat the “open source” label as unrestricted commercial permission |
| **F5-TTS** | Useful research and architecture reference | MIT code and **non-commercial pretrained-weight terms** are separate |

Chatterbox, Indic Parler, and Kokoro are the most relevant first self-hosted investigations for this project. Fish and F5 require particular licensing care. citeturn676449view2turn676449view3turn565458view7turn676449view4turn676449view5

CosyVoice and Qwen3-TTS remain useful alternatives, but should not expand the deployment stack without a demonstrated language or quality advantage. citeturn858572view5turn145960view2

### My self-hosting verdict

**Do not self-host first solely to save the TTS API fee.**

Start self-hosting when one of these is demonstrated:

- A tested model provides a better required language or voice.
- Privacy/offline requirements justify it.
- Real usage exceeds the complete hosting, maintenance, and QA cost.
- Vendor independence is valuable enough to fund the engineering.

The supplied package does **not** include pretrained weights or claim that a neural TTS model was run locally.

---

# 4. Public narration Skills and integrations

The downloadable directory covers **28 repositories, APIs, model families, and audio tools**, classified by their actual function.

## Recommended reuse

| Resource | What to reuse | What not to assume |
|---|---|---|
| **ElevenLabs Skills** | `text-to-speech`, `speech-to-text`, `voice-changer`, `voice-isolator`, selective dubbing | A Skill installation does not approve a voice or establish scientific pronunciation |
| **ElevenLabs MCP** | Supervised auditions and asset operations | MCP is not a permission sandbox or durable production queue |
| **Cartesia Skills** | `cartesia-api` | A conversational-agent platform is not necessary for prerecorded lessons |
| **Cartesia MCP** | Optional development/audition interface | Production should still have controlled SDK/API workers |
| **Remotion Skills** | Audio timing, captions, rendering, multimedia guidance | Remotion composes audio; it is not itself a speech model |
| **Manim Voiceover** | Voiceover/bookmark synchronization patterns | Its service adapters do not validate the scientific narration |
| **Anthropic Skill Creator** | Trigger tests, functional evaluations, regression cases | A polished `SKILL.md` is not evidence of effectiveness |
| **OpenAI speech Skill** | Selected CLI and workflow patterns | Its model defaults require lifecycle review |

The official ElevenLabs repository currently provides ten relevant product Skills and documents both Python and JavaScript SDK usage. Its JavaScript guidance distinguishes the current scoped package from an outdated package name. citeturn676449view0

Cartesia explicitly distinguishes its Skills, documentation, SDKs, and optional MCP interface. That separation should remain intact in ExamLeaf’s architecture. citeturn676449view1

### Installation policy

Before enabling a public Skill:

> Confirm origin → inspect scripts and permissions → review licences → pin the selected revision → test in isolation → enable only the needed components.

Do not run unreviewed shell installers, install entire collections indiscriminately, or give a script-writing agent unrestricted synthesis and publishing credentials.

For bulk narration, use **SDK/API workers with explicit budgets and persistent job records**. Use MCP primarily for supervised development and auditions.

---

# 5. The fifteen custom narration Skills

These are authored in the starter pack. Each contains a `SKILL.md`, handoff template, references, and positive/negative evaluation cases.

They are **fifteen capabilities—not fifteen mandatory LLM calls for every segment**.

| Skill | Input → output | Essential safeguard |
|---|---|---|
| **1. Super Teacher Scriptwriter** | Approved claims and answer key → conversational lesson | Preserve conditions and prerequisites |
| **2. Human Dialogue Naturalizer** | Draft → minimal spoken-language revision | Do not remove qualifiers, negations, or exact quantities |
| **3. Educational Storytelling** | Concept → story/analogy card | Specify the mapping and where it breaks |
| **4. Humour & Meme Director** | Teaching beat → optional relevant humour | Zero jokes is acceptable; never ridicule students |
| **5. Student Psychology Director** | Lesson sequence → confidence/scaffolding audit | Confidence must follow evidence of competence |
| **6. Interactive Teaching Director** | Objectives → predictions, attempts, pauses, feedback | Hide answers and allow adequate response time |
| **7. Voice Acting Director** | Approved text → delivery metadata | One dominant intention per segment |
| **8. Narration Pacing Controller** | Complexity and audio timing → pace/hold plan | Never rush a formula to fit an arbitrary slot |
| **9. STEM Pronunciation Specialist** | Terms and expressions → contextual speech forms | No blanket symbol replacement |
| **10. Multilingual Language Director** | Approved meaning → locale-specific narration | Preserve science and examination terminology |
| **11. TTS Provider Adapter** | Canonical narration → model-specific request | Reject unsupported controls and deprecated models |
| **12. Speech-to-Animation Synchronizer** | Accepted audio/alignment → sample/frame events | Timing comes from the actual accepted take |
| **13. Audio Production Engineer** | Raw audio → measured master | Preserve intentional silence and intelligible consonants |
| **14. Narration Quality Reviewer** | Script, audio evidence, visuals → defect report | ASR or alignment alone cannot approve pronunciation |
| **15. Cost & Regeneration Optimizer** | Changes, jobs, cache → smallest repair plan | Do not regenerate unrelated approved segments |

### How they integrate with the existing engine

The package includes a mapping to the earlier ExamLeaf Skills so you do not create competing owners for the same task.

For example:

**Existing Super Teacher workflow** delegates naturalization and delivery preparation to these Skills.

**Existing scientific reviewer** remains the authority for the explanation and answer key.

**Existing renderer** receives measured narration events.

**Existing release workflow** requires audio-specific approval evidence rather than trusting the narration agent’s own conclusion.

---

# 6. ExamLeaf’s voice identity

## The defining brief

> **A highly competent teacher who is warm toward the learner, precise about the science, and occasionally amused by the problem.**

The voice should sound interested—not constantly excited.

### Recommended personality rules

**Intelligence appears through explanation.**

> “The equation is useful here because we know these two quantities.”

**Warmth appears through repair.**

> “Your relationship is correct. Recheck the substitution rather than restarting.”

**Humour appears through a relevant observation.**

> “Changing the substance would be a very efficient way to answer a different question.”

**Confidence appears through a check.**

> “The counts match on both sides. That is the evidence supporting your answer.”

Do not manufacture intelligence by using difficult vocabulary, warmth through fake intimacy, or humanity through random “ums,” breaths, and laughter.

## Emotional delivery by teaching situation

The following are proposed performance directions, not universal psychological prescriptions.

| Situation | Delivery | Example |
|---|---|---|
| Introducing a mystery | Curious, modest anticipation | “These graphs look similar. Which difference changes the answer?” |
| Difficult explanation | Steady, unhurried, reassuring | “There are two counts here. Let’s keep them separate.” |
| Revealing the answer | Brief satisfaction, then explanation | “Four. Here is why.” |
| Formula or condition | Deliberate emphasis | “This conclusion holds **when the temperature stays constant**.” |
| Joke | Slightly amused, no forced laugh | “A shortcut to the wrong question.” |
| Student question | Inviting, then genuinely quiet | “Choose a direction before we reveal it.” |
| Correcting an error | Specific and matter-of-fact | “You counted atoms correctly; now account for the pair in each molecule.” |
| Recognizing progress | Conditional, evidence-based | “If you selected that relationship without the example, you completed the key step.” |
| Examination strategy | Focused, credible | “Write the relationship before substituting, then include the unit.” |

Research does not establish that maximum enthusiasm is optimal. A 2024 multimedia study found context-dependent effects of vocal enthusiasm and visual cues rather than a simple additive benefit from intensifying both. citeturn719963search0

---

# 7. Pacing and teenage-appropriate interaction

## 7.1 Starting voice targets

| Passage | Pilot target |
|---|---|
| Ordinary English explanation | **130–155 active words/minute** |
| Familiar recap | Approximately **145–165**, when clearly understandable |
| New symbolic relationship | Often **105–125**, plus inspection time |
| Brief conversational beat | Approximately **0.2–0.6 seconds** |
| Important contrast | Approximately **0.8–1.5 seconds** |
| Completed formula/diagram inspection | Approximately **2–4 seconds**, adjusted for complexity |
| Simple prediction | Approximately **4–8 seconds**, answer hidden |
| Writing, drawing, multistep calculation | Learner-controlled pause |

These are **ExamLeaf starting specifications to test**. They should not be represented as neuroscientifically optimal rates.

Also distinguish **active speaking rate** from total lesson rate. A ten-minute lesson containing silence and practice instructions should not be scripted as ten uninterrupted minutes of speech.

## 7.2 Dora-inspired structure without childish delivery

Use:

> **Specific question → opportunity to attempt → explanation → targeted repair → fresh attempt.**

Avoid predictable questions after every sentence.

A suitable initial pattern is **three or four brief checks and two or three substantial attempts** in a ten-minute lesson. Place them at meaningful reasoning boundaries, not at a fixed attention-reset timer.

Retrieval practice has strong classroom support, but that evidence does not establish a universal question interval. citeturn719963search1

### Improve the user’s sample phrases

| Original approach | Stronger ExamLeaf version |
|---|---|
| “Got it? Beautiful.” | “Check it with the next example.” |
| “You just solved the first part!” | “If your result matches, check that you used this relationship.” |
| “What happens next?” | “At the same voltage, what happens to current when resistance doubles?” |
| “Pause and write the formula.” | “Pause, write the formula and the condition under which we are using it.” |
| “Now let’s make it interesting.” | “Now the diagram changes, but the underlying relationship is the same.” |

A prerecorded voice cannot know what an unseen student answered. **Never pretend it heard them.**

---

# 8. Script example: textbook reading versus teaching

The scientific target is the distinction between a coefficient and a subscript in a chemical equation. Changing coefficients adjusts quantities; changing the specified formula changes the chemical representation. citeturn676449view5

*The citation above concerns the tool project rather than chemistry and should not be used to establish the chemistry claim; the complete example’s scientific source is recorded in the downloadable script.*

## Textbook version

> “A balanced chemical equation contains equal numbers of atoms of each element on the reactant and product sides. Balancing is performed by changing coefficients, not the subscripts in the specified chemical formulas. Two water molecules contain four hydrogen atoms and two oxygen atoms.”

This is clear factual narration. It is not necessarily badly voiced. Its weakness is that it provides little help in constructing or testing the learner’s understanding.

## ExamLeaf version

**CURIOUS**

> “Two water molecules. How many hydrogen atoms altogether? Count each complete molecule before you answer.”

*Show two intact water molecules. Keep totals hidden. Insert six seconds of actual silence after the question audio ends.*

**DELIBERATE**

> “Four hydrogen atoms. Each water molecule contains two, and we have two complete copies. That is what the coefficient changes: how many molecules—not what a molecule is.”

*Reveal the hydrogen count when it is spoken. Highlight the coefficient when it is named.*

**LIGHT**

> “Changing water into hydrogen peroxide would be a very efficient way to answer a different question.”

*Show the rejected change separately and clearly label it.*

**FOCUSED**

> “Keep the given formulas fixed. Use coefficients to change the counts.”

**REASSURING**

> “Your turn again: three water molecules. How many hydrogen atoms, and how many oxygen atoms? Pause here and write both counts.”

*Allow a learner-controlled pause. Do not treat the short media hold as a deadline.*

**FOCUSED**

> “Six hydrogen atoms and three oxygen atoms. If those match, check the method too: the number of copies multiplies every atom count in the formula.”

[**Read the full before-and-after example and directions**](sandbox:/mnt/data/ExamLeaf_Narration_System/examples/Before_After.md)

### Why this version is more useful

The proposed script separates counts, creates a genuine attempt, explains the error, and checks a new case. The humour reinforces the identity-versus-quantity distinction.

Its value should be measured through the next independent question—not simply whether students preferred the voice.

---

# 9. Structured narration format

Keep directing instructions out of canonical spoken text. The provider adapter decides what can safely become a model-specific control.

The included plan contains a voice identity, version, locale, rights record, source-claim manifest, lexicon version, and an ordered set of segments.

### One segment from the implemented schema

```yaml
segment_id: question
objective_id: count_atoms
claim_ids:
  - water-composition

text_template: >
  Two water molecules. How many hydrogen atoms altogether?
  Count each complete molecule before you answer.

direction:
  mode: curious
  target_wpm: 140
  emphasis:
    - each complete molecule

pause_after:
  kind: think
  seconds: 6
  prompt: Count hydrogen atoms in two separate water molecules.

expected_visuals:
  - Two water molecules; label elements, not totals.

critical_phrases:
  - Two water molecules
  - hydrogen

cues:
  - cue_id: show_molecules
    phrase: Two water molecules
    action: show
    element_id: molecule-pair
```

The answer segment declares `answers_after: question`. Its answer-reveal events cannot precede the protected response window.

## Provider translation strategy

**ElevenLabs:** map supported delivery cues into the selected model’s actual controls. Preserve unsupported detailed direction for the reviewer.

**Cartesia:** use its actual versioned request fields. A speed multiplier is a heuristic, not an exact words-per-minute guarantee.

**Gemini:** pass exact dialogue separately from `speech_metadata.style`.

**OpenAI:** keep the deprecated request only for migration inspection; implement and test the replacement separately.

**Human performance:** export the same segment text and direction as a recording sheet.

This separation allows a voice provider to change without rewriting the lesson’s educational structure.

---

# 10. STEM pronunciation system

## 10.1 Do not send raw formulas and hope

Maintain at least four representations:

**Scientific meaning → displayed notation → intended spoken form → accepted audio realization.**

Example:

| Display | Context-dependent spoken form |
|---|---|
| \(I=neAv_d\) | “Current magnitude equals number density times elementary charge times cross-sectional area times drift-speed magnitude.” |
| \(mA\) | “milliamperes” |
| \(MA\) | “megaamperes” |
| \(10^{-3}\) | “ten to the power minus three” |
| \(x^{-2}\) | “x to the power minus two” |
| \(\sin^{-1}x\) | “inverse sine of x,” where that notation is intended |
| \(1/\sin x\) | “one divided by sine x” |
| \(Na^+\) | “sodium ion with a positive charge,” or the shorter approved form |
| \(5'\rightarrow3'\) | “five-prime to three-prime” |
| \(\Delta G\) | “delta G,” with the meaning introduced separately |

These are **contextual authoring examples**, not one universal pronunciation dictionary.

The included library uses explicit identifiers such as `{{water_formula}}` rather than replacing every occurrence of a short symbol in arbitrary text.

## 10.2 What the dictionary must record

Each entry should contain:

**Subject, meaning, display form, locale, spoken form, allowed variants, model-specific phoneme/alias override, reviewer status, and accepted audio reference.**

Critical distinctions include:

- Molarity versus molality.
- Milli versus mega.
- Minus signs, charges, exponents, and reciprocals.
- “Increase” versus “decrease.”
- “Not,” “only,” “provided that,” and other conditions.
- Biological directions and counts.
- Similar-sounding scientific names.

Do not automatically use English phonetic spelling as the final Assamese or Hindi representation.

## 10.3 Pronunciation overrides are model-specific

An IPA string, phoneme dictionary, alias dictionary, and SSML tag are not interchangeable mechanisms. ElevenLabs documents different pronunciation options across models; the adapter must verify what the selected endpoint actually accepts. citeturn145960search0turn145960search10

For ExamLeaf, **an explicit spoken alias is the portable baseline**. Use provider phoneme features only after a successful acoustic test.

---

# 11. Exact synchronization and audio QA

## 11.1 The correct sequence

```text
Accepted narration text
        ↓
Generate coherent sentence groups
        ↓
Save raw audio and provider usage
        ↓
Independent ASR and critical-term review
        ↓
Accept or repair the take
        ↓
Forced alignment to accepted speech
        ↓
Resolve semantic animation markers
        ↓
Insert protected thinking/writing pauses
        ↓
Compose captions and visual events
        ↓
Master, encode, re-measure and review
```

Do not begin by estimating that every sentence needs eight seconds.

## 11.2 ASR and forced alignment answer different questions

**ASR asks:** “What does another system think was spoken?”

**Forced alignment asks:** “Where does the supplied text fit in this audio?”

A forced aligner can attempt to place expected words even when the performance is imperfect. ASR can also normalize a mispronunciation into the intended term.

Therefore:

> **Zero word error rate and a successful alignment do not prove correct STEM pronunciation.**

WhisperX documents language-resource requirements and limitations involving some numbers and symbols. Montreal Forced Aligner likewise relies on appropriate dictionaries and acoustic models. citeturn565458view2turn145960view4

For independent Assamese transcription, Gemini’s current transcription documentation lists Assamese and word-level timestamps. That is a relevant candidate, not an integration tested in this package. citeturn280214search3

## 11.3 Timing should be sample-based

At 48 kHz:

\[
6\text{ seconds}=288{,}000\text{ samples}
\]

The starter inserts those samples explicitly. It does not ask the TTS engine to “pause for exactly six seconds.”

Store animation events against the accepted audio’s sample positions, then convert once to output-frame time. Avoid repeated floating-point rounding or independent sentence-duration estimates.

Repeated phrases need an explicit occurrence index. “Highlight when the word ‘current’ is spoken” is ambiguous when it appears four times.

## 11.4 QA layers

| Layer | Automated checks | Human responsibility |
|---|---|---|
| Text | Missing conditions, unresolved terms, forbidden metadata in dialogue | Scientific meaning and natural teaching |
| Transcript | Added/omitted words, critical numbers and phrases | Ambiguous pronunciation and ASR mistakes |
| Signal | Clipping, DC offset, duration, unexpected silence | Audible distortion, joins, fatigue |
| Voice consistency | Flag unusual rate, level, or speaker changes | Judge acceptable performance variation |
| Alignment | Word order, monotonic timestamps, audio/transcript hashes | Inspect difficult anchors |
| Interaction | Answer hidden until response window ends | Confirm the task is fair and meaningful |
| Captions | Timing and text checks | Readability and accurate meaning |
| Final video | Automated defect report | Listen/watch the whole result |

Pitch tracks or model-generated “naturalness scores” may help triage. They should not automatically reject a voice because of accent or approve a lesson because it scores highly.

## 11.5 Mastering standards

Proposed ExamLeaf starting target:

**48 kHz mono, 24-bit archival WAV; approximately −16 LUFS integrated; true peak no higher than −1 dBTP.**

This is an **internal production target**, not a universal platform requirement. FFmpeg supports two-pass loudness processing, but the final encoded delivery should be measured again. citeturn552538search0

Avoid processing clean synthetic speech as though it were a noisy location recording. Excessive denoising can damage consonants; removing all breaths can sound unnatural.

Keep background music **off during the main explanation initially**. Add music or sound effects only when their contribution survives a comprehension and listening-effort comparison.

---

# 12. Human performance, speech-to-speech, and voice consistency

## 12.1 Best use of a human reference

Commission a performer to record a small **performance reference corpus**:

**A calm explanation, prediction, difficult formula, understated joke, supportive correction, and confident recap.**

This gives directors and reviewers a concrete standard. It does not necessarily need to become a cloned voice.

There are two different uses:

**Performance reference:** demonstrates rhythm and intention.

**Identity reference:** creates or conditions a voice resembling that speaker.

The latter requires specific permission and the provider’s applicable verification process. Consent to record a lesson should not be silently treated as consent to create an indefinitely reusable synthetic identity. ElevenLabs’ professional-cloning workflow, for example, has explicit verification requirements. citeturn391053search12

## 12.2 When speech-to-speech is worthwhile

Use it for passages where the actor’s performance makes a material difference: a dry joke, difficult multilingual transition, careful contrast, or unusually subtle reassurance.

It is less compelling for every ordinary explanatory sentence.

Speech-to-speech can transfer performance into a target voice, but it does not automatically fix wrong science, missing words, or an incorrect pronunciation in the input. The official ElevenLabs Skill describes it as voice transformation—not an academic correction system. citeturn676449view0

## 12.3 Protect consistency without making delivery flat

Version the voice profile, pronunciation dictionary, reference passages, model, settings, and accepted samples.

Keep a “golden set” of difficult passages. Re-run it before model upgrades.

Do not silently replace a voice when a provider fails. A fallback must be an approved voice/model combination, or the job should wait.

A voice identity can be consistent while moving between curiosity, precision, amusement, and reassurance. Consistency is not identical pitch and rhythm on every sentence.

---

# 13. Costs for 1, 100, and 1,000 ten-minute videos

## 13.1 Scope and assumptions

These estimates cover the **narration subsystem**, including script-direction allowance, synthesis, audio QA, editing, and the modeled human work.

They do **not** include full academic research, animation production, platform marketing, or audience streaming. Avoid adding the same review cost twice when combining this workbook with the broader Video Engine budget.

All values are **USD before tax**, using one monthly accounting period.

### Baseline inputs

| Input | Assumption |
|---|---:|
| Finished media length | 10 minutes |
| Active speech | 8.5 minutes |
| Transcript length | 7,800 characters |
| Generation/retry allowance | 20% |
| LLM narration editing/direction | $0.60/video |
| ASR/alignment/automatic QA allowance | $0.08/video |
| Storage/export allowance | $0.05/video |
| Academic audio reviewer | $20/hour |
| Audio editor | $15/hour |
| Performer | $30/recording hour |
| Illustrative GPU cost | $0.80/hour |
| Self-hosted real-time factor | 2 compute seconds per generated audio second |

Personnel rates, processing times, retry rate, and GPU figures are **editable planning assumptions, not quotations or measured TTS benchmarks**.

## 13.2 Provider generation costs

The reference commercial calculation uses **$0.10 per 1,000 characters**, a published v2/v3 rate—not an invented Eleven v4 price. With 20% regeneration:

\[
7{,}800\times1.2/1{,}000\times\$0.10=\$0.936
\]

The published speech-to-speech reference is **$0.12 per generated minute**, before separate performer and review costs. citeturn500117search4

Gemini 3.8 Flash TTS currently lists **$0.50/million input tokens and $9/million audio output tokens**, with scheduled increases to **$1 and $18 from 1 January 2027**. Its pricing specifies 25 audio tokens per second. Under the workbook’s workload, synthesis is approximately **$0.139 now** or **$0.278 at the scheduled rate**, before QA and labour. citeturn500117search0

Cartesia’s plans list **$5/100,000 credits, $49/1.25 million, and $299/8 million**. At 9,360 generated characters per lesson, 100 lessons fit within 1.25 million credits, but 1,000 lessons require 9.36 million—beyond the 8-million allowance. Obtain the actual overage or higher-tier quote rather than extrapolating a false fixed price. citeturn500117search2

## 13.3 Five production methods

| Method | Variable cost/video | Monthly fixed allowance | 1 video | 100 videos | 1,000 videos |
|---|---:|---:|---:|---:|---:|
| **Premium commercial TTS** | **$12.50** | $100 | **$112.50** | **$1,349.93** | **$12,599.33** |
| Primarily self-hosted | $14.75 | $300 | $314.75 | $1,775.20 | $15,052.00 |
| Human recorded | $42.40 | $100 | $142.40 | $4,339.67 | $42,496.67 |
| Human performance + speech-to-speech | $34.87 | $125 | $159.87 | $3,612.07 | $34,995.67 |
| Hybrid: 80% TTS, 20% performed/converted | $17.06 | $150 | $167.06 | $1,855.69 | $17,206.93 |

The table assumes different review/editing workloads for each method. **It does not prove that self-hosting inherently costs more.** At equal labour requirements, it can be cheaper; actual retakes and maintenance decide the result.

### The dominant cost

The premium case allows **25 minutes of academic audio review and ten minutes of editing per video**. At 1,000 videos, that is approximately **583 human hours**.

Reducing generation from roughly one dollar to a few cents matters less than eliminating avoidable pronunciation and synchronization repairs.

An illustrative **$4,000 initial narration-subsystem implementation reserve** is separate. Voice buyouts, broader licences, substantial new localization, and hardware purchases require additional budgeting.

---

# 14. Benchmark the voice before making it the brand

Run three separate studies.

## A. Voice/provider audition

Use identical passages, normalized playback levels, blinded provider names, and rotated order.

Include connected explanations—not only isolated impressive sentences.

The corpus should cover numbers, units, negation, scientific conditions, formula reading, Indian names, code-switching, a question, a correction, and a restrained joke.

Use native teachers and language editors to identify **meaning-changing defects**, and students to rate clarity, listening effort, warmth, dignity, and preference.

## B. Script-style comparison

Hold the science and study opportunity comparable. Compare a straightforward explanation with the Super Teacher version.

The two Runway demonstrations produced here are useful for discussion, but **not** sufficient for a causal conclusion because several variables changed together.

## C. Learning evaluation

Measure an independent question immediately and a fresh question later.

Do not use preference, voice similarity, completion rate, or apparent confidence as the primary learning outcome.

Use short listening panels first to find obvious problems, then a properly designed study for claims about learning effectiveness. A small panel is not enough to establish a modest examination-performance advantage.

---

# 15. Integration roadmap and operating instructions

## Repository structure

```text
ExamLeaf_Narration_System/
├── src/examleaf_narration/
│   ├── contracts.py
│   ├── pronunciation.py
│   ├── compiler.py
│   ├── cache.py
│   ├── timeline.py
│   ├── qa.py
│   └── cli.py
├── skills/                  # 15 custom Skill drafts
├── configs/                 # Voice/provider/lexicon contracts
├── examples/                # Textbook and teacher versions
├── tests/
├── outputs/                 # Reports and NOT-SPEECH fixtures
├── research/
├── docs/
└── ExamLeaf_Narration_Cost_Model.xlsx
```

## Run the local starter

```bash
python -m venv .venv
# Activate the environment for your operating system.

python -m pip install -e '.[test]'

PYTHONPATH=src python scripts/build_examples.py
PYTHONPATH=src pytest -q

PYTHONPATH=src python -m examleaf_narration.cli validate \
  examples/teacher.json

PYTHONPATH=src python -m examleaf_narration.cli compile \
  examples/teacher.json \
  --lexicon configs/pronunciation.json \
  --profile configs/gemini_38.json \
  --out outputs/request_preview.json
```

The compile command creates request JSON and sends **zero network requests**. Provider IDs and environment markers are templates, not credentials.

The release check intentionally blocks the supplied fixtures:

```bash
PYTHONPATH=src python -m examleaf_narration.cli release-check \
  outputs/timeline.json
```

Do not bypass that result with fabricated reviewer identities.

## Practical six-week sequence

| Phase | Build | Completion gate |
|---|---|---|
| **Week 1** | Voice casting, language-specific corpus, rights records | Approved primary voice per required locale |
| **Week 2** | One live provider transport, usage records, limits, recovery | Successful controlled synthesis and failure tests |
| **Week 3** | Independent ASR, actual alignment, critical-term checks | Manually verified timing and pronunciation samples |
| **Week 4** | Integrate with existing renderer; complete four subject pilots | Full academic/native-language/listening approval |
| **Weeks 5–6** | Controlled 20–30-lesson batch, dashboard and queue | Predictable accepted-output cost and defect rate |

The current starter completes portions of the contracts, timing, caching, request compilation, and signal QA. It does not substitute synthetic test timestamps for real alignment or claim that the fifteen Skills have already operated as autonomous agents.

---

## Final recommendation

**Launch with commercially generated narration, a carefully cast and licensed voice, explicit pronunciation control, and selective human performance where it genuinely improves the teaching.**

Keep self-hosted models as measured alternatives, not mandatory infrastructure. Keep the voice provider replaceable, but the approved teaching language, terminology, timing, and academic standards under ExamLeaf’s control.

**The strongest ExamLeaf voice will not be the one that sounds most excited. It will be the one that makes a difficult step understandable, gives the student time to attempt it, and responds with a useful explanation rather than a manufactured celebration.**

---

Here's a quick summary of the conversation:

The conversation focuses on designing a scalable, AI-powered video production system named ExamLeaf for Class 10 and 12 STEM subjects. It discusses selecting a well-integrated technology stack—including HyperFrames, Manim, and FFmpeg—while emphasizing scientific rigor, reusable components, and clear licensing distinctions. The conversation also details a comprehensive approach to narration incorporating effective voice selection, emotional direction, synchronization with animations, and human oversight to enhance student engagement and understanding.

Key recommendations include starting with HyperFrames for composition, using Claude Code/Codex for automation of scripts and production, and prioritizing scientific validation and psychological research to optimize learning and confidence. Additionally, narration technologies such as ElevenLabs and Cartesia Sonic are evaluated, with a structured pipeline ensuring quality, naturalness, and alignment with educational goals.




Tab Context:
- Executed on tabId: seed
- Available tabs:
  • tabId seed: "AI Video System Research" ("https://chatgpt.com/share/6acf03ec-b480-83ee-a000-3701059934d9")
