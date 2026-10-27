# Public Skills and Integrations — checked 13 October 2026

This is an audited shortlist and discovery ledger, not a claim to enumerate every changing public repository. Documentation inspection is not full code/security audit or execution. Blob SHAs identify inspected files; they are **not commit SHAs for checkout**. No third-party Skill code is redistributed here.

## higgsfield-skills
- Type/origin: Agent Skills — Official Higgsfield
- Source: https://github.com/higgsfield-ai/skills
- Select: higgsfield-video-explainer; higgsfield-generate; higgsfield-brandkit; higgsfield-youtube-thumbnail
- Decision: Reference/adapt for optional non-scientific illustration and packaging; replace fixed ten-second lesson assembly
- Licence: Repository MIT; service and model terms separate
- Authentication: CLI/MCP account OAuth; API credentials are a separate surface
- Installation after audit: Read selected folders from a pinned reviewed commit; do not run installer scripts
- Risk: Bash execution; generative spend; external asset upload; unvalidated virality scoring
- Verification: Documentation inspected; not installed or executed
- Snapshot: Explainer v0.13.0; SKILL.md blob 8f50a15dda4a9c8a448d4ccbd1cdc1267ed65b2b (blob is NOT a commit pin)

## higgsfield-cli
- Type/origin: CLI — Official Higgsfield
- Source: https://github.com/higgsfield-ai/cli
- Select: account/workspace; model list/get; generation estimate/submit/get/wait
- Decision: Implement optional provider adapter after authenticated cost probe
- Licence: CLI MIT; SaaS billing/rights separate
- Authentication: higgsfield auth login
- Installation after audit: Inspect approved release and digest, then install @higgsfield/cli at reviewed exact version
- Risk: Do not pipe downloaded scripts to a shell; persist job IDs; account cost estimates required
- Verification: Documentation inspected; not installed or executed
- Snapshot: Public documentation inspected; no immutable package pin established.

## higgsfield-mcp
- Type/origin: MCP server — Official Higgsfield
- Source: https://higgsfield.ai/creator-hub/help-center/integrations/what-is-higgsfield-mcp
- Select: OAuth tools for asset/audio/video generation and workflows
- Decision: Optional supervised authoring; not queue owner
- Licence: Hosted service terms; subscription credits; Unlimited web mode not presumed to apply
- Authentication: OAuth per workspace
- Installation after audit: Add official MCP endpoint after account and permissions review
- Risk: Model/provider costs, file uploads, creative workflow may bypass local quality gates
- Verification: Documentation inspected; not installed or executed
- Snapshot: Public documentation inspected; no immutable package pin established.

## higgsfield-api
- Type/origin: HTTP API — Official Higgsfield
- Source: https://higgsfield.ai/higgsfield-api
- Select: Generation submission/status APIs
- Decision: Investigate endpoint parity before implementing; not interchangeable with MCP
- Licence: Separate pay-per-generation API economics; no verified whole-lesson quote
- Authentication: Developer API credential
- Installation after audit: Use documented SDK/HTTP only after access and endpoint schema probe
- Risk: Subscription credits do not establish API budget or endpoint access
- Verification: Documentation inspected; not installed or executed
- Snapshot: Public documentation inspected; no immutable package pin established.

## remotion-skills
- Type/origin: Agent Skills — Official Remotion
- Source: https://github.com/remotion-dev/skills
- Select: remotion-best-practices; remotion-render; remotion-captions; remotion-multimedia; remotion-docs
- Decision: Reuse only if Remotion is selected; avoid overlapping engine Skill suites
- Licence: Review Skill licence separately; Remotion engine has conditional commercial licence
- Authentication: None for local instruction files; cloud auth separate
- Installation after audit: Documented npx skills add remotion-dev/skills; production uses reviewed local copies
- Risk: Installation is not a scientific validator; avoid agents automatically upgrading dependencies
- Verification: Documentation inspected; not installed or executed
- Snapshot: README blob 7718807e9e289dc95e66347fb96f11f20128508e; 12 listed Skills

## hyperframes
- Type/origin: Engine + Agent Skills — Official HeyGen
- Source: https://github.com/heygen-com/hyperframes
- Select: hyperframes; hyperframes-core; hyperframes-animation; hyperframes-keyframes; hyperframes-audio; hyperframes-cli
- Decision: Primary production compositor candidate; compare same fixtures with Remotion before adoption
- Licence: Apache-2.0 engine; inspect optional runtime/assets separately
- Authentication: Local engine none; optional hosted generation/rendering separately authenticated
- Installation after audit: Node 22+ and FFmpeg; pinned hyperframes package; reviewed selected Skill copies
- Risk: Current router can install on-demand workflows: disable unaudited auto-expansion; no network assets in final render
- Verification: Documentation inspected; not installed or executed
- Snapshot: skills-manifest.json blob 960e5a88ac87ff5aee65660b8085fb1a943e95d8; 21 manifest entries, cached README count differs

