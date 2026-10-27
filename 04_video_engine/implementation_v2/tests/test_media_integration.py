"""Integration tests use rendered fixtures; no provider calls or paid credentials."""
import json, subprocess, wave
from pathlib import Path
import pytest
from examleaf.contracts import SceneSpec
from examleaf.pipeline import media_check,render,release_check,sha256
from examleaf.audio import mux_supplied_audio
ROOT=Path(__file__).resolve().parents[1]

@pytest.mark.parametrize('name',['physics_rc','chemistry_balance','mathematics_chain','biology_genetics'])
@pytest.mark.parametrize('aspect',['16:9','9:16'])
def test_actual_mp4(name,aspect):
    file=ROOT/'outputs'/f'{name}_{aspect.replace(":","x")}.mp4'
    if not file.exists():pytest.skip('run batch before media integration')
    scene=SceneSpec.model_validate_json((ROOT/'examples'/f'{name}.json').read_text())
    q=media_check(file,scene,aspect)
    assert q['passed'] and not q['audio_present']

def test_real_cache_hit():
    file=ROOT/'outputs'/'physics_rc_16x9.mp4'
    if not file.exists():pytest.skip('run batch first')
    old=file.stat().st_mtime_ns
    receipt=render(ROOT/'examples'/'physics_rc.json',ROOT/'outputs','16:9')
    assert receipt['cache_hit'] and file.stat().st_mtime_ns==old

def test_actual_release_blocked():
    file=ROOT/'outputs'/'physics_rc_16x9.mp4'
    if not file.exists():pytest.skip('run batch first')
    receipt=json.loads(file.with_suffix('.manifest.json').read_text())
    reasons=release_check(file,receipt,[])
    assert 'approved narration missing' in reasons and 'production approval missing for this hash' in reasons

def test_audio_mux_and_mismatch(tmp_path):
    file=ROOT/'outputs'/'physics_rc_16x9.mp4'
    if not file.exists():pytest.skip('run batch first')
    wav=tmp_path/'synthetic_test_silence.wav'
    with wave.open(str(wav),'wb') as f:
        f.setnchannels(1);f.setsampwidth(2);f.setframerate(48000);f.writeframes(bytes(30*48000*2))
    q=mux_supplied_audio(file,wav,tmp_path/'mux.mp4')
    assert q['audio_present']
    with wave.open(str(wav),'wb') as f:
        f.setnchannels(1);f.setsampwidth(2);f.setframerate(48000);f.writeframes(bytes(48000*2))
    with pytest.raises(ValueError):mux_supplied_audio(file,wav,tmp_path/'bad.mp4')

def test_native_pdf_cli(tmp_path):
    reportlab=pytest.importorskip('reportlab.pdfgen.canvas')
    file=tmp_path/'native.pdf';canvas=reportlab.Canvas(str(file));canvas.drawString(40,750,'ExamLeaf fixture: charge is conserved.');canvas.save()
    out=tmp_path/'extracted.json'
    subprocess.run(['python','-m','examleaf.cli','extract-pdf',str(file),'--out',str(out)],cwd=ROOT,check=True)
    data=json.loads(out.read_text())
    assert 'charge is conserved' in data['pages'][0]['text']
    assert data['sha256']==sha256(file) and data['syllabus_mapping_status']=='not_performed'
