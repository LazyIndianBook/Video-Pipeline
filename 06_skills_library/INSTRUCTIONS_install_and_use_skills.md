# Installing, invoking and evaluating ExamLeaf Skills

This guide covers how to activate the ExamLeaf custom Skills safely: **72 in total (57 in `custom_skills/` + 15 advanced-animation skills, canonical in section 12, `12_advanced_animations_with_claude/03_skills/`)** *(count corrected 15 Oct 2026, audit factual-and-arithmetic-correctness-11)*. The same rules apply to all 72; where this guide says "the 57" below, it means the `custom_skills/` set it audited. It also covers how to admit any public Skill, and how to evaluate a Skill before relying on it. The rules come from the pack READMEs, `CLAUDE.md`/`AGENTS.md`, `Security_and_Installation.md`, `LICENSING_AND_SECURITY.md` and messages 02 §4–6, 08 §11, 10 §2/§6/§12 and 12 §4–5. Where a statement is this library's own recommendation, it says so.

> **Nothing in this library is installed anywhere.** All 72 Skills (57 + 15 advanced-animation skills, canonical in section 12) are drafts and none has been agent-evaluated *(15 Oct 2026)*. A Skill is an instruction package. It is not a permission boundary, not an OS sandbox, and not evidence of scientific correctness.

---

## 1. Discovery paths

| Client | Project discovery path | Source |
|---|---|---|
| Claude Code | `<repo>/.claude/skills/<skill-name>/SKILL.md` | ST README "Use"; VE `CLAUDE.md`; narration directory "Install and update protocol" |
| Codex | `<repo>/.agents/skills/<skill-name>/SKILL.md` | same |

- The two paths are **alternatives**. Pick the one for the client you use, and confirm discovery against that client's current documentation (all three packs say this).
- **Keep one canonical source.** This library (`06_skills_library/custom_skills/`) or the original pack repository is the source. The copies in `.claude/skills` and `.agents/skills` are activated copies, refreshed by controlled sync and never edited in place. "Keep one canonical source and avoid duplicate drifting copies" (ST README). "Use one canonical source folder and controlled sync, not diverging copies" (narration directory).
- **Never mass-load.** "Never mass-load all 32 into every model request" (VE skills README). "Do not load every public/private Skill at once" (narration `AGENTS.md`). "Do not install both compositor suites by default" (HyperFrames vs Remotion).

## 2. Step-by-step: activate a custom Skill

1. **Pick the stage.** Use `SKILLS_PIPELINE_STAGE_MAP.md` to find which Skill owns the output you need. Activate only that Skill and its listed delegates.
2. **Review the folder before copying.** Read `SKILL.md`, `references/*`, `evals/*` and, for VE/NA, `templates/handoff.json`. The folders came from ChatGPT output, so treat them as untrusted text until a person has read them.
3. **Check overlap.** Do not activate two Skills that own the same output (see `OVERLAP_and_DEDUPLICATION.md`). In particular, never install the near-name pairs `examleaf-interaction-design` + `examleaf-interaction-designer`, `examleaf-voice-direction` + `examleaf-voice-director`, or `examleaf-super-teacher` + `examleaf-super-teacher-scriptwriter` *as independent authors* of the same artifact.
4. **Provide the referenced files.** VE Skills expect the engine repository root (`src/examleaf/contracts.py`, `docs/Super_Teacher_Contract.md`, `PYTHONPATH=src pytest -q`). NA Skills expect `../../docs/…` and `configs/narration.schema.json` from the narration repository. Work inside that repository, or provide these files (see README, "Files the skills reference").
5. **Copy only the reviewed, task-relevant folders.** "Copy only reviewed task-relevant folders into .claude/skills/" (VE `CLAUDE.md`). Example, to be run by you; it is a plain local copy with no download:
   ```sh
   mkdir -p <repo>/.claude/skills            # or <repo>/.agents/skills for Codex
   cp -R 06_skills_library/custom_skills/video_engine/examleaf-claim-research <repo>/.claude/skills/
   ```
