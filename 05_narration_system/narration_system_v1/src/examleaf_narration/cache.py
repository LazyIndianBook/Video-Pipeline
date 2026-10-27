from pathlib import Path
import hashlib,json,os,tempfile

def file_hash(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def atomic_json(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(dir=path.parent,suffix='.tmp')
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as f:
            json.dump(data,f,ensure_ascii=False,indent=2,allow_nan=False);f.flush();os.fsync(f.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)

def cache_record(audio_path,key,approved=False):
    return {'cache_key':key,'audio_sha256':file_hash(audio_path),'bytes':Path(audio_path).stat().st_size,'approved':approved}

def cache_valid(audio_path,record,key):
    p=Path(audio_path)
    return p.is_file() and record['cache_key']==key and record['audio_sha256']==file_hash(p)

def decide_submission(state):
    if state in {'submitted','running','unknown'}:return 'reconcile-existing-job-never-blindly-resubmit'
    if state=='succeeded':return 'validate-and-cache-existing-output'
    if state=='not-submitted':return 'reserve-budget-then-submit-once'
    if state=='failed':return 'review-failure-and-authorize-bounded-retry'
    raise ValueError('Unknown job state')