## elevenlabs-skills
- Type/origin: Agent Skills — Official ElevenLabs
- Source: https://github.com/elevenlabs/skills
- Select: text-to-speech; speech-to-text; optional voice-isolator; dubbing after language review
- Decision: Reuse selected instructions; custom audio timing, terminology, budget and release wrappers
- Licence: MIT Skills; commercial voice rights and API terms separate
- Authentication: ELEVENLABS_API_KEY in secret store, not scripts
- Installation after audit: Python elevenlabs; JavaScript @elevenlabs/elevenlabs-js; documented npx skills add elevenlabs/skills
- Risk: Do not use deprecated JS package named elevenlabs; no secrets in prompts/eval logs
- Verification: Documentation inspected; not installed or executed
- Snapshot: README blob 1df95fc2fb6a7a4803381e6138ddc91942a239cf; 10 listed Skills

## anthropic-skills
- Type/origin: Agent Skills + marketplace — Official Anthropic
- Source: https://github.com/anthropics/skills
- Select: skill-creator; webapp-testing; mcp-builder patterns
- Decision: Reuse evaluation and testing patterns; do not wholesale install document bundle
- Licence: Many Apache-2.0; docx/pdf/pptx/xlsx source-available under distinct terms
- Authentication: Claude account/API for model execution
- Installation after audit: Reviewed local copies or documented /plugin marketplace add anthropics/skills
- Risk: Example Skills are not production warranties; evaluate negative cases
- Verification: Documentation inspected; not installed or executed
- Snapshot: README blob eb54ee8b92f2d40b4b26569be0772be3c1e23156

## blender-mcp
- Type/origin: MCP server + Blender add-on — Community; NOT Blender Foundation
- Source: https://github.com/ahujasid/mcp-for-blender
- Select: execute_blender_code; look; scene inspection
- Decision: Isolated asset-authoring workstation only; production uses approved headless Blender Python
- Licence: MIT bridge; Blender GPL; imported asset licences separate
- Authentication: Local bridge; optional generator/asset keys separate
- Installation after audit: Old ahujasid/blender-mcp redirects; new package mcp-for-blender. Manually audit/pin server + add-on; no curl|sh
- Risk: Arbitrary Python; TCP bridge exposure; DISABLE_TELEMETRY=true. Current content telemetry opt-in; minimal anonymous usage default on
- Verification: Documentation inspected; not installed or executed
- Snapshot: README blob 09f5b9fa318dc33a2a2654bf2224a19229ba5188; old path failed then renamed repository inspected

## manim-community-skills
- Type/origin: Agent Skills — Community
- Source: https://github.com/adithya-s-k/manim_skill
- Select: manimce-best-practices; manim-composer
- Decision: Audit selected CE guidance; do not mix ManimGL and Manim Community APIs
- Licence: MIT Skill repository; Manim Community MIT
- Authentication: None locally
- Installation after audit: Read pinned files; install Manim Community from its current official requirements
- Risk: Community README runtime guidance may lag; claimed tests were not run here
- Verification: Documentation inspected; not installed or executed
- Snapshot: Public documentation inspected; no immutable package pin established.

## scientific-agent-skills
- Type/origin: Agent Skills — Community K-Dense
- Source: https://github.com/K-Dense-AI/scientific-agent-skills
- Select: Selective sympy, rdkit, biopython and scientific visualization guidance
- Decision: Consult package guidance; use ExamLeaf-specific verification contracts
- Licence: Check individual Skill licence/dependencies; no blanket asset clearance
- Authentication: Depends on selected task; local libraries need none
- Installation after audit: Vendor only reviewed needed instructions; do not auto-install full scientific stack
- Risk: Instructions and executable helpers are separate audit surfaces
- Verification: Documentation inspected; not installed or executed
- Snapshot: Public documentation inspected; no immutable package pin established.

## playwright-mcp
- Type/origin: MCP server — Official Microsoft
- Source: https://github.com/microsoft/playwright-mcp
- Select: Browser inspection and local preview tests
- Decision: Optional authoring inspection; CI uses direct Playwright tests
- Licence: Apache-2.0 repository; browser separately distributed
- Authentication: None for local preview
- Installation after audit: Pin reviewed server/client; use local-only preview browser profile
- Risk: Browsing untrusted content can prompt-inject; do not share authenticated general-purpose profile
- Verification: Discovery/documentation reference; not executed as MCP
- Snapshot: Public documentation inspected; no immutable package pin established.

