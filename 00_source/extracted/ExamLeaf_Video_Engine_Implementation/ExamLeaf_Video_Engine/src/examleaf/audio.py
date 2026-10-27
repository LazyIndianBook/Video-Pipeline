"""Tested local WAV integration; remote providers intentionally have no live credentials."""
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol
import json,math,subprocess,wave

@dataclass(frozen=True)
class AudioAsset:
    path: Path
    duration_s: float
    source: str
    approved: bool=False

class VoiceProvider(Protocol):
    def synthesize(self,text:str,voice_id:str,output:Path)->AudioAsset:...

class UnconfiguredRemoteVoice:
    def synthesize(self,text:str,voice_id:str,output:Path)->AudioAsset:
        raise RuntimeError('Remote TTS is not configured or live-tested. Supply approved audio or validate an authorized provider first.')

def inspect_wav(path:Path)->AudioAsset:
    with wave.open(str(path),'rb') as f:
        if f.getframerate()<=0 or f.getnchannels() not in (1,2):raise ValueError('unsupported WAV')
        duration=f.getnframes()/f.getframerate()
        if duration<=0:raise ValueError('empty WAV')
    return AudioAsset(path=path,duration_s=duration,source='supplied_local_wav')

def verify_alignment(words:list[dict],duration_s:float)->list[str]:
    errors=[];last=0
    for i,w in enumerate(words):
        a=w.get('start_s');b=w.get('end_s')
        if not isinstance(a,(int,float)) or not isinstance(b,(int,float)) or not math.isfinite(a) or not math.isfinite(b):errors.append(f'{i}: invalid numeric timestamp');continue
        if a<last or b<=a or b>duration_s+.01:errors.append(f'{i}: out-of-order or out-of-range')
        if not w.get('text'):errors.append(f'{i}: empty token')
        last=b
    return errors

def mux_supplied_audio(video:Path,audio:Path,output:Path,tolerance_s:float=.05)->dict:
    from .pipeline import probe
    if output.resolve() in (video.resolve(),audio.resolve()):raise ValueError('output must not overwrite input')
    v=probe(video);duration=float(v['format']['duration']);a=inspect_wav(audio)
    if abs(duration-a.duration_s)>tolerance_s:raise ValueError('Audio/video duration mismatch. Conform the timeline; do not silently stretch speech.')
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(video),'-i',str(audio),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(output)],check=True,timeout=120)
    result=probe(output)
    return {'audio_present':any(s['codec_type']=='audio' for s in result['streams']),'status':'mux_test_only_not_voice_quality_approval'}
