# Skills 9–15: audio, timing, orchestration, governance, QA and vertical layout

These are skills 9–15 of the "Advanced Animations with Claude" layer, as specified in report §10 (`12_advanced_animations_with_claude/01_research/RESEARCH_REPORT_advanced_animations_with_claude.md`). Skills 1–8 (`examleaf-anim-brief` … `examleaf-threejs-scenes`) are documented by their own author.

Every folder contains:
- `SKILL.md`, with YAML `name` = folder name and a third-person `description` starting "Use when…" (≤ 1024 characters);
- `references/`: at least two deep documents;
- `templates/`: `handoff.json` in the library schema, plus JSON and prompt templates;
- `evals/cases.json`: at least 4 positive and 5 negative cases, `"status": "authored_not_agent_executed"`;
- `scripts/`: Python 3, stdlib only, each with a `--selftest` that exits 0 offline.

**Status:** drafts dated 14–15 Oct 2026. None is agent-evaluated. Nothing was installed, and no network or MCP call was made. The script selftests are the only executed evidence.

**Conventions:**
- [V#] = reference videos; [N#] = verified web claims; #N = master edge case from report §8.
- Exit codes are shared across all scripts: 0 ok, 1 blocked or refused (structured JSON on stdout), 2 usage, IO or dependency error. `credit_ledger.py` adds 3 (cap) and 4 (overrun recorded, ledger frozen).
- Repair limit: at most two repair attempts, then human escalation. Authoring loops are capped at 3 (AD-11).

---

## 9. `examleaf-audio-compose`

- **Purpose:** seeded, bar-aligned Python music beds and SFX one-shots per house style.
  - Fixed tempo: about 100 BPM for the storybook style [V4-MP].
  - Mood variants: low-passed somber, end-card swell.
  - Licensed-bed or no-bed fallback when synthesis sounds "chiptune".
- **Inputs → outputs:** `bed_request.json` (style, segment role, bpm, length, seed, mood, SFX list) → `pad.wav`, `pluck.wav`, `perc.wav` (48 kHz, 16-bit, mono, −12 dBFS peak), `bed_meta.json` (BPM, bars, seed, bar and beat grid, hashes), `<sfx>.wav` with `sfx_palette.json`, and `handoff.json`.
- **Owns:** bed stems, SFX one-shots and their metadata.
- **Extends:** none (new). It hands loudness to `examleaf-audio-production-engineer` (the mastering owner), placement to `examleaf-cue-sheet`, and provenance to `examleaf-asset-library`.
- **Policy:** music is off under the core explanation (`04_NARRATION_SUBPIPELINE.md` §13; AD-15). House loudness is −16 LUFS / ≤ −1 dBTP; [V4-MP]'s −14 LUFS is noted, not adopted (AD-04).
- **Edge cases:** #10, #13, #17 (audio analogue), #39, #63; sample licensing; the chiptune risk.
- **Scripts:**
  - `python3 examleaf-audio-compose/scripts/compose_bed.py --selftest`
  - `python3 examleaf-audio-compose/scripts/sfx_palette.py --selftest`

## 10. `examleaf-audio-analysis`

- **Purpose:** beat grid, onsets and energy envelope for beds and Reels.
  - In-house beds are read exactly from metadata, with no detection.
  - External or licensed audio goes through a lazily imported, fully guarded librosa path.
  - Falls back to a narration phrase grid when there are no beats.
- **Inputs → outputs:** `--bed-meta bed_meta.json`, or `--audio file` plus an optional `--start-bpm` | `--prior-norm`, `--bpm-curve` and `--words alignment.json` → `analysis.json` (seconds only: `tempo_bpm` as a float, `beats_s`, `onsets_s`, `energy`, `fallback`, warnings, provenance).
- **Owns:** `analysis.json`.
- **Extends:** none (new). Word timing stays with `examleaf-alignment-localize`.
- **Edge cases:** #13, #31 stereo/sparse [N37], #32 ndarray tempo [N38], #33 `units='time'` [N39], #34 empty beats or 0 BPM [N41], #35 `sr=None` drift [N81], #36 ParameterError [N40], #37 start_bpm vs prior [N36], #38 bpm shape [N42].
- **Scripts:** `python3 examleaf-audio-analysis/scripts/beat_grid.py --selftest`. This is stdlib only and exercises every guard on a synthetic onset envelope. librosa was not installed here, so the `--audio` path is untested and exits 2 with a clear message.

## 11. `examleaf-cue-sheet`

- **Purpose:** the canonical per-scene cue sheet (report §5.5).
  - Merges word timings, beats, SFX and reveal cues.
  - Reveal on, or about 0.05 s before, the word, with a 1-based occurrence index for repeated words.
  - Duration comes from the narration and is snapped so frames = DURATION × fps [N72].
  - Re-times on TTS regeneration (#63).
  - Reel `--window`, plus beat snapping for decorative cues only.
- **Inputs → outputs:** `cue_spec.json` + Alignment JSON + narration WAV (+ synchronizer `timeline.json`, `analysis.json`, `sfx_palette.json`) → `cue_sheet.json` (harness schema 1.0 shape, 15 Oct 2026), `cue_sheet.provenance.json` (hashes, anchors, `contains_fixture`, snapped, dropped) and `cue_sheet.retime.json`.
- **Owns:** the merged cue sheet and its sidecars, **not** alignment and not captions.
- **Extends:** `examleaf-speech-animation-synchronizer` (its cue frames win, after a ≤ 1-frame cross-check) and `examleaf-alignment-localize` (its Alignment is read, never recomputed).
- **Edge cases:** #13, #16, #33, #35, #63; answer protection (`reveal-answer` never leads its word); Reel windows through words.
- **Scripts:**
  - `python3 examleaf-cue-sheet/scripts/build_cue_sheet.py --selftest`
  - Validation: `python3 -B -I ../04_harness_contract/validate_cue_sheet.py SHEET.json --production`. *15 Oct 2026 (audit M7): the skill-local `validate_cue_sheet.py` was deleted; the builder imports the harness validator by path, emits `schema_version`, `language`, `narration_audio_sha256` and `script_sha256`, and its selftest runs its own output through the harness validator with `--production`.*

## 12. `examleaf-mcp-orchestrator`

- **Purpose:** the guard layer for Higgsfield and future Blender, music or voice MCPs.
  - Per-job permission grants and estimate-before-call.
  - A hard credit ledger: reserve, submit, commit or release, a cap stop, and a freeze on overrun.
  - Idempotent job keys, 60 s result reconciliation [N35], throttling backoff [N80].
  - Secrets in env or user config only [N19]; reference images for character consistency.
  - No text or labels in images; a diff of MCP-bound text against the approved script.
- **Inputs → outputs:** `mcp_job_request.json` + `permission_grant.json` + gate approval → `credit_ledger.json`, `mcp_jobs/<key>.json`, `script_diff.json`, asset-library entries, and `handoff.json`.
- **Owns:** the grant record, MCP job records, the credit sub-ledger (in credits), reconciliation, and the text diff.
- **Extends:** none (new). It is the MCP transport guard **for** `examleaf-selective-generation` (owner of paid generation) and `examleaf-anim-storyboard-gate` (owner of the grid). It posts committed credits to `examleaf-observability-cost`.
- **Facts used:** credits are always billed via agents [N33]; no native cap [N34]; the CLI path [N31]; the connector URL [N29] (contested); plan figures [N75]–[N77], which are competitor-authored.
- **Edge cases:** #11, #40, #41, #42, #43, #44, #45, #46, #47, #48, #54.
- **Scripts:** `python3 examleaf-mcp-orchestrator/scripts/credit_ledger.py --selftest`. The text diff reuses `examleaf_narration.qa.transcript_check`; no new script.

## 13. `examleaf-effort-governor`

- **Purpose:** model, effort and iteration policy per task (report §3.4).
  - Explicit effort, never the medium default [N22]; pinned full model IDs [N28]; requested vs effective level logged [N23].
  - Ultracode refused [N24][N25][V1]; max only with a justification; thinking always counted [N26].
  - Long Haiku prompts rerouted [N28]; 3 authoring loops and 2 repair attempts (#60).
  - Token caps with budget alerts, and a cache-friendly session plan.
- **Inputs → outputs:** task, job, scene, round, `model_pins.json`, `budget_caps.json` → `run_config.json` (env `CLAUDE_CODE_EFFORT_LEVEL`, `--effort`, caps, cache plan) and `runs.jsonl` (`planned` and `completed` events).
- **Owns:** the model, effort and iteration policy and the effective-level run log.
- **Extends:** `examleaf-observability-cost`, which keeps the pipeline ledger, dashboard and reconciliation.
- **Edge cases:** #1, #2, #3, #4, #5, #6, #58, #60, #61.
- **Scripts:** `python3 examleaf-effort-governor/scripts/effort_policy.py --selftest`. Model pins and token caps are deliberately left unfilled ("no cap, no run"); the founder fills them from the catalog and the pilot.

## 14. `examleaf-anim-qa`

- **Purpose:** the animation-specific QA layer, with severity classes and release-blocking rules. The checks:
  - safe zones against the vertical tokens (#51);
  - hold times: headlines ≥ 1.2 s [N60], longer for Indic text; equations until narration ends plus 0.5 s (#50);
  - reveal-on-cue after re-time (#63); caption-over-science overlap; camera fx during labels (#64);
  - per-frame luminance flash test (#56; WCAG 2.3.1 three-flashes rule, **verify exact thresholds**);
  - determinism hash via the harness checker (#17);
  - fixture-vs-rendered text diff from a DOM dump or OCR (#12, #54);
  - Indic cluster and tofu (#55);
  - final-mux LUFS and true peak (#39).
  It then hands a hash-bound report to `examleaf-release-review`.
- **Inputs → outputs:** render MP4 + PPM frames + `elements.json` / `dom_text.json` (from `templates/dom_dump_snippet.js`) + cue sheet + tokens + zones + `expected_text.json` + determinism result + audio QA → `safe_zone_report.json`, `flash_report.json`, `text_diff.json`, `anim_qa_report.json` and `handoff.json`.
- **Owns:** the animation checks and their report.
- **Extends:** `examleaf-visual-qa` (frames, contrast, phone layout) and `examleaf-audio-caption-qa` (captions, listen).
- **Edge cases:** #12, #17, #39, #50, #51, #54, #55, #56, #63, #64.
- **Scripts:**
  - `python3 examleaf-anim-qa/scripts/flash_check.py --selftest`
  - `python3 examleaf-anim-qa/scripts/safe_zone_check.py --selftest`
  - `python3 examleaf-anim-qa/scripts/text_fixture_diff.py --selftest`

## 15. `examleaf-vertical-adapt`

- **Purpose:** rules and helpers for 16:9 → 9:16 re-layout.
  - Stacked zones: title at the top, visual in the middle, captions at the bottom.
  - Safe insets come from tokens ("measure per platform, no verified pixel values"); the side minimum is the token `zones.side_margin_min_px` = 96 px (15 Oct 2026, AD-42; was the [V4-MP] 90 px), and the zone shares are read from the same file.
  - Contain, never crop; a mapping table for every [V4-MP] recurring layout.
  - Caption placement, and the Reel sub-range re-seek and beat re-time recipe.
- **Inputs → outputs:** tokens + style guide + `relayout_request.json` (+ Reel window) → `zones.json` (`provisional` when insets are unmeasured), `relayout_plan.json`, contain-fit numbers, and `handoff.json`.
- **Owns:** the re-layout rules, zones per scene, the re-layout plan, and the Reel recipe.
- **Extends:** none (new). It feeds `examleaf-reel-repurpose`, which keeps content selection and the ShortSpec, and it uses `examleaf-cue-sheet` for the window and snap.
- **Edge cases:** #49, #51, plus #50, #63 and #64 for Reels.
- **Scripts:** `python3 examleaf-vertical-adapt/scripts/layout_zones.py --selftest`

---

## Run every selftest

From `12_advanced_animations_with_claude/03_skills/`:

```sh
for s in examleaf-audio-compose/scripts/compose_bed.py examleaf-audio-compose/scripts/sfx_palette.py \
         examleaf-audio-analysis/scripts/beat_grid.py \
         examleaf-cue-sheet/scripts/build_cue_sheet.py ../04_harness_contract/validate_cue_sheet.py \
         examleaf-mcp-orchestrator/scripts/credit_ledger.py examleaf-effort-governor/scripts/effort_policy.py \
         examleaf-anim-qa/scripts/flash_check.py examleaf-anim-qa/scripts/safe_zone_check.py \
         examleaf-anim-qa/scripts/text_fixture_diff.py examleaf-vertical-adapt/scripts/layout_zones.py; do
  python3 -B -I "$s" --selftest || echo "FAIL $s"; done
```

## How the seven connect

```text
audio-compose ──bed_meta.json──> audio-analysis ──analysis.json──┐
      └──sfx_palette.json──────────────────────────────────────┐ │
alignment-localize ──Alignment──┐                              ▼ ▼
speech-animation-synchronizer ──timeline.json──> cue-sheet ──cue_sheet.json──> anim-brief → scene code (harness)
vertical-adapt ──zones.json──────────────────────────────────────────────────┘          │
effort-governor ──run_config.json / runs.jsonl ──> runner ── observability-cost         ▼ render
mcp-orchestrator ──credit_ledger.json ──> selective-generation / storyboard-gate ──> asset-library
anim-qa (+ visual-qa, audio-caption-qa) ──anim_qa_report.json──> release-review ──> human GF/GS
```

## Overlap notes (for the project owner)

1. **mcp-orchestrator vs selective-generation.** Under the library proposal, selective-generation is the single owner of paid generation, cost reservation and job persistence (`OVERLAP_and_DEDUPLICATION.md` cluster 15). This skill is scoped as its MCP guard: it does not decide what to generate. Its credit sub-ledger sits beside the engine's cents `BudgetLedger`. Confirm that split, or record this skill as an extension of selective-generation in `SKILLS_PIPELINE_STAGE_MAP.md`.
2. **anim-qa loudness vs audio-caption-qa / audio-production-engineer.** anim-qa only *verifies* the final-mux numbers produced by the audio tools. Mastering stays with audio-production-engineer, and the audio QA report stays with audio-caption-qa. Avoid two loudness verdicts: one report should cite the other.
3. **cue-sheet vs speech-animation-synchronizer.** Captions and narration cue frames stay with the synchronizer, and the cue sheet consumes them. The cue sheet adds animation-only cues, beats, SFX, windows and snapping.
4. **Indic tokenization.** The narration `normalized_words` regex splits Devanagari and Bengali-Assamese words at vowel signs. This was checked here: `re.findall(r'[^\W_]+', 'विद्युत्')` returns four fragments. The synchronizer's `cue_time` therefore cannot anchor most Hindi or Assamese words. The cue-sheet builder uses its own Unicode-aware tokenizer; the narration code is untouched.
5. **Token-file shape.** `safe_zone_check.py` and `layout_zones.py` accept `insets` or `platforms{…insets}`. If the harness author's `vertical_safe_zones.tokens.json` uses another shape, both refuse it loudly. Align them deliberately.
6. **anim-qa cluster check vs kinetic-typography.** kinetic-typography (skill 7) authors grapheme-safe animation; anim-qa only verifies the rendered spans.
