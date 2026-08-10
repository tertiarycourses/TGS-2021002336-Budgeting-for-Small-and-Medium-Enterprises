#!/usr/bin/env python3
"""Generate one workflow diagram PNG per lab (labs/assets/lab-NN-workflow.png)
from the single-source data files, in the Tertiary house palette. Embedded in
the Learner Guide and referenced by the lab MD files."""
import os, sys, textwrap
from PIL import Image, ImageDraw, ImageFont

HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import course_data as C
from data_domain1 import DOMAIN1; from data_domain2 import DOMAIN2
from data_domain3 import DOMAIN3; from data_domain4 import DOMAIN4
from data_domain5 import DOMAIN5; from data_domain6 import DOMAIN6
from data_domain7 import DOMAIN7
ACT=DOMAIN1+DOMAIN2+DOMAIN3+DOMAIN4+DOMAIN5+DOMAIN6+DOMAIN7

def _find_repo(start):
    env=os.environ.get("COURSE_REPO")
    if env and os.path.isdir(env): return env
    d=start
    for _ in range(8):
        d=os.path.dirname(d)
        if os.path.isdir(os.path.join(d,"courseware")) and os.path.isdir(os.path.join(d,"labs")): return d
    return os.path.dirname(os.path.dirname(HERE))
REPO=_find_repo(HERE)
OUT=os.path.join(REPO,"labs","assets"); os.makedirs(OUT,exist_ok=True)

BLUE=(31,111,235); TEAL=(16,185,129); VIOLET=(124,58,237); AMBER=(245,158,11)
INK=(22,27,38); GREY=(91,99,114); LIGHT=(245,248,252); WHITE=(255,255,255); LINEC=(226,232,240)
PALETTE=[BLUE,TEAL,VIOLET,AMBER]

def font(sz,bold=False):
    cands=(["/System/Library/Fonts/Supplemental/Arial Bold.ttf","/Library/Fonts/Arial Bold.ttf"] if bold
           else ["/System/Library/Fonts/Supplemental/Arial.ttf","/Library/Fonts/Arial.ttf"])
    for c in cands:
        if os.path.exists(c): return ImageFont.truetype(c,sz)
    return ImageFont.load_default()

def condense(txt,limit=72):
    t=txt.strip()
    if t.startswith("STEP") and " — " in t:
        t=t.split(" — ",1)[1]
    for sep in (": ",". "):
        head=t.split(sep)[0]
        if sep in t and len(head)>=12:
            t=head; break
    t=t.rstrip(".")
    return t if len(t)<=limit else t[:limit-1].rsplit(" ",1)[0]+"…"

W=1760
for a in ACT:
    steps=[condense(instr) for instr,_ in a["steps"]]
    n=len(steps)
    cols=min(4,n); rows=(n+cols-1)//cols
    M=48; GX=36; GY=64; BH=180; TH=120
    BW=(W-2*M-GX*(cols-1))//cols
    H=TH+rows*BH+(rows-1)*GY+M
    img=Image.new("RGB",(W,H),WHITE); d=ImageDraw.Draw(img)
    d.rectangle([0,0,W,10],fill=BLUE)
    d.text((M,34),f"Lab {a['num']} — {a['title']}",font=font(38,True),fill=INK)
    d.text((M,84),f"Workflow · Tools: {a['services']}",font=font(24),fill=GREY)
    for i,st in enumerate(steps):
        r=i//cols; c=i%cols
        x=M+c*(BW+GX); y=TH+r*(BH+GY); col=PALETTE[i%4]
        d.rounded_rectangle([x,y,x+BW,y+BH],radius=14,fill=LIGHT,outline=LINEC,width=2)
        d.rectangle([x,y,x+BW,y+10],fill=col)
        d.ellipse([x+18,y+28,x+66,y+76],fill=col)
        f=font(26,True); tb=d.textbbox((0,0),str(i+1),font=f)
        d.text((x+42-(tb[2]-tb[0])/2,y+52-(tb[3]-tb[1])/2-tb[1]),str(i+1),font=f,fill=WHITE)
        lines=textwrap.wrap(st,width=int(BW/13))[:4]
        yy=y+92
        for ln in lines:
            d.text((x+18,yy),ln,font=font(20),fill=INK); yy+=27
        # connector: horizontal arrows within a row only (the numbered badges carry the order)
        if i<n-1 and c<cols-1:
            ax=x+BW+4; ay=y+BH//2
            d.line([ax,ay,ax+GX-12,ay],fill=col,width=4)
            d.polygon([(ax+GX-12,ay-8),(ax+GX-12,ay+8),(ax+GX-2,ay)],fill=col)
    fn=os.path.join(OUT,f"lab-{a['num']:02d}-workflow.png")
    img.save(fn); print("Saved",fn)
