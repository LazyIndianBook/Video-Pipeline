# Higgsfield workflow: what to reuse and what to replace
## Evidence checked
- Official blog: https://higgsfield.ai/blog/faceless-channel-one-prompt
- Official Skills: https://github.com/higgsfield-ai/skills
- CLI: https://github.com/higgsfield-ai/cli
- MCP explanation: https://higgsfield.ai/creator-hub/help-center/integrations/what-is-higgsfield-mcp
- Separate API offering: https://higgsfield.ai/higgsfield-api

The blog packages topic research, a long explainer, dubbing, thumbnails, Shorts and a calendar into a chat workflow. Its income/reach/retention claims are marketing, not controlled evidence of ExamLeaf learning or revenue. Embedded completed videos were not independently auditioned here.

The live inspected explainer Skill v0.13.0 describes a more specific pipeline: research/style planning; one shared style image; roughly 20–24-word narration blocks; generate Seed audio; generate Gemini Omni Flash ten-second 720p clips; assemble through explainer_video. A ten-minute run uses sixty ten-second blocks by its minutes×6 convention. It uses provider-side assembly, not local FFmpeg, within that Skill. Read the original at a reviewed commit before implementation, because this changes rapidly.

The fixed-slot design helps automate general faceless content but conflicts with variable STEM inspection time, learner practice pauses and stable scientific diagrams. It is not enough to ask a video model to make sixty individually plausible scientific shots. We do not inherit automatic narration speed fitting or novelty-first scene selection.

Reuse the brandkit/style-key idea, model discovery/cost estimation, persistent asynchronous job state, optional thumbnail exploration and concept-neutral illustrations. Replace the science generator, curriculum writer, strict ten-second pacing and automatic virality objective with ExamLeaf's typed state/teaching/QA system.

The generate Skill exposes a brain_activity/Virality Predictor scoring capability. No calibration against ExamLeaf sales, subject learning or genuine neurological attention was verified. Treat it, at most, as optional creative feedback; never as a learning score or objective truth.

MCP/CLI account credit use, web Unlimited use and separate developer API pricing are not the same billing product. No exact authenticated ten-minute Higgsfield quote was obtained. Require: model discovery → complete request estimate → attempt reserve → explicit budget → request/job persistence → actual invoice reconciliation. Some operations do not support cost estimation; those need a separate approved bound rather than an invented price.

No Higgsfield integration was executed. No public installer or downloaded Skill script ran. The linked blog is a useful example of workflow packaging, not the core ExamLeaf scientific architecture.
