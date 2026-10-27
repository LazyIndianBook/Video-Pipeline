# Fixes applied after the end-to-end audit (15 Oct 2026)

Five Opus 5.5 fix agents with disjoint file ownership (07 runbook; 07/10 decisions + root README; 13 strategy + 06 registration; 12 animation code and docs; 05/06/08/09/10/11), followed by one Sonnet 5.5 verifier that re-ran every check, then the lead closed the items that fell between ownership boundaries. About 94 files changed. `00_source/` untouched.

## Verification after the fixes (11 of 11 pass)

| Check | Result |
|---|---|
| All offline self-tests (24 scripts: Python, Node, bash) | 24 pass, 0 fail |
| Cue-sheet builder validates through the single harness validator; skill-local copy deleted | Pass |
| 16:9 / 1920×1080 mentions in 07 and root README | Every remaining hit is marked superseded, smoke-test, P1 build item or provenance |
| AI-voice disclosure gate present in 07/06, 07/03, 07/11 | Pass (14 mentions) |
| Decisions RD-41…RD-46 recorded; RD-16 and RD-26 marked SUPERSEDED | Pass |
| Stale "57 skills" counts | Gone; remaining "57 passed" hits are the narration pack's historical delivery records, with the later 58+2 / 60 figures noted where docs discuss them |
| Section 13: Reels never inherit approval; GA and H-SB precede rendering | Pass |
| JSON validity (67 files under 12 and 13) | Pass |
| Relative markdown links (282) | 0 broken |
| Storyboard approval record: two roles + fixture/style/hero hashes | Pass (schema 1.1) |
| No cache directories outside 00_source | Pass |

## What changed, by audit finding

