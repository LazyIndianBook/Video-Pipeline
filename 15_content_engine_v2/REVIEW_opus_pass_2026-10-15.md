# Opus 5.5 review and fix pass over Content Engine v2 (15 Oct 2026)

**Provenance.** One workflow, 55 agents: 14 Opus 5.5 reviewers (one lens each, read-only), 28 verifiers (a Sonnet 5.5 evidence-reproduction lens and an Opus 5.5 materiality lens per reviewer; a finding was dropped only when both refuted it), 10 Opus 5.5 fixers with disjoint file ownership, one Opus stitcher for cross-group edits and decisions, one Opus final verifier and one Opus completeness critic. 205 findings confirmed (critical 20, major 157, minor 28); 278 fix entries applied and every one re-checked against the files; 6 schemas added (epp, approval_record, format_plan, locale_profile, lex_entry, golden_set); decisions CE-73 to CE-110 recorded. `00_source/` untouched. The completeness critic's 12 items were applied in a second pass the same day (see the addendum at the end).

| Lens | Reviewer verdict | Found | Confirmed |
|---|---|---|---|
| scripting | sound-with-fixes | 15 | 15 |
| interaction | sound-with-fixes | 15 | 15 |
| voice | sound-with-fixes | 14 | 12 |
| music | sound-with-fixes | 15 | 15 |
| visual | sound-with-fixes | 15 | 14 |
| packaging | sound-with-fixes | 15 | 15 |
| qa | sound-with-fixes | 15 | 15 |
| skills | sound-with-fixes | 15 | 15 |
| schemas | sound-with-fixes | 15 | 15 |
| resolver | sound-with-fixes | 15 | 15 |
| walkthrough | sound-with-fixes | 14 | 14 |
| coverage | sound-with-fixes | 15 | 15 |
| sceptic | sound-with-fixes | 15 | 15 |
| safety | sound-with-fixes | 15 | 15 |

---

# Opus review and fix pass, 15 Oct 2026

**Verdict: sound.** All 205 confirmed findings are applied, and I checked every entry in the applied-fix list (278 entries, 0 missing or wrong) in its file. 8 of the 9 mechanical checks pass. Check 9 fails on two stale secondary mentions of the precedence chain; the four canonical copies of R8 agree word for word. I edited no files in this pass.

## Checks

| # | Check | Result | Detail |
|---|---|---|---|
| 1 | Draft-07 meta-validation | Pass | All 19 schemas pass (9 in `schemas/`, 10 in `subsystems/schemas/`). The "13" in the brief predates the 6 schemas added today. |
| 2 | Commercial lint | Pass | 0 hits across 19 JSON files. Scope: every key at every depth, property and definition names, required entries, enum and const values. |
| 3 | Embedded examples | Pass | 6 examples validate with 0 errors (INTERACTION §17 once its hash placeholders are filled). 4 skeletons have 0 errors beyond placeholders. 9 YAML skeletons have no extra and no missing required keys. |
| 4 | Relative links | Pass | No v2 file uses markdown link syntax, so 0 links and 0 broken. 351 backticked paths were scanned; the 43 names that don't resolve are external shortnames or runtime artefacts. |
| 5 | Stale ids | Pass | `access_tier` survives only in dated notes, P1-01, the README logs, negative test NP-01 and retired-field lists. `paper-collage-vertical` survives only as the legacy key, `super_teacher@` only in log K. `tier` in schemas appears only in regex or prose about the ban. `fills[].tier` appears only in CE-70. |
| 6 | Persona ids | Pass | Only the five registered ids are used. |
| 7 | 00_source | Pass | 0 of 579 files changed on or after 15 Oct. |
| 8 | Counts | Pass | All 29 §3 rows equal `wc -w` exactly. Total 101,447; the CSV has 89 data rows. The root README row says 52, and `find` gives 52. |
| 9 | Precedence chain | **Fail (minor)** | Arch R8, CE-09, README §2 item 7 and VISUAL §4.1 step 9 are identical. MUSIC §2.1 item 1 and the style_entry schema description still carry the old five- and six-element chains. |

I also probed several fixes with mutated instances, and all behaved as claimed:
- solve_independently with a think window is rejected.
- A sidecar whose only approval is RELEASE_CHECK is rejected.
- A Path B sidecar carrying a Path A disclosure variant is rejected.
- An ac0 classification on a Path B sidecar is rejected.
- A `gs/` pin is rejected.

## Counts by lens (found → confirmed → applied)

