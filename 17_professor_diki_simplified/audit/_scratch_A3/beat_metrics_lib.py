import json, wave, sys, numpy as np, pathlib
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
