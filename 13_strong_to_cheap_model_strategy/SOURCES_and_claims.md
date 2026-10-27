# Sources and evidence status

**What the status labels mean:**
- **Verified** means the quote was checked against the cited page by the research pipeline.
- **Contested** means a verifier disagreed or the figure conflicts with another source. Re-measure these on ExamLeaf before relying on them.

**Supplementary sources:**
- **[D#]** entries are Anthropic API notes I checked against the bundled Claude API reference skill (cached 2026-10-06).
- **[P#]** entries are ExamLeaf project files.
- **[V1]** is the internal reference experiment.

## Evidence list [N1]–[N96]

### Haiku 5.5 release coverage (computingforgeeks)

- **[N1]** Haiku 5.5 lists at $0.10 in / $0.50 out per MTok.
  - Quote: "Claude Haiku 5.5 costs $0.10 per million input tokens and $0.50 per million output"
  - Source: https://computingforgeeks.com/claude-haiku-5-5-released-features-benchmarks/
  - Status: Verified
- **[N2]** The new tokenizer uses up to 36% more tokens than Haiku 4.5 on English prose and YAML.
  - Quote: "English prose and YAML took the biggest hit at 36%."
  - Source: same page as [N1]
  - Status: Verified. Note that the comparison is against Haiku 4.5, not Opus 5.5.
- **[N3]** At low effort, 8/8 Python tasks passed versus 4/8 for Haiku 4.5, at about a tenth of the cost.
  - Quote: "At low effort, Haiku 5.5 solved every task, finished faster than Haiku 4.5 and cost a tenth as much."
  - Source: same page
  - Status: Contested
- **[N4]** Terminal-Bench 4.0: 39.2% versus 70.6% for Sonnet 5.5.
  - Quote: "Terminal-Bench is the gap that stays wide: 39.2% against 70.6% for Sonnet 5.5."
  - Source: same page
  - Status: Verified
- **[N5]** Bills 5x the base rate above 100K-token prompts.
  - Quote: "Haiku 5.5 charges five times its base rate once the prompt passes 100K tokens"
  - Source: same page
  - Status: Contested. It is consistent with [N20] and [N82].
- **[N6]** 1M-token context window.
  - Quote: "The context window grew five times, which puts a 1M-token window on the cheapest Claude model"
  - Source: same page
  - Status: Verified
- **[N7]** About 2x faster text output with thinking off at low effort.
  - Quote: "With thinking off, Haiku 5.5 starts as fast as Haiku 4.5 and writes text about twice as fast."
  - Source: same page
  - Status: Verified
- **[N8]** Prompt-injection attack success fell from 58.4% to 0.08%.
  - Quote: "the attack success rate fell from 58.4% on Haiku 4.5 to 0.08%"
  - Source: same page
  - Status: Verified

### Anthropic: prompting Claude Haiku 5.5

- **[N9]** Moving from low to medium effort roughly halved early stopping and more than doubled output tokens.
  - Quote: "moving from `low` to `medium` effort roughly halved early stopping. It also more than doubled the output tokens"
  - Source: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5
  - Status: Verified
- **[N10]** Sometimes reports a code change as done without running a check.
  - Quote: "sometimes reports a code change as done without running a check"
  - Source: same page
  - Status: Contested
- **[N11]** Adding the date plus a search nudge added searches on only 0–3% of no-search prompts.
  - Quote: "it added searches in only 0–3 percent of tries."
  - Source: same page
  - Status: Verified
- **[N12]** Blanket "always search" instructions caused searches on half of the prompts that needed none.
  - Quote: "that instruction made the model search on half of the prompts that needed no search"
  - Source: same page
  - Status: Contested
- **[N13]** With thinking off plus JSON output, the model may skip a needed tool call.
  - Quote: "With thinking off, Claude Haiku 5.5 might skip a tool call it needs when you also request JSON output"
  - Source: same page
  - Status: Verified
- **[N14]** Changing the top-level effort value invalidates the messages cache.
  - Quote: "Changing the top-level `effort` value between requests invalidates the prompt cache for the conversation's messages."
  - Source: same page
  - Status: Verified
- **[N15]** Reasoning-like text leaks more often with thinking off or at low effort.
  - Quote: "This happens more often with thinking off or at `low` effort."
  - Source: same page
  - Status: Verified
- **[N16]** Refusals have no server-side fallback, and retries usually refuse again.
  - Quote: "Sending the same request to Claude Haiku 5.5 again usually returns another refusal."
  - Source: same page
  - Status: Verified

### Anthropic: pricing

- **[N17]** Fable 5.1 pricing row.
  - Quote: "Claude Fable 5.1 / $10 / MTok / $12.50 / MTok / $20 / MTok / $0.25 / MTok / $50 / MTok". The table delimiters are rendered as slashes.
  - Source: https://platform.claude.com/docs/en/about-claude/pricing
  - Status: Verified
- **[N18]** Opus 5.5 pricing row.
  - Quote: "Claude Opus 5.5 / $4 / MTok / $5 / MTok / $8 / MTok / $0.20 / MTok / $20 / MTok"
  - Source: same page
  - Status: Verified
- **[N19]** Sonnet 5.5 pricing row.
  - Quote: "Claude Sonnet 5.5 / $2 / MTok / $2.50 / MTok / $4 / MTok / $0.10 / MTok / $10 / MTok"
  - Source: same page
  - Status: Verified. The $0.10 cache-read figure conflicts with the supplied price block and [D11], which both give $0.20. The strategy uses $0.20.
- **[N20]** Haiku 5.5 pricing row, for prompts up to 100K tokens.
  - Quote: "Claude Haiku 5.5 (for prompts up to 100,000 tokens) / $0.10 / MTok / $0.125 / MTok / $0.20 / MTok / $0.01 / MTok / $0.50 / MTok"
  - Source: same page
  - Status: Contested (the ratio wording). The prices themselves are consistent with [N1], [N40] and [N80].
- **[N21]** The Batch API gives 50% off input and output.
  - Quote: "The Batch API allows asynchronous processing of large volumes of requests with a 50% discount on both input and output tokens."
  - Source: same page
  - Status: Verified
- **[N22]** Caching break-even: one read for the 5-minute TTL, two reads for the 1-hour TTL.
  - Quote: "caching pays off after one cache read for the 5-minute duration (1.25x write), or after two cache reads for the 1-hour duration (2x write)"
  - Source: same page
  - Status: Contested

### Anthropic engineering: agent skills

- **[N23]** SKILL.md needs YAML frontmatter with a name and description.
  - Quote: "must start with YAML frontmatter that contains some required metadata"
  - Source: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
  - Status: Contested
- **[N24]** Only the name and description preload at startup.
  - Quote: "At startup, the agent pre-loads the `name` and `description` of every installed skill into its system prompt."
  - Source: same page
  - Status: Verified
- **[N25]** Progressive disclosure: bundled files are read only as needed.
  - Quote: "which Claude can choose to navigate and discover only as needed."
  - Source: same page
  - Status: Contested
- **[N26]** Bundled context is effectively unbounded.
  - Quote: "the amount of context that can be bundled into a skill is effectively unbounded."
  - Source: same page
  - Status: Verified
- **[N27]** Scripts run without entering context.
  - Quote: "Claude can run this script without loading either the script or the PDF into context."
  - Source: same page
  - Status: Verified
- **[N28]** Split SKILL.md when it becomes unwieldy.
  - Quote: "When the `SKILL.md` file becomes unwieldy, split its content into separate files and reference them."
  - Source: same page
  - Status: Verified
- **[N29]** Install skills from trusted sources only.
  - Quote: "We recommend installing skills only from trusted sources."
  - Source: same page
  - Status: Contested
- **[N30]** Distil successful approaches and mistakes into skills.
  - Quote: "ask Claude to capture its successful approaches and common mistakes into reusable context and code within a skill."
  - Source: same page
  - Status: Verified

### Small open models in production (arXiv 2312.14972)

- **[N31]** 5x–29x cost reduction compared with GPT-4.
  - Quote: "a cost reduction of 5x-29x when compared to OpenAI GPT-4"
  - Source: https://arxiv.org/abs/2312.14972v1
  - Status: Verified
- **[N32]** The study evaluated 9 SLMs and 29 variants.
  - Quote: "across 9 SLMs and 29 variants"
  - Source: same page
  - Status: Verified
- **[N33]** Competitive quality of results for the authors' use case.
  - Quote: "competitive quality-of-results for our use case"
  - Source: same page
  - Status: Verified
- **[N34]** Better performance consistency.
  - Quote: "significant performance consistency improvement"
  - Source: same page
  - Status: Verified

### Haiku 5.5 benchmarks (apidog)

- **[N35]** OSWorld 2.1: 72.4% at max effort.
  - Quote: "Claude Haiku 5.5 scores 72.4% on OSWorld 2.1"
  - Source: https://apidog.com/blog/claude-haiku-5-5-benchmarks/
  - Status: Contested. This is a max-effort figure and is not used to justify medium effort.
- **[N36]** GDPval-AA at medium is 1277, versus 1620 at max.
  - Quote: "at the default `medium` effort, GDPval-AA drops to 1277"
  - Source: same page
  - Status: Contested
- **[N37]** The widest gap with Sonnet is Terminal-Bench 4.0.
  - Quote: "The widest gap is Terminal-Bench 4.0: 39.2% versus 70.6%."
  - Source: same page
  - Status: Verified
- **[N38]** At max effort, edges Sonnet on FrontierCode Main.
  - Quote: "At max effort, Haiku 5.5 edges Sonnet 5.5 on Main, 46.4% to 46.2%."
  - Source: same page
  - Status: Verified. This is a max-effort figure.
- **[N39]** Max effort costs about 28x medium on GDPval-AA.
  - Quote: "On GDPval-AA, max costs about 28x medium for 343 more Elo points."
  - Source: same page
  - Status: Verified
- **[N40]** Price for prompts up to 100K tokens.
  - Quote: "$0.10/$0.50 per million tokens for prompts up to 100K tokens"
  - Source: same page
  - Status: Verified
- **[N41]** Tools nearly double the Chartography score.
  - Quote: "Chartography nearly doubles with tools (46.4% to 86.2%)"
  - Source: same page
  - Status: Verified. No effort level is stated.
- **[N42]** The tokenizer yields about 30% more tokens than Haiku 4.5.
  - Quote: "The new tokenizer produces about 30% more tokens than Haiku 4.5's for the same text."
  - Source: same page
  - Status: Verified. Again, the comparison is against Haiku 4.5.

### Anthropic: structured outputs

- **[N43]** Compiled grammars are cached for 24 hours.
  - Quote: "Compiled grammars are cached for 24 hours from last use, making subsequent requests much faster"
  - Source: https://platform.claude.com/docs/en/build-with-claude/structured-outputs
  - Status: Verified
- **[N44]** At most 20 strict tools per request.
  - Quote: "Maximum number of tools with `strict: true`. Non-strict tools don't count toward this limit."
  - Source: same page
  - Status: Contested
- **[N45]** At most 24 optional parameters.
  - Quote: "Total optional parameters across all strict tool schemas and JSON output schemas."
  - Source: same page
  - Status: Contested
- **[N46]** At most 16 anyOf or type-array parameters.
  - Quote: "Total parameters that use `anyOf` or type arrays (for example, `"type": ["string", "null"]`) across all strict schemas."
  - Source: same page
  - Status: Contested
- **[N47]** Schema compilation times out at 180 seconds.
  - Quote: "As a final stop-gap, the API also enforces a compilation timeout of 180 seconds."
  - Source: same page
  - Status: Verified
- **[N48]** `minItems` accepts only 0 or 1.
  - Quote: "Array `minItems` (only values 0 and 1 supported)"
  - Source: same page
  - Status: Verified
- **[N49]** The deprecated `output_format` needs a beta header or returns 400.
  - Quote: "To use it anyway, add the `structured-outputs-2025-11-13` beta header. Without it, the API returns a 400 error."
  - Source: same page
  - Status: Contested

### Anthropic: prompt caching

- **[N50]** Default 5-minute cache lifetime, refreshed free on each use.
  - Quote: "By default, the cache has a 5-minute lifetime. The cache is refreshed for no additional cost each time the cached content is used."
  - Source: https://platform.claude.com/docs/en/build-with-claude/prompt-caching
  - Status: Verified
- **[N51]** 1-hour TTL writes cost 2x.
  - Quote: "You can specify a 1-hour TTL at 2x the base input token price:"
  - Source: same page
  - Status: Verified
- **[N52]** 5-minute writes cost 1.25x.
  - Quote: "5-minute cache write tokens are 1.25 times the base input tokens price"
  - Source: same page
  - Status: Verified
- **[N53]** Cache reads cost 0.1x, with per-model exceptions.
  - Quote: "Cache read tokens are 0.1 times the base input tokens price (see the table footnote for per-model exceptions)"
  - Source: same page
  - Status: Contested
- **[N54]** Minimum cacheable length is 4,096 tokens for Opus 4.6 and 4.5.
  - Quote: "4,096 tokens for Claude Opus 4.6 and Claude Opus 4.5"
  - Source: same page
  - Status: Verified, but it does not apply to the 5.5 family (see [D6])
- **[N55]** The lookback window is 20 blocks.
  - Quote: "The lookback window is 20 blocks."
  - Source: same page
  - Status: Verified
- **[N56]** At most 4 breakpoints.
  - Quote: "You can define up to 4 cache breakpoints if you want to:"
  - Source: same page
  - Status: Verified
- **[N57]** Setting `max_tokens: 0` pre-warms the cache.
  - Quote: "Set `max_tokens: 0` in your request."
  - Source: same page
  - Status: Contested

### Anthropic: agent skills best practices

- **[N58]** Test skills on every model; Haiku may need more detail.
  - Quote: "What works perfectly for Opus might need more detail for Haiku."
  - Source: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
  - Status: Verified
- **[N59]** Keep SKILL.md under 500 lines.
  - Quote: "Keep SKILL.md body under 500 lines for optimal performance"
  - Source: same page
  - Status: Verified
- **[N60]** Write evaluations before extensive documentation.
  - Quote: "Create evaluations BEFORE writing extensive documentation."
  - Source: same page
  - Status: Verified
- **[N61]** Match the degree of freedom to how fragile the operation is.
  - Quote: "Operations are fragile and error-prone"
  - Source: same page
  - Status: Verified
- **[N62]** Validator feedback loops.
  - Quote: "This pattern greatly improves output quality."
  - Source: same page
  - Status: Verified
- **[N63]** Plan-validate-execute.
  - Quote: "Catches errors early: Validation finds problems before changes are applied"
  - Source: same page
  - Status: Verified
- **[N64]** Prefer pre-made scripts.
  - Quote: "More reliable than generated code"
  - Source: same page
  - Status: Verified
- **[N65]** References one level deep.
  - Quote: "Keep references one level deep from SKILL.md"
  - Source: same page
  - Status: Verified
- **[N66]** One default approach.
  - Quote: "Don't present multiple approaches unless necessary"
  - Source: same page
  - Status: Verified

### ManimBench: LLM-based Manim animation generation

- **[N67]** 17 open sub-30B models evaluated across 9 strategy combinations.
  - Quote: "It evaluates 17 open-source sub-30B LLMs across nine combinations of training and inference strategies using ManimBench."
  - Source: https://deeplearn.org/arxiv/815516/training-and-agentic-inference-strategies-for-llm-based-manim-animation-generation
  - Status: Verified
- **[N68]** 94% render success and 85.7% visual similarity.
  - Quote: "achieved the highest overall performance, with a 94% Render Success Rate (RSR) and 85.7% Visual Similarity (VS)."
  - Source: same page
  - Status: Verified
- **[N69]** +3 points over GPT-4.1 on visual similarity.
  - Quote: "surpassing the baseline GPT-4.1 model by +3 percentage points in VS."
  - Source: same page
  - Status: Verified
- **[N70]** SFT improves code; GRPO improves visuals.
  - Quote: "SFT generally improves code quality, while GRPO enhances visual outputs."
  - Source: same page
  - Status: Verified
- **[N71]** Unified reward.
  - Quote: "using a unified reward signal that fuses code and visual assessment signals."
  - Source: same page
  - Status: Verified
- **[N72]** More responsive to renderer feedback during self-correction.
  - Quote: "increases the models' responsiveness to extrinsic signals during self-correction at inference time."
  - Source: same page
  - Status: Verified

### TensorZero: distillation and programmatic data curation

- **[N73]** Up to 30x cost reduction and 4x latency reduction.
  - Quote: "reducing inference costs by up to 30x and inference time by up to 4x."
  - Source: https://www.tensorzero.com/blog/distillation-programmatic-data-curation-smarter-llms-5-30x-cheaper-inference/
  - Status: Verified
- **[N74]** 24.1x lower cost per success.
  - Quote: "Gemini 2.0 Flash Lite (fine-tuned) achieves the highest cost efficiency with 24.1x lower cost per success than GPT-4o."
  - Source: same page
  - Status: Verified. The page's text and table name different baselines.
- **[N75]** About 90% of teacher accuracy at 5x lower cost.
  - Quote: "they can recover 90% accuracy at 5x lower cost and significantly faster response times."
  - Source: same page
  - Status: Verified
- **[N76]** Pass^1 rose from 35.7% to 43.3%.
  - Quote: "Gemini 2.0 Flash from 35.7% to 43.3% pass^1."
  - Source: same page
  - Status: Verified
- **[N77]** Out-of-distribution regression.
  - Quote: "others (GPT-4.1 mini, GPT-4o mini, and Gemini 2.0 Flash-Lite) experience performance regression."
  - Source: same page
  - Status: Verified
- **[N78]** 446 demonstrations.
  - Quote: "446 successful GPT-4.1 conversations as demonstrations (356 training, 90 validation)."
  - Source: same page
  - Status: Verified
- **[N79]** Fine-tuning cost $2.30–$32.
  - Quote: "fine-tuning costs ranged from $2.30 (BabyAI) to $32 (τ-bench)."
  - Source: same page
  - Status: Verified

### Haiku 5.5 release news (letsdatascience)

- **[N80]** Haiku 5.5 price.
  - Quote: "Anthropic lists Haiku 5.5 at $0.10 per million input tokens and $0.50 per million output tokens"
  - Source: https://letsdatascience.com/news/anthropic-releases-claude-haiku-55-with-lower-prices-and-eff-f698c663
  - Status: Verified
- **[N81]** Haiku 4.5 was $1 / $5.
  - Quote: "The comparable Haiku 4.5 rates are $1 and $5."
  - Source: same page
  - Status: Verified
- **[N82]** Prices above 100K tokens.
  - Quote: "Haiku 5.5's listed input and output prices rise to $0.50 and $2.50 per million tokens."
  - Source: same page
  - Status: Verified
- **[N83]** About 90% of previous Haiku requests fall in the short tier.
  - Quote: "covers about 90% of requests to the previous Haiku model"
  - Source: same page
  - Status: Verified
- **[N84]** Sonnet 5.5 cache-read price cut.
  - Quote: "cut the listed cache-read price for Claude Sonnet 5.5 from $0.20 to $0.10 per million tokens"
  - Source: same page
  - Status: Verified. This conflicts with the supplied price block; see [N19] and [D11].
- **[N85]** OSWorld 2.1: 72.4% versus 15.7%.
  - Quote: "it reports 72.4% for Haiku 5.5 versus 15.7% for Haiku 4.5"
  - Source: same page
  - Status: Verified (vendor-reported)
- **[N86]** Configurable effort levels.
  - Quote: "The release adds configurable effort levels, allowing developers to trade token use against capability"
  - Source: same page
  - Status: Verified
- **[N87]** Beta computer-use and browser-use support in the SDKs.
  - Quote: "Anthropic also announced beta computer-use and browser-use support in its Python and TypeScript SDKs"
  - Source: same page
  - Status: Verified

### Large Language Monkeys: repeated sampling (arXiv 2407.21787)

- **[N88]** SWE-bench Lite rose from 15.9% to 56% with 250 samples.
  - Quote: "increases from 15.9% with one sample to 56% with 250 samples"
  - Source: https://arxiv.org/abs/2407.21787
  - Status: Verified
- **[N89]** Beats the single-sample state of the art.
  - Quote: "outperforming the single-sample state-of-the-art of 43%"
  - Source: same page
  - Status: Verified
- **[N90]** Coverage scales over four orders of magnitude.
  - Quote: "scales with the number of samples over four orders of magnitude"
  - Source: same page
  - Status: Verified
- **[N91]** The relationship is log-linear.
  - Quote: "the relationship between coverage and the number of samples is often log-linear"
  - Source: same page
  - Status: Verified
- **[N92]** Without verifiers, selection plateaus.
  - Quote: "majority voting and reward models) plateau beyond several hundred samples"
  - Source: same page
  - Status: Verified

### Anthropic: effort

- **[N93]** Opus 5.5 and Haiku 5.5 default to medium effort.
  - Quote: "Claude Opus 5.5 and Claude Haiku 5.5 default to medium."
  - Source: https://platform.claude.com/docs/en/build-with-claude/effort
  - Status: Verified
- **[N94]** Five effort levels; low suits subagents.
  - Quote: "Simpler tasks that need the best speed and lowest costs, such as subagents"
  - Source: same page
  - Status: Contested
- **[N95]** Low effort makes Haiku more likely to skip a search, stop early or skip a check.
  - Quote: "the model is more likely to skip a search, stop early, or skip a check at `low`"
  - Source: same page
  - Status: Verified
- **[N96]** Effort affects all output tokens.
  - Quote: "The effort parameter affects **all tokens** in the response, including:"
  - Source: same page
  - Status: Verified

## Supplementary API reference notes [D#]

Source: bundled Claude API skill, cached 2026-10-06. Each item mirrors Anthropic's model-migration, prompt-caching and effort documentation. Re-check against live documentation before shipping.

- **[D1]** Forced `tool_choice` (`any` or `tool`) returns HTTP 400 on Fable 5.1, Opus 5.5 and Sonnet 5.5. Use `auto` with `strict: true` and a prompt instruction, or use structured outputs instead.
- **[D2]** Haiku 5.5 accepts forced `tool_choice`, but the response then starts with the tool call and carries no thinking block.
- **[D3]** Effort goes in `output_config.effort`, not as a top-level field. Opus 5.5 and Haiku 5.5 default to medium; Sonnet 5.5 defaults to high, with recalibrated levels.
- **[D4]** Per-message effort is a beta (`mid-conversation-output-config-2026-07-01`). It is supported on Fable 5.1, Opus 5.5, Sonnet 5.5 and Haiku 5.5 when thinking is on, and changes effort without a cache reset. Available on the Claude API and Google Cloud.
- **[D5]** Preserved thinking: sending a thinking block back after editing `system`, `tools` or earlier messages returns 400. This is enforced by default for accounts created on or after 2026-08-31. Keep histories append-only.
- **[D6]** The minimum cacheable prefix is 512 tokens for Opus 5.5, Sonnet 5.5, Haiku 5.5 and Fable 5.1. The reference itself advises checking the caching documentation.
- **[D7]** Opus 5.5 thinking cannot be disabled. On Sonnet 5.5, thinking can be turned off only with `{type: "between_tools"}`, at effort high or below.
- **[D8]** Opus 5.5 uses the tokenizer family introduced with Opus 4.7. Haiku 5.5 produces about 30% more tokens than Haiku 4.5. Re-baseline with `messages.count_tokens`.
- **[D9]** Server-side refusal `fallbacks` (beta) are available on Fable 5.1, Opus 5.5 and Sonnet 5.5. They are rejected on the Batches API. Haiku 5.5 has no server-side fallback.
- **[D10]** Fable 5.1 requires 30-day data retention, so it is not available under zero data retention unless Anthropic expressly authorises it.
- **[D11]** The model table lists the Sonnet 5.5 cache-read price as $0.20. This conflicts with [N19] and [N84].
- **[D12]** Task budgets (beta `task-budgets-2026-03-13`) are an advisory token ceiling for agentic loops on Opus 5.5, Haiku 5.5, Sonnet 5.5 and others. The minimum total is 20,000.

## Project files [P#]

All paths are relative to `~/Desktop/Personal/Book/Videos/ExamLeaf_Video_EdTech_Pipeline/`.

- **[P1]** `08_cost_models/CONSOLIDATED_COST_SCENARIOS.md` §B.2. The hybrid per-video line items:
  - LLM 1.716, narration 0.96, generated clips 4, stills 0.2, encoding/render 0.5, alignment 0.1, storage 0.2
  - human: academic 15, QA 5, repairs 6.6667, making 26.6667 in total
  - **total 34.3427**; 85 human minutes; hybrid FTE 8.85 FTE-months at 1,000 videos
  - the narration inputs list GPU at $0.80 per hour (an assumption)
  - Status: project workbook
- **[P2]** Same file. Rendering example: 8 vCPU / 16 GB, 45 worker-minutes, 20% retry, **$0.3555**, described as "not a measured benchmark".
- **[P3]** Same file, "Measured Proof". Eight silent 30-second fixture renders at 1280×720 and 720×1280 took 27.3–29.4 s wall each on two local CPU workers. Explicitly not a cloud price.
- **[P4]** Same file. The three-Short package costs **$4.316 per lesson**. The default generated-video allowance should be zero seconds. Hybrid with zero generated clips is $30.34 per video.
- **[P5]** `12_advanced_animations_with_claude/04_harness_contract/`: `contract.md`, `lint_seek_contract.js`, `determinism_hash_check.py`, `validate_cue_sheet.py`, `cue_sheet.schema.json`, `vertical_safe_zones.tokens.json`, `preflight.sh`, `scene_template.html`. These are existing harness files; none has been run on a real render yet.
- **[P6]** `12_advanced_animations_with_claude/02_documentation/12_EDGE_CASES_master_table.md` (65 edge cases) and `06_prompts_and_templates/negative_tests.md` (31 negative tests).

## Internal experiment

- **[V1]** Devarf reference run: Claude Code, Opus 5.5, one 79-second motion-graphics music video from a bare prompt.
  - Low effort: about 78K tokens, about $3.
  - Max effort: about 625K tokens, about $49.
  - Max + ultracode: at least 2.5M tokens, at least $348, never finished.
  - Status: **unreconciled**. Both dollar figures imply more than $20 per MTok, which exceeds Opus 5.5's output price, so the token counts must be incomplete. Use these figures only as bounds until the week-1 metering exists.
