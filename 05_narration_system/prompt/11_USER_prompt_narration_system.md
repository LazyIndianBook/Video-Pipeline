<!-- source: ChatGPT share 6acf03ec-b480-83ee-a000-3701059934d9 | message bbcd91bd-45e5-4150-848f-d955054c8ef5 | bbcd91bd-45e5-4150-848f-d955054c8ef5 role=user content_type=text create_time=1791907371.529 chars=8893 -->

# ExamLeaf — Advanced AI Narration, Human Voice Acting & Teaching Skills

Research and develop a **complete AI-powered narration and voice-production system** for ExamLeaf, integrated with Claude Code/Codex and our educational video-generation pipeline.

Our narration must feel like an **exceptionally talented, energetic, funny, warm, and experienced human teacher**—never like an AI reading a textbook.

Students should feel that a brilliant teacher is personally explaining the concept, asking them questions, making them laugh naturally, encouraging them, and helping them confidently solve problems.

### 1. Research Public Narration Skills & Voice Technologies

Discover and evaluate all relevant public Claude Skills, agent plugins, MCP servers, APIs, and open-source tools, especially:

- ElevenLabs Skills (TTS, STT, voice changer, dubbing, audio cleanup).
- Cartesia Skills and Sonic TTS.
- Remotion voiceover and audio synchronization Skills.
- Gemini TTS and its expressive speech controls.
- OpenAI speech-generation technologies.
- Chatterbox, Fish Speech, F5-TTS, CosyVoice, Kokoro, and other relevant open-source alternatives.
- Forced-alignment, audio analysis, pronunciation, mastering, and automated QA tools.

Verify current documentation, actual capabilities, licensing, pricing, Indian English/Hindi/Assamese support, emotional expressiveness, voice consistency, and suitability for bulk production.

### 2. Build Dedicated Custom Claude Narration Skills

Design reusable Skills for:

1. **Super Teacher Scriptwriter** — Convert academic material into simple, conversational, engaging explanations.
2. **Human Dialogue Naturalizer** — Remove robotic phrasing, unnatural transitions, textbook language, and repetitive AI expressions.
3. **Educational Storytelling** — Introduce relatable stories, analogies, real-life situations, and memorable explanations.
4. **Humour & Meme Director** — Add natural jokes, witty observations, appropriate shayari, and culturally relevant humour without interrupting learning.
5. **Student Psychology Director** — Use curiosity, achievable challenges, encouragement, and genuine confidence-building techniques.
6. **Interactive Teaching Director** — Insert questions, student-response pauses, predictions, note-taking instructions, and guided practice.
7. **Voice Acting Director** — Specify emotional delivery, vocal energy, excitement, warmth, emphasis, suspense, comedic timing, and natural pauses.
8. **Narration Pacing Controller** — Adjust speaking speed according to concept complexity, calculations, emotional moments, and student interaction.
9. **STEM Pronunciation Specialist** — Ensure correct spoken formulas, equations, symbols, Greek letters, units, chemicals, scientific terms, and Indian names.
10. **Multilingual Language Director** — Manage natural English, selective Hinglish, Hindi, and Assamese while preserving scientific correctness.
11. **TTS Provider Adapter** — Translate our standardized narration instructions into provider-specific settings, supported expressive tags, and API requests.
12. **Speech-to-Animation Synchronizer** — Align narration with diagrams, equations, scene changes, captions, highlights, and interactive pauses.
13. **Audio Production Engineer** — Handle audio mastering, loudness consistency, clean dialogue, silence, music, and sound effects.
14. **Narration Quality Reviewer** — Detect mispronunciation, missing words, artificial delivery, unsuitable emotion, inconsistent voices, awkward pauses, and script/audio mismatches.
15. **Cost & Regeneration Optimizer** — Cache approved audio, regenerate only affected segments, and minimize paid synthesis costs.

Determine which existing Skills can be reused and which require custom development.

### 3. Create a Consistent ExamLeaf Voice Personality

Develop the **ExamLeaf Super Teacher Voice Identity**:

- Highly intelligent but never intimidating.
- Energetic without shouting.
- Funny without forced comedy.
- Confident without arrogance.
- Friendly without sounding childish.
- Emotionally expressive without artificial enthusiasm.
- Simple enough for students with weak fundamentals.
- Serious and precise when explaining examinations, formulas, and calculations.