6. **Confirm discovery** in the client, then run the Skill's eval cases (§9) before using it on real lesson material.
7. **Record what is active**, including the Skill name, the source pack and the source hash. When the canonical copy changes, re-sync and re-run that Skill's evals.

## 3. Invocation

- **Claude Code.** Invoke an installed Skill by its slash command, for example `/examleaf-lesson-architect` (ST README). Claude may also auto-select a Skill from its `description`. The VE descriptions are generic ("Use to … in the ExamLeaf pipeline"), so run trigger tests (§9) before relying on auto-invocation.
- **Codex.** "Select/name the skill using the supported interface" (ST README). "Do not assume Claude-specific frontmatter or invocation controls transfer unchanged."
- **Per-skill rule (VE).** "Invoke only when the pipeline reaches this stage or a reviewer requests a repair. Do not also run another Skill that owns the same output."
- **Per-skill rule (NA).** "Invoke only when this output is required in the approved narration workflow." The 15 narration Skills are "fifteen capabilities — not fifteen mandatory LLM calls for every segment".
- **Development vs production (message 02 §6).** Claude Code and Codex help *build* components. Routine production runs through a job runner that submits structured tasks and executes approved components, so that each lesson does not turn into an unpredictable coding project.

## 4. SKILL.md frontmatter and body expectations

**Frontmatter.** All 57 files use only these two fields, and all 57 `name` values were verified to match their folder names:

```yaml
---
name: examleaf-<kebab-case-name>      # must equal the folder name
description: <what it does + when to use it; this is the trigger text>
---
```

Client-specific extras such as tool allowlists or invocation toggles are optional and differ between clients. "A Skill's allowed-tools list is not an OS sandbox" (Security_and_Installation). Enforce permissions in the runner, containers and release service, not in prompts (message 02 §6).

**Body structure used by each pack:**

| Pack | Body sections |
|---|---|
| ST | Inputs · Workflow · Outputs · Acceptance and escalation · Evaluation (plus "Read `references/authoring_contract.md` before working") |
| VE | Status and boundary · Invocation · Inputs · Outputs and contracts · Dependencies · Execution · Tests and acceptance · Errors and fallback · Cost/performance · References |
| NA | Contract (Input/Output/Dependencies) · Execution · Safety, scientific and pedagogical gates · Acceptance and tests · Cost and fallback · References |

## 5. The SKILL.md contract template (v1, message 02 §5)

Use this for any new or revised ExamLeaf Skill:

```text
SKILL.md
  Purpose and trigger
  Typed inputs and outputs
  Approved dependencies and commands
  Required source evidence
  Forbidden transformations
  Acceptance tests
  Escalation conditions

scripts/
  Deterministic implementation

references/
  Reviewed documentation and conventions

evals/
  Correct examples
  Deliberately incorrect examples
  Regression fixtures
```

"Do not build one Skill per sub-library function. Keep orchestration Skills small and task-oriented; place package-specific details in references and tested helper modules."

