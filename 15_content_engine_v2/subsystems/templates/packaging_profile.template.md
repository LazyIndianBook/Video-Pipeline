# Packaging profile template (`content/registry/packaging/<id>.yaml`)

Validates against `../schemas/packaging_profile.schema.json`. A packaging profile says how an approved artefact is encoded, captioned, titled, disclosed and described for one channel. It has two halves with different change classes (Architecture §3.1 addendum, CE-63):

- **Bytes** (`render_variant`, burned captions): pinned in the EPP as `packaging/<id>@x.y.z#render`, the SHA-256 of {`render_variant`, `loudness`, `captions.max_lines`, `safe_zone`}. The whole-profile hash goes in the sidecar's `binding.packaging_profile_sha256`. An end-card disclosure line, where the format has one, is part of the master and never a packaging field (15 Oct 2026). A change is Presentational or Render toolchain class, so it re-encodes and re-runs the automated checks, and reopens GF/GS only where bytes change.
- **Distribution** (copy rules, sidecar, chapters mode, disclosure placements, audience rules, series display): pinned in the Distribution Package record. A change is Metadata class and re-exports without reopening the full-watch gate.

The profile never carries entitlement, price, destination, campaign, analytics or learner data. The neutral metadata sidecar it points at (`#/definitions/metadata_sidecar`) is `additionalProperties: false`, so a forbidden field is impossible by construction. Spec: `../PACKAGING_and_DISTRIBUTION_REGISTRY.md`. Dated 15 Oct 2026.

Rules to remember before you fill it in:

- **No invented platform figures.** Bitrate, file-size, title and description lengths, cover dimensions, chapter rules and caption-sidecar support are `verify_value` objects: `{value: null, status: verify}` until someone measures or confirms them from the platform's current documentation, with a `source` and `checked_on`. The schema rejects a value on a `verify` status.
- **A profile cannot be `released` until its safe-zone insets are measured** (`safe_zone.insets_measured: true`, with `measured_on` and `device_list`). Placeholder insets from 12/04 are for drafts only.
- **Any profile that allows `safety/ac0`** must set `loudness_test_variant_allowed: false` (the −14 LUFS A/B arm is never used with children), must use `audio_sources: owned_audio_only` (CE-66) and must state `platform_end_elements: ac0_playlist_only`. On `youtube_long` or `youtube_shorts`, ac0 `publish` is never `allowed`; on `instagram_reels` it is `not_published_pending_g_counsel` (schema, 15 Oct 2026).
- **Loudness is fixed** at −16.0 LUFS ±1 LU, true peak at most −1.0 dBTP (constants). The AD-04 −14 LUFS Reels arm is a separate rendition, never the house master, and only an `instagram_reels` profile may set `loudness_test_variant_allowed: true`.
- **No commercial or "tier" field names** (CE-26, CE-70).
- **Print profiles** *(level-3+, CE-119, 15 Oct 2026)*. `render_target: print` (channel `print_pdf`) carries `print_variant` instead of `render_variant`, `loudness` and `captions`: a PDF/UA plus an HTML twin from the pinned Chrome print path, vendored fonts, fixed document metadata, the answer key as a separate file or final section, and a `file_size_limit` that stays `verify`. Aspects are `["none"]`, chapters `none`, and `export_qa` must include `Q-A11Y.print_structure` and `Q-META.size`. `safe_zone` and `disclosure` are not required for print (PACKAGING §15 items 10 and 11). Every non-print profile must carry `render_variant`, `loudness`, `captions`, `safe_zone` and `disclosure`, and must not carry `print_variant` (schema).

## Fill-in skeleton