| Lens | Found | Confirmed | Applied |
|---|---|---|---|
| scripting | 15 | 15 | 15 |
| interaction | 15 | 15 | 15 |
| voice | 14 | 12 | 12 |
| music | 15 | 15 | 15 |
| visual | 15 | 14 | 14 |
| packaging | 15 | 15 | 15 |
| qa | 15 | 15 | 15 |
| skills | 15 | 15 | 15 |
| schemas | 15 | 15 | 15 |
| resolver | 15 | 15 | 15 |
| walkthrough | 14 | 14 | 14 |
| coverage | 15 | 15 | 15 |
| sceptic | 15 | 15 | 15 |
| safety | 15 | 15 | 15 |
| **Total** | **208** | **205** | **205** |

## Ten most important fixes

1. **scripting-01 / resolver-07:** the record `sha256` now excludes lifecycle fields. GA-Δ binds a new `script_content_sha256`, so CE-34 re-affirmation works.
2. **schemas-01 / sceptic-01 / safety-05:** the English-only disclosure regex is replaced by `disclosure_variant` plus `text_ref`, keyed to voice path. as-IN direct narration is now possible.
3. **schemas-08 / resolver-13/14/15:** the EPP, approval-record and format-plan schemas now exist, with required pins, reviewer requirements and toolchain versions inside `epp_hash`.
4. **walkthrough-07 / resolver-01:** there is now a single per-gate binding table (Arch §3.7, QA §4.1, approval_record).
5. **resolver-04 / resolver-05:** rule evaluation order is now R2, R3, R1…, and R8 takes the most restrictive value for `x-kind: limit` fields.
6. **packaging-01/02/03:** AC0 needs a made-for-kids designation or is not published. Classification and disclosure must agree. Copy is hash-bound with a COPY gate.
7. **scripting-02 / safety-04:** a sentence is non-assertive only through a registered template, and `submitted` requires closure `pass`.
8. **interaction-08/09/11/12:** pause-video is required for written work. Short think windows require `binary_choice`. AC0 needs a seated alternative and a grown-up cue, and AC0 spacing is video-only.
9. **voice-01/08 / safety-10:** clones need consent, counsel and provider verification. Retention, deletion and purge are now recorded.
10. **walkthrough-06 / packaging-05:** DISCLOSURE moves to S12, bound to the delivered file. Publish receipts record the platform flags.

## Skipped, and why

- **schemas-13:** `multipleOf` was added only to the think and pause-video branches.
- **packaging-09:** no `test_variant_integrated` field; the AD-04 arm is a token, per sceptic-02.
- **voice-05:** the schema part was skipped. **voice-07:** no `approved_fallbacks` and no renewal refusal.
- **music-02(c)** and the Reels arm of **music-14** were dropped as instructed.
- **packaging-15:** no blanket ban on real children's faces; a guardian release is required instead.
- **visual-09:** no WCAG, area or boil interim numbers; the source is marked verify.
- **schemas-04 / coverage-12:** vocational was not added to Q-FIX.
- **interaction-15:** no `base_locale_seconds` field.
- **resolver-13 / schemas-02:** `gs/` and `reviewer/` pin kinds are excluded (resolver-06/08).
- **interaction-02:** the GA-Δ note uses the content hashes, not record `sha256` (CE-73).
- **qa-09 / qa-14:** waiver data went into one §2.12 table instead of a new column in every table; `Q-INT.answer_surfaces` keeps the single-suffix id rule.
- **sceptic-06:** the closure-formula part was superseded by resolver-03.

## Leftovers for the lead

1. Update the precedence chain in MUSIC §2.1 item 1 and in the style_entry schema description. The schema description also predates resolver-03: it still says token hashes "enter the EPP pins and the closure hash". This is outside my edit licence.
2. `12/03_skills/examleaf-audio-compose/templates/bed_request.json` still has seed 2738136501 (the stated rule gives 2440031311) and `segment_role: hook`, which is not in the new enum. The music-10 example seed 995300448 recomputes correctly.
3. No filled Script Spec exists. Add a golden positive instance and negatives for the ten new allOf rules to P1-04.
4. Optional: v2 uses backticked paths, not markdown links, so CI cannot check cross-references. Convert the key ones to links.
5. Rulings still open: en-IN disclosure wording (RD-45 vs 07/06 §6.4), O-5, O-19 and O-22. Sign-off is also needed on CE-73…CE-110.
6. Outside-scope follow-ups: the 11 PLAYBOOK bed-level lines (row J), and the `access_tier` mentions in 07/12, 07/00 and 12/13 (P1-01).

## Addendum: completeness-critic items applied (15 Oct 2026, 7 agents)

Six writers with disjoint files and one Opus verifier. Leftovers 2 and 6 above are now closed.

