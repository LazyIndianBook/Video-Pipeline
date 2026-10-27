from pathlib import Path
import argparse,json
from .contracts import NarrationPlan,ProviderProfile
from .compiler import compile_plan
from .cache import atomic_json
from .qa import signal_report,loudness_measure,master,release_report

def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def main():
    p=argparse.ArgumentParser(description='Offline-first narration tools: compile never calls providers.')
    s=p.add_subparsers(dest='command',required=True)
    a=s.add_parser('validate');a.add_argument('plan')
    a=s.add_parser('compile');a.add_argument('plan');a.add_argument('--lexicon',required=True);a.add_argument('--profile',required=True);a.add_argument('--out',required=True)
    a=s.add_parser('qa');a.add_argument('audio');a.add_argument('--out',required=True)
    a=s.add_parser('master');a.add_argument('audio');a.add_argument('--out',required=True)
    a=s.add_parser('release-check');a.add_argument('timeline')
    args=p.parse_args()
    if args.command=='validate':
        plan=NarrationPlan.model_validate(load(args.plan));print(f'Valid contract: {plan.lesson_id}; not academic/audio approval')
    elif args.command=='compile':
        result=compile_plan(NarrationPlan.model_validate(load(args.plan)),ProviderProfile.model_validate(load(args.profile)),load(args.lexicon))
        atomic_json(args.out,result);print(f'Compiled {len(result["requests"])} payloads; sent 0 requests')
    elif args.command=='qa':atomic_json(args.out,{'signal':signal_report(args.audio),'loudness':loudness_measure(args.audio)})
    elif args.command=='master':print(json.dumps(master(args.audio,args.out),indent=2))
    else:print(json.dumps(release_report(load(args.timeline),{},{}),indent=2));raise SystemExit(2)
if __name__=='__main__':main()
