import copy,json,math,subprocess
from pathlib import Path
import numpy as np
import pytest
import soundfile as sf
from examleaf_narration.contracts import NarrationPlan,ProviderProfile,Pause,Cue,Alignment,AlignedWord
from examleaf_narration.pronunciation import expand,digest,normalized_words
from examleaf_narration.compiler import compile_plan
from examleaf_narration.cache import file_hash,cache_record,cache_valid,decide_submission,atomic_json
from examleaf_narration.timeline import compose,frame_at,cue_time,validate_alignment,write_vtt
from examleaf_narration.qa import transcript_check,signal_report,loudness_measure,master,release_report
ROOT=Path(__file__).resolve().parents[1]

def data(name):return json.loads((ROOT/name).read_text())
@pytest.fixture
def raw():return data('examples/teacher.json')
@pytest.fixture
def lex():return data('configs/pronunciation.json')
@pytest.fixture
def plan(raw):return NarrationPlan.model_validate(raw)
@pytest.fixture
def profile():return ProviderProfile(provider='elevenlabs',model='eleven_v4',voice_id='voice-example')

def test_contract(plan):assert len(plan.segments)==5

def test_extra_field(raw):
    raw['execute']='rm -rf data'
    with pytest.raises(ValueError):NarrationPlan.model_validate(raw)

def test_duplicate_segment(raw):
    raw['segments'].append(copy.deepcopy(raw['segments'][0]))
    with pytest.raises(ValueError):NarrationPlan.model_validate(raw)

def test_forward_answer(raw):
    raw['segments'][0]['answers_after']='retry'
    with pytest.raises(ValueError):NarrationPlan.model_validate(raw)

def test_no_response_window(raw):
    raw['segments'][0]['pause_after']={'kind':'none','seconds':0}
    with pytest.raises(ValueError):NarrationPlan.model_validate(raw)

def test_pause_needs_task():
    with pytest.raises(ValueError):Pause(kind='think',seconds=6)

def test_pause_none_no_time():
    with pytest.raises(ValueError):Pause(kind='none',seconds=2)

@pytest.mark.parametrize('tag',['[excited]','<short pause>','[REVEAL answer]'])
def test_direction_not_spoken(raw,tag):
    raw['segments'][0]['text_template']=tag+' hello'
    with pytest.raises(ValueError):NarrationPlan.model_validate(raw)

def test_alias_water(lex):assert expand('{{two_waters}}',lex,'en-IN')=='two water molecules'

def test_display_separate(lex):assert expand('{{two_waters}}',lex,'en-IN','display')=='2H₂O'

def test_missing_term(lex):
    with pytest.raises(ValueError):expand('{{invented}}',lex,'en-IN')

def test_malformed_term(lex):
    with pytest.raises(ValueError):expand('{{bad token}}',lex,'en-IN')

def test_no_unreviewed_language(lex):
    with pytest.raises(ValueError):expand('{{two_waters}}',lex,'as-IN')

@pytest.mark.parametrize('one,two',[('inverse_sine','reciprocal_sine'),('milliampere','megaampere'),('moles_per_litre','moles_per_kilogram'),('five_prime','three_prime'),('mitosis','meiosis')])
def test_distinct_scientific_readings(lex,one,two):
    assert expand('{{'+one+'}}',lex,'en-IN')!=expand('{{'+two+'}}',lex,'en-IN')

def test_unknown_provider_model(plan,profile,lex):
    profile.model='latest-magic'
    with pytest.raises(ValueError):compile_plan(plan,profile,lex)

def test_block_unverified_production(plan,profile,lex):
    with pytest.raises(ValueError):compile_plan(plan,profile,lex,production=True)

def test_lexicon_version(plan,profile,lex):
    lex['version']='different'
    with pytest.raises(ValueError):compile_plan(plan,profile,lex)

def test_v4_no_legacy_knobs(plan,profile,lex):
    r=compile_plan(plan,profile,lex)['requests'][0]
    assert r['url'].endswith('text-to-dialogue')
    assert 'voice_settings' not in r['body']
    assert 'speed' not in r['body']
    assert 'inputs' in r['body']
    assert r['body']['inputs'][0]['text'].startswith('[curious]')

def test_gemini_metadata(plan,lex):
    p=ProviderProfile(provider='gemini',model='gemini-3.8-flash-tts',voice_id='Kore')
    c=compile_plan(plan,p,lex)['requests'][0]['body']['input'][0]['content'][0]
    assert c['annotations'][0]['type']=='speech_metadata'
    assert c['text']==plan.segments[0].text_template
    assert 'Curious' not in c['text']

def test_openai_metadata(plan,lex):
    p=ProviderProfile(provider='openai',model='gpt-4o-mini-tts-2025-12-15',voice_id='marin')
    r=compile_plan(plan,p,lex)['requests'][0]['body']
    assert 'instructions' in r and 'input' in r and r['response_format']=='wav'

