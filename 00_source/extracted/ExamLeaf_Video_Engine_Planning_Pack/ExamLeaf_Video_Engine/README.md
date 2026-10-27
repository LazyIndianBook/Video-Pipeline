# ExamLeaf Video Engine — implementation planning pack

Research date: 13 October 2026.

## Contents
- ExamLeaf_Cost_and_Skills.xlsx: editable assumptions, formula-driven unit and volume costs, 40 proposed custom Skills, and verified existing Skill resources.
- ExamLeaf_Skills_Inventory.csv: importable custom-Skill backlog.
- design_tokens.json: proposed palette, typography, timing and audio standards.
- QA_and_Implementation_Contract.md: release gates, negative tests and artifact contracts.

## Recommendation
Use HyperFrames as the initial scene compositor, with approved SVG/KaTeX components,
seekable animation, Python scientific validation, selective Manim inserts and FFmpeg assembly.
Retain a renderer-independent LessonSpec/SceneSpec. Choose Remotion instead when its React
workflow or support reduces total engineering cost; do not maintain duplicate engines without need.

The LLM drafts and assembles. Verified data drives equations, geometry, molecular structures,
simulation trajectories and biological process states.

## Scope and limitations
This pack is a researched design and planning model. It does not contain a deployed engine,
validated Skill implementations, benchmarked render timings, or auditioned narration samples.
The $8,000 initial implementation budget and all staffing, token and workload volumes are
illustrative assumptions, not vendor quotes. Academic and final-video review remain mandatory.

## Price and capability sources
- HyperFrames: https://github.com/heygen-com/hyperframes
- HyperFrames Skills manifest: https://raw.githubusercontent.com/heygen-com/hyperframes/main/skills-manifest.json
- Remotion licensing: https://www.remotion.dev/docs/license/pricing
- Remotion Skills: https://github.com/remotion-dev/skills
- Anthropic pricing: https://platform.claude.com/docs/en/about-claude/pricing
- OpenAI pricing: https://developers.openai.com/api/docs/pricing
- ElevenLabs API pricing: https://elevenlabs.io/pricing/api
- Cartesia pricing: https://cartesia.ai/pricing
- AWS Fargate: https://aws.amazon.com/fargate/pricing/
- Cloudflare R2: https://developers.cloudflare.com/r2/pricing/
- Anthropic Skills: https://github.com/anthropics/skills
- OpenAI Skills: https://github.com/openai/skills
- K-Dense Skills: https://github.com/K-Dense-AI/scientific-agent-skills

Pin reviewed dependency commits and repeat availability, license and model-lifecycle checks before deployment.
Do not use a floating latest version in production.
