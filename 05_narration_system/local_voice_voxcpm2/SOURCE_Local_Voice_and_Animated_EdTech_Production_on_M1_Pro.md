Build the first production workflow around **VoxCPM2 through MLX Audio for your own voice, Keynote for animated teaching scenes, and DaVinci Resolve Free for finishing**. Produce English narration at 180–210 words per minute, with 195 WPM as the working target.

Start with one complete 60-second lesson. Approve its voice, scientific accuracy, pacing and visual clarity before expanding to longer lessons or automating more of the process. This plan is for prerecorded videos on your MacBook M1 Pro.

The setup includes a small amount of Terminal work. Once configured, each episode reuses the same narration command and visual templates. Software references checked on 27 October 2026.

# 1 Choose the production stack

| Job | Tool | How you will use it |
| - | - | - |
| Narration | VoxCPM2-4bit through MLX Audio | Turn approved English scripts into speech using your voice reference |
| Voice recording and simple audio edits | Audacity for Apple Silicon | Record and trim the reference; inspect takes and adjust tempo when needed |
| Diagrams and animation | Keynote | Reuse layouts, reveal labels, move objects and export scene movies |
| Final video and sound | DaVinci Resolve Free | Assemble scenes against narration, mix audio, correct captions and export |
| Local caption draft | whisper.cpp with small.en | Transcribe the finished narration into an editable SRT |
| Audio conversion | FFmpeg | Make transcription copies and apply small tempo corrections |

Audacity is useful for initial voice preparation; Resolve can handle the regular final sound mix. Caption generation and conversion are utilities rather than additional editing environments.