def test_cartesia_version_required(plan,lex):
    p=ProviderProfile(provider='cartesia',model='sonic-3.5-2026-05-04',voice_id='example')
    with pytest.raises(ValueError):compile_plan(plan,p,lex)

def test_multilingual_v2_reject_assamese(raw,lex):
    raw['voice']['locale']='as-IN';p=NarrationPlan.model_validate(raw)
    with pytest.raises(ValueError):compile_plan(p,ProviderProfile(provider='elevenlabs',model='eleven_multilingual_v2',voice_id='example'),lex)

def test_cache_ignores_visual_edit(plan,profile,lex):
    a=compile_plan(plan,profile,lex)['requests'][0]['audio_cache_key']
    plan.segments[0].expected_visuals=['New correct layout']
    plan.segments[0].pause_after.seconds=9
    b=compile_plan(plan,profile,lex)['requests'][0]['audio_cache_key']
    assert a==b

def test_cache_changes_voice(plan,profile,lex):
    a=compile_plan(plan,profile,lex)['requests'][0]['audio_cache_key']
    profile.voice_id='another-voice'
    assert a!=compile_plan(plan,profile,lex)['requests'][0]['audio_cache_key']

def test_cache_changes_speech(plan,profile,lex):
    a=compile_plan(plan,profile,lex)['requests'][0]['audio_cache_key']
    plan.segments[0].text_template+=' Please check.'
    assert a!=compile_plan(plan,profile,lex)['requests'][0]['audio_cache_key']

def test_corrupt_cache(tmp_path):
    p=tmp_path/'audio';p.write_bytes(b'good');r=cache_record(p,'k');assert cache_valid(p,r,'k')
    p.write_bytes(b'bad');assert not cache_valid(p,r,'k')

def test_atomic_manifest(tmp_path):
    p=tmp_path/'a.json';atomic_json(p,{'ok':1});assert json.loads(p.read_text())=={'ok':1}
    assert not list(tmp_path.glob('*.tmp'))

@pytest.mark.parametrize('state',['unknown','submitted','running'])
def test_never_duplicate_unknown_paid_job(state):assert decide_submission(state).startswith('reconcile')

def test_invalid_aligned_interval():
    with pytest.raises(ValueError):AlignedWord(text='a',start=2,end=1)

def test_overlapping_single_voice_alignment():
    with pytest.raises(ValueError):Alignment(segment_id='a',audio_sha256='0'*64,transcript_sha256='0'*64,method='human',engine_version='1',words=[{'text':'a','start':0,'end':1},{'text':'b','start':.5,'end':2}])

def test_second_occurrence_anchor():
    ws=[AlignedWord(text='two',start=.1,end=.2),AlignedWord(text='two',start=.4,end=.5)]
    c=Cue(cue_id='c',phrase='two',occurrence=2,action='show',element_id='x')
    assert cue_time(c,ws)==.4

def test_missing_anchor_fails():
    with pytest.raises(ValueError):cue_time(Cue(cue_id='c',phrase='six',action='show',element_id='x'),[AlignedWord(text='four',start=0,end=1)])

def test_indic_words_stay_whole():
    # Regression: \w-based splitting fragmented Indic words at vowel signs, virama, nukta and anusvara.
    assert normalized_words('विद्युत् धारा।')==['विद्युत्','धारा']
    assert normalized_words('ओम का नियम: V = IR')==['ओम','का','नियम','v','=','ir']
    assert normalized_words('বিদ্যুৎ প্রবাহ')==['বিদ্যুৎ','প্রবাহ']
    assert normalized_words('ক্ষেত্র')==['ক্ষেত্র']
    assert normalized_words('क्‍ष')==['क्ष']  # ZWJ/ZWNJ transparent for comparison
    assert normalized_words('Don’t x-ray 2H₂O')==['don’t','x','-','ray','2h₂o']  # English behaviour unchanged
    assert normalized_words('a_b')==['a','b']  # underscore still separates

def test_cue_time_anchors_hindi_words():
    ws=[AlignedWord(text='ओम',start=.1,end=.3),AlignedWord(text='का',start=.3,end=.4),AlignedWord(text='नियम',start=.4,end=.8)]
    assert cue_time(Cue(cue_id='c',phrase='नियम',action='show',element_id='x'),ws)==.4
    assert cue_time(Cue(cue_id='d',phrase='का नियम',edge='end',action='show',element_id='x'),ws)==.8

def test_transcript_check_hindi_critical_phrase():
    r=transcript_check('विद्युत् धारा बढ़ती है','विद्युत् धारा घटती है',['बढ़ती'])
    assert r['critical_mismatches']==['बढ़ती'] and r['edit_count']==1

def test_frame_mapping():
    assert frame_at(48000,48000)==30
    assert frame_at(600*48000,48000,30000,1001)==17982

def test_negation_loss():
    r=transcript_check('Change coefficients, not subscripts.','Change coefficients, subscripts.',['not'])
    assert r['critical_mismatches']==['not'] and r['edit_count']==1

