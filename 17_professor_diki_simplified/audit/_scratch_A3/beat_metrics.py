import json, wave, sys, numpy as np, pathlib
R = pathlib.Path(sys.argv[1])
def readwav(p):
    with wave.open(str(p)) as w:
        sr=w.getframerate(); x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float64)/32768
    return x,sr
def db(x): return 20*np.log10(max(np.sqrt(np.mean(x**2)),1e-9))
def f0_track(x,sr,fmin=70,fmax=300):
    hop=int(0.01*sr); win=int(0.04*sr); out=[]
    for i in range(0,len(x)-win,hop):
        f=x[i:i+win]; 
        if db(f)<-35: out.append(np.nan); continue
        f=f-f.mean(); ac=np.correlate(f,f,'full')[win-1:]
        lo=int(sr/fmax); hi=int(sr/fmin)
        if ac[0]<=0: out.append(np.nan); continue
        k=lo+np.argmax(ac[lo:hi]); 
        out.append(sr/k if ac[k]/ac[0]>0.45 else np.nan)
    return np.array(out)
def st(a,b): return 12*np.log2(a/b)
res={}
for subj in ['physics','chemistry','biology']:
    d=R/subj/'opus/narration'; tl=json.load(open(d/'timeline.json'))
    sc={b['id']:b for b in json.load(open(R/subj/'opus/script.json'))['beats']}
    rows=[]
    for b in tl['beats']:
        al=json.load(open(d/'beats'/f"{b['id']}.align.json")); W=al['words']
        x,sr=readwav(d/'beats'/f"{b['id']}.wav")
        dur=len(x)/sr; t0=W[0]['t0']; t1=W[-1]['t1']; span=t1-t0
        gaps=[(W[i]['w'],round(W[i+1]['t0']-W[i]['t1'],2)) for i in range(len(W)-1) if W[i+1]['t0']-W[i]['t1']>=0.25]
        art=span-sum(g for _,g in gaps)
        # energy envelope tail: last sample above -40 dBFS rel
        fr=int(0.02*sr); e=np.array([db(x[i:i+fr]) for i in range(0,len(x)-fr,fr)])
        act=np.where(e>-45)[0]; head=act[0]*0.02 if len(act) else None; tail=dur-(act[-1]+1)*0.02 if len(act) else None
        f0=f0_track(x[int(t0*sr):int(min(t1,dur)*sr)],sr); v=f0[~np.isnan(f0)]
        med=float(np.median(v)) if len(v) else np.nan
        p10,p90=(np.percentile(v,10),np.percentile(v,90)) if len(v) else (np.nan,np.nan)
        # last word pitch slope (question rise?)
        lw=W[-1]; seg=f0_track(x[int(lw['t0']*sr):int(min(lw['t1'],dur)*sr)],sr); sv=seg[~np.isnan(seg)]
        lastslope=st(np.mean(sv[-5:]),np.mean(sv[:5])) if len(sv)>=10 else np.nan
        # per-word level & duration
        wl=[]
        for w in W:
            a,bb=int(w['t0']*sr),int(min(w['t1'],dur)*sr)
            if bb-a>sr*0.03: wl.append((w['w'],round(w['t1']-w['t0'],2),round(db(x[a:bb]),1)))
        rows.append(dict(id=b['id'],slot=b['slot'],tag=sc[b['id']].get('tag'),mode=sc[b['id']].get('mode'),vt_start=b['start'],
            file_s=round(dur,2),head_s=round(head,2),tail_s=round(tail,2),first_word=t0,last_word_end=t1,align_overrun=round(t1-dur,2),
            n=len(W),wpm_file=round(len(W)/dur*60),wpm_speech=round(len(W)/span*60),wpm_artic=round(len(W)/art*60),gaps=gaps,
            rms_db=round(db(x[int(t0*sr):int(min(t1,dur)*sr)]),1),f0_med=round(med,1),f0_range_st=round(st(p90,p10),1) if len(v) else None,
            last_word=lw['w'],last_word_slope_st=round(lastslope,1) if not np.isnan(lastslope) else None, words=wl, unmatched=al.get('unmatched_words')))
    res[subj]=rows
json.dump(res,open(pathlib.Path(sys.argv[2]),'w'),indent=1)
for s,rows in res.items():
    print('==',s)
    for r in rows: print({k:v for k,v in r.items() if k!='words'})