VoxCPM2 has Apache 2.0 model licensing, and its original model card explicitly permits commercial use. MLX Audio uses MIT licensing. This is a suitable model-license basis for monetized educational videos using your own recording. There is no hosted speech fee per generated minute. [VoxCPM2 model](https://huggingface.co/openbmb/VoxCPM2) · [MLX Audio](https://pypi.org/project/mlx-audio/)

Begin with the approximately 2.30 GB 4-bit checkpoint. Compare the approximately 3.23 GB 8-bit checkpoint only if the initial voice test warrants it. These are download sizes; runtime memory is higher and shares the M1 Pro’s unified memory with other applications. [MLX model variants](https://github.com/Blaizzy/mlx-audio/blob/main/mlx_audio/tts/models/voxcpm2/README.md)

Keep one narration job active at a time during setup. Close heavy applications while generating the first samples, and avoid simultaneous video rendering. With 16 GB, use the 4-bit baseline first; with 32 GB, it remains a sensible starting point before an 8-bit comparison. Actual speed and acceptable take quality must be established on your Mac.

Use the direct MLX path for VoxCPM2. Voicebox is a useful alternative desktop interface, but its currently documented engine list does not include VoxCPM2. [Voicebox engines](https://github.com/jamiepine/voicebox)

# 2 Set up the Mac once

## Check compatibility

MLX requires Apple Silicon, native ARM Python 3.10 or newer, and macOS 14 or newer. Use a native Terminal and Python installation; an Intel Python running through Rosetta can cause installation failures. [Apple MLX installation](https://ml-explore.github.io/mlx/build/html/install.html)

The Homebrew route below assumes a currently supported Homebrew installation; its current macOS support starts at macOS 15. If you already have a working native Python 3.11, you can skip the Homebrew Python installation. [Homebrew](https://brew.sh/)

Install compatible versions of [Audacity](https://www.audacityteam.org/download/mac/), [Keynote](https://support.apple.com/guide/keynote/welcome/mac) and [DaVinci Resolve Free](https://www.blackmagicdesign.com/products/davinciresolve). The latest Keynote release currently requires macOS 26; an existing compatible version with object animations and movie export is sufficient for this workflow. [Keynote requirements](https://support.apple.com/en-ke/guide/keynote/tan115e144b4/mac)

Check the Mac with these commands:

```bash
sw_vers -productVersion
uname -m
```

The architecture should show arm64. Check memory and free storage in About This Mac and System Settings. Reserve room for model downloads, audio takes and exported movies; 20–30 GB of working space is a useful initial allocation, not a published minimum.

## Install the voice environment

If Homebrew is not installed, use the installer at its official website and follow its PATH instructions. Then:

```bash
brew install python@3.11 ffmpeg

mkdir -p ~/Movies/DikiStudio
cd ~/Movies/DikiStudio
mkdir -p models voice scripts audio visuals projects exports

python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install "mlx-audio==0.6.2" soundfile

python -c "from mlx_audio.tts.models.voxcpm2.voxcpm2 import Model; print('VoxCPM2 backend available')"
```

MLX Audio 0.6.2 is the current published release checked for this plan. The import check confirms that the installed package exposes the required backend before you download a checkpoint. Let MLX Audio resolve its MLX dependency. [Published package](https://pypi.org/project/mlx-audio/) · [Python formula](https://formulae.brew.sh/formula/python@3.11)

Download the model into the project:

```bash
hf download mlx-community/VoxCPM2-4bit --local-dir models/VoxCPM2-4bit
```

This model identifier and the Hugging Face download command are documented by the checkpoint publisher. [Exact checkpoint](https://huggingface.co/mlx-community/VoxCPM2-4bit)

After successful audio generation, save the installed versions:

```bash
python -m pip freeze > requirements.lock.txt
```

Keep the working checkpoint and environment stable while producing a series. If you open a new Terminal later, return to DikiStudio and activate .venv before running the narration command.

## Keep narration local

Installation and the initial model download need internet. The generation script below loads a local model folder and a local voice recording. After one successful generation, use Hugging Face offline mode for repeat runs:

```bash
export HF_HUB_OFFLINE=1
export HF_HUB_DISABLE_TELEMETRY=1
```

These variables control Hugging Face network behavior. Validate the complete setup by generating a new sentence with networking disabled after all needed assets are present. Re-enable downloads deliberately if you later choose another checkpoint. [Offline settings](https://huggingface.co/docs/huggingface_hub/package_reference/environment_variables)

# 3 Record a reusable reference of your voice

Record two or three takes of roughly 45–60 seconds in a quiet, softly furnished room. Read a simple explanation in the delivery you want viewers to hear: engaged, clear, conversational and brisk.

Keep your normal accent. Speak clearly without shouting, whispering or exaggerating every word. Keep a consistent microphone distance; turn away slightly if plosives are strong. Start with the microphone you already have and judge the recording before buying equipment.

Choose a clean **15–20 second excerpt** with continuous speech, natural sentence variation and no mistakes. The upstream practical reference range is 5–30 seconds. Clean reference audio is more useful than an unnecessarily long sample. [VoxCPM reference guidance](https://voxcpm.readthedocs.io/en/latest/usage_guide.html)

In Audacity:

1. Record a single voice without background music.

2. Trim long empty space and exclude coughing, clipping and room noise.

3. Export the selected excerpt as a mono WAV, preferably 48 kHz.

4. Save it as **voice/reference.wav**.

5. Keep the full original recording separately.

Avoid heavy noise removal, reverb or voice effects on the reference. If the room sounds poor, rerecord before trying to repair it extensively.

For the selected reference-only mode, you do not need to train a model or prepare a reference transcript. Reuse the same reference file throughout the series. Keep a second clean reference as a backup, but avoid switching references casually between scenes.

# 4 Generate narration from a text file

Save the following as **narrate.py** in DikiStudio. The current MLX implementation accepts both a voice-reference path and delivery instructions, and returns audio with its actual sample rate. The script keeps a floating-point WAV master for later level adjustment. [MLX implementation](https://github.com/Blaizzy/mlx-audio/blob/main/mlx_audio/tts/models/voxcpm2/voxcpm2.py) · [SoundFile documentation](https://python-soundfile.readthedocs.io/en/latest/)

```python
from pathlib import Path
import sys
import time
import mlx.core as mx
import numpy as np
import soundfile as sf
from mlx_audio.tts.utils import load

if len(sys.argv) != 3:
    raise SystemExit("Usage: python narrate.py script.txt output.wav")

text = Path(sys.argv[1]).read_text(encoding="utf-8").strip()
output = Path(sys.argv[2])
if not text:
    raise SystemExit("The script is empty.")
if output.exists():
    raise SystemExit("Output exists. Choose a new take filename.")

model = load("models/VoxCPM2-4bit")
started = time.perf_counter()
result = next(model.generate(
    text=text,
    ref_audio="voice/reference.wav",
    instruct="Brisk, energetic English teaching. Clear pronunciation, natural emphasis, and short natural pauses.",
    inference_timesteps=10,
    cfg_value=2.0,
))
audio = np.asarray(result.audio.astype(mx.float32))
elapsed = time.perf_counter() - started
if audio.ndim != 1 or audio.size == 0 or not np.isfinite(audio).all():
    raise RuntimeError("Invalid generated audio.")

rate = int(result.sample_rate)
output.parent.mkdir(parents=True, exist_ok=True)
sf.write(str(output), audio, rate, subtype="FLOAT")
seconds = audio.size / rate
words = len(text.split())
print(f"Saved {output}: {seconds:.2f} seconds at {rate} Hz")
print(f"Approximate pace: {60 * words / seconds:.0f} WPM")
print(f"Generation: {elapsed:.1f} seconds, excluding model loading")
```

Create a UTF-8 plain-text file named **scripts/pilot_01.txt** containing 30–60 spoken words. If using TextEdit, choose Format > Make Plain Text. Include narration only; keep scene directions in the storyboard.

Run:

```bash
cd ~/Movies/DikiStudio
source .venv/bin/activate
python narrate.py scripts/pilot_01.txt audio/pilot_01_take1.wav
```

Use a different output name for another take:

```bash
python narrate.py scripts/pilot_01.txt audio/pilot_01_take2.wav
```

The script intentionally refuses to overwrite an existing take. It reports approximate WPM from the supplied text and generated duration. Expand numbers and abbreviations into their spoken form before interpreting that estimate, and listen for omissions or repetitions.

The code was checked against current source and syntax-validated. Model inference and performance have not been tested on your Mac.

Generate a few connected sentences per request, usually 30–60 words, rather than submitting an entire chapter. One request can cover several visual beats. Reuse approved takes and regenerate only faulty sections.

The starting settings are 10 inference steps and CFG 2.0. Keep them unchanged for the first pilot. Inference steps affect synthesis computation; they are not a speech-speed control. The backend has no reliable numeric WPM setting. It also does not automatically split a chapter into production scenes.

Use reference cloning with delivery instructions initially. Upstream Hi-Fi/continuation-style cloning prioritizes reference fidelity and can ignore style instructions. Test that mode later only if voice similarity remains the main problem. [Generation modes](https://voxcpm.readthedocs.io/en/latest/usage_guide.html)

# 5 Approve the voice before building a full lesson

Make a small audition using three passages:

| Passage | What it checks |
| - | - |
| A natural 30–60 word explanation | Your recognizable voice and comfortable rhythm |
| A passage with technical terms, an acronym and a number | Pronunciation and exact wording |
| A connected 80–100 word explanation, generated in sensible groups | Consistency across takes and joined sections |

Compare the output with your original recording. Review with headphones and ordinary speakers.

A usable pilot must preserve meaning exactly, retain a consistent voice, pronounce the subject terms correctly and remain understandable inside the 180–210 WPM range. A missing “not,” a changed number or a duplicated phrase requires correction even if the audio otherwise sounds polished.

Allow two or three takes for a difficult section. If the same problem persists, change one thing at a time:

1. Improve the reference recording if the clone is noisy or unlike you.

2. Rewrite pronunciation in the spoken script or split an awkward sentence.

3. Compare the 8-bit VoxCPM2 checkpoint using the same script and reference.

4. If similarity or clarity still fails, audition Qwen3-TTS Base with an exact reference transcript.

5. Use direct human narration for a deadline or a passage that remains unreliable.

For the 8-bit comparison, download **mlx-community/VoxCPM2-8bit** into **models/VoxCPM2-8bit**, then change the model path in narrate.py. Use the higher-memory option only if it works comfortably on your Mac and the audible result justifies it.

If Terminal setup itself becomes the main obstacle, use Voicebox with a supported cloning engine such as Qwen3-TTS Base. This changes the voice setup; it is not a VoxCPM2 interface in its current documented lineup. Qwen Base handles personal cloning, whereas CustomVoice examples concern preset speakers. [Qwen model modes](https://github.com/Blaizzy/mlx-audio/blob/main/mlx_audio/tts/models/qwen3_tts/README.md) · [Voicebox](https://github.com/jamiepine/voicebox)

# 6 Write the lesson and budget its duration

Start each video with a single learning outcome: “After this video, the learner can explain \_\_\_.” Choose the audience level and the one example that will make the explanation concrete.

For each episode, keep a small source packet: the relevant textbook or curriculum section, links supporting important claims, and notes on any simplifications. Resolve factual uncertainty before generating the narration.

Create a storyboard with four fields: spoken narration, visual action, on-screen text and source or accuracy note. Keep two forms of the script when necessary:

| Display form | Spoken form |
| - | - |
| 5 kg | five kilograms |
| 0.25 | zero point two five |
| DNA | D N A, if that spelling produces the correct result |
| v = d / t | speed equals distance divided by time |

These are pronunciation inputs, not automatic guarantees. Listen to the rendered result. Keep captions and visual labels conventionally spelled even when the TTS input uses a pronunciation workaround.

Use complete connected sentences, familiar vocabulary and one new idea at a time. Define a technical term before using it repeatedly. Preserve qualifications that change the science. Give a new term slightly more room within your chosen pacing range, then move briskly through familiar connective material.

## Word budgets

Use **195 WPM** for planning. Here, narration duration includes natural punctuation pauses but excludes deliberate silent visual holds.

**Word budget = target WPM × narration seconds ÷ 60.**

| Total video | Example silent visual time | Narration time | Approximate words at 195 WPM |
| - | -: | -: | -: |
| 60 seconds | 5 seconds | 55 seconds | 179 |
| 3 minutes | 15 seconds | 165 seconds | 536 |
| 5 minutes | 30 seconds | 270 seconds | 878 |
| 8 minutes | 60 seconds | 420 seconds | 1,365 |

These silence allowances are planning choices. For the first Short, write roughly **175–185 spoken words** and measure the resulting audio. A 180-word narration lasting 55 seconds is about **196 WPM**, leaving five seconds for visual emphasis.

A useful first 60-second structure is:

| Approximate time | Teaching job |
| - | - |
| 0–4 seconds | Pose the question or show the surprising result |
| 4–12 seconds | Give the essential definition |
| 12–32 seconds | Explain the mechanism or reasoning |
| 32–45 seconds | Show one concrete example |
| 45–54 seconds | Correct the likely misunderstanding |
| 54–60 seconds | State the takeaway |

Adjust the sections to the concept. This is a creative template, not a measured breakdown of Fireship’s videos.

## Calibrate the actual pace

Trim excess leading and trailing silence, approve the words, then calculate:

**Actual WPM = spoken word count × 60 ÷ narration duration in seconds.**

If a take is close to the target, use a small pitch-preserving tempo change in Audacity or FFmpeg. For example, moving a measured 180 WPM take to 195 WPM needs a factor of **195 ÷ 180 = 1.083333**:

```bash
ffmpeg -i audio/narration_raw.wav \
  -af "atempo=1.083333" \
  -c:a pcm_s24le audio/narration_paced.wav
```

FFmpeg’s atempo filter uses time stretching. The multiplier above is an example, not a preset for every take. [FFmpeg atempo implementation](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_atempo.c)

Keep routine changes modest, roughly five to ten percent, and listen again. If a take needs substantial acceleration or sounds strained, rewrite or regenerate it. Finish timing changes before creating final captions or carefully synchronized animation.

# 7 Build reusable teaching scenes in Keynote

Create separate project templates for **1080 × 1920 vertical Shorts** and **1920 × 1080 landscape lessons**. Design for the actual orientation; a cropped landscape slide rarely gives a well-composed vertical lesson.

Use a restrained visual system: one readable typeface, a consistent background, two main accent colors and a clear distinction between the object being explained and its labels. Check the result at phone size.

Create six reusable scene types:

| Scene | Reusable elements |
| - | - |
| Question or hook | One large object or question and a brief reveal |
| Definition | Term, simple diagram and one explanatory phrase |
| Process | Objects, connecting arrows and staged steps |
| Comparison | Two aligned examples with matching labels |
| Worked example | A value or equation plus an annotation |
| Recap | The central diagram with one takeaway |

Use object builds and movement to reveal the explanation in the order it is spoken. Apple documents object actions, motion paths and timing controls. [Keynote object animation](https://support.apple.com/lt-lt/guide/keynote/tanf96d92cb6/mac)

For the first Short, aim for about eight to twelve meaningful visual beats. A beat can be a new label, highlighted region or moved object; it does not need a completely new scene. Let dense diagrams remain visible while the narration explains them.

Build exact equations, arrows and scientific labels as editable text and shapes. Keep critical diagrams traceable to the lesson source. Use decorative assets only when they support the explanation.

Once the narration is approved:

1. Mark the words that trigger each reveal.

2. Build the corresponding scene.

3. Export the scene or a short section as a movie.

4. Import it into Resolve above the matching audio.

5. Adjust the hold or re-export that scene if the timing changes.

Keynote supports movie export, selected slide ranges, automatic playback and frame-rate/resolution controls. Use File > Export To > Movie and a consistent 30 fps for this project. [Keynote movie export](https://support.apple.com/guide/keynote/tana0d19882a/mac)

Export visual-only scene movies for the main workflow so you can control narration in Resolve without accidental duplicate audio. Keep the editable Keynote source next to its exported clips.

# 8 Assemble the video and finish the sound

Create a Resolve project with the correct orientation, 30 fps and a 48 kHz audio timeline. Establish these settings before arranging the episode.

Put approved narration on the first audio track. Add markers at key explanations, examples and conclusions. Place the Keynote movie clips above it, then add any separate labels or emphasis overlays.

Use this simple track structure:

| Track | Content |
| - | - |
| Video 1 | Main animated scenes |
| Video 2 | Extra labels or highlights |
| Subtitle track | Corrected captions |
| Audio 1 | Narration |
| Audio 2 | Occasional sound effects |
| Audio 3 | Optional background music |

Keep the voice clear and even. Use short fades at edits, small level adjustments, and gentle EQ or compression only where needed. Resolve’s Fairlight tools include ordinary editing, EQ and dynamics. The free edition is sufficient for this workflow; automatic AI repair is not required. [Resolve](https://www.blackmagicdesign.com/products/davinciresolve) · [Fairlight](https://www.blackmagicdesign.com/products/davinciresolve/fairlight)

The first pilot can use narration alone. When adding music later, make it quiet enough that technical terms remain effortless to hear through a phone speaker.

An optional initial house target is around **−16 LUFS integrated with true peaks at or below −1 dBTP**. This is a proposed mixing target, not a YouTube upload requirement. Listen to the final export rather than relying only on meters.

For a longer lesson, work in coherent sections. Keep each section’s audio takes, scenes and review notes together; revise only the affected section when a fact changes.

# 9 Make captions locally

For a first pilot, manual subtitle creation in Resolve is acceptable. For repeat production, use whisper.cpp to draft captions from the **finished narration-only timeline export**, including its deliberate gaps. This keeps timestamps aligned with the video.

Install the utility:

```bash
brew install whisper.cpp
```

The Homebrew package is **whisper.cpp**, with a dot, and provides the **whisper-cli** executable. It requires a separate model file. [Homebrew formula](https://formulae.brew.sh/formula/whisper.cpp)

Download **ggml-small.en.bin** from the [official model file page](https://huggingface.co/ggerganov/whisper.cpp/blob/main/ggml-small.en.bin) and place it in the models folder. Use the English model for this English-only workflow.

Export narration_final.wav from the beginning of the Resolve timeline, with the same timing as the final video. Make a separate transcription copy:

```bash
ffmpeg -i audio/narration_final.wav \
  -ar 16000 -ac 1 -c:a pcm_s16le audio/captions_input.wav

whisper-cli \
  -m models/ggml-small.en.bin \
  -f audio/captions_input.wav \
  -l en -osrt -otxt -ml 42 -sow \
  -of exports/pilot_captions
```

The 16 kHz file is only for transcription; keep the original editing audio. The CLI supports SRT and text output, character-based segment limits and word-boundary splitting. The 42-character limit is an initial layout aid. [whisper.cpp](https://github.com/ggml-org/whisper.cpp) · [CLI implementation](https://github.com/ggml-org/whisper.cpp/blob/master/examples/cli/cli.cpp)

Import pilot_captions.srt into Resolve. Correct terminology, numbers, punctuation and timing against the approved script and the actual audio. If the spoken audio is wrong, fix the audio too.

Use short readable phrases, normally one or two lines. Position captions away from essential diagram labels. Keep a corrected SRT even when you burn captions into the video.

Resolve supports imported SRT files, subtitle styling, burned-in captions and separate subtitle exports. This plan does not depend on its paid AI transcription features. [Resolve subtitle workflow](https://www.blackmagicdesign.com/products/davinciresolve/edit)

Regenerate or retime captions whenever the narration timing changes.

# 10 Review and export the finished lesson

Review each finished export in three passes.

**Content pass:** Check definitions, numbers, units, equations, arrow directions, omissions and negations against your source packet. Verify that the animation shows what the voice actually says.

**Listening pass:** Play the video without looking at the screen. Check the complete explanation, voice consistency, joins, pronunciation and pacing.

**Phone pass:** Watch the exported file at normal size and volume. Check label readability, caption placement, text contrast and whether the learner has enough time to inspect each diagram.

Recommended starting export settings:

| Setting | Short | Longer lesson |
| - | - | - |
| Frame size | 1080 × 1920 | 1920 × 1080 |
| Frame rate | 30 fps | 30 fps |
| Container and video | MP4 with H.264 | MP4 with H.264 |
| Color | SDR Rec.709 | SDR Rec.709 |
| Video bitrate | Start around 8–12 Mbps | Start around 8–12 Mbps |
| Audio | AAC, 48 kHz | AAC, 48 kHz |
| Captions | Burn in if useful and retain SRT | Retain SRT for selectable captions |

YouTube recommends MP4/H.264, progressive video, 48 kHz audio and preserving the source frame rate. Its reference bitrate for standard-frame-rate 1080p SDR is 8 Mbps; the wider range above is a practical starting choice for these graphics. [YouTube upload guidance](https://support.google.com/youtube/answer/1722171?hl=en)

Upload the pilot as unlisted if you want to check the processed YouTube version on a phone before release. Review it again after processing.

Keep the approved script, source notes, narration takes, Keynote project, Resolve project, final WAV, final MP4 and corrected SRT. Record the reference filename, model version and any tempo changes so that later revisions match the existing episode.

# 11 Roll out the workflow in seven sessions

Treat these as milestones; their duration depends on your familiarity with the software.

| Session | Work | Completion condition |
| - | - | - |
| 1 | Install the voice environment and record references | One successful cloned-voice WAV |
| 2 | Audition technical and natural passages | A chosen voice reference and acceptable delivery |
| 3 | Write the first 60-second lesson and build scene templates | Approved script plus a reusable visual set |
| 4 | Generate final audio, animate and assemble | First complete exported pilot |
| 5 | Make a second Short using the templates | Clear reduction in repeated setup work |
| 6 | Make a 3–5 minute lesson in sections | Stable voice and visual consistency across sections |
| 7 | Review bottlenecks and prepare the next batch | A short list of changes worth automating |

Track time spent on research, script writing, accepted narration, animation and finishing. Also record the number of rejected takes. This will reveal whether the next improvement should target pronunciation, templates or editing.

After several successful videos, automate repeated work in this order:

1. Load the voice model once and generate several approved text chunks in sequence.

2. Save duration and settings alongside each take.

3. Regenerate only changed sections.

4. Run caption generation from the final narration export.

5. Build a small local interface if repeated Terminal use is inconvenient.

6. Add a specialist animation tool only when the lesson requires motion that your templates cannot express efficiently.

A future local interface needs only a script input, reference selection, generate button, audio preview, duration readout and save control. Keep lesson approval and final listening review in the workflow.

Your immediate production target is **one finished 60-second English lesson in your cloned voice at roughly 195 WPM**. Once that works, reuse the same voice reference, script structure, scene templates and export preset for the next lesson.

# 12 Repeatable episode checklist

- [ ] One clear learning outcome and a defined audience level.

- [ ] Important claims checked against the source packet.

- [ ] Spoken script expanded for numbers, units and acronyms.

- [ ] Approved voice reference and model settings reused.

- [ ] Every generated section checked for exact meaning and pronunciation.

- [ ] Narration paced within the chosen 180–210 WPM range.

- [ ] Visuals timed to approved audio.

- [ ] Scientific labels and diagrams checked independently.

- [ ] Captions corrected against the audio and script.

- [ ] Final export checked on headphones and a phone.

- [ ] Editable project files and the final deliverables retained.
