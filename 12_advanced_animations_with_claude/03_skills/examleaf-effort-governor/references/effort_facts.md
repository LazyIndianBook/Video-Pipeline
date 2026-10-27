# Effort, model and thinking facts

All [N#] quotes are from https://code.claude.com/docs/en/model-config, as recorded in `01_research/SOURCES_and_claims.md`. [N28]'s row notes "page partly unread". Re-read the live page when Claude Code updates. [V1] is one creator's measurement and [V2] is a tutorial. Nothing here was measured by ExamLeaf.

## 1. Levels and defaults

| Fact | Quote / evidence | Source | Status |
|---|---|---|---|
| Levels in use | low, medium, high, xhigh, max, plus ultracode (a separate multi-agent mode after max on the app slider) | [V1] | Observed |
| Defaults | "`high` on every model that supports effort, except that Opus 5.5, Sonnet 5.5, and Haiku 5.5 default to `medium`" | [N22] | unanimous |
| Fallback | "Claude Code falls back to the highest supported level at or below the one you set." Example: xhigh runs as high on Opus 4.6 | [N23] | unanimous |
| Guidance | Opus 5.5 at high or xhigh ("extra") for JS animation; max only "if… incredibly complex"; "99% of the time you won't need anything more than extra" | [V2] | Tutorial |
| Quality vs effort | Low produced 2D; medium to max produced 3D; the ultracode run mixed both. Improvements from medium to max were visible, but low was "still good" | [V1] | Single creator |

**Consequence (#1).** Opus 5.5 left unset runs at medium. ExamLeaf always passes the effort explicitly per run and logs it.

## 2. Ultracode

| Fact | Quote / evidence | Source |
|---|---|---|
| Launch | "launch with `claude --effort ultracode`, which starts the session at `xhigh` effort with ultracode on" | [N24] |
| Not persistable | "The persisted `effortLevel` setting and the `CLAUDE_CODE_EFFORT_LEVEL` environment variable don't accept `ultracode`." | [N25] |
| Cost blow-up | Set by mistake as max + ultracode: at least 2.5 million tokens (at least 4× the max run), at least $348 estimated at API prices; "almost three 5-hour limits" on a Max plan; never finished, and stopped while "trying to fix the video" | [V1] |
| Mechanism | "kept reviewing the video with multiple agents"; each agent built its own cache in its own session; unfinished agents restarted fresh after the limit | [V1] |
| Creator's advice | "Don't use Ultra Code". If you must, try it at low effort in the terminal (untested by him) | [V1] |

**Consequences (#3, #4).** Ultracode is refused in every ExamLeaf run, and `effort_policy.py` exits 1 on it. Because settings and the env var reject it, the only way in is the launch flag, so audit launch scripts for `--effort ultracode`.

## 3. Thinking

- "You can't turn thinking off on Opus 5.5, Sonnet 5.5, Haiku 5.5, or the Fable models." [N26]
- **Consequence (#5):** some thinking cost is always present. Budget for it inside output tokens, and use a lower effort for clerical tasks.
- "set `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1` to revert to the previous fixed thinking budget controlled by `MAX_THINKING_TOKENS`" applies to 4.6 models [N27]. It is **contested** and not applicable to 5.5. Do not use it.

## 4. Model identity

- "aliases resolve to the newest version on the Anthropic API and to an earlier version on some other providers" [N28].
- **Consequence (#6):** pin the full model ID in `model_pins.json`, taken from the current model catalog. The production plan refuses placeholders.
- Haiku 5.5 prompts over 100K tokens cost more per token [N28] (#61). Keep Haiku prompts short, or route to Sonnet.
- Opus 5.5 has a 1M-token context and up to 128K output tokens, "as of" a tutorial [N73]. **Recheck** the catalog; split long scene files (#58).
- [N59] (a third-party tutorial with no link) dates Opus 5.5 to 22 Sep 2026; it is unverified (#59).
- Fable 5.5 ([V5]) is unverified. The "Fable" family exists [N26], but plan nothing on it (#57). Any model switch re-runs determinism and science QA (AD-03).

## 5. Operational rules (report §3.4 [Recommendation])

1. Run headless in the terminal, one workspace per job ([V1] used the terminal, not the app, to avoid "fill[ing] up my chat list"; [V2] keeps the model contained in one folder).
2. Tell the agent not to read sibling project folders ([V3]: "do not inspect any of my older projects or folders"), and enforce it with permissions (#9).
3. Cap iteration rounds. The report's example is 3 fix loops per scene; ExamLeaf's AD-11 sets 3 authoring loops, plus the VE rule of 2 repair attempts after automated failures.
4. Never use "don't stop until perfect" without a budget (#60). [V2]'s L3 prompt contained "don't stop working until the animation matches the exact quality of the reference video", and [V1]'s prompt said "work on its own from start to finish and not to stop and ask".
5. Log tokens per run to `examleaf-observability-cost`.

## 6. Caching (what is and is not known)

- **Observed** ([V1]): multi-agent work multiplies cache-creation cost, because each sub-agent caches separately and restarts fresh after a limit.
- **Recommended** (report §3.3):
  - one main session per scene batch;
  - stable context at the start of the prompt, unchanged between scenes;
  - in order: harness contract, style guide, brand tokens, fixtures.
- **Not verified:** exact cache lifetimes, minimum cacheable sizes, and cache read and write prices. Confirm them in the Claude API documentation before putting cache savings in a cost model. Until then, log `cache_read` and `cache_write` counts and let the measurements speak.

## 7. Questions for Anthropic (report §11 item 1)

- Is there an official "Claude Motion" feature? None is verified; treat it as a community term (AD-10).
- What are the confirmed Opus 5.5 release date and current context and output limits?
- How does prompt caching behave across ultracode sub-agents?
- Is there an official cost per effort level?
