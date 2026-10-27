"""REQUEST compiler. Does not send HTTP or consume provider credits."""
from .contracts import NarrationPlan,ProviderProfile
from .pronunciation import expand,digest,TOKEN
VERSION="0.1.1"
LEGACY_MODELS={"gpt-4o-mini-tts-2025-12-15"}
LANGUAGES={
("elevenlabs","eleven_v4"):{"en-IN","hi-IN","as-IN"},
("elevenlabs","eleven_v3"):{"en-IN","hi-IN","as-IN"},
("elevenlabs","eleven_multilingual_v2"):{"en-IN","hi-IN"},
# Documented snapshot, not advertised as the latest Sonic.
("cartesia","sonic-3.5-2026-05-04"):{"en-IN","hi-IN"},
("gemini","gemini-3.8-flash-tts"):{"en-IN","hi-IN","as-IN"},
("gemini","gemini-3.8-flash-lite-tts"):{"en-IN","hi-IN","as-IN"},
("openai","gpt-4o-mini-tts-2025-12-15"):{"en-IN","hi-IN"}}
STYLE={"curious":"Invite a genuine prediction, curious without theatrical suspense.",
"steady":"Explain conversationally with clear causal emphasis.",
"deliberate":"Measure phrases carefully; distinguish scientific terms and conditions.",
"light":"A small amused smile in the delivery, without added laughter.",
"reassuring":"Warm and matter-of-fact; make correction specific and repairable.",
"focused":"Precise and credible, not promotional."}
ELEVEN_TAG={"curious":"[curious] ","steady":"","deliberate":"[calm] ","light":"","reassuring":"[calm] ","focused":""}

def compile_plan(plan:NarrationPlan,profile:ProviderProfile,lexicon:dict,production=False):
    key=(profile.provider,profile.model)
    if key not in LANGUAGES: raise ValueError("Unreviewed provider/model contract")
    if plan.voice.locale not in LANGUAGES[key]: raise ValueError("Language not admitted by this model contract")
    if production:
        if profile.model in LEGACY_MODELS: raise ValueError("Deprecated model: new production blocked; migrate before 2027-01-06")
        if plan.voice.rights_status not in {"licensed-stock","consented-custom"}: raise ValueError("Production voice rights not cleared")
        if not profile.live_contract_verified: raise ValueError("Live endpoint contract not approved")
        if "REPLACE" in profile.voice_id.upper(): raise ValueError("Replace placeholder voice ID")
    if plan.lexicon_version!=lexicon["version"]: raise ValueError("Lexicon version mismatch")
    requests=[]
    for seg in plan.segments:
        text=expand(seg.text_template,lexicon,plan.voice.locale)
        caption=expand(seg.text_template,lexicon,plan.voice.locale,"caption")
        style=" ".join([plan.voice.brief,STYLE[seg.direction.mode],
         f"Aim for approximately {seg.direction.target_wpm} spoken words per minute; do not add words.",
         "Emphasize: "+"; ".join(seg.direction.emphasis) if seg.direction.emphasis else "",seg.direction.notes]).strip()
        warnings=["Compiled offline; live behavior and pronunciation require separate approval."]
        if len(text)>1800: raise ValueError("Split at a sentence boundary; 1800-character scaffold segment cap")
        headers={"Content-Type":"application/json"}
        if profile.provider=="elevenlabs":
            headers["xi-api-key"]="ENV:ELEVENLABS_API_KEY"
            tagged=text if profile.model=="eleven_multilingual_v2" else ELEVEN_TAG[seg.direction.mode]+text
            if profile.model=="eleven_v4":
                endpoint="https://api.elevenlabs.io/v1/text-to-dialogue"
                payload={"model_id":profile.model,"inputs":[{"text":tagged,"voice_id":profile.voice_id}],"language_code":plan.voice.locale.split('-')[0]}
                # Deliberately no v2-style speed/style controls or SSML.
            else:
                endpoint=f"https://api.elevenlabs.io/v1/text-to-speech/{profile.voice_id}"
                payload={"model_id":profile.model,"text":tagged}
                if profile.model=="eleven_v3":payload["language_code"]=plan.voice.locale.split('-')[0]
            warnings.append("WPM and detailed acting cues are editorial targets, not exact API controls.")
        elif profile.provider=="cartesia":
            if not profile.api_version: raise ValueError("Specify verified Cartesia-Version")
            endpoint="https://api.cartesia.ai/tts/bytes"
            headers.update({"Authorization":"Bearer ENV:CARTESIA_API_KEY","Cartesia-Version":profile.api_version})
            payload={"model_id":profile.model,"transcript":text,"voice":{"mode":"id","id":profile.voice_id},
                "language":plan.voice.locale.split('-')[0],"output_format":{"container":"wav","encoding":"pcm_s16le","sample_rate":48000},
                "generation_config":{"speed":round(max(.6,min(1.5,seg.direction.target_wpm/145)),3),"volume":1}}
            warnings.append("Speed multiplier is a starting heuristic, not a WPM guarantee; beta emotion disabled.")
        elif profile.provider=="gemini":
            endpoint="https://generativelanguage.googleapis.com/v1beta/interactions";headers["x-goog-api-key"]="ENV:GEMINI_API_KEY"
            payload={"model":profile.model,"input":[{"type":"user_input","content":[{"type":"text","text":text,
              "annotations":[{"type":"speech_metadata","style":style}]}]}],"response_format":{"type":"audio"},
              "generation_config":{"speech_config":[{"voice":profile.voice_id}]}}
            warnings.append("Unary 3.8 output is WAV: do not prepend another header. Streaming differs.")
        else:
            warnings.append("LEGACY MIGRATION FIXTURE ONLY: deprecated 2026-10-01; shutdown 2027-01-06; replacement gpt-realtime-2.1-mini requires a separately tested adapter.")
            endpoint="https://api.openai.com/v1/audio/speech";headers["Authorization"]="Bearer ENV:OPENAI_API_KEY"
            payload={"model":profile.model,"voice":profile.voice_id,"input":text,"instructions":style,"response_format":"wav"}
        speech_inputs={"compiler":VERSION,"text":text,"profile":profile.model_dump(),"voice":plan.voice.model_dump(),
                       "direction":seg.direction.model_dump(),"lexicon_digest":digest({k:lexicon["entries"][k] for k in sorted(set(TOKEN.findall(seg.text_template)))})}
        # Deliberately exclude visuals/holds: no paid resynthesis for an editorial timing change.
        requests.append({"segment_id":seg.segment_id,"method":"POST","url":endpoint,"headers_template":headers,
          "body":payload,"canonical_spoken":text,"caption_text":caption,"audio_cache_key":digest(speech_inputs),
          "editorial_style":style,"warnings":warnings})
    return {"status":"offline-request-compilation-not-live-integration","lesson_id":plan.lesson_id,"requests":requests,"network_operations":0}
