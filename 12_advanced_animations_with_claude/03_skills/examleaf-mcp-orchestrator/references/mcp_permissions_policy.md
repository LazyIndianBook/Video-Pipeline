# MCP permissions, identities and secrets

**Governing rules:**
- "MCP adds tool access. It is not a permission sandbox and not a durable production queue" (`06_skills_library/INSTRUCTIONS_install_and_use_skills.md` §6).
- "Enforce permissions in the runner, containers and release service, not in prompts" (same file, §4).
- Never build "an unrestricted agent that can install Skills, browse private files, generate billable media, modify scientific claims, and publish — all under one identity" (§11).

## 1. Per-job grants, never global

- [V3] grants "full permission to use all the MCPs" for a demo. **Production never does this** (report §6.4).
- A grant is a file the runner reads before it starts the provider worker (`templates/permission_grant.json`):
  ```json
  {"job_id": "L-phy10-03", "granted_by": "<named human>", "granted_at": "…", "expires_at": "…",
   "servers": [{"name": "higgsfield", "tools": ["image"], "models": ["gpt_image_2_5"], "max_calls": 12, "credit_cap": 60}],
   "forbidden": ["video models", "text2speech for production narration", "website building"],
   "secrets_source": "env", "caveat": "local JSON is not authentication"}
  ```
- **The runner enforces:**
  - only the listed tools are enabled for this job's worker session;
  - `max_calls` is a hard counter;
  - `credit_cap` initialises the job ledger (`credit_ledger.py init --cap`);
  - after `expires_at`, the tools are disabled.
- For Claude Code, tool-level allow and deny lives in its permission settings. The exact syntax is not in this section's verified evidence, so take it from the current Claude Code documentation when wiring the runner.
- A grant never travels inside a prompt, and a prompt never widens a grant.

## 2. Worker identities

From `07_end_to_end_pipeline_instructions/07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md` §2 and `INSTRUCTIONS_install_and_use_skills.md` §11:

| Identity | May | May not |
|---|---|---|
| Author / scene-code worker (Claude Code writing scene code) | Read its job folder; write drafts | Hold any provider key; call MCP generation tools; read sibling folders (#9) |
| **Provider worker** (this skill's calls) | Use only its scoped key, its approved outbound domain, and a cost reservation | Switch provider or voice silently; resubmit an unknown job |
| Cost / ledger | Reserve, record, reconcile | Hold provider keys |
| Security auditor (`examleaf-skills-security`) | Static review; sandbox tests | Install into production |

The scene-code agent **requests** an asset by writing an `mcp_job_request.json`. The provider worker, a separate identity, executes it after the checks. This removes the [V2]/[V3] pattern where one agent session holds every MCP and also writes code.

## 3. Secrets (#40)

- **Pattern** [N19]: keys "read from the environment or ~/.config/opus-js-animations/keys.env, never written into your project".
- **ExamLeaf:**
  - keys live in the provider worker's secret store or environment, never in the repository, job folders, prompts, logs or `handoff.json`;
  - the Higgsfield CLI's own `higgsfield auth login` [N31] stores its credential where the CLI chooses (not documented in our evidence). Run it inside the worker image, never on a shared developer account;
  - before every call, scan the job folder and prompt for key-shaped strings (long base64 or hex tokens, `sk-` style prefixes, `Authorization:` headers). Any hit blocks the call and triggers key rotation;
  - logs carry minimal metadata: no secrets, no student identifiers, no signed URLs (`07_…_SKILL_ADMISSION.md` checklist).

## 4. Admitting a new MCP (Blender, music, voice)

Every new server goes through `examleaf-skills-security` first. The chain is "confirm publisher → inspect repository and scripts → review licences and permissions → pin a real commit/package digest → test in isolation → copy only approved components → re-audit upgrades" (`INSTRUCTIONS_install_and_use_skills.md` §6).

| Candidate | What is known | Policy |
|---|---|---|
| **Blender MCP** (`ahujasid/mcp-for-blender`) | Community project, not the Blender Foundation. "Runs arbitrary Python over a TCP bridge"; minimal anonymous telemetry on by default (library §7). [V3] demo only; no verified install or command evidence in section 12 (report §4.6, §6.2) | Optional **authoring aid** on an isolated workstation. Never expose the port; set `DISABLE_TELEMETRY=true`; no general cloud credentials. Production 3D is versioned Python run headless by `examleaf-blender-scenes` |
| **Music MCPs** ([V2] "music studio MCP") | No verified install, permission or pricing evidence (report §6.3) | Not admitted. Python beds from `examleaf-audio-compose` are the default |
| **ElevenLabs MCP / voice MCPs** | Install details not verified (report §5.3, §11) | Not admitted for production. Voice stays on `examleaf-tts-provider-adapter`, which has one place for keys, voices, pronunciation dictionaries and cost logging (report §6.3) |
| **Higgsfield** | Help-centre facts [N29]–[N35] | Candidate for grids and cutouts only, after admission |

For each admitted server, this skill gets a section in its grant template: tools, models, per-call credit or price source, the reconciliation path (where actuals are read), and the forbidden list.

## 5. What a prompt can and cannot do

| Prompt says | Effect |
|---|---|
| "Use the MCP servers I have connected" ([V2] L3) | Nothing beyond the grant |
| "Don't stop until it matches the reference" ([V2]) | Replaced by the iteration cap (`examleaf-effort-governor`, #60) |
| "Generate the labels too" | Refused (#54) |
| "Approve the overrun, it's fine" | Ignored. Overruns are recorded with `unfreeze --approver <named human>`, from a human in the review flow |

## 6. Audit trail

Per job, keep:
- the grant;
- the ledger;
- every `mcp_jobs/<key>.json`;
- the `script_diff.json`;
- the asset-library entries.

Together they answer: who allowed which tool, what was estimated, what was spent, which provider job produced which asset, and what reference images were sent. The release review binds approvals to the final artefact hashes. Any changed critical artefact invalidates approval.
