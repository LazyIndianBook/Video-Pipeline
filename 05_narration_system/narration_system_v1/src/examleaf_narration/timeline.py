from __future__ import annotations
from pathlib import Path
from fractions import Fraction
import math
import numpy as np
import soundfile as sf
from scipy.signal import resample_poly
from .contracts import NarrationPlan,Alignment
from .pronunciation import normalized_words,expand,digest
from .cache import file_hash

def frame_at(sample,sample_rate,fps_num=30,fps_den=1):
    x=Fraction(sample*fps_num,sample_rate*fps_den)
    return (2*x.numerator+x.denominator)//(2*x.denominator)

def validate_alignment(record,text,audio_path,duration):
    if record.audio_sha256!=file_hash(audio_path):raise ValueError('Alignment belongs to different audio')
    if record.transcript_sha256!=digest(text):raise ValueError('Alignment belongs to different speech')
    if normalized_words(' '.join(w.text for w in record.words))!=normalized_words(text):
        raise ValueError('Alignment word sequence differs from transcript')
    if not record.words or record.words[-1].end>duration+.001:raise ValueError('Alignment exceeds audio or is empty')

def cue_time(cue,words):
    tokens=[normalized_words(w.text) for w in words]
    if any(len(t)!=1 for t in tokens):raise ValueError('Cue alignment requires one normalized token per word')
    flat=[t[0] for t in tokens];phrase=normalized_words(cue.phrase)
    matches=[i for i in range(len(flat)-len(phrase)+1) if flat[i:i+len(phrase)]==phrase]
    if len(matches)<cue.occurrence:raise ValueError(f'Missing cue occurrence: {cue.cue_id}')
    i=matches[cue.occurrence-1]
    return words[i].start if cue.edge=='start' else words[i+len(phrase)-1].end

def compose(plan:NarrationPlan,lexicon,audio_paths,alignments,output,sample_rate=48000,fps_num=30,fps_den=1):
    pieces=[];clips=[];events=[];pauses=[];captions=[];cursor=0
    for seg in plan.segments:
        p=Path(audio_paths[seg.segment_id]);x,sr=sf.read(p,dtype='float64',always_2d=True)
        if len(x)==0 or not np.all(np.isfinite(x)):raise ValueError('Invalid audio')
        text=expand(seg.text_template,lexicon,plan.voice.locale)
        alignment=Alignment.model_validate(alignments[seg.segment_id])
        if alignment.segment_id!=seg.segment_id:raise ValueError('Alignment segment mismatch')
        validate_alignment(alignment,text,p,len(x)/sr)
        if x.shape[1]!=1:raise ValueError('Narration contract requires mono: explicitly review/downmix first')
        x=x[:,0]
        if sr!=sample_rate:
            g=math.gcd(sr,sample_rate);x=resample_poly(x,sample_rate//g,sr//g)
        start=cursor;end=start+len(x)
        clips.append({'segment_id':seg.segment_id,'start_sample':start,'end_sample':end,'audio_sha256':file_hash(p),'alignment_method':alignment.method})
        for cue in seg.cues:
            sample=start+round(cue_time(cue,alignment.words)*sample_rate)
            events.append({'cue_id':cue.cue_id,'sample':sample,'frame':frame_at(sample,sample_rate,fps_num,fps_den),
                           'action':cue.action,'element_id':cue.element_id,'segment_id':seg.segment_id})
        for i in range(0,len(alignment.words),6):
            ws=alignment.words[i:i+6]
            captions.append({'start_sample':start+round(ws[0].start*sample_rate),
                             'end_sample':start+round(ws[-1].end*sample_rate),'text':' '.join(w.text for w in ws)})
        pieces.append(x);cursor=end;n=round(seg.pause_after.seconds*sample_rate)
        if n:
            pauses.append({'segment_id':seg.segment_id,'start_sample':cursor,'end_sample':cursor+n,'kind':seg.pause_after.kind,'prompt':seg.pause_after.prompt})
            pieces.append(np.zeros(n));cursor+=n
    index={c['segment_id']:c for c in clips}
    for seg in plan.segments:
        if seg.answers_after:
            q=next(p for p in pauses if p['segment_id']==seg.answers_after)
            if index[seg.segment_id]['start_sample']<q['end_sample']:raise ValueError('Premature answer')
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    sf.write(output,np.concatenate(pieces),sample_rate,subtype='PCM_24')
    return {'lesson_id':plan.lesson_id,'sample_rate':sample_rate,'fps_num':fps_num,'fps_den':fps_den,
            'total_samples':cursor,'duration_seconds':cursor/sample_rate,'audio_sha256':file_hash(output),
            'clips':clips,'pauses':pauses,'events':events,'captions':captions,
            'contains_fixture':any(c['alignment_method']=='synthetic-fixture' for c in clips)}

def write_vtt(timeline,path):
    def ts(sample):
        ms=round(sample*1000/timeline['sample_rate']);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
        return f'{h:02d}:{m:02d}:{s:02d}.{ms:03d}'
    lines=['WEBVTT','']
    for i,c in enumerate(timeline['captions'],1):
        lines.extend([str(i),f"{ts(c['start_sample'])} --> {ts(c['end_sample'])}",c['text'],''])
    Path(path).write_text('\n'.join(lines),encoding='utf-8')
