# Target production architecture
## Decision
Use HyperFrames as the primary compositor candidate, with SVG/KaTeX components driven by verified Python data. Add Manim Community for specialist mathematical inserts and Blender/Three.js only when spatial reasoning benefits. FFmpeg performs final assembly, audio processing and encoding. Remotion is the alternative when the same golden-scene benchmark shows React workflow/maturity saves more engineering cost than its licence. Do not maintain both by default.

This is a recommendation based on documentation and use-case fit. The local proof tested native SVG/CairoSVG/FFmpeg, not HyperFrames or Remotion. Promotion of the selected browser engine requires the pilot comparison below.

## Do not confuse layers
Skill = instructions/resources an agent loads. MCP = protocol exposing tools/resources to an agent. API = callable service contract. SDK = client library. CLI = executable interface. Platform = hosted workflow/UI/billing. None supplies scientific verification merely by existing. A plugin can bundle multiple layers and installation hooks.

## Data flow
Permitted source PDF + current official syllabus → native extraction and visual flags → SourceRef/claim ledger → curriculum/prerequisite map → LessonPlan → original Super Teacher script → independent science review → storyboard and routing → validated state data + approved components → narration → actual-audio alignment → 16:9 lesson → automated QA → academic + full-video approval → release. ShortSpec selects complete teaching units and reflows them into 9:16, followed by a separate release review.

## Stage ownership
| Stage | AI work | Deterministic work | Required human action |
|---|---|---|---|
| Source/curriculum | Propose mapping, identify gaps | Hash, page extract, schema validation | Approve rights, edition and syllabus fit |
| Lesson/script | Scope, explain, analogy, interaction drafts | Coverage checks and referenced claim IDs | Approve scientific explanations and answer keys |
| Model/data | Suggest appropriate model | Symbolic/numerical/count/units tests | Approve assumptions and limits |
| Visuals | Select component and propose layout | Render verified state at explicit time | Inspect scientific implications and readability |
| Audio | Normalize pronunciation/delivery | Synthesis request cache and waveform alignment | Listen for terminology and natural delivery |
| QA | Summarize defects, suggest bounded fixes | Media/schema/hash/bounds/caption tests | Final complete-video review |
| Publishing | Draft titles/CTAs | Verify approved hashes/access metadata | Authorize release and disclosures |

## Core records
SourceRef retains URI, locator, rights status, date and claim scope. Production extends it with stored source hash, academic-year version and exact extracted coordinates.
Claim includes source IDs, assumptions and review state. A statement is not approved because an LLM marked it approved.
LessonPlan includes board, division, class, language, objectives, prerequisites and review gates.
SceneSpec separates scientific parameters, explanatory cues, visible state, voice direction and duration. Content never contains executable Python/JS.
AssetManifest records SHA-256, origin, licence, attribution and provider/model/job when generated.
ProviderJob retains input hash, idempotency key, provider job ID, state and estimated/actual cost. Unknown status triggers rejoin, not a duplicate submission.
ShortSpec keeps source claim IDs, assumptions, complete payoff, access destination and reflow strategy.
Approval binds an authenticated reviewer role to an exact artifact hash and full-watch evidence. Local JSON is only a policy prototype.

## Scene router
1. Equation, calculation, graph or model state: deterministic only.
2. Molecular identity, reaction state, chromosome/process count: approved domain representation only.
3. Anatomy/spatial structure: licensed or reviewed model/SVG; 3D only if needed.
4. Real-world explanatory context: owned/licensed media or a clearly non-authoritative generated illustration, when it adds value.
5. Branding, thumbnail background or metaphor: optional generation with deterministic text/labels placed afterward.
6. Any failed scientific generative asset: replace with the correct deterministic/static representation; never regenerate until it merely looks plausible.

Default generated-video seconds are ZERO. The cost model's twenty seconds are an optional allowance, not a quota. Numerical/diagram assertions may not be delegated to a diffusion/video model.

## Agents and orchestration
During development, Claude Code/Codex use isolated worktrees: architecture/component author, independent science reviewer, test/QA engineer. Do not let multiple agents concurrently modify the same renderer contract.
During production, a durable workflow engine owns state; the chat does not. Start with local job execution and SQLite. Promote to Prefect + PostgreSQL + object storage + isolated Docker workers once the four narrated pilots pass. Keep CPU rendering and paid provider jobs in separate queues. No Kubernetes requirement at launch.

MCP is useful for repository issues, approved source retrieval, constrained provider tools and local preview inspection. It is not required to import SymPy or run internal FFmpeg. Do not route every function call through an LLM.

## Branding and readability
Central tokens: background #F7F9FC; text #14213D; blue #185ABD; teal #087986; amber #9A5B00; purple #6E44AA; error #B42318. These are design choices, not neuroscience-based memory colours. Use labels/shapes in addition to colour. Target 4.5:1 normal text contrast, check adjacent graph colours and actual phone rendering.

A 1920px master scaled to 360px reduces an 88px label to 16.5px. Essential text must survive that display or be split/enlarged. The technical preview's finer labels are not claimed to pass the eventual phone-readability acceptance gate.

Final production target: 1920×1080 and 1080×1920, 24 or 30fps chosen consistently, H.264/yuv420p delivery, high-quality audio master, accurate VTT/SRT. The local benchmark is only 1280×720/720×1280 at 24fps. Vertical content is re-authored/reflowed, never blindly cropped or generatively outpainted to invent scientific details.

## Multilingual design
Keep display notation, spoken text, translations and phoneme/pronunciation guidance separate. Original English and native-reviewed Assamese-supported variants may have different durations and line breaks. Translate meaning and exam terminology; do not merely dub the English timeline. Model language support is a hard gate verified through a real request and native review, not a generic marketing language count.
