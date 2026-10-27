# Storyboard gate procedure

## 1. Where the gate sits (report §9)

```text
script approved (academic ⛔) -> storyboard-route tags scenes -> [THIS GATE: grid + beats + estimate ⛔]
  -> assets (selective-generation via mcp-orchestrator) -> brief -> scene authoring -> harness lint/hash
  -> composition -> anim-qa -> release-review ⛔
```

Narration synthesis and alignment run on their own approved path (`examleaf-voice-synthesis`, `examleaf-alignment-localize`); the gate does not block them, but scene authoring needs both the gate approval and the cue sheet.

## 2. Beats

- One sentence of the approved script = one visual beat ([V4-MP] sync rule).
- A lesson segment is cut into grids of nine beats (3×3); a 60 s Reel at the [V4-MP] density is usually one grid.
- Each beat records the scene, its order, a one-line description of what is on screen, and the cue ID it will be keyed to once the cue sheet exists.
- Descriptions are written from the approved script and storyboard route only. If a beat needs a fact, it names the fixture field ("angle_r_deg from fx-refraction-glass"), never a value typed from memory.

## 3. Code-thumbnail recipe (default)

1. For each beat, build a draft scene (or reuse the scene draft if it exists) that implements the contract (`window.DURATION`, `async window.seek(t)` [N72]).
2. Seek to the beat's representative time (the cue time if known, otherwise the beat midpoint) and capture a 1080×1920 still through the harness's still render.
3. Downscale panels to a common size and tile them 3×3 with FFmpeg's `tile` filter (standard usage, verify on your build), with a thin gutter in the style's background colour.
4. Overlay panel numbers in code (SVG/HTML), not by an image model.
5. Thumbnails may be rough (flat fills, placeholder characters drawn as simple shapes) but must show the real composition: zones, what reveals on which word, and where text sits.

Why code first: no credits, the reviewer sees the actual vertical composition and the actual fonts, and the same code becomes the scene.

## 4. When a generated grid is justified

Only when all of these hold:
- the style is `paper-collage-vertical` (or another style that depends on raster cutouts);
- the beat's meaning depends on a character or prop look that does not yet exist in the asset library;
- a human approved the credit estimate for the grid.

Then: one job through `examleaf-mcp-orchestrator` → `examleaf-selective-generation`, using `06_prompts_and_templates/storyboard_request.md`; nine portrait panels; "no text" in the prompt; the hero reference image attached ([V4-MP] cutout guidance); job ID logged. [V4-MP] asks for "one 16:9 image with 3×3 panels"; ExamLeaf asks for portrait panels instead (vertical adaptation).

## 5. Reviewer checklist (paste into `review_checkpoint.md`)

- [ ] Every beat matches one sentence of the approved script, in order.
- [ ] Nothing on screen states a fact that is not traceable to a fixture.
- [ ] Each panel is a readable 9:16 composition: title zone, visual zone, caption zone respected.
- [ ] One idea per panel; reveals spread across the scene.
- [ ] Recurring character looks the same in every panel (#48).
- [ ] No text, labels or formulas drawn by an image model (#54).
- [ ] No full-frame flash or rapid luminance pattern implied (#56).
- [ ] No decorative motion that would contradict the science (report §7.13).
- [ ] Estimate: expected and worst-case tokens and credits are within caps, or an override reason is written.
- [ ] Style `id@version` is approved (or this is a declared pilot).

Decision: approve / approve with notes / reject with notes. Approval is recorded by the reviewer, never by the agent. *15 Oct 2026 (audit M10, RD-46):* two approvals are required, from two different identities: the founder (cost) and the academic lead (science fit with the approved script and fixtures). Each is recorded in the RD-17 approval service; the runner verifies identities and signature there and then runs `--verify-approval` (roles plus estimate/beats/grid/script/fixture/style/hero hashes). The agent's workspace denies `Edit(./storyboard/**)`.

## 6. Re-approval triggers

| Change | Why it invalidates | Action |
|---|---|---|
| Script hash changed | Beats derive from the script | Re-run gate |
| Style version changed | Look and cost change | Re-run gate |
| Beats or grid edited | Bound hashes differ | Re-run gate |
| Estimate rose above the approved one | Spend authority exceeded | New estimate approval |
| TTS regenerated only (#63) | Timing, not visuals | No re-approval; cue sheet rebuild only |

## 7. Failure modes and responses

- **Agent tries to continue after presenting the grid** → `--verify-approval` exits 1; the job runner stops the stage.
- **Generated grid arrives late** → wait and reconcile by job ID; do not resubmit [N35].
- **Throttling during batch storyboards** → off-peak batches, backoff (#44, handled by mcp-orchestrator) [N80].
- **Reviewer unavailable** → segment waits; no "auto-approve after timeout".