| Item | Level | Where it landed | Decision |
|---|---|---|---|
| 1 Curriculum Framework | 1 | Arch §2.6, §3.1 `framework/`; `schemas/curriculum_framework`; TEMPLATES §6; `examleaf-curriculum-ingest` (SKILLS, CSV); P1-14 | CE-111 |
| 2 Rights basis | 1 | Arch §3.1 `rights/`, O-23; SRC `rights_basis`; Q-RIGHTS; SUBJECT §1.7; P1-17 | CE-112 |
| 3 Approval authenticity | 1 | Arch §2.2, §3.2, §3.7; `signature`, `signing_keys[]`; RELEASE-CHECK; P1-16 | CE-113 |
| 4 Storage and recovery | 1 | Arch §9.5; `content/blobs/sha256`; `retention_class`; M1 restore drill; P1-15 | CE-114 |
| 5 Incidents | 2 | Arch §9.6; `export/withdrawals.jsonl`; `reviewer/on-call`; Packaging §3, §12 | CE-115 |
| 6 Edition change model | 2 | Arch §3.6 framework diff; `valid_academic_years[]`; Packaging §12 | CE-116 |
| 7 Learning signals | 2 / 3+ | Arch §9.7; `schemas/learning_signal`; TEMPLATES §7; F15 intake | CE-117 |
| 8 Transcreation | 3+ | Arch §8; `adapted_from`, `locale_scope[]`; Q-LOC.meaning | CE-118 |
| 9 Print target | 3+ | Arch §3.3; `render_target: print`; F-W, F-TN, F-GN, Revision Sheet print; `packaging/print-pdf` | CE-119 |
| 10 Accessibility profiles | 3+ | Arch §3.1 `a11y/`; LP §4; Q-A11Y rows; VOICE §3.11; O-24, S-14, S-15 | CE-120 |
| 11 Representation audit | 3+ | Arch §7; `depicted_attributes`; Q-REPR (QA §2.13) | CE-121 |
| 12 Surge and freeze | 3+ | Arch §3.6, §11; `exam_windows[]`; LP §5; Roadmap §6 | CE-122 |

**Leftovers fixed.** MUSIC §2.1 item 1 now cites the corrected R8 (the old chain is struck). The `style_entry` description is corrected.

**Outside notes applied.** These are the PLAYBOOK bed-level lines (20–24 dB) and the `bed_request.json` scene `phy-10-03-reel01` with seed 995300448. They also cover the pos-1 case in `cases.json`, RD-53 in 07/10, and the `access_tier` notes in 07/12 (×2), 07/00 and 12/13.

**Verifier fixes.**
- Arch §2.6 used the example `framework/seba_hslc_science`, which fails the schema pattern `framework/<id>` and would have minted different GUIDs. It now uses `framework/seba_hslc_science`.
- Arch §3.7 now records the signature scope the schema uses (`state` and `reqa_records` as at signing).
- Arch §11 risk 1 gains the surge pointer.
- The counts are updated: subsystems §3 word counts, 91 skills (19 new), 55 files in the root README, and the Architecture word count.

| Check | Result |
|---|---|
| Draft-07 meta-validation, 21 schemas | pass |
| Commercial lint, 21 JSON files (keys, required, enum, const) | 0 hits |
| Template JSON examples | 6 concrete pass; 5 skeletons fail only on placeholder values, with no structural errors |
| Canonical names for 12 items | all present |
| GUIDs in TEMPLATES §6 recomputed | match |
| `00_source` changed today | 0 |
| `.py`/`.js`/`.sh` changed since 20:00 | none |
| audio-compose self-tests (compose_bed, sfx_palette) | OK; no eval runner exists |

## Lead closure of the verifier's leftovers (15 Oct 2026)

The critic-pass verifier left eleven items that were either lead decisions or one-line edits. The lead closed all of them directly, recorded as CE-123 (data-subject shredding keys; signatures required on every human gate; `a11y_isl` as an R1 Path A reason) and CE-124 (print accepted by the Script Spec with P1-19 to relax its video-only rules; Interaction Spec stays video and audio; sidecar print form and print disclosure decided at level 3; `framework`, `rights` and `a11y` in the §3.1 character-set sentence; `framework/<id>` form in every example; overlay `exam_windows` and the reviewer schema split wait for P1-11; ISL consent field level-3+; P1-18 schemas for blob manifest, ledger rows and withdrawals). The root README now counts 26 Format Specs (18 full, 8 compact), the SKILLS §9 note is marked resolved, and the `__pycache__` left by the self-test run was removed. Validation after these edits is in the table below.

| Check after the lead closure | Result |
|---|---|
| Draft-07 meta-validation of all 21 schemas | pass |
| Commercial-term lint over every JSON file under section 15 (property names, required entries, enum and const strings) | 0 hits |
| Signature rule covers the 13 human gates; A_SUITE and RELEASE_CHECK unsigned | pass |
| `00_source/` files modified today | 0 |
| Cache directories outside `00_source/` | 0 |
| Section 15 file count stated in the root README | 55, matches |
