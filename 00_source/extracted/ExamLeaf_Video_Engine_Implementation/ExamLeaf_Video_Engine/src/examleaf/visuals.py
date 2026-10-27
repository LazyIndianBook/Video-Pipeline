"""Original SVG scene templates. Animation is a pure function of frame time."""
from __future__ import annotations
import html, json, math, textwrap
from pathlib import Path
from PIL import ImageFont
from .contracts import SceneSpec
from .science import rc_state, chain_rule

FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
ROOT=Path(__file__).resolve().parents[2]
TOKENS=json.loads((ROOT/'configs/design_tokens.json').read_text())

def ease(x):
    x=max(0,min(1,x)); return x*x*(3-2*x)

class Canvas:
    def __init__(self,w,h): self.w=w; self.h=h; self.parts=[]; self.boxes=[]
    def rect(self,x,y,w,h,fill=None,stroke=None,r=0):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill or TOKENS["card"]}" stroke="{stroke or "none"}"/>')
    def line(self,x1,y1,x2,y2,color=None,width=3,dash=None):
        dash=f' stroke-dasharray="{dash}"' if dash else ''
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color or TOKENS["ink"]}" stroke-width="{width}"{dash}/>')
    def circle(self,x,y,r,fill,stroke=None):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke or "none"}" stroke-width="2"/>')
    def path(self,points,color=None,width=4):
        if not points:return
        d='M '+' L '.join(f'{x:.3f},{y:.3f}' for x,y in points)
        self.parts.append(f'<path d="{d}" fill="none" stroke="{color or TOKENS["blue"]}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')
    def text(self,x,y,text,size=30,color=None,weight=400,anchor='start',max_width=None,lineheight=1.28,essential=True):
        # Measurement matches the proof renderer's local font; no user-supplied SVG/HTML accepted.
        font=ImageFont.truetype(FONT,size)
        rows=[]
        for para in str(text).split('\n'):
            line=''
            for word in para.split():
                candidate=f'{line} {word}'.strip()
                if max_width and font.getlength(candidate)>max_width and line:
                    rows.append(line);line=word
                else:line=candidate
            rows.append(line)
        for i,row in enumerate(rows):
            yy=y+i*size*lineheight; ww=float(font.getlength(row))
            xx=x-ww/2 if anchor=='middle' else x-ww if anchor=='end' else x
            self.boxes.append({'text':row,'x':xx,'y':yy-size,'w':ww,'h':size*1.2,'size':size,'essential':essential})
            self.parts.append(f'<text x="{x}" y="{yy}" font-family="DejaVu Sans" font-size="{size}" font-weight="{weight}" fill="{color or TOKENS["ink"]}" text-anchor="{anchor}">{html.escape(row)}</text>')
        return len(rows)*size*lineheight
    def group(self,x,y,scale,callback):
        self.parts.append(f'<g transform="translate({x},{y}) scale({scale})">')
        # Only internal diagram primitives use groups; text bboxes are emitted in final coords elsewhere.
        callback();self.parts.append('</g>')
    def svg(self):
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}">'+''.join(self.parts)+'</svg>'


def chart(c,x,y,w,h,points,xmax,ymax,xlabel,ylabel,marker=None):
    l=x+64;b=y+h-65;r=x+w-26;top=y+48
    for f in (.25,.5,.75,1):c.line(l,b-(b-top)*f,r,b-(b-top)*f,TOKENS['line'],1)
    c.line(l,b,r,b,width=2);c.line(l,b,l,top,width=2)
    c.text(l,y+30,ylabel,23,color=TOKENS['muted'])
    c.text((l+r)/2,y+h-12,xlabel,23,color=TOKENS['muted'],anchor='middle')
    c.text(l-14,b+5,'0',20,anchor='end')
    coords=[(l+(r-l)*xx/xmax,b-(b-top)*yy/ymax) for xx,yy in points]
    c.path(coords,width=5)
    if marker:
        xx,yy=marker;px=l+(r-l)*xx/xmax;py=b-(b-top)*yy/ymax
        c.line(px,b,px,py,TOKENS['teal'],2,'6 6');c.circle(px,py,8,TOKENS['teal'])
    return l,b,r,top


