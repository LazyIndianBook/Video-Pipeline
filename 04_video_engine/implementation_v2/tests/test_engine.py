import json,math,sqlite3,wave
from pathlib import Path
import pytest
from pydantic import ValidationError
from fractions import Fraction
from examleaf.contracts import SceneSpec,Cue
from examleaf.science import rc_state,reaction_counts,cross_probabilities,chain_rule,validate_science,molecule_counts
from examleaf.pipeline import render_svg,layout_check,cache_key,captions,release_check,sha256
from examleaf.budget import BudgetLedger
from examleaf.audio import verify_alignment,inspect_wav,UnconfiguredRemoteVoice,mux_supplied_audio
ROOT=Path(__file__).resolve().parents[1]

def load(name):return SceneSpec.model_validate_json((ROOT/'examples'/f'{name}.json').read_text())

@pytest.mark.parametrize('name',['physics_rc','chemistry_balance','mathematics_chain','biology_genetics'])
def test_science(name):assert validate_science(load(name)).passed
@pytest.mark.parametrize('name',['physics_rc','chemistry_balance','mathematics_chain','biology_genetics'])
@pytest.mark.parametrize('aspect',['16:9','9:16'])
def test_layout(name,aspect):assert layout_check(load(name),aspect)['passed']
def test_bad_subject():
    d=load('physics_rc').model_dump();d['subject']='biology'
    with pytest.raises(ValidationError):SceneSpec.model_validate(d)
def test_unknown_source():
    d=load('physics_rc').model_dump();d['claims'][0]['source_ids']=['invented']
    with pytest.raises(ValidationError):SceneSpec.model_validate(d)
def test_cue_gap():
    d=load('physics_rc').model_dump();d['cues'][1]['start_s']=7
    with pytest.raises(ValidationError):SceneSpec.model_validate(d)
def test_answer_hidden():
    with pytest.raises(ValidationError):Cue(start_s=0,end_s=2,text='guess',role='question',answer_visible=True)
def test_bad_parameters():
    d=load('physics_rc').model_dump();d['parameters']['resistance_ohm']=-1
    assert not validate_science(SceneSpec.model_validate(d)).passed
def test_bad_balance():
    d=load('chemistry_balance').model_dump();d['parameters']['coefficients']=[1,1,1]
    assert not validate_science(SceneSpec.model_validate(d)).passed
def test_nonsimplest_balance():
    d=load('chemistry_balance').model_dump();d['parameters']['coefficients']=[4,2,4]
    r=validate_science(SceneSpec.model_validate(d));assert not r.passed
    assert next(c for c in r.checks if c.name=='element_conservation').passed
def test_rc_tau():assert rc_state(1,10000,.0001,10)['voltage_v']==pytest.approx(6.321205588)
def test_rc_negative():
    with pytest.raises(ValueError):rc_state(-1,1,1,1)
def test_rdkit_counts():assert molecule_counts('O')=={'O':1,'H':2}
def test_untrusted_molecule_rejected():
    with pytest.raises(ValueError):molecule_counts("__import__('os').system('echo unsafe')")
def test_cross():assert cross_probabilities()=={'AA':Fraction(1,4),'Aa':Fraction(1,2),'aa':Fraction(1,4)}
def test_invalid_allele():
    with pytest.raises(ValueError):cross_probabilities('AB','Aa')
def test_derivative():
    x,y,d=chain_rule(3,1);assert float(d.subs(x,1))==24
def test_renderer_reproducible():
    s=load('physics_rc');assert render_svg(s,500)[0]==render_svg(s,500)[0]
def test_parameter_changes_frame():
    s=load('physics_rc');d=s.model_dump();d['parameters']['source_v']=20
    assert render_svg(s,500)[0]!=render_svg(SceneSpec.model_validate(d),500)[0]
def test_feedback_frame_matches_number():
    svg,_=render_svg(load('physics_rc'),22*24)
    assert '6.32 V' in svg and '63.2%' in svg

def test_vertical_not_crop():
    s=load('physics_rc');a,_=render_svg(s,20);b,_=render_svg(s,20,'9:16')
    assert 'width="1280" height="720"' in a and 'width="720" height="1280"' in b
    assert 'y="619"' in b

def test_caption_file():
    v=captions(load('physics_rc'));assert v.startswith('WEBVTT') and '00:00:11.000 --> 00:00:16.500' in v

def test_idempotent_budget(tmp_path):
    b=BudgetLedger(tmp_path/'b.db',100);assert b.reserve('a',40);assert not b.reserve('a',40)
    with pytest.raises(RuntimeError):b.reserve('b',61)
def test_different_key_cost(tmp_path):
    b=BudgetLedger(tmp_path/'b.db',100);b.reserve('a',40)
    with pytest.raises(ValueError):b.reserve('a',41)
def test_overrun_recorded(tmp_path):
    path=tmp_path/'b.db';b=BudgetLedger(path,100);b.reserve('a',40)
    with pytest.raises(RuntimeError):b.settle('a',110)
    with sqlite3.connect(path) as db:assert db.execute('select cents from jobs').fetchone()[0]==110

def test_alignment():assert verify_alignment([{'start_s':0,'end_s':.5,'text':'charge'}],1)==[]
def test_alignment_reject():assert verify_alignment([{'start_s':.4,'end_s':.2,'text':'bad'}],1)
def test_voice_fail_closed(tmp_path):
    with pytest.raises(RuntimeError):UnconfiguredRemoteVoice().synthesize('test','none',tmp_path/'voice.wav')
def test_local_wav(tmp_path):
    p=tmp_path/'silence.wav'
    with wave.open(str(p),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(48000);f.writeframes(bytes(48000*2))
    assert inspect_wav(p).duration_s==1

def test_no_audio_no_release(tmp_path):
    p=tmp_path/'test.mp4';p.write_bytes(b'fixture')
    reasons=release_check(p,{'sha256':sha256(p),'render_status':'passed'},[])
    assert 'approved narration missing' in reasons and len(reasons)>=5

def test_plans_total_600():
    for f in (ROOT/'examples').glob('*_600s_plan.json'):
        d=json.loads(f.read_text());assert sum(b['duration_s'] for b in d['beats'])==600 and d['status']=='blueprint_only'
