# 05 · Style guides for the advanced-animation layer

**What this folder is.** Five versioned house style guides for illustrative and narrative scenes in ExamLeaf's 1080×1920 (9:16) lessons and Reels, plus one machine-readable token file. They are the "style guide replaces the reference video" idea from [V4-MP], generalised into a library (report §10 item 3, skill `examleaf-style-guides`).

**Evidence labels.** [V#]/[N#] are cited from `12_advanced_animations_with_claude/01_research/RESEARCH_REPORT_advanced_animations_with_claude.md`. [Recommendation] = design judgement. [Hypothesis] = plausible, untested. "verify" = could not be confirmed. Edge cases are #1-#65 (report §8). Project decisions are RD-xx (`07_end_to_end_pipeline_instructions/10_DECISIONS_and_CONFLICT_RESOLUTIONS.md`). Nothing in this folder has been installed, run or validated on real phones.

## 1. The five styles

| Style ID | File | Source | Best for | Credits | Indic coverage |
|---|---|---|---|---|---|
| `doodle-handdrawn` | `doodle-handdrawn.md` | [V2] doodle; report §4.2 | **Default for Reels** [Recommendation]; hooks, analogies, recaps | zero | Kalam Devanagari claimed (verify); Assamese via Noto Sans Bengali |
| `paper-collage-vertical` | `paper-collage-vertical.md` | [V4-MP] adapted to 9:16 | Story, history-of-science, analogy and recap scenes that need painted charm | zero (tier A/B); tier C credit-bearing and gated | Latin display fonts only; Indic uses word strips and Noto fonts |
| `editorial-vox` | `editorial-vox.md` | [V3] | Comparisons and scale stories driven by validated numbers | zero (own/licensed assets) | Noto Serif/Sans Devanagari and Bengali (verify) |
| `kinetic-type` | `kinetic-type.md` | [V3]; [N50]-[N55], [N60] | Text-only hooks, key-term pops, labels, CTAs | zero | Per word; Noto and candidate Indic display faces (verify) |
| `voxel-isometric` | `voxel-isometric.md` | Report §4.5; [V1]; [V5] (unverified) | Cubic lattices, stylised organelles, concept islands | zero (render-box time) | DOM labels in Noto fonts |
| (tokens) | `style_tokens.json` | All of the above | Machine-readable palette, fonts, motion, sizes, loudness, determinism and forbidden flags | n/a | `fonts_registry` with coverage flags |

Each guide opens with a **Digest** (about ten lines) that a brief can carry verbatim; the full guide governs if they differ.

## 2. How a style is selected

**Rule 0: styles apply to illustrative and narrative scenes only.** `examleaf-storyboard-route` tags every scene first. A `data-bound` scene (axes, values, equations, structures, labelled diagrams) is NOT drawn in any of these styles; it is built from validated fixtures by `examleaf-svg-scenes`, `examleaf-manim-scenes`, `examleaf-molecule-scenes` or `examleaf-biology-scenes`. A `spatial-hero` scene goes to `examleaf-blender-scenes`. The styles may only frame a fixture panel (a mixed scene), and the framed element is never wobbled, boiled, drifted or push-in'd (#12, #64). The accuracy invariant: any glyph that encodes science is traceable to a fixture field (report §9).

**Decision table** (route tag `illustrative/narrative` or `typographic`):

| If the scene's job is... | Use | Why |
|---|---|---|
| A Reel hook, analogy or recap with no special need | `doodle-handdrawn` | Cheapest, deterministic, no image-model risk |
| A story, a history-of-science beat or a warm analogy where painted charm matters | `paper-collage-vertical` | Richest look; credit-heavy if cutouts are generated ([V4]) |
| "See the ratio": matched cases, a tenfold step, orders of magnitude | `editorial-vox` | Number callouts and matched frames |
| Putting 1-3 words on screen as the hook, a key term, a condition tag or a CTA | `kinetic-type` | Timed straight from the cue sheet |
| A cubic lattice, a stylised organelle block, a concept island | `voxel-isometric` | Needs a 3D-ish structure; fixture grid |
| An exam-critical graph, equation or structure | none of these | Data-bound: SVG/Manim/molecule/biology skills |

**Tie-breakers.** (1) Zero-credit styles first. (2) One illustrative style per lesson; at most two per Reel [Recommendation], with a clear cut between them. (3) Locale: Indic scenes need verified fonts (§6). (4) Render box: voxel inserts need the pinned WebGL box (#65). (5) The style is part of the storyboard approval; changing it later invalidates the approval and re-opens the gate (#47).

**Not offered.** Style-morph montages (the [V5] demos) are unverified and rarely useful for teaching (report §4.7). Photoreal and cinematic styles are out of scope (#52).

## 3. Versioning

- Each guide and `style_tokens.json` carry a semantic version. The brief names `style_id@version`.
- **Patch** (1.0.1): wording fixes, no change to any rendered value. **Minor** (1.1.0): a new optional rule or token. **Major** (2.0.0): anything that changes how an existing scene renders, such as a palette, size, safe-zone share, timing, or font change.
- A **major** change invalidates approvals made under the old value (the runbook's rule that a decision touching layout invalidates approvals, `10_DECISIONS_and_CONFLICT_RESOLUTIONS.md`). Re-run the storyboard gate for affected scenes.
- A guide and its entry in `style_tokens.json` change together. A mismatch is a bug in the JSON; fix it and bump the version.
- The brief records the SHA-256 of the guide file and the token file it used, so any scene can be rebuilt from the exact style.
- Each guide ends with a changelog. Current versions: all `1.0.0`.

## 4. How a style guide is pasted into a brief

The brief assembler (`examleaf-anim-brief`) fills the style section from the job's `style.*` and `fonts.*` fields:

1. **Reference** (always): style ID and version (`{{style_id}}@{{style_version}}` in the brief), the guide path (`style_guide_path`), and, in the job manifest, the SHA-256 of the guide file and of `style_tokens.json`.
2. **Fonts** (always): `fonts_allow` and `fonts_ban`, computed from the tokens:
   - `fonts_allow` = the font IDs under `styles[id].fonts.primary`, `.secondary`, `.handwriting` and `.science_text`, plus the `indic_fallback` entries for the lesson language, mapped to family names through `fonts_registry`.
   - `fonts_ban` = `common.font_policy.ban_as_display` plus `styles[id].fonts.ban_as_display`.
3. **Digest** (see below).

The full guide is staged read-only in the job workspace; the agent may read it but never edit it. The brief tells the agent to read the guide's **Digest** (about ten lines, at the top of every guide) first and then the body. The body governs if they differ. If the brief and the guide conflict, the stricter rule wins and the agent returns a blocker rather than guessing.

**Digest pasting (integration note).** The current brief helper has no digest field, so the brief references the guide by path and relies on the digest being the first thing the agent reads. If the assembler gains a `style_digest` field, it should paste the digest verbatim near the top of the prompt in a fixed order, because stable context placed first is cache-friendly (report §3.3; the [V1] caching observation). Until then, `master_prompt_paper_collage_VERTICAL.md` shows the paste form.

Minimal paste block:

```text
## Style: doodle-handdrawn@1.0.0
Guide (read-only): 12_advanced_animations_with_claude/05_style_guides/doodle-handdrawn.md  sha256 <hash>
Tokens (read-only): 12_advanced_animations_with_claude/05_style_guides/style_tokens.json  sha256 <hash>
  section: styles["doodle-handdrawn"]; common.* applies to every style
Digest: <the guide's "Digest" text, verbatim>
Fonts allow: <names>   Fonts ban: <names>
```

The filled examples are in `06_prompts_and_templates/prompt_*.md`.

## 5. Safe zones and sizes (shared by all five styles)

- **Canvas:** 1080×1920 at 30 fps (vertical-only decision of 15 Oct 2026, RD-16 superseded; AD-07). Never a crop of a 16:9 composition (#49).
- **Safe box:** insets come only from `12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json`. These guides store no inset values on purpose: exact platform pixel values are not in the verified evidence (report §7.9, §11 item 9). If that file is missing, the brief assembler blocks the brief. While its `platform_insets_px.measured` is false, the insets named by `applies_until_measured` (currently generic conservative PLACEHOLDERS) apply and the job manifest records them as provisional; measured values replace them and re-open the layout approvals of affected scenes.
- **Stacked zones** inside the safe box [Recommendation]: title 22%, visual 54%, caption 24% of the usable band between the top and bottom insets; these mirror `zones.*.share` in the token file, and the file wins. Side margin at least 96 px (larger than [V4-MP]'s 90 px). A three-row title (3 rows of 96-148 px type or tiles) does not fit in 22%, so the title zone may grow to 30%, taking space from the visual zone and never from the caption zone.
- **Text sizes at 1080 wide** (RD-01, RD-18; `Displayed = Source × 360/1080`): essential labels and captions 50-54 px; equations 63-81 px; headings 59-72 px; secondary non-essential floor 36-40 px.

## 6. Indic font policy (summary)

Locale gate: en-IN only until the W3 medium decision (RD-26). The Hindi, Hinglish and Assamese rules are written now and activate when the gate passes. Language drafts need native-speaker and subject review (ROOT/03 §5.5).

| Rule | Policy |
|---|---|
| Fonts | Noto Sans/Serif Devanagari for Hindi; Noto Sans/Serif Bengali for Assamese (Bengali-Assamese script; verify ৰ U+09F0 and ৱ U+09F1). Latin display faces named in [V4-MP] are Latin only. Candidate Devanagari display and handwriting faces (Rozha One, Yatra One, Baloo 2, Kalam) are "verify" |
| Coverage | A font passes only after the glyph smoke test (`क्ष ज्ञ श्र द्ध विद्युत प्रतिरोध`; `ৰ ৱ ক্ষ জ্ঞ অসম`). Never trust a family name |
| Vendoring | Vendored, SHA-256 hashed into the cache key, licence recorded (all licences currently "verify"); no CDN at render time (RD-23) |
| Animation unit | Per word or per grapheme cluster, never per code point (#55). Treat `Intl.Segmenter` grapheme handling of Indic conjuncts as [Hypothesis] until tested in the pinned Chrome |
| Typesetting | No `letter-spacing`, no `text-transform`, ligatures on, real bold weights (no synthetic bold/italic); line height at least 1.4 [Hypothesis] |
| Mixed script | Hindi captions in Devanagari with technical terms in Latin script; one `lang` per run; never mix scripts inside a word; science digits in Latin unless the approved edition says otherwise |
| Holds | Latin headline at least 1.2 s [N60]; Indic ×1.5 [Hypothesis] |
| Test | End-state equality: the last frame of an animated word must be pixel-identical to the static render of that word |
| Captions | From the original script and the same alignment as the cue sheet, never from pronunciation respellings |

## 7. Edge cases covered

| # | Edge case | Handled in |
|---|---|---|
| 7 | One-line prompt | Digest in every guide (§4); brief template |
| 8 | Generic look | Named fonts and palettes in every guide; font ban list; rotation [N55] |
| 9 | Context contamination | Forbidden lists in each guide; brief isolation (`06_prompts_and_templates/`) |
| 10 | Missing audio | Sound sections in each guide; `examleaf-audio-compose` |
| 11 | Weak or agent-written script | Writing sections; script ownership statement in each guide |
| 12 | Hallucinated facts on screen | Rule 0 (§2), fixture-bound rules in every guide |
| 48 | Character drift | Collage §4 (hero sheet, reference attached); doodle has no generated characters |
| 49 | 16:9 guide in a 9:16 pipeline | Collage §7, all guides §layout; no crop |
| 50 | Short headline hold | Hold rules in every guide; `style_tokens.json` `common.holds` |
| 51 | Platform UI overlap / caption clash | Safe-box rules (§5); caption interplay in `kinetic-type.md` §9 |
| 52 | Photoreal request | "Not offered" (§2) |
| 53 | Parser expects a fenced block | Brief template output format section |
| 54 | Image model draws text | Collage §12; forbidden lists; code-built text everywhere |
| 55 | Indic glyph gaps / per-code-point animation | §6; collage §13; kinetic §8 |
| 56 | Photosensitive flashes | Collage §9 (flash replaced), motion sections, QA lists |
| 60 | "Don't stop until perfect" | Forbidden lists; iteration cap in the brief template |
| also | #15-#19 determinism, #39 loudness, #41-#42 credits, #47 gate, #63 cue sheet, #64 camera fx, #65 headless WebGL | Collage §15, §11.3, §12; voxel §7 |

## 8. Dependencies on other parts of the section

| Needed | Expected path | Status at time of writing |
|---|---|---|
| Safe-zone tokens | `12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json` | Exists (token version 1.0.0). Zone shares mirrored here; platform insets are the file's own PLACEHOLDERS (`measured` false) and are not copied |
| Harness contract, linter, cue-sheet schema and validator, scene template | `.../04_harness_contract/contract.md`, `lint_seek_contract.js`, `cue_sheet.schema.json`, `validate_cue_sheet.py`, `scene_template.html` | Exist (contract 1.0.0). The style guides defer to them on every conflict |
| Cue sheet shape | `.../04_harness_contract/cue_sheet.schema.json` | Authoritative; the filled examples in `06_prompts_and_templates/` conform to it |
| Skills | `.../03_skills/examleaf-style-guides`, `examleaf-anim-brief`, `examleaf-kinetic-typography`, `examleaf-procedural-2d`, `examleaf-threejs-scenes` | In progress by others; names as in report §10 |
| Prompt templates | `.../06_prompts_and_templates/` | Written alongside this folder |

## 9. Conflicts with existing tokens and rules (and how each is resolved)

| # | Conflict | Resolution |
|---|---|---|
| C1 | Typography ranges: message-04 (88-96 / 112-144 / 104-128 at 1920) versus planning pack (64-72 / 84-112 / 72-88) | RD-01 picks message-04; scaled by 0.5625 for 1080 wide (RD-18). Planning-pack values are a floor for secondary text only |
| C2 | Loudness: [V4-MP] -14 LUFS / -1.5 dBFS versus house -16 LUFS / -1 dBTP. The harness tokens (`vertical_safe_zones.tokens.json` `audio.loudness_conflict`) leave this open | This folder resolves it to the house target (-16 LUFS, -1 dBTP), which matches the narration system; record it in the pilot sheet |
| C3 | Edge margin: [V4-MP] 90 px versus planning-pack 96 px and the safe-zone file | Larger wins; at least 96 px |
| C4 | [V4-MP] "never frozen, idle on everything" versus ROOT/02 E3 "decorative change: avoid" and the reduced-motion need | Finite idle only on decorative characters in hook/analogy/recap; off in holds, `think`, fixture panels and reduced motion |
| C5 | [V4-MP] 0.5-0.7 s sheet transitions versus ROOT/02 150-300 ms simple transitions | Classified: sheets are scene-level; element transitions stay 150-300 ms |
| C6 | [V4-MP] white flash or bloom versus #56 | Forbidden; localised paper burst instead |
| C7 | ROOT/02 and RD-23 use Inter; [N51] says avoid Inter | Inter allowed for labels and captions, banned as a display face |
| C8 | Equation hold: message-04 2-4 s versus planning pack 1-3 s | RD-02: 2-4 s, longer when necessary |
| C9 | ExamLeaf teal `#087986` is 4.37:1 on cream `#f3ecdf` (below 4.5) | Science labels sit on `#F7F9FC` tags |
| C10 | ROOT/02 has no green; subject colours are not defined | Biology green `#1F7A3E` is a proposed new token (5.09:1), pending brand-owner approval |
| C11 | [V4-MP] number tags drawn on the storyboard grid | Added in code; image models never draw text (#54) |
| C12 | [V4-MP] "dark red" tile letters is not in the 13-colour palette | Use ExamLeaf red `#B42318` (3.42:1 on blush; display only) |
| C13 | Five delivery modes in the Super Teacher framework versus six in RD-12 | Five plus FOCUSED (exam strategy) |
| C14 | [V4-MP] crying and cheering poses | Replaced with puzzled/thinking and a capability-tied quiet-win pose (anxiety safeguards, no fake enthusiasm) |
| C15 | Zone shares are defined by the harness tokens (22 / 54 / 24) | The style guides mirror them and defer to the file; a three-row title may grow the title zone to 30% |
| C16 | Reveal timing: "about 0.05 s before" ([V4-MP]) versus the cue-sheet validator | A reveal cue `at` is in `[t0 - 0.05, t0]`; the validator rejects later and warns above 0.10 s early; the entrance may run on for about 0.30 s |
| C17 | Hold for longer copy: no source formula | Use the harness tokens' `max(headline_min, 0.3 s × word_count)` |
| C18 | Subject colours: the harness tokens say "NOT DEFINED in the sources, assign in examleaf-style-guides" | Assigned here (physics blue, chemistry teal, mathematics purple, biology green `#1F7A3E` proposed); mirror them into the harness tokens when approved |

## 10. Verify list (not confirmed by evidence)

Font licences and glyph coverage (every font); Assamese letters ৰ ৱ in Noto Sans/Serif Bengali; a handwriting font for Assamese; `Intl.Segmenter` on Indic conjuncts; the WCAG large-text definition used for display pairs; whether HyperFrames bundles GSAP or seeks the Web Animations timeline; tabular-figure support per font; the Higgsfield model ID `gpt_image_2_5` and its options, per-generation credit costs and aspect-ratio support; the software-GL flag for the pinned Chrome; platform safe-zone pixel values; the biology green token; phone legibility of every size in this folder.

## 11. Files

`README.md`, `paper-collage-vertical.md`, `doodle-handdrawn.md`, `editorial-vox.md`, `kinetic-type.md`, `voxel-isometric.md`, `style_tokens.json`.

## 12. Fonts are not vendored yet (16 Oct 2026)

The pilot builds (`16_pilot_builds_2026-10-16/COMPARISON_and_GAPS.md` §1 L-09) found none of the guides' display faces installed or shipped: Kalam/Caveat for `doodle-handdrawn`, Noto Serif/Georgia for `editorial-vox`, the ransom-tile display faces and Patrick Hand for `paper-collage-vertical`, the display allow-list for `kinetic-type`, and the Noto Indic families everywhere. Each guide's display face MUST ship as local `@font-face` files next to the harness (licence and SHA-256 recorded; contract §6) before any production render. Until then the system stack is the pilot fallback, and frames rendered with it are not comparable across machines (or with a later vendored render). Tracked as a P1 build item in `07_end_to_end_pipeline_instructions/02_PHASED_BUILD_ROADMAP.md`.
