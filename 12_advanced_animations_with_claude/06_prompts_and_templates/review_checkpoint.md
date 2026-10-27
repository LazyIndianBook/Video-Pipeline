# Review checkpoint: wording and what the human reviews

**Used by:** `examleaf-anim-storyboard-gate`; step "⛔ Review checkpoint" of `master_prompt_paper_collage_VERTICAL.md`; section 18 of `brief_template.md`. **Version:** 1.0.0 | **Date:** 15 Oct 2026.
**Source idea:** [V4-MP] stops after the script and storyboard ("show me, then wait for my approval") so credits are not wasted on rejected visuals (#47). ExamLeaf keeps the stop, removes the script from it (the script is already approved and is not the agent's), and binds the approval to hashes and a credit cap.

**Evidence labels:** [V#]/[N#] from `01_research/RESEARCH_REPORT_advanced_animations_with_claude.md`; [Recommendation] = design judgement. Edge cases #1-#65 (report §8). Project decisions RD-xx (`07_end_to_end_pipeline_instructions/10_DECISIONS_and_CONFLICT_RESOLUTIONS.md`).

## 1. What this checkpoint is, and is not

- It **is** the storyboard gate: a human approves the visuals, the style match and the credit estimate before any voice, paid asset or scene code is produced.
- It is **not** the academic script approval (GA). The script was approved earlier and must arrive unchanged. It is not the final full-video review (GF/GS) either.
- The agent can neither pass nor skip it. An approval is valid only if it is recorded by the approval service, or, until that service exists (RD-17), by a human reviewer in the job folder. Agents never write approvals (RD-32). *15 Oct 2026 (audit M10, RD-46): two approvals are needed (founder for cost, academic lead for science fit, two identities); the job folder's `storyboard/` is Edit-denied to the agent, and the runner verifies the record (service identities and signature, then `estimate_and_gate.py --verify-approval`) before any paid step.*

## 2. The checkpoint message (what the agent prints)

```text
⛔ REVIEW CHECKPOINT: STORYBOARD
Scene: <scene_id>   Lesson: <lesson_id>   Style: <style_id>@<style_version>   Storyboard: <storyboard_id>

1. SCRIPT (unchanged)
   Approved script: <script_path>
   SHA-256: <script_sha256>   (compare with the approved record before replying)
2. STORYBOARD
   Grid: storyboard/grid.png (3x3, nine 9:16 panels)   Beats: storyboard/beats.json
   Timings are PLANNED until the voice is generated and measured.
3. ESTIMATE
   <the CREDIT ESTIMATE line>
   Token estimate: <n or "unmeasured">   Effort: <effort_level>   Model: <effort_model>
4. STYLE MATCH
   <one paragraph: which style rules the panels follow; anything intentionally different>
5. SCIENCE-FREE PANELS
   <"Confirmed: no panel contains text, numbers, symbols, formulae, graphs or labelled
   diagrams; data-bound beats b__ b__ are placeholder cards." or a list of exceptions>

I am stopping here. I will not generate voice, assets or scene code until an approval
record exists that is bound to script_sha256=<script_sha256> and credits_max=<cap>.
I cannot approve my own work.
Approval line: APPROVED storyboard=<storyboard_id> script_sha256=<script_sha256> credits_max=<cap> reviewer=<role or name>
Or reply with the changes you want (at most 2 revision rounds).
```

## 3. What the human reviews

Tick every item; one failure means REVISE, NARROW or REJECT.

**A. Script unchanged**
- [ ] The hash in the message equals the hash in the approved script record.
- [ ] `beats.json` sentence IDs cover the whole script in order: no sentence added, dropped, reordered or reworded. Timing notes (for example "this sentence is too long for one beat") are advice to the script owner, not edits.

**B. Storyboard**
- [ ] Nine panels in beat order; each panel shows one idea that matches its sentence.
- [ ] Panel 1 carries the hook; the prediction or `think` beat does not show the answer; the last panel carries the single next action.
- [ ] Merged or unused panels are explained in `beats.json`.

**C. Estimate**
- [ ] The credit-estimate line is present. For Higgsfield it states the number of generations, the unit cost with its source, the total, the cap and the ledger path.
- [ ] No unit cost is invented. `UNVERIFIED` costs have been replaced by a human-supplied number, or the mode is code thumbnails (0 credits). Competitor-authored prices are not a source ([N75]).
- [ ] The cap is acceptable; no premium video models (RD-39); no retry loops that can double spend (#43, #44).
- [ ] The token and effort estimate is plausible: scene code at effort high, never ultracode (#1, #3).

**D. Style match**
- [ ] The look follows the style guide: palette, die-cut border and shadows (collage), stacked zones, text kinds, no 3D or gloss.
- [ ] The recurring character, if any, matches the hero sheet (#48).
- [ ] Setting cues are context, not costume; no stereotype, no caricature, no humiliation of a wrong answer. Any cultural accessory has native-reviewer sign-off.
- [ ] The tone fits the Super Teacher: warm, exacting, playful about the problem; no fake enthusiasm; at most the allowed light moments.

**E. Science-free panels**
- [ ] No panel contains text, numerals, symbols, formulae, graphs, labelled diagrams, or arrows with scientific direction (#54). Number tags exist only as review aids added in code.
- [ ] Every data-bound beat is a placeholder and names its fixture(s).
- [ ] No gag or decoration contradicts the science (for example a "tear in half" on a molecule, a bent ray).
- [ ] Nothing in a visual brief states a fact that the script does not state (#12).

**F. Layout, accessibility, audio plan**
- [ ] Top and bottom bands of each panel are quiet (title and caption zones); the composition is vertical, not a crop (#49, #51).
- [ ] No flash, strobe or full-frame brightness jump is implied (an "explosion" uses a paper burst, #56).
- [ ] A reduced-motion variant is planned.
- [ ] Music appears only in hook, transitions, recap and Reel beds; none under reasoning; no trending or unlicensed audio.

**G. Rights**
- [ ] Asset tiers are stated (A code-only, B own or licensed, C generated). Licences or job IDs will be recorded. No reference-creator artwork, no scraped images.

## 4. Outcomes

| Outcome | Meaning | Next |
|---|---|---|
| **APPROVE** | All items pass | The approval service records the approval line; the pipeline continues to voice, assets and scene code |
| **REVISE** | Specific fixes needed | The agent changes only what the reviewer named; re-estimates if credits are involved; at most 2 rounds [Recommendation] |
| **NARROW** | Too costly or too broad | Switch Higgsfield to code thumbnails, drop a scene, or change the style (re-opens the gate) |
| **REJECT** | Not viable | Stop; the human decides the replacement approach |

A request to change the script goes back to the script owner and the academic approval gate, changes the hash, and restarts this checkpoint.

## 5. The approval record

Written by the approval service or a human reviewer, never by the agent.

*Superseded 15 Oct 2026 (audit M10):* the single-role shape below (`reviewer_role`) is kept for history only. The canonical record is `12_advanced_animations_with_claude/03_skills/examleaf-anim-storyboard-gate/templates/approval_record.json` (schema 1.1): `approvers[]` with `founder` (cost) and `academic_lead` (science fit), plus `fixture_hashes`, `style_hash`, `hero_hash` and the bound estimate/beats/grid/script hashes (doc 05 §5.1). The approval line above is given once per role.

```json
{
  "schema_version": "1.0.0",
  "storyboard_id": "<storyboard_id>",
  "scene_id": "<scene_id>",
  "script_sha256": "<64 hex>",
  "grid_sha256": "<64 hex>",
  "beats_sha256": "<64 hex>",
  "estimate_sha256": "<64 hex>",
  "style_id": "<style_id>",
  "style_version": "<style_version>",
  "credits_max": 0,
  "decision": "APPROVED",
  "reviewer_role": "<role>",
  "reviewed_at": "<ISO 8601 time>",
  "notes": ""
}
```

**It stops being valid when any of these change:** the script hash; the grid, beats or estimate hash; the style ID or version (a major version change); the credit cap; the safe-zone tokens used for the layout. Material changes require a new checkpoint.

## 6. Reviewer guidance

- Approve what is on the page. "Looks good" is not an approval line; the agent will keep waiting.
- Look at the grid on a phone-sized view as well as a monitor; the final video is watched on small screens.
- If the cost line is `UNVERIFIED`, do not approve until a person has supplied a number from a real source.
- Prefer NARROW to approving an expensive look that was not needed. The zero-credit doodle style is the default for Reels [Recommendation].
- Record why you rejected a panel, so the next round fixes it once.

## 7. Edge cases

#11, #12 (script and facts untouched), #41, #42, #43, #45 (estimate and cap), #47 (gate), #48 (hero consistency), #49, #51 (vertical, safe areas), #54 (science-free panels), #56 (no flashes), #60 (revision cap).
