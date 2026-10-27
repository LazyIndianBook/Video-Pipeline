"""Local atomic outputs, media validation, cache identity and approval gates."""
from __future__ import annotations
import hashlib, importlib.metadata, json, os, platform, shutil, subprocess, tempfile, time
from pathlib import Path
import cairosvg
from .contracts import SceneSpec, Approval
from .science import validate_science
from .visuals import render_svg, FONT

ROOT=Path(__file__).resolve().parents[2]

def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
    return h.hexdigest()

def environment()->dict:
    return {'python':platform.python_version(),'platform':platform.platform(),
      'packages':{n:importlib.metadata.version(n) for n in ['numpy','scipy','sympy','pydantic','CairoSVG','Pillow','rdkit']},
      'ffmpeg':subprocess.check_output(['ffmpeg','-version'],text=True).splitlines()[0],
      'font_sha256':sha256(Path(FONT))}

def cache_key(scene:SceneSpec,aspect:str)->str:
    files=sorted((ROOT/'src/examleaf').glob('*.py'))+[ROOT/'configs/design_tokens.json']
    payload={'scene':scene.model_dump(),'aspect':aspect,'versions':environment(),
      'implementation':{str(f.relative_to(ROOT)):sha256(f) for f in files}}
    return hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()

def probe(path:Path)->dict:
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(path)],text=True))

def media_check(path:Path,scene:SceneSpec,aspect:str)->dict:
    info=probe(path);video=next(s for s in info['streams'] if s['codec_type']=='video')
    w,h=(1280,720) if aspect=='16:9' else (720,1280)
    dur=float(info['format']['duration']);count=int(video.get('nb_frames',0))
    checks={'dimensions':(video['width'],video['height'])==(w,h),'duration':abs(dur-scene.duration_s)<.03,
      'frame_count':count==round(scene.duration_s*scene.fps),'codec':video['codec_name']=='h264','pixel_format':video['pix_fmt']=='yuv420p'}
    return {'passed':all(checks.values()),'checks':checks,'duration_s':dur,'frames':count,'width':w,'height':h,
            'audio_present':any(s['codec_type']=='audio' for s in info['streams'])}

def layout_check(scene:SceneSpec,aspect:str)->dict:
    w,h=(1280,720) if aspect=='16:9' else (720,1280)
    issues=[]
    times={0,scene.duration_s-1/scene.fps}
    for cue in scene.cues:times.update((cue.start_s,min(cue.end_s-1/scene.fps,scene.duration_s-1/scene.fps)))
    for t in sorted(times):
        _,boxes=render_svg(scene,int(round(t*scene.fps)),aspect)
        for b in boxes:
            if b['x']<0 or b['y']<0 or b['x']+b['w']>w+1 or b['y']+b['h']>h+1:
                issues.append({'t':t,'type':'out_of_canvas',**b})
    return {'passed':not issues,'sampled_frames':len(times),'issues':issues,
      'boundary':'Canvas bounds only. Does not prove absence of all overlaps or mobile readability.'}

def stamp(seconds:float)->str:
    ms=round(seconds*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}'

def captions(scene:SceneSpec)->str:
    return 'WEBVTT\n\n'+'\n\n'.join(f'{i}\n{stamp(c.start_s)} --> {stamp(c.end_s)}\n{c.text}' for i,c in enumerate(scene.cues,1))+'\n'

