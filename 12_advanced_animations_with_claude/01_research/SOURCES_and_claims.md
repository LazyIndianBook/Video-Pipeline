| ID | Claim | Quote | URL | Kind | Status | Edge case |
|---|---|---|---|---|---|---|
| N1 | Remotion skills install with one npx command | "npx skills add remotion-dev/skills" | https://www.remotion.dev/docs/ai/skills | official-doc | unanimous | — |
| N2 | Skills can be added at project creation | "You are also offered the option to add skills when you create a new Remotion project" | https://www.remotion.dev/docs/ai/skills | official-doc | contested | — |
| N3 | Skills target Claude Code, Codex, Kimi Code, Cursor | "These skills are useful for AI agents like Claude Code, Codex, Kimi Code or Cursor." | https://www.remotion.dev/docs/ai/skills | official-doc | unanimous | — |
| N4 | /remotion-best-practices is the umbrella skill | "This skill encompasses all other skills." | https://www.remotion.dev/docs/ai/skills | official-doc | unanimous | — |
| N5 | /remotion-render renders a video or still | "Invoke a render into a video or a still." | https://www.remotion.dev/docs/ai/skills | official-doc | unanimous | — |
| N6 | /remotion-maps covers map libraries and CesiumJS | "Mapbox, MapLibre, MapTiler, GeoJSON, and 3D geographic flyovers with CesiumJS." | https://www.remotion.dev/docs/ai/skills | official-doc | unanimous | — |
| N7 | /remotion-upgrade updates packages and skills together | "Upgrade Remotion, related packages, compatible Mediabunny packages, and installed Remotion Agent Skills." | https://www.remotion.dev/docs/ai/skills | official-doc | unanimous | Version drift if not run |
| N8 | HyperFrames needs Node 22+ and FFmpeg | "Requirements: Node.js 22+, FFmpeg" | https://github.com/heygen-com/hyperframes | repo | unanimous | Fails on older Node or without FFmpeg |
| N9 | Scaffold via npx hyperframes init | "npx hyperframes init my-video" | https://github.com/heygen-com/hyperframes | repo | unanimous | — |
| N10 | Claude Code plugin install | "claude plugin install hyperframes@hyperframes" | https://github.com/heygen-com/hyperframes | repo | unanimous | Add the marketplace first |
| N11 | Repo ships 21 on-demand skills | "HyperFrames ships 21 skills agents load on demand." | https://github.com/heygen-com/hyperframes | repo | unanimous | — |
| N12 | Codex archive has a size cap | "fails if the archive exceeds Codex's 100 MB upload limit" | https://github.com/heygen-com/hyperframes | repo | unanimous | Archive over 100 MB fails |
| N13 | Skip LFS on clone | "GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/heygen-com/hyperframes.git" | https://github.com/heygen-com/hyperframes | repo | unanimous | — |
| N14 | Apache 2.0 licence, no per-render fees | "Apache 2.0 license, with no per-render fees or commercial-use thresholds." | https://github.com/heygen-com/hyperframes | repo | unanimous | — |
| N15 | opus-js-animations marketplace install | "/plugin marketplace add klsoen/opus-js-animations" | https://github.com/klsoen/opus-js-animations | repo | unanimous | — |
| N16 | Manual skill install by copy | "cp -r opus-js-animations/skills/opus-js-animations ~/.claude/skills/" | https://github.com/klsoen/opus-js-animations | repo | unanimous | — |
| N17 | CHROME env var overrides autodetect | "set `CHROME=/path` if it isn't found" | https://github.com/klsoen/opus-js-animations | repo | unanimous | Render fails if Chrome not found and CHROME unset |
| N18 | Deterministic seek-per-frame rendering | "headless Chrome renders frame i as seek(i / fps) across parallel workers" | https://github.com/klsoen/opus-js-animations | repo | unanimous | — |
| N19 | Voiceover keys stored outside the project | "read from the environment or ~/.config/opus-js-animations/keys.env, never written into your project" | https://github.com/klsoen/opus-js-animations | repo | unanimous | — |
| N20 | Audio not processed unless requested | "It is cut on zero crossings, with no normalising, EQ or fades unless you ask." | https://github.com/klsoen/opus-js-animations | repo | unanimous | Loudness not normalised |
| N21 | MIT licence | "MIT © klsoen." | https://github.com/klsoen/opus-js-animations | repo | unanimous | Other-model support untested |
| N22 | Opus/Sonnet/Haiku 5.5 default to medium effort | "`high` on every model that supports effort, except that Opus 5.5, Sonnet 5.5, and Haiku 5.5 default to `medium`" | https://code.claude.com/docs/en/model-config | official-doc | unanimous | — |
| N23 | Unsupported effort falls back silently | "Claude Code falls back to the highest supported level at or below the one you set." | https://code.claude.com/docs/en/model-config | official-doc | unanimous | xhigh may run as high on older models |
| N24 | Ultracode launch flag starts at xhigh | "launch with `claude --effort ultracode`, which starts the session at `xhigh` effort with ultracode on" | https://code.claude.com/docs/en/model-config | official-doc | unanimous | — |
| N25 | Ultracode not accepted by settings or env | "The persisted `effortLevel` setting and the `CLAUDE_CODE_EFFORT_LEVEL` environment variable don't accept `ultracode`." | https://code.claude.com/docs/en/model-config | official-doc | unanimous | Cannot be a persistent default |
| N26 | Thinking cannot be disabled on 5.5 and Fable | "You can't turn thinking off on Opus 5.5, Sonnet 5.5, Haiku 5.5, or the Fable models." | https://code.claude.com/docs/en/model-config | official-doc | unanimous | Thinking cost cannot be eliminated |
| N27 | Disable adaptive thinking on 4.6 models | "set `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1` to revert to the previous fixed thinking budget controlled by `MAX_THINKING_TOKENS`" | https://code.claude.com/docs/en/model-config | official-doc | contested | — |
| N28 | Aliases resolve newest only on the Anthropic API | "aliases resolve to the newest version on the Anthropic API and to an earlier version on some other providers" | https://code.claude.com/docs/en/model-config | official-doc | unanimous | Haiku 5.5 prompts >100K tokens cost more; page partly unread |
| N29 | Higgsfield MCP URL for Claude connectors | "https://mcp.higgsfield.ai/mcp" | https://higgsfield.ai/creator-hub/help-center/integrations/how-do-i-connect-higgsfield-to-ai-agent | official-doc | contested | — |
| N30 | ChatGPT uses the Higgsfield Plugin | "ChatGPT uses the official Higgsfield Plugin from the Plugins Directory" | https://higgsfield.ai/creator-hub/help-center/integrations/how-do-i-connect-higgsfield-to-ai-agent | official-doc | contested | — |
| N31 | CLI agents install the Higgsfield CLI | "npm i -g @higgsfield/cli" | https://higgsfield.ai/creator-hub/help-center/integrations/how-do-i-connect-higgsfield-to-ai-agent | official-doc | unanimous | — |
| N32 | No audio or Website Building in ChatGPT | "Audio generation and the Website Building skill aren't available in ChatGPT." | https://higgsfield.ai/creator-hub/help-center/integrations/how-do-i-connect-higgsfield-to-ai-agent | official-doc | unanimous | Use claude.ai, Cursor or CLI for audio |
| N33 | Agent generations always deduct credits | "Every generation through a connected agent deducts credits, regardless of your plan." | https://higgsfield.ai/creator-hub/help-center/integrations/how-do-i-connect-higgsfield-to-ai-agent | official-doc | unanimous | Unlimited and free don't apply via MCP |
| N34 | No native credit cap | "There's no native credit cap." | https://higgsfield.ai/creator-hub/help-center/integrations/how-do-i-connect-higgsfield-to-ai-agent | official-doc | unanimous | Prompt limits are not hard limits |
| N35 | Results within about 60 s | "Results typically appear within 60 seconds of the job completing." | https://higgsfield.ai/creator-hub/help-center/integrations/how-do-i-connect-higgsfield-to-ai-agent | official-doc | unanimous | — |
| N36 | start_bpm ignored if a prior is given | "If provided, `start_bpm` will be ignored." | https://librosa.org/doc/0.11.0/generated/librosa.beat.beat_track.html | official-doc | unanimous | — |
| N37 | Multi-channel only with sparse=False | "multi-channel input is only supported when `sparse=False`." | https://librosa.org/doc/0.11.0/generated/librosa.beat.beat_track.html | official-doc | unanimous | Stereo with sparse=True fails |
| N38 | Tempo returned as an ndarray | "By default, the tempo is returned as an ndarray even for mono input." | https://librosa.org/doc/0.11.0/generated/librosa.beat.beat_track.html | official-doc | unanimous | — |
| N39 | Beat units default to frames | "By default, 'frames' are used." | https://librosa.org/doc/0.11.0/generated/librosa.beat.beat_track.html | official-doc | unanimous | — |
| N40 | ParameterError on missing input or bad units | "if neither `y` nor `onset_envelope` are provided, or if `units` is not one of" | https://librosa.org/doc/0.11.0/generated/librosa.beat.beat_track.html | official-doc | unanimous | — |
| N41 | No onsets gives 0 BPM and empty beats | "beat_tracker estimates 0 BPM and returns an empty list." | https://librosa.org/doc/0.11.0/generated/librosa.beat.beat_track.html | official-doc | unanimous | Silent audio yields no beats |
| N42 | Time-varying bpm shape must match | "the shape of `bpm` should match that of `onset_envelope`" | https://librosa.org/doc/0.11.0/generated/librosa.beat.beat_track.html | official-doc | unanimous | — |
| N43 | sparse=False gives a dense boolean array | "detections are encoded as a dense boolean array" | https://librosa.org/doc/0.11.0/generated/librosa.beat.beat_track.html | official-doc | unanimous | — |
| N44 | Both Manim skills install in one command | "npx skills add adithya-s-k/manim_skill" | https://github.com/adithya-s-k/manim_skill | repo | unanimous | — |
| N45 | Install the CE skill by path | "npx skills add adithya-s-k/manim_skill/skills/manimce-best-practices" | https://github.com/adithya-s-k/manim_skill | repo | unanimous | — |
| N46 | Manim CE pip install | "pip install manim" | https://github.com/adithya-s-k/manim_skill | repo | unanimous | — |
| N47 | ARM macOS ManimGL prerequisites | "arch -arm64 brew install pkg-config cairo" | https://github.com/adithya-s-k/manim_skill | repo | unanimous | Install fails without them |
| N48 | CE and GL are incompatible | "These are separate, incompatible frameworks." | https://github.com/adithya-s-k/manim_skill | repo | unanimous | Code doesn't port between them |
| N49 | Parallel tests can OOM | "Parallel testing with many workers can cause out-of-memory errors." | https://github.com/adithya-s-k/manim_skill | repo | unanimous | Too many workers exhaust memory |
| N50 | Claude defaults to safe design choices | "defaults to safe choices unless explicitly encouraged otherwise." | https://platform.claude.com/cookbook/coding-prompting-for-frontend-aesthetics | official-doc | unanimous | — |
| N51 | Avoid generic fonts | "Avoid generic fonts like Arial and Inter" | https://platform.claude.com/cookbook/coding-prompting-for-frontend-aesthetics | official-doc | unanimous | — |
| N52 | Dominant colours with sharp accents | "Dominant colors with sharp accents outperform timid, evenly-distributed palettes." | https://platform.claude.com/cookbook/coding-prompting-for-frontend-aesthetics | official-doc | unanimous | — |
| N53 | One orchestrated staggered load | "one well-orchestrated page load with staggered reveals" | https://platform.claude.com/cookbook/coding-prompting-for-frontend-aesthetics | official-doc | unanimous | — |
| N54 | CSS-only for HTML, Motion for React | "Prioritize CSS-only solutions for HTML. Use Motion library for React when available." | https://platform.claude.com/cookbook/coding-prompting-for-frontend-aesthetics | official-doc | unanimous | — |
| N55 | Outputs converge on common choices | "You still tend to converge on common choices (Space Grotesk, for example)" | https://platform.claude.com/cookbook/coding-prompting-for-frontend-aesthetics | official-doc | unanimous | Repeated generations converge on the same fonts |
| N56 | Helper parses a fenced html block | "Our parser depends on this format - do not deviate from it!" | https://platform.claude.com/cookbook/coding-prompting-for-frontend-aesthetics | official-doc | contested | Missing block raises an error |
| N57 | Remotion skills npx install | "npx skills add remotion-dev/skills" | https://aiidelist.com/blog/opus-5-5-motion-design | tutorial | unanimous | No version pin or verification documented |
| N58 | HyperFrames skills npx install | "npx skills add heygen-com/hyperframes" | https://aiidelist.com/blog/opus-5-5-motion-design | tutorial | unanimous | Preview and render commands not given |
| N59 | Opus 5.5 release date claim | "Anthropic lists Opus 5.5 as a September 22, 2026 release." | https://aiidelist.com/blog/opus-5-5-motion-design | tutorial | unanimous | No source link |
| N60 | Headline hold of at least 1.2 s | "Hold the primary headline fully readable for at least 1.2 seconds" | https://aiidelist.com/blog/opus-5-5-motion-design | tutorial | unanimous | Example timing, not a tested threshold |
| N61 | Pure function of time for determinism | "The same time value must always produce the same visual state." | https://aiidelist.com/blog/opus-5-5-motion-design | tutorial | contested | Unseeded randomness causes render differences |
| N62 | Not a cinematic text-to-video model | "Opus 5.5 does not natively behave like a cinematic text-to-video model." | https://aiidelist.com/blog/opus-5-5-motion-design | tutorial | unanimous | Photoreal humans and real physics poorly suited |
| N63 | Remotion CLI skills subcommands | "npx remotion skills <subcommand>" | https://www.remotion.dev/docs/cli/skills | official-doc | unanimous | Only add and update documented |
| N64 | add installs from remotion-dev/skills | "Install skills from `remotion-dev/skills`:" | https://www.remotion.dev/docs/cli/skills | official-doc | unanimous | No flags or pinning documented |
| N65 | update refreshes skills | "Update skills from `remotion-dev/skills`:" | https://www.remotion.dev/docs/cli/skills | official-doc | unanimous | Behaviour if never added is undocumented |
| N66 | Installs to .agents/skills | "Skills are installed to the `.agents/skills` directory in your project." | https://www.remotion.dev/docs/cli/skills | official-doc | unanimous | Path configurability undocumented |
| N67 | Claude Code compatibility via symlink | "symlinking `.claude/skills` to `.agents/skills`." | https://www.remotion.dev/docs/cli/skills | official-doc | unanimous | Symlink creation, Windows and existing dirs unclear |
| N68 | HyperFrames seeks, never plays | "The renderer never calls play()." | https://www.heygen.com/research/html-to-video | blog | contested | Wall-clock animation breaks |
| N69 | rAF doesn't fire in BeginFrame mode | "rAF doesn't fire in beginFrame mode." | https://www.heygen.com/research/html-to-video | blog | unanimous | rAF polling hangs |
| N70 | Single worker for video-heavy renders | "drop back to a single worker for video-heavy renders." | https://www.heygen.com/research/html-to-video | blog | unanimous | Decoder exhaustion |
| N71 | Opus 5.5 outputs text only | "It outputs text only." | https://huggingface.co/blog/karmen-beatapi/how-to-make-videos-with-claude-opus-5-5 | tutorial | unanimous | Never emits frames or MP4 |
| N72 | DURATION and async seek contract | "The scene must set `window.DURATION` and expose `async window.seek(t)`." | https://huggingface.co/blog/karmen-beatapi/how-to-make-videos-with-claude-opus-5-5 | tutorial | unanimous | Missing contract breaks render |
| N73 | 1M context, 128K output | "with a 1M-token context window and up to 128K output tokens" | https://huggingface.co/blog/karmen-beatapi/how-to-make-videos-with-claude-opus-5-5 | tutorial | unanimous | Figures may change |
| N74 | Max starts at $100/month | "From $100" | https://claude.com/pricing | pricing | unanimous | — |
| N75 | Higgsfield plan prices | "$15/month for Starter (200 credits), $34/month for Plus (1,000 credits)" | https://creatify.ai/blog/what-is-higgsfield-mcp-what-it-does-what-it-costs-and-how-to-use-it | blog | unanimous | Competitor-authored, not verified |
| N76 | Premium video models cost 40–70 credits | "Premium models like Veo 3.1 and Kling 3.0 consume 40-70 credits per generation." | https://creatify.ai/blog/what-is-higgsfield-mcp-what-it-does-what-it-costs-and-how-to-use-it | blog | unanimous | — |
| N77 | Starter credits run out in days | "Starter's 200 credits runs out in 3-5 days of active use on premium models" | https://creatify.ai/blog/what-is-higgsfield-mcp-what-it-does-what-it-costs-and-how-to-use-it | blog | unanimous | Heavy iteration exhausts Starter |
| N78 | 15+ video models in one subscription | "Higgsfield aggregates 15+ AI video models under one subscription" | https://creatify.ai/blog/what-is-higgsfield-mcp-what-it-does-what-it-costs-and-how-to-use-it | blog | unanimous | — |
| N79 | Unlimited covers lower tiers only | "Unlimited access limited to lower-tier models only" | https://creatify.ai/blog/what-is-higgsfield-mcp-what-it-does-what-it-costs-and-how-to-use-it | blog | unanimous | Premium still uses credits |
| N80 | Unlimited may be throttled | "Unlimited usage may be throttled during high-traffic periods" | https://creatify.ai/blog/what-is-higgsfield-mcp-what-it-does-what-it-costs-and-how-to-use-it | blog | unanimous | Throttling stalls batches |
| N81 | librosa.load mixes to mono at 22050 Hz | "By default, all audio is mixed to mono and resampled to 22050 Hz at load time." | https://librosa.org/doc/0.11.0/tutorial.html | official-doc | unanimous | Mismatched sr causes drift |

**Reference videos**

| ID | Title | Channel | URL | Status |
|---|---|---|---|---|
| V1 | I Had Opus 5.5 Make the Same Music Video at Every Effort | Devarf | https://www.youtube.com/watch?v=3S4vuHxGh7c | Single-creator measurement; costs are estimates at API prices |
| V2 | Claude Opus 5.5 + JavaScript = INSANE 2D Animations (Full Tutorial) | RandomAI | https://www.youtube.com/watch?v=MPDhk385gSg | Tutorial |
| V3 | Claude Opus 5.5 Is INSANE at Motion Graphics | RandomAI | https://www.youtube.com/watch?v=OIAWkkSO4WY | Tutorial |
| V4 | Claude Opus 5.5 Makes INSANE Educational Animations (Full Tutorial) | RandomAI | https://www.youtube.com/watch?v=WXu4O9oIdIE | Tutorial, Higgsfield-sponsored; master prompt in description |
| V5 | Claude Fable 5.5 Just Got Leaked and It's INSANE | RandomAI | https://www.youtube.com/watch?v=BbsoRYprICI | Unverified capability signal |