## skills-sh
- Type/origin: Skill directory — Vercel ecosystem
- Source: https://skills.sh/
- Select: Discover relevant packages then follow original repository
- Decision: Discovery only
- Licence: Per referenced repository
- Authentication: Not required to read directory
- Installation after audit: No directory-wide installation
- Risk: Install counts and security badges are not full audits
- Verification: Documentation inspected; not installed or executed
- Snapshot: Public documentation inspected; no immutable package pin established.

## mcp-registry
- Type/origin: MCP directory — MCP ecosystem
- Source: https://registry.modelcontextprotocol.io/
- Select: Discover and identify original publishers
- Decision: Discovery only
- Licence: Per service/server
- Authentication: Depends on selected server
- Installation after audit: Confirm publisher, package digest, OAuth audience and requested scopes
- Risk: Registry presence does not prove safety, uptime or scientific suitability
- Verification: Documentation inspected; not installed or executed
- Snapshot: Public documentation inspected; no immutable package pin established.

## claude-plugin-marketplace
- Type/origin: Plugin marketplace — Official Anthropic
- Source: https://github.com/anthropics/claude-plugins-official
- Select: Selected developer/testing integrations
- Decision: Use only when it fills a measured capability gap
- Licence: Per plugin
- Authentication: Per service
- Installation after audit: Inspect manifest, hooks, scripts and requested tools at pinned revision
- Risk: A plugin can bundle Skills, MCP and hooks; not equivalent to plain instructions
- Verification: Documentation inspected; not installed or executed
- Snapshot: Public documentation inspected; no immutable package pin established.

## runway
- Type/origin: Hosted APIs + connected MCP — Official Runway
- Source: https://docs.dev.runwayml.com/
- Select: Optional concept-neutral visuals; one speech audition tested separately
- Decision: Selective media only; never solver/diagram authority
- Licence: Hosted API/voice/model terms separate; account capability gating
- Authentication: Connected workspace or separate API key
- Installation after audit: Provider adapter against documented API; current local connector is not in packaged runtime
- Risk: Current workspace has no available video models; one nine-credit speech job submitted
- Verification: Read-only authentication tested; speech job separately recorded; generative video not tested
- Snapshot: Public documentation inspected; no immutable package pin established.

## pika
- Type/origin: Hosted generation API — Official Pika
- Source: https://dev.pika.art/pricing
- Select: Optional creative clips
- Decision: Secondary candidate; not core STEM renderer
- Licence: API Club membership plus usage; review model/output terms
- Authentication: Pika developer account
- Installation after audit: Documented API after account/price check
- Risk: Do not assume web credits equal API balance or correctness
- Verification: Documentation inspected; not installed or executed
- Snapshot: Public documentation inspected; no immutable package pin established.

## luma
- Type/origin: Hosted generation API — Official Luma
- Source: https://lumalabs.ai/api
- Select: Optional image-to-video/context clips
- Decision: Deferred; current final rate not resolved
- Licence: Service terms; all-in current quote unresolved
- Authentication: Developer API key
- Installation after audit: Use official SDK/docs after current account probe
- Risk: Landing page could not be fully retrieved; no live generation tested
- Verification: Official API existence/docs checked; pricing unresolved
- Snapshot: Public documentation inspected; no immutable package pin established.

## kling-seedance-veo
- Type/origin: Models behind provider APIs — Multiple model owners/providers
- Source: https://docs.dev.runwayml.com/guides/pricing/
- Select: Kling, Seedance, Veo provider catalogue comparisons
- Decision: Optional illustration; choose exact model/resolution/audio route per request
- Licence: Provider-specific prices/access/terms; aggregator access is not direct-owner API access
- Authentication: Provider account/API key
- Installation after audit: Probe model catalogue and capability schema before submit
- Risk: No model advertised as physics-realistic is a substitute for an equation solver
- Verification: Documentation inspected; not installed or executed
- Snapshot: Public documentation inspected; no immutable package pin established.

## motion-canvas
- Type/origin: Animation engine — Official project
- Source: https://github.com/motion-canvas/motion-canvas
- Select: TypeScript generators and editor for vector explanations
- Decision: Alternative, not an additional default runtime
- Licence: MIT
- Authentication: None locally
- Installation after audit: Pin official packages and renderer plugins
- Risk: No local execution/benchmark performed
- Verification: Documentation inspected; not installed or executed
- Snapshot: Public documentation inspected; no immutable package pin established.

## blender
- Type/origin: 3D application + Python API — Blender Foundation
- Source: https://www.blender.org/about/license/
- Select: Headless rendering of approved .blend/Python scenes
- Decision: Selective 3D inserts
- Licence: GPL software; output artwork not automatically GPL; third-party models separate
- Authentication: None locally
- Installation after audit: Pinned Blender build and approved script; disable automatic .blend execution
- Risk: Do not render untrusted .blend/scripts with production credentials
- Verification: Documentation inspected; not installed or executed
- Snapshot: Public documentation inspected; no immutable package pin established.