```yaml
packaging_id: packaging/<lowercase-id>          # e.g. packaging/youtube-shorts
version: 1.0.0
title: <Human title>
status: draft                                   # draft | released | deprecated | revoked
channel: <youtube_long | youtube_shorts | instagram_reels | in_app_player | offline_download | audio_only | print_pdf>   # print_pdf ⇔ render_target print (15 Oct 2026)
render_target: <video | audio_only | print>     # audio_only ⇒ m4a, no video codec, frame_rate 0, never burned captions, aspects ["none"]; print ⇒ print_variant below, no render_variant/loudness/captions, aspects ["none"] (level-3+, CE-119)
formats_allowed: [format/<id>]                  # audio_only only for the R10 formats
safety_classes_allowed: [safety/<ac0 | ac1 | ac2>]
aspects_accepted: [<9x16 | 16x9 | none>]       # 16x9 only for F20 and after O-19
duration_class: <long | short | any>
print_variant:                                  # print only (level-3+, CE-119); BYTES half of a print profile
  outputs: [pdf_ua, html]                       # both required
  renderer: pinned_chrome_print_path            # constant
  fonts: vendored_bundle                        # constant
  document_metadata: fixed_no_wall_clock        # constant, so artefact_sha256 is stable
  answer_key: <separate_file | separate_final_section>
  file_size_limit: {value: null, status: verify}   # low-bandwidth ceiling; never an invented number
render_variant:                                 # BYTES half (video and audio_only)
  container: <mp4 | m4a>
  video_codec: <h264 | none>
  pixel_format: <yuv420p | none>                # video ⇒ yuv420p
  frame_rate: <30 for video | 0 for audio_only>
  audio_codec: aac                              # constant
  audio_sample_rate_hz: 48000                   # constant
  faststart: <true for video>
  bitexact_single_thread_master: true           # constant (CE-38)
  video_bitrate: {value: null, status: verify}  # never an invented number
  audio_bitrate: {value: null, status: verify}
  renditions: []                                # each {rendition_id, resolution, video_bitrate: verify_value, purpose: <low_bandwidth | small_storage>, rechecks: [A9, A11, A13]}
  burned_captions: <never | optional_variant | required_variant>
loudness:
  integrated: "-16.0 LUFS"                      # constant (house loudness, MUSIC policy 6)
  tolerance_lu: 1                               # constant
  true_peak_max: "-1.0 dBTP"                    # constant
  measured_after_final_mux: true                # constant
  loudness_test_variant_allowed: false          # ac0 ⇒ false; true only for instagram_reels (AD-04 −14 LUFS arm, a separate rendition, never the house master)
captions:
  source: approved_script                       # constant: never ASR, never pronunciation respellings
  sidecar_formats: [<webvtt | srt>]
  platform_sidecar_upload: {value: null, status: verify}
  max_lines: <1 or 2>
  keyword_highlight: one_per_caption_not_colour_alone     # constant
  inside_caption_reserve: true                  # constant
  answer_protected: true                        # constant: no answer before its think window ends (A10)
chapters:
  mode: <none | webvtt_chapters | webvtt_chapters_and_description_timestamps>
  from: format_plan_chapter_boundaries          # when mode is not none
  platform_rules: {value: null, status: verify}
cover:
  source: <cue_frame | code_card | none>
  text_source: string_table                     # constant
  max_words: 4
  generated_text: forbidden                     # constant
  answer_reveal: forbidden                      # constant
  dimensions: {value: null, status: verify}
copy_rules:
  title_pattern_ref: <PACKAGING_and_DISTRIBUTION_REGISTRY.md#4.2>
  title_max_length: {value: null, status: verify}
  description_max_length: {value: null, status: verify}
  computed_fields_only: [<duration | chapter_count | item_count | episode_number | marks | year | as_of_date>]
  banned_phrases_ref: <PACKAGING_and_DISTRIBUTION_REGISTRY.md#4.1>
  description_order: [<what_you_get | condition | audience_line | next_step | chapters | disclosure | credits | sources | last_revised | errata>]
safe_zone:
  tokens: {path: <token file>, json_pointer: <platform key pointer>, sha256: <64 hex>}
  platform_key: <key in the token file>
  insets_measured: <false for draft | true to release>
  measured_on: "<YYYY-MM-DD>"  # when measured
  device_list: [<devices used>]
  release_requires_measured: true               # constant
disclosure:
  template_source: voice_registry               # constant: the voice/ entry is the single source of the line
  placements: [<description_line | platform_synthetic_toggle | platform_ai_label | end_card_line | transcript_header | player_page_line | sidecar_field | spoken_line>]
  c2pa_mode: <sidecar_manifest | embedded_in_distribution_copy>
  strip_upstream_provenance: false              # constant
audience_rules:                                 # all three classes are required; ac0 publish: youtube_* ⇒ never 'allowed', instagram_reels ⇒ not_published_pending_g_counsel
  safety/ac0: {publish: <allowed_with_made_for_kids_designation | not_published_pending_g_counsel | allowed>, links: none, engagement_prompts: forbidden, platform_end_elements: ac0_playlist_only, audio_sources: owned_audio_only}
  safety/ac1: {links: official_board_or_government_only, data_solicitation: forbidden}
  safety/ac2: {links: registered_sources_only}
series:
  playlist: <one_per_series_id | none>
  episode_numbering: from_composition_ordering  # constant
  prerequisites_display: <artefact_titles | none>
accessibility_deliverables: [<captions | transcript | audio_description_vtt | audio_described_mix | reduced_motion_variant | chapters | tagged_pdf_ua | html_twin | separate_answer_key>]   # print: tagged_pdf_ua and html_twin required
sidecar_schema: "#/definitions/metadata_sidecar"   # constant
export_qa: [<check ids; must include RELEASE-CHECK, Q-META.hash_bind, Q-META.sidecar_complete, Q-COMM.sidecar, Q-COMM.copy, Q-DISC.placement and Q-RIGHTS.scope; plus A9.package and Q-META.interactions_sidecar when render_target is not print; plus Q-A11Y.print_structure and Q-META.size when it is print; plus A11.package, A4.platform and Q-A11Y.captions when render_target is video; plus Q-SAFE.no_external_prompts when ac0 or ac1 is allowed>]
evidence: [{claim: <…>, tag: <Recommendation | Hypothesis | Inherited | Evidence>, source: <ref>, owner: <if Hypothesis>, pilot_ref: <if Hypothesis>}]
changelog: [{version: <x.y.z>, date: "<YYYY-MM-DD>", change_class: <Metadata | Presentational | Render toolchain | Narration/disclosure | Safety | Revocation>, summary: <…>}]
```

