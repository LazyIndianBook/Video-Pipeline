# ElevenLabs Eleven v4: API and MCP setup (verified in the founder's browser, 16 Oct 2026)

> **Retired for narration on 27 Oct 2026 (PD-29, RD-55).** Voice-over is now local VoxCPM2 in the founder's cloned voice, and speech-to-text is local Whisper: see `local_voice_voxcpm2/SETUP.md`. Kept as the record of the pilot narrations. The API key in `~/.zshenv` is no longer used by the pipeline; rotate or delete it from the developers page.

Everything below was read from the live ElevenLabs dashboard and documentation on 16 Oct 2026 using the founder's logged-in Chrome session. Nothing here was synthesised; no credits were spent.

## 1. Account state found

| Item | State on 16 Oct 2026 |
|---|---|
| Login | Logged in; dashboard home shows "Introducing Eleven v4" |
| Onboarding | **Not completed.** Every app page (`/app/subscription`, `/app/developers/api-keys`) redirects to `/app/onboarding` "Choose your platform" (ElevenCreative vs ElevenAgents, 5 steps). Pick **ElevenCreative** (Text to Speech, Voice Changer, Dubbing, Speech to Text). Left for the founder to complete: later steps ask personal and use-case questions |
| Plan | Unknown until onboarding completes. The free tier is documented at 10k credits per month |
| API key | None created yet (page unreachable before onboarding) |
| Cookie banner | Declined ("Reject all") |

### 1.1 Live check after the founder finished onboarding and created the key (16 Oct 2026, later the same day)

| Item | Result |
|---|---|
| Plan | **Free**: 10,000 characters per month, concurrency 2, no instant or professional voice cloning. Free-tier output is MP3 only; the plan's commercial-use and attribution terms must be read before any released artefact uses it (verify) |
| Key | Created by the founder, stored only in `~/.zshenv` (mode 600). **It was pasted into the Claude chat to get there, so it exists in the session transcript; rotate it from the developers page once the audition is over** |
| Models available to this account | `eleven_v4`, `eleven_v4_turbo` (94 languages incl. hi, as, bn), `eleven_v3` (74), `eleven_multilingual_v2` (29), `eleven_multilingual_sts_v2` (speech-to-speech; **hi yes, as no, bn no**: Assamese and Bengali conversion are not offered, which matches RD-42) |
| Voices in the account | 21 premade, all American, British or Australian English. No Indian-English or Hindi voice until one is added from the shared library |
| Shared library, Hindi (sorted by adoption, all `free_users_allowed`) | Devi "Encouraging and Motivating" (`MF4J4IDTRo0AxOO4dpFR`, female, young, informative_educational); Raju "Clear, Natural and Warm" (`zT03pEAEi0VHKciJODfn`, male, middle-aged, conversational); Monika Sogam "Calm and Natural" (`1qEiC6qsybMkmnNdVMbK`, female, middle-aged, narrative); Niraj, Bunty, Viraj, Rian, Ranga (entertainment and Reel registers) |
| Shared library, English with Indian accent | Ziina "Confident and Clear" (`FaqthkZu1EWxXxUFbAfb`, female, middle-aged); Ruhaan "Clear, Loud and Cheerful" (`siw1N9V8LmYeEWKyWBxv`, male, middle-aged); Maya "Friendly and Cheerful" (`4O1sYUnmtThcBoSBrri7`, female, middle-aged); Viraj "Energetic and Confident" (`bajNon13EdhNMndG3z05`, male, young); Monika Sogam, Anika, Bunty (social-media registers) |
| Smoke test | The compiler's first emitted request (segment `question`, 114 characters, `[curious]` tag, `language_code: en`, `seed: 20261016`) sent to `POST /v1/text-to-dialogue?output_format=mp3_44100_128` with the premade voice George: **HTTP 200**, 122,505 bytes, about 7.7 s of audio, 7.4 s latency, `request-id 7qe6fO79BCXq0CjsP1Jq`, concurrency 1 of 2, sha256 `b364410d…`. Saved outside the repository (scratchpad). The subscription counter still read 0 of 10,000 afterwards; the first bill may post later. Not a candidate voice and not an approved artefact: it proves the route, the key and the request shape only |
| Hosted MCP | Still `Needs authentication` (founder OAuth pending) |

**Before the audition.** Adding a shared voice to the account (`POST /v1/voices/add/{public_user_id}/{voice_id}`) is an account change and the Free plan has a small custom-voice allowance, so the lead asks the founder which three to add. Audition budget: two beats (hook and one explanation) × three voices × two locales ≈ 1,500 to 2,500 characters, inside the free allowance. Every output is rated against the native gate before any `voice/` entry is written.


## 2. Eleven v4 facts (docs, 16 Oct 2026)

