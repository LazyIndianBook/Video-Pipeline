# Packaging and Distribution Registry (Content Engine v2 subsystem)

Status: subsystem specification, 15 Oct 2026. Nothing here has run, and no platform figure has been measured. Parent: `../ARCHITECTURE_content_engine_v2.md` §1.2 (P1), §3.6, §4 (S12–S14), §9.1 and §9.3; `../FORMAT_REGISTRY.md` "Render targets and outputs". Schema: `schemas/packaging_profile.schema.json` (the neutral sidecar is `#/definitions/metadata_sidecar`). Template: `templates/packaging_profile.template.md`. Siblings: `VISUAL_STYLE_and_ANIMATION_REGISTRY.md` (safe zones, holds, styles) and `QA_PROFILES_REGISTRY.md` (check IDs; §2.7 packaging checks).

**Tags.** **[Recommendation]**, **[Hypothesis]** and "verify" (not in the verified evidence) as in the Architecture. **Citations.** [N#] = `../SOURCES_and_claims.md`; [11:N#] = `11_human_feel_voice_audio_research/SOURCES_and_claims_pass2.md`. 07/05 = `07_end_to_end_pipeline_instructions/05_SHORTS_and_REELS_PROCEDURE.md`, 07/06 = `.../06_QA_GATES_and_RELEASE.md`, 11 PB = the 11 playbook, and 01 RB = `01_business_model/REEL_BACKLOG_36.md`.

---

## 0. Summary

Packaging turns one approved, hash-bound artefact into the files a channel receives:

- encodes and renditions;
- captions, chapters and transcripts;
- cover, title and description;
- disclosure placements;
- a **neutral metadata sidecar**.

It is commercially agnostic. A package carries ids, competency GUIDs, level, format, locale, versions, hashes, the audience safety class, accessibility tracks, disclosure and provenance, and nothing else (P1, CE-L1). Entitlement, price, playback tokens, destinations and analytics are joined by the platform outside the pipeline.

Packaging can never change what an artefact says. Every title, cover and description sentence passes the same closure rules as the script.

## 1. What a packaging profile is

[Recommendation] Profiles are a new registry kind, `packaging/<id>@<semver>`, validated by `packaging_profile.schema.json`. The Architecture §3.1 table has no such kind yet (§15 item 1). A profile has two halves with different change classes:

- **Render variant (bytes).** Container, codecs, fps, renditions and burned captions. These fields are pinned in the EPP by Resolver rule R14 (Architecture §3.4), because they change bytes that GF/GS must watch. The EPP pins only `packaging/<id>@x.y.z#render`, the SHA-256 of {`render_variant`, `loudness`, `captions.max_lines`, `safe_zone`}; the whole-profile hash is the sidecar's `binding.packaging_profile_sha256` (15 Oct 2026). An end-card disclosure line is part of the master, never of packaging (§7).
- **Distribution (metadata).** Copy rules, sidecar, chapters mode, disclosure placements, audience rules and series display. They are pinned in the **Distribution Package** record `content/packages/PKG-<id>.json`, which is the neutral sidecar (§6) stored under its package id. `export/sidecar.json` is its exported copy and replaces v1 `export/export_record.json`; `package_sha256` is its SHA-256 (CE-32 canon). A change re-exports without reopening the full-watch gate, because the EPP pins only the bytes half (15 Oct 2026).

**Files a package can hold.**

- **The master.** The bit-exact MP4 or M4A from the pinned single-thread bitexact encode (Architecture §9.3), bound to GF/GS by SHA-256.
- **Renditions.** Lower-bitrate or lower-resolution encodes from the master by a pinned encoder. They carry `derived_from_sha256` and pass automated checks A9, A11 and A13. [Recommendation, needs a lead ruling against CE-14] They need no second full watch, because the content is unchanged.
- **Variants.** Burned-caption, reduced-motion and audio-described renders. Each changes what a learner sees or hears, so any variant actually delivered gets its own GF/GS on its own hash. Gates are never sampled (CE-14).

**Profile selection.** [Recommendation, 15 Oct 2026; Resolver rule R14, Architecture §3.4 (R13 is the voice-selection rule)] The profiles an artefact is packaged for are `request.packaging_profiles` if present, else the §2.2 Default profiles for its format group. Each must accept the format and the safety class (for example `instagram-reels` excludes ac0), otherwise it is a compile error. The master is rendered to the bytes half of `packaging/in-app-player`; each other selected profile whose bytes half differs yields a variant, gated as above (subject to the open CE-14 ruling, §15 item 5). An unmeasured profile may be pinned, but A4 and RELEASE-CHECK block its release. M1 exports to `packaging/in-app-player` only, with the master and no variants.

**Order of work.** ~~The neutral exporter writes the package at S14, only after RELEASE-CHECK (07/06 §6) recomputes the closure. The publisher then confirms each platform placement for DISCLOSURE (07/06 §6.4) before upload.~~ **Corrected 15 Oct 2026:** DISCLOSURE is approved at S12, before RELEASE-CHECK, as in Architecture §4.

- **S12.** `examleaf-thumbnail-package` has drafted the title, cover and description, with computed fields filled from the render. The GF/GS reviewers approve the master, each delivered variant, and the copy (a COPY approval on `copy_sha256`, §6). DISCLOSURE (publisher identity) approves the line text for the resolved voice path and locale, a non-empty `ai_voice_disclosure` and `performer_credit`, the end-card or child-variant line, and `placements_required` against each file to be uploaded. Its `bound_sha256` is that delivered file's SHA-256 (§14); the approval record also names the voice pin and the disclosure text's SHA-256, and it reopens when the voice version, locale or wording changes.
- **S13.** RELEASE-CHECK verifies all of these approvals and recomputes the closure.
- **S14.** The neutral exporter writes the package. No approval is added after S13.
- **Publish** (after S14; unnumbered, because v1 07/03 and 07/11 use S15 for cache keys). For each channel the publisher sets the platform flags in the upload flow before the item is public, and writes the publish receipt `content/packages/PKG-<id>.publish.<channel>.json` (schema `#/definitions/publish_receipt`; never inside the sidecar). Q-DISC.placement reads that receipt; at ac0 on YouTube it fails unless `made_for_kids_flag` is `set`. The upload step refuses a channel with no passing Q-DISC.placement record. 07/06 §6.4 "before upload" is read as "before the item is public", because the toggle and AI label exist only in the upload flow (RD-45 says publish). The §12 takedown list is every receipt whose `uploaded_file_sha256` is, or derives from, the revoked hash.

## 2. Render targets per format

### 2.1 Common encode

| Item | Value | Source |
|---|---|---|
| Container | MP4 (video), M4A (audio_only), with `+faststart` for streaming | 12/02 doc 04 §12 |
| Video | H.264, yuv420p, 30 fps constant, at the EPP resolution (1080×1920; 1920×1080 only for F20) | 12/02 doc 04 §12; CE-46 |
| Audio | AAC, 48 kHz; 48 kHz WAV stems archived, never delivered | 11 PB §5 |
| Bitrate | **verify**, per platform and pilot viewing tests; no figure is stored | 12/02 doc 04 §12 |
| Loudness | −16 LUFS integrated ±1, true peak at most −1 dBTP, re-measured after the final mux on every delivered audio-bearing file | 07/06 §2.1; A9 |
| Reels −14 LUFS | The AD-04 A/B test only; true-peak ceiling unchanged; never at ac0 | 12/04 tokens `reels_test_variant` |
| Captions | WebVTT plus SRT sidecars from the approved script. A burned variant only where a profile requires it, inside the caption reserve | Architecture §9.1; 12/02 doc 08 §8.2 |
| Chapters | WebVTT `chapters` file from the Format Plan chapter boundaries (each at most 360 s). Description timestamps where the platform supports them (rules verify) | CE-15 |
| Cover | A deterministic `seek(t)` capture at a `cover_cue`, or a code-built card in the artefact's style. Text from the string table | 07/05 SH6 |

### 2.2 Per format

The "Default profiles" column is the default packaging profile set per format group; Resolver rule R14 reads it when the request names no `packaging_profiles` (Architecture §3.4; 15 Oct 2026). Short names: in-app = `packaging/in-app-player`, offline = `packaging/offline-download`, audio-only = `packaging/audio-only`, youtube-long = `packaging/youtube-long`, youtube-shorts = `packaging/youtube-shorts`, instagram-reels = `packaging/instagram-reels`, print = `packaging/print-pdf` (level-3+, CE-119, 15 Oct 2026).

| Format group | Length class / gate | Chapters | audio_only (R10) | Default profiles |
|---|---|---|---|---|
| detailed, simplified, worked_example, concept_intro, lab_demo, comparison, story_history, qa_doubt, prerequisite_repair, source_analysis, perspectives, read_along, concept_map, misconception_fix | long / GF | Yes when the plan has more than one chapter | F14 at ac0, F15, F23 (passage in transcript); others no | in-app-player, youtube-long, offline-download; audio-only for F14 (ac0), F15, F23 |
| recap, revision_sheet, practice_set, exam_strategy, viva_prep, question_analysis | long / GF | Revision Sheet and Practice Set chapters | F3, F9, F10, F25 only; never F4, F17 | in-app, youtube-long, offline; audio-only for F3, F9, F10, F25 only |
| short, flashcard_reel | short / GS | None | No | youtube-shorts, instagram-reels, in-app |
| derivation_proof, teacher_explainer | long / GF | Yes | No | in-app, youtube-long, offline |
| lecture_segment (16:9) | long / GF | Yes | No | in-app, youtube-long (after O-19) |
| series | inherits members | Chapter One-Shot: member boundaries become chapters | Members' rules | in-app playlist, youtube-long playlist |
| Print configurations (level-3+, CE-119, 15 Oct 2026): F-W Worksheet (`format/practice_set`), F-TN Teacher Notes (`format/teacher_explainer`), F-GN Guardian Note at AC0 (`format/recap`), Revision Sheet print (`format/revision_sheet`) | print / GF on the rendered PDF and its HTML twin | None | No (no narration) | print only |

Audio-only is allowed only for the formats listed in "Render targets and outputs" (F3, F9, F10, F15, F23, F25, and F14 at ac0), and only when every `visual_essential` scene is narrated (R10). The FORMAT_REGISTRY lists F23, but F23 is Path A read-along with on-screen text highlighting. [Recommendation] F23 audio-only therefore needs the text passage in the transcript.

**Print (level-3+, CE-119, 15 Oct 2026).** `render_target: print` is a tagged PDF/UA plus an HTML twin, both rendered from the same Format Plan through the pinned Chrome print path (vendored fonts, fixed document metadata, no wall-clock timestamps), so `artefact_sha256` is stable and Q-DET applies. It is allowed only for the four print configurations above (`../FORMAT_REGISTRY.md` "Print format configurations"), and only when every `visual_essential` element has a text alternative in the tag tree. There is no narration, so no voice path, loudness or caption rules apply. The answer key is a separate file or a separate final section, never on the question page. The profile is `packaging/print-pdf` (§3).

## 3. Platform packaging profiles

Safe-zone insets for every platform remain **measure per platform**. The 12/04 values are conservative placeholders (`measured: false`). A profile cannot be `released` until its platform key is measured, with `measured_on` and `device_list` recorded (schema; QA Profiles A4 blocks release on unmeasured insets).

| Profile | Accepts | Captions | Chapters | Disclosure placements | Notes |
|---|---|---|---|---|---|
| `packaging/youtube-long` | 9x16 long formats; 16x9 F20 after O-19 | Sidecar upload per locale (support verify) | WebVTT plus description timestamps (rules verify) | Description line; altered/synthetic toggle on every upload with AI voice (Path A converted, Path B); for A_direct only when another realistic synthetic element is present (house rule, narrowed 15 Oct 2026); C2PA not stripped | How a long vertical upload is classified (Short or not) is a platform rule to verify, never assumed |
| `packaging/youtube-shorts` | short, flashcard_reel | Sidecar (verify) plus an optional burned variant | None | As youtube-long | Safe-zone key `youtube_shorts` (placeholder) |
| `packaging/instagram-reels` | short, flashcard_reel; ac1, ac2 | Burned variant required [Recommendation; sidecar support unverified] | None | Caption line plus Meta AI label (07/06 §6.4; Meta rules unverified, 11 PB Step 14) | ac0 not published until G-COUNSEL records a decision [Recommendation] |
| `packaging/in-app-player` | All formats | Sidecar per locale | WebVTT | Player-page line, transcript header, sidecar | The platform transcodes and streams; the pipeline delivers master, variants and sidecars only |
| `packaging/offline-download` | All video formats | Sidecar | WebVTT | Sidecar, transcript header, end-card line where the format has one | For low-connectivity learners (02 §J): a `low_bandwidth` rendition (bitrate verify), file-size limit verify (NEW-8), and the transcript and captions as small files. **Withdrawals (level-2, CE-115, 15 Oct 2026):** the offline client checks `export/withdrawals.jsonl` {artefact_sha256, reason_class, replacement_sha256?, erratum_text} on every reconnect and hides each downloaded file whose `artefact_sha256` (or `derived_from_sha256`) matches a row, showing the `erratum_text` and, where present, offering the replacement. The pipeline publishes the file; the client behaviour is a platform requirement, recorded here so the profile cannot be released without it (Architecture §9.6) |
| `packaging/audio-only` | R10 formats only | Transcript (with described visuals) | WebVTT chapters | Listing line, transcript header; a spoken disclosure line waits on O-5 | M4A, −16 LUFS |
| `packaging/print-pdf` (level-3+, CE-119, 15 Oct 2026) | The four print configurations (§2.2), ac0 only for F-GN | None (tagged text) | None | Undecided: no `voice/` entry exists for a print artefact, so the disclosure source is open (§15 item 11) | PDF/UA plus HTML twin; answer key as a separate file; `print_variant.file_size_limit` for low-bandwidth use is **verify** (no figure set); Q-META.size checks it once set. Withdrawals reach downloaded print files the same way as offline video (`export/withdrawals.jsonl`). Schema: `print_variant` replaces `render_variant`, `loudness` and `captions`; worked example in `templates/packaging_profile.template.md` |

## 4. Titles, covers and descriptions

### 4.1 Rules (all formats)

1. **Truthful and exact.** "The title must accurately describe what the viewer receives. A 60-second checklist is not 'the complete chapter mastered in one minute'" (07/05 SH6).
   - The title names the format's real scope.
   - Durations, chapter counts, item counts, episode numbers, marks, years and as-of dates are **computed** from the Format Plan and the render, never typed (`computed_fields_only`).
2. **Closure.** Assertive title, cover and description sentences must map to approved nodes, and numbers must appear in a node or fixture. A question form must not state a misconception as fact. Copy never reveals a check answer (SCRIPTING_REGISTRY SQ-04). These rules run in Q-META.package_truth.
3. **Banned copy** (Q-COMM.copy [Recommendation]: the property-name lint extended to copy strings). It runs on the title, cover text, every description block and the hashtags (§4.6). **Corrected 15 Oct 2026:** the commercial and engagement lists are case-insensitive phrase patterns, not bare words, because bare words blocked standard curriculum titles such as "Like and Unlike Terms", "Free Fall", "Trial and Improvement" and "Comment on the Poet's Tone".
   - Every item on the 07/05 SH6 "Never" list: guaranteed-marks claims, "only for intelligent students", invented statistics, fake urgency, generated testimonials and virality scores.
   - Commercial phrases: `\bfor free\b` · `\bfree (lesson|chapter|class|course|access|trial|download|demo|content|video)s?\b` · `\bunlock(s|ed|ing)?\b` · `\bpremium (access|content|lesson|course|plan|member|version)s?\b` · `\b(buy|purchase|order) (now|today|our|the (book|course|app|full))\b` · `\boffer (ends|valid|expires)\b` · `\blimited[- ]time\b` · `\btrial (period|version|access|pack)\b` · `\bfull access\b`.
   - Engagement and data prompts: `\bsubscribe\b` · `\blike (and|&) (subscribe|share)\b` · `\b(like|share|save) (this|the|our) (video|reel|short|lesson|channel)\b` · `\bsmash (that|the) like\b` · `\bhit the bell\b` · `\bcomment (below|down|your)\b` · `\bfollow (us|me|for more)\b` · `\bdm (us|me)\b` · `\blink in bio\b` · `\btag a friend\b` · `\bshare (it )?with (your )?friends\b`.
   - At ac0, additionally exclamation runs and "challenge" framing.
   - **Waiver.** A hit is waived only when it lies inside the label of an approved VOC or CON node of this artefact's Format Plan that appears in the same string. Waived hits are recorded in `qa/Q-COMM.json`.
4. **Make relevance clear.** Show class, board or exam label, topic and medium, because the first objection is "is this relevant to my exam?" (07/05 SH6). The labels come from the Curriculum Graph framework record.

### 4.2 Title patterns

| Format | Pattern (bracketed parts computed or taken from nodes) |
|---|---|
| detailed | `<Topic>: Full Lesson in <n> Chapters (<Class> <Subject>)` |
| simplified | `<Topic>, Simply: One Idea and One Worked Example` |
| recap | `<Topic> Recap: <duration> Retrieval Check` |
| question_analysis | Past item: `<Exam> <year> <marks>-Mark Question: <what is asked>` (marks only with `marks_source`). Original: `Practice Question: <what is asked>` |
| short | The hook as a question or contradiction, from the `hook.*` slot text (07/05 SH6 examples) |
| worked_example | `Worked Example: <problem>, Then Try the Twin` |
| misconception_fix | `<misconception as a question>?`, ending in the correct model |
| exam_strategy | `<Exam> <section>: Time Plan from the Official Pattern (as of <date>)` |
| revision_sheet, flashcard_reel | `<Chapter> Revision: <n> Key Ideas` / `<Term>: Quick Recall` |
| lab_demo | `<Activity> (Real Demo)` or `(Virtual Lab)`; the label is mandatory |
| comparison | `<A> vs <B>: <n> Differences` |
| lecture_segment, series member | `<Course> · Lecture <k>, Part <m>: <topic>` / `<Series> · Episode <n>: <title>` |

### 4.3 Covers

- At most 4 words [Recommendation; backlog covers run 3–4 words, for example CHECK THE AXES, 01 RB].
- Text from the GA-Δ-approved string table, at style minimum sizes and contrast.
- Uppercase is for Latin only. Indic covers keep their script with no `text-transform`.
- No generated text (#54). No reveal of the check answer. No numbers unless traceable to a fixture.
- No shocked faces or alarm graphics [Recommendation]. No generated real-looking child at any audience class; a real child appears only with a guardian release on the MED node (Q-SAFE.child_likeness, CE-54). No red cross on an answer. (Corrected 15 Oct 2026: the rule was limited to ac0.)

### 4.4 Description blocks (in order)

1. `what_you_get`: exact content, with computed duration.
2. `condition`: the retained conditions (07/05 SH2 `retained_conditions`).
3. `audience_line`: class, subject, topic, locale.
4. `next_step`: the **title** of an approved artefact (`next_step_ref`). Never a URL or a commercial destination; the platform may resolve the ID inside its own app.
5. `chapters`.
6. `disclosure`: the exact template line (§7).
7. `credits`: "Script: <named author, or the Professor Diki Simplified team>. Academic review: <reviewer>." and the optional last line "Published by ExamLeaf." (the publisher line, the only place the publisher's name appears in audience-readable copy).
8. `sources`: citation text; URLs only per §8.
9. `last_revised`: provenance "contributors, sources and last revision date" [N60].
10. `errata`, if any.

### 4.5 Hindi, Hinglish and Assamese copy

- **Script.** hi-IN titles in Devanagari, with technical terms in Latin script per the Locale Profile code-mix policy. Hinglish in Latin script using the house transliteration table, never ad-hoc romanisation (CE-40). Assamese only after locale admission, in Bengali-Assamese script with ৰ and ৱ verified.
- **Authoring.** Copy is a REN rendering of the approved English string-table entry. It is approved by the native subject editor at GA-Δ for that locale, and is rewritten rather than translated (11 PB Step 7).
- **Rendering.** Glyph coverage (A8a) runs on the cover, the hashtags and burned captions. Title-length limits are verify per platform.

### 4.6 Hashtags, platform tags and upload text (added 15 Oct 2026)

- [Recommendation] At most 3 hashtags per locale (`copy[].hashtags`; schema pattern `^#[^\s#]+$`, unique). They come from the approved string table and name only a class, board or exam label, subject or topic from the Curriculum Graph framework record. No trend, challenge or engagement hashtags, and no brand or handle tags.
- **ac0: none.** The schema allows 0 hashtags at ac0, because a description hashtag is a clickable route out of the item (platform behaviour verify), which §8 "No outward routes" forbids.
- **Same checks as other copy.** Hashtags pass closure (Q-META.package_truth), Q-COMM.copy, Q-SAFE.no_external_prompts and A8a glyph coverage. They are inside `copy_sha256`, so the COPY approval covers them. Locale script follows §4.5.
- **Platform tag or keyword fields** carry nothing beyond the approved hashtags (without `#`), or stay empty. Field names and limits are verify.
- **Nothing is added at upload.** The uploaded title, description and hashtags equal the approved `copy[]` entry for that locale; the publisher adds no tags, hashtags or text.

## 5. Captions and transcripts per locale and level

- **Source.** The approved script text, with zero word mismatches. Timing comes from the measured timeline within the 05 alignment tolerance (Q-A11Y.captions). Captions never come from ASR (Architecture §9.1) or from pronunciation respellings (12/05 README §6).
- **Shape.** 1–2 lines, large and high-contrast. Kept clear of the bottom UI band and the right action rail (11 PB Step 12, platform specs unverified). One keyword highlight per caption, using the beat's emphasis word, marked by weight as well as colour. SRT carries plain text and WebVTT carries the highlight.
- **Level.**
  - l1_2: `access_only`. Captions exist for hearing access, but the lesson never depends on them.
  - l3_5, l6_8: `short_lines` (Cal, O-20).
  - All other levels: `standard`.
  - Captions never simplify the script. Reading level is set at script time (SCRIPTING_REGISTRY).
- **Locale.**
  - en-IN in Latin script.
  - hi-IN in Devanagari, with technical terms in Latin script.
  - Hinglish in Latin script.
  - RTL locales use RTL cue direction after the Q-LOCALE test.
  - Fonts are vendored Noto families.
- **Mathematics.** Captioned in display notation. The transcript carries both display and spoken forms (RD-29).
- **Answer protection.** No caption or transcript line shows an answer before its think window ends (A10).
- **Transcript.**
  - `transcript.txt` in reading order.
  - `transcript.json`: sentence → `node_ids[]`, cue times, display and spoken forms.
  - Described visuals from `ad.vtt` for `visual_essential` scenes.
  - The disclosure line as a header.

## 6. The neutral metadata sidecar

`export/sidecar.json` validates against `#/definitions/metadata_sidecar` (`additionalProperties: false`). Measured quantities are decimal strings with units (CE-32).

| Block | Holds |
|---|---|
| ids | `package_id`, `artefact_id`, `packaging_profile` (versioned) |
| `files[]` | Role, path, SHA-256 and locale; variants and renditions carry `derived_from_sha256` |
| `binding` | Master `artefact_sha256`, `epp_hash`, `closure_hash`, `graph_subtree_sha256`, `format_plan_sha256`, `packaging_profile_sha256` (whole profile), `release_manifest_sha256` (the signed S13 manifest, 07/06 §6.3), and `approvals[]` (gate, ID, state, bound hash). The schema requires GA_DELTA, H_SB, GF or GS, COPY, DISCLOSURE and RELEASE_CHECK entries |
| `classification` | Format@version, variant, level@version, `audience_class`, family@version, subject, locale, overlay, persona, voice path, render target, aspect |
| `curriculum` | Framework ID and version, `competency_guids[]`, `objective_ids[]` |
| `pins` | Every registry pin@version mapped to its SHA-256, including `music/`, `lex/` and `persona/<id>@x.y.z#<variant>`; the packaging profile only as `packaging/<id>@x.y.z#render` |
| `copy[]` | Per locale: title, cover text, description blocks, hashtags (§4.6), string-table ref, `copy_sha256` (over locale, title, cover text, description blocks, hashtags and the cover image hash) and `copy_approval_id` (the COPY approval bound to `copy_sha256`) |
| `chapters[]`, `series` | Chapter titles and times. `series_position`, `episode_number`, `prerequisites[]`, `next_step_ref` (artefact or objective IDs) |
| `render` | Codec, resolution, fps, duration, loudness, true peak |
| `accessibility` | a11y profile, caption locales, transcript, audio description, reduced-motion variant; sign language deferred (O-18) |
| `disclosure` | Voice identity, path, `disclosure_variant`, `text_ref`, `ai_voice_disclosure`, `performer_credit`, child variant text, required placements |
| `provenance` | Contributors (registry IDs), sources (SRC IDs and citations), last revision date, created_at, ledger ref, C2PA block |
| `audience` | `audience_class`, G-COUNSEL record, designation hint |
| `links[]` | Source links allowed by §8 only |
| `supersedes_package_id` | Optional: the released package this corrected package replaces |

**Corrections (15 Oct 2026).** `artefact_id` is stable across corrections. A corrected artefact gets new hashes, approvals and `package_id` under the same `artefact_id`, so the platform's artefact-id join (CE-68) switches to it. When a released package exists for the same `artefact_id` and `packaging_profile`, the new package names it in `supersedes_package_id` (checked by Q-META.sidecar_complete).

**Forbidden fields.** They are documented in the schema `description`, and are impossible by construction:

1. The CE-26 regex, case-insensitive (widened 15 Oct 2026, Architecture §1.2 P1): `(price|pricing|paid|is_free|free_|premium|entitle|subscri|sku|paywall|unlock|monetis|monetiz|revenue|discount|coupon|tier|destination_resource|cta_destination|funnel|purchase_|checkout_|product_id|offer_|trial_|utm_|campaign_|affiliate_|activation_code|storefront)`, applied to every object key at every depth (including REN fields keys), every `required` entry, pattern key and enum or const value; `series_position`, `flagship` and `demo_kind` are exempt. A scan of all `*.json` under `15_content_engine_v2` with this regex and scope gives 0 hits as of 15 Oct 2026.
2. Any field containing `tier`, including v1 `ShortSpec.access_tier` (07/05 SH2).
3. v1 routing and funnel fields: `destination_resource_id`, `funnel_objective` (01 RB CSV), CTA destinations, purchase or checkout fields, product, bundle, offer and trial fields, and book-activation fields and secrets (07/06 §7 "never exported").
4. Advertising and analytics: ads, campaigns, UTM tags, affiliates, conversion fields, experiment IDs and arms, virality and "brain activity" scores (07/05 §4).
5. Learner data: names, IDs, contacts, schools, handles, submissions (CE-20).
6. Secrets and access tokens: API keys, auth and playback tokens, signed URLs.

The editorial fields `series_position`, `flagship` and `demo_kind` stay exempt (CE-25). Only `series_position` is exported.

## 7. Disclosure placements per platform and voice path

The template text comes from the `voice/` registry entry, which is the single source (Architecture §3.1).

- **Path A (converted):** "Performed by X; voice converted with AI tools; reviewed by Y."
- **Path A (direct, as-IN):** ~~`ai_voice_disclosure` is "No AI voice processing." (VOICE §3.9).~~ "Narrated by X; no AI voice processing; reviewed by Y." (VOICE §3.9 and 07/06 §6.4 A-direct row; wording pending counsel, O-5; aligned 15 Oct 2026).
- **Path B:** "AI-generated narration; script by X; reviewed by Y." `X` is a named person or "the Professor Diki Simplified team", never the publisher name (16 Oct 2026).

~~These are the 07/06 §6.4 wording, and the schema enforces them by pattern.~~ **Corrected 15 Oct 2026:** the lines above are the 07/06 §6.4 en-IN wording. The text is held once per locale in the `voice/` entry (VOICE §3.9) and the sidecar names it by `disclosure.text_ref`. Q-DISC enforces the exact per-locale text from the `voice/` entry, byte for byte; the schema enforces that `disclosure_variant` (`path_a_converted`, `path_a_direct`, `path_b_tts`), voice path and `performer_credit` agree. The en-IN wording itself is still open (§15 item 3). Path A wording on Path B content is rejected. `performer_credit` is `none` for Path B. An empty value fails release.

| Channel | Placement (both paths unless stated) |
|---|---|
| YouTube long and Shorts | Description line. Altered/synthetic toggle on every upload with AI voice (Path A converted, Path B); for A_direct only when another realistic synthetic element is present (house rule, RD-45, narrowed 15 Oct 2026; YouTube itself requires it for realistic synthetic content [11:N40] and may auto-label [11:N45]). C2PA not stripped |
| Instagram Reels | Caption line and the Meta AI label (07/06 §6.4) |
| In-app player | Player-page line, transcript header, sidecar. ~~[Recommendation] An end-card line for Path B~~ (moved to the master, below) |
| Offline / download | Sidecar and transcript header |
| Audio-only | Listing line and transcript header. A spoken line is a counsel decision (O-5) |

**End-card line (15 Oct 2026).** Where the Format Spec has an end-card slot, the end card carries the `voice/` entry's disclosure line (the child variant at ac0). For `concept_short_60` (PD-10, PD-13, PD-20; 16 Oct 2026) it carries instead the two literal lines of `17_professor_diki_simplified/brand/strings.json`: the brand line "Professor Diki Simplified" and "Free lesson: <topic>", with no disclosure line, URL, QR code, handle or price; the disclosure template line stays in the description and in `ai_voice_disclosure`. It is rendered into the master for every channel, covered by the master's GF/GS, and never added or removed by packaging; `placements_required` then includes `end_card_line`.

- **ac0.** Age-appropriate child-variant wording (CE-19) on the end card, with the full template line in the description for grown-ups.
- **No mismatch.** A real-teacher cutaway is never placed over Path B audio (11 PB Step 14).
- **Non-realistic visuals.** Non-realistic animated visuals need no platform disclosure in themselves [11:N42], but the house line is always used.

**C2PA.** CE-38 strips container metadata (`-map_metadata -1`) so that masters are bit-identical, while 07/06 §6.4 forbids stripping C2PA. [Recommendation] The resolution:

- The master stays stripped and hash-bound.
- Before the mux, the exporter records by hash any provenance manifests present in vendor TTS or STS audio (whether vendors embed them is verify; 11 PB question 4).
- The exporter (`examleaf-packaging-export`) ships a C2PA **sidecar manifest** that references the master hash.
- Embedding into a distribution copy, and whether platforms read sidecars, is verify.
- `stripped_by_pipeline` is `false` by schema.

## 8. Kids' packaging (ac0) and minors (ac1)

**ac0 (l1_2, l3_5):**

- **Designation.** `audience_class: safety/ac0` maps to `designation_hint: made_for_kids_required`. The publisher sets the platform flag under a current G-COUNSEL record (CE-17, CE-37; sources S-4 and S-5, open items O-3 and O-4).
- **Instagram.** [Recommendation] Not published to Instagram until G-COUNSEL decides.
- **No outward routes.** No links, URLs, QR codes, handles or hashtags anywhere: video, cover, description or transcript (Q-SAFE.no_external_prompts; hashtags §4.6). `links[]` must be empty (schema). Sources are listed by citation text only.
- **No engagement prompts.** No like, subscribe, comment, share or "next video" prompts. [Recommendation] No platform end elements that point outside ac0 playlists (feature names verify).
- **Audio.** Owned audio only: commissioned or code-composed, admitted in the `music/` registry (MUSIC_and_SOUND_REGISTRY policy 4). No licensed stock, trend or platform-library tracks (`audio_sources: owned_audio_only`).
- **Copy and covers.** No brand names. No real-looking children on covers. Plain, calm titles with no urgency.
- **Playlists.** ac0 playlists contain ac0 members only.
- **Comments.** Comment settings are publisher-side (verify per platform). The pipeline never asks for comments.

**ac1 (l6_8–l11_12, ug, voc):**

- No data solicitation. "Comment your answer", "DM us" and "tell us your school" are all solicitation (CE-20).
- Links only to official board or government sources (LEVEL_PROFILES §2; the schema enum enforces this).
- No fear or urgency in exam copy.
- Doubts are paraphrased, never attributed.

**ac2:** links only to registered sources.

## 9. Series and course packaging

- **Episode numbers.** `episode_number` is computed from `composition.ordering` and is 1-based. `series_position` must agree with the member's Content Request; `first` forces Path A (R1). Titles take the `Episode <n>` prefix.
- **Playlists.** One playlist per `series_id`. Members must be approved with valid closures (`members_must_be_approved`). The series package lists every member's master hash.
  - A stale member makes the series stale.
  - A revoked member blocks the series and withdraws its playlist entry.
- **Prerequisites.** `requires` edges and Curriculum Graph `prerequisite_of` become "Before this:" with the title of an approved artefact covering the prerequisite, or the competency label if none exists. Never a URL at ac0.
- **Chapter One-Shot.** One file whose member boundaries become WebVTT chapters, keeping each at most 360 s [N2][N3].
- **Paper Walkthrough.** `paper_order`, the paper's licence among the sources, and marks only from the official key.
- **Bridges.** `bridge.return_link` and `chapter.title` have their own GF.

## 10. Accessibility deliverables

| Deliverable | When | Channels | Produced by (15 Oct 2026; SKILLS_and_KIT_MAP_v2 §6 rule 6) |
|---|---|---|---|
| Captions (WebVTT and SRT per locale) | Always | All; burned variant where the profile requires it | `examleaf-alignment-localize` / `examleaf-speech-animation-synchronizer` |
| Transcript (txt and json, display and spoken forms) | Always | In-app, offline, audio-only; on request elsewhere | `examleaf-speech-animation-synchronizer` |
| `ad.vtt` and `audio_described.m4a` | Any `visual_essential` scene whose meaning is not fully spoken (Architecture §9.1) | In-app, offline | `ad.vtt`: `examleaf-speech-animation-synchronizer` (text from the script's `ad_sentences[]`); `audio_described.m4a`: `examleaf-voice-synthesis` (AD voicing, S9) + `examleaf-audio-production-engineer` (mix, S10) |
| Reduced-motion variant | Always rendered (schema constant) | In-app and offline as an alternate; social platforms lack alternates (verify). A package lists the variant in `files[]` only when the channel delivers it, and then `binding.approvals` must hold a GF/GS approval on its sha256; otherwise the sidecar says `rendered_not_delivered_on_channel` (15 Oct 2026) | `examleaf-render-batch` (S10) |
| Audio-only derivative | R10 formats only | audio-only profile | `examleaf-packaging-export` (S14) |
| ~~Sign language~~ Indian Sign Language inset (`a11y/isl`; level-3+, CE-120, 15 Oct 2026) | ~~Deferred until triggered (O-18)~~ Only when a request names `a11y/isl`; O-18 trigger reworded: the first `a11y/isl` request or a pilot with a special-education partner. Path A only; a qualified ISL reviewer approves it at GF (Q-A11Y.isl) | In-app, offline | A human interpreter recorded under Path A consent, composited into the safe-zone token by `examleaf-web-composition` [Recommendation] |
| Keyboard keys and screen-reader labels for every ASM option (level-3+, CE-120, 15 Oct 2026) | Every interaction that presents options (mcq, match, ordering, diagram_label) | In-app (through `export/interactions.json` `option_labels[]`) | Copied by `examleaf-packaging-export` from the Interaction Spec; checked by Q-A11Y.asm_labels |
| Tagged PDF/UA, HTML twin and separate answer key (level-3+, CE-119, 15 Oct 2026) | `render_target: print` | print-pdf | The print render skill (`examleaf-print-render`, SKILLS map §3); checked by Q-A11Y.print_structure |

## 11. Export QA

Every ID below is catalogued in `QA_PROFILES_REGISTRY.md` §2.7 (Q-META.hash_bind in §2.1), which owns severities; this table lists what the export stage runs (15 Oct 2026). The export checks are run by `examleaf-packaging-export` (S14), except RELEASE-CHECK (approval service). (added 15 Oct 2026)

| ID | Verifies | Severity |
|---|---|---|
| RELEASE-CHECK | Closure recomputed; no stale or revoked pin or approval; every QA-Profile gate requirement met (15 Oct 2026); every approval's `signature` verified with `ssh-keygen -Y verify` (namespace `examleaf-approval`) against the reviewer key valid at its `timestamp`, an unsigned or mis-signed row counting as absent (level-1, CE-113, 15 Oct 2026) | C |
| Q-META.hash_bind | Master hash equals the GF/GS-bound hash. Each delivered variant has its own GF/GS. Each rendition carries `derived_from_sha256` and passes its re-checks. Each `copy[]` entry's `copy_sha256` equals the `bound_sha256` of the COPY approval named by its `copy_approval_id` | C |
| Q-META.sidecar_complete | Sidecar validates; every required block is present; when a released package exists for the same `artefact_id` and `packaging_profile`, `supersedes_package_id` names it | C |
| Q-COMM.sidecar / Q-COMM.copy | No forbidden field name; no banned copy phrase (§4.1) in title, cover text, description blocks or hashtags | C |
| Q-META.package_truth | Copy claims trace to approved nodes; computed fields match the plan and render; no answer reveal | C (15 Oct 2026; QA §2.7) |
| Q-DISC.placement | Runs per channel after S14 on the publish receipt (§1). Every required placement confirmed by the publisher; correct path template; child variant at ac0; `made_for_kids_flag: set` at ac0 on YouTube; C2PA mode recorded. `disclosure.voice_identity` equals the `voice/` pin in `sidecar.pins` and the EPP; `disclosure.voice_path` equals EPP `resolved.voice_path` | C |
| Q-A11Y.captions (packaged) | Every packaged caption file and burned variant equals the script; timing within tolerance | C |
| A9.package | Loudness and true peak on every delivered audio-bearing file, including renditions, the AD mix and audio-only | C |
| A11.package | Probe of every video file against the profile and the EPP resolution | C |
| A4.platform | Safe-zone overlay against the target platform's **measured** insets | C at release |
| Q-SAFE.no_external_prompts (copy) | ac0 and ac1 link and prompt rules on title, cover, description, hashtags and transcript | C |
| Q-SAFE.child_likeness (cover) | The cover image, including every asset a `code_card` composes, against Q-SAFE.child_likeness | C |
| Q-META.interactions_sidecar | `export/interactions.json` validates against `#/definitions/interaction_sidecar`; every Interaction Spec interaction appears exactly once; times equal the measured final timeline (15 Oct 2026); `option_labels[]` copied verbatim from the Interaction Spec (level-3+, CE-120, 15 Oct 2026) | C |
| Q-A11Y.asm_labels (level-3+, CE-120, 15 Oct 2026) | Every ASM option in the sidecar has a keyboard key and a screen-reader label; no label marks the key | C |
| Q-A11Y.print_structure (print only; level-3+, CE-119, 15 Oct 2026) | Tag tree, reading order, alt text, table headers, language, contrast; answers never on the question page | C |
| A8a.copy | Glyph coverage on cover text, hashtags and burned captions | C |
| Q-META.chapters | Chapter cues equal the Format Plan boundaries, within ±1 frame | M |
| Q-META.size | File size within the profile's configured limit (verify value; NEW-8); for print, `print_variant.file_size_limit` (verify; 15 Oct 2026) | M |
| Q-RIGHTS.scope | For every `voice/` and `music/` pin in the closure, on the export date: the voice entry is admitted and not revoked; the export date is ≤ voice `expiry.expires_on` and, where a consent block exists, ≤ `consent.term_end`; the package channel is in `consent.platforms` and, for music, in `commission.platforms`; the artefact locale is in `consent.languages`; music `expiry.expires_on` is null or ≥ the export date. Until profiles carry a distribution-territory field, the publisher confirms territory at DISCLOSURE (15 Oct 2026) | C |

## 12. Invalidation rules

| Change | Class | Re-QA | Gates reopened | Published |
|---|---|---|---|---|
| Profile copy rules, sidecar fields, chapters mode, series display | Metadata | Re-export; export QA | DISCLOSURE only if placements change | Stale until re-exported |
| Approved title, cover, description text or hashtags | Metadata (copy) | Q-COMM.copy, Q-META.package_truth, Q-SAFE.no_external_prompts (ac0, ac1) | COPY on the new `copy_sha256`, by the GF/GS reviewer pair. No re-watch, because the video bytes are unchanged | Stale |
| Encode or rendition settings | Render toolchain | Re-encode; A9, A11, A13; hashes | None while the master is unchanged | Stale, then re-affirmed |
| Burned-caption style | Presentational | Re-render the variant; A-suite on it | GF/GS on that variant | Stale |
| Platform insets measured or changed | Presentational | A4 on every artefact for that platform | H-SB where layout changes; GF/GS | Stale |
| Voice disclosure text (new `voice/` version) | Narration/disclosure | Q-DISC; re-export (re-mux if spoken) | DISCLOSURE (VOICE and GF/GS if audio changes) | Stale |
| ac0 or ac1 audience rules, or designation mapping | Safety | Q-SAFE on all affected packages | G-COUNSEL re-record if loosened | Failing packages withdrawn |
| ~~Curriculum framework version~~ (split 15 Oct 2026 by the framework diff, Architecture §3.6, CE-116) | ~~Metadata~~ | ~~Metadata re-export~~ | ~~H-CG~~ | ~~Stale~~ |
| Framework item text or metadata edited; item moved to another class or unit (level-2, CE-116) | Metadata | Sidecar re-export (`curriculum` block) | H-CG | Stale until re-exported |
| Framework item removed (level-2, CE-116) | Semantic | Every package whose sidecar lists only removed GUIDs | H-CG; content gates for any artefact re-scoped | Relabelled "Not in <board> <year> syllabus" or unlisted for that framework edition; never silently kept. Packages stay releasable for every edition still inside its `valid_academic_years` |
| Framework item added (level-2, CE-116) | Metadata | Coverage-gap row only | H-CG | Unaffected |
| Framework depth or outcome changed (level-2, CE-116) | Semantic | Recompile the affected subtree | H-CG, GA-Graph and the downstream gates | Stale |
| Master or member revoked | Revocation | — | — | Withdrawn on every channel; the publisher gets a takedown list: every publish receipt whose `uploaded_file_sha256` is, or derives from, the revoked hash. *(Level-2, CE-115, 15 Oct 2026.)* A row is appended to `export/withdrawals.jsonl` {artefact_sha256, reason_class, replacement_sha256?, erratum_text} for the master and every derived file; the platform polls it and offline and print clients hide matching files on reconnect. [Recommendation] targets: S1 withdrawn from every channel within 24 h, S2 corrected or labelled within 7 days (Architecture §9.6); each incident writes an `incident` ledger row |
| Correction of a released artefact (07/06 §8) | Per the changed content | Full re-QA of the changed bytes; export QA | GA-Δ (GA-Graph if a node changed), GF/GS, DISCLOSURE, COPY if copy changed | New package under the same `artefact_id` with `supersedes_package_id`; the platform switches by artefact id (CE-68) |

## 13. Negative tests

| # | Input | Expected result |
|---|---|---|
| NP-01 | Sidecar with `access_tier: free` | Schema and Q-COMM.sidecar fail |
| NP-02 | Description "Unlock the full chapter" | Q-COMM.copy fails |
| NP-03 | ac0 package with a URL in `links[]` | Schema and Q-SAFE fail |
| NP-04 | ac0 Short end card "Subscribe for more!" | Q-SAFE.no_external_prompts fails |
| NP-05 | Path A line on Path B audio | Schema variant rule and Q-DISC.script fail |
| NP-06 | Burned captions differ from the sidecar text | Q-A11Y.captions fails |
| NP-07 | Master hash differs from the GF hash | Q-META.hash_bind and RELEASE-CHECK fail |
| NP-08 | Recap titled "Complete chapter mastered in 90 seconds" | package_truth and banned-phrase failure |
| NP-09 | hi-IN title with ad-hoc romanisation, or a missing Devanagari glyph | Q-LOCALE / A8a fails |
| NP-10 | audio_only package for `format/detailed` | R10 compile error |
| NP-11 | 16:9 package for `format/short` | Format Spec rejects it (CE-46) |
| NP-12 | Lesson mastered at −14 LUFS outside AD-04 | A9.package fails |
| NP-13 | Series playlist with a stale or unapproved member | Series package blocked |
| NP-14 | Cover from an image model containing letters | A7 OCR fails |
| NP-15 | Sidecar includes a learner's name from a doubt | Schema and Q-SAFE fail |
| NP-16 | Profile `released` with `insets_measured: false` | Schema rejects it |
| NP-17 | Profile stating a bitrate with `status: verify` | Schema rejects it (no invented platform specs) |
| NP-18 | Distribution copy with the C2PA manifest stripped | `stripped_by_pipeline` must be false; Q-DISC fails |
| NP-19 | Sidecar with `classification.audience_class: safety/ac0` but `audience.audience_class: safety/ac2` and `designation_hint: per_counsel_record` | Schema rejects it |
| NP-20 | ac0 sidecar with `voice_path: B` | Schema rejects it (R1, CE-L9) |
| NP-21 | Sidecar with `series_position: first` and `voice_path: B` | Schema rejects it (R1) |
| NP-22 | Sidecar with `classification.voice_path: A` and `disclosure.voice_path: B` | Schema rejects it |
| NP-23 | Titles "Like and Unlike Terms", "Free Fall", "Comment on the Poet's Tone", "Issue of Shares at a Premium" | Q-COMM.copy passes; "Unlock the full chapter" (NP-02) and "Subscribe for more!" still fail |
| NP-24 | `youtube_shorts` or `instagram_reels` profile with ac0 `publish: allowed`, or an ac0 rule without `platform_end_elements` | Schema rejects it |
| NP-25 | A `print` profile carrying `loudness` or `render_variant`, or a print profile on channel `in_app_player` (level-3+, CE-119, 15 Oct 2026) | Schema rejects it |
| NP-26 | `packaging/print-pdf` with a typed `file_size_limit` value and `status: verify` | Schema rejects it (no invented figures) |
| NP-27 | An interaction sidecar with an MCQ and no `option_labels` (level-3+, CE-120, 15 Oct 2026) | Schema rejects it; Q-META.interactions_sidecar fails |
| NP-28 | A revoked artefact with no `export/withdrawals.jsonl` row (level-2, CE-115, 15 Oct 2026) | The Revocation is incomplete: the incident's withdraw time stays unset in its `incident` ledger row, and offline and print copies stay visible, until the row is appended (Architecture §9.6) [Recommendation] |
| NP-29 | A video profile without `A9.package` in `export_qa` (15 Oct 2026: the rule moved into the non-print branch) | Schema rejects it |

## 14. Worked example sidecars

The values are **illustrative**. Hashes are placeholders, and the GUID, SRC, reviewer, model, kit and slot IDs are invented for the example. Both files validate against `#/definitions/metadata_sidecar`. *(15 Oct 2026.)* Each `pins` map lists every required EPP pin kind (format, level, safety, family, locale, a11y, persona with `#variant`, voice, `lex/core.<locale>`, `qa/catalogue`, one model per cascade rung, kit, harness, every slot used, style, packaging as `#render`) plus the `music/` candidates selected at S5. GA_DELTA's `bound_sha256` is a `script_content_sha256` placeholder and H_SB's a `storyboard_sha256` placeholder (Architecture §3.7 per-gate binding); DISCLOSURE's is the delivered file's SHA-256.

### 14.1 Detailed lesson (`format/detailed`, `level/l9_10`, en-IN, Path A, in-app player)

Three chapters, each at most 360 s (blueprint segments). Reduced-motion variant delivered, with its own GF. Path A per R1 (format default and `first` in series).

```json
{
  "schema_version": "1.0.0",
  "package_id": "PKG-ohm1-l9_10-detailed-en-in-001",
  "artefact_id": "ART-ohm1-l9_10-detailed-en-in",
  "packaging_profile": "packaging/in-app-player@1.0.0",
  "files": [
    {"role": "master_video", "path": "master.mp4", "sha256": "000000000000000000000000000000000000000000000000000000000000d001"},
    {"role": "reduced_motion_variant", "path": "master.reduced_motion.mp4", "sha256": "000000000000000000000000000000000000000000000000000000000000d002"},
    {"role": "captions_webvtt", "path": "captions.en-IN.vtt", "sha256": "000000000000000000000000000000000000000000000000000000000000d003", "locale": "locale/en-in"},
    {"role": "captions_srt", "path": "captions.en-IN.srt", "sha256": "000000000000000000000000000000000000000000000000000000000000d004", "locale": "locale/en-in"},
    {"role": "chapters_webvtt", "path": "chapters.vtt", "sha256": "000000000000000000000000000000000000000000000000000000000000d005"},
    {"role": "transcript_txt", "path": "transcript.en-IN.txt", "sha256": "000000000000000000000000000000000000000000000000000000000000d006", "locale": "locale/en-in"},
    {"role": "transcript_json", "path": "transcript.en-IN.json", "sha256": "000000000000000000000000000000000000000000000000000000000000d007", "locale": "locale/en-in"},
    {"role": "cover_image", "path": "cover.png", "sha256": "000000000000000000000000000000000000000000000000000000000000d008"},
    {"role": "c2pa_manifest", "path": "master.c2pa", "sha256": "000000000000000000000000000000000000000000000000000000000000d009"}
  ],
  "binding": {
    "artefact_sha256": "000000000000000000000000000000000000000000000000000000000000d001",
    "epp_hash": "000000000000000000000000000000000000000000000000000000000000e001",
    "closure_hash": "000000000000000000000000000000000000000000000000000000000000e002",
    "graph_subtree_sha256": "000000000000000000000000000000000000000000000000000000000000e003",
    "format_plan_sha256": "000000000000000000000000000000000000000000000000000000000000e004",
    "approvals": [
      {"gate": "GA_GRAPH", "approval_id": "APR-ga-graph-ohm1-001", "state": "valid", "bound_sha256": "000000000000000000000000000000000000000000000000000000000000e003"},
      {"gate": "GA_DELTA", "approval_id": "APR-ga-delta-ohm1-det-001", "state": "valid", "bound_sha256": "000000000000000000000000000000000000000000000000000000000000e0c5"},
      {"gate": "H_SB", "approval_id": "APR-hsb-ohm1-det-001", "state": "valid", "bound_sha256": "000000000000000000000000000000000000000000000000000000000000e05b"},
      {"gate": "VOICE", "approval_id": "APR-voice-ohm1-det-001", "state": "valid", "bound_sha256": "000000000000000000000000000000000000000000000000000000000000e005"},
      {"gate": "GF", "approval_id": "APR-gf-ohm1-det-001", "state": "valid", "bound_sha256": "000000000000000000000000000000000000000000000000000000000000d001"},
      {"gate": "GF", "approval_id": "APR-gf-ohm1-det-rm-001", "state": "valid", "bound_sha256": "000000000000000000000000000000000000000000000000000000000000d002"},
      {"gate": "COPY", "approval_id": "APR-copy-ohm1-det-en-in-001", "state": "valid", "bound_sha256": "000000000000000000000000000000000000000000000000000000000000d00a"},
      {"gate": "DISCLOSURE", "approval_id": "APR-disc-ohm1-det-inapp-001", "state": "valid", "bound_sha256": "000000000000000000000000000000000000000000000000000000000000d001"},
      {"gate": "RELEASE_CHECK", "approval_id": "APR-rc-ohm1-det-001", "state": "valid", "bound_sha256": "000000000000000000000000000000000000000000000000000000000000e002"}
    ],
    "packaging_profile_sha256": "000000000000000000000000000000000000000000000000000000000000e006",
    "release_manifest_sha256": "000000000000000000000000000000000000000000000000000000000000e007"
  },
  "classification": {"format": "format/detailed@1.0.0", "level": "level/l9_10@1.0.0", "audience_class": "safety/ac1", "family": "family/stem_fixture@1.0.0", "subject": "physics", "locale": "locale/en-in", "persona": "persona/super-teacher@1.0.0#core", "voice_path": "A", "render_target": "video", "aspect": "9x16"},
  "curriculum": {"framework_id": "framework/seba_hslc_science", "framework_version": "1.0.0", "competency_guids": ["00000000-0000-4000-8000-000000000101"], "objective_ids": ["OBJ-ohm1"]},
  "pins": {
    "format/detailed@1.0.0": "000000000000000000000000000000000000000000000000000000000000f001",
    "level/l9_10@1.0.0": "000000000000000000000000000000000000000000000000000000000000f002",
    "safety/ac1@1.0.0": "000000000000000000000000000000000000000000000000000000000000f003",
    "family/stem_fixture@1.0.0": "000000000000000000000000000000000000000000000000000000000000f004",
    "locale/en-in@1.0.0": "000000000000000000000000000000000000000000000000000000000000f005",
    "style/doodle-handdrawn@1.0.0": "000000000000000000000000000000000000000000000000000000000000f006",
    "style/whiteboard-science@1.0.0": "000000000000000000000000000000000000000000000000000000000000f007",
    "voice/brand-en-in-sts@1.0.0": "000000000000000000000000000000000000000000000000000000000000f008",
    "harness/render-linux@1.0.0": "000000000000000000000000000000000000000000000000000000000000f009",
    "packaging/in-app-player@1.0.0#render": "000000000000000000000000000000000000000000000000000000000000f00a",
    "a11y/base@1.0.0": "000000000000000000000000000000000000000000000000000000000000f00b",
    "persona/super-teacher@1.0.0#core": "000000000000000000000000000000000000000000000000000000000000f010",
    "lex/core.en-in@1.0.0": "000000000000000000000000000000000000000000000000000000000000f011",
    "qa/catalogue@1.0.0": "000000000000000000000000000000000000000000000000000000000000f012",
    "model/kit-fill-haiku@1.0.0": "000000000000000000000000000000000000000000000000000000000000f013",
    "model/kit-fill-sonnet@1.0.0": "000000000000000000000000000000000000000000000000000000000000f014",
    "model/kit-fill-opus@1.0.0": "000000000000000000000000000000000000000000000000000000000000f015",
    "kit/detailed-stem-l9-12@1.0.0": "000000000000000000000000000000000000000000000000000000000000f016",
    "slot/hook.realworld@1.0.0": "000000000000000000000000000000000000000000000000000000000000f020",
    "slot/misconception.elicit@1.0.0": "000000000000000000000000000000000000000000000000000000000000f021",
    "slot/explain.ladder_step@1.0.0": "000000000000000000000000000000000000000000000000000000000000f022",
    "slot/check.interpolated@1.0.0": "000000000000000000000000000000000000000000000000000000000000f023",
    "slot/explain.analogy@1.0.0": "000000000000000000000000000000000000000000000000000000000000f024",
    "slot/worked.step@1.0.0": "000000000000000000000000000000000000000000000000000000000000f025",
    "slot/worked.faded_twin@1.0.0": "000000000000000000000000000000000000000000000000000000000000f026",
    "slot/check.retrieval@1.0.0": "000000000000000000000000000000000000000000000000000000000000f027",
    "slot/misconception.confront@1.0.0": "000000000000000000000000000000000000000000000000000000000000f028",
    "slot/recap.retrieval@1.0.0": "000000000000000000000000000000000000000000000000000000000000f029",
    "slot/close.next_step@1.0.0": "000000000000000000000000000000000000000000000000000000000000f02a",
    "music/logo-core-short@1.0.0": "000000000000000000000000000000000000000000000000000000000000f030",
    "music/logo-core-full@1.0.0": "000000000000000000000000000000000000000000000000000000000000f031"
  },
  "copy": [{
    "locale": "locale/en-in",
    "title": "Ohm's Law and I–V Graphs: Full Lesson in 3 Chapters (Class 10 Physics)",
    "cover_text": "CHECK THE CONDITION",
    "description_blocks": [
      {"kind": "what_you_get", "text": "A 10-minute lesson in 3 chapters: the relationship, one worked calculation with a practice twin, and reading I–V graphs."},
      {"kind": "condition", "text": "The rule holds for an ohmic conductor at constant temperature and other conditions."},
      {"kind": "audience_line", "text": "Class 10 · Physics · Electricity · English (India)"},
      {"kind": "next_step", "text": "Next: the I–V graph check Short."},
      {"kind": "chapters", "text": "1 Voltage, current and the condition · 2 Calculating current · 3 Reading I–V graphs"},
      {"kind": "disclosure", "text": "Performed by [performer]; voice converted with AI tools; reviewed by [reviewer]."},
      {"kind": "credits", "text": "Script: the Professor Diki Simplified team. Academic review: [reviewer]. Production review: [production reviewer]. Published by ExamLeaf."},
      {"kind": "sources", "text": "[Board textbook, Class 10 Science, Electricity chapter; registered edition SRC-board-sci10-elec]"},
      {"kind": "last_revised", "text": "Last revised 2026-10-15"}
    ],
    "hashtags": ["#Class10Physics", "#OhmsLaw"],
    "string_table_ref": "ST-ohm1-l9_10-detailed-en-in@1.0.0",
    "copy_sha256": "000000000000000000000000000000000000000000000000000000000000d00a",
    "copy_approval_id": "APR-copy-ohm1-det-en-in-001"
  }],
  "chapters": [{"index": 1, "title": "Voltage, current and the condition", "start": "0.000 s", "end": "210.000 s"}, {"index": 2, "title": "Calculating current", "start": "210.000 s", "end": "440.000 s"}, {"index": 3, "title": "Reading I–V graphs", "start": "440.000 s", "end": "600.000 s"}],
  "series": {"series_id": "SER-class10-electricity", "series_position": "first", "episode_number": 1, "prerequisites": [], "next_step_ref": "ART-ohm1-l9_10-short-trap-en-in"},
  "render": {"container": "mp4", "video_codec": "h264", "pixel_format": "yuv420p", "resolution": "1080x1920", "frame_rate": 30, "audio_codec": "aac", "audio_sample_rate_hz": 48000, "duration": "600.000 s", "integrated_loudness": "-16.0 LUFS", "true_peak": "-1.2 dBTP"},
  "accessibility": {"a11y_profile": "a11y/base@1.0.0", "caption_locales": ["locale/en-in"], "captions_source": "approved_script", "transcript": true, "audio_description": "not_required_all_visual_essential_narrated", "reduced_motion_variant": "provided", "sign_language": "deferred_until_o18_trigger"},
  "disclosure": {"voice_identity": "voice/brand-en-in-sts@1.0.0", "voice_path": "A", "disclosure_variant": "path_a_converted", "text_ref": "voice/brand-en-in-sts@1.0.0#disclosure.en-in", "ai_voice_disclosure": "Performed by [performer]; voice converted with AI tools; reviewed by [reviewer].", "performer_credit": "[performer]", "placements_required": ["player_page_line", "transcript_header", "sidecar_field"]},
  "provenance": {
    "contributors": [{"role": "script_author", "reviewer_id": "reviewer/author-01", "display_name": "the Professor Diki Simplified team"}, {"role": "academic_reviewer", "reviewer_id": "reviewer/physics-01", "display_name": "[reviewer]"}, {"role": "production_reviewer", "reviewer_id": "reviewer/prod-01", "display_name": "[production reviewer]"}, {"role": "performer", "reviewer_id": "performer/perf-01", "display_name": "[performer]"}],
    "sources": [{"source_id": "SRC-board-sci10-elec", "citation": "[Board textbook, Class 10 Science, Electricity chapter, registered edition]"}],
    "last_revision_date": "2026-10-15",
    "created_at": "2026-10-15T00:00:00Z",
    "ledger_ref": "ledger/2026-10.jsonl#ART-ohm1-l9_10-detailed-en-in",
    "c2pa": {"mode": "sidecar_manifest", "manifest_sha256": "000000000000000000000000000000000000000000000000000000000000d009", "upstream_manifests_recorded": [], "stripped_by_pipeline": false}
  },
  "audience": {"audience_class": "safety/ac1", "g_counsel_record": "GCR-ac1-export-1.0.0", "designation_hint": "per_counsel_record"},
  "links": []
}
```

### 14.2 Short (`format/short`, `short.trap`, Path B, YouTube Shorts)

The Short is laid out natively, never cropped (07/05 §1). The published burned-caption variant has its own GS. DISCLOSURE binds to the uploaded file. The reduced-motion variant is rendered but not delivered on this channel (§10), so it is not in `files[]`.

```json
{
  "schema_version": "1.0.0",
  "package_id": "PKG-ohm1-l9_10-short-trap-en-in-yts-001",
  "artefact_id": "ART-ohm1-l9_10-short-trap-en-in",
  "packaging_profile": "packaging/youtube-shorts@1.0.0",
  "files": [
    {"role": "master_video", "path": "master.mp4", "sha256": "000000000000000000000000000000000000000000000000000000000000a001"},
    {"role": "burned_caption_variant", "path": "master.captions_burned.en-IN.mp4", "sha256": "000000000000000000000000000000000000000000000000000000000000a002", "derived_from_sha256": "000000000000000000000000000000000000000000000000000000000000a001"},
    {"role": "captions_webvtt", "path": "captions.en-IN.vtt", "sha256": "000000000000000000000000000000000000000000000000000000000000a004", "locale": "locale/en-in"},
    {"role": "captions_srt", "path": "captions.en-IN.srt", "sha256": "000000000000000000000000000000000000000000000000000000000000a005", "locale": "locale/en-in"},
    {"role": "transcript_txt", "path": "transcript.en-IN.txt", "sha256": "000000000000000000000000000000000000000000000000000000000000a006", "locale": "locale/en-in"},
    {"role": "transcript_json", "path": "transcript.en-IN.json", "sha256": "000000000000000000000000000000000000000000000000000000000000a007", "locale": "locale/en-in"},
    {"role": "cover_image", "path": "cover.png", "sha256": "000000000000000000000000000000000000000000000000000000000000a008"},
    {"role": "c2pa_manifest", "path": "master.c2pa", "sha256": "000000000000000000000000000000000000000000000000000000000000a009"}
  ],
  "binding": {
    "artefact_sha256": "000000000000000000000000000000000000000000000000000000000000a001",
    "epp_hash": "000000000000000000000000000000000000000000000000000000000000b001",
    "closure_hash": "000000000000000000000000000000000000000000000000000000000000b002",
    "graph_subtree_sha256": "000000000000000000000000000000000000000000000000000000000000e003",
    "format_plan_sha256": "000000000000000000000000000000000000000000000000000000000000b004",
    "approvals": [
      {"gate": "GA_DELTA", "approval_id": "APR-ga-delta-ohm1-short-001", "state": "valid", "bound_sha256": "000000000000000000000000000000000000000000000000000000000000b0c5"},
      {"gate": "H_SB", "approval_id": "APR-hsb-ohm1-short-001", "state": "valid", "bound_sha256": "000000000000000000000000000000000000000000000000000000000000b05b"},
      {"gate": "VOICE", "approval_id": "APR-voice-ohm1-short-001", "state": "valid", "bound_sha256": "000000000000000000000000000000000000000000000000000000000000b005"},
      {"gate": "GS", "approval_id": "APR-gs-ohm1-short-001", "state": "valid", "bound_sha256": "000000000000000000000000000000000000000000000000000000000000a001"},
      {"gate": "GS", "approval_id": "APR-gs-ohm1-short-burned-001", "state": "valid", "bound_sha256": "000000000000000000000000000000000000000000000000000000000000a002"},
      {"gate": "COPY", "approval_id": "APR-copy-ohm1-short-en-in-001", "state": "valid", "bound_sha256": "000000000000000000000000000000000000000000000000000000000000a00a"},
      {"gate": "DISCLOSURE", "approval_id": "APR-disc-ohm1-short-yts-001", "state": "valid", "bound_sha256": "000000000000000000000000000000000000000000000000000000000000a002"},
      {"gate": "RELEASE_CHECK", "approval_id": "APR-rc-ohm1-short-001", "state": "valid", "bound_sha256": "000000000000000000000000000000000000000000000000000000000000b002"}
    ],
    "packaging_profile_sha256": "000000000000000000000000000000000000000000000000000000000000b006",
    "release_manifest_sha256": "000000000000000000000000000000000000000000000000000000000000b007"
  },
  "classification": {"format": "format/short@1.0.0", "variant": "short.trap", "level": "level/l9_10@1.0.0", "audience_class": "safety/ac1", "family": "family/stem_fixture@1.0.0", "subject": "physics", "locale": "locale/en-in", "persona": "persona/super-teacher@1.0.0#core", "voice_path": "B", "render_target": "video", "aspect": "9x16"},
  "curriculum": {"framework_id": "framework/seba_hslc_science", "framework_version": "1.0.0", "competency_guids": ["00000000-0000-4000-8000-000000000101"], "objective_ids": ["OBJ-ohm1"]},
  "pins": {
    "format/short@1.0.0": "000000000000000000000000000000000000000000000000000000000000c001",
    "level/l9_10@1.0.0": "000000000000000000000000000000000000000000000000000000000000f002",
    "safety/ac1@1.0.0": "000000000000000000000000000000000000000000000000000000000000f003",
    "style/doodle-handdrawn@1.0.0": "000000000000000000000000000000000000000000000000000000000000f006",
    "style/whiteboard-science@1.0.0": "000000000000000000000000000000000000000000000000000000000000f007",
    "voice/brand-en-in-tts@1.0.0": "000000000000000000000000000000000000000000000000000000000000c002",
    "harness/render-linux@1.0.0": "000000000000000000000000000000000000000000000000000000000000f009",
    "packaging/youtube-shorts@1.0.0#render": "000000000000000000000000000000000000000000000000000000000000c003",
    "family/stem_fixture@1.0.0": "000000000000000000000000000000000000000000000000000000000000f004",
    "locale/en-in@1.0.0": "000000000000000000000000000000000000000000000000000000000000f005",
    "a11y/base@1.0.0": "000000000000000000000000000000000000000000000000000000000000f00b",
    "persona/super-teacher@1.0.0#core": "000000000000000000000000000000000000000000000000000000000000f010",
    "lex/core.en-in@1.0.0": "000000000000000000000000000000000000000000000000000000000000f011",
    "qa/catalogue@1.0.0": "000000000000000000000000000000000000000000000000000000000000f012",
    "model/kit-fill-haiku@1.0.0": "000000000000000000000000000000000000000000000000000000000000f013",
    "model/kit-fill-sonnet@1.0.0": "000000000000000000000000000000000000000000000000000000000000f014",
    "model/kit-fill-opus@1.0.0": "000000000000000000000000000000000000000000000000000000000000f015",
    "kit/short-stem-l9-12@1.0.0": "000000000000000000000000000000000000000000000000000000000000c016",
    "slot/hook.question_reveal@1.0.0": "000000000000000000000000000000000000000000000000000000000000c020",
    "slot/worked.step@1.0.0": "000000000000000000000000000000000000000000000000000000000000f025",
    "slot/check.retrieval@1.0.0": "000000000000000000000000000000000000000000000000000000000000f027",
    "music/logo-core-short@1.0.0": "000000000000000000000000000000000000000000000000000000000000f030"
  },
  "copy": [{
    "locale": "locale/en-in",
    "title": "Which Line Has the Larger Resistance? Check the Axes (Class 10 Physics)",
    "cover_text": "CHECK THE AXES",
    "description_blocks": [
      {"kind": "what_you_get", "text": "A 30-second graph check: compare the current at the same voltage to find the larger resistance."},
      {"kind": "condition", "text": "I is on the vertical axis and V on the horizontal axis."},
      {"kind": "audience_line", "text": "Class 10 · Physics · Electricity · English (India)"},
      {"kind": "next_step", "text": "Next: Ohm's Law and I–V Graphs, full lesson."},
      {"kind": "disclosure", "text": "AI-generated narration; script by the Professor Diki Simplified team; reviewed by [reviewer]."},
      {"kind": "credits", "text": "Script: the Professor Diki Simplified team. Academic review: [reviewer]. Published by ExamLeaf."},
      {"kind": "last_revised", "text": "Last revised 2026-10-15"}
    ],
    "hashtags": ["#Class10Physics"],
    "string_table_ref": "ST-ohm1-l9_10-short-trap-en-in@1.0.0",
    "copy_sha256": "000000000000000000000000000000000000000000000000000000000000a00a",
    "copy_approval_id": "APR-copy-ohm1-short-en-in-001"
  }],
  "chapters": [],
  "series": {"series_position": "standalone", "prerequisites": [], "next_step_ref": "ART-ohm1-l9_10-detailed-en-in"},
  "render": {"container": "mp4", "video_codec": "h264", "pixel_format": "yuv420p", "resolution": "1080x1920", "frame_rate": 30, "audio_codec": "aac", "audio_sample_rate_hz": 48000, "duration": "30.000 s", "integrated_loudness": "-16.0 LUFS", "true_peak": "-1.4 dBTP"},
  "accessibility": {"a11y_profile": "a11y/base@1.0.0", "caption_locales": ["locale/en-in"], "captions_source": "approved_script", "transcript": true, "audio_description": "not_required_all_visual_essential_narrated", "reduced_motion_variant": "rendered_not_delivered_on_channel"},
  "disclosure": {"voice_identity": "voice/brand-en-in-tts@1.0.0", "voice_path": "B", "disclosure_variant": "path_b_tts", "text_ref": "voice/brand-en-in-tts@1.0.0#disclosure.en-in", "ai_voice_disclosure": "AI-generated narration; script by the Professor Diki Simplified team; reviewed by [reviewer].", "performer_credit": "none", "placements_required": ["description_line", "platform_synthetic_toggle", "sidecar_field"]},
  "provenance": {
    "contributors": [{"role": "script_author", "reviewer_id": "reviewer/author-01", "display_name": "the Professor Diki Simplified team"}, {"role": "academic_reviewer", "reviewer_id": "reviewer/physics-01", "display_name": "[reviewer]"}, {"role": "production_reviewer", "reviewer_id": "reviewer/prod-01", "display_name": "[production reviewer]"}],
    "sources": [{"source_id": "SRC-board-sci10-elec", "citation": "[Board textbook, Class 10 Science, Electricity chapter, registered edition]"}],
    "last_revision_date": "2026-10-15",
    "created_at": "2026-10-15T00:00:00Z",
    "ledger_ref": "ledger/2026-10.jsonl#ART-ohm1-l9_10-short-trap-en-in",
    "c2pa": {"mode": "sidecar_manifest", "manifest_sha256": "000000000000000000000000000000000000000000000000000000000000a009", "upstream_manifests_recorded": [], "stripped_by_pipeline": false}
  },
  "audience": {"audience_class": "safety/ac1", "g_counsel_record": "GCR-ac1-export-1.0.0", "designation_hint": "per_counsel_record"},
  "links": []
}
```

## 15. Inconsistencies and open items

1. **No `packaging/` registry.** Architecture §3.1 has no `packaging/` kind and §3.6 has no packaging row. This document proposes both: the Metadata class for copy and sidecar, and Render toolchain or Presentational for bytes. **Resolved 15 Oct 2026 (CE-63):** the Architecture §3.1 addendum adds `packaging/` with exactly that split.
2. **C2PA against bit-exact masters.** CE-38's `-map_metadata -1` conflicts with 07/06 §6.4 "C2PA not stripped". Resolved here by a sidecar manifest, but the C2PA tooling is unverified.
3. **Disclosure wording.** 07/06 §6.4 ("voice converted with AI tools; reviewed by Y") and 11 PB Step 14 ("voice converted with AI. Reviewed by…") differ. The `voice/` entry must hold one text. **15 Oct 2026:** RD-45, 07/06 §6.4 and VOICE §3.9 still differ, and the VOICE §3.9 text failed the old sidecar pattern. The schema no longer fixes the wording (§7); the en-IN text needs a lead ruling. Resolved 15 Oct 2026 (in part): VOICE §3.9 uses the 07/06 §6.4 wording; whether RD-45's row text or 07/06 §6.4 is the house text still needs the lead ruling..
4. **v1 commercial fields.** v1 `ShortSpec.access_tier` and `destination_resource_id`, the 07/06 §7 "free / preview / book-entitlement" and "destination resource" rows, the 07/05 SH1 product CTAs, and the 01 RB "free lesson" CTAs and funnel objectives are all excluded from v2 packaging. `v1-import` must drop them, and Q-COMM.copy catches the copy. **Recorded 15 Oct 2026 (CE-68):** 07/05 and Architecture §10 carry a dated note retiring `access_tier` and `destination_resource_id` from the pipeline contract; removing them from the 04 code is a P1 build item.
5. **Review of variants and renditions.** Whether variants (reduced-motion, burned captions) each need GF/GS, and whether renditions are exempt, needs a lead ruling under CE-14. The capacity cost is real.
6. **Unverified platform figures.** Bitrates, file-size limits, title and description lengths, chapter rules, cover dimensions, Shorts classification, caption-sidecar support on Reels and platform age designations are all verify.
7. **Other gates.** The 16:9 youtube-long path waits on O-19. The audio-only spoken disclosure waits on O-5. ac0 on Instagram waits on G-COUNSEL.
8. **F23 audio-only.** F23 is listed as audio-only, yet its meaning is on-screen text; the transcript must carry the passage.
9. **F16 mixed-path compositions** (15 Oct 2026) have no sidecar form: `voice_path` is A or B, and `voice_identity` is single. Until specified, a mixed series ships as a playlist of single-path members.
10. **Print sidecar** (level-3+, CE-119, 15 Oct 2026). The neutral `metadata_sidecar` requires `classification.voice_path`, a `master_video` or `audio_only` file and a video or audio `render` block, so a print package has no valid sidecar yet. The profile schema accepts `render_target: print` and `print_variant`; the sidecar's print form (file roles for the PDF, HTML twin and answer key; no voice fields) is a schema change still to make, and `packaging/print-pdf` stays `draft` until it exists.
11. **Print disclosure** (15 Oct 2026). `disclosure.template_source` is the `voice/` entry, and a print artefact has none. Which disclosure text a print artefact carries (and the AC0 wording for F-GN) needs a lead ruling; until then `disclosure` is not required on a print profile and DISCLOSURE is recorded on the line text the publisher confirms.
12. **Offline withdrawal check** (level-2, CE-115, 15 Oct 2026). Hiding withdrawn files on reconnect is client behaviour outside the pipeline; the pipeline's part is the `export/withdrawals.jsonl` row. No profile field records the client's compliance yet.
