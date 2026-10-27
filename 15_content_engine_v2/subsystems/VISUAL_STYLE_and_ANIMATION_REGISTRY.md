# Visual Style and Animation Registry (Content Engine v2 subsystem)

Status: subsystem specification, 15 Oct 2026. Nothing here has run or been phone-tested. Parent: `../ARCHITECTURE_content_engine_v2.md` §3.1, §3.4 (R4, R8), §3.6, §5, §9.3. Schema: `schemas/style_entry.schema.json`. Template: `templates/style_entry.template.md`. Siblings: `QA_PROFILES_REGISTRY.md` and `PACKAGING_and_DISTRIBUTION_REGISTRY.md`.

**Tags.** **[Recommendation]** is a design choice made here. **[Hypothesis]** needs an owner and a pilot. "verify" means not confirmed by any evidence. **Cal** means calibrate in pilot (a Hypothesis).

**Citations.** [N#] = `../SOURCES_and_claims.md`; [12:N#] = `12_advanced_animations_with_claude/01_research/SOURCES_and_claims.md`; [V#] and [V4-MP] = the 12 references; #n and NEW-n = 12/02 doc 12 edge cases. 12/05 = `.../05_style_guides/`, 12/04 = `.../04_harness_contract/`, and 02 §X = `02_learning_psychology/INSTRUCTIONS_production_rules.md`.

---

## 0. Summary

A **style entry** is a versioned, hash-bound registry record that says how an artefact *looks and moves*, never what it says. The five existing vertical styles become `style/doodle-handdrawn`, `style/paper-collage`, `style/editorial-vox`, `style/kinetic-type` and `style/voxel-isometric`. Four are new:

- `style/whiteboard-science`, the data-bound science layer (absorbing 12's `base-science`);
- `style/lecture-slides`, UG/PG and educator; the only illustrative or hybrid style that supports 16:9 (F20), once version 1.1.0 adds that aspect after O-19 (§5; matches CE-72 as corrected 15 Oct 2026);
- `style/storybook-junior`, for `safety/ac0`, derived from paper-collage with stricter motion;
- `style/exam-sheet`.

All of them extend `style/base@1.0.0` and bind existing 12 and 02 token files by pointer and hash. Values are not copied. Style has the lowest scalar precedence above persona (R8). A style may tighten any limit, but it may never loosen one or change what a scene asserts.

## 1. What a style entry is

### 1.1 Fields and binding

Files live at `content/registry/style/<id>@<semver>.json` and are validated by `style_entry.schema.json` (`additionalProperties: false`; IDs `^style/[a-z0-9_-]+$` as in `format_spec.styles_allowed`). An entry holds:

- **Lineage.** `legacy_style_id` (the 12/05 token key), `extends[]` (always `style/base@1.0.0`) and `layer` (science, expressive or hybrid).
- **Applicability.** Safety classes, levels, formats, aspects with one safe-zone token set each, and route tags.
- **Token bindings.** `{path, json_pointer, sha256}` references into the 02, 12/05 and 12/04 token files. The file hashes are fields of the style entry, so they enter the closure through the style pin inside `epp_hash` (Architecture §3.7 closure manifest M), not as separate closure keys; a token edit is a new style version, which reaches the dependency index (corrected 15 Oct 2026).
- **Motion.** A motion profile with `by_safety_class` overrides, which may only tighten.
- **Slots.** `slot_types_implemented[]`. A Format Plan that gives a slot to a style without its Kit template is a compile error.
- **The rest.** Asset sources, cost class, references, sonic bindings, determinism extras, A-check parameters, forbidden list, edge cases and evidence. A style's `sonic.sfx` must be a subset of its MUSIC §5 row after the level filter (spec-linter rule; 15 Oct 2026).

There are no price or commercial fields. Credit estimates exist only at H-SB, in the ledger.

### 1.2 Two layers and Rule 0

Every element belongs to one of two layers (12/02 doc 08 §2).

- **Science layer.** Labels, values, units, axes, equations, structures, map boundaries and timeline dates. The text comes **only** from fixture fields or, for claim-ledger families, from approved node fields.
  - Each glyph carries a typed `data-fx` [Recommendation, generalising 12/04 contract §9]: `fixture:<FX-id>#<json.path>` or `node:<CLM|MED|TXT-id>#<field>`. The `#` separates the id from the path, as in `examleaf-anim-qa/scripts/text_fixture_diff.py`, because node ids may contain "." (corrected 15 Oct 2026; the 12/04 harness does not yet read this form, see §14 item 12).
  - An untraceable science glyph is a Critical A7 failure (12/10 §5).
- **Expressive layer.** Titles, punchlines, tags, characters and transitions. The text comes from the approved script or string tables (CE-39).

**Rule 0** (12/05 README §2). A `data-bound` scene is never drawn in an illustrative style; it resolves to `style/whiteboard-science`. An illustrative style may *frame* a fixture panel, but it never wobbles, boils, drifts or pushes in on it (#12, #64, NEW-28). "4 V" in a tilted ransom tile is still science (12/02 doc 08 §2).

R4 requires the style to support the format's aspect and the EPP safety class. Changes to a style are in the Presentational class (Architecture §3.6), refined in §11.

## 2. Shared limits by safety class

These sit in `style/base`. A style's `by_safety_class` block may only tighten them. Values marked Cal belong to the child-development reviewer (O-2) and stay report-only until signed (CE-35).

### 2.1 Flash and luminance

| Rule | `safety/ac0` | `safety/ac1`, `safety/ac2` |
|---|---|---|
| Policy | `ac0_zero_flash` (CE-21): zero general or red flashes, with the area threshold removed, per tile. A 10×10 grid runs report-only until O-2 signs the grid and a per-tile luminance-rate limit [Hypothesis]. Release is gated on O-1 and O-2. | `wcag_2_3_1` floor; thresholds await S-1/O-1 |
| Full-frame flash or bloom | Forbidden (Critical) | Forbidden (house rule; #56) |
| Flashes per second | 0 | At most 3 (12/04 `flash_policy`, verify) |
| Whole-frame luminance step | Within the signed `motion.max_visual_change_rate` | No full-frame mean change greater than 20% of range in 0.25 s [Hypothesis] (12/05 collage) |
| Dark mood sheets | Forbidden | Mood only, with no science text, pending AD-17; otherwise light theme (RD-27) |
| Spatial pattern (house rule) [Hypothesis; owner production QA; ac0 values signed under O-2] (added 15 Oct 2026) | No regular stripe, grid or checker pattern with more than five light–dark pairs covering more than 25% of the frame may move, flicker, oscillate or reverse; a static one needs a human check | Same, reviewed at ac1/ac2. Source to register with O-1 (ITU-R BT.1702 or Ofcom guidance), verify. Checked as Q-FLASH.pattern (§10 A6) |

### 2.2 Motion verbs

| Verb | ac0 | ac1 / ac2 |
|---|---|---|
| Boil (8–10 fps) | Off until O-2; then at most 8 fps, decorative outlines only [Hypothesis] | Decorative strokes only; never on text, fixtures or in reduced motion |
| Idle (1.5–4°, finite) | Hook and recap characters, at most 1.5° [Hypothesis] | Hook, analogy and recap; off in holds, think windows and fixture panels |
| Shake, whip, push-in, drift, orbit, fixture rotation (fixture rotation added 15 Oct 2026) | Forbidden | Per style limits; never during science reveals (A14) |
| Pop overshoot | At most 1.4 | Per style (1.4–3); science labels never overshoot |
| Count-up | Forbidden | At most 0.8 s, non-exam-critical, ending on the fixture string |
| Reduced-motion variant | Always | Always |
| Reduced-motion variant content (`style/base`, all classes; added 15 Oct 2026) [Recommendation] | Disables boil, idle, wiggle, parallax_drift, push_in, pan, zoom, orbit, shake, whip, paper_burst, somber_drop, count_up (shows the final fixture string) and sheet_slide (becomes a 150–300 ms cross-dissolve). Other reveals become 150–300 ms fades. equation_transform and fixture-driven motion stay as essential motion; a rotation sweep shows its end pose. Holds, think windows and reveal times are unchanged | Same |

**Schema enforcement (15 Oct 2026).** `style_entry.schema.json` enforces the ac0 column for every style that allows `safety/ac0`: `verbs_forbidden` must contain shake, whip, push_in, parallax_drift, orbit, boil (until O-2), count_up, paper_burst and fixture_rotate, with `pop_overshoot_max` ≤ 1.4 and `idle_rotation_deg_max` ≤ 1.5 required, and `flash.policy_by_class` must list `safety/ac0`. It also requires every `reduced_motion.verbs_disabled` to contain the fourteen verbs above. When O-2 signs boil for ac0, the boil item is dropped in a minor schema version (Safety class).

### 2.3 Durations and holds

| Item | Value | Source and tag |
|---|---|---|
| Element transition / highlight / equation transform | 150–300 ms / 300–600 ms / 0.8–1.5 s | 02 §E4 (production hypotheses) |
| Paper sheet | 0.5–0.7 s, starting at least 0.3 s after the last word; somber 0.9 s | [V4-MP]; 12/04 `motion` |
| Reveal sync | `at` within [t0 − 0.05 s, t0]; settles within 0.3 s | 12/05 `common.sync` |
| Headline hold | `m_script × m_level × max(1.2, 0.3 × words)` | 1.2 s [12:N60] is an example figure; 0.3 s per word [Hypothesis]; applying the multiplier to the per-word floor is [Recommendation] |
| `m_script` | Latin 1.0; Devanagari and Bengali-Assamese 1.5 (1.8 s); Latin-script Hinglish 1.0 Cal | 12/04 `hold_times_s` [Hypothesis] |
| `m_level` | l1_2–l6_8: Cal ≥ 1.0; l9_10 and above: 1.0 | LEVEL_PROFILES (`hold_level_multiplier`), CE-62. A style may only add `hold_extra_multiplier` (≥ 1.0, per safety class) on top (corrected 15 Oct 2026; the style schema formerly held `hold_level_multiplier` per safety class, which cannot separate l6_8 from l9_10) |
| Equation | Until `max(t_end + 0.5 s, transform_end + 2.0 s)` | 12/02 doc 08 §6; RD-02 |
| Completed transformation or diagram | 2–4 s, longer when necessary | RD-02 |
| Prediction prompt | The whole think window: default 6 s, range 5–8 s; answer hidden; no motion; SFX muted | RD-11 |

## 3. Style entries

### 3.0 Applicability at a glance

Formats per style are listed in the §4.2 matrix, which is the single source; the spec linter compares both sides. `ac0` = `safety/ac0`, and so on.

**Token bindings.** Legacy styles bind `12/05/style_tokens.json#/styles/<legacy key>` and `#/common`. New styles bind `#/common` and keep their own values in the entry until the 12/05 owner adds `#/styles/<id>` blocks in token release 1.1.0 [Recommendation].

| Style (legacy 12/05 key) | Layer | Safety classes | Levels | Aspects | Credit cost |
|---|---|---|---|---|---|
| `style/base@1.0.0` (root, not selectable) | — | — | — | — | — |
| `style/whiteboard-science` (12 brief `base-science`) | science | ac0, ac1, ac2 | all ten | 9x16 (1.0.0); 16x9 added in 1.1.0 when the O-19 token set is approved (F20 only) | 0, code |
| `style/doodle-handdrawn` (`doodle-handdrawn`) | expressive | ac0 (ac0 profile), ac1, ac2 | all ten | 9x16 | 0, CPU |
| `style/paper-collage` (`paper-collage-vertical`) | expressive | ac1, ac2 | l6_8–pg, adult_prof, voc | 9x16 | 0 by default; gated generation is credit-bearing |
| `style/editorial-vox` (`editorial-vox`) | expressive | ac1, ac2 | l6_8–pg, adult_prof, voc | 9x16 | 0 unless gated cut-outs |
| `style/kinetic-type` (`kinetic-type`) | expressive | ac1, ac2 | l6_8–pg, adult_prof, voc, educator | 9x16 | 0 |
| `style/voxel-isometric` (`voxel-isometric`) | expressive + fixture voxels | ac1, ac2 | l6_8–pg, adult_prof, voc | 9x16 | 0; render-box minutes |
| `style/lecture-slides` (new) | hybrid | ac1 (ug), ac2 | ug, pg, adult_prof, educator | 9x16 (1.0.0); 16x9 added in 1.1.0 when the O-19 token set is approved (F20) | 0; Path A studio minutes |
| `style/storybook-junior` (new; extends paper-collage) | expressive | ac0 only | l1_2, l3_5 | 9x16 | 0; child-development minutes |
| `style/exam-sheet` (new) | hybrid | ac1, ac2 | l6_8–pg, adult_prof, voc | 9x16 | 0 |

**Aspect releases (15 Oct 2026).** WS and LS 1.0.0 are released with `aspects_supported` = 9x16 only. Listing 16x9 with `token_status: missing` would keep them in draft (schema: a released 16x9 aspect needs `approved` tokens), which would hold every STEM science scene behind O-19. The 16x9 aspect is added in 1.1.0 (§11).

"Credit cost" is a class, never a price. A credit estimate exists only at H-SB, against the verified pricing source, and is recorded in the ledger (#41, #42; 12/05 tokens `credits_note`). Token and render cost are logged by `examleaf-observability-cost`. Effort comes from the ModelProfile, never from the style.

### 3.1 `style/base@1.0.0`

Built from `02_learning_psychology/palette_and_typography_tokens.json` (Architecture §10) together with `12/05/style_tokens.json#/common` and `12/04/vertical_safe_zones.tokens.json`. It holds:

- **Palette and roles.** The light palette (02 §D2): blue primary explanatory, teal relationship, amber condition only, purple secondary relationship, red error marker only.
- **Contrast floors.** 4.5:1 for text and 3:1 for essential graphics, checked on real frames.
- **Subject accents.** Physics blue, chemistry teal, mathematics purple, biology green `#1F7A3E`. The green is proposed, pending the brand owner (C10). Accents are chrome only and never encode a quantity. [Recommendation] Non-STEM families use secondary `#526074` until accents are assigned through GR.
- **Everything else.** Minimum sizes at 1080 wide (label 50, equation 63, heading 59 px), holds, sync, loudness (−16 LUFS, at most −1 dBTP), music policy (muted under all teaching, including spoken recaps; owned audio only; beds start 20 dB under speech and are allowed in hooks, transitions and outros only; code-composed beds only for Reel hooks, SFX and prototypes; sonic logo core length 1.5–3 s; all owned by `MUSIC_and_SOUND_REGISTRY.md`, which wins on any difference), determinism, font policy, forbidden block and §2.

There is no dark theme (RD-27).

### 3.2 `style/whiteboard-science@1.0.0`

- **Purpose.** The science layer for every data-bound scene or element in any format: graphs, equations, structures, worked steps, maps, timelines and concept-map links. It gives continuous drawn flow on a clean board [N5]. It is the default for Worked Example, Derivation/Proof, Concept Map and virtual Lab/Demo.
- **Bindings.** Base palette, with Inter, Noto Sans script families and KaTeX (RD-23). A quantity keeps its colour for the whole lesson. Lines carry a label and a dash pattern as well as colour (WCAG 1.4.1). Blue/purple and teal/green differ by only 1.05 in luminance (12/05 tokens `contrast.accent_luminance_note`).
- **Motion.** Semantic change only. Appear, draw-on without overshoot, highlight, and equation transforms that preserve symbol correspondence (02 §E5). No camera, idle, boil, shake, push-in or parallax. Layouts may stay still for 20–60 s or longer (02 §E3). At ac0, numbers appear only as counted objects from fixture integers.
  - **Fixture-driven motion (added 15 Oct 2026) [Recommendation].** Where depth or dynamics carry the teaching point (orbitals, lattices, field lines; 12/02 doc 07 §1.2), two verbs are allowed. `fixture_rotate`: an orthographic or fixed-perspective camera, with the start angle and sweep read from fixture fields such as `view.start_deg` and `view.sweep_rad`; frozen during `label_reveal`, `measurement` and `hold`. `fixture_simulate`: a closed-form or fixed-step replay from t = 0 (contract.md §4 Stateless physics; 12/02 doc 07 §2.4). Renderers are SVG/KaTeX, three.js orthographic, and Manim or Blender as frame-indexed PNG sequences with the clip hash in the AssetManifest. Scene rotation under `fixture_rotate` is not a camera move. `fixture_rotate` is forbidden at ac0 (§2.2). WS adds the route tag `spatial-hero` to `route_tags_allowed`. When three.js is used, the §10 A2, A3, A15 and A17 rows apply to WS.
- **Slots.** `explain.ladder_step`, `explain.definition`, `explain.derivation_step`, `worked.step`, `worked.faded_twin`, `check.interpolated`, `check.predict`, `check.retrieval`, `misconception.confront`, `misconception.retest`, `compare.dimension`, `activity.observe`, `exam.pattern`, `marking.scheme`, `map.node`, `map.link`, `source.show`, `recap.statement`, `qa.answer`, `viva.model_answer`.
- **References and edge cases.** 12/02 doc 03 §1.2; the four 04 models; 02 §E1, §E5. Edge cases #12, #50, #64, NEW-19, NEW-28, NEW-30.

### 3.3 `style/doodle-handdrawn@1.0.0`

- **Purpose.** The zero-credit default for hooks, analogies, recaps and Shorts (12/05 README §1 [Recommendation]). The [V2] "flat" critique is fixed by depth rules: at least four layers, parallax 0.25/0.6/1.0/1.4, hatch shadows and a line-weight hierarchy.
- **Bindings.** Fills are subject-accent tints. Labels in Inter or Noto Sans. Titles in Kalam (Latin and Devanagari, verify) or Caveat (Latin). Assamese titles use Noto Sans Bengali with a per-word wipe. Titles are at most 3 words, 96–140 px.
- **Motion.** Draw-on at 1,100 px/s (0.25–1.2 s). Pop `back.out(1.7)` over 0.3–0.4 s. Underline 0.3–0.4 s. Finite wiggle of 2°. Boil at 10 fps, 0.8–1.5 px. A seeded static pencil texture, never on captions or fixture panels. At ac0, boil is off until O-2 and there is no drift.
- **Slots.** `hook.realworld`, `hook.surprise`, `hook.question_reveal`, `explain.analogy`, `misconception.elicit`, `recap.statement`, `recap.retrieval`, `close.next_step`, `story.beat`, `bridge.return_link`, `qa.doubt_statement`, `activity.setup`, `activity.safety_cue`, `activity.do` (framing MED), `teach.move`, `chapter.title`.
- **References and edge cases.** `12/05/doodle-handdrawn.md` with SHA-256; `prompt_doodle_reel.md`; a reference clip or 3–5 stills. Edge cases #8, #17–#19, #49–#51, #54–#56, #63, #64.

### 3.4 `style/paper-collage@1.0.0`

- **Purpose.** Painted charm for stories, history-of-science beats, warm analogies and recap endings, never the core worked explanation (12/02 doc 03 §2.1). It is the default for Story/History at l6_8 and above.
- **Bindings.**
  - The 13-colour storybook palette for artwork. Science text sits on base-token `#F7F9FC` tags, because teal on cream is only 4.37:1 (C9).
  - Ransom pairs below 4.5:1 (cream on tomato 3.62, mustard on ultramarine 3.48, ultramarine on blush 3.89) are display-only (NEW-31).
  - Ransom fonts are Latin only. Indic uses Noto word strips, one tile per word, at 3°.
- **Motion.** Pop `back.out(2–3)` at the feet. Sheets power3.out over 0.5–0.7 s. Boil 8–10 fps, uneven cadence. Push-in 1.03–1.04, shake at most 3 steps, whip 0.4 s. No exit animations. A paper burst over at least 0.5 s replaces the white flash. Reduced motion uses a 150–300 ms cross-dissolve.
- **Assets.** `asset_sources_allowed` replaces the old Tier A/B/C:
  - `code_only` (the default);
  - `owned_or_licensed`;
  - `generated_gated`, only after H-SB approves an estimate, through `examleaf-mcp-orchestrator`, with OCR proving there is no text (#54).
  
  A hero sheet with SHA-256 keeps characters consistent (#48). No faces on atoms or cells in explanations, no causal faces on objects, no crying poses, and no stereotypes (collage §4, §14).
- **Slots.** `hook.realworld`, `hook.surprise`, `explain.analogy`, `story.beat`, `misconception.elicit`, `recap.statement`, `recap.retrieval`, `close.next_step`, `bridge.return_link`, `chapter.title`, `source.show`.
- **References and edge cases.** `12/05/paper-collage-vertical.md`; `master_prompt_paper_collage_VERTICAL.md`; a 3×3 grid of 9:16 panels; the hero sheet. Edge cases #41, #42, #47–#49, #54–#56, #64.

### 3.5 `style/editorial-vox@1.0.0`

- **Purpose.** Comparisons and scale stories built from validated numbers; also source analysis, perspectives and history at l6_8 and above (F14). It is the default for Comparison, Source Analysis and Perspectives.
- **Bindings.** Base palette, with 22–28% highlighter tints and amber for conditions only. Noto Serif headlines (Devanagari and Bengali variants). Tabular numerals (verify per font). Callouts are 160–240 px.
- **Layout.** A over B in matched frames (each 40–46% of the visual zone), or a log ladder above three orders of magnitude.
- **Motion.** One staggered entrance per beat [12:N53] (60–90 ms stagger). Slide 0.3–0.5 s. Highlighter 0.35–0.5 s, at most 2 passes. Push-in 1.05–1.08, never while a number is revealed. No whip pans.
- **Integrity.** Sizes and positions are a pure function of fixture values. The encoding note ("area-proportional", "not to scale") comes from the fixture or brief. Ratios such as "tenfold" are fixture fields.
- **Assets.** Owned or recorded-licence images only. No outlet branding. Maps only as approved MED assets.
- **Slots.** `compare.dimension`, `hook.question_reveal`, `hook.realworld`, `source.show`, `source.read`, `source.interpret`, `perspective.position`, `exam.pattern`, `explain.analogy`, `recap.statement`, `chapter.title`.
- **References and edge cases.** `12/05/editorial-vox.md`; a [V3] clip for pacing only. Edge cases #11, #12, #49, #50, #54, #64.

### 3.6 `style/kinetic-type@1.0.0`

- **Purpose.** 1–3 key words timed from the cue sheet's `words[]`: hook questions, term pops, chapter titles, card faces, read-along highlighting and the next-step line. It is the default for Recap and Series bridges at l6_8 and above, and for Read-Along at l6_8.
- **Bindings.** Ink and paper dominant, at most two accents [12:N52], one keyword highlighted at a time. Allow-listed display faces, rotated between Reels. Arial, Helvetica, Roboto, system-ui, Space Grotesk and Inter are banned as display [12:N51][12:N55]. At most 6 words and 3 lines.
- **Modes.** Ransom (Latin per letter at 0.04–0.05 s; Indic per word tile). Handwriting (Indic word mask of at most 0.6 s). Label (at most 4 words, pop 0.25–0.3 s).
- **Rules.** Captions stay static in the caption zone while kinetic text moves. Kinetic text never replaces captions, and there are no karaoke captions. Equations never become kinetic text. Displayed tokens must exist in the approved bundle.
- **Slots.** `hook.question_reveal`, `hook.surprise`, `explain.definition` (term pop; the text is the approved claim), `card.front`, `card.back`, `recap.statement`, `chapter.title`, `close.next_step`, `bridge.return_link`, `source.read`, `viva.prompt`, `qa.doubt_statement`.
- **References and edge cases.** `12/05/kinetic-type.md`; 12/02 doc 08. Edge cases #8, #50, #51, #55, #63, NEW-1, NEW-3, NEW-18. The legacy route tag `cta` is renamed `next-step` [Recommendation].

### 3.7 `style/voxel-isometric@1.0.0`

- **Purpose.** Cubic lattices, stylised organelle maps and concept-island recaps. Never for bond angles, molecular geometry, field lines, simulations, or anything where angle or proportion carries the science. [Recommendation] Excluded from ac0, because of orbit motion and WebGL variance (#65).
- **Technique.** Orthographic camera at 45° azimuth and 35.264° elevation. Baked face multipliers 1.0/0.8/0.62; no lights, shadow maps or post-processing. Fixture-grid voxels. DOM labels from fixture strings, projected at time t within 4 px. A legend; red and amber are never species colours.
- **Motion.** Build-up `back.out(1.4)` with 30–60 ms layer stagger. Orbit at most 45°. Zoom 1.0–1.15. At least 2 s dwell on a labelled view. No camera movement during label reveal.
- **Slots.** `explain.ladder_step` (insert), `recap.statement`, `map.node`, `map.link`, `compare.dimension`.
- **References and edge cases.** `12/05/voxel-isometric.md`; `prompt_voxel_insert.md`. Edge cases #15, #17, #57, #64, #65, NEW-15, NEW-21, NEW-22.

### 3.8 `style/lecture-slides@1.0.0` (new)

- **Purpose.** Slides or a board interleaved with an instructor head at transitions. Talking head interspersed with slides beats slides alone [N4]; derivations are drawn [N5]. Chapters stay at most 360 s even in long lectures [N3][N31]. It is the default for Lecture Segment (the only 16:9 format) and Teacher Explainer (9:16).
- **Bindings.** Base palette on a slide card. At 16:9 the type sizes are the 02 §D6 values on the 1920×1080 master: labels 88–96, equations 112–144, headings 104–128 px (RD-01), under the same 360 px test (02 §D5). Dense notation, with every symbol defined before use.
- **Motion.** Hard cuts or 150–300 ms slides. Data panels follow §3.2. No camera effects.
- **Talking head.** An instructor MED with a release, imported as frame-indexed PNGs or as one video element on one worker (C14, #20). Head cutaways run only over Path A audio. [Recommendation] Teacher Explainer (Path B) uses none, which avoids the "real teacher over synthetic voice" case (11 Playbook Step 14).
- **Slots.** `chapter.title`, `explain.ladder_step`, `explain.definition`, `explain.derivation_step`, `worked.step`, `check.interpolated`, `check.predict`, `perspective.position`, `source.show`, `source.interpret`, `teach.move`, `viva.prompt`, `viva.model_answer`, `recap.statement`, `close.next_step`.
- **References and edge cases.** F20; the planning-pack 16:9 tokens (12/02 doc 03 §3.1). Edge cases #20, #49, #51, NEW-19; depends on O-19.

### 3.9 `style/storybook-junior@1.0.0` (new; `extends: style/paper-collage@1.0.0`)

- **Purpose.** Story, song, activity and picture-card visuals for Classes 1–5, supporting play-way and multimodal response (say-aloud, point, move, draw, sing [N9][N10]). It is the ac0 default in every format available at l1_2 or l3_5 (§4.2).
- **Bindings.** Storybook artwork colours on light surfaces only, with text on base-token tags. On-screen text is icons and single words at l1_2 and short phrases at l3_5. Minimum sizes are Cal, never below base. One language per lesson at l1_2 and l3_5 unless the child-development reviewer approves a code-mix pattern (corrected 15 Oct 2026; Resolver R4).
- **Motion (tightened from the parent).** Pop overshoot at most 1.4. Sheets slide at 0.5–0.7 s or cross-dissolve at 150–300 ms. Idle follows §2.2. Boil, shake, whip, push-in, drift, orbit, fixture rotation, count-up, paper burst and somber drop are all off. Flash policy is `ac0_zero_flash`, and holds use `m_level` (Cal).
- **Content.**
  - No generated real-looking children (`real_child_likeness: false`). Characters come from an owned hero sheet, and [Recommendation] `generated_gated` assets are not allowed.
  - No brands or logos. A "with a grown-up" card for activities.
  - No wrong-answer framing (gentle form, CE-42). No countdowns.
  - Owned music only (commissioned, or code-composed where the music registry allows it), never licensed stock (MUSIC_and_SOUND_REGISTRY policy 4, CE-66; O-7 settles song_chant), with the child sonic-logo variant `music/logo-junior` (Architecture §10).
- **Slots.** `story.beat`, `story.song_chant`, `activity.setup`, `activity.do`, `activity.observe`, `activity.safety_cue`, `hook.surprise`, `hook.realworld`, `explain.ladder_step` (SIM text only), `check.retrieval` (say-aloud), `card.front`, `card.back`, `recap.retrieval`, `recap.statement`, `source.read`, `close.next_step`, `bridge.return_link`. Added 15 Oct 2026, so that ac0 formats compile with one illustrative style (§4.1 step 8):
  - `hook.question_reveal`: a picture question with no countdown (F4, F6, F17 at l3_5);
  - `explain.definition`: a picture-word card from VOC or the approved claim (F23);
  - `explain.analogy`: only an ANL permitted at the level (F1, F2, F8);
  - `check.predict`: a say-aloud prediction with the answer hidden (F4, F8, F12, F18);
  - `misconception.elicit`: a gentle "what do you think?", with no wrong framing (CE-42; F1 and the F5 misconception variant at ac0);
  - `chapter.title`: a picture title card (F16 bridges at ac0).

  `worked.step` is not added; WS supplies it as the science layer.
- **References and edge cases.** Collage §4 and §14; F7 (gentle), F14, F23; LEVEL_PROFILES §3.1–3.2. Edge cases #48, #54–#56; depends on O-2, O-7 and O-10.

### 3.10 `style/exam-sheet@1.0.0` (new)

- **Purpose.** A clean exam-paper look. Default for Question Analysis, Revision Sheet, Practice Set, Exam Strategy, Viva Prep and Flashcard Reel at l6_8 and above, and used for the Short `short.trap` variant. Never at ac0, because there is no exam framing at l3_5 (F4).
- **Layout.**
  - The question card and target quantity stay visible through the whole think window (F4, F17).
  - The answer card stays covered until its reveal cue (`meta.answer_protection`).
  - A marks column appears only when `marks_source ∈ {source_paper, official_key}` (CE-31).
  - Past items show board or exam, year and source. Original items show "Original practice question".
  - Pattern tables show the as-of date (F9).
- **Bindings.** Base palette. A trap gets an amber tag plus a shape. There is never a red cross on a learner's answer. KaTeX from fixtures with the display/spoken split (RD-29).
- **Motion.** Static-heavy. Card flip or slide 150–300 ms. No camera, boil or idle. No ticking clocks: `exam.time_plan` is an allocation table (02 §H5; Q-SAFE.no_timers).
- **Slots.** `hook.question_reveal`, `check.predict`, `explain.definition`, `misconception.confront`, `worked.step`, `worked.faded_twin`, `marking.scheme`, `recap.retrieval`, `card.front`, `card.back`, `check.retrieval`, `exam.pattern`, `exam.time_plan`, `viva.prompt`, `viva.model_answer`, `qa.answer`.

**Coverage lint.** All 43 slot types are implemented by at least one style. CI also checks that, for every grammar slot of every format and every safety class that format allows, some style in its `styles_allowed` implements the slot.

**ac0 coverage re-run (15 Oct 2026, by hand against FORMAT_REGISTRY beats and LEVEL_PROFILES §6).** At l1_2 and l3_5 the admissible styles are SJ, DH and WS. With the §3.9 additions, every illustrative slot of F1–F8, F11, F12, F14, F16, F17, F18 and F23 is implemented by SJ alone, and the science slots (`worked.step`, `worked.faded_twin`, `check.interpolated`, `misconception.confront`, `marking.scheme`) by WS, so each format needs at most one illustrative style (§4.1 step 8). Before the additions, F17 (`hook.question_reveal`) and F23 (`explain.definition`) had no admissible style, and F2, F4 and F8 needed DH as a second illustrative style. CI must repeat this check (MATURITY_MODEL_and_ROADMAP §7, P1-04).

## 4. Style selection rules

### 4.1 Resolution (inside `profile-resolver`)

The rule is safety beats level, level beats format, and format beats style (R8). Each step records provenance.

1. Start from the format's `styles_allowed`.
2. Keep the styles whose `safety_classes_allowed` contains the EPP class. The class comes from the level only (R2).
3. Keep the styles whose `levels_allowed` contains the level.
4. Keep the styles whose `aspects_supported` contains the format's aspect (R4). Record that aspect's `token_status` in the EPP as `resolved.aspect_token_status`; the status never filters a style. H-SB refuses an artefact whose status is `missing`. A4 blocks release while the status is `missing` or `placeholder_insets` (QA Profiles §2.5). A11 accepts 1920×1080 only when the Format Spec declares 16:9 and a 16:9 token set exists (CE-69). (Corrected 15 Oct 2026: the step formerly also required the token set to be `approved`, which no set is today, so it removed every style from every format.)
5. Keep the styles whose fonts pass A8a glyph coverage for the locale's script, plus the A8b test card for Indic modes.
6. If `request.style` is set and did not survive steps 1–5, compile error. It is never silently swapped.
7. Otherwise use the Format Spec's `style_defaults` entry whose `levels` contains the level (copied from §4.2; one default per level, added 15 Oct 2026).
8. **Scene rules.**
   - `data-bound` scenes take whiteboard-science, or the science panel of a hybrid style.
   - Long formats use at most one illustrative style; Shorts use at most two, with a clean cut. The science layer does not count (12/05 README).
8a. A grammar slot that the primary illustrative style does not implement is bound to `style/whiteboard-science` when the §4.2 cell for the format is S or D. Otherwise it is a compile error. The Format Plan records `style_ref` per slot instance (15 Oct 2026).
9. ~~**Limits.** Each limit takes the most restrictive value across safety class, level, overlay, format and style. Ordinary scalars follow precedence order.~~ **Limits (R8, word for word with Architecture §3.4 and CE-09; corrected 15 Oct 2026).** (a) A limit is any field its schema marks `"x-kind": "limit"` (maxima such as max_segment_s, flash, motion, bed level and duration ceilings; minima such as hold times, contrast and think windows). A limit takes the most restrictive value across safety class, a11y profile, level, overlay, format, locale and style. A lower entry may tighten a limit but never loosen it. (b) Every other scalar takes the value of the highest entry in the order safety class > a11y profile > level > overlay > format > locale > style > persona. (c) Locale sets only surface fields (R9); persona sets no number (CE-16). Provenance records which entry set or tightened each value. In `style_entry.schema.json` the hold multipliers, class limits, flash policy, boil rates and text-count limits carry `"x-kind": "limit"`.
10. The resolved styles and their token hashes sit in the EPP. ~~A style change after H-SB reopens H-SB (#47).~~ Selecting a different style after H-SB reopens H-SB (#47; RD-46 binds the style). A new version of the same style reopens H-SB only where the layout grid changes; otherwise the approval is re-affirmed (§11; Architecture §3.6) (15 Oct 2026).

### 4.2 Allowed and default styles per format

The columns are DH doodle-handdrawn, PC paper-collage, EV editorial-vox, KT kinetic-type, VI voxel-isometric, WS whiteboard-science, LS lecture-slides, SJ storybook-junior and ES exam-sheet. **D** = default (the band follows in brackets), Y = allowed, S = science layer only, — = not allowed. The level and safety filters of §4.1 still apply: SJ is ac0 only; PC, EV, KT, VI and ES need ac1 or ac2; LS needs ug or above.

| Format | DH | PC | EV | KT | VI | WS | LS | SJ | ES |
|---|---|---|---|---|---|---|---|---|---|
| detailed | D (l6_8+) | Y | Y | Y | Y | S | Y | D (ac0) | — |
| simplified | D (l6_8+) | Y | Y | Y | — | S | Y | D (l3_5) | — |
| recap | Y | Y | — | D (l6_8+) | Y | S | — | D (ac0) | Y |
| question_analysis | Y | — | — | Y | — | S | — | D (l3_5) | D (l6_8+) |
| short | D (ac1/2) | Y | Y | Y | Y | S | — | D (ac0) | Y |
| worked_example | Y | — | — | — | — | D | Y | Y (l3_5) | Y |
| misconception_fix | D (l6_8+) | Y | — | Y | — | S | — | D (gentle) | — |
| concept_intro | D (l6_8+) | Y | Y | Y | Y | S | Y | D (ac0) | — |
| exam_strategy | — | — | Y | Y | — | S | — | — | D |
| revision_sheet | — | — | — | Y | — | S | — | — | D |
| flashcard_reel | Y | — | — | Y | — | S | — | D (ac0) | D (l6_8+) |
| lab_demo | Y | — | — | — | — | D (virtual) | — | D (ac0) | — |
| comparison | Y | — | D | — | Y | S | Y | — | Y |
| story_history | Y | D (l6_8+) | Y | — | — | S | — | D (ac0) | — |
| qa_doubt | D | — | — | Y | — | S | Y | — | Y |
| series (bridges) | members | members | members | D (l6_8+) | members | S | members | D (ac0) | members |
| practice_set | — | — | — | — | — | S | — | D (l3_5) | D (l6_8+) |
| prerequisite_repair | = target | = target | — | Y | — | S | = target | = target (l3_5) | — |
| derivation_proof | — | — | — | — | — | D | Y | — | — |
| lecture_segment | — | — | — | — | — | S (16:9, from WS 1.1.0) | D (from LS 1.1.0) | — | — |
| source_analysis | Y | — | D | Y | — | S | — | — | Y |
| perspectives | — | — | D | Y | — | S | Y | — | — |
| read_along | Y | Y (l6_8) | — | D (l6_8) | — | — | — | D (l1_2, l3_5) | — |
| concept_map | Y | — | — | — | Y | D | — | — | — |
| viva_prep | — | — | — | Y | — | S | Y | — | D |
| teacher_explainer | Y | — | — | Y | — | S | D | — | — |

[Recommendation] Format Spec owners copy each row into `styles_allowed`, and each D cell into a required `style_defaults` array of `{levels: [level ids], style: style_id}` (added 15 Oct 2026, so that §4.1 step 7 has one machine-readable default per level). The spec linter checks that the `levels` sets are disjoint, that their union equals the format's `levels_allowed`, that each style is in `styles_allowed`, and that each style's `levels_allowed` and `safety_classes_allowed` admit every level listed for it. On 15 Oct 2026 the DH default in simplified, misconception_fix and concept_intro was narrowed to l6_8+, because DH and SJ were both unbanded or overlapping defaults at ac0. The spec linter fails if a format's `styles_allowed` and a style's `formats_allowed` disagree, mirroring the level/format matrix rule (LEVEL_PROFILES §6). Lab/Demo real footage is a MED asset with rights, framed by the style, and is not itself a style.

---

## 5. Aspect policy

1. **Vertical default.** 1080×1920 at 30 fps (P6, CE-L7). fps is a contract parameter. 24 fps is used only by the 04 proof fixtures.
2. **Aspect is a Format Spec field.** The schema allows `16x9` only with `1920x1080` and only for ug, pg and adult_prof (CE-46). Only `format/lecture_segment` declares it. A request, style or lesson cannot set aspect.
3. **Style support needs tokens.** A style that lists `16x9` must bind a 16:9 token set, and the schema requires that set to be `approved` before the style is `released`.
4. **The 16:9 token set does not exist yet (O-19).** [Recommendation] Create `12/04/landscape_safe_zones.tokens.json`, seeded from the planning pack (`safe_margin_px` 96, `caption_reserve_bottom_px` 190 at 1920×1080; Inherited) and approved through GR. Player insets stay **measure per platform**. ~~Until then F20 compiles, but it cannot pass H-SB, A4 or A11.~~ Until then no released style lists 16x9, so F20 is a compile error at §4.1 step 4 (corrected 15 Oct 2026).
5. **Recompose, never crop.** A crop that removes an axis or condition is a scientific defect (07/05 §1; #49).
6. **Contract parameterisation.** 12/04 C11, 12/10 A11 and the token `canvas` block are vertical-only. They must read the EPP resolution (see also QA Profiles §11 item 1).

## 6. Typography and Indic rules per level

| Level | On-screen text | Notation | Minimum px at 1080 wide (label / equation / heading) | Captions |
|---|---|---|---|---|
| l1_2 | `icons_and_single_words` | none | ≥ base; Cal | `access_only` |
| l3_5 | `short_phrases` | basic | ≥ base; Cal | `short_lines` |
| l6_8 | `sentences` | standard (introduced) | 50 / 63 / 59 | `short_lines` |
| l9_10, l11_12, voc, educator | `sentences` | standard, advanced | 50 / 63 / 59 | `standard` |
| ug, pg, adult_prof | `dense_notation` | advanced | 50 / 63 / 59; at 16:9, 88 / 112 / 104 on the 1920 master | `standard` |

The Level Profiles own these values. This table restates LEVEL_PROFILES §3 and proposes the values it leaves unstated [Recommendation]. Split, enlarge or zoom instead of shrinking. Confusable glyphs (I/l/1, O/0, minus, decimal point, indices, Greek) are tested at 360 px display width (02 §D5–§D6).

**Indic and locale rules.**

- **Fonts.** Noto Sans or Serif Devanagari for Hindi. Noto Sans or Serif Bengali for Assamese, with ৰ and ৱ verified. Fonts are vendored, hashed and licence-checked, with no CDN (RD-23). Each face must pass the 12/05 smoke-test strings.
- **Animation unit.** Per word, as one shaped run with a mask. Per grapheme cluster only after the test card passes in the pinned Chrome (12/02 doc 08 §7.6). Never per code point (#55). Re-test after Chrome or HarfBuzz upgrades (NEW-18).
- **Typesetting.** No `letter-spacing` or `text-transform`. Real bold. Line height at least 1.4 [Hypothesis]. One `lang` per run, and no mixed scripts inside a word.
- **Script choice.** Hinglish is Latin script under the house transliteration and code-mix policy (CE-40). Hindi captions are in Devanagari with technical terms in Latin (11 Playbook Step 12).
- **Numerals.** Follow the edition's convention, as recorded in the fixture (NEW-30).
- **Layout.** Labels reflow, never shrink (CE-39). RTL locales need the Q-LOCALE RTL layout test before any style is admitted.

## 7. Density rules per level (count unexplained relationships)

02 §B3 counts **unexplained relationships**, not objects. [Recommendation] Operational rule for `level-lint`:

- **Definitions.** A *relationship* is any on-screen encoding that links two or more entities: an equation, arrow, axis pairing, plotted dependence, map link or comparison frame. It is *unexplained* while its reveal precedes the narration words (`words[]`) that establish it.
- **Rule 1.** No relationship stays unexplained beyond its establishing beat plus the A10 tolerance.
- **Rule 2.** Each beat has one dominant focus (02 §B2), and new relationships per segment stay within `attention.max_new_ideas_per_segment`.
- **Rule 3.** Before a dense explanation, four things are shown or narrated: what each symbol is, what changes, what stays constant, and what is being sought (02 §B3).
- **Rule 4.** Text elements stay at or below `on_screen.max_text_elements`.

| Level | Cap |
|---|---|
| l1_2 | One idea per frame; new ideas per segment Cal (expected 1) |
| l3_5 | One dominant focus; Cal |
| l6_8 | 02 §B3 (Inherited, as Hypothesis for this age) |
| l9_10, l11_12 | 02 §B3, §E2 (Inherited) |
| ug, pg, adult_prof | Dense notation; every symbol defined before use |

The motion budget of 25–35% of runtime is a production hypothesis, and animation is never added just to meet it (02 §E2). Styles may only lower these caps. Q-LEVEL is report-only until the pilots confirm the values (CE-35).

## 8. Science-visual rules per family

| Family | Rules (science layer) |
|---|---|
| `stem_fixture` | Every number, label and unit is a fixture value (Q-FIX, A7, A12). Axes and units are always visible, and scales stay fixed across compared states. Distortions are labelled (02 §E5). Atom identity is kept, and no morph hides a discontinuity. Biology shows the completed state before advancing. Data strokes have zero wobble. CS output on screen equals the sandbox capture. |
| `quant_social` | Charts are drawn from `ledger_recompute` fixtures. The encoding is declared, with a log ladder above three orders of magnitude. Time-bound rates show their as-of date and jurisdiction (CE-30). |
| `humanities_citation` | **Maps** are approved MED assets with a boundary review against the registered policy source (CE-53, O-8) and a source caption; never generated or agent-drawn. **Timelines** come from `date_fact` and `historical_event` claims (`data-fx="node:…"`), on linear time unless the encoding note says otherwise. **People** appear as generic paper figures with code-built name tags, never model likenesses (12/02 doc 03 §2.7). Contested events are labelled as attributed. |
| `languages_literature` | TXT is shown verbatim from the registered edition, within the quote-rights length, and is never set in ransom tiles. Read-along highlighting is per word on one shaped run. Phonics graphemes come from the lexicon. |
| `arts_skills`, `vocational` | MED demonstrations need a performer release. Procedure steps stay visible. Safety cards are distinct by shape and label; at ac0, a "with a grown-up" card. |
| `exam_strategy` | Pattern tables show the official source and as-of date. Marks only from the source paper or official key. |
| `health_medicine`, `law` | Not activated (O-9). Later: `dosage_fixture` values, jurisdiction and as-of date on screen, and the family's disclaimer card. |

## 9. Determinism conformance checklist (per style)

**Base checklist (every style).**

- [ ] ~~12/04 contract C1–C18: `DURATION` and `seek(t)`; no play, wall clock, timers, rAF or wall-clock CSS; stateless keyed PRNG only (`sceneId:elementId:step`); finite repeats; cue-sheet times; frozen fixtures; local awaited fonts; no network; at most one `<video>` on one worker; fixed-step simulations; no camera effects on science; no full-frame flash; an idempotent, clamped `seek`.~~ (replaced 15 Oct 2026: the C-numbers are 12/02 doc 04 clauses, not the normative contract). 12/04 `contract.md` v1.0.0 at Level 2 (§2; §4 rules F01–F13 and W01–W05; §5–§11). C-numbers cited elsewhere are 12/02 doc 04 clause ids, and contract.md wins where they differ. Randomness: a seeded stream only while building precomputed data at load, in a fixed order; inside `render(t)`, only the stateless `rngAt(seed, i)` with `i` keyed by object id (contract F04–F05; 12/02 doc 07 §2.5). Video: two or more `<video>` elements require `SCENE_META.workersMax = 1` (F13); PNG sequences preferred; lecture-slides keeps its own one-`<video>` limit (§3.8). Seed: `seed = int(sha256(f"{artefact_id}|{scene_id}|visual|v1").hexdigest()[:8], 16)` (mirrors MUSIC_and_SOUND_REGISTRY §5.1 step 3), recorded in the render manifest; it never includes a style, token or toolchain version, so a re-render of unchanged inputs reproduces bytes (§11).
- [ ] Every animated element declares its verbs in `data-motion` (canvas and WebGL layers on the canvas element, listing every verb drawn inside it), and the render writes a per-frame, per-element transform log to `qa/motion_log.json` for DOM and SVG elements (added 15 Oct 2026; checked by A1 and A14, §10).
- [ ] Canvas at the **EPP resolution**.
- [ ] A1 lint is clean.
- [ ] A3 frame hashes are identical across two processes and a reverse-order render.
- [ ] Q-DET: the MP4 is byte-identical from the pinned bitexact single-thread encode (`-map_metadata -1`).
- [ ] Narration audio and slot fills are replayed by hash.
- [ ] `harness/` digests are pinned (CE-38).

**Per-style additions.**

| Style | Extra rules |
|---|---|
| whiteboard-science | Identity camera throughout (scene rotation under `fixture_rotate` reads fixture fields and is not a camera move). Typed `data-fx` on every science glyph. Geometry is a pure function of fixture values. three.js, Manim and Blender scenes follow the voxel-isometric row (15 Oct 2026). |
| doodle-handdrawn | `boil_step = floor(t × boil_fps)`. Fixed `feTurbulence` seed. Zero wobble on data layers. |
| paper-collage | AssetManifest entry (SHA-256, source class, licence or job ID) for every asset. Hero sheet hash pinned. Deterministic crop, never stretch. |
| editorial-vox | Sizes computed from fixture numbers. No hand-tuned ratio pixels. Seeded highlighter ends. |
| kinetic-type | Timing from `words[]`. Tokens exist in the approved bundle, in order. Seeded font rotation. End-state equality with the static render. |
| voxel-isometric | Pinned render box. Render on seek only. Software-GL fallback test. PNG sequence import. Cross-box tolerance [Hypothesis]. Fail on `WEBGL_CONTEXT_LOST`. |
| lecture-slides | 16:9 only via the EPP. Talking head as a PNG sequence or one worker. Clip audio never used. |
| storybook-junior | Everything from collage, plus the ac0 tile analyser. `data-motion` verbs checked by A1 against the ac0 forbidden set. |
| exam-sheet | Answer card protected (`meta.answer_protection`). No timer code. |

## 10. A1–A17 mapped per style

Every check runs for every style. Severities follow `QA_PROFILES_REGISTRY.md` §2.5; only the parameters differ.

| Check | Style-specific parameters |
|---|---|
| A1 | Every style (15 Oct 2026): A1 fails a `data-motion` verb that is not in the style's `motion.vocabulary` or that is in the EPP's resolved forbidden set for its class (`style/base` plus the style's `by_safety_class`). Ships as a Level 2 check in `lint_seek_contract.js` (contract.md 1.1.0, MINOR under contract §14; §14 item 12). ~~SJ adds a forbidden-verb rule.~~ KT adds the no-CSS-time rule. |
| A2 | VI, and WS when three.js is used: WebGL box and software-GL flag (verify). LS: MED decoders. |
| A3 | 2D styles: exact. VI, and WS three.js scenes: exact on the same box; cross-box tolerance [Hypothesis]. |
| A4 | Token set for the EPP aspect. LS at 16:9 needs O-19. Unmeasured insets block release (QA Profiles §2.5). |
| A5 | §2.3 formula with `m_script` and `m_level`; `m_level` is read from the Level Profile (`hold_level_multiplier`) and multiplied by any style `hold_extra_multiplier`. WS and ES keep the question visible through the think window. |
| A6 / Q-FLASH | ac0 analyser for any ac0 artefact (SJ, DH, WS). WCAG floor otherwise. PC adds its paper-burst rule. Spatial patterns (§2.1) for every style, as Q-FLASH.pattern (added 15 Oct 2026). |
| A7 | All styles. OCR on `generated_gated` assets and lecture MED. Typed `data-fx` for maps and timelines. |
| A8a/b | Indic and RTL locales. Ransom and handwriting modes run the test card per font and mode. |
| A9, A10 | −16 LUFS ±1, at most −1 dBTP. KT keeps captions static. ES checks answer protection. |
| A11 | EPP resolution (parameterised; §5 item 6), 30 fps, h264, yuv420p. |
| A12 | WS panels in any style. EV numbers. VI fixture voxels. ES worked steps. |
| A13 | PC tile pairs, EV highlighters, SJ fills and KT accents, on real frames (NEW-31). |
| A14 | Asserts identity for WS, ES and SJ. Push-in, pan and drift windows for DH, PC and EV. Orbit for VI. Every style (15 Oct 2026): from `qa/motion_log.json`, A14 fails an element whose transform changes without a declared `data-motion` verb, and any composition transform during a `data-fx` reveal or hold. The log covers DOM and SVG elements only; canvas-internal motion is checked at H-SB and GF. Severity M; C at `safety/ac0` (QA Profiles §2.5). |
| A15 | VI, and WS when three.js is used: context loss and blank capture (NEW-21, NEW-22). WS, ES and LS: stall detection skips frames inside a `hold` cue whose [`at`, `until`] interval covers the still interval. Scene code emits such a `hold` cue for every intended still layout longer than the A15 margin. A still interval that no cue covers fails (15 Oct 2026). |
| A16 | PC and SJ hero sheets and cutouts. EV images. VI meshes. LS instructor MED and release. |
| A17 | VI, and WS when three.js is used: render-box minutes. LS studio minutes. |

## 11. Invalidation rules

The dependency index maps every `style/<id>@<ver>` and every bound token-file hash to its artefacts.

| Change | Semver | Class | Re-QA | Human gates | Published |
|---|---|---|---|---|---|
| Wording only, no rendered value changed | patch | Presentational | Re-render; identical bytes auto re-affirm | None if bytes are identical | Stale, then re-affirmed |
| New optional rule or token | minor | Presentational | Re-render; A-suite, Q-FLASH, Q-A11Y | GF/GS if bytes change | Stale |
| Palette, size, zone share, timing, font or motion value | major | Presentational | Full A-suite (plus A8 for fonts, A13 for palette) | H-SB where the layout grid changes; GF/GS | Stale |
| Safety classes narrowed, flash or motion limit tightened, ac0 block edited | any | **Safety** | Full suite under the new limits | Child-development re-sign (ac0); GF/GS if bytes change | Failing artefacts revoked |
| Safety classes or levels widened (any class added), any flash or motion limit loosened, a verb removed from verbs_forbidden, asset_sources_allowed widened (added 15 Oct 2026) | any | **Safety (loosening)** | Full suite under the new limits on every artefact that would newly resolve to the style | Child-development re-sign (ac0), G-COUNSEL re-record for the class, H-SB for newly routed formats; GF/GS if bytes change | Not selectable for the widened class until signed |
| Formats, levels or aspects narrowed | minor | Structural | Recompile; dropped pairs flagged | GA-Δ/H-SB on re-route | No new release on dropped pairs |
| Aspect added (16x9 after O-19) (added 15 Oct 2026) | minor | Structural | A4, A11 on the new aspect | H-SB for affected layouts | No change to existing 9:16 releases |
| Bound token file edited, or measured insets replace placeholders | file version | Presentational | Every style pinning it; A4 everywhere for insets | H-SB for affected layouts (12/05 README §5); GF/GS | Stale |
| Font binary, harness, Chrome, FFmpeg or HarfBuzz | `harness/` | Render toolchain | Re-render from the closure; compare bytes | None if bytes are identical | Stale, then re-affirmed |
| Defect in a style (for example a flash) | new version | Revocation | — | Re-approve on the new bytes | Blocked and withdrawn |

GR rejects a version bump whose class does not match its diff.

## 12. Negative tests (each must be refused or blocked)

| # | Input | Expected result |
|---|---|---|
| NT-S01 | `style/voxel-isometric` requested for `level/l3_5` | Compile error at §4.1 step 2 (ac0) |
| NT-S02 | A Detailed request asking for 16:9 through the style | Refused; aspect comes only from the Format Spec |
| NT-S03 | `format/lecture_segment` before WS and LS 1.1.0 (changed 15 Oct 2026) | Compile error at §4.1 step 4 (no allowed style supports 16x9) |
| NT-S04 | Doodle boil on an I–V line | A12/NEW-28 failure (Critical science error) |
| NT-S05 | "4 V" in a kinetic ransom tile | A7 untraceable science text (Critical) |
| NT-S06 | Hindi title animated per code point | A1 lint and A8b failure |
| NT-S07 | Storybook-junior code containing a shake or whip | A1 undeclared or forbidden `data-motion` verb; A14 undeclared transform (changed 15 Oct 2026) |
| NT-S08 | White bloom on an ac1 Short | Q-FLASH.full_frame Critical |
| NT-S09 | ac0 small-tile flash pair below the WCAG area threshold | Q-FLASH.ac0_zero fails; release blocked |
| NT-S10 | Entry with a property `premium_palette` or `asset_tier` | Q-COMM regex and the "no tier" rule (CE-26) |
| NT-S11 | Palette change filed as a patch | GR class-mismatch rejection |
| NT-S12 | Generated cutout containing letters | A7 OCR failure (#54) |
| NT-S13 | Cream on tomato (3.62:1) for an essential title | A13 contrast failure |
| NT-S14 | Requested style not in `styles_allowed` | Compile error; no substitution |
| NT-S15 | `marking.scheme` slot assigned to storybook-junior | Compile error: slot not implemented |
| NT-S16 | A map drawn in scene code without a MED review | Q-RIGHTS `map_boundary` failure |
| NT-S17 | Exam-sheet answer visible during the think window | Q-INT.reveal_order Critical |
| NT-S18 | Comparison lines distinguished by colour only | Q-A11Y.cvd (report-only until O-20) plus the H-SB rubric |
| NT-S19 | A Short cropped from a 16:9 lecture render | Refused: recompose, never crop |

## 13. Worked example: one Ohm's-law objective in four styles

**Fixture status.** Graph values come from fixture `FX-ohm-iv`, which **does not exist yet**. The four 04 models are RC, chemical balance, maths chain and genetics. The 02 blueprint §C gives the first line (10 Ω: 2 V → 0.2 A, 4 V → 0.4 A) but leaves the steeper line's resistance unresolved (§D item 1). M1 must author the fixture.

### 13.1 I–V scene in whiteboard-science (`format/detailed`, `level/l9_10`)

```yaml
epp.resolved:
  safety_class: safety/ac1                    # level/l9_10 (R2)
  aspect: 9x16; resolution: 1080x1920         # format/detailed
  styles:
    primary_illustrative: style/doodle-handdrawn@1.0.0  # §4.2 default
    scene SC-ch2-05: style/whiteboard-science@1.0.0     # Rule 0 (data-bound)
scene SC-ch2-05:                              # blueprint 05:00–06:35
  slots: [explain.ladder_step, check.predict, misconception.confront]
  elements:
    - axes I vertical / V horizontal, fixed scale; data-fx: fixture:FX-ohm-iv#axes.*
    - line_a: draw-on, no overshoot, blue, solid, direct label; data-fx: fixture:FX-ohm-iv#line_a.*
    - slope: one teal rise/run highlight, then KaTeX ΔI/ΔV = 1/R; data-fx: fixture:FX-ohm-iv#slope.expr_display
    - line_b (steeper): purple, dashed, direct label     # blue/purple luminance 1.05, so a pattern is required
    - think: blueprint 8 s, within RD-11 5–8 s; question and labels visible; answer hidden; SFX muted
    - wrong rule "steeper means more resistance": distinct shape and label, visibly retired (F7)
  holds: equation until max(t_end + 0.5 s, transform_end + 2.0 s); completed graph 2–4 s
  reduced_motion: draw-on becomes a 150–300 ms fade
  checks: A7, A12, A13, A14 (identity camera), NEW-28
```

### 13.2 Hook in doodle-handdrawn (`format/short`, variant `short.trap`, `level/l9_10`)

- **Hook.** `hook.question_reveal`: "Which line has the larger resistance? Check the axes." (backlog CSV 2, 07/05 SH5). Title "CHECK THE AXES" in 3 words.
- **Hold.** `max(1.2, 0.3 × 3) = 1.2 s` for en-IN. The hi-IN REN rendering holds 1.8 s [Hypothesis].
- **Frame.** A doodle magnifier and an underline on the word "axes". The two lines sit in a whiteboard-science panel. Boil runs only on the frame, and drift is zero during the label reveal and the think window.
- **Then.** `worked.step`, then `check.retrieval` with a 6 s window.
- **Audio.** A bed under the hook only, starting 20 dB below speech. In a Short it is a code-composed `reel_hook` bed (owned audio, MUSIC_and_SOUND_REGISTRY policy 4); it ends before `worked.step`, because music is muted under teaching.
- **Release.** A4 blocks release while the 12/04 insets are placeholders.

### 13.3 Same objective, `style/storybook-junior` (`level/l3_5`)

The request **does not compile**:

- "OBJ-ohm1 has no ACT or STY for level/l3_5".
- No SIM with `permitted_levels ∋ level/l3_5` exists, so the graph is invisible at this level (Architecture §5.1 step 2).

[Recommendation] The Resolver should also warn when the competency's framework stage differs from the level band. The honest route is a crosswalked Preparatory objective [N50] with an approved household-safe ACT. That resolves to storybook-junior with:

- Path A (R1) and `ac0_zero_flash`, with boil, whip, shake and push-in off;
- short phrases with say-aloud icons, Cal holds, and counted objects from fixture integers;
- a grown-up card, owned music (commissioned or code-composed, per the music registry) and the child sonic logo `music/logo-junior`;
- child-development co-signs at GA-Δ, H-SB and GF.

Doodle may be requested instead; editorial, kinetic, voxel, collage and exam-sheet are refused.

### 13.4 Same objective, `style/lecture-slides` (`level/ug`)

- **(a) `format/lecture_segment`.** ~~Compiles at 16x9, but is **blocked at H-SB** until O-19 is approved and A11 reads the EPP resolution.~~ Does not compile until LS and WS 1.1.0 add 16x9 after O-19; then H-SB, A4 and A11 gate it as usual (corrected 15 Oct 2026).
- **(b) `format/detailed` at ug.** 9:16 now. Slide card and instructor head at chapter transitions [N4], over Path A audio. ac1 (CE-18). Dense notation, with every symbol defined first. The I–V graph is a whiteboard-science element at 9:16 sizes. Any conductivity extension needs its own claims and fixture.

## 14. Inconsistencies and open items

1. **paper-collage ID.** The 12/05 key `paper-collage-vertical` differs from `style/paper-collage`; they are mapped through `legacy_style_id`.
2. **Vertical-only rules.** 12/04 C11, doc 04 §5, 12/10 A11 and the token `canvas` hard-code 1080×1920, against CE-46/F20. **Partly resolved 15 Oct 2026 (CE-69):** the 12/10 A11 text now follows the Format Spec aspect. 12/04 C11, doc 04 §5 and the token `canvas` stay vertical-only until the 16:9 safe-zone tokens exist (O-19); recorded as P1.
3. **Indic gate.** The 12/05 tokens keep `common.locale.indic_rules_active: false` (RD-26), against CE-L5's Hinglish and hi-IN launch.
4. **`base-science`.** It had no registry entry; whiteboard-science replaces it.
5. **Base files.** Architecture §10 maps only the 02 tokens to `style/base`, but sizes, holds and determinism live in the 12 files.
6. **Naming.** Collage "Tier A/B/C" breaks the no-tier naming rule; it is renamed `asset_sources_allowed`. The kinetic tag `cta` becomes `next-step`.
7. **Two determinism checks.** A3 compares frames and never MP4 bytes (NEW-12), while Q-DET compares MP4 bytes. Both are kept.
8. **Missing fixture.** There is no Ohm's-law fixture in 04.
9. **No stage check.** R4 lacks a framework-stage versus level check.
10. **Pending approvals.** Biology green, the non-STEM accents and AD-17 dark sheets.
11. **Music alignment (resolved 15 Oct 2026).** This document formerly placed beds in recaps at 20–24 dB and allowed "in-house or licensed" music. It now follows `MUSIC_and_SOUND_REGISTRY.md`: spoken recaps muted, beds start 20 dB under speech, owned audio only, code-composed beds for Reel hooks, SFX and prototypes only, sonic logo core 1.5–3 s. `style_entry.schema.json` `sonic.music_sources` is now `commissioned | code_composed` and `sonic.sonic_logo_ref` takes a `music/<id>@x.y.z` pin (CE-66).
12. **Harness contract 1.1.0 (P1, added 15 Oct 2026).** 12/04 `contract.md` §9 moves to 1.1.0 (MINOR under contract §14) with three changes: typed `data-fx` (`fixture:<id>#<path>`, `node:<id>#<field>`) required at Level 2; `scene_template.html` `fx()` strips the `fixture:<id>#` prefix and raises `E_FIXTURE_MISSING` when `<id>` differs from the fixture id that the harness passes with the fixture and records in the render manifest (resolving `node:` paths needs a harness-supplied node text table); and the A1 `data-motion` verb rule as a Level 2 check in `lint_seek_contract.js` (§10). Today the template uses a bare path (`data-fx="parameters.resistance_ohm"`), so a scene written to §1.2 fails until this lands.
