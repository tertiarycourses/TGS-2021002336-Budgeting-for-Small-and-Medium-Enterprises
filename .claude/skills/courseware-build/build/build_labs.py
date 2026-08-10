#!/usr/bin/env python3
"""Generate labs/lab-NN-*.md + labs/README.md from the single-source data files."""
import os, sys, re, glob

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
LABS=os.path.join(REPO,"labs")

def slug(t):
    s=re.sub(r"[^a-z0-9]+","-",t.lower()).strip("-")
    return s[:60]

for f in glob.glob(os.path.join(LABS,"lab-*.md")): os.remove(f)

TOPICS_BY_NUM={t["num"]:t for t in C.TOPICS}
for a in ACT:
    t=TOPICS_BY_NUM[a["topic"]]
    fn=os.path.join(LABS,f"lab-{a['num']:02d}-{slug(a['title'])}.md")
    out=[f"# Lab {a['num']} — {a['title']}",""]
    out.append(f"**Course:** {C.TITLE} ({C.COURSE_CODE})  ")
    out.append(f"**Topic {t['code']}:** {t['title']}  ")
    out.append(f"**Learning outcome:** {a['objective']}  ")
    out.append(f"**Tools:** {a['services']}")
    out+=["",f"## Goal","",a["desc"],"","## What you'll produce","",a["build"],"",
          f"![Lab {a['num']} workflow](assets/lab-{a['num']:02d}-workflow.png)","","## Step-by-step",""]
    for i,(instr,cmd) in enumerate(a["steps"],1):
        out.append(f"{i}. {instr}")
        if cmd: out+=["",f"   ```",f"   {cmd}","   ```",""]
    out+=["","## Check your work","",a["test"],""]
    with open(fn,"w") as f: f.write("\n".join(out))
    print("Saved",fn)

# index
out=[f"# {C.TITLE} — Hands-On Labs","",
     f"12 hands-on activities across the 7 course topics, aligned to the Skills Framework TSC {C.TSC_TITLE} ({C.TSC_CODE}).",
     ""]
for t in C.TOPICS:
    out.append(f"## Topic {t['code']} — {t['title']}")
    out.append("")
    for a in [x for x in ACT if x["topic"]==t["num"]]:
        out.append(f"- [Lab {a['num']} — {a['title']}](lab-{a['num']:02d}-{slug(a['title'])}.md)")
    out.append("")
with open(os.path.join(LABS,"README.md"),"w") as f: f.write("\n".join(out))
print("Saved",os.path.join(LABS,"README.md"))