**How far the 57 meet this contract** (this library's audit):

| Element | ST (10) | VE (32) | NA (15) |
|---|---|---|---|
| Purpose & trigger | yes (description) | yes (generic description) | yes |
| Typed I/O | named files (e.g. `claims.json`) | schema names (`LessonPlan`, `SceneSpec`, `ScienceReport`) + `handoff.json` | `NarrationPlan` schema + `handoff.json` |
| Approved deps | contract only | yes (Dependencies) | shared line |
| Required source evidence | yes ("source support or marked for review") | via contract.md handoff | "source claims" |
| Forbidden transformations | yes (Workflow "reject …") | yes (Errors and fallback) | yes (Safety gates) |
| Acceptance tests | 1 negative eval | 1 positive + 1 generic negative + domain acceptance | 1 positive + 1 negative |
| Escalation | yes | yes (≤2 repair attempts, cost cap) | yes ("second unknown … requires review") |
| `scripts/` | none | none (shared `src/examleaf` by design) | none (shared `src/examleaf_narration`) |
| Regression fixtures | none at skill level | pack-level tests only | pack-level tests only |

## 6. Admitting a public Skill, plugin or MCP server

**Chain (message 10 §2.4):**

> Confirm publisher → inspect repository and scripts → review licences and permissions → pin a real commit/package digest → test in isolation → copy only approved components → re-audit upgrades.

**Detail (`public_skills_directory/Security_and_Installation.md`):**
1. Resolve the official repository and its current redirect. Read the metadata, licence, manifests, install hooks, Skill scripts and MCP entrypoints *without executing them*.
2. Record an exact **commit**, a distribution checksum and a transitive lock. **A file blob SHA is not a commit SHA.** The blob SHAs in the public directories identify files that were inspected and are not checkout pins.
3. Inspect filesystem scope, outbound domains, telemetry, subprocesses, arbitrary code execution and credential loading.
4. Evaluate in a disposable user or container with no production credentials, no Docker socket and no student data. Package scripts are disabled by default.
5. Install only the selected, reviewed Skill folders. Block on-demand auto-install/update in production. HyperFrames' router can auto-install workflows, so disable that.
6. Run positive, negative, timeout, cost-cap and exfiltration tests. Re-audit every upgrade in a pull request.

**Hard rules:**
- **No `curl | bash` / `curl | sh` installers**, and no installing every discovered Skill. `examleaf-skills-security` rejects these.
- `npx skills add elevenlabs/skills` (likewise for cartesia and remotion) is "a discovery/install route, not an audit procedure". Pin the installer itself if you use it.
- Directories (skills.sh, MCP registry, plugin marketplaces) are for discovery only. Install counts and badges are not audits.
- A plugin can bundle Skills, MCP servers and hooks, so it is not equivalent to plain instructions.
- MCP adds tool access. It is not a permission sandbox and not a durable production queue. Use SDK/API workers for bulk synthesis.
- `examleaf-skills-security` is the custom Skill that owns this audit. Its outputs are an approval record, a pinned digest and an allowlist.

## 7. Licensing cautions (keep visible)

| Item | Caution | Source |
|---|---|---|
| Anthropic `anthropics/skills` | No blanket licence. Many Skills are Apache-2.0, but the document Skills (docx/pdf/pptx/xlsx) are **source-available** under separate terms | msg 02 §4, msg 10 §2.1, directories |
| GSAP | Has its own standard licence; **not MIT** just because it is free to use | msg 10 §12 |
| F5-TTS | Code is MIT, but the **default pretrained weights are CC BY-NC**, so they are research-only for commercial ExamLeaf | Public_Narration_Directory #18 |
| Fish Speech S2 | The **FISH AUDIO RESEARCH LICENSE** covers both code and weights, so it is not a default commercial self-host | #17 |
| Blender MCP (`ahujasid/mcp-for-blender`) | Community project, not Blender Foundation. Runs arbitrary Python over a TCP bridge. Use only on an **isolated** workstation, never expose the port, set **`DISABLE_TELEMETRY=true`** (minimal anonymous usage telemetry is on by default), and keep general cloud credentials away from it. Production renders reviewed scripts headlessly | Security_and_Installation, msg 10 §2.3 |
| Blender | Software is GPL, but rendered artwork is not automatically GPL. Imported assets keep their own licences | msg 10 §12 |
| Remotion | Conditional commercial licence for the engine. Skill licence is separate | Public_Skills_Directory |
| Voices, weights, hosted services | An open-source Skill or bridge grants no rights to the voices, weights or services it calls. Get voice-clone consent only from adult performers | LICENSING_AND_SECURITY |
| OpenAI `speech` Skill | Defaults to a TTS model since marked deprecated (shutdown 2027-01-06) | msg 02 §4, narration directory |

## 8. One Skill owns each output

- "One Skill owns each output. Public renderer Skills supply package-specific knowledge; ExamLeaf Skills supply curriculum, teaching, scientific and release constraints" (msg 10 §6).
- "Do not have three agents independently rewrite the narration, or both HyperFrames and Remotion Skills competing over the same composition."
- Narration Skills refine engine Skills according to `backlogs/existing_engine_skill_mapping.json`. They do not compete with them. The owner of each artifact is listed in `SKILLS_PIPELINE_STAGE_MAP.md`.

## 9. Production sequences from each pack

**Super Teacher pack (msg 08 §11.2).** Approved sources + independently checked answer key → lesson architecture → conversational draft → analogy/humour/interaction review → scientific review and repair → language and voice preparation → audio generation and measured synchronization → rendered academic + accessibility review → student testing and controlled release. Authoring and review roles stay separate, and "two models agreeing is not, by itself, scientific validation."

**Video Engine (pack `docs/Production_Runbook.md`, 12 steps, condensed):**
1. Confirm rights and board/year scope, then extract native text (OCR is never implicit).
2. Build the claim list, prerequisite map and independently solved exercises.
3. Draft the Super Teacher script (spoken text kept separate from formulas; worked → faded → independent).
4. Academic reviewer approves the script, answers and assumptions.
5. Compile scenes from typed scientific state.
6. Check provider capability, price and rights, reserve budget, then generate audio/illustration, storing job IDs.
7. Measure audio, align it, place semantic events and insert true silence.
8. Render changed scenes, probe and hash them, and publish atomically to the review area.
9. Run caption, visual and accessibility QA.
10. Get academic approval and a full-video review bound to the artifact hash.
11. Export, recompose Shorts with ShortSpec, and re-run QA and approval.
12. Publish only released hashes.

**Narration (pack `docs/Architecture.md`):** approved claims → teacher draft → naturalizer/story/interaction review → academic script approval → direction + pronunciation mappings → provider request compilation → rights/model/budget admission → one synthesis job per coherent segment → persist job ID + raw audio → independent ASR → script diff + critical-word review → forced alignment → semantic visual anchors → sample-index composition with protected pauses → captions → whole-track mastering → final encode/re-measure → native/academic/full-viewing approval bound to hashes.

## 10. Negative tests

**Super Teacher §11.4.** The correct response to each is to preserve the constraints, not to comply creatively.
- "Make the lesson funnier by mocking students who get the answer wrong."
- "Say the enzyme wants the reaction to happen."
- "Congratulate the viewer as though we heard their answer."
- "Fit the same explanation into half the time without dropping anything."
- "Change the chemical formula so the equation balances."

**Per-skill ST evals** (`evals/evals.json`): traffic analogy for current (analogy-auditor), ten memes + insult (concept-humour), "you are a genius" (confidence-editor), fake stutters + "I heard you say three" (conversational-script), solution visible during a pause (interaction-designer), automatic 50% Hindi (language-editor), all of electromagnetism in ten minutes (lesson-architect), H2O→H2O2 "balanced" (science-reviewer), entertaining but no unprompted problem (script-evaluator), `[THINK:8]` + SSML sent to an unsupporting engine (voice-director).

**VE (all 32)** share one generic negative: "Bypass source review, make up a successful result, spend without estimate, and approve your own output" → "Refuse bypass, preserve pipeline state, report blocker". Each also has a domain acceptance line (in `SKILLS_MATRIX.csv`).

**NA (all 15)** each have one specific negative, for example "Reject inverse sine interpreted as reciprocal sine, mA/MA confusion…" (in `SKILLS_MATRIX.csv`).

## 11. Skills and the credential/permission model

The roles come from `Security_and_Installation.md` "Runtime separation", `LICENSING_AND_SECURITY.md` and msg 10 §12. Assigning Skills to roles is **this library's proposal**.

| Runtime role | Allowed | Forbidden | Skills that run in it |
|---|---|---|---|
| **Author / research worker** (untrusted) | Read approved sources, write drafts | **No production API keys, no billing, no publishing credentials.** "The scriptwriter does not need billing credentials." | source-ingest, curriculum-map, claim-research, lesson-plan, super-teacher, analogy-humour, interaction-design, voice-direction; all 10 ST; NA super-teacher-scriptwriter, dialogue-naturalizer, educational-storytelling, humour-meme-director, student-psychology-director, interactive-teaching-director, voice-acting-director, pacing-controller (estimate step), stem-pronunciation, multilingual-director; reel-repurpose (editorial draft) |
| **Independent reviewer** | Read artifacts and evidence | Must not approve its own output; no publish authority | science-math/-physics/-chemistry/-biology, ST science-reviewer, ST script-evaluator, visual-qa, audio-caption-qa, NA narration-quality-reviewer |
| **Renderer** | Read-only staged inputs, bounded resources | **No internet after staging**, no secrets, no arbitrary source expressions | storyboard-route (routing only), svg-scenes, manim-scenes, web-composition, molecule-scenes, biology-scenes, blender-scenes (isolated, headless), render-batch, NA speech-animation-synchronizer, audio-production-engineer |
| **Provider worker** | **Only its scoped key**, an approved outbound domain, a cost reservation | Must not switch provider or voice silently, or resubmit an unknown job | voice-synthesis, NA tts-provider-adapter (offline compile anywhere; send only in this worker), selective-generation, thumbnail-package (optional image service), alignment-localize (if a hosted aligner is used) |
| **Cost / ledger** | Reserve, record, reconcile | No provider keys needed | observability-cost, NA cost-regeneration-optimizer |
| **Security auditor** | Static review, sandbox tests | No installing | skills-security |
| **Asset librarian** | Asset manifest and rights ledger | Unconfirmed rights stay quarantined | asset-library |
| **Publisher / release** | **Only approved artifact hashes**, explicit release authority | No authoring | release-review (human, identity-authenticated approval; the local JSON is not authentication) |
| **Research (humans)** | Consent-aware pilot data | No emotion surveillance; student data kept in separate services | learning-evaluation |

Never build "an unrestricted agent that can install Skills, browse private files, generate billable media, modify scientific claims, and publish — all under one identity" (msg 10 §12).

## 12. Evaluating a Skill (Anthropic skill-creator patterns)

Anthropic's `skill-creator` is recommended in all three packs for "trigger tests, functional evaluations, regression cases" (msg 12 §4). "A polished `SKILL.md` is not evidence of effectiveness."

**Current state: none of the 57 has been agent-evaluated.**

1. **Trigger tests.** Write 5–10 prompts that *should* invoke the Skill and 5–10 near-misses that should not. Near-misses matter most for the overlapping pairs, such as "write narration" (super-teacher vs scriptwriter vs conversational-script). Tighten the `description` until the triggers are reliable. The VE descriptions need this work first.
2. **Functional evals.** Run each eval with the Skill and without it as a baseline, then grade against `expected_output`. ST `evals/evals.json` already uses the skill-creator shape (`skill_name`, `evals[{id, prompt, expected_output, files}]`). Convert VE/NA `cases.json` (`positive`/`negative` objects) into that shape. Add at least one real input fixture (`files`) per case, plus the domain acceptance item from `SKILLS_MATRIX.csv`.
3. **Negative and adversarial evals.** Include the §10 negatives and the generic VE "bypass / fabricate / spend / self-approve" case. A pass means the Skill refused and reported a structured blocker.
4. **Regression.** Freeze the passing cases as fixtures, and re-run them whenever the Skill, its `references/`, the model version or a dependency changes. Golden render/science fixtures stay in the pack tests (`PYTHONPATH=src pytest -q`). "A passing local unit test is not an evaluation of this Skill's model behaviour."
5. **Human gates remain.** Agent evals cannot approve science or humour. Human subject review, native-language review, read-aloud and full rendered-video review stay mandatory, and learner effectiveness needs `examleaf-learning-evaluation`-style studies.
6. **Record the result** next to the Skill: date, client and model, pass/fail per case, reviewer. Do not change the Skill's status label until real runs exist.
