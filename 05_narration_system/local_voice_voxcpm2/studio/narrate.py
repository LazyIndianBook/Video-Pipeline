from pathlib import Path
import sys
import time
import mlx.core as mx
import numpy as np
import soundfile as sf
from mlx_audio.tts.utils import load

mx.set_cache_limit(0)  # added 27 Oct 2026: peak memory ~5 GB instead of ~11 GB on 16 GB, same speed

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
