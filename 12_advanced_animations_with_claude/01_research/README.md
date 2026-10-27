# 01_research — how the research was produced (14 October 2026)

| File | What it is |
|---|---|
| `RESEARCH_REPORT_advanced_animations_with_claude.md` | The cited report (≈10,500 words): what the five reference videos show, rendering harnesses (HyperFrames, Remotion, raw Canvas/SVG/three.js, Manim CE, Blender) with a decision table, Claude Code effort/ultracode/cost facts, drawing styles in code, Python audio composition and librosa analysis, MCP orchestration (Higgsfield, Blender, ElevenLabs), motion-design craft rules, **65 edge cases**, integration with the ExamLeaf pipeline, the **15 proposed skills**, open questions |
| `SOURCES_and_claims.md` | Every [N#] claim behind the report with its verbatim quote, URL, source kind, verification status and any stated edge case |

## Inputs

- The five YouTube videos supplied by the user (transcripts, descriptions and chapters in `../00_reference_videos/`, pulled with yt-dlp auto-captions, so wording is approximate), cited as [V1]–[V5].
- The verbatim "Paper-Cutout Storybook Collage" master prompt linked from video 4 (`../00_reference_videos/master_prompt_paper_collage.md`), cited as [V4-MP].
- Web evidence gathered by the workflow below, cited as [N1]–[N81].

## Workflow (Fable 5.1 lead; Sonnet 5.5 search/fetch/verify; Opus 5.5 synthesis)

| Phase | Agents | Result |
|---|---|---|
| Search, 10 angles (Remotion with Claude; HyperFrames; JS/Canvas/SVG/three.js frame pipelines; "Claude Motion", effort levels, ultracode, cost; MCP media orchestration; Python audio synthesis and analysis; Manim/Motion Canvas; motion-design craft and prompting; edge cases and failure modes; educational explainer styles 2026) | 10 | 102 unique sources |
| Fetch and extract falsifiable, actionable claims with quotes and stated edge cases | 10 (3 URLs each) | 30 sources read in full, 215 claims, 110 unique after dedup/cap |
| Adversarial verification, two lenses per claim (source-support; currency-and-contradiction); killed only when both refute | 20 | 81 survived (unanimous or contested), 29 killed |
| Synthesis from surviving claims plus the five transcripts | 1 | The report |

## Caveats

- Single-day research pass; only 30 of 102 sources were read in full, and 12 carried all surviving claims.
- "(contested)" claims had one of two verifiers refuse to confirm; re-check before relying on them.
- "Claude Motion" was not found as an official product or feature name; the report treats it as a community term.
- Fable 5.5 material ([V5]) is a leak-based, unverified capability signal.
- No tool was installed or executed during the research; the build phase that follows adds offline self-testing scripts only.