- Model ids: `eleven_v4` (batch, highest quality) and `eleven_v4_turbo` (real-time, ~100 ms, Text to Dialogue websocket). `eleven_v3` is now "previous generation".
- **v4 is served only by the Text to Dialogue API**: `POST https://api.elevenlabs.io/v1/text-to-dialogue`, header `xi-api-key`. The plain `/v1/text-to-speech` route is not listed for v4. The 05 compiler already targets this route (`compiler.py` line 47) and emits `xi-api-key: ENV:ELEVENLABS_API_KEY`.
- Request body: `inputs[]` of `{text, voice_id}` (≤10 unique voices), `model_id` (defaults to `eleven_v3`, so the compiler must keep sending `eleven_v4`), `language_code` (ISO 639-1; ISO 639-3 only for ast, yue, ceb, fil), `settings`, `seed` (0–4294967295, "best effort" determinism, not guaranteed: CE-38 stands), `apply_text_normalization` (auto/on/off), `pronunciation_dictionary_locators` (≤3 per request), `previous_text`/`future_text` (≤100 chars) and `previous_request_ids`/`next_request_ids` (≤3) for prosodic continuity across beats, `audio_effects`.
- **Length rule for this route: keep the total characters across `inputs[].text` at or below 2,000 per request** (longer requests can terminate early or fail validation). The 10,000-character figure on the models page is the model limit, not the per-request guidance. The compiler's per-beat segments are far below 2,000; a chapter-length segment is not.
- `output_format` defaults to `mp3_44100_128`; `mp3_44100_192` needs Creator or above; **PCM or WAV at 44.1 kHz needs Pro or above**. The house mastering chain (48 kHz WAV, −16 LUFS, −1 dBTP) therefore decodes MP3 on Free, Starter and Creator plans, or needs Pro for PCM.
- Languages: 90+ for the v4 family, including Hindi (hi), Assamese (as), Bengali (bn), Odia (or), Tamil (ta), Telugu (te), Gujarati (gu), Marathi (mr), Punjabi (pa), Urdu (ur). Assamese remains human-voiced by RD-42 regardless.
- Concurrency by plan (Multilingual v2 column): Free 2, Starter 3, Creator 5, Pro 10, Scale 15. Zero-retention requests (`enable_logging=false`) are enterprise-only.
- Speech to speech: `eleven_multilingual_sts_v2` lists **Hindi** among its 29 languages. This answers the "verify Hindi STS" item in `15_content_engine_v2/subsystems/VOICE_and_PERSONA_REGISTRY.md` §3.4 and 11 [N19]/[N20]: Hindi conversion is documented. It still needs 07/07 processor admission and the native gate before use. `eleven_english_sts_v2` is English-only.
- Pronunciation: the dialogue route accepts up to three pronunciation-dictionary locators per request, so the `lex/` entries can be uploaded as ElevenLabs dictionaries once a locale lexicon is native-approved (05-NP §9.3: provider phonemes only after an acoustic test).

## 3. MCP

- The local package `elevenlabs-mcp` (uvx) is **deprecated** by ElevenLabs in favour of the **hosted MCP server**, which uses OAuth so no API key is copied into the client. Scopes: ElevenAgents read and write, and Text to Speech. It can "generate speech audio from text, returned as a short-lived download link", which is enough for interactive auditions, not for pipeline batches (those use the REST route with the API key).
- Documented URL: `https://api.elevenlabs.io/v1/mcp`. **Claude Code rejects that URL** ("Protected resource https://api.us.elevenlabs.io/v1/mcp does not match expected…"), because the server's OAuth metadata names the US host. Registered instead at user scope:

```bash
claude mcp add --transport http -s user elevenlabs https://api.us.elevenlabs.io/v1/mcp
```

