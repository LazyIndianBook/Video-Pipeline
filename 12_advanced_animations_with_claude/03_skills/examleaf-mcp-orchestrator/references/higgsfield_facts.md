# Higgsfield: verified facts, contested claims and unknowns

The status labels follow `12_advanced_animations_with_claude/01_research/SOURCES_and_claims.md`:
- **unanimous** = both verifiers confirmed;
- **contested** = one verifier did not;
- **competitor-authored** = from a rival vendor's blog.

Nothing here was tested by a live call.

## 1. Connection paths

| Path | Claim | Source | Status |
|---|---|---|---|
| claude.ai custom connector | URL `https://mcp.higgsfield.ai/mcp`, added under Settings → Connectors | [N29] Higgsfield help centre | **contested** |
| ChatGPT | "ChatGPT uses the official Higgsfield Plugin from the Plugins Directory" (no URL) | [N30] | **contested** |
| CLI agents (Claude Code, etc.) | `npm i -g @higgsfield/cli`, then `higgsfield auth login` | [N31] | unanimous |
| Web flow in [V4] | "install Higgsfield MCP" → "connect to Higgsfield" → continue (pre-filled) | [V4] video (sponsored by Higgsfield) | Demonstration only |

The project's earlier research also lists the official Skills repository (`github.com/higgsfield-ai/skills`), the CLI repository (`github.com/higgsfield-ai/cli`) and a separate API offering (`04_video_engine/implementation_v2/docs/Higgsfield_Findings.md`).

**ExamLeaf stance:** the CLI path in the provider worker is the candidate, because it is unanimous and scriptable. Any install is an `examleaf-skills-security` admission:
- confirm the publisher;
- inspect the package;
- pin a version or digest;
- test in isolation;
- block auto-update.

The global `-g` install in [N31] needs particular care: install into the worker image, not a developer laptop with broad credentials.

## 2. Capabilities seen

| Capability | Where seen | ExamLeaf use |
|---|---|---|
| Image generation with a selectable model; GPT Image 2.5 (`gpt_image_2_5`) | [V4-MP] Step 3, §12 | 3×3 storyboard grid; collage cutouts (transparent, 2K) and backgrounds |
| `text2speech_v2` with an ElevenLabs variant and preset voices ("Arthur", a specific voice_id) | [V4-MP] Step 4 | **Exploratory storyboards only.** Production voice uses ExamLeaf's TTS adapter (report §5.3) |
| 15+ aggregated video models | [N78] (competitor blog) | **Not used.** Premium video is avoided entirely (report §6.1) |
| Audio generation and the Website Building skill are not available in ChatGPT | [N32] | Edge case #46. ExamLeaf audio does not go through MCP anyway |

[V4] calls the paper-collage style "on the expensive side regarding credits" because it needs many individual assets.

## 3. Credit facts (official help centre, unanimous)

- [N33] "Every generation through a connected agent deducts credits, regardless of your plan." Unlimited and free generations do not apply via MCP.
- [N34] "There's no native credit cap." Prompt-level limits are not hard limits. **The pipeline ledger is the only cap.**
- [N35] "Results typically appear within 60 seconds of the job completing." Otherwise check Manage Account → Usage.

The earlier project research adds a billing distinction: "MCP/CLI account credit use, web Unlimited use and separate developer API pricing are not the same billing product. No exact authenticated ten-minute Higgsfield quote was obtained" (`Higgsfield_Findings.md`).

## 4. Plan figures (competitor-authored, unverified)

| Claim | Source | Use |
|---|---|---|
| Starter $15/month for 200 credits; Plus $34/month for 1,000 credits | [N75] creatify.ai | Planning only |
| Premium video models (e.g. Veo 3.1, Kling 3.0) use 40–70 credits per generation | [N76] | Reason to avoid premium video |
| Starter's 200 credits run out in 3–5 days of active premium use | [N77] | Edge case #45 sizing |
| Unlimited covers lower-tier models only | [N79] | MCP calls are billed regardless [N33] |
| Unlimited may be throttled at peak | [N80] | Edge case #44 |

Never put these figures into a reservation `--estimate-source`. Reservations use the account's own model page, estimate call or price list, with the date captured.

## 5. What ExamLeaf will and will not use it for (report §6.1 [Recommendation])

**Will:**
1. 3×3 storyboard grids at the review gate, when code thumbnails are not enough for look development;
2. optional collage cutouts and backgrounds for `paper-collage-vertical` hooks, analogies and recaps.

**Will not:**
- labelled science, or any text, formula, label or number in an image (#54);
- premium video models;
- production narration;
- "full permission to use all the MCPs" ([V3] demo).

## 6. The cutout prompt pattern ([V4-MP] §12)

The master prompt's cutout template asks for a single isolated object on a FULLY TRANSPARENT background, die-cut white border, flat straight-on view, no cast shadow, no ground, no scenery, **no text**, house palette, and "Match the character designs and art style of the attached storyboard sheet."

- Attach the approved grid or an earlier cutout as the image reference (#48).
- Trim transparent margins before use.
- Background prompts are opaque. Re-specify the aspect for 9:16, because the [V4-MP] backgrounds are 16:9 (#49; see `examleaf-vertical-adapt`).
- **Built in code, never generated:** ransom letters, captions and tags, washi tape, confetti, doodles, underlines, and screens or simple UI ([V4-MP] §12).

## 7. Open vendor questions (report §11 item 5)

| Question | Why it matters | Owner |
|---|---|---|
| Is the MCP URL path [N29] or the CLI [N31] the supported route for Claude Code? | Admission and pinning | Ops + skills-security |
| Per-model credit costs for image and TTS | Real estimates for reservations | Ops |
| Actual plan prices (the [N75] figures are competitor-authored) | Budget sizing | Founder |
| API-level spend caps | Defence in depth beyond our ledger | Ops |
| Data retention of uploaded storyboards | Privacy; no student data ever | Founder + legal |
| Licence and ownership of generated assets for commercial education | Rights quarantine in asset-library | Legal |
| Indian-English and Hindi voice quality via the ElevenLabs variant | Only relevant to exploratory storyboards | Narration lead |
