# Safe installation and execution
## Public package admission
1. Resolve the official repository and its current redirect. Fetch a commit and read metadata, licence, package manifests, install hooks, Skill scripts and MCP entrypoints without executing them.
2. Record an exact commit, distribution checksum and transitive dependency lock. Inspected file blob SHAs in this delivery are not usable commit pins.
3. Inspect filesystem scope, outbound domains, telemetry, subprocesses, arbitrary code execution and credential loading. A Skill's allowed-tools list is not an OS sandbox.
4. Evaluate in a disposable user/container without production credentials, Docker socket or student data. Disable package scripts by default; approve essential build steps individually.
5. Install only selected reviewed Skill folders. Block on-demand auto-install/update in production.
6. Run positive, negative, timeout, cost-cap and exfiltration tests. Re-audit upgrades in a pull request.

## Examples after a maintainer has approved the revision
```sh
git clone --no-checkout https://github.com/elevenlabs/skills.git vendor/elevenlabs-skills
# Replace APPROVED_COMMIT with a real reviewed commit SHA, not a blob SHA.
git -C vendor/elevenlabs-skills checkout --detach APPROVED_COMMIT
mkdir -p .claude/skills .agents/skills
# Inspect first; then copy only text-to-speech, not the entire repository.
cp -R vendor/elevenlabs-skills/text-to-speech .claude/skills/
```
These illustrative commands were not executed here. For reproducibility pin the skills installer itself if using npx skills. Prefer reviewed local copies to downloading current main at every run.

## Runtime separation
Untrusted author/research worker: no production API keys, no publishing credentials. Renderer: no internet after assets are staged; read-only input, bounded resources, no arbitrary source expressions. Provider worker: only its scoped key, approved outbound domain and cost reservation. Publisher: only approved artifact hashes and explicit release authority.

## Blender MCP
The renamed mcp-for-blender is third-party. Arbitrary Python execution and a local TCP bridge require isolation. Do not expose the port, assume safe-mode is a full sandbox, or run with general cloud credentials. Current content telemetry is opt-in; minimal anonymous usage is on by default. Set DISABLE_TELEMETRY=true to disable all telemetry. Production should render reviewed scripts headlessly, not run an unconstrained MCP conversation.

## Local proof boundary
This repository's approval objects are an executable policy demonstration, not authenticated role access. Integrate an authenticated review service, append-only audit log and artifact signatures before production. Path/URI fields are data; remote fetching is not implemented.
