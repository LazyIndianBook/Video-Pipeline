from __future__ import annotations
import argparse,json,sys
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from .contracts import SceneSpec,Approval
from .science import validate_science
from .pipeline import render,layout_check,release_check,sha256

def _job(args):return render(*args)

def main():
    p=argparse.ArgumentParser(description='Offline ExamLeaf technical proof. No API calls or publishing.')
    sub=p.add_subparsers(dest='command',required=True)
    v=sub.add_parser('validate');v.add_argument('scene',type=Path)
    r=sub.add_parser('render');r.add_argument('scene',type=Path);r.add_argument('--out',type=Path,default=Path('outputs'));r.add_argument('--aspect',choices=['16:9','9:16'],default='16:9');r.add_argument('--force',action='store_true')
    b=sub.add_parser('batch');b.add_argument('--examples',type=Path,default=Path('examples'));b.add_argument('--out',type=Path,default=Path('outputs'));b.add_argument('--workers',type=int,choices=[1,2,3,4],default=2)
    d=sub.add_parser('extract-pdf');d.add_argument('pdf',type=Path);d.add_argument('--out',required=True,type=Path)
    g=sub.add_parser('release-check');g.add_argument('video',type=Path);g.add_argument('manifest',type=Path);g.add_argument('--approvals',type=Path)
    s=sub.add_parser('schema');s.add_argument('--out',type=Path,default=Path('schemas/scene.schema.json'))
    a=p.parse_args()
    try:
        if a.command=='validate':
            scene=SceneSpec.model_validate_json(a.scene.read_text());science=validate_science(scene)
            result={'science':science.model_dump(),'landscape':layout_check(scene,'16:9'),'vertical':layout_check(scene,'9:16')}
            print(json.dumps(result,indent=2));return 0 if science.passed and result['landscape']['passed'] and result['vertical']['passed'] else 1
        if a.command=='render':print(json.dumps(render(a.scene,a.out,a.aspect,a.force),indent=2))
        elif a.command=='batch':
            jobs=[(f,a.out,aspect,False) for f in sorted(a.examples.glob('*.json')) if not f.stem.endswith('_600s_plan') for aspect in ('16:9','9:16')]
            with ProcessPoolExecutor(max_workers=a.workers) as executor:results=list(executor.map(_job,jobs))
            (a.out/'benchmark.json').write_text(json.dumps(results,indent=2));print(json.dumps([{'id':r['scene_id'],'aspect':r['aspect'],'seconds':r['render_wall_seconds'],'cache_hit':r['cache_hit']} for r in results],indent=2))
        elif a.command=='extract-pdf':
            import pdfplumber
            # Native text only. An empty page is flagged; OCR never runs implicitly.
            with pdfplumber.open(a.pdf) as pdf:
                pages=[{'page_1_based':i,'text':page.extract_text() or '', 'requires_visual_review':True,'empty_text':not bool(page.extract_text())} for i,page in enumerate(pdf.pages,1)]
            result={'source_file':a.pdf.name,'sha256':sha256(a.pdf),'extraction':'native_text_only','pages':pages,'syllabus_mapping_status':'not_performed'}
            a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2))
        elif a.command=='release-check':
            approvals=[Approval.model_validate(v) for v in json.loads(a.approvals.read_text())] if a.approvals else []
            reasons=release_check(a.video,json.loads(a.manifest.read_text()),approvals)
            print(json.dumps({'allowed':not reasons,'blocking_reasons':reasons,'policy_only_not_authenticated_approval_service':True},indent=2));return 1 if reasons else 0
        else:a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(SceneSpec.model_json_schema(),indent=2))
    except Exception as e:
        print(f'{type(e).__name__}: {e}',file=sys.stderr);return 1
    return 0

if __name__=='__main__':raise SystemExit(main())