## Worked example

A draft in-app player profile. The hashes are placeholders, every platform figure is `verify`, and the safe-zone insets are not yet measured, so the profile cannot be `released`. This block validates against the schema.

```json
{
  "packaging_id": "packaging/in-app-player",
  "version": "1.0.0",
  "title": "In-app player",
  "status": "draft",
  "channel": "in_app_player",
  "render_target": "video",
  "formats_allowed": ["format/detailed", "format/simplified", "format/recap", "format/question_analysis", "format/short"],
  "safety_classes_allowed": ["safety/ac0", "safety/ac1", "safety/ac2"],
  "aspects_accepted": ["9x16"],
  "duration_class": "any",
  "render_variant": {
    "container": "mp4",
    "video_codec": "h264",
    "pixel_format": "yuv420p",
    "frame_rate": 30,
    "audio_codec": "aac",
    "audio_sample_rate_hz": 48000,
    "faststart": true,
    "bitexact_single_thread_master": true,
    "video_bitrate": {"value": null, "status": "verify"},
    "audio_bitrate": {"value": null, "status": "verify"},
    "burned_captions": "never"
  },
  "loudness": {"integrated": "-16.0 LUFS", "tolerance_lu": 1, "true_peak_max": "-1.0 dBTP", "measured_after_final_mux": true, "loudness_test_variant_allowed": false},
  "captions": {"source": "approved_script", "sidecar_formats": ["webvtt", "srt"], "max_lines": 2, "keyword_highlight": "one_per_caption_not_colour_alone", "inside_caption_reserve": true, "answer_protected": true},
  "chapters": {"mode": "webvtt_chapters", "from": "format_plan_chapter_boundaries"},
  "cover": {"source": "cue_frame", "text_source": "string_table", "max_words": 4, "generated_text": "forbidden", "answer_reveal": "forbidden", "dimensions": {"value": null, "status": "verify"}},
  "copy_rules": {
    "title_pattern_ref": "PACKAGING_and_DISTRIBUTION_REGISTRY.md#4.2",
    "title_max_length": {"value": null, "status": "verify"},
    "computed_fields_only": ["duration", "chapter_count", "episode_number", "as_of_date"],
    "banned_phrases_ref": "PACKAGING_and_DISTRIBUTION_REGISTRY.md#4.1",
    "description_order": ["what_you_get", "condition", "audience_line", "next_step", "chapters", "disclosure", "credits", "sources", "last_revised"]
  },
  "safe_zone": {
    "tokens": {"path": "12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json", "json_pointer": "/platform_insets_px/in_app_player", "sha256": "0000000000000000000000000000000000000000000000000000000000000001"},
    "platform_key": "in_app_player",
    "insets_measured": false,
    "release_requires_measured": true
  },
  "disclosure": {"template_source": "voice_registry", "placements": ["player_page_line", "transcript_header", "sidecar_field"], "c2pa_mode": "sidecar_manifest", "strip_upstream_provenance": false},
  "audience_rules": {
    "safety/ac0": {"publish": "allowed", "links": "none", "engagement_prompts": "forbidden", "platform_end_elements": "ac0_playlist_only", "audio_sources": "owned_audio_only"},
    "safety/ac1": {"links": "official_board_or_government_only", "data_solicitation": "forbidden"},
    "safety/ac2": {"links": "registered_sources_only"}
  },
  "series": {"playlist": "one_per_series_id", "episode_numbering": "from_composition_ordering", "prerequisites_display": "artefact_titles"},
  "accessibility_deliverables": ["captions", "transcript", "audio_description_vtt", "audio_described_mix", "reduced_motion_variant", "chapters"],
  "sidecar_schema": "#/definitions/metadata_sidecar",
  "export_qa": ["RELEASE-CHECK", "Q-META.hash_bind", "Q-META.sidecar_complete", "Q-META.interactions_sidecar", "Q-META.package_truth", "Q-META.chapters", "Q-COMM.sidecar", "Q-COMM.copy", "Q-DISC.placement", "Q-A11Y.captions", "A9.package", "A11.package", "A4.platform", "Q-SAFE.no_external_prompts", "Q-RIGHTS.scope"],
  "evidence": [{"claim": "In-app safe-zone insets are not measured; a draft cannot be released", "tag": "Recommendation", "source": "PACKAGING_and_DISTRIBUTION_REGISTRY.md section 3"}]
}
```