def render_svg(scene:SceneSpec,frame:int,aspect:str='16:9') -> tuple[str,list[dict]]:
    if aspect not in ('16:9','9:16'):raise ValueError('unsupported aspect')
    if not 0<=frame<round(scene.duration_s*scene.fps):raise ValueError('frame outside timeline')
    t=frame/scene.fps;phase=t/scene.duration_s
    vertical=aspect=='9:16';w,h=(720,1280) if vertical else (1280,720)
    c=Canvas(w,h);c.rect(0,0,w,h,TOKENS['background'])
    c.rect(0,0,w,8,TOKENS['teal'])
    margin=42 if vertical else 54
    c.text(margin,53,'EXAMLEAF',24,TOKENS['teal'],700)
    c.text(w-margin,53,scene.subject.upper(),16,TOKENS['muted'],anchor='end',essential=False)
    c.text(margin,113,scene.title,42 if vertical else 46,weight=700,max_width=w-2*margin)
    if vertical:
        A=(36,220,610,375);B=(36,619,610,355);caption_y=1040;caption_w=568
    else:
        A=(54,164,700,383);B=(782,164,444,383);caption_y=598;caption_w=1172
    for x,y,ww,hh in (A,B):c.rect(x,y,ww,hh,r=18)
    ax,ay,aw,ah=A;bx,by,bw,bh=B
    p=scene.parameters
    is_question=any(q.start_s<=t<q.end_s and q.role=='question' for q in scene.cues)
    reveal=phase>=.55
    if scene.kind=='rc_charge':
        R=float(p['resistance_ohm']);C=float(p['capacitance_f']);V=float(p['source_v']);tau=R*C
        physical_t=(min(phase/.42,1) if phase<.42 else 1 if phase<.8 else 1+(phase-.8)/.2*4)*tau
        state=rc_state(physical_t,R,C,V)
        points=[(i/80*5,V*(1-math.exp(-i/80*5))) for i in range(81) if i/80*5<=physical_t/tau]
        l,bb,r,top=chart(c,*A,points,5,V,'Time / RC','Capacitor voltage (V)',(physical_t/tau,state['voltage_v']))
        c.text(r,bb+27,'5',20,anchor='end')
        c.text(l+(r-l)/5,bb+27,'1',20,anchor='middle')
        c.text(l-12,top+7,f'{V:g}',20,anchor='end')
        c.text(bx+25,by+48,'IDEAL RC CIRCUIT',22,TOKENS['muted'],700)
        c.text(bx+25,by+102,'V/V₀ = 1 − exp(−t/RC)',26 if not vertical else 34)
        c.text(bx+25,by+153,f'R = {R/1000:g} kΩ   C = {C*1e6:g} μF',22 if not vertical else 28)
        c.text(bx+25,by+198,f'RC = {tau:g} second',30,TOKENS['blue'],700)
        value='Predict first' if is_question else f'{state["voltage_v"]:.2f} V'
        c.text(bx+25,by+261,value,47,TOKENS['teal'],700)
        c.text(bx+25,by+307,f'Supply: {V:g} V • initially uncharged',19 if not vertical else 25,max_width=bw-50)
    elif scene.kind=='atom_balance':
        c.text(ax+24,ay+45,'COUNT ATOMS, NOT MOLECULES',23,TOKENS['muted'],700,max_width=aw-48)
        coeff=[1,1,1] if phase<.25 else [1,1,2] if phase<.55 else [2,1,2]
        cx=ax+aw/2
        c.text(cx,ay+115,f'{coeff[0] if coeff[0]>1 else ""}H₂ + O₂ → {coeff[2] if coeff[2]>1 else ""}H₂O',48,anchor='middle',weight=700)
        # Discrete molecular states, not an asserted reaction mechanism or orbital model.
        for i in range(coeff[0]):
            yy=ay+202+i*77;xx=ax+76
            c.line(xx,yy,xx+48,yy,TOKENS['blue'],4)
            for dx in (0,48):c.circle(xx+dx,yy,21,TOKENS['blue']);c.text(xx+dx,yy+8,'H',22,'#FFFFFF',anchor='middle')
        xx=ax+aw*.46;yy=ay+236
        c.line(xx,yy-4,xx+46,yy-4,TOKENS['error'],3);c.line(xx,yy+4,xx+46,yy+4,TOKENS['error'],3)
        for dx in (0,46):c.circle(xx+dx,yy,22,TOKENS['error']);c.text(xx+dx,yy+8,'O',22,'#FFFFFF',anchor='middle')
        for i in range(coeff[2]):
            xx=ax+aw*.82;yy=ay+200+i*82
            for dx in (-37,37):c.line(xx,yy,xx+dx,yy+25,TOKENS['muted'],3);c.circle(xx+dx,yy+25,17,TOKENS['blue']);c.text(xx+dx,yy+32,'H',18,'#FFFFFF',anchor='middle')
            c.circle(xx,yy,21,TOKENS['error']);c.text(xx,yy+8,'O',22,'#FFFFFF',anchor='middle')
        c.text(bx+24,by+48,'ATOM LEDGER',23,TOKENS['muted'],700)
        
        for xx,txt in [(bx+24,'Element'),(bx+bw*.54,'Left'),(bx+bw*.78,'Right')]:c.text(xx,by+105,txt,24 if not vertical else 30)
        for j,(atom,l,r) in enumerate([('H',2*coeff[0],2*coeff[2]),('O',2,coeff[2])]):
            color=TOKENS['teal'] if l==r else TOKENS['amber']
            
            for xx,txt in [(bx+25,atom),(bx+bw*.54,str(l)),(bx+bw*.78,str(r))]:c.text(xx,by+167+j*60,txt,32,color,700)
        c.text(bx+24,by+291,'Balanced' if coeff==[2,1,2] else 'Recount every element',30 if vertical else 25,TOKENS['teal'] if reveal else TOKENS['amber'],700,max_width=bw-48)
        c.text(bx+24,by+332,'Schematic counts, not a mechanism',18 if not vertical else 24,TOKENS['muted'],max_width=bw-48)
    elif scene.kind=='chain_rule':
        a=int(p['a']);b=int(p['b']);xv=-.9+min(phase/.4,1)*1.05 if phase<.4 else .15 if phase<.68 else .15+(phase-.68)*.6
        # Plot coordinates transform x∈[-1,1] to a nonnegative chart axis.
        points=[(i/100*2,(a*(-1+i/100*2)+b)**2) for i in range(101)]
        l,bb,r,top=chart(c,*A,points,2,16,'x : −1 to +1','y = (3x + 1)²',(xv+1,(a*xv+b)**2))
        c.text(l,bb+27,'−1',20);c.text((l+r)/2,bb+27,'0',20,anchor='middle');c.text(r,bb+27,'+1',20,anchor='end')
        c.text(l-12,top+7,'16',20,anchor='end')
        slope=2*a*(a*xv+b);yv=(a*xv+b)**2
        ts=[]
        for k in range(61):
            xx=xv-.3+k*.01; yy=yv+slope*(xx-xv)
            if -1<=xx<=1 and 0<=yy<=16:ts.append((l+(r-l)*(xx+1)/2,bb-(bb-top)*yy/16))
        c.path(ts,TOKENS['teal'],4)
        c.text(bx+24,by+48,'OUTSIDE × INSIDE',23,TOKENS['muted'],700)
        c.text(bx+24,by+107,'u = 3x + 1',36,TOKENS['blue'])
        c.text(bx+24,by+161,'y = u²',36)
        c.text(bx+24,by+219,'dy/dx = 2u × ?',32,TOKENS['amber']) if not reveal else c.text(bx+24,by+219,'dy/dx = 2u × 3',32,TOKENS['teal'])
        if reveal:c.text(bx+24,by+282,'= 6(3x + 1)',34,TOKENS['teal'],700)
        c.text(bx+24,by+331,'Both layers change with x.',21 if not vertical else 28,TOKENS['muted'],max_width=bw-48)
    else:
        c.text(ax+24,ay+42,'Aa × Aa : ONE MENDELIAN LOCUS',22,TOKENS['muted'],700,max_width=aw-48)
        sz=110 if vertical else 117;gx=ax+aw/2-sz*.6;gy=ay+120
        c.text(gx+sz*.5,gy-18,'A',32,TOKENS['blue'],anchor='middle',weight=700)
        c.text(gx+sz*1.5,gy-18,'a',32,TOKENS['purple'],anchor='middle',weight=700)
        c.text(gx-31,gy+sz*.57,'A',32,TOKENS['blue'],anchor='middle',weight=700)
        c.text(gx-31,gy+sz*1.57,'a',32,TOKENS['purple'],anchor='middle',weight=700)
        combos=['AA','Aa','Aa','aa'];n=4 if reveal else min(4,int(phase/.32*4))
        for i,combo in enumerate(combos):
            xx=gx+(i%2)*sz;yy=gy+(i//2)*sz
            c.rect(xx,yy,sz,sz,TOKENS['background'],TOKENS['line'],r=8)
            if i<n:c.text(xx+sz/2,yy+sz*.62,combo,38,TOKENS['ink'],700,anchor='middle')
        c.text(bx+24,by+48,'EXPECTED PROBABILITIES',22,TOKENS['muted'],700,max_width=bw-48)
        if reveal:
            c.text(bx+24,by+121,'AA  ¼    Aa  ½    aa  ¼',27 if not vertical else 34)
            c.text(bx+24,by+192,'Dominant: ¾',38,TOKENS['teal'],700)
            c.text(bx+24,by+250,'Recessive: ¼',36,TOKENS['purple'])
        else:c.text(bx+24,by+136,'What fraction shows\nthe dominant trait?',30 if vertical else 27,TOKENS['amber'],max_width=bw-48)
        c.text(bx+24,by+310,'Complete dominance assumed.',21 if not vertical else 27,TOKENS['muted'],max_width=bw-48)
    cue=next(q for q in scene.cues if q.start_s<=t<q.end_s)
    c.text(margin,caption_y,cue.text,31 if vertical else 32,TOKENS['ink'],max_width=caption_w,lineheight=1.25)
    c.text(margin,h-43,'TECHNICAL PREVIEW • NO AUDIO • REVIEW PENDING',12,TOKENS['muted'],essential=False)
    c.rect(margin,h-23,w-2*margin,4,TOKENS['line'])
    c.rect(margin,h-23,(w-2*margin)*phase,4,TOKENS['teal'])
    return c.svg(),c.boxes
