# Remotion notes

Remotion is the benchmark challenger to HyperFrames (report §2.2, §2.6).

## Verified facts (evidence set)

| Fact | Source |
|---|---|
| Install agent skills: `npx skills add remotion-dev/skills` | [N1] |
| Skills may be offered at project creation | [N2] (contested) |
| Skills target Claude Code, Codex, Kimi Code, Cursor | [N3] |
| `/remotion-best-practices` "encompasses all other skills" | [N4] |
| `/remotion-render` renders a video or still | [N5] |
| `/remotion-maps` covers Mapbox, MapLibre, MapTiler, GeoJSON, CesiumJS flyovers | [N6] |
| `/remotion-upgrade` upgrades Remotion, related packages, compatible Mediabunny packages and installed skills | [N7] |
| CLI family `npx remotion skills <subcommand>`; `add` [N64] and `update` [N65] documented | [N63] |
| Skills install to `.agents/skills` | [N66] |
| Claude Code compatibility via symlinking `.claude/skills` to `.agents/skills` | [N67] |

## Not verified

- Commercial licence terms for a company of ExamLeaf's size (the library lists Remotion as a "conditional commercial licence for the engine"); read the current licence before any commercial decision (report §2.2, §11.3).
- Required Node version, captions and audio APIs, error catalogue.
- Whether `skills add` creates the `.claude/skills` symlink, and how it treats Windows or an existing folder [N67]; behaviour of `update` before `add` [N65] — always `add` first (#27).

## Conformance mapping [Hypothesis]

Remotion renders by frame number rather than by a `seek(t)` export. A scene written to the ExamLeaf contract maps onto Remotion by deriving `t = frame / fps` inside the component and calling the same pure `render(t)` logic; fixtures arrive as typed props from validated JSON. Verify the exact frame hook and interpolation helpers in the current docs via `/remotion-best-practices` [N4]; `contract.md` §17 holds the informative Remotion mapping, also marked **verify API**. The determinism test is the same: render twice, hash PNG frames.

## Benchmark rules (report §2.6)

- Same three test lessons (physics, chemistry, biology) in both engines.
- Measure render time, determinism (identical frame hashes across two renders), agent token cost per scene, fix-loop count and reviewer edit time.
- Run `/remotion-upgrade` before benchmarking to avoid version drift (#25) [N7].
- Check the `.claude/skills` symlink after installing skills (#26) [N66][N67]; `preflight.sh` reports it.
- Composition size 1080×1920 to be confirmed in the benchmark (report §2.2 [Hypothesis]).