Research optimal speaking rates, vocal variation, pauses, pronunciation, conversational rhythm, and listening comfort.

### 4. Emotionally Intelligent Narration

Define voice-delivery rules for different teaching situations:

- **Introducing a mystery:** Curious, playful, slightly suspenseful.
- **Explaining a difficult concept:** Calm, clear, reassuring.
- **Revealing an answer:** Excited, satisfying, confident.
- **Teaching formulas:** Precise, measured, with intentional emphasis.
- **Making jokes:** Naturally playful, with appropriate comedic timing.
- **Asking students questions:** Inviting and genuinely interactive.
- **Correcting mistakes:** Supportive, never humiliating.
- **Celebrating understanding:** Warm and enthusiastic without exaggerated praise.
- **Explaining exam strategies:** Focused, credible, and motivating.

Do not use one emotional tone throughout the entire lesson.

### 5. Advanced Interactive Narration

Research how to incorporate age-appropriate Dora-inspired interactive teaching into Class 10–12 lessons.

Examples:

- "Okay, your turn. What do you think happens next?"
- "Before I reveal the answer, try this yourself."
- "Got it? Beautiful. Now watch what happens when we change this value."
- "Pause here and write down this formula. We'll use it in the next question."
- "See? You just solved the first part. Now let's make it a little more interesting!"

Design intentional pauses, response windows, writing prompts, retrieval questions, and increasingly challenging examples.

Avoid predictable questions every few seconds. Interaction must serve learning rather than becoming repetitive.

### 6. Narration-to-Animation Integration

Create a structured narration format containing:

- Spoken dialogue.
- Emotional direction.
- Voice identity.
- Pacing and emphasis.
- Pronunciation overrides.
- Pauses and interaction cues.
- Expected visual elements.
- Animation synchronization markers.
- Scene transitions.
- Educational objectives.

Keep directing metadata separate from spoken text and convert it into whichever format the selected TTS provider supports.

Use forced alignment and accurate audio timing to synchronize narration, formula highlights, visual reveals, and animations.

Where possible, adjust animation timing to natural narration rather than forcing speech into rigid scene lengths.

### 7. Complete Automated Narration Pipeline

**Academic Content → Human-Like Script → Teaching Psychology Review → Humour & Storytelling → Emotional Voice Direction → Pronunciation Validation → TTS Generation → Speech Alignment → Audio QA → Animation Synchronization → Final Mastering.**

Implement automatic checks for missing words, inaccurate scientific pronunciation, awkward phrasing, inconsistent delivery, clipped audio, excessive silence, unnatural intonation, and incorrect synchronization.

Require human listening tests before approving the main ExamLeaf voice.

### 8. Compare Narration Production Methods

Benchmark:

- Premium commercial TTS.
- Open-source self-hosted TTS.
- Human-recorded narration.
- Human-performed narration enhanced by speech-to-speech AI.
- Hybrid approaches using a human performance reference and consistent licensed synthetic voice.

For each method, evaluate realism, expressiveness, consistency, costs, scalability, language support, and quality-control requirements.

Use only appropriately licensed or consented voices and voice samples.

### Required Deliverables

Provide:

1. Complete public narration Skills directory.
2. Recommended voice-generation technology stack.
3. Custom Claude narration Skills architecture and implementation specifications.
4. ExamLeaf Super Teacher Voice & Personality Guide.
5. Scriptwriting, voice-direction, and emotional-delivery templates.
6. Structured narration data format and TTS integration strategy.
7. Full pronunciation, timing, and audio QA pipeline.
8. Cost comparisons for 1, 100, and 1,000 ten-minute videos.
9. Working example showing the same academic explanation as boring textbook narration versus outstanding human-like teaching, including voice directions and animation cues.
10. An implementation roadmap for integrating the complete narration system into ExamLeaf Video Engine.

**Ultimate Goal:** Produce narration so natural, captivating, understandable, funny, and encouraging that students feel they are learning directly from an exceptional human teacher—not listening to generated speech.

Prioritize **authentic teaching, scientific accuracy, real understanding, memorable explanations, emotional connection, and genuine student confidence** over artificial excitement or unnecessary theatrical delivery.