def test_wrong_atom_count():
    r=transcript_check('Four hydrogen atoms.','Two hydrogen atoms.',['four hydrogen'])
    assert r['critical_mismatches']==['four hydrogen']

def test_zero_wer_not_pronunciation_approval():
    r=transcript_check('mitosis','mitosis')
    assert r['surface_word_error_rate']==0 and 'zero WER does not approve' in r['limitation']

def test_reject_empty_transcript():
    with pytest.raises(ValueError):transcript_check('','test')

def test_fixture_timing_and_answer_protection(plan,lex,tmp_path):
    align=data('outputs/fixture_alignment.json')
    paths={s.segment_id:ROOT/f'outputs/fixtures/{s.segment_id}_signal_NOT_SPEECH.wav' for s in plan.segments}
    t=compose(plan,lex,paths,align,tmp_path/'test.wav')
    a,sr=sf.read(tmp_path/'test.wav');assert len(a)==t['total_samples'] and sr==48000
    assert t['contains_fixture']
    for pause in t['pauses']:
        assert np.all(a[pause['start_sample']:pause['end_sample']]==0)
    q=t['pauses'][0];assert (q['end_sample']-q['start_sample'])/sr==6
    answer=next(c for c in t['clips'] if c['segment_id']=='answer')
    assert answer['start_sample']>=q['end_sample']
    reveal=next(e for e in t['events'] if e['cue_id']=='reveal_hydrogen')
    assert reveal['sample']>=q['end_sample']
    write_vtt(t,tmp_path/'a.vtt');assert (tmp_path/'a.vtt').read_text().startswith('WEBVTT')

def test_alignment_wrong_waveform(plan,lex,tmp_path):
    record=Alignment.model_validate(data('outputs/fixture_alignment.json')['question']);p=tmp_path/'wrong.wav';sf.write(p,np.zeros(48000),48000)
    with pytest.raises(ValueError):validate_alignment(record,plan.segments[0].text_template,p,1)

def test_signal_clipping(tmp_path):
    p=tmp_path/'clip.wav';sf.write(p,np.ones(4800),48000,subtype='FLOAT')
    assert signal_report(p)['clipped_sample_count']==4800

def test_silence_is_planned(tmp_path):
    sr=24000;t=np.arange(sr)/sr;tone=.1*np.sin(2*np.pi*220*t)
    p=tmp_path/'a.wav';sf.write(p,np.concatenate([tone,np.zeros(sr),tone]),sr)
    report=signal_report(p,[(1,2)])
    assert len(report['silences'])==1 and report['silences'][0]['planned']

def test_silent_loudness_rejected(tmp_path):
    p=tmp_path/'silence.wav';sf.write(p,np.zeros(48000),24000)
    with pytest.raises(ValueError):loudness_measure(p)

def test_two_pass_master_real_signal_file(tmp_path):
    src=ROOT/'outputs/timing_fixture_NOT_SPEECH.wav';dst=tmp_path/'master.wav'
    r=master(src,dst);assert r['within_target']
    assert sf.info(dst).samplerate==48000

def test_master_source_protected():
    with pytest.raises(ValueError):master('same.wav','same.wav')

def test_release_fail_closed():
    r=release_report(data('outputs/timeline.json'),{'loudness_pass':True},{})
    assert not r['release_allowed'] and any('Synthetic fixture' in b for b in r['blockers'])

def test_no_fabricated_local_human_approval():
    t={'audio_sha256':'a','contains_fixture':False}
    evidence=dict.fromkeys(['academic_listening','voice_rights','native_language_review','caption_review','sync_review'],True);evidence['audio_sha256']='a'
    assert not release_report(t,{'loudness_pass':True},evidence)['release_allowed']


def test_unused_lexicon_entry_does_not_regenerate(plan,profile,lex):
    a=compile_plan(plan,profile,lex)['requests'][0]['audio_cache_key']
    lex['entries']['never_used']={'display':'x','locales':{'en-IN':{'spoken':'not used','editorially_checked':True}}}
    assert a==compile_plan(plan,profile,lex)['requests'][0]['audio_cache_key']

def test_used_lexicon_entry_does_regenerate(plan,profile,lex):
    a=compile_plan(plan,profile,lex)['requests'][2]['audio_cache_key']
    lex['entries']['water_formula']['locales']['en-IN']['spoken']='water'
    assert a!=compile_plan(plan,profile,lex)['requests'][2]['audio_cache_key']


def test_deprecated_model_blocked_even_with_approval(plan,lex):
    p=ProviderProfile.model_validate(data('configs/openai_snapshot.json'))
    p.live_contract_verified=True
    plan.voice.rights_status='licensed-stock'
    with pytest.raises(ValueError,match='Deprecated model'):
        compile_plan(plan,p,lex,production=True)
    result=compile_plan(plan,p,lex)
    assert '2027-01-06' in ' '.join(result['requests'][0]['warnings'])
