#!/usr/bin/env python3
"""Generate the activities/ tree from the single-source data files.

One subfolder per activity — activities/activity01 … activity12 — each holding the guide
(README.md), the workflow diagram and the mock data files (.xlsx + .csv),
plus a labs/README.md index."""
import os, sys, re, glob, shutil

HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import course_data as C
from data_domain1 import DOMAIN1; from data_domain2 import DOMAIN2
from data_domain3 import DOMAIN3; from data_domain4 import DOMAIN4
from data_domain5 import DOMAIN5; from data_domain6 import DOMAIN6
from data_domain7 import DOMAIN7
from data_files import DATA
ACT=DOMAIN1+DOMAIN2+DOMAIN3+DOMAIN4+DOMAIN5+DOMAIN6+DOMAIN7

def _find_repo(start):
    env=os.environ.get("COURSE_REPO")
    if env and os.path.isdir(env): return env
    d=start
    for _ in range(8):
        d=os.path.dirname(d)
        if os.path.isdir(os.path.join(d,"courseware")) and os.path.isdir(os.path.join(d,"activities")): return d
    return os.path.dirname(os.path.dirname(HERE))
REPO=_find_repo(HERE)
ACTS=os.path.join(REPO,"activities")

# clear superseded layouts (old labs/ tree variants)
for f in glob.glob(os.path.join(ACTS,"lab-*.md")): os.remove(f)
for d in glob.glob(os.path.join(ACTS,"lab*")) + [os.path.join(ACTS,"data"),os.path.join(ACTS,"assets")]:
    if os.path.isdir(d): shutil.rmtree(d)

TOPICS_BY_NUM={t["num"]:t for t in C.TOPICS}
for a in ACT:
    t=TOPICS_BY_NUM[a["topic"]]
    folder=os.path.join(ACTS,f"activity{a['num']:02d}"); os.makedirs(folder,exist_ok=True)
    guide=os.path.join(folder,"README.md")
    out=[f"# Activity {a['num']} — {a['title']}",""]
    out.append(f"**Course:** {C.TITLE} ({C.COURSE_CODE})  ")
    out.append(f"**Topic {t['code']}:** {t['title']}  ")
    out.append(f"**Learning outcome:** {a['objective']}  ")
    out.append(f"**Tools:** {a['services']}")
    out+=["",f"## Goal","",a["desc"],"","## What you'll produce","",a["build"],"",
          f"![Activity {a['num']} workflow](activity-{a['num']:02d}-workflow.png)","","## Step-by-step",""]
    for i,(instr,cmd) in enumerate(a["steps"],1):
        out.append(f"{i}. {instr}")
        if cmd: out+=["",f"   ```",f"   {cmd}","   ```",""]
    d=DATA.get(a["num"])
    if d:
        out+=["","## Data files (in this folder)",""]
        for df,desc in d["files"]:
            out.append(f"- [`{df}`]({df}) — {desc}")
        out+=["","## Analyzing the Excel workbook — step by step",""]
        for i,s in enumerate(d["excel_steps"],1): out.append(f"{i}. {s}")
        out+=["","## Analyzing the CSV data — step by step",""]
        for i,s in enumerate(d["csv_steps"],1): out.append(f"{i}. {s}")
    out+=["","## Check your work","",a["test"],""]
    with open(guide,"w") as f: f.write("\n".join(out))
    print("Saved",guide)

# index
out=[f"# {C.TITLE} — Hands-On Labs","",
     f"12 hands-on activities across the 7 course topics, aligned to the Skills Framework TSC {C.TSC_TITLE} ({C.TSC_CODE}).",
     "Each activity folder holds the guide (README.md), the workflow diagram and the activity's mock data (Excel + CSV).",
     ""]
for t in C.TOPICS:
    out.append(f"## Topic {t['code']} — {t['title']}")
    out.append("")
    for a in [x for x in ACT if x["topic"]==t["num"]]:
        out.append(f"- [Activity {a['num']} — {a['title']}](activity{a['num']:02d}/README.md)")
    out.append("")
with open(os.path.join(ACTS,"README.md"),"w") as f: f.write("\n".join(out))
print("Saved",os.path.join(ACTS,"README.md"))
