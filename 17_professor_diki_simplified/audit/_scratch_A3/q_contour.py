import json,sys,wave,numpy as np,pathlib
sys.path.insert(0,str(pathlib.Path(__file__).parent))
from beat_metrics_lib import *

B=pathlib.Path(sys.argv[1])
Q=[('physics','b01',[('Does','current'),('Here','it'),('Now','volts')]),('physics','b05',[('But','safe')]),('chemistry','b01',[('Did','vanish')]),('chemistry','b02',[('Which','short')]),('chemistry','b05',[('Why','two')]),('biology','b01',[('So','from')]),('biology','b02',[('Where','air'),('Pause','predict')])]
for s,b,spans in Q:
    d=B/s/'opus/narration/beats'; W=json.load(open(d/f'{b}.align.json'))['words']; x,sr=readwav(d/f'{b}.wav')
    for a,z in spans:
        i=next(k for k,w in enumerate(W) if w['w'].strip('?.,:')==a); j=next(k for k in range(i,len(W)) if W[k]['w'].strip('?.,:')==z)
        f=f0_track(x[int(W[i]['t0']*sr):int(min(W[j]['t1'],len(x)/sr)*sr)],sr); v=f[~np.isnan(f)]
        n=len(v); 
        if n<20: print(s,b,a,z,'too few voiced'); continue
        body=np.median(v[:int(n*0.7)]); end=np.median(v[-8:]); 
        # last word only
        g=f0_track(x[int(W[j]['t0']*sr):int(min(W[j]['t1'],len(x)/sr)*sr)],sr); gv=g[~np.isnan(g)]
        print(s,b,f'"{a}..{z}"','body',round(body),'end',round(end),'end-vs-body st',round(st(end,body),1),'lastword max-min',(round(gv.max()),round(gv.min())) if len(gv) else None, 'peak st over body', round(st(np.percentile(v,95),body),1))
