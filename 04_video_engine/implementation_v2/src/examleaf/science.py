"""Bounded deterministic science checks. No eval/sympify of model-supplied strings."""
from __future__ import annotations
from collections import Counter
from fractions import Fraction
import math
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from .contracts import SceneSpec, ScienceReport, Check


def rc_state(t: float, resistance: float, capacitance: float, source_v: float) -> dict:
    if resistance<=0 or capacitance<=0 or source_v<=0 or t<0:
        raise ValueError('positive R,C,V and non-negative time required')
    tau=resistance*capacitance
    decay=math.exp(-t/tau)
    return {'t_s':t, 'tau_s':tau, 'voltage_v':source_v*(1-decay),
            'current_a':source_v/resistance*decay, 'charge_c':capacitance*source_v*(1-decay)}


def molecule_counts(smiles: str) -> dict[str,int]:
    # These are a deliberately bounded model inventory, not an arbitrary chemistry evaluator.
    if smiles not in ('[H][H]','O=O','O'):
        raise ValueError('molecule not in approved pilot inventory')
    from rdkit import Chem
    mol=Chem.MolFromSmiles(smiles)
    if mol is None: raise ValueError('invalid molecular representation')
    mol=Chem.AddHs(mol)
    return dict(Counter(atom.GetSymbol() for atom in mol.GetAtoms()))


def reaction_counts(coefficients: list[int]) -> tuple[dict,dict]:
    if len(coefficients)!=3 or any(type(c) is not int or c<=0 for c in coefficients):
        raise ValueError('three positive integer coefficients required')
    left=Counter()
    for smiles,k in zip(('[H][H]','O=O'),coefficients[:2]):
        for atom,n in molecule_counts(smiles).items(): left[atom]+=n*k
    right={atom:n*coefficients[2] for atom,n in molecule_counts('O').items()}
    return dict(left),right


def chain_rule(a: int, b: int, power: int=2):
    if a == 0 or power != 2:
        raise ValueError('pilot supports a nonzero linear inner function squared')
    x=sp.Symbol('x',real=True)
    y=(a*x+b)**power
    d=sp.diff(y,x)
    return x,y,d


def cross_probabilities(parent1: str='Aa',parent2: str='Aa') -> dict[str,Fraction]:
    if any(p not in ('AA','Aa','aa') for p in (parent1,parent2)):
        raise ValueError('single biallelic Mendelian locus only')
    result=Counter()
    for a in parent1:
        for b in parent2: result[''.join(sorted(a+b))]+=1
    return {g:Fraction(n,4) for g,n in sorted(result.items())}


def validate_science(scene: SceneSpec) -> ScienceReport:
    p=scene.parameters; checks=[]
    def add(name,ok,detail): checks.append(Check(name=name,passed=bool(ok),detail=detail))
    try:
        if scene.kind=='rc_charge':
            R=float(p['resistance_ohm']); C=float(p['capacitance_f']); V=float(p['source_v'])
            tau=R*C; initial=rc_state(0,R,C,V); at=rc_state(tau,R,C,V)
            add('initial_condition',initial['voltage_v']==0,'V_C(0)=0 for an initially uncharged capacitor')
            add('one_time_constant',abs(at['voltage_v']/V-(1-math.exp(-1)))<1e-12,'V_C(tau)/V_s=1-exp(-1)')
            t=np.linspace(0,5*tau,101)
            sol=solve_ivp(lambda t,y:[(V-y[0])/(R*C)],(0,5*tau),[0.0],t_eval=t,rtol=1e-10,atol=1e-12)
            expected=V*(1-np.exp(-t/tau))
            error=float(np.max(np.abs(sol.y[0]-expected)))
            add('numerical_ode_crosscheck',sol.success and error<1e-7,f'max absolute voltage error {error:.3g} V')
            add('voltage_law',abs(V-at['current_a']*R-at['voltage_v'])<1e-10,'V_s=IR+V_C')
            add('monotonic_charge',np.all(np.diff(expected)>0),'Charging is monotonic for the ideal model')
        elif scene.kind=='atom_balance':
            coeff=list(p['coefficients']); left,right=reaction_counts(coeff)
            add('element_conservation',left==right,f'reactants={left}; products={right}')
            add('smallest_whole_numbers',math.gcd(*coeff)==1,'coefficients have greatest common divisor 1')
            add('approved_formulas',molecule_counts('O')=={'O':1,'H':2},'RDKit explicit-H atom count verifies H2O composition')
        elif scene.kind=='chain_rule':
            
            if type(p['a']) is not int or type(p['b']) is not int:raise ValueError('integer a,b required; do not truncate')
            a=p['a'];b=p['b'];x,y,d=chain_rule(a,b)
            target=2*a*(a*x+b)
            add('template_parameter_contract',a==3 and b==1,'This visual template is the reviewed (3x+1)^2 fixture; build a new template for another expression')
            add('symbolic_derivative',sp.simplify(d-target)==0,str(d))
            h=1e-5;errors=[]
            for xv in (-1,-.4,0,.25,.5):
                numerical=(float(y.subs(x,xv+h))-float(y.subs(x,xv-h)))/(2*h)
                errors.append(abs(numerical-float(d.subs(x,xv))))
            add('finite_difference_crosscheck',max(errors)<1e-7,f'max finite-difference error {max(errors):.3g}')
            add('real_domain',True,'Polynomial and derivative valid for all real x')
        else:
            probs=cross_probabilities(str(p['parent1']),str(p['parent2']))
            add('probability_normalization',sum(probs.values())==1,str(probs))
            add('genotype_ratio',probs=={'AA':Fraction(1,4),'Aa':Fraction(1,2),'aa':Fraction(1,4)},'Expected 1:2:1 for Aa x Aa')
            add('complete_dominance_phenotype',probs.get('AA',0)+probs.get('Aa',0)==Fraction(3,4),'3/4 dominant phenotype under complete dominance assumption')
            add('no_small_sample_guarantee',any('probabil' in s.lower() for s in scene.assumptions),'Probabilities are not guaranteed counts in four offspring')
    except Exception as exc:
        add('validator_completed',False,f'{type(exc).__name__}: {exc}')
    return ScienceReport(scene_id=scene.id,checks=checks)