## Worked example: print (added 15 Oct 2026; level-3+, CE-119)

A draft `packaging/print-pdf` profile for the print configurations (F-W Worksheet, F-TN Teacher Notes, F-GN Guardian Note, Revision Sheet print). The file-size limit is `verify`. It cannot be released while the neutral sidecar has no print form and the print disclosure source is undecided (PACKAGING §15 items 10 and 11). This block validates against the schema.

```json
{
  "packaging_id": "packaging/print-pdf",
  "version": "1.0.0",
  "title": "Print PDF and HTML",
  "status": "draft",
  "channel": "print_pdf",
  "render_target": "print",
  "formats_allowed": ["format/practice_set", "format/teacher_explainer", "format/recap", "format/revision_sheet"],
  "safety_classes_allowed": ["safety/ac0", "safety/ac1", "safety/ac2"],
  "aspects_accepted": ["none"],
  "duration_class": "any",
  "print_variant": {
    "outputs": ["pdf_ua", "html"],
    "renderer": "pinned_chrome_print_path",
    "fonts": "vendored_bundle",
    "document_metadata": "fixed_no_wall_clock",
    "answer_key": "separate_file",
    "file_size_limit": {"value": null, "status": "verify"}
  },
  "chapters": {"mode": "none"},
  "cover": {"source": "code_card", "text_source": "string_table", "max_words": 4, "generated_text": "forbidden", "answer_reveal": "forbidden", "dimensions": {"value": null, "status": "verify"}},
  "copy_rules": {
    "title_pattern_ref": "PACKAGING_and_DISTRIBUTION_REGISTRY.md#4.2",
    "computed_fields_only": ["item_count", "marks", "as_of_date"],
    "banned_phrases_ref": "PACKAGING_and_DISTRIBUTION_REGISTRY.md#4.1",
    "description_order": ["what_you_get", "audience_line", "credits", "sources", "last_revised", "errata"]
  },
  "audience_rules": {
    "safety/ac0": {"publish": "allowed", "links": "none", "engagement_prompts": "forbidden", "platform_end_elements": "ac0_playlist_only", "audio_sources": "owned_audio_only"},
    "safety/ac1": {"links": "official_board_or_government_only", "data_solicitation": "forbidden"},
    "safety/ac2": {"links": "registered_sources_only"}
  },
  "series": {"playlist": "none", "episode_numbering": "from_composition_ordering", "prerequisites_display": "artefact_titles"},
  "accessibility_deliverables": ["tagged_pdf_ua", "html_twin", "separate_answer_key"],
  "sidecar_schema": "#/definitions/metadata_sidecar",
  "export_qa": ["RELEASE-CHECK", "Q-META.hash_bind", "Q-META.sidecar_complete", "Q-META.package_truth", "Q-META.size", "Q-COMM.sidecar", "Q-COMM.copy", "Q-DISC.placement", "Q-A11Y.print_structure", "Q-SAFE.no_external_prompts", "Q-RIGHTS.scope"],
  "evidence": [{"claim": "The print file-size limit for low-bandwidth use is not set; it is a value to verify", "tag": "Recommendation", "source": "FORMAT_REGISTRY.md render targets (print), CE-119"}]
}
```

