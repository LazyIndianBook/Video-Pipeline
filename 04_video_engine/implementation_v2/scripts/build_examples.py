"""Create original, explicitly bounded technical previews and 600-second pilot plans."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE={'schema_version':'1.0','duration_s':30,'fps':24,'status':'technical_preview'}
source_date='2026-10-13'
items=[
('physics','rc_charge','physics_rc','Charging takes time',{'resistance_ohm':10000,'capacitance_f':.0001,'source_v':10},
 'Connect ideal RC charging to its graph and one-time-constant value.',
 'Class 12 circuit-model technical benchmark; board coverage is not yet approved.',
 ['Ideal linear resistor and capacitor; constant 10 V source.','Capacitor initially uncharged.','Model time is explicitly shown as t/(RC); not a footage timestamp.'],
 'https://openstax.org/books/university-physics-volume-2/pages/10-6-rc-circuits','Section 10.6: RC circuits',
 ['Voltage rises quickly, then approaches the supply more slowly.','Keep R, C and the supply fixed. Watch the same model drive the graph.',
  'Predict: after one RC, is the capacitor fully charged?','No. After one RC, it reaches about 63.2% of the supply.','The curve approaches 10 V; it does not jump there instantly.']),
('chemistry','atom_balance','chemistry_balance','Same atoms. New counts.',{'coefficients':[2,1,2]},
 'Distinguish coefficients from molecular formulas and verify element counts.',
 'Class 10 chemistry / Class 12 prerequisite repair; not a Class 12 chapter pilot.',
 ['Correct starting and product formulas are supplied.','Counts are conserved for each element.','Discrete schematic states are not a reaction mechanism or lab demonstration.'],
 'https://openstax.org/books/chemistry-2e/pages/4-1-writing-and-balancing-chemical-equations','Section 4.1: writing and balancing chemical equations',
 ['Balance the quantities without replacing the substances.','Two water molecules fix oxygen—but change the hydrogen total.',
  'Your turn: how many hydrogen molecules supply four H atoms?','Two H₂ molecules. Now every element matches on both sides.','Change coefficients, not the specified chemical formulas.']),
('mathematics','chain_rule','mathematics_chain','Two layers. One derivative.',{'a':3,'b':1},
 'Differentiate a squared linear expression using the chain rule.',
 'Class 12: differentiation technical benchmark.',
 ['Real x; polynomial function.','The tangent and displayed derivative share the same symbolic model.'],
 'https://openstax.org/books/calculus-volume-1/pages/3-6-the-chain-rule','Section 3.6: the chain rule',
 ['First change the inside. Then square its result.','Let u = 3x + 1. The outside function is y = u².',
  'The outside gives 2u. What factor comes from the inside?','Multiply by 3: dy/dx = 6(3x + 1).','The inside function is not on leave. Account for both layers.']),
('biology','mendel_cross','biology_genetics','A ratio is not a promise.',{'parent1':'Aa','parent2':'Aa'},
 'Distinguish genotype probabilities from guaranteed small-sample counts.',
 'Class 12 inheritance technical benchmark.',
 ['One Mendelian locus with two alleles and equal gamete probabilities.','Random gamete union; complete dominance for phenotype mapping.','Probabilities are not guaranteed counts in four offspring.'],
 'https://openstax.org/books/biology-2e/pages/12-2-characteristics-and-traits','Section 12.2: characteristics and traits',
 ['Each parent can contribute A or a with equal probability.','Combine one allele from each parent; keep genotype and trait distinct.',
  'Under complete dominance, what fraction shows the dominant trait?','Three quarters: AA and Aa show the dominant trait in this model.','A 3:1 expectation does not guarantee three out of exactly four.'])]

for sub,kind,ident,title,params,obj,context,assumptions,uri,locator,lines in items:
 source={'id':ident+'_source','uri':uri,'locator':locator,'rights_status':'open_reference','claim_scope':obj,'retrieved_at':source_date}
 ranges=[(0,6),(6,11),(11,16.5),(16.5,24),(24,30)]
 cues=[{'start_s':a,'end_s':b,'text':line,'role':('question' if i==2 else 'feedback' if i==3 else 'recap' if i==4 else 'explain'),'voice':('curious' if i==2 else 'light' if sub=='mathematics' and i==4 else 'steady'),'answer_visible':i>=3} for i,((a,b),line) in enumerate(zip(ranges,lines))]
 scene={**BASE,'id':ident,'subject':sub,'kind':kind,'title':title,'objective':obj,'class_context':context,'parameters':params,'assumptions':assumptions,'sources':[source],
  'claims':[{'id':ident+'_claim','statement':obj,'source_ids':[source['id']],'assumptions':assumptions,'status':'draft'}],'cues':cues}
 (ROOT/'examples'/f'{ident}.json').write_text(json.dumps(scene,indent=2),encoding='utf-8')
 # Full ten-minute plan, not represented as a rendered or narrated lesson.
 phase_plan=[(25,'curiosity','A concrete misconception and prediction, no sensational statistic.'),(35,'prerequisite','Check essential terms and symbols; link a separate foundation route.'),(60,'intuitive_model','Make the central relation visible with one focus.'),(60,'formal_model','Connect plain language to formal notation and assumptions.'),(90,'worked_example','Explain why each step is selected, preserving the diagram.'),(45,'micro_recap','Hide the key result and ask for reconstruction.'),(75,'guided_example','Fade one step; allow a learner-controlled pause.'),(65,'independent_practice','Remove the worked method; show answer only after the attempt.'),(55,'feedback','Address the precise likely mistake and provide a changed problem.'),(50,'exam_conversion','Return to answer language, units, labels and conditions.'),(40,'confidence_and_spacing','Ask what was done independently; assign one delayed retrieval task.')]
 cursor=0;beats=[]
 for d,k,task in phase_plan:
  beats.append({'start_s':cursor,'duration_s':d,'end_s':cursor+d,'purpose':k,'task':task,'script_status':'requires_authoring_and_review'});cursor+=d
 assert cursor==600
 plan={'id':ident+'_full_pilot','status':'blueprint_only','duration_s':600,'subject':sub,'technical_scene':ident,'objective':obj,'prerequisites':assumptions,
 'board_mapping_status':'pending current syllabus and ExamLeaf source review','beats':beats,'audio_status':'not_generated','mandatory_reviews':['academic','full_render','native_language_when_localized'],
 'success_measures':['zero critical science errors','full timed voice listen','mobile visual review','independent item','delayed retrieval','measured human_minutes','measured generation_and_render_cost']}
 (ROOT/'examples'/f'{ident}_600s_plan.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
print('Created four original 30-second scene specs and four unrendered 600-second pilot plans.')