- Status after registration: `! Needs authentication`. Completing OAuth is a founder action: run `/mcp` in an interactive `claude` terminal, choose `elevenlabs`, sign in, pick the workspace and authorise. India data-residency hosts (`api.in.residency.elevenlabs.io`) are separate enterprise workspaces and do not apply to this account.
- Deleting an agent through the MCP is destructive; keep per-call approval on for write tools (Claude's connector tool controls).
- **Second server, the deprecated local package (16 Oct 2026, evening).** Because the hosted server needs an OAuth sign-in and exposes mainly agent tools, the local `elevenlabs-mcp` package was also registered at user scope as `elevenlabs-local`, wrapped so the key never enters any config file: the command is `/bin/zsh -c 'exec /opt/homebrew/bin/uvx elevenlabs-mcp'`, and zsh reads `ELEVENLABS_API_KEY` from `~/.zshenv`; `ELEVENLABS_MCP_BASE_PATH` is the Videos folder (the package reads and writes files only inside it) and `ELEVENLABS_MCP_OUTPUT_MODE=files`. Its first health check timed out at 30 s while `uvx` downloaded the package; with the wheels cached it reports **Connected**. Its tools (per the package README: text to speech, speech to speech, voice clone, voice design, transcription, audio isolation, sound effects) are the ones useful for Path A and Path B experiments from chat; whether its text-to-speech tool can select `eleven_v4` is unverified. ElevenLabs no longer maintains the package, so treat any breakage as a signal to move to the hosted server or the REST route.
- **To make both live:** start a new Claude Code session (MCP servers load at session start), then type `/mcp`, choose `elevenlabs` and sign in with the ElevenLabs account to finish the hosted server's OAuth; `elevenlabs-local` needs no sign-in.

## 4. API key for the pipeline (founder action, never Claude)

1. After onboarding, open `https://elevenlabs.io/app/developers/api-keys` and create a key restricted to Text to Speech, Speech to Speech, Voices (read) and Pronunciation Dictionaries, with a character cap for the audition.
2. Put it in the shell environment only, never in the repository or the ChatGPT export tree:

```bash
echo 'export ELEVENLABS_API_KEY="paste-here"' >> ~/.zshenv
```

3. Verify without printing the key (shows plan and character quota only):

```bash
curl -s https://api.elevenlabs.io/v1/user/subscription -H "xi-api-key: $ELEVENLABS_API_KEY" | python3 -c 'import json,sys;d=json.load(sys.stdin);print(d.get("tier"),d.get("character_count"),"/",d.get("character_limit"))'
```

4. The compiler's emitted requests carry the placeholder `ENV:ELEVENLABS_API_KEY`; the runner substitutes from the environment at send time (05-NP §6). Secret scanning in `12/04_harness_contract/preflight.sh` rejects a literal key in any tracked file.

## 4.1 Audition attempt and the plan decision (16 Oct 2026, evening)

- Three library voices were added to the account for the audition: Devi (`MF4J4IDTRo0AxOO4dpFR`, Hindi, female), Raju (`zT03pEAEi0VHKciJODfn`, Hindi, male), Ziina (`FaqthkZu1EWxXxUFbAfb`, Indian English, female). All three are `free_users_allowed`, rate 1.0, with a 730-day owner notice period (record this in `expiry`/`superseded_by` when a `voice/` entry is written). Library voices do not consume the Free plan's three custom-voice slots.
- **The audition was refused: HTTP 402 `paid_plan_required`, "Free users cannot use library voices via the API".** All twelve requests (two beats × three voices × en and hi) failed identically; nothing was billed. Texts, voice ids and request ids are in `10_pilots_and_examples/narration_outputs/audition_eleven_v4_2026-10-16/manifest.json`, ready to re-run unchanged. The only voices a Free account can synthesise through the API are the 21 premade American, British and Australian English voices, none of which is a candidate.
- API pricing read from `elevenlabs.io/pricing/api` the same day (excludes tax; verify at purchase):

| Plan | Price | v4 characters included | Notes |
|---|---|---|---|
| Free | $0 | 10,000 | no library voices via API; MP3 only; non-commercial |
| Starter | $6/month (first month $1) | 75,000 | unlocks library voices via API; commercial licence (verify) |
| Creator | $22/month (first month $11) | 275,000 | 192 kbps MP3; the "most popular" tier on the page |
| Pro | $99/month | 1,238,000 | PCM/WAV 44.1 kHz output, which the house mastering chain prefers |
| Pay-as-you-go | $0.08 per 1,000 v4 characters ($0.04 for v4 Turbo) | — | Voice Changer (speech-to-speech) $0.12 per minute |
| Startup Grants Program | free for 12 months | 33,000,000 | "Build … into your new product or startup for free with an ElevenLabs Grant"; an edtech startup should apply before paying |

- Cost sense for the pipeline (08 cost models already assume about $0.14 per lesson for Gemini-class TTS): a 600-second lesson is roughly 1,300 to 1,500 words, about 8,000 characters, so about **$0.64 per Path B lesson at v4 list price**, or inside the Starter allowance for about nine lessons a month. The audition needs about 2,100 characters.
- **Decision for the founder (purchase, so not Claude's to make):** Starter is enough to run the audition and the M1 pilot; Pro is only needed when PCM output matters for mastering; the grant removes the question for a year if approved. Until a plan is active, Path B cannot be auditioned and R1 keeps every artefact on Path A.

## 5. What still has to happen before a single v4 line is produced

| Step | Owner | Gate |
|---|---|---|
| Finish onboarding (ElevenCreative) and create the API key | Founder | — |
| Authorise the hosted MCP (`/mcp`) | Founder | — |
| Choose the plan for the audition (PCM output needs Pro; Free gives 10k credits) | Founder | RD-48 style attended spend approval |
| Provider admission record for ElevenLabs v4 and `eleven_multilingual_sts_v2` | Lead | 07/07 §2 |
| Audition: Ohm's-law hook and one explanation beat, three candidate voices, en-IN and hi-IN, Path B, `seed` fixed, requests from `outputs/eleven_v4_requests.json` with an approved `voice_id` | Lead + founder | Golden set `gs/<locale>-<family>` |
| Native-speaker gate per locale | Native reviewers | GL-voice (VOICE §3.7); until it passes, R1 resolves every artefact to Path A |

## 6. Records to update when the audition runs

`15_content_engine_v2/subsystems/VOICE_and_PERSONA_REGISTRY.md` §3.5 row for `eleven_v4` (verified live contract, 2,000-char rule, plan-bound output formats), the `voice/` entry with `provider.model_id = eleven_v4`, the ledger row (voice@version, model id, golden-set hash, audio hashes, reviewers), and `05_narration_system/TTS_PROVIDER_COMPARISON.md` §2.1.