def render(scene_path:Path,outdir:Path,aspect:str='16:9',force:bool=False)->dict:
    scene=SceneSpec.model_validate_json(scene_path.read_text());outdir.mkdir(parents=True,exist_ok=True)
    science=validate_science(scene)
    if not science.passed:raise ValueError(science.model_dump_json())
    layout=layout_check(scene,aspect)
    if not layout['passed']:raise ValueError(json.dumps(layout))
    key=cache_key(scene,aspect);name=f'{scene.id}_{aspect.replace(":","x")}'
    target=outdir/f'{name}.mp4';receipt=outdir/f'{name}.manifest.json'
    if not force and target.exists() and receipt.exists():
        old=json.loads(receipt.read_text())
        if old['cache_key']==key and old['sha256']==sha256(target):
            return {**old,'cache_hit':True,'cache_lookup_only':True}
    start=time.perf_counter();frames=round(scene.duration_s*scene.fps)
    fd,temp=tempfile.mkstemp(suffix='.mp4',prefix='.render-',dir=outdir);os.close(fd)
    temp=Path(temp);log=outdir/f'{name}.ffmpeg.log'
    try:
        with log.open('wb') as errors:
            command=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','image2pipe','-vcodec','png','-framerate',str(scene.fps),'-i','pipe:0',
                '-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-threads','2','-movflags','+faststart',str(temp)]
            proc=subprocess.Popen(command,stdin=subprocess.PIPE,stderr=errors)
            try:
                for i in range(frames):
                    svg,_=render_svg(scene,i,aspect)
                    proc.stdin.write(cairosvg.svg2png(bytestring=svg.encode()))
                proc.stdin.close();ret=proc.wait(timeout=180)
                if ret:raise RuntimeError(f'ffmpeg failed ({ret}); see {log}')
            except BaseException:
                proc.kill();proc.wait();raise
        qa=media_check(temp,scene,aspect)
        if not qa['passed']:raise RuntimeError(json.dumps(qa))
        os.replace(temp,target)
    finally:
        if temp.exists():temp.unlink()
    (outdir/f'{name}.vtt').write_text(captions(scene))
    for label,seconds in [('opening',2),('question',13),('answer',22),('recap',28)]:
        svg,_=render_svg(scene,int(seconds*scene.fps),aspect)
        (outdir/f'{name}_{label}.svg').write_text(svg)
        cairosvg.svg2png(bytestring=svg.encode(),write_to=str(outdir/f'{name}_{label}.png'))
    result={'scene_id':scene.id,'aspect':aspect,'cache_key':key,'cache_hit':False,'sha256':sha256(target),
      'video':target.name,'render_wall_seconds':round(time.perf_counter()-start,3),'frames':frames,'resolution':[qa['width'],qa['height']],
      'render_status':'passed','release_status':'blocked_pending_audio_and_expert_review','audio_status':'intentionally_silent_technical_preview',
      'science':science.model_dump(),'media_qa':qa,'layout_qa':layout,'environment':environment(),
      'invoice_cost_usd':0.0,'billing_note':'No external generation APIs invoked. Local execution was not separately invoiced or cloud-priced.',
      'warnings':['Not a full ten-minute pilot.','Academic correctness not signed off by a teacher.','Voice quality and alignment untested.','No student-learning study performed.']}
    receipt.write_text(json.dumps(result,indent=2))
    return result


def release_check(artifact:Path,receipt:dict,approvals:list[Approval])->list[str]:
    """Offline fail-closed policy check, NOT a production identity/authentication service."""
    reasons=[];digest=sha256(artifact)
    if receipt.get('sha256')!=digest:reasons.append('artifact hash differs from tested receipt')
    if receipt.get('render_status')!='passed':reasons.append('render not passed')
    if receipt.get('audio_status')!='approved_narration':reasons.append('approved narration missing')
    if not receipt.get('science',{}).get('checks') or not all(c['passed'] for c in receipt['science']['checks']):reasons.append('scientific checks missing or failing')
    if not receipt.get('media_qa',{}).get('passed'):reasons.append('media checks missing or failing')
    if not receipt.get('media_qa',{}).get('audio_present'):reasons.append('audio stream missing')
    reviewers=[]
    for role in ('academic','production'):
        valid=[a for a in approvals if a.role==role and a.approved and a.artifact_sha256==digest]
        if not valid:reasons.append(f'{role} approval missing for this hash')
        else:
            reviewers.append(valid[0].reviewer_id)
            if role=='production' and not valid[0].full_video_watched:reasons.append('full-video review missing')
    if len(reviewers)==2 and len(set(reviewers))<2:reasons.append('review roles require different reviewer identities')
    return reasons
