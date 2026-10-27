"""Build the original, unrendered ExamLeaf sample script and timing plan."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
rows = [
(0,30,5,'curious', 'The tempting shortcut',
'''Look at this equation. Hydrogen plus oxygen gives water. The oxygen count does not match. So, can we fix it by changing water from H two O to H two O two?
Hold that answer.
That would balance the count here. It would also change the product. Very efficient way to solve a different question. Let's fix the original one.''',
'Show H2 + O2 → H2O. In a separate panel explicitly labelled PROPOSED WRONG FIX, show H2O2. Ask, hold for 5 seconds, then identify changed product. Do not animate an unlabelled change of substance.',
'prediction','Can changing H2O to H2O2 balance the original water equation?','No. It changes the specified product.','Pause occurs after “Hold that answer.”; original equation remains visible.'),
(30,65,2,'steady','Read the symbols before balancing',
'''First, let's make the symbols readable. H stands for hydrogen. O stands for oxygen. In these molecules, the small number tells us how many atoms of that element are present.
H two means two hydrogen atoms in one molecule. O two means two oxygen atoms. Water, H two O, contains two hydrogen atoms and one oxygen atom. No small number beside the O means one.
Those small numbers are called subscripts.''',
'Show labelled molecular models beside H2, O2 and H2O. Use letters as well as colour. Keep subscripts large enough to read.',
'none','','','Hold each molecule while naming its atom counts.'),
(65,100,2,'steady','What balancing preserves',
'''The arrow separates the starting substances, called reactants, from the products formed.
In an ordinary chemical reaction, atoms are rearranged. We don't make extra hydrogen atoms appear, or quietly turn oxygen atoms into hydrogen.
So the equation needs the same number of atoms of each element on both sides. Not the same number of molecules. The same number of each kind of atom.
That's the job. We need careful counting, not a new set of substances.''',
'Build an atom ledger: H left/right, O left/right. State ordinary chemical reaction; show molecule count separately from atom count. Label diagrams as bookkeeping, not a reaction mechanism.',
'none','','','Emphasize “each element”; do not imply conservation of molecule count.'),
(100,145,6,'curious','Coefficient versus subscript',
'''There is a number we can change: the number in front of a formula. That's its coefficient.
Watch two H two O. It means two water molecules, not one strange new molecule. Each copy still has two hydrogen atoms and one oxygen atom.
Together, how many hydrogen atoms? And how many oxygen atoms?
Four hydrogen; two oxygen. The coefficient multiplies the whole formula.
Now compare H two O two. That's one molecule of hydrogen peroxide. Changing a subscript changes the composition. We are balancing water's equation, so water must stay water.''',
'Show 2(H2O) as two intact copies. Ask and hold 6 seconds before atom-count reveal. Show H2O2 in a separate comparison panel, not as permitted editing.',
'prediction','How many H and O atoms are represented by 2H2O?','H=4; O=2.','Pause after the two counting questions. Answer panel hidden during pause.'),
(145,180,2,'light','A short canteen analogy',
'''Think of a canteen recipe card: one sandwich uses two bread slices and one portion of filling. Ordering three sandwiches multiplies every item. It doesn't rewrite what one sandwich contains.
That is the useful comparison: the coefficient changes how many copies; the subscripts describe each molecule.
The comparison stops there. Molecules aren't sandwiches, and real reactions need suitable conditions. This little story helps us read the numbers; it isn't a model of how a reaction happens.''',
'Use one recipe card, then three copies. Immediately return to formula. Display mapping: copies ↔ coefficient; contents of each molecular copy ↔ subscripts. Display explicit analogy limit.',
'none','','','No canteen crowd scene or unrelated sound effect.'),
(180,220,2,'steady','Worked example: match oxygen',
'''Back to hydrogen plus oxygen giving water. Keep the formulas fixed and count.
On the left: two hydrogen atoms and two oxygen atoms. On the right: two hydrogen atoms, but only one oxygen atom.
Let's match oxygen first by putting a two in front of water. We now have two water molecules, so two oxygen atoms on the right.
But don't stop at the first matching row. That coefficient changed the hydrogen count as well. Recount it.''',
'Show H2 + O2 → 2H2O, explicitly marked NOT YET BALANCED. Ledger becomes H 2/4, O 2/2. Reveal O row before H row; keep formula labels unchanged.',
'none','','','Hold the partly balanced equation; no success sound or checkmark for the whole equation.'),
(220,260,6,'curious','Repair the changed hydrogen count',
'''Two water molecules contain four hydrogen atoms. Our left side has only two.
Each hydrogen molecule supplies a pair. How many hydrogen molecules give four hydrogen atoms?
Two. Put a two in front of H two.
Now count both elements: four hydrogen atoms on each side, and two oxygen atoms on each side.
That's why the coefficients are two, one, two. The middle one is normally not written. Nothing was invented, and none of the formulas needed changing.''',
'Ask on H2 + O2 → 2H2O. Hold 6 seconds before revealing 2H2 + O2 → 2H2O. Count all atoms using the same ledger.',
'prediction','How many H2 molecules supply four H atoms?','Two H2 molecules.','Do not show coefficient 2 on H2 until the answer begins.'),
(260,295,2,'steady','Preserve the important distinction',
'''Notice something slightly surprising. We started with three molecules in this written ratio: two hydrogen molecules and one oxygen molecule. We finish with two water molecules.
Three molecules became two, but the atom counts still match. Balancing preserves the number of each type of atom, not the number of molecules.
For your notes, keep one short rule: change coefficients, keep the specified formulas fixed, and check every element. We will use it again without the pictures.''',
'Before/after count summary: molecules 3→2; H atoms 4→4; O atoms 2→2. Stable final molecular models. Not a simultaneous collision mechanism.',
'none','','','Hold the molecule-count contrast; avoid a joke here.'),
(295,335,7,'inviting','Guided completion',
'''Try a shorter repair. Carbon monoxide plus oxygen gives carbon dioxide. The formulas are C O, O two, and C O two.
I've put a two before carbon dioxide. That gives two carbon atoms on the right. What coefficient must go before carbon monoxide?
Work that out, then check oxygen as well. Pause the video if you'd like to write both counting rows.
Don't change the small two inside carbon dioxide. We're choosing how many molecules take part.''',
'Show __CO + __O2 → 2CO2. Answer remains hidden through a 7-second hold. After the hold continue to the next beat. This is symbolic balancing, not a practical demonstration.',
'guided_pause','Complete __CO + __O2 → 2CO2; check C and O.','2CO + O2 → 2CO2.','No new instruction over the writing hold; no countdown.'),
(335,375,2,'reassuring','Check rather than congratulate blindly',
'''Two carbon monoxide molecules give two carbon atoms and two oxygen atoms. One oxygen molecule supplies another two oxygen atoms.
So the left has two carbon atoms and four oxygen atoms. The right has the same counts. Two C O plus O two gives two C O two.
If that matches your work, your counting method is working on a new equation.
If you changed a subscript, restore the original formula first. Then use coefficients to adjust the totals.''',
'Reveal 2CO + O2 → 2CO2 and ledger C 2/2, O 4/4. Keep both feedback routes conditional and visually simple.',
'feedback','','','Praise the verified method conditionally, not an unseen learner response.'),
(375,425,10,'inviting','Independent attempt',
'''Now take away the counting table. Nitrogen and hydrogen form ammonia. The given formulas are N two, H two, and N H three.
Balance the equation using the smallest whole-number coefficients. Start by counting nitrogen, then hydrogen. Write a final count for both elements.
Pause here and give yourself the time you need. This isn't a speed test. Resume when you have a candidate answer, even if you still want to check one part.
Get a candidate answer on the page before you look at the solution.''',
'Show N2 + H2 → NH3 with coefficient blanks, no solved molecular models. Reserve 10 seconds of hold; invite a longer external pause. Reveal begins only in following beat.',
'independent_pause','Balance N2 + H2 → NH3 with smallest whole-number coefficients.','N2 + 3H2 → 2NH3.','No answer visible in caption, thumbnail overlay or background.'),
(425,465,2,'steady','Explain the independent solution',
'''One nitrogen molecule contains two nitrogen atoms, so we need two ammonia molecules on the right. Those two ammonia molecules contain six hydrogen atoms.
Hydrogen arrives in pairs in H two. Three pairs give six.
That gives one, three, two: N two plus three H two gives two N H three.
Check nitrogen: two on each side. Check hydrogen: six on each side.
If you wrote six before H two, you counted hydrogen atoms correctly but forgot that each molecule contains two.''',
'Reveal nitrogen match, then hydrogen match. Finish N2 + 3H2 → 2NH3. Conditional correction shows 6 H atoms ≠ 6 H2 molecules.',
'feedback','','','Keep the correct solution persistent while describing the alternative error.'),
(465,500,5,'light','Balanced versus simplest',
'''One final trap. Two N two plus six H two gives four N H three. Is that balanced?
Yes. But the coefficients all share a factor of two. Divide all three coefficients by two to get the simplest whole-number ratio: one, three, two.
The bigger version isn't chemically unbalanced. It just isn't the requested simplest answer. Bigger numbers do not earn bonus marks for looking busy.
Check the ratio as well as the atom totals.''',
'Show 2N2 + 6H2 → 4NH3. Hold 5 seconds before “Yes”. Label BALANCED, NOT SIMPLEST, then reduce all coefficients together. Humour ends before next task.',
'prediction','Is 2N2 + 6H2 → 4NH3 balanced, and is it simplest?','Balanced yes; simplest no. Reduce all coefficients by two.','No red WRONG stamp on a balanced equation.'),
(500,535,7,'inviting','Retrieve and draw',
'''Close the worked examples. Write one sentence explaining why we change coefficients rather than the given subscripts. Then sketch what two H two O represents. Circles and letters are enough; the diagram does not need to win an art competition.
Pause while you write.
When you return, check two things: did you draw two separate water molecules, and does your sentence explain that changing a subscript changes the composition of the substance?''',
'Hide solved examples. Show recall prompt only; hold 7 seconds after “Pause while you write.” Then reveal two water copies and short check. No decorative art contest imagery.',
'retrieval_pause','Explain coefficient/subscript distinction; sketch 2H2O.','Two water molecules; coefficient scales copies, subscript changes molecular composition.','No new content while learner writes or draws.'),
(535,570,2,'steady','Turn the idea into an exam answer',
'''Now put the idea into an exam-ready sentence: a balanced chemical equation has equal numbers of atoms of each element on its reactant and product sides.
Underneath, write your balanced equation and check its smallest whole-number coefficients. Include state symbols and conditions when the question requires them; this lesson has left those out to focus on balancing.
Remember: a balanced equation checks the atom bookkeeping. By itself, it does not establish the conditions, speed, or steps of a real reaction.''',
'Show concise definition, one checked equation and a separate note about state symbols/conditions. Do not label authored wording an official marking scheme.',
'none','','','Slow on the scientific limitation rather than accelerating to finish.'),
(570,600,1,'reassuring','Evidence-based confidence and next practice',
'''Look back at the first shortcut. You can now explain why changing water's formula answered the wrong question.
Check your own work: can you count the atoms, choose coefficients, and verify the result without the animation? Any unfinished part tells you exactly what to practise next.
Tomorrow, balance a fresh equation before reopening your notes. You don't need to remember my sandwich. You need the counting method.''',
'Close the original H2O2 misconception. Show three self-checks: count, choose, verify. End with one delayed-practice instruction, no autoplay pressure.',
'none','','','Warm but matter-of-fact; no claim that every student mastered the skill.')
]
beats=[]
for n,(start,end,hold,tone,title,spoken,visual,itype,prompt,answer,note) in enumerate(rows,1):
    wc=len(re.findall(r"\b[\w]+(?:['’-][\w]+)*\b",spoken))
    beats.append(dict(id=f'B{n:02}',start_s=start,end_s=end,hold_s=hold,tone=tone,title=title,spoken_text=spoken,visual_direction=visual,interaction=dict(type=itype,prompt=prompt,expected_answer=answer),sync_note=note,word_count=wc,estimated_active_wpm=round(wc/(end-start-hold)*60,1)))
lesson=dict(schema_version='1.0',title='Balancing Chemical Equations: Change the Count, Not the Substance',language='en-IN',target_runtime_s=600,status='UNRENDERED_DRAFT',academic_review='PENDING_HUMAN_REVIEW',timing_status='PLANNED_NOT_AUDIO_MEASURED',audience='Class 10 foundations/revision; Class 12 prerequisite repair, not a complete Class 12 chapter',scope='Simple neutral molecular equations with supplied correct formulas; excludes ionic equations, redox half-reactions, mechanism and practical reaction procedures',sources=['https://openstax.org/books/chemistry-2e/pages/4-1-writing-and-balancing-chemical-equations'],beats=beats)
(ROOT/'examples/sample_lesson.json').write_text(json.dumps(lesson,indent=2,ensure_ascii=False)+'\n')
lines=['# '+lesson['title'],'','## Production status','Original ExamLeaf script. Planned ten-minute cut; not recorded or empirically validated. Timecodes must be conformed to the final voice performance. Learner-controlled pauses add study time. Human academic and full audio/visual review remain required.','',f"**Audience:** {lesson['audience']}",f"**Scope:** {lesson['scope']}",'','**Chemistry reference:** '+lesson['sources'][0],'','Square-bracket directions and visual notes are production metadata, not narration. Chemical formulas stay in the visual layer; the spoken text spells out their reading.','']
for b in beats:
    def tc(s):return f'{s//60:02}:{s%60:02}'
    lines.extend([f"## {tc(b['start_s'])}–{tc(b['end_s'])} | {b['title']}",'',f"**Direction:** {b['tone']}; reserve {b['hold_s']} seconds for the specified hold(s).",'',b['spoken_text'],'',f"**Visual:** {b['visual_direction']}",f"**Synchronization:** {b['sync_note']}",''])
lines += ['## Timing audit','',f"Narration words (approximate tokenizer): {sum(b['word_count'] for b in beats)}.",f"Explicit planned silent/inspection allowance: {sum(b['hold_s'] for b in beats)} seconds.",'The remaining runtime includes speech and natural prosody. Actual audio duration, comprehension and pronunciation override these planning estimates. Do not accelerate dense science to fit a time box.','']
(ROOT/'examples/Complete_Sample_Script.md').write_text('\n'.join(lines))
print('Words:',sum(b['word_count'] for b in beats),'Holds:',sum(b['hold_s'] for b in beats))
for b in beats:print(b['id'], b['word_count'],b['estimated_active_wpm'])
