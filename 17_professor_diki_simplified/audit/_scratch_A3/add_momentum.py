import json,sys
p=sys.argv[1]; d=[x for x in json.load(open(p)) if not x['id'].startswith('A3-M')]
SC="script.json beat/slot rules (16_pilot_builds_2026-10-16/PILOT_CONTRACT.md §3; 15_content_engine_v2/subsystems/SCRIPTING_REGISTRY.md)"
M=[
("all","phy 22.4–65.3; chem 21.5–66.5; bio 18.8–60.6",
 "Per-beat curve, written as wpm / tag / silence before→after. Physics: b01 163 curious 0.71→0.91; b02 144 curious 0.91→5.51; b03 153 calm 5.51→0.89; b04 129 thoughtful 0.89→1.02; b05 146 thoughtful 1.02→1.03; b06 144 warm 1.03→0.94; b07 75 calm 0.94→2.19. Chemistry: 152 curious / 156 thoughtful / 143 calm / 146 calm / 140 thoughtful / 143 warm / 74 none. Biology: 204 curious / 166 curious / 160 calm / 127 thoughtful / 164 thoughtful / 147 warm / 77 calm. Flat zone after the think window, 33–38 s in each video: beat RMS within ±0.5 dB (phy −22.7 to −23.4 dBFS) and beat median F0 131–141 Hz (phy). Energy peaks in the hook and never peaks again; every teaching beat sits between two ≥0.6 s silences.",
 "No arc. Energy is front-loaded, flat through the explanation, and lowest at the outro, so the learner is not pulled forward.",
 {"layer":"narration direction + contract","location":"PILOT_CONTRACT §3 four low-arousal tags; one tag per long beat; no energy-curve target anywhere"},
 "The founder's 'not motivating enough'.","high",
 {"what":"Energy-curve target per slot (direction sheet: hook up, reveal up, turn = second peak, recap warm), with short beats so the tag changes every 2–6 s","where":"narration direction sheet, PILOT_CONTRACT §3, qa.py","control":"gate: reveal and turn beats ≥ video median +1 st F0 or +1 dB; no run of >20 s of beats within ±0.5 dB and ±1 st"}),
("all","phy 31.2; chem 34.6; bio 21.4–23.2",
 "Time to first insight (the first new relationship the learner can use, not setup or a question): physics 'twice the voltage, twice the current' at 31.2 s (0.4 A shown at 27.9 s); chemistry 'each element needs the same count on both sides' at 34.6 s, and the first method ('Put a two in front of water') at 36.8 s; biology 'carbon dioxide enters from the air' at 21.4–23.2 s. The physics prediction (11.2–17.1 s) asks for a current before any tool is given (I = V/R is never said, and 0.2 A at 2 V is never shown), so a weak learner can only guess.",
 "The learner waits 21–35 s for something usable, and the 'small effort' is a guess rather than an effort that can succeed.",
 {"layer":"script beat rules","location":SC+": hook → check.predict order without a 'give the tool' beat; no time-to-insight target"},
 "No early win, so curiosity is not converted into competence.","high",
 {"what":"Beat rule: within the first 10 s, give one concrete tool the learner can use (e.g. 'ten ohms: divide the volts by ten'), then ask a prediction that the tool makes solvable","where":"scripting framework, check_script.py","control":"gate: first insight word t0 ≤ 10 s, and the prediction's answer is derivable from on-screen fields"}),
("all","phy 31.17–34.79, 34.79–38.03, 42.87–46.33; chem 25.57–34.53, 39.17–42.69; bio 35.45–39.80, 44.17–47.29",
 "Change events (cue reveals, cue emphases, scene cuts) during the explanation span: physics 18 in 34.9 s (5.2 per 10 s, mean 1.94 s); chemistry 17 in 38.1 s (4.5 per 10 s, mean 2.24 s); biology 18 in 33.5 s (5.4 per 10 s, mean 1.86 s). Gaps over 3 s: physics 3, chemistry 2 (the longest is 8.96 s with no cue while the conservation law is spoken), biology 2. Counted from cue sheets only; animation between cues is the visual auditors' scope.",
 "The average rate meets the 1–3 s rhythm, but the explanation stalls exactly where the abstract statements are spoken.",
 {"layer":"script beat rules + cue authoring","location":"script.json cues (no rule tying each sentence to a visual change); qa.py has no density check"},
 "Attention drops in the hardest sentences.","medium",
 {"what":"Rule: every spoken clause anchors a meaningful visual change (ChangeValue, MapSymbol, TracePath…); a law statement must act on the persistent diagram","where":"scripting framework, cue schema, qa.py","control":"gate: no gap > 3.0 s between change events from the end of the think window to the recap; ≥ 4 events per 10 s"}),
("physics, biology","phy window end 22.50 → 27.89 (0.4 A) and → 46.44–53.64 ('always'); bio 18.87 → 23.24 ('air') → 37.34 / 47.34",
 "Physics: the numeric part of the prediction pays off 5.4 s after the window (good), but the 'is always safe?' part pays off 24–31 s later. Biology: the answer is implied 4.4 s after the window ('from the air'), stated 18.5 s after ('all from carbon dioxide'), and stated again 28.5 s after ('the carbon in wood comes from the air'), with the 40 % detour in between. Chemistry: answered 4.0 s after the window ('Right: only one'), but the hook already half-answered it. No video confirms the learner's prediction ('If you said 0.4 A, you were right').",
 "The payoff is diffuse or delayed, so the learner never gets a clear 'I called it' moment.",
 {"layer":"script beat rules","location":SC+": no payoff-placement rule; the predict prompt may hold two questions"},
 "Lost reward moment, which is the core motivation loop.","high",
 {"what":"One question per prediction; the answer lands ≤ 3 s after the window, as a short standalone line plus an explicit confirmation ('If you said air: right.'), followed by the why","where":"scripting framework, check_script.py","control":"gate: answer word t0 − window end ≤ 3.0 s; one '?' per check.predict"}),
("all","phy 57.40–71.93; chem 59.78–73.20; bio 52.34–67.10",
 "Every close is a recap restatement → spoken disclosure → 2.2 s silence. The optional check.retrieval slot is unused in all three; there is no transfer question (e.g. the external audit's 6 V → 0.6 A), no conditional-confidence line, and no next step (brief C01's CTA 'Try the free lesson' is absent).",
 "The video stops rather than closes; the learner is never shown they can do one on their own.",
 {"layer":"contract slot order","location":"PILOT_CONTRACT §3: check.retrieval optional, outro.disclosure mandatory and spoken; no transfer slot"},
 "No earned confidence ('I can do this one') and no pull towards the next lesson.","high",
 {"what":"Mandatory close: transfer question (2–3 s window from the pause table) → answer + conditional confidence ('If you got 0.6 A, you can use this rule.') → one-line next step → 0.4–0.8 s motif. Disclosure on screen","where":"PILOT_CONTRACT §3, check_script.py, scripting framework","control":"gate: a transfer.check slot exists after the misconception slot; the last spoken line is a next step or a confidence line, not the disclosure"}),
("all","see A3-02, 03, 05, 06, 07",
 "Audio dead time: lead-in, dead inter-beat gaps, think time above the pause-table value, the spoken disclosure and the tail. Physics 0.71+0.91+1.03+0.94+2.51+4.00+2.19 = 12.3 s; chemistry 0.70+0.93+0.70+0.98+4.06+4.00+2.25 = 13.6 s; biology 0.70+0.81+0.92+0.84+3.25+3.92+2.18 = 12.6 s. That is 17–19 % of each video, before counting visual dead time (judges: physics opens on a 3–3.5 s empty board; biology s04 has 2.2 s of empty sky).",
 "About one second in six does nothing.",
 {"layer":"tooling + contract","location":"narrate.py LEAD_IN_S / TAIL_S / gap handling; think_window_s; spoken disclosure"},
 "Momentum loss, and most of the 7–13 s overrun.","high",
 {"what":"The A3-02/03/05/06/07 fixes together","where":"narrate.py, script schema, PILOT_CONTRACT","control":"gate: unlabelled silence ≥ 0.6 s = 0; total dead time ≤ 2.0 s"}),
]
for i,(v,t,ev,pr,rc,ef,sev,fx) in enumerate(M,1):
    d.append({"id":f"A3-M{i}","video":v,"t":t,"evidence":ev,"problem":pr,"root_cause":rc,"effect":ef,"severity":sev,"fix":fx})
json.dump(d,open(p,'w'),ensure_ascii=False,indent=1)
from collections import Counter; print(len(d),Counter(x['severity'] for x in d))
