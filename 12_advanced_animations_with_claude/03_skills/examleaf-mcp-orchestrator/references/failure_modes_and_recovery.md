# MCP failure modes and recovery

Each row: what you see, why it happens, how to detect it, and the exact recovery. Credit facts: [N33] every agent generation is billed; [N34] no native cap; [N35] results within about 60 s of completion, else Usage. The [Hypothesis] in report §6.4 applies throughout: "The agent retries a failed generation and silently doubles spend." Most rules below exist to stop that.

## 1. Result late or missing (#43)

- **Symptom:** the call returned a job ID, but no asset appeared.
- **Cause:** delivery takes "within 60 seconds of the job completing" [N35]; completion itself can take longer.
- **Detect:** `credit_ledger.py due --window-s 60` lists submitted jobs older than the window.
- **Recover:**
  1. wait out the window;
  2. look up the job ID in Manage Account → Usage [N35];
  3. if the result is there, fetch it by job ID and then `commit`;
  4. if the job is not visible, run `mark-unknown`. The job still counts against the cap.
- **Never** resubmit an unknown job. A second submission is a second bill [N33].

## 2. Error returned with no job ID

- **Symptom:** a transport error or timeout before an ID came back.
- **Risk:** the provider may have created the job anyway.
- **Recover:**
  1. check the provider's job list or Usage for a job created in that minute with the same prompt;
  2. if one exists, record its ID with `submit` and continue at §1;
  3. if none exists after the 60 s window, retry **the same job key**. `reserve` is a no-op, so no double reservation is made. Back off 60 s, then 120 s, with at most two retries;
  4. after that, escalate.

## 3. Throttling (#44)

- **Symptom:** slow responses, queued jobs, a stalled batch.
- **Cause:** "Unlimited usage may be throttled during high-traffic periods" [N80] (competitor blog).
- **Recover:**
  - slowness is not failure; do not cancel and resubmit;
  - run batches off-peak;
  - use one job at a time per scene, which also keeps reconciliation simple;
  - for transport errors use the §2 backoff.
- Report the stall to ops with timestamps, so the off-peak window can be measured. No verified peak times exist.

## 4. Cap reached or overrun (#42, #45)

| Event | Ledger behaviour | Human action |
|---|---|---|
| Reserve would exceed the cap | `reserve` exits 3 before any call | Approve a cap increase for this lesson (recorded), drop the asset, or use a code illustration |
| Actual > estimate | `commit` records `estimate_exceeded: true` and a warning | Fix the estimate source for future reservations |
| Exposure > cap after commit | Ledger **frozen**; `commit` exits 4 | Founder or ops review; `unfreeze --approver <name> --note <reason>`; the cap still binds new reservations |
| Plan credits exhausted mid-lesson | Provider refuses or errors | Stop cleanly. The ledger shows exactly which assets exist. Resize the plan from measured usage; competitor figures say Starter's 200 credits last 3–5 days of premium use [N75][N77] |

## 5. Character drift (#48)

- **Symptom:** the hero looks different from shot to shot.
- **Cause:** independent generations.
- **Prevent:** always attach the approved storyboard grid or the canonical hero cutout as the image reference ([V4-MP] §4, §12). Make pose variants (pointing, crying, cheering, waving) from the same reference.
- **Recover:** one repair attempt with a stricter reference and prompt. If it still drifts, use the existing cutout with a code-side pose change: flip, rotate, or a squash per `examleaf-procedural-2d`. A third generation is not allowed (two-repair limit).

## 6. Text or labels in a generated image (#54)

- **Detect:** human intake check at phone scale, plus an OCR pass where available. Any glyph means reject: image models produce "misspelled labels, wrong equations" (report §8).
- **Recover:** regenerate once with "no text" reinforced, and remove from the prompt every noun that implies writing (sign, label, poster, book cover). Then fall back to a code-drawn equivalent. Never inpaint or "fix" text in a raster; text is always built in code.

## 7. MCP text drifts from the approved script (#11)

- **Where it happens:** exploratory storyboard voice via `text2speech_v2`, panel captions, or any MCP that "helpfully" rewrites text ([V3]: the AI-written script was the weak point).
- **Detect:** run `transcript_check(approved, sent_or_returned, critical_phrases)` from `examleaf_narration.qa`.
  - `edit_count > 0` or a non-empty `critical_mismatches` blocks.
  - The comparator is English and surface-level; Indic text needs a native reviewer.
- **Recover:** resend with the approved text verbatim. The orchestrator never edits approved text.

## 8. Wrong platform for audio (#46)

- **Symptom:** no audio tool in a ChatGPT session.
- **Cause:** "Audio generation and the Website Building skill aren't available in ChatGPT" [N32].
- **Recover:** the CLI agent or claude.ai path [N31]/[N29]. In ExamLeaf, production audio does not use MCP at all.

## 9. Gate skipped (#47)

- **Symptom:** an asset call with no storyboard approval record, or one whose hash does not match.
- **Recover:** refuse. Credits spent on rejected visuals are what [V4]'s review checkpoint exists to prevent.

## 10. Recovery decision tree

```text
call made? ── no ──> (blocked before spend: fix grant/estimate/lint/gate)
   │yes
job id? ── no ──> check usage/job list ── found ──> submit(id) ─┐
   │yes                                 └ none after 60 s ──> same-key retry (≤2, backoff 60→120 s)
   ▼                                                             │
result within 60 s of completion? ── yes ──> commit(actual) ──> intake (no-text check, hash, asset-library)
   │no
   ▼
due ──> usage page ── found ──> fetch by id ──> commit
                   └ not found ──> mark-unknown ──> escalate (never resubmit)
```