## Checklist before GR (registry change review)

1. The entry validates, the commercial-term lint is clean, and no copy rule or field name introduces a commercial word.
2. Every platform figure is `verify` until measured or confirmed, with a source and date. No invented bitrate, length or dimension.
3. The profile is `released` only with measured insets, a measured-on date and a device list.
4. AC0 is listed only with the audience rules above, a current G-COUNSEL record for the designation, and no engagement elements or outward links. Instagram stays `not_published_pending_g_counsel` until counsel records a decision.
5. `export_qa` includes, always, `RELEASE-CHECK`, `Q-META.hash_bind`, `Q-META.sidecar_complete`, `Q-COMM.sidecar`, `Q-COMM.copy`, `Q-DISC.placement` and `Q-RIGHTS.scope`; `Q-META.interactions_sidecar` and `A9.package` unless `render_target` is print; `Q-A11Y.print_structure` and `Q-META.size` when it is print (15 Oct 2026); when `render_target` is video, also `A11.package`, `A4.platform` and `Q-A11Y.captions` (audio-only delivers a transcript instead of captions); and `Q-SAFE.no_external_prompts` when the profile allows ac0 or ac1 (schema-enforced, 15 Oct 2026).
6. Variants (burned-caption, reduced-motion, audio-described) are listed so each gets its own GF/GS on its own hash. Renditions carry `derived_from_sha256` and re-check A9, A11 and A13.
7. Run the impact preview. A bytes change queues a re-encode of every package pinned to this profile. A copy or sidecar change is a re-export only, and published packages are stale until it completes.
