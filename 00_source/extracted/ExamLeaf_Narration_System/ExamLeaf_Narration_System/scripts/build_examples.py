"""Build original examples and synthetic timing fixtures, never counterfeit narration."""
from pathlib import Path
import json
import platform
import numpy as np
import soundfile as sf
from examleaf_narration.contracts import NarrationPlan
from examleaf_narration.pronunciation import expand,digest,normalized_words
from examleaf_narration.cache import atomic_json,file_hash
from examleaf_narration.timeline import compose,write_vtt
from examleaf_narration.qa import signal_report,master,release_report

ROOT=Path(__file__).resolve().parents[1]

def main():
    terms=[
      ('water_formula','H₂O','H two O','Water formula; prefer water in explanatory prose.'),
      ('two_waters','2H₂O','two water molecules','Coefficient multiplies the whole formula.'),
      ('hydrogen_peroxide','H₂O₂','hydrogen peroxide','Do not replace water with this to balance an equation.'),
      ('hydrogen_molecule','H₂','a hydrogen molecule','Diatomic identity.'),
      ('oxygen_molecule','O₂','an oxygen molecule','Diatomic identity.'),
      ('sodium_ion','Na⁺','sodium ion with one positive charge','Not neutral sodium.'),
      ('sulfate_ion','SO₄²⁻','sulfate ion with two negative charges','Ion charge is not a stoichiometric coefficient.'),
      ('iron_three','Fe³⁺','iron three ion','Formal oxidation state reading; explain positive three charge.'),
      ('moles_per_litre','mol L⁻¹','moles per litre','Not moles per kilogram.'),
      ('moles_per_kilogram','mol kg⁻¹','moles per kilogram','Specify solvent when describing molality.'),
      ('three_point_two','3.2','three point two','Decimal point required.'),
      ('negative_power','10⁻³','ten to the power of negative three','Do not read as ten minus three.'),
      ('microfarad','µF','microfarad','µ prefix; context is capacitance, not coefficient of friction.'),
      ('milliampere','mA','milliampere','Not megaampere.'),
      ('megaampere','MA','megaampere','Not milliampere.'),
      ('speed_unit','m s⁻¹','metres per second','Speed, not acceleration.'),
      ('acceleration_unit','m s⁻²','metres per second squared','Squared denominator.'),
      ('ohm_law','V = IR','voltage equals current multiplied by resistance','Application conditions required.'),
      ('epsilon_zero','ε₀','epsilon nought','Context: vacuum permittivity.'),
      ('mu_zero','µ₀','mu nought','Context: vacuum permeability.'),
      ('tau','τ','tau','Time constant context, not a generic reading for all symbols.'),
      ('delta_phi','ΔΦ','change in magnetic flux','Conceptual expansion, not just Greek letter names.'),
      ('gradient','dy/dx','the derivative of y with respect to x','Do not silently call it a fraction in every context.'),
      ('inverse_sine','sin⁻¹x','the inverse sine of x','Chosen inverse-function meaning; never guess from syntax alone.'),
      ('reciprocal_sine','1/sin x','one divided by sine of x','Not inverse sine.'),
      ('log_ten','log₁₀x','logarithm of x to base ten','Base explicit.'),
      ('natural_log','ln x','natural logarithm of x','Base e.'),
      ('square_root_real','√(x²) = |x|','the square root of x squared equals the absolute value of x','Real x; nonnegative principal square root.'),
      ('integral','∫₀¹ f(x) dx','the integral from zero to one of f of x, with respect to x','Bounds are ordered.'),
      ('degrees','30°','thirty degrees','Not radians.'),
      ('radians','π/6 rad','pi over six radians','Angle unit explicit.'),
      ('five_prime','5′','five prime','DNA/RNA end label, not five feet.'),
      ('three_prime','3′','three prime','DNA/RNA direction label.'),
      ('dna','DNA','D N A','Letters separated.'),
      ('rna','RNA','R N A','Letters separated.'),
      ('atp','ATP','A T P','Letters separated.'),
      ('heterozygous','Aa','one uppercase A allele and one lowercase a allele','Explain genotype, do not pronounce aa ambiguously.'),
      ('diploid','2n','diploid, two n','Use ploidy in context; not DNA mass.'),
      ('mitosis','mitosis','mitosis','Native voice pronunciation audition required.'),
      ('meiosis','meiosis','meiosis','Must stay audibly distinct from mitosis.')]
    lex={'version':'en-reviewed-example-1','review_scope':'Original explicit text mappings checked during this build; no external teacher or acoustic approval.',
         'entries':{k:{'display':d,'meaning':note,'locales':{'en-IN':{'spoken':spoken,'caption':spoken,'editorially_checked':True,'acoustic_approved':False}}} for k,d,spoken,note in terms}}
    atomic_json(ROOT/'configs/pronunciation.json',lex)
    voice={'identity_id':'examleaf-super-teacher','version':'audition-1','brief':'An adult teacher speaking clear Indian English. Warm, precise, energetic without shouting. No fake laughter or added words.',
           'locale':'en-IN','rights_status':'audition-only','rights_record':'Must replace with actual stock-voice licence or written informed performer consent.'}
    plan={'lesson_id':'water_coefficient_demo','academic_edition':'Demonstration only; board alignment not certified',
          'source_claim_manifest':'examples/claims.json','voice':voice,'lexicon_version':lex['version'],'segments':[
      {'segment_id':'question','objective_id':'count_atoms','claim_ids':['water-composition'],
       'text_template':'Two water molecules. How many hydrogen atoms altogether? Count each complete molecule before you answer.',
       'direction':{'mode':'curious','target_wpm':140,'emphasis':['each complete molecule']},
       'pause_after':{'kind':'think','seconds':6,'prompt':'Count hydrogen atoms in two separate water molecules.'},
       'expected_visuals':['two water molecules; label elements, not totals'],'critical_phrases':['Two water molecules','hydrogen'],
       'cues':[{'cue_id':'show_molecules','phrase':'Two water molecules','action':'show','element_id':'molecule-pair'}]},
      {'segment_id':'answer','objective_id':'count_atoms','claim_ids':['water-composition','coefficient-quantity'],
       'text_template':'Four hydrogen atoms. Each water molecule contains two, and we have two complete copies. That is what the coefficient changes: how many molecules, not what a molecule is.',
       'direction':{'mode':'deliberate','target_wpm':130,'emphasis':['Four','not']},'answers_after':'question',
       'pause_after':{'kind':'beat','seconds':.4},'expected_visuals':['highlight four hydrogen atoms, coefficient stays separate from subscript'],
       'critical_phrases':['Four hydrogen atoms','not'],
       'cues':[{'cue_id':'reveal_hydrogen','phrase':'Four hydrogen atoms','action':'reveal-answer','element_id':'hydrogen-count'},
               {'cue_id':'highlight_coefficient','phrase':'coefficient','action':'highlight','element_id':'coefficient'}]},
      {'segment_id':'repair','objective_id':'preserve_identity','claim_ids':['subscript-identity'],
       'text_template':'Changing {{water_formula}} into {{hydrogen_peroxide}} would be a very efficient way to answer a different question. Keep the given formulas fixed. Use coefficients to change the counts.',
       'direction':{'mode':'light','target_wpm':142,'notes':'Dry observation, not a laugh. Return to focused explanation after different question.'},
       'pause_after':{'kind':'beat','seconds':.3},'expected_visuals':['wrong proposed formula clearly labelled, then restore water'],
       'critical_phrases':['fixed','coefficients']},
      {'segment_id':'retry','objective_id':'count_atoms','claim_ids':['water-composition'],
       'text_template':'Your turn again: three water molecules. How many hydrogen atoms, and how many oxygen atoms? Pause here and write both counts.',
       'direction':{'mode':'reassuring','target_wpm':140},
       'pause_after':{'kind':'pause-video','seconds':5,'prompt':'Write hydrogen and oxygen atom totals for three water molecules.'},
       'expected_visuals':['three water molecules with totals hidden'],'critical_phrases':['three water molecules']},
      {'segment_id':'check','objective_id':'count_atoms','claim_ids':['water-composition'],
       'text_template':'Six hydrogen atoms and three oxygen atoms. If those match, check the method too: the number of copies multiplies every atom count in the formula.',
       'direction':{'mode':'focused','target_wpm':140},'answers_after':'retry',
       'expected_visuals':['six hydrogen atoms; three oxygen atoms'],'critical_phrases':['Six hydrogen','three oxygen'],
       'cues':[{'cue_id':'reveal_retry','phrase':'Six hydrogen atoms','action':'reveal-answer','element_id':'retry-totals'}]}]}
    atomic_json(ROOT/'examples/teacher.json',plan)
    boring={**plan,'lesson_id':'water_textbook_demo','segments':[{'segment_id':'textbook','objective_id':'count_atoms','claim_ids':['water-composition','coefficient-quantity'],
         'text_template':'A balanced chemical equation contains equal numbers of atoms of each element on the reactant and product sides. Balancing is performed by changing coefficients, not the subscripts in the specified chemical formulas. Two water molecules contain four hydrogen atoms and two oxygen atoms. Verification requires counting each element on both sides.',
         'direction':{'mode':'steady','target_wpm':140},'critical_phrases':['equal','not','four hydrogen','two oxygen']}]}
    atomic_json(ROOT/'examples/textbook.json',boring)
    atomic_json(ROOT/'examples/claims.json',{'status':'example-source-ledger-not-external-approval','claims':[
       {'id':'water-composition','claim':'A water molecule has two H atoms and one O atom.','source':'https://openstax.org/books/chemistry-2e/pages/4-1-writing-and-balancing-chemical-equations'},
       {'id':'coefficient-quantity','claim':'In the molecular counting representation, a coefficient multiplies all atoms in each specified molecule.','source':'https://openstax.org/books/chemistry-2e/pages/4-1-writing-and-balancing-chemical-equations'},
       {'id':'subscript-identity','claim':'Do not alter supplied correct chemical formulas merely to balance the equation.','source':'https://openstax.org/books/chemistry-2e/pages/4-1-writing-and-balancing-chemical-equations'}]})
    profiles={
       'eleven_v4':{'provider':'elevenlabs','model':'eleven_v4','voice_id':'REPLACE_WITH_APPROVED_VOICE_ID'},
       'eleven_v3':{'provider':'elevenlabs','model':'eleven_v3','voice_id':'REPLACE_WITH_APPROVED_VOICE_ID'},
       'cartesia_snapshot':{'provider':'cartesia','model':'sonic-3.5-2026-05-04','voice_id':'REPLACE_WITH_APPROVED_VOICE_ID','api_version':'REPLACE_WITH_REVIEWED_API_VERSION'},
       'gemini_38':{'provider':'gemini','model':'gemini-3.8-flash-tts','voice_id':'Kore'},
       'openai_snapshot':{'provider':'openai','model':'gpt-4o-mini-tts-2025-12-15','voice_id':'marin'}}
    from examleaf_narration.contracts import ProviderProfile
    from examleaf_narration.compiler import compile_plan
    plan=NarrationPlan.model_validate(plan)
    for name,profile in profiles.items():
        atomic_json(ROOT/f'configs/{name}.json',profile)
        atomic_json(ROOT/f'outputs/{name}_requests.json',compile_plan(plan,ProviderProfile.model_validate(profile),lex))
    atomic_json(ROOT/'configs/narration.schema.json',NarrationPlan.model_json_schema())
    # Signals validate PCM duration, protected holds and event arithmetic, NOT speech quality.
    sample_rate=24000;audio={};align={};fixture_dir=ROOT/'outputs/fixtures';fixture_dir.mkdir(exist_ok=True)
    for i,seg in enumerate(plan.segments):
        text=expand(seg.text_template,lex,plan.voice.locale);tokens=normalized_words(text)
        dur=.4+len(tokens)*.18;t=np.arange(round(dur*sample_rate))/sample_rate
        carrier=.08*np.sin(2*np.pi*(170+i*25)*t)+.03*np.sin(2*np.pi*430*t)
        envelope=np.minimum(1,t/.025)*np.minimum(1,(dur-t)/.025)
        path=fixture_dir/(seg.segment_id+'_signal_NOT_SPEECH.wav');sf.write(path,carrier*envelope,sample_rate,subtype='PCM_16')
        audio[seg.segment_id]=str(path)
        align[seg.segment_id]={'segment_id':seg.segment_id,'audio_sha256':file_hash(path),'transcript_sha256':digest(text),
          'method':'synthetic-fixture','engine_version':'fixture-1-NOT-forced-alignment',
          'words':[{'text':w,'start':.15+j*.18,'end':.15+j*.18+.16} for j,w in enumerate(tokens)]}
    atomic_json(ROOT/'outputs/fixture_alignment.json',align)
    timeline=compose(plan,lex,audio,align,ROOT/'outputs/timing_fixture_NOT_SPEECH.wav')
    atomic_json(ROOT/'outputs/timeline.json',timeline);write_vtt(timeline,ROOT/'outputs/fixture_captions.vtt')
    pauses=[(p['start_sample']/48000,p['end_sample']/48000) for p in timeline['pauses']]
    report=signal_report(ROOT/'outputs/timing_fixture_NOT_SPEECH.wav',pauses)
    atomic_json(ROOT/'outputs/signal_qa.json',report)
    atomic_json(ROOT/'outputs/mastering_qa.json',master(ROOT/'outputs/timing_fixture_NOT_SPEECH.wav',ROOT/'outputs/master_fixture_NOT_SPEECH.wav'))
    atomic_json(ROOT/'outputs/release_blockers.json',release_report(timeline,{},{}))
    atomic_json(ROOT/'outputs/environment.json',{'python':platform.python_version(),'platform':platform.platform(),'numpy':np.__version__,'soundfile':sf.__version__,
         'status':'Offline signal tests; no speech model downloaded or executed locally.'})
    print(f'Built {len(terms)} explicit term mappings, {len(profiles)} request recipes; fixture duration {timeline["duration_seconds"]:.3f}s')

if __name__=='__main__':main()
