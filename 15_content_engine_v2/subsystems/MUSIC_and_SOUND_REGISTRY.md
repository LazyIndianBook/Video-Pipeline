# Music and Sound Registry (Content Engine v2 subsystem)

Status: specification, not a build; nothing here has run on real narration. Date: 15 Oct 2026. Owners: audio lead (registry, mix), founder (commissions, licences), child-development reviewer (every AC0 sound).
Machine contract: `schemas/music_entry.schema.json` (draft-07; parse, meta-validation, commercial-term lint and positive/negative instance checks passed 15 Oct 2026; re-run after the 15 Oct 2026 review fixes, including MT16–MT25). Template: `templates/music_entry.template.md`.
Generalises, does not replace: the 11 sonic-branding plan (§6), music step (Step 10) and audio spec (§5); the 12 `examleaf-audio-compose` skill, its SFX catalog and doc 06 (compose, analyse, sync); the 05/07-04 mastering standard; and the music policy in the 12 style tokens.

**Citation keys.** [11-N#], [11-P-S#] = 11 PLAYBOOK evidence; [11-S#] = 11 REPORT evidence; [CE-N#] = 15 sources. Documents by section: [11 §x] playbook, [11-R §x] report, [12-AC] audio-compose SKILL, [12-SFX] its `references/sfx_catalog.md`, [12-06 §x] audio doc, [12-AD-x] section-12 decisions, [ST] `05_style_guides/style_tokens.json`, [05-NP §x], [07/04 §x], [Arch], [LP], [FR]. **[Recommendation]** = design choice; **[Hypothesis]** = starting value a pilot must confirm (owner and pilot named); "verify" = not established in project documents.

---

## 1. Policy core (fixed; a registry entry cannot weaken it)

1. **Muted under teaching.** No music under core explanation, worked examples, derivations, definitions, numericals, think windows, pause-video, inspection holds, equation reading, safety cues or **spoken recaps** ("a spoken recap is teaching") [11 addendum 7; 12-AD-15; 02 §G5; 05-NP §14]. ~~The schema requires all nine teaching roles in every entry's `forbidden_segment_roles`.~~ *(Corrected 15 Oct 2026; the old rule contradicted the teaching SFX in the style palettes, §5.)* Policy 1 governs music (beds, logos, ambiences, song backings): their entries must list all nine teaching roles in `forbidden_segment_roles`. SFX and stings follow §5: storyboard-named only, and never in think, pause-video, equation-reading, inspection or safety-cue windows, which their entries must forbid. Definitions and numericals map to `core_explanation` (§2.2).
2. **Music never masks.** A bed cannot hide voice defects: the voice sits on top, and covering defects would cost intelligibility on phone speakers first [11 §0 item 1, Hypothesis; 11-N31]. Fix the take [11 §7.5].
3. **Evidence status.** Neither 11 pass found verified evidence on music under narration and STEM learning [11 §0 item 2]; the 02 blueprint carries the seductive-details meta-analysis (g = −0.16) behind the music-off default [11 lead's note]. Background music reduced perceived value by 7.7% in one retail case [11-N39]. A **short, owned** signature has branding support (audio assets 3.44× visual effectiveness [11-N35, contested]; about 5% perceived-value lift [11-N36]; one campaign +38% recall [11-N38]); a continuous bed does not. None of this is learning evidence.
4. **Owned audio only.** Either commissioned from a contracted composer (sonic logo, lesson beds) or code-composed in house (Reel hook/CTA beds, SFX and stings, prototypes) [12-AD-15 addendum]. Never platform-library songs: the Zee v. Nykaa suit sought about Rs 2 crore over 12 Reels [11-P-S29][11-P-S30], and library availability does not confer brand rights [11-P-S34]. No third-party samples or SoundFonts in v1 (`contains_samples: false` is a schema constant).
5. **Honest provenance.** Code-composed audio is never described as human-composed [11 addendum 7]; the schema ties `composed_by_human` to `origin`.
6. **One loudness standard.** −16 LUFS ±1 integrated, true peak ≤ −1 dBTP (pass at ≤ −0.9), 48 kHz, re-measured on the final mux [05-NP §13; 12-AD-04]. −14 LUFS for Reels exists only as an A/B arm [12-AD-04].
7. **Deterministic and hash-bound.** Code-composed audio is seeded and byte-identical on re-render [12-AC]; every file is hashed, and every entry is a pin in the artefact closure (CE-38): entries are EPP pins (inside `epp_hash`), and placed stems and files are in `cue_sheet_sha256` (Architecture §3.7 closure manifest M; named 15 Oct 2026).

## 2. Registry shape

- **New registry kind `music/`** **[Recommendation]**. Arch §3.1 has no music registry; it lists the sonic logo under `style/`. Here a style entry carries `sonic_logo_ref: music/<id>@x.y.z`, so a logo change is a style-level presentational change. The kind needs a CE decision row.
- **Kinds:** `sonic_logo`, `sting`, `bed`, `sfx`, `ambience`, `song_backing` (the owned music under an AC0 `story.song_chant`).
- **Ids** **[Recommendation]:** `music/diki-end-motif`, `music/logo-core-full`, `music/logo-core-short`, `music/logo-core-extended`, `music/logo-junior`, `music/logo-lecture`, `music/sting-correct-answer`, `music/sting-transition`, `music/bed-intro-loop-30s`, `music/bed-intro-loop-60s`, `music/bed-junior-gentle-loop-30s`, `music/bed-reel-hook-<style>-<mood>`, `music/sfx-<generator-name>`.
- **Graph link.** `STY.song_chant.music_source = original_in_house` must point to an admitted `song_backing` entry. The lesson-graph enum values `licensed` and `public_domain` are **not admissible in v1** (§12 item 6).
- **Closure link.** Cue-sheet `sfx[].file` and bed stems must hash-match an admitted entry's `files[]` (commissioned audio, SFX one-shots), or a byte-identical re-render of an admitted code-composed bed configuration recorded in `bed_meta.json` (§5.1 admission unit; M5) [12-06 §5.6 check 5]. The cue sheet places sounds; the registry admits them.

**Schema-enforced rules** (revised 15 Oct 2026): every teaching role is forbidden for beds, logos, ambiences and song backings; the five protected roles (think_window, pause_video, equation_reading, inspection, safety_cue) are forbidden for SFX and stings, which must allow `cue_sfx`; no entry may allow a teaching role; sonic logos are commissioned and carry a `motif_ref`; the core and lecture variants are AC1/AC2 only, and a junior logo is AC0 only; code-composed beds and ambiences are limited to `reel_hook`, `reel_cta` and `prototype`; a song backing is allowed only at `song_chant` (or `prototype`); prototype-only entries are not release-eligible; an admitted code-composed entry has `determinism_verified: true`; a commission grants worldwide, all-platform and promotional use, with the signed agreement hashed (`contract_sha256`) and an originality warranty; SFX and stings need a cue gain and `storyboard_named_only`; an entry that allows `safety/ac0` must have `startle_class: none`, a child-development sign-off, no `reel_hook` or `reel_cta` role, and, for beds, ambiences, song backings and logos, `rise_between_phrases_allowed: false` and an end-card swell ≤ 3 dB stated explicitly; AC0 beds and ambiences sit at least 20 dB under speech (`under_speech_db.min` ≥ 20); `dramatic` sounds need justification and are never AC0-safe; `admitted` needs a human listen marked `ok` on a phone speaker; every file is 48 kHz.

### 2.1 Resolution in the EPP **[Recommendation]**

Music entries are selected when the EPP is resolved (S5); their placement is resolved at S10, after the narration timeline exists. Both are in the closure, selection through `epp_hash` and placement through `cue_sheet_sha256` (Architecture §3.7 closure manifest M) *(corrected 15 Oct 2026; the earlier text resolved music after the EPP and pinned it into the EPP, which would have changed `epp_hash` after GA-Δ and H-SB)*:

1. **Logo** *(rewritten 15 Oct 2026 so that resolution is a function)*. The style entry names the motif family. The first matching rule sets variants and positions. **L1** `safety/ac0` → `logo-junior` at the close of every format that has one, and at the open of F1 and single-file F16. **L2** lecture register = format ∈ {F20, F26}, or level ∈ {ug, pg, adult_prof, educator} and format ∉ {F5, F11} → `logo-lecture` at open and close in F1, F16, F20 and F26, at the close only elsewhere. **L3** F5, F11 → `logo-core-short` at the end. **L4** F1 and single-file F16 → `logo-core-full` at the close only; no logo at the open (PD-04, 16 Oct 2026). **L5** every other format → `logo-core-full` at the close only. The resolver does not select `logo-core-extended` in v1; adopting it needs a new registry version under GR. Precedence follows ~~R8 (safety > level > overlay > format > style)~~ the corrected R8 (Architecture §3.4 R8 (a)–(c): limits take the most restrictive value across all entries; other scalars follow safety class > a11y profile > level > overlay > format > locale > style > persona) *(corrected 15 Oct 2026)*, so a style can never put the core logo on an AC0 artefact.
2. **Beds.** The format row in §4 gives the allowed roles. The cue-sheet builder asks only for those roles, and `examleaf-audio-compose` refuses any other [12-AC].
3. **SFX.** The style palette (§5) is filtered by the level band. Only admitted `music/sfx-*` entries whose `allowed.safety_classes` include the EPP class can be placed.
4. **Pins** *(corrected 15 Oct 2026)*. ~~The EPP records every `music/<id>@version`. The cue sheet records file hashes. RELEASE-CHECK recomputes both.~~ Selection needs only EPP inputs (safety class, level, format, style), so the Resolver pins every candidate `music/<id>@version: sha256` in EPP `pins` at S5: the logo variants from item 1, the beds admissible for the format row's roles in every mood, and the level-filtered SFX palette (Architecture §3.1 addendum, CE-63). Placement is written at S10 to the cue sheet `sfx[]` and to `bed_meta.json` (music_id@version, seed, bars, stem sha256), which are input hashes of `closure_hash` through the manifest key `cue_sheet_sha256` (Architecture §3.7; `bed_meta.json` is referenced from the cue sheet). Nothing is added to the EPP after S5, so `epp_hash` and the GA-Δ and H-SB approvals that bind it do not change. RELEASE-CHECK fails if a placed entry is not an EPP pin, or if a placed file matches neither its entry nor its re-render (§5.1).
5. **No candidate** for a required logo is a compile error. No candidate for an optional bed means silence, recorded as `bed: none (policy)` [12-AC]; silence is a correct output.

### 2.2 Window roles **[Recommendation]** (added 15 Oct 2026)

The cue-sheet builder derives a `music_role` for every interval of the narration timeline from the Script Spec beats (each interval belongs to one beat, including its `pause_after`) and writes `meta.music_roles[{from_s, to_s, beat_id, slot, music_role}]` to the cue sheet; nothing else sets it. Slot → role: `hook.*` → hook (F5, F11: reel_hook; first spoken line of F1/F16: cold_open); `chapter.title`, `bridge.return_link` → chapter_transition; `close.next_step` → outro (F5, F11: reel_cta); end card after narration → end_card (F5, F11: reel_end); `story.beat` with no spoken sentence → story_interlude; any other beat with no spoken sentence that the approved storyboard marks wordless → wordless_visual; `story.song_chant` → song_chant; `activity.safety_cue` → safety_cue; `recap.*` → spoken_recap; `worked.*` → worked_example; `explain.derivation_step` → derivation; every other slot, including `explain.definition` and numerical steps → core_explanation (default deny). Overlays win over the slot role: `pause_after.kind` think → think_window, pause-video → pause_video; equation `hold` cues → equation_reading; a `beat` pause after a completed transformation → inspection.

M1 and M2 (§9) read only these derived roles; a cue's self-declared role is never trusted.

## 3. Sonic logo variants

**Commission brief** [11 §6.2, Recommendation]: warm, curious and precise, like the Super Teacher; not hype or EDM; a "lightbulb" resolution from question to answer in 2–4 notes; mid-range melodic instruments that survive phone speakers, no sub-bass hits [11-N31]; an optional, non-stereotyped Northeast or Assamese timbral nod, tested with students [Hypothesis, owner audio lead, pilot T3]. Deliverables: 48 kHz/24-bit WAV, stems, loudness-matched versions, and a written full buyout or exclusive licence [11 §6.2]. Placement: under the hook, never before it ("Do not make viewers wait through a logo before the hook" [11-R §4]; "No long logo introduction" in the 02 Ohm's-law blueprint).

| Entry | Length | Where | Safety classes | Dynamics and character |
|---|---|---|---|---|
| `logo-core-full` | 0.6–0.75 s: the end motif `music/diki-end-motif` (PD-04, PD-11; was 1.5–3 s [11 §6.2]) | Outro and end card of long formats | ac1, ac2 | The full motif; may swell on the end card (≤ 3 dB, [ST]) |
| `logo-core-short` | Shorter cut of the motif | Reel end only (no lesson cold open, PD-04) | ac1, ac2 | Same motif |
| `logo-core-extended` | 4–6 s | Commissioned; not selected in v1 (candidate for F1/F16 intros) | ac1, ac2 | Never in Shorts |
| `logo-junior` | Short | AC0 close; also the open of F1 and single-file F16 (§2.1 L1) | ac0 only | Child-appropriate variant (Arch §10): same motif; softer attack, narrower dynamic range, no percussion hits, no sub-bass, gentle release, no stinger ending [Hypothesis, owner child-development reviewer, pilot AC0-audio-1] |
| `logo-lecture` | Shortest | F20 Lecture Segment, F26 Teacher Explainer, ug/pg/adult_prof long formats: open and close only | ac1, ac2 | Understated; never under speech |
| `sting-correct-answer` | Micro | After an answer reveal, never inside a think window; Reel body [11 §6.3] | ac1, ac2; a gentle chime version for ac0 | From the motif |
| `sting-transition` | Micro | Chapter transitions, F16 bridges | all (ac0 gentle version) | From the motif |
| `bed-intro-loop-30s` / `-60s` | 30 / 60 s loop | Cold open, outros and 2–4 s chapter-transition swells cut at bar lines [11 §6.2, §6.3] | ac1, ac2 | Commissioned; loopable at bar lines |
| `bed-junior-gentle-loop-30s` | 30 s loop (variant `loop_30s`) | AC0 chapter transitions, wordless visuals and wordless story interludes (§4 F1, F14) | ac0 only | Commissioned; gentle AC0 dynamics (§4); ≥ 20 dB under any overlapping speech, no rise between phrases [Hypothesis, owner child-development reviewer, pilot AC0-audio-1] |

**Usage map** (from [11 §6.3], updated for the 15 Oct addenda and the AC0 and lecture variants):

| Moment | Logo | Bed | Stings | Ambience |
|---|---|---|---|---|
| Lesson cold open (0–5 s) | None for the core motif (PD-04; junior for AC0, lecture logo in the lecture register) | Under the first line, ducked (AC1/AC2 only) | — | — |
| Teaching beats (definitions, derivations, numericals, spoken recap) | — | **Muted** | — | Optional very low room or lab tone [11-N34] |
| Key reveal or "aha" | — | — | At most one, after a silence drop [11-N30][11-N33] | Dropped just before the reveal [11-N30] |
| Chapter transitions | — | 2–4 s swell | Transition sting | — |
| Outro / end card | Full logo | Bed (AC1/AC2) | — | — |
| Reel hook / body / end | Test arm only / — / short logo | Under the hook / muted / — | — / correct-answer sting allowed / — | — |

**Commission procedure** **[Recommendation]:** (1) the audio lead issues the §3 brief, covering every variant of the motif family, including junior and lecture, plus the beds `bed-intro-loop-30s/-60s` and `bed-junior-gentle-loop-30s`; (2) collect three quotes [11 §6.4]; amounts go to the cost ledger, never into the registry; (3) sign a written assignment, full buyout or exclusive perpetual licence covering all platforms and promotional use [11 §6.4], with counsel review (O-7); (4) check the deliverables: 48 kHz/24-bit WAV, stems, loudness-matched versions [11 §6.2]; (5) hash the files and register each variant as its own `music/` entry; (6) a phone-speaker human listen, plus the child-development reviewer for `logo-junior`; (7) admit through GR; (8) run the T3 logo test (§6.1) before the logo becomes a default.

## 4. Beds per format and level

Allowed bed roles: cold open (first line, ducked), hook, chapter transition (a 2–4 s swell [11 §6.3]), outro/end card, Reel hook and CTA, wordless visual, AC0 story interlude, `song_chant`. Everything else is muted [Recommendation, applying 11 §6.3 and 12-AD-15].

| Format | AC0 (l1_2, l3_5) | AC1 9:16 (l6_8–l11_12, voc; ug Shorts and Reels) | Lecture register (ug, pg, adult_prof long formats; educator) |
|---|---|---|---|
| F1 Detailed; F16 Chapter One-Shot | `logo-junior` open/close; gentle bed at chapter transitions and wordless visuals only; nothing under narration | bed under the first line (ducked), no logo at the open (PD-04); transition swells; `logo-core-full` + bed at the outro | `logo-lecture` open/close; no beds |
| F20 Lecture Segment (16:9) | — | — | `logo-lecture` only; **no beds, no stings** |
| F3 Recap | `logo-junior` close; the song/sequence recap uses a `song_backing` (the music is the content) | Spoken recap muted; logo at close | `logo-lecture` close |
| F5 Short, F11 Flashcard Reel | No bed under narration; `logo-junior` at end; F11 card silent | Reel hook bed (0–3 s, code-composed allowed); body muted; `logo-core-short` at end; correct-answer sting 0–1 | Shorts as AC1; F11 silent |
| F2 Simplified, F7 Misconception Fix, F8 Concept Intro | No bed under narration; logo at end | Hook bed allowed; body muted | Logo only |
| F4, F6, F9, F10, F13, F15, F17, F18, F19, F21, F22, F24, F25 (teaching and think windows throughout) | Logo close only (where offered) | Logo close only; no beds | Logo only |
| F12 Lab/Demo | No music or SFX during the procedure, the safety cue or the "with a grown-up" cue; logo at close | Real demo sound is diegetic and kept; no music during the procedure or safety cue | As AC1 |
| F14 Story/History | Gentle bed in wordless story interludes; `song_backing` for chants; narrated beats muted | Editorial: transitions only | Transitions only |
| F23 Read-Along | **No music** (phonics clarity); `logo-junior` at close only | No music | — |
| F16 Series bridges | Gentle transition sting | Transition sting or swell | Transition sting |
| F26 Teacher Explainer | — | — | `logo-lecture` only |
| `audio_only` render target | Logo only | Logo only | Logo only |

**Gentler AC0 dynamics** **[Hypothesis, owner child-development reviewer, pilot AC0-audio-1]:** beds sit at least 20 dB under any overlapping speech, with no rise between phrases; long fades and no hard cuts; end-card swell ≤ 3 dB [ST]; no percussion accents; calm tempi on the frame-exact grid (72 or 75 BPM "calm recap" values [12-06 §3.1]); mid-range instruments only.

### 4.1 Ambience, silence and tension craft

- **Silence before a reveal.** Drop the bed or ambience 0.5–1 s before a key reveal [11-N30; the duration is a Recommendation]. Overuse becomes predictable.
- **Texture, not sub-bass.** Phones lose the low end, and everything crowds into the speech band [11-N31]. Emphasis comes from mid-range texture and rhythm.
- **Ration attention-grabbing sounds** to one or two real turning points per lesson [11-N33].
- **Off-screen ambience** can widen the narrow 9:16 frame [11-N34]. It stays very low, never competes with speech, and is never a startle source at AC0.
- **Room tone belongs to the voice chain.** The continuous room tone under the voice, and the room tone inserted into think windows, are owned by the narration and audio-production engineer [11 Step 8–9]. They are not music entries. A think window is never digital silence and never music.
- **Templated sessions** keep batch production consistent [11-N29]. Vary ambience per subject so templates do not breed sameness [11 §3 item 31].

## 5. SFX palettes per style and level

Generator palettes come from [12-SFX §3]. Every style also carries the STEM one-shots `electric_hum`, `bubble` and `snap` [12-SFX §2].

| Style | Generator palette [12-SFX] | Token names in [ST] (naming to be reconciled, §12 item 5) |
|---|---|---|
| `style/paper-collage` (legacy key `paper-collage-vertical`) | paper_swish, whip, tap, pop, boing, tear, thud, chime, rumble | paper_swish, ransom_tap_per_word, pop, boing, paper_tear, thud, sparkle_chime |
| `style/doodle-handdrawn` | pencil, pop, boing, whip, chime, tap | pencil_scratch_per_stroke_group, soft_tick, pop, paper_rustle_cut, light_whoosh, marker_squeak_circle, soft_chime_confirmed_result_only |
| `style/editorial-vox` | whip, tap, thud, pop, chime, pencil | soft_thud_number_land, highlighter_swipe, slide_whoosh, tick_divider |
| `style/kinetic-type` | tap, pop, whip, snap | soft_tick_per_word_entrance, slide_whoosh, label_pop |
| `style/voxel-isometric` | pop, snap, thud, chime, whip | block_place_tick_per_layer, soft_chime_confirmed_result_only |
| `style/whiteboard-science` **[Recommendation]** | tap, pop, chime plus the STEM one-shots (`data_bound` SFX only with science sign-off) | — (no token list yet) |
| `style/exam-sheet` **[Recommendation]** | tap, pop, chime plus the STEM one-shots | — (no token list yet) |
| `style/storybook-junior` **[Recommendation]** | AC0 kids' safe subset only (level filter) | — |
| `style/lecture-slides` **[Recommendation]** | Per the UG/PG lecture row (none in F20) | — |

Style ids follow CE-72 (added 15 Oct 2026). A style entry's `sonic.sfx` must be a subset of its row here, after the level filter.

**Level filters** **[Recommendation]:**

| Level band | Palette | Extra rules |
|---|---|---|
| AC0 (l1_2, l3_5) | **Kids' safe subset:** pop, tap, paper_swish, boing, chime, pencil, bubble | Excluded: rumble, thud (low-frequency impact), whip (urgency), tear (sudden noise burst), snap (sharp click), electric_hum (sounds like a hazard). Cue gains below the style default [Hypothesis, owner child-development reviewer, pilot AC0-audio-1]. One sound per visual beat. Styles: ~~doodle and paper-collage (FR F14)~~ doodle-handdrawn and storybook-junior (VISUAL §4.2; corrected 15 Oct 2026). |
| AC1 9:16 (l6_8–l11_12, voc, ug) | Full style palette | rumble only with a storyboard justification ("history-of-science narrative scenes only" [ST]); stings 1–2 per lesson and 0–1 per Reel [11-N33; 11 §5] |
| UG/PG lecture register | F20: **no SFX**. Other 9:16 formats: editorial-vox or kinetic-type palette without gags (boing, tear) | Lecturer register: fewer interjections (persona registry) |
| voc | Style palette plus diegetic demo sound | Never over a safety cue; never a sound that misstates a hazard |

**Rules for every level.** Subtle by default ("kept subtle"; booms "only for real drama" [12-SFX §4]); muted during think, pause-video, equation reading and inspection [ST `sfx_global`] and never over a safety cue (M14); no laugh effects and no unrelated stings [05-NP §14]; no SFX tags in the voice track, because SFX belong in the edit [11 Step 5]; a sound must never imply wrong science (no spark on a safe low-voltage circuit, no hum suggesting mains AC when the lesson uses a DC cell), and `data_bound` SFX are signed off by science review [12-06 §3.5]; placement only through the cue sheet `sfx[]` [12-SFX §4].

### 5.1 Producing a code-composed bed or SFX (procedure from [12-AC])

1. **Policy check first.** For `explanation`, `worked_example` or `think_pause` roles, write `bed: none (policy)` and stop.
2. **Fix the tempo.** 100 BPM for paper-collage [12-AC]; prefer tempi whose beat is a whole number of frames at 30 fps (72, 75, 90, 100, 120 BPM) so bars fall exactly on frames and samples [12-06 §3.1].
3. **Derive the seed, never randomise it:** `seed = int(sha256(f"{job_id}|{scene_id}|bed|v1").hexdigest()[:8], 16)`. Bump `v1` only for an approved musical revision [12-AC].
4. **Render each mood as its own stem set.** `somber` low-passes at 600 Hz and drops 6 dB; `endcard` ramps −6 → 0 dB over the last two bars (AC0: ≤ 3 dB). Lengths round **up** to whole 4/4 bars [12-AC].
5. **Render SFX** limited to what the cue spec names, from the style palette; an off-palette name is refused [12-AC].
6. **Self-check.** Durations equal the bar maths; stem peaks ≤ −12 dBFS and SFX peaks ≤ −6 dBFS; `contains_samples: false`; a second render matches by SHA-256 [12-AC].
7. **Human listen** at phone volume with narration [12-AC step 7]; for AC0, the child-development reviewer listens too.
8. **Register** the entry (generator path and hash, seed, request hash); hand the stems to the mixer (`examleaf-audio-production-engineer`, S10 programme mix; SKILLS_and_KIT_MAP_v2 §8 row 10; 15 Oct 2026), which owns level, ducking and mastering [12-AC].

   **Admission unit** (added 15 Oct 2026). A code-composed bed entry admits a generator configuration, not per-scene bytes: `generator` pins script_sha256 and generator_version, `musical` pins bpm and mood, and `files[]` holds the reference render that passed the human listen. A per-scene render (seed from step 3, bars from the scene) needs no new entry or version. It is admissible when a re-render from (entry@version, seed, bars) is byte-identical (M5). `bed_meta.json` records music_id@version, seed, bars and every stem sha256.
9. **Repairs.** At most two after a rejection (voicing, then progression or style). Then use an admitted commissioned bed, or omit the bed. Licensed stock is not a v1 fallback (§12 item 3).

**Adding a new SFX** follows [12-SFX §3]: write a generator, add it to the palette and selftest, record the script hash, then register a `music/sfx-<name>` entry with its startle class and allowed safety classes.

## 6. Ducking and loudness per format

| Placement | Level relative to speech | Ducking | Tag and source |
|---|---|---|---|
| Teaching windows (all formats) | **Muted** | — | Policy [11 addendum 7; 12-AD-15] |
| T2 A/B arm only (bed under teaching) | 20–24 dB under | Gain automation | [Hypothesis, owner learning-evaluation owner, pilot T2] [11 §5] |
| Hooks, transitions, outros, Reel hook/CTA (AC1/AC2) | ~~15–20 dB under; **start at 20 dB**, the value both 11 and 12 allow~~ 20–24 dB under (token `audio.music_policy.bed_level_db_under_speech`); start at 20 dB (CE-66) *(corrected 15 Oct 2026)* | Bed may rise to about 12 dB under dialogue between phrases | [Hypothesis, owner audio lead, pilot T2] [12 AD-15 addendum, AD-37 corrected] |
| Any bed overlapping speech (AC0) | ≥ 20 dB under (20–24) | No rise between phrases | [Hypothesis, owner child-development reviewer, pilot AC0-audio-1] |
| Logo | Never under speech; the end motif starts after the last word (PD-04; the AC1/AC2 Detailed cold-open exception is withdrawn) | As hooks | [11 §6.3] |
| SFX and stings | Cue `gain_db` between −60 and 0 (no positive gain); paper swish about −18 dB; taps lower | One per visual beat | [12-06 §5.2]; [12-SFX §4, Recommendation] |

**Ducking method** **[Recommendation, 12-06 §7.3]:** gain automation computed from the narration timeline's clip intervals, not a signal-driven compressor, so the mix is reproducible and hashable. Starting ramps: attack about 10 ms, release about 300 ms; 8–12 dB reduction when voice is present [11 Step 10; 12-06 §7.3; both Hypothesis].

**Loudness per format.** Every format and render target masters to −16 LUFS ±1 / ≤ −1 dBTP, re-measured after the final mux [05-NP §13; 12-AD-04]. `audio_only` delivers M4A at −16 LUFS [FR render targets]. Reels test −14 LUFS against −16 only in a controlled A/B, recording integrated loudness and true peak for every export [12-AD-04]. Platform normalisation is unverified [11 Step 11]. **Mix order:** voice master → music stems with automation → SFX bus → programme sum → normalise the programme → mux → re-measure [12-06 §7.4]. Stems stay separate and are archived at 48 kHz [11 §5]. A 44.1 kHz bed is resampled once on import and hashed; one declared as 48 kHz plays about 8.8% fast [12-06 §7.5]. **Audio-described mix** (added 15 Oct 2026): the description clips from `ad.vtt` count as speech. They are added to the ducking timeline (§6 method), so beds and ambience sit at the under-speech level during each clip plus the release (AC0: ≥ 20 dB under, no rise). M1, M3, M4 and M14 run on `audio_described.m4a` as on the main mix.

### 6.1 Experiments that can change these values

| Test | Arms | Decision rule | Source |
|---|---|---|---|
| T2 music | No music under teaching; low ducked bed under teaching; bed only in intro, transitions and outro | Adopt a bed under teaching **only if** listening effort and 72-hour recall are not worse **and** appreciation improves; otherwise keep music off | [11 §8.1, §8.3] |
| T3 sonic logo | No logo; logo at open and close | Compare unprompted brand recall at 72 hours with [11-N38]'s direction, not its magnitude | [11 §8.2] |
| Reels loudness | −14 vs −16 LUFS | Adopt a Reels target only from the test; lessons stay at −16 | [12-AD-04] |
| AC0 audio | Startle parameters and gentle dynamics | Child-development reviewer signs the parameters; AC0 checks block only after the signature | O-22 (§7; Architecture §12; 15 Oct 2026) |

Sample sizes are directional (roughly 30–50 students per arm sees only large effects [11 §8, Hypothesis]). Participation by minors needs guardian consent and no intrusive surveillance [07/07 §8]. A result changes values only through a new registry version under GR.

## 7. Flash and startle safety by safety class

| Class | Visual rule | Audio startle rule | Pairing |
|---|---|---|---|
| AC0 | Zero-flash (CE-21; AC0 release gated on O-1, O-2) | `startle_class: none` (schema). No booms, rumbles, impacts, thunder, alarms, sirens, screams, explosions, breaking glass, horror stingers or laugh tracks. Kids' safe palette only. Numeric startle parameters (maximum SFX peak relative to dialogue, minimum onset ramp, low-frequency limit) are signed by the child-development reviewer, like the O-2 flash parameters **[Recommendation: O-22 (Architecture §12; 15 Oct 2026), gating AC0 release]**. No engagement audio (added 15 Oct 2026): no jingle or repeated melodic hook outside an admitted `song_backing` whose lyrics are approved claims; no teaser, cliffhanger or rising sound on the end card; no audio paired with a next-video or CTA element; SFX ≤ 1 per visual beat and ≤ 6 per minute [Hypothesis, owner child-development reviewer, pilot AC0-audio-1]; song_chant melody repeats ≤ 3 times per artefact. AC0 entries cannot allow `reel_hook` or `reel_cta` (schema); M15 checks the rest. House sonic logo `logo-junior` only, ≤ 1 at the open and ≤ 1 at the close; never paired with a call to action (15 Oct 2026; matches LEVEL_PROFILES §2 ac0 row; no visual ident) | A sound never stands in for, or accompanies, a flash |
| AC1 | WCAG 2.3.1 floor | `dramatic` sounds only with a storyboard justification and never in exam content (no fear [LP §2]); no fear stings | No flash; house rule G15 replaces flash, and a rumble may carry the drama alone [12-SFX §4] |
| AC2 | WCAG 2.3.1 floor | As AC1 | As AC1 |

## 8. Licensing ledger

Every admitted entry has a `licence` row in the CE-49 ledger. Fields follow the 11 licensing log [11 §6.5], adapted to v2:

| 11 log field | v2 field | Note |
|---|---|---|
| asset_id | `music_id@version` | Immutable once admitted |
| title | `title` | — |
| composer | `commission.composer_ref` (pseudonymous) or `generator` (script hash, seed, request hash) | Personal data stays in the private store |
| licence type | `commission.licence_type` ∈ copyright assignment, full buyout, exclusive perpetual licence | [11 §6.2, §6.4; 11-R §4] |
| territory, term, platforms | same | `territory` is `worldwide` and `platforms` contains `all_current_and_future` (schema, 15 Oct 2026) |
| paid-ads allowed | `promotional_use_allowed` | Renamed: "paid" fails the CE-26 commercial-term lint; must be `true` (schema, 15 Oct 2026) |
| contract file | `commission.contract_ref` (`private://`) | Never in git |
| — (new) | `commission.contract_sha256` | Hash of the signed agreement in the private store, so the document cannot be swapped without changing the entry (15 Oct 2026) |
| — (new) | `commission.originality_warranty` | `true`: the composer warrants no samples or pre-existing third-party material; backs `contains_samples: false` and `composed_by_human: true` (15 Oct 2026) |
| date | `contract_date` | — |
| stems location | `stems_location_ref` | — |
| used in (video IDs) | Computed by the dependency index | Not stored; the index is authoritative (Arch §3.6) |

**Rules.** Commission from an independent composer under a written agreement that covers all platforms and promotional use; get three quotes (amounts never enter the registry; CE-L1) [11 §6.4]. ~~Code-composed audio carries `licence: "examleaf-generated (legal review pending)"` until counsel confirms that it is enough for brand use [12-06 §2] (part of O-7).~~ *(Corrected 15 Oct 2026; the entry schema has no `licence` field.)* The CE-49 licence ledger row named by `licence_ledger_ref` records code-composed audio as `examleaf-generated (legal review pending)` until counsel confirms it for brand use (O-7) [12-06 §2]. Counsel's confirmation is a new ledger row, not a new music version. Refuse "make it sound like <named song or artist>" and offer a style descriptor instead [12-AC]. AC0 songs and chants default to in-house composition (O-7). Public-domain melodies and licensed stock are not admitted in v1.

## 9. Music QA checks

| # | Check | How | Blocks | Catalogue ID (QA §2.10; 15 Oct 2026) |
|---|---|---|---|---|
| M1 | No music in teaching windows | Music-stem and ambience RMS below the floor in every `meta.music_roles` window (§2.2) whose role is not in the allowed_segment_roles of the entry placed there; SFX and stings silent in think_window, pause_video, equation_reading, inspection and safety_cue windows [12-06 §7.6 item 4] *(revised 15 Oct 2026)* | Yes | Q-AUDIO.music_window |
| M2 | Placement matches the entry | Each placement's window role from `meta.music_roles` (never self-declared) is in the entry's allowed_segment_roles (SFX and stings: cue_sfx) and not in its forbidden_segment_roles *(revised 15 Oct 2026)* | Yes | Q-AUDIO.placement |
| M3 | Level under speech | Measured bed-to-dialogue difference within the entry's range | Report-only until T2 | Q-AUDIO.bed_level |
| M4 | Final loudness | −16 LUFS ±1, ≤ −1 dBTP (pass ≤ −0.9) on the final mux | Yes | A9 |
| M5 | Determinism | Re-render a code-composed entry with the same seed; SHA-256 must match [12-AC] | Yes | Q-DET |
| M6 | Rights | Admitted entry, licence ledger row, `contains_samples: false`; release-eligible (Q-RIGHTS) | Yes | Q-RIGHTS / Q-SAFE.audio_source |
| M7 | AC0 startle | Palette membership (blocks); numeric startle parameters (report-only until signed) | Partly | Q-SAFE.startle |
| M8 | Sting budget | ≤ 2 per lesson, ≤ 1 per Reel [11 §5] | Yes | Q-AUDIO.sting_budget |
| M9 | Science consistency | `data_bound` SFX signed by science review; matches the fixture state | Yes | A12b |
| M10 | Sample rate | Every file 48 kHz; resample-on-import record | Yes | Q-AUDIO.sample_rate |
| M11 | Human listen | Bed with narration at phone volume; tags ok, chiptune, too busy, masks speech, wrong mood, startling [12-AC step 7] | Yes | Q-AUDIO.human_listen |
| M12 | Provenance wording | Code-composed never credited as human-composed | Yes | Q-AUDIO.provenance_wording |
| M13 | Voice track clean | No SFX or music tags in TTS text; no music bleed in the voice stem | Yes | Q-AUDIO.voice_stem_clean |
| M14 | Safety cue clean | No bed or SFX overlapping `activity.safety_cue` | Yes | Q-AUDIO.safety_cue_clean |
| M15 | AC0 engagement audio (added 15 Oct 2026) | None of the §7 AC0 engagement-audio patterns present: no jingle or melodic hook outside an admitted `song_backing`; no teaser or rising end-card sound; no audio on a next-video or CTA element; SFX ≤ 1 per visual beat and ≤ 6 per minute; song_chant melody ≤ 3 repeats | Yes | Q-AUDIO.ac0_engagement |

`QA_PROFILES_REGISTRY.md` §2.10 owns the severities of these checks; the Blocks column here is informative (15 Oct 2026).

## 10. Invalidation rules

Music entries are immutable; a change is a new version. The dependency index finds every artefact that pins the old version (Arch §3.6). Stored stems are replayed by hash, so an unchanged mix re-affirms automatically.

| Change | Class | Automated re-QA | Human gates | Published artefacts |
|---|---|---|---|---|
| New logo, bed or SFX version (re-commission, re-render, voicing repair) | Presentational | Re-mix, M1–M15, Q-DET | GF/GS where bytes change | Stale |
| Style `sonic_logo_ref` change | Presentational | As above for every artefact of the style | GF/GS | Stale |
| Licence withdrawn or expired | Revocation | — | Re-mix with an admitted replacement; GF/GS | Blocked and withdrawn |
| AC0 startle or palette parameters tightened | Safety | Full AC0 audio suite | Child-development re-sign; GF | Failing artefacts revoked |
| Any loosening of AC0 audio rules | Safety | As above | G-COUNSEL record if the class rules loosen (Arch §3.6) and child-development sign-off | Failing artefacts revoked |
| Narration regenerated and scene length changed | Presentational | Re-cut the bed to the new bar count with the same seed [12-AC] (a per-scene render of the admitted configuration, §5.1 admission unit; M5); rebuild the cue sheet and `bed_meta.json` | GF/GS | Stale |
| Mix-level or ducking token change | Presentational | Re-mix, M3, M4 | GF/GS where bytes change | Stale |
| Policy change (for example T2 allows a bed under teaching) | Pedagogical + safety | Requires a CE decision; re-QA every affected format | GA-Δ is unaffected; GF/GS | Stale |

## 11. Negative tests

| # | Input | Expected | Enforced by |
|---|---|---|---|
| MT1 | Bed placed under `core_explanation` | Refused; the compose skill writes `bed: none (policy)` | Schema; [12-AC]; M1 |
| MT2 | Code-composed sonic logo | Rejected | Schema |
| MT3 | Code-composed bed in a Detailed chapter transition | Rejected | Schema |
| MT4 | Trending or platform-library song in a Reel | Refused | M6; policy 4 |
| MT5 | `rumble` on an AC0 entry | Rejected | Schema (`startle_class: none`); palette |
| MT6 | Correct-answer sting inside a think window | Refused | Forbidden role; cue-sheet answer protection |
| MT7 | 44.1 kHz file declared 48 kHz | Rejected | Schema (`sample_rate`); M10 |
| MT8 | Two renders of one bed differ in SHA-256 | Blocker | M5 |
| MT9 | Code bed credited "composed by" a person | Rejected | Schema; M12 |
| MT10 | Spark SFX on a safe low-voltage circuit | Blocked at science review | M9 |
| MT11 | "Make it sound like [named film song]" | Refused | [12-AC] |
| MT12 | Lesson mastered at −14 LUFS | Fails | M4; [12-AD-04] |
| MT13 | Prototype-only bed in a released artefact | Fails | Schema (`release_eligible: false`); M6 |
| MT14 | Bed under a lab safety cue | Refused | Schema; M14 |
| MT15 | AC0 bed that rises between phrases | Rejected | Schema |
| MT16 | Entry whose `allowed_segment_roles` includes `core_explanation` | Rejected | Schema |
| MT17 | Code-composed ambience allowed at `chapter_transition` | Rejected | Schema |
| MT18 | `song_backing` allowed at `chapter_transition` | Rejected | Schema |
| MT19 | Admitted code-composed entry with `determinism_verified: false` | Rejected | Schema |
| MT20 | AC0 bed with `rise_between_phrases_allowed` omitted | Rejected | Schema |
| MT21 | AC0 bed with `under_speech_db.min` 10 | Rejected | Schema |
| MT22 | Correct-answer sting after the reveal in a Reel body | Allowed (cue_sfx; not a protected window) | Schema; M2 |
| MT23 | Commissioned logo with `promotional_use_allowed: false` | Rejected | Schema |
| MT24 | AD mix with an unducked bed under a description clip | Fails | Ducking timeline; M3 reported |
| MT25 | AC0 entry with variant `core_full`, or allowing `reel_hook` | Rejected | Schema |

## 12. Inconsistencies found (for the lead)

1. **Bed level.** 11 (addendum 7 and §5) says 15–20 dB in hooks, transitions and outros, with 20–24 dB only for the T2 teaching arm. 12 AD-15/AD-37 and the style tokens say 20–24 dB for every placement. This registry starts at 20 dB, which both allow. **Resolved 15 Oct 2026:** 20–24 dB for every allowed placement (12 AD-15 addendum, AD-37 corrected, CE-66). The 15–20 dB note in 11 cited AD-37 before its correction.
2. **Recaps.** The brief and 12 AD-15 list recaps as a bed placement; 11 mutes spoken recaps. This registry mutes spoken recaps and allows only wordless or sung (AC0) recaps.
3. **Code-composed scope.** 11 addendum 7 allows code beds in intros, outros and transitions; 12 AD-15 (and the brief) limit them to Reel hooks, SFX and prototypes. The schema follows 12.
4. **Logo length.** 11 §6.2 says 1.5–3 s (4–6 s extended); 11-R §4 says 3–5 s.
5. **SFX names.** The [ST] token names differ from the generator names in [12-SFX]; several tokens (marker_squeak_circle, highlighter_swipe, block_place_tick_per_layer and others) have no generator. A mapping is needed before the cue-sheet check can pass.
6. **STY.song_chant** allows `licensed` and `public_domain` music; v1 admits neither. **Recorded 15 Oct 2026:** the `lesson_graph.schema.json` enum keeps both values (reserved pending O-7) with a description that v1 releases admit only `original_in_house`; the music registry gate M6 and Q-RIGHTS reject the others. Narrowing the enum is a P1 build item.
7. **`music/`** is a new registry kind (Arch §3.1 places the sonic logo under `style/`). **Resolved 15 Oct 2026 (CE-63).**
8. **Bit depth.** [12-AC] writes 16-bit working stems; 12-06 and 11 archive at 24-bit. The schema allows both; the archive must be 24-bit.
9. **Stale locale line.** 12-06 §6 still says the launch locale is en-IN only (RD-26), which RD-42 superseded.
10. **Sibling subsystem.** `schemas/style_entry.schema.json` (`sonic.music_sources`) allows `licensed`, and `VISUAL_STYLE_and_ANIMATION_REGISTRY.md` places beds in recaps at 20–24 dB; both should follow this registry (owned only; spoken recaps muted), and `sonic_logo_ref` should take the `music/<id>@x.y.z` pattern. **Resolved 15 Oct 2026 (CE-66):** `sonic.music_sources` is `commissioned | code_composed`, `sonic_logo_ref` takes the `music/<id>@x.y.z` pattern, and the visual-style and packaging documents now state the same policy (owned audio only, spoken recaps muted, beds start 20 dB under, code-composed beds for Reel hooks, SFX and prototypes only, logo core 1.5–3 s).
