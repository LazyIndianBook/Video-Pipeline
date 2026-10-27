from __future__ import annotations
import math,json,re,subprocess
from pathlib import Path
import numpy as np
import soundfile as sf
from .pronunciation import normalized_words,critical_counts

def transcript_check(expected,observed,critical_phrases=()):
    a,b=normalized_words(expected),normalized_words(observed)
    if not a:raise ValueError('Empty expected transcript')
    prev=list(range(len(b)+1))
    for i,x in enumerate(a,1):
        row=[i]
        for j,y in enumerate(b,1):row.append(min(row[-1]+1,prev[j]+1,prev[j-1]+(x!=y)))
        prev=row
    changed=[p for p in critical_phrases if critical_counts(expected,[p])[p]!=critical_counts(observed,[p])[p]]
    return {'surface_word_error_rate':prev[-1]/len(a),'edit_count':prev[-1],'critical_mismatches':changed,
            'needs_human_check':bool(prev[-1] or changed),
            'limitation':'ASR can normalize mispronunciation into the intended word; zero WER does not approve pronunciation.'}

def signal_report(path,protected_intervals=(),silence_seconds=.6):
    x,sr=sf.read(path,dtype='float64',always_2d=True)
    if x.size==0 or not np.all(np.isfinite(x)):raise ValueError('Empty/non-finite audio')
    peak=float(np.max(np.abs(x)));rms=float(np.sqrt(np.mean(x*x)));dc=float(np.max(np.abs(x.mean(axis=0))))
    frame=max(1,round(.02*sr));regions=[];begin=None
    for a in range(0,len(x),frame):
        quiet=float(np.sqrt(np.mean(x[a:a+frame]**2)))<10**(-50/20)
        if quiet and begin is None:begin=a
        if not quiet and begin is not None:
            if (a-begin)/sr>=silence_seconds:regions.append((begin/sr,a/sr))
            begin=None
    if begin is not None and (len(x)-begin)/sr>=silence_seconds:regions.append((begin/sr,len(x)/sr))
    def planned(a,b):return any(a>=s-.05 and b<=e+.05 for s,e in protected_intervals)
    return {'duration_seconds':len(x)/sr,'sample_rate':sr,'channels':x.shape[1],
            'sample_peak_dbfs':20*math.log10(max(peak,1e-12)),'rms_dbfs':20*math.log10(max(rms,1e-12)),
            'clipped_sample_count':int(np.sum(np.abs(x)>=.9999)),'dc_offset_max':dc,
            'silences':[{'start':a,'end':b,'planned':planned(a,b)} for a,b in regions],
            'not_measured':['naturalness','accent authenticity','STEM pronunciation','true-peak until FFmpeg measurement']}

def loudness_measure(path):
    cmd=['ffmpeg','-hide_banner','-nostdin','-i',str(path),'-af','loudnorm=I=-16:TP=-1:LRA=7:print_format=json','-f','null','-']
    r=subprocess.run(cmd,capture_output=True,text=True,timeout=60,check=True)
    blocks=re.findall(r'\{[^{}]*"input_i"[^{}]*\}',r.stderr,flags=re.S)
    if not blocks:raise ValueError('No FFmpeg loudness measurement')
    data=json.loads(blocks[-1])
    for k in ['input_i','input_tp','input_lra','input_thresh','target_offset']:
        if not math.isfinite(float(data[k])):raise ValueError('Unmeasurable loudness (e.g. silence)')
    return data

def master(source,output):
    source,output=Path(source),Path(output)
    if source.resolve()==output.resolve():raise ValueError('Do not overwrite source audio')
    d=loudness_measure(source)
    filt=(f"loudnorm=I=-16:TP=-1:LRA=7:measured_I={d['input_i']}:measured_TP={d['input_tp']}:"
          f"measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}:linear=true:print_format=json")
    output.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(['ffmpeg','-hide_banner','-nostdin','-y','-i',str(source),'-af',filt,'-ar','48000','-ac','1','-c:a','pcm_s24le',str(output)],
                   capture_output=True,check=True,timeout=60)
    final=loudness_measure(output)
    return {'before':d,'after':final,'target':'-16 LUFS and <= -1 dBTP; ExamLeaf engineering target, not platform law',
            'within_target':abs(float(final['input_i'])+16)<=1 and float(final['input_tp'])<=-.9}

def release_report(timeline,checks,evidence):
    blockers=[]
    if timeline.get('contains_fixture'):blockers.append('Synthetic fixture is not speech and cannot be released')
    for key in ['academic_listening','voice_rights','native_language_review','caption_review','sync_review']:
        if not evidence.get(key):blockers.append(f'Missing {key}')
    if evidence.get('audio_sha256')!=timeline.get('audio_sha256'):blockers.append('Approval/audio hash mismatch')
    if checks.get('critical_mismatches'):blockers.append('Critical transcript mismatch')
    if not checks.get('loudness_pass'):blockers.append('Audio mastering not passed')
    blockers.append('Authenticated approval service not implemented; local booleans are not trusted approvals')
    return {'release_allowed':False,'blockers':blockers}
