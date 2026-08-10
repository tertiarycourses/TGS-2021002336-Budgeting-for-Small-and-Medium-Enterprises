#!/usr/bin/env python3
"""
tms_assessment.py — pull the ORIGINAL assessment papers from LMS-TMS and report what a
revision must mirror: the instrument type, the number of questions, the K/A codes and the
timings.

The TMS course record is the source of truth for the paper that is actually in use. A copy
sitting in reference/ may be stale, may be the wrong course, or may simply not be the paper
the ATO has on file. So we read the links off the course record itself:

    writtenAssessmentLink                 -> the WA (SAQ) paper
    practicalPerformanceAssessmentLink    -> the PP paper
    assessmentMethods[*].enabled+link     -> which practical instrument is actually declared
                                             (practicalExam / caseStudy / project / rolePlay …)

Each link is a Google Doc; we export it as text (the docs are anyone-with-link) and count.

Usage:
    python3 tms_assessment.py --course-code TGS-XXXXXXXXXX [--save-dir reference/tms]
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.request

API = "https://lms-tms.tertiaryinfotech.com"
UA = {"User-Agent": "Mozilla/5.0"}

# assessmentMethods key -> the instrument name used on the WSQ cover page
METHOD_INSTRUMENT = {
    "practicalExam": ("PP", "Practical Performance (PP)"),
    "caseStudy": ("CS", "Case Study (CS)"),
    "project": ("PJ", "Project (PJ)"),
    "rolePlay": ("RP", "Role Play (RP)"),
    "assignment": ("AS", "Assignment (AS)"),
    "writtenAssessment": ("WA", "Written Assessment (SAQ)"),
    "oralQuestioning": ("OQ", "Oral Questioning (OQ)"),
}


def get_json(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"GET {url} -> {e.code}: {e.read()[:300].decode(errors='replace')}")
    except urllib.error.URLError as e:
        raise SystemExit(f"GET {url} failed: {e.reason}")


def resolve_course(code):
    for c in get_json(f"{API}/api/courses/list").get("data", []):
        if (c.get("courseCode") or "").strip().upper() == code.upper():
            return c["id"], c.get("title", "")
    raise SystemExit(f"Course code {code} is not in LMS-TMS.")


def doc_text(link):
    """Export a Google Doc / Drive file as plain text. Returns '' if it is not readable
    (private, or not a Doc) — the caller decides whether that is fatal."""
    m = re.search(r"/document/d/([\w-]+)", link or "") or re.search(r"/d/([\w-]+)", link or "")
    if not m:
        return ""
    url = f"https://docs.google.com/document/d/{m.group(1)}/export?format=txt"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  ! could not export {url}: {e}", file=sys.stderr)
        return ""


# The instrument printed at the top of the PAPER, not the TMS field it happens to be filed
# under. These disagree in practice: a Case Study is routinely stored in the practicalExam
# slot. The paper is what the assessor and the auditor hold, so the paper wins.
TITLE_INSTRUMENT = [
    (r"case\s*study", "CS", "Case Study (CS)"),
    (r"practical\s*performance", "PP", "Practical Performance (PP)"),
    (r"written\s*assessment|\bSAQ\b", "WA", "Written Assessment (SAQ)"),
    (r"\brole\s*play", "RP", "Role Play (RP)"),
    (r"\bproject\b", "PJ", "Project (PJ)"),
]


def instrument_from_paper(text):
    head = "\n".join(text.splitlines()[:12])
    for pat, short, name in TITLE_INSTRUMENT:
        if re.search(pat, head, re.I):
            return short, name
    return None, None


def analyse(text, kind):
    """Count the questions and harvest the codes. Papers are written by humans, so accept
    the several numbering styles that show up: 'Question 1', '1.', 'Task 1', 'Q1'."""
    qs = set()
    for pat in (r"^\s*(?:Question|Task|Activity)\s+(\d+)\b",
                r"^\s*Q\s*(\d+)[.):]",
                r"^\s*(\d{1,2})[.)]\s+\S"):
        for m in re.finditer(pat, text, re.M | re.I):
            qs.add(int(m.group(1)))
        if qs:
            break

    codes = sorted(set(re.findall(r"\b([KA]\d{1,2})\b", text)),
                   key=lambda c: (c[0], int(c[1:])))
    mins = re.findall(r"(\d{2,3})\s*(?:minutes|mins?\b)", text, re.I)
    hrs = re.findall(r"(\d(?:\.\d)?)\s*hours?\b", text, re.I)

    return {
        "kind": kind,
        "questions": len(qs),
        "numbers": sorted(qs),
        "codes": codes,
        "k_codes": [c for c in codes if c.startswith("K")],
        "a_codes": [c for c in codes if c.startswith("A")],
        "duration": (f"{mins[0]} minutes" if mins else f"{hrs[0]} hours" if hrs else "?"),
        "chars": len(text),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--course-code", required=True)
    ap.add_argument("--save-dir", help="also write the exported text here")
    a = ap.parse_args()

    cid, title = resolve_course(a.course_code)
    c = get_json(f"{API}/api/courses/edit-data?courseId={cid}").get("data") or {}
    print(f"LMS course  : {title}  ({a.course_code})")

    methods = c.get("assessmentMethods") or {}
    enabled = [(k, v.get("link", "")) for k, v in methods.items()
               if isinstance(v, dict) and v.get("enabled")]

    papers = []
    if c.get("writtenAssessmentLink"):
        papers.append(("WA", "Written Assessment (SAQ)", c["writtenAssessmentLink"]))
    for key, link in enabled:
        if key == "writtenAssessment":
            continue
        short, name = METHOD_INSTRUMENT.get(key, (key.upper(), key))
        papers.append((short, name, link or c.get("practicalPerformanceAssessmentLink", "")))
    if not any(p[0] != "WA" for p in papers) and c.get("practicalPerformanceAssessmentLink"):
        papers.append(("PP", "Practical Performance (PP)", c["practicalPerformanceAssessmentLink"]))

    if not papers:
        raise SystemExit("The TMS course record carries no assessment links. Fall back to reference/.")

    print(f"Assessment  : {c.get('assessmentHours', '?')} hours declared\n")
    out = []
    for short, name, link in papers:
        print(f"── {name}\n   {link}")
        text = doc_text(link)
        if not text.strip():
            print("   ! not readable from the TMS link — check that it is anyone-with-link.\n")
            continue
        if a.save_dir:
            import os
            os.makedirs(a.save_dir, exist_ok=True)
            p = os.path.join(a.save_dir, f"original-{short}.txt")
            open(p, "w").write(text)
            print(f"   saved: {p}")
        paper_short, paper_name = instrument_from_paper(text)
        if paper_short and paper_short != short:
            print(f"   ! the TMS files this under {name}, but the PAPER is titled "
                  f"{paper_name}. The paper wins — build a {paper_short}.")
            short, name = paper_short, paper_name

        r = analyse(text, short)
        r["instrument"] = name
        out.append(r)
        print(f"   instrument: {name}")
        print(f"   questions : {r['questions']}   {r['numbers']}")
        print(f"   codes     : {', '.join(r['codes']) or '(none printed)'}")
        print(f"   duration  : {r['duration']}\n")

    print("MIRROR THIS in the new paper — same instrument, same question count, same codes, "
          "same timings. Rewrite only the content.")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