| Finding | Fix |
|---|---|
| **M1** vertical-only not in operating docs | Every 16:9 remnant in 07/00, 07/03, 07/06, 07/11, 07/README, 07/02 and the root README changed to 1080×1920 @ 30 fps, dated; the proof renderer's 720×1280 @ 24 fps limit stated and a 1080×1920 output mode added as a P1 build item; the benchmark scores 9:16 only (16:9 unscored smoke test); 10 pilots, 12/10 A11, the walkthrough B.6 and the style tokens updated; RD-16 marked SUPERSEDED |
| **M2** no disclosure gate | Blocking reason in 07/06 §6.1 (marked not yet in `release_check()`), new §6.4 with the YouTube toggle, Meta label and C2PA rules, Path A / Path B wording templates; `ai_voice_disclosure` and `performer_credit` added to the S14 export record, the ShortSpec table and the contracts doc; checklist items; RD-45; playbook and pass-1 report aligned; negative tests for disclosure removal added |
| **M3** Reels inherited approval in 13 | §5.7 rewritten: a Reel never inherits approval; LLM-drafted hook/CTA is new script → GA; full A-suite and GS bound to the Reel's hash by two identities |
| **M4** academic approval after rendering in 13 | §2.1 diagram and §5.5 reordered: GA (bundle hash) → H-SB → TTS → cascade → A-suite → GF, GS per Reel |
| **M5** animation layer, storyboard gate, ultracode rule absent from 07 | PA-03 (H-SB gate between S8 and S9/S10 in 07/00, 07/03, 07/06, 07/11), PA-07 (A1–A17 table in 07/06 §3.1), PA-11 (animation-authoring cost line in 07/08), PA-12 (effort/ultracode rule in 07/09 §4.1 and 07/08 §8), PA-17 (checklist Section A: setup, preflight, S-ANIM); Node 22+ and Chrome required when animation is in scope; this Mac's blockers listed; RD-43 records the accepted amendments; per-surface effort defaults stated once |
| **M6** "$0 review" not in runbook or cost docs | RD-41 (review cash $0; 85 min/lesson kept as capacity ≈1,417 h per 1,000 lessons); dated addenda in 07/README, 07/08, 08 README and CONSOLIDATED Part E; principle reworded to "review minutes are the throughput constraint"; business ₹3,000 line relabelled opportunity cost |
| **M7** cue-sheet builder failed its own schema | Builder emits `schema_version`, `language`, `narration_audio_sha256`, `script_sha256`; self-test runs output through `04_harness_contract/validate_cue_sheet.py` including `--production`; duplicate validator deleted; ZWJ/ZWNJ handling aligned with the narration comparator; matrix row updated |
| **M8** language scope | RD-42: launch locales en-IN, Hinglish, hi-IN behind the locale gate; as-IN deferred, human voice only; 07/03 S5 rule 10 and 07/04 §18 updated (old text struck through) |
| **M9** playbook 3 s pause cap | Scoped to TTS break tags only; protected think windows follow RD-11 (default 6 s, 5–8 s range) or pause-video; the 07/10 addendum corrected |
| **M10** forgeable single-role storyboard approval | Approval record v1.1 with founder (cost) and academic lead (science) roles plus fixture/style/hero hashes; `verify()` checks both roles and all hashes and states the runner verifies against the authenticated service; `Edit(./storyboard/**)` denied; `Read(../**)` rule replaced by staged hashed copies |
| **M11** preflight credited with checks it lacks | Secret scan and ultracode/alias greps added to `preflight.sh`; remaining items relabelled proposed in 12/02_documentation/01 |
| **M12** section 13 verifier stack | V2/V4 point to the existing anim-qa scripts; V5 uses the contract timing rule (late = fail; ±150 ms quality metric only); V3 adds reverse-order render; V0–V8 stated as additional to 12/10 and 07/06; fixture-visual archetypes routed to SVG/Manim adapters |
| Cost framing in 13 | "40–100× at the lean floor" corrected to the table's maxima (≈7× vs an Opus Kit; 14–27× vs bespoke; 40–100× only vs max-effort bespoke runs); "Today" re-priced at 5.5 tariffs and shown both ways; today's generated clips set to $0; open-model saving restated for the review-free case; batched cascade ≈$0.71–0.80; S-arm budget reconciled; cache reads 2.5–10%; TTS lean floor $0.14 now / $0.28 from 1 Jan 2027; rater pairs 10; Path A row added; lean floor scoped to Path B content |
| Effort/ultracode conflicts | `kit_cascade` task family with its own caps added to `effort_policy.py` (ultracode still refused everywhere); AD rows scope AD-02/11/24 to the strong-model phase; S5 probe is an attended, founder-approved exception (RD-48); edge case #3 wording aligned |
| Safe-zone geometry | `vertical_safe_zones.tokens.json` is the single owner of zone shares and side margin; `layout_zones.py` reads shares from tokens; stale 0.20/0.58/0.22 note removed |
| Loudness/music records | AD-37 wording corrected (−1.5 dBFS sample peak in the original); clip-import notes point to the current key; one music policy everywhere (muted under teaching; beds only in hooks/transitions/recaps/outros at 20–24 dB under speech; owned sonic logo commissioned; code beds for Reel hooks/SFX/prototypes) |
| anim-qa severities | Untraceable science text, full-frame flashes and early answer reveal → critical in scripts, 12/10 and 07/06 |
| Stale counts and claims | Narration gates read 58 passed + 2 FFmpeg-environment failures (60 with FFmpeg); the two intentionally changed narration files noted against DELIVERY_MANIFEST; "72 skills" everywhere; 34 sheets; Start-here rows for sections 11–14 in the root README; byte-identical provenance sentence corrected |
| Registration | Section 13's proposed `examleaf-fill-<archetype>` skills registered as PROPOSED in 06 README and OVERLAP (owners named); section 14 row in the root README; 09 VERIFIED_vs_PROPOSED references 11–14 |
| Setup executability | python3 only (no `python` binary), venv pinned to 3.13 or 3.11, Node 24 via nvm, ffmpeg and ffprobe missing; minimal frame-capture command added, flags marked [verify] |

## Not changed (deliberately)

- **Code build items, not docs:** a 1080×1920 output mode in the proof renderer; disclosure reason in `release_check()`; `ShortSpec` fields; these are recorded as P1 build items in 07/02 and 07/06.
- **Amendments PA-01/02/04/05/06/08/09/10/13/14/15/16/18** remain proposals (RD-43 accepts only PA-03/07/11/12/17).
- **Narration repo records** (`DELIVERY_MANIFEST.json`, `outputs/tests.txt`) record the delivered state and were not regenerated.
- **00_source** is untouched; its README's "35 sheets" is noted as 34 in 08.

## Founder decisions still open

RD-44 (free-chapter policy and digital-only SKU), RD-47 (Path A scope), RD-48 (keep or drop the attended $50 Ultra probe). See `07_end_to_end_pipeline_instructions/10_DECISIONS_and_CONFLICT_RESOLUTIONS.md`.
