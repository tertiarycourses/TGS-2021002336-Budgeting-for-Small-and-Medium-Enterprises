#!/usr/bin/env python3
"""
lms_push.py — push a course's Google Drive courseware links into LMS-TMS.

The Google Drive courseware folder is read FROM THE LMS ITSELF — the course's "Courseware
Link" field (courseLink / DB courseware_link), fetched via the API. Pass a folder link
explicitly only to override it.

Reads the current courseware files from that folder (via rclone), takes their "anyone with
the link can view" URLs, and writes them into the course record on
lms-tms.tertiaryinfotech.com:

    Trainer Slides URL  <- the .pptx in the  Master Trainer Slides  folder
    Learner Slides URL  <- the slides .pdf   in the  Learner Guide   folder
    Learner Guide URL   <- the LG-*.pdf      in the  Learner Guide   folder
    Lesson Plan URL     <- the LP-*.pdf      in the  Lesson Plan     folder

The LMS update endpoint (PUT /api/courses/update-course) is NOT a partial update: every
column it does not receive is overwritten with NULL, and its learning-unit / assessment
rows are re-synced from the payload. So this script does a strict read-modify-write —
GET /api/courses/edit-data, patch only the four URL keys, PUT the whole object back —
exactly as the CourseEditor UI does.

Usage:
    python3 lms_push.py [--course-code TGS-...] [--drive-folder <link>] [--dry-run]
"""

import argparse
import glob
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

REMOTE = os.environ.get("GDRIVE_REMOTE", "gdrive")
API = os.environ.get("LMS_TMS_API", "https://lms-tms.tertiaryinfotech.com")
# Machine auth: the LMS accepts a server-side service key in the x-api-key header
# (lib/auth/serviceKey.ts in ai-lms-tms). The key is resolved in this order:
#   1. shell env      LMS_TMS_API_KEY
#   2. project level  ./.claude/lms_tms_api_key, or LMS_TMS_API_KEY=... in ./.claude/.env / ./.env
#   3. user level     ~/.claude/lms_tms_api_key, or LMS_TMS_API_KEY=... in ~/.claude/.env
# Never hardcode it here; this file is pushed to GitHub. A project-level key file must be
# gitignored — it is a credential.


def _read_key_file(path):
    try:
        with open(path) as f:
            text = f.read()
    except OSError:
        return ""
    if os.path.basename(path).endswith(".env"):
        m = re.search(r"^\s*(?:export\s+)?LMS_TMS_API_KEY\s*=\s*['\"]?([^'\"\n#]+)", text, re.M)
        return m.group(1).strip() if m else ""
    return text.strip().splitlines()[0].strip() if text.strip() else ""


KEY_ENV_NAMES = ("LMS_TMS_API_KEY", "EXTERNAL_API_KEY_FOR_CLAWDBOT")

# Set from --repo in main(). The project-level key must be looked up under the repo being
# pushed, not the cwd — otherwise `--repo <other-course>` silently misses that course's key
# and the run 401s.
REPO_FOR_AUTH = "."


def _resolve_api_key(repo=None):
    for name in KEY_ENV_NAMES:
        key = os.environ.get(name, "").strip()
        if key:
            return key
    repo = repo or REPO_FOR_AUTH
    home = os.path.expanduser("~")
    for path in (os.path.join(repo, ".claude", "lms_tms_api_key"),
                 os.path.join(repo, ".claude", ".env"),
                 os.path.join(repo, ".env"),
                 os.path.join(home, ".claude", "lms_tms_api_key"),
                 os.path.join(home, ".claude", ".env")):
        key = _read_key_file(path)
        if key:
            return key
    return ""


def _lms_headers():
    # Resolved per call, not at import: --repo is parsed after this module loads.
    key = _resolve_api_key()
    return {"x-api-key": key} if key else {}


def _no_key_message():
    return (
        "\nNo API key was found, so LMS-TMS treated this as an anonymous request.\n"
        "The API accepts a service key in the `x-api-key` header. Provide it as:\n"
        "  1. export LMS_TMS_API_KEY=<key>              # shell env\n"
        "  2. ./.claude/lms_tms_api_key                 # project-level key file\n"
        "  3. ~/.claude/lms_tms_api_key  (chmod 600)    # user level — every repo can push\n"
        "The value is EXTERNAL_API_KEY_FOR_CLAWDBOT from the ai-lms-tms deployment.\n"
        "A key file is a credential: keep it gitignored and never commit it.\n\n"
        "Alternatively, paste the link block by hand — generate it with:\n"
        "  python3 <gdrive-push-skill>/gdrive_push.py --repo <repo> --links-only")

# Drive subfolder -> (canonical name, lowercase hint for fuzzy match)
FOLDERS = {
    "trainer_slides": ("Master Trainer Slides", "trainer slide"),
    "learner_guide": ("Learner Guide", "learner guide"),
    "lesson_plan": ("Lesson Plan", "lesson plan"),
    "assessment": ("Assessment", "assessment"),
    # The labs are a FOLDER of many files, not a single document, so the
    # Activities/Lab URL links the folder itself (see take_folder below).
    "activities": ("Activities", "activit"),
}


def is_answer_key(name):
    """'Answer to …' / 'Answers to …' — the marking guide. TRAINER-ONLY: it lives on Drive and
    is NEVER attached to the LMS, a learner-visible field, or GitHub."""
    return re.match(r"^\s*answers?\s+to\b", name.strip(), re.I) is not None


# ---------------------------------------------------------------- Google Drive

def rc(args, root, parse=False):
    r = subprocess.run(["rclone", *args, "--drive-root-folder-id", root],
                       capture_output=True, text=True)
    if r.returncode != 0:
        err = r.stderr.strip()
        if "couldn't fetch token" in err or "didn't find section" in err:
            raise SystemExit(
                f"rclone is not authorised yet.\nRun once:  rclone config create {REMOTE} drive scope=drive\n"
                f"and complete the Google sign-in in the browser.\n\nrclone said: {err[:300]}")
        raise SystemExit(f"rclone {' '.join(args[:2])} failed: {err[:600]}")
    return json.loads(r.stdout or "[]") if parse else r.stdout.strip()


def folder_id(link):
    """Accept a Drive folder URL or a bare folder ID."""
    m = re.search(r"/folders/([A-Za-z0-9_-]+)", link) or re.search(r"[?&]id=([A-Za-z0-9_-]+)", link)
    fid = m.group(1) if m else link.strip()
    if not re.fullmatch(r"[A-Za-z0-9_-]{10,}", fid):
        raise SystemExit(f"Not a Google Drive folder link or ID: {link!r}")
    return fid


def find_dir(root, canonical, hint):
    dirs = rc(["lsjson", f"{REMOTE}:", "--dirs-only"], root, parse=True)
    match = (next((d for d in dirs if d["Name"].strip().lower() == canonical.lower()), None)
             or next((d for d in dirs if hint in d["Name"].strip().lower()), None))
    if not match:
        raise SystemExit(f"Drive folder '{canonical}' not found. Run /gdrive-push first to create "
                         f"and populate it. Found: {[d['Name'] for d in dirs] or 'nothing'}")
    return match["Name"]


def files_in(root, path):
    """Current files in a folder (archive/ is a subfolder, so it is not listed)."""
    return rc(["lsjson", f"{REMOTE}:{path}", "--files-only"], root, parse=True)


def share_link(root, path, file_id):
    """Ensure 'anyone with the link can view', return a clean Drive view URL."""
    rc(["link", f"{REMOTE}:{path}"], root)  # creates the reader permission
    return f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"


def pick(files, pred, prefer=None):
    """Best match: those satisfying `prefer` win; ties broken by newest ModTime."""
    hits = [f for f in files if pred(f["Name"])]
    if not hits:
        return None, []
    hits.sort(key=lambda f: (bool(prefer and prefer(f["Name"])), f.get("ModTime", "")), reverse=True)
    return hits[0], hits


def is_learner_guide(n):
    """The Learner Guide document itself — as opposed to the slide deck PDF that also
    lives in the Learner Guide folder. Handles both naming lineages:
        LG-Full Stack React….pdf / LG_TGS-2020505042_….pdf      -> guide
        WSQ - Learner Guide Slides - ….pdf / <deck>-v3.0.pdf     -> deck
    """
    low = n.lower()
    if re.match(r"^lg[-_ ]", low):
        return True
    return "learner guide" in low and "slide" not in low


def collect_links(root):
    """Resolve the four courseware files on Drive.

    Returns ({lms field: (filename, url)}, [human-readable descriptions of what is missing]).
    """
    pdf = lambda n: n.lower().endswith(".pdf")
    out, missing = {}, []

    def take(field, folder_key, pred, what, prefer=None):
        canonical, hint = FOLDERS[folder_key]
        d = find_dir(root, canonical, hint)
        files = files_in(root, d)
        f, hits = pick(files, pred, prefer)
        if not f:
            missing.append(f"{FIELD_LABELS[field]}: no {what} in Drive folder '{d}' "
                           f"(present: {', '.join(x['Name'] for x in files) or 'nothing'})")
            return
        if len(hits) > 1:
            others = ", ".join(x["Name"] for x in hits[1:])
            print(f"  ! {len(hits)} candidates for {what} in '{d}' — using '{f['Name']}' (not: {others})")
        out[field] = (f["Name"], share_link(root, f"{d}/{f['Name']}", f["ID"]))

    # Trainer deck: the PPT. Prefer the "Master Trainer Slides" copy over a
    # trainer-personalised one (e.g. "WSQ - Dr. Alfred Ang - ....pptx").
    take("trainerSlidesUrl", "trainer_slides", lambda n: n.lower().endswith(".pptx"),
         "trainer slides .pptx", prefer=lambda n: "master" in n.lower())
    # Both learner artifacts live in the Learner Guide folder: the Learner Guide document
    # and the slide deck PDF. Anything that is not the guide is the deck.
    take("slidesUrl", "learner_guide", lambda n: pdf(n) and not is_learner_guide(n), "learner slides .pdf")
    take("learnerGuideUrl", "learner_guide", lambda n: pdf(n) and is_learner_guide(n), "learner guide .pdf")
    take("lessonPlanUrl", "lesson_plan", pdf, "lesson plan .pdf")

    # ---- the assessment: QUESTION PAPERS ONLY. Answer keys are trainer-only and never
    # reach the LMS, so they are filtered out before anything is picked.
    docx = lambda n: n.lower().endswith(".docx") and not is_answer_key(n)
    take("writtenAssessmentLink", "assessment",
         lambda n: docx(n) and re.match(r"^\s*wa\b|written assessment", n, re.I),
         "WA (SAQ) question paper .docx")
    # The practical instrument is EITHER a Case Study OR a Practical Performance — never both.
    take("caseStudyLink", "assessment",
         # `^cs\b` mirrors the WA rule: papers are named "CS Assessment- <course> - vNN.docx"
         # as often as "Case Study", and answer keys are already filtered out above.
         lambda n: docx(n) and re.search(r"^\s*cs\b|case study|\(cs\)", n, re.I),
         "Case Study (CS) question paper .docx")
    # "Practical Test" and "Practical Performance" are the same instrument — the house naming
    # varies between courses (the cover page reads "PRACTICAL TEST (PP)" either way), so both
    # spellings must resolve to the PP field. Without this a "Practical Test - ….docx" silently
    # reports as missing and the LMS keeps serving whatever stale paper it already had.
    take("practicalPerformanceAssessmentLink", "assessment",
         lambda n: docx(n) and re.search(
             r"^\s*pp\b|practical performance|practical test|\(pp\)", n, re.I),
         "PP / Practical Test question paper .docx")

    # A course has exactly ONE practical instrument — a Case Study or a PP, never both.
    # Whichever paper is on Drive IS the instrument; the absence of the other is not "missing",
    # so drop its complaint. (The one that is absent gets cleared on the LMS — see build_payload.)
    cs, pp = "caseStudyLink", "practicalPerformanceAssessmentLink"
    if cs in out and pp in out:
        raise SystemExit(
            "BOTH a Case Study and a PP question paper are on Drive — a course has ONE practical "
            "instrument. Remove the wrong one from the Drive Assessment folder and re-run.")
    absent = pp if cs in out else (cs if pp in out else None)
    if absent:
        missing[:] = [m for m in missing if not m.startswith(FIELD_LABELS[absent])]

    # ---- Activities / labs. Unlike every field above this links a FOLDER, not a
    # file: the labs are a whole tree (lab-NN markdown + the template library), and
    # learners need the folder so they can open any of them.
    take_folder("activitiesUrl", "activities", root, out, missing)

    return out, missing


def take_folder(field, folder_key, root, out, missing):
    """Link a Drive FOLDER (not a file) into an LMS URL field.

    Every other field points at one document; the labs are a whole tree, so the
    Activities/Lab URL has to be the folder itself.
    """
    canonical, hint = FOLDERS[folder_key]
    # find_dir aborts the run when a folder is absent, which is right for the
    # courseware folders but too harsh here: a course may legitimately have no
    # labs. Resolve it leniently and report a miss instead.
    dirs = rc(["lsjson", f"{REMOTE}:", "--dirs-only"], root, parse=True)
    match = (next((d for d in dirs if d["Name"].strip().lower() == canonical.lower()), None)
             or next((d for d in dirs if hint in d["Name"].strip().lower()), None))
    if not match:
        missing.append(f"{FIELD_LABELS[field]}: no '{canonical}' folder on Drive "
                       f"(found: {', '.join(d['Name'].strip() for d in dirs) or 'nothing'})")
        return
    d = match["Name"]
    # RECURSIVE count: the labs live in per-lab subfolders (lab1-…/, lab2-…/), so a
    # top-level-only listing reports a fully populated Activities folder as empty.
    entries = rc(["lsjson", f"{REMOTE}:{d}", "--files-only", "-R"], root, parse=True)
    entries = [e for e in entries if not e.get("Path", "").startswith("archive/")]
    if not entries:
        missing.append(f"{FIELD_LABELS[field]}: Drive folder '{d.strip()}' holds no files — "
                       f"run /gdrive-push first so the labs are uploaded")
        return
    # share the folder itself, then link it by id
    rc(["link", f"{REMOTE}:{d}"], root)
    url = f"https://drive.google.com/drive/folders/{match['ID']}"
    out[field] = (f"{d.strip()}/ ({len(entries)} file(s))", url)


# ------------------------------------------------------- course code (authoritative)

CODE_RE = re.compile(r"\bTGS-\d{6,}\b")


def codes_in_docx_or_pptx(path):
    """Every course code appearing in an Office file's text (docx/pptx are zipped XML)."""
    import xml.etree.ElementTree as ET
    import zipfile
    found = set()
    with zipfile.ZipFile(path) as z:
        parts = [n for n in z.namelist()
                 if n.startswith(("word/document", "ppt/slides/slide"))and n.endswith(".xml")]
        for n in sorted(parts)[:40]:  # cover slides / first pages are enough
            text = "".join(ET.fromstring(z.read(n)).itertext())
            found |= set(CODE_RE.findall(text))
    return found


def course_code_from_courseware(repo):
    """Read the course code OUT OF the courseware itself (deck cover / LG / LP), so we can
    never push one course's material onto another course's record.

    Returns (code, [(file, codes)]) or (None, []) if no courseware is present."""
    seen, evidence = {}, []
    for path in sorted(glob.glob(os.path.join(repo, "courseware", "*.pptx"))
                       + glob.glob(os.path.join(repo, "courseware", "*.docx"))):
        if os.path.basename(path).startswith("~$"):
            continue
        try:
            codes = codes_in_docx_or_pptx(path)
        except Exception as e:
            print(f"  ! could not read {os.path.basename(path)}: {str(e)[:80]}")
            continue
        if codes:
            evidence.append((os.path.basename(path), sorted(codes)))
            for c in codes:
                seen[c] = seen.get(c, 0) + 1
    if not seen:
        return None, evidence
    if len(seen) > 1:
        raise SystemExit("The courseware names MORE THAN ONE course code — refusing to guess "
                         "which course to update:\n  " +
                         "\n  ".join(f"{f}: {', '.join(c)}" for f, c in evidence))
    return next(iter(seen)), evidence


# ---------------------------------------------------------------------- LMS API

def get_json(url):
    try:
        req = urllib.request.Request(url, headers=_lms_headers() if url.startswith(API) else {})
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read()[:300].decode(errors="replace")
        hint = _no_key_message() if e.code in (401, 403) else ""
        raise SystemExit(f"GET {url} -> {e.code}: {body}{hint}")
    except urllib.error.URLError as e:
        raise SystemExit(f"GET {url} failed: {e.reason}")


def check_link(url):
    """Fetch a Drive link the way a learner would: is it reachable and anyone-with-link?
    Returns (ok, detail)."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            html = r.read(200_000).decode(errors="replace")
            if r.status != 200:
                return False, f"HTTP {r.status}"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, f"unreachable: {str(e)[:60]}"
    if "Request access" in html or "you need permission" in html.lower():
        return False, "NOT public — asks for access"
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    name = (m.group(1) if m else "?").replace(" - Google Drive", "").strip()
    if "/drive/folders/" in url:
        return True, f"public folder, serves '{name}'"
    return True, f"public, serves '{name}'"


def put_multipart(url, fields):
    boundary = "----lmspush" + os.urandom(8).hex()
    body = b""
    for name, value in fields.items():
        body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n"
                 ).encode() + value.encode() + b"\r\n"
    body += f"--{boundary}--\r\n".encode()
    req = urllib.request.Request(
        url, data=body, method="PUT",
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}",
                 "Content-Length": str(len(body)), **_lms_headers()})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, json.loads(r.read() or "{}")
    except urllib.error.HTTPError as e:
        body = e.read()[:500].decode(errors="replace")
        hint = _no_key_message() if e.code in (401, 403) else ""
        raise SystemExit(f"PUT {url} -> {e.code}: {body}{hint}")
    except urllib.error.URLError as e:
        raise SystemExit(f"PUT {url} failed: {e.reason}")


def resolve_course(code):
    res = get_json(f"{API}/api/courses/list")
    courses = res.get("data", [])
    hit = next((c for c in courses if (c.get("courseCode") or "").strip().upper() == code.upper()), None)
    if not hit:
        raise SystemExit(f"Course code {code} not found in LMS-TMS ({len(courses)} courses listed).")
    return hit["id"], hit.get("title", "")


def build_payload(course, urls):
    """Mirror CourseEditor.tsx's courseData exactly, with the four URLs overridden.

    Every column update-course does not receive is written as NULL, and learning units /
    assessments are re-synced from this payload — so pass the whole course back."""
    payload = {k: v for k, v in course.items() if k not in ("id", "topics", "assessments",
                                                            "isLeaderboardEnabled", "approvedTrainers")}
    payload["isGamified"] = course.get("isLeaderboardEnabled") or False
    payload["learningUnits"] = [
        {"id": t["id"], "title": t["title"], "position": i + 1,
         "subtopics": [{"id": s["id"], "title": s["title"], "position": j + 1}
                       for j, s in enumerate(t.get("subtopics", []))]}
        for i, t in enumerate(course.get("topics", []))
    ]
    payload["assessments"] = [
        {"id": a["id"], "title": a.get("title"), "category": a.get("category"),
         "status": a.get("status") or "Published", "fileUrl": a.get("fileUrl"), "action": "update"}
        for a in course.get("assessments", [])
    ]
    payload.update({k: v[1] for k, v in urls.items()})

    # ---- assessment links. The LMS stores each instrument twice: a flat *Link column AND an
    # entry in assessmentMethods{} (link + enabled) — the course page renders the latter, so
    # both must be written or the page keeps showing the old document.
    methods = dict(payload.get("assessmentMethods") or {})

    def set_method(key, url):
        methods[key] = {"link": url or "", "enabled": bool(url)}

    if "writtenAssessmentLink" in urls:
        set_method("writtenAssessment", urls["writtenAssessmentLink"][1])

    # ONE practical instrument: set the one we have, and CLEAR the other so a stale link
    # (e.g. a PP doc left behind on a Case Study course) cannot survive on the LMS.
    cs_url = urls.get("caseStudyLink", (None, None))[1]
    pp_url = urls.get("practicalPerformanceAssessmentLink", (None, None))[1]
    if cs_url or pp_url:
        set_method("caseStudy", cs_url)
        set_method("practicalExam", pp_url)
        payload["practicalPerformanceAssessmentLink"] = pp_url or ""

    payload["assessmentMethods"] = methods
    payload.pop("caseStudyLink", None)   # not a real column — it lives in assessmentMethods
    return payload


# ------------------------------------------------------------------------ main

FIELD_LABELS = {
    "trainerSlidesUrl": "Trainer Slides URL",
    "slidesUrl": "Learner Slides URL",
    "learnerGuideUrl": "Learner Guide URL",
    "lessonPlanUrl": "Lesson Plan URL",
    "writtenAssessmentLink": "Written Assessment (question paper)",
    "caseStudyLink": "Case Study (question paper)",
    "practicalPerformanceAssessmentLink": "Practical Performance (question paper)",
    "activitiesUrl": "Activities/Lab URL",
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--course-code", help="e.g. TGS-2020505042 (default: from the repo folder name)")
    ap.add_argument("--drive-folder", help="override the Drive folder (default: the course's "
                                           "Courseware Link, read from the LMS)")
    ap.add_argument("--repo", default=os.getcwd(), help="course repo root (default: cwd)")
    ap.add_argument("--dry-run", action="store_true", help="show the plan; do not write to LMS-TMS")
    ap.add_argument("--allow-missing", action="store_true",
                    help="update only the fields whose file exists on Drive, instead of aborting")
    ap.add_argument("--only", metavar="FIELD", action="append",
                    help="write ONLY these LMS fields (repeatable), e.g. --only activitiesUrl. "
                         "Every other field is left exactly as it is on the LMS. Use when one "
                         "field is verified good but others are still blocked on QA.")
    a = ap.parse_args()

    global REPO_FOR_AUTH
    REPO_FOR_AUTH = a.repo

    # The course code is taken FROM THE COURSEWARE ITSELF (deck cover / LG / LP), not from
    # the folder name — a renamed or copied repo folder must never be able to publish one
    # course's material onto another course's record.
    ware_code, evidence = course_code_from_courseware(a.repo)
    folder_m = re.search(r"(TGS-\d+)", os.path.basename(os.path.abspath(a.repo)))
    folder_code = folder_m.group(1) if folder_m else None

    print(f"LMS-TMS     : {API}")
    if ware_code:
        src = ", ".join(f"{f}" for f, _ in evidence[:3])
        print(f"Course code : {ware_code}  (read from the courseware: {src})")
    for other, label in ((folder_code, "repo folder name"), (a.course_code, "--course-code")):
        if ware_code and other and other.upper() != ware_code.upper():
            raise SystemExit(
                f"\nCOURSE CODE MISMATCH — refusing to push.\n"
                f"  the courseware says : {ware_code}\n"
                f"  the {label} says : {other}\n"
                f"Publishing this material onto {other} would put one course's slides on another "
                f"course's page. Fix the mismatch (or point --repo at the right course) and re-run.")
    code = ware_code or a.course_code or folder_code
    if not code:
        raise SystemExit("No course code found in the courseware, the repo folder name, or "
                         "--course-code. Cannot tell which LMS course to update.")
    if not ware_code:
        print(f"Course code : {code}  (! not found in the courseware — falling back to "
              f"{'--course-code' if a.course_code else 'the repo folder name'})")

    course_id, title = resolve_course(code)
    print(f"LMS course  : {title}  ({course_id})")

    res = get_json(f"{API}/api/courses/edit-data?courseId={course_id}")
    course = res.get("data") or {}
    if not course.get("title"):
        raise SystemExit(f"edit-data returned no course object for {course_id}; aborting rather than "
                         f"PUTting an empty payload (it would null the course).")

    # The Drive folder comes from the LMS course record itself (Courseware Link).
    if a.drive_folder:
        src, link = "--drive-folder override", a.drive_folder
    else:
        link = course.get("courseLink")
        src = "Courseware Link (from LMS)"
        if not link:
            raise SystemExit(
                f"{code} has no Courseware Link set in LMS-TMS, so there is no Drive folder to read.\n"
                f"Set it on the course page, or pass --drive-folder <link>.")
    root = folder_id(link)
    print(f"Drive folder: {link}\n              ({src}, id {root})\n")

    print("Resolving courseware files on Google Drive…")
    urls, missing = collect_links(root)

    # --only: restrict the write to an explicit whitelist. Everything else is dropped from
    # the payload entirely (not blanked), so untouched fields keep their current LMS value.
    if a.only:
        unknown = [f for f in a.only if f not in FIELD_LABELS]
        if unknown:
            raise SystemExit(f"--only: unknown field(s) {unknown}. "
                             f"Valid: {', '.join(sorted(FIELD_LABELS))}")
        absent = [f for f in a.only if f not in urls]
        if absent:
            raise SystemExit("--only: no file/folder resolved on Drive for "
                             f"{[FIELD_LABELS[f] for f in absent]} — nothing to write.")
        urls = {f: urls[f] for f in a.only}
        missing = []   # the excluded fields are deliberately untouched, not "missing"
        print(f"  --only: writing {len(urls)} field(s); all others left untouched on the LMS.")

    for field, (name, url) in urls.items():
        print(f"  {FIELD_LABELS[field]:<20} {name}\n  {'':<20} {url}")

    if missing:
        print("\nMISSING on Google Drive — these files do not exist, so their LMS field "
              "cannot be set:")
        for msg in missing:
            print(f"  ✗ {msg}")
        if not a.allow_missing:
            raise SystemExit("\nAborting: refusing to do a partial update by default. Either produce "
                             "the missing file(s) and re-run /gdrive-push, or re-run with "
                             "--allow-missing to update only the fields that were found "
                             "(the rest keep their current LMS value).")
        print("  → --allow-missing: these fields keep their current LMS value.")

    print("\nChanges:")
    for field, (_, url) in urls.items():
        old = course.get(field) or "(empty)"
        same = " (unchanged)" if old == url else ""
        print(f"  {FIELD_LABELS[field]}{same}\n    old: {old}\n    new: {url}")

    if a.dry_run:
        print("\n[dry-run] nothing written. Re-run without --dry-run to push to LMS-TMS.")
        return

    payload = build_payload(course, urls)
    # Guard: never PUT a payload that would blank identity/structure columns.
    for must in ("title", "courseCode"):
        if not payload.get(must):
            raise SystemExit(f"Refusing to PUT: '{must}' is empty in the read-back course object.")

    status, body = put_multipart(f"{API}/api/courses/update-course?courseId={course_id}",
                                 {"courseData": json.dumps(payload)})
    if not body.get("success", status == 200):
        raise SystemExit(f"Update rejected ({status}): {json.dumps(body)[:400]}")
    print(f"\n✅ PUT update-course -> {status}")

    # Verify by reading the course back.
    after = (get_json(f"{API}/api/courses/edit-data?courseId={course_id}") or {}).get("data", {})
    ok = True
    print("\nVerification (read back from LMS-TMS, then fetch each link):")
    def stored_value(field):
        """Read the field back. caseStudy has no flat column — it lives in assessmentMethods,
        which is also what the course page renders."""
        if field == "caseStudyLink":
            return ((after.get("assessmentMethods") or {}).get("caseStudy") or {}).get("link")
        return after.get(field)

    def same_file(a, b):
        """The LMS normalises Drive URLs (it drops ?usp=sharing), so compare by ID.
        Also matches /drive/folders/<id> for the Activities folder link."""
        fid = lambda u: (re.search(r"/d/([\w-]+)|/folders/([\w-]+)|[?&]id=([\w-]+)",
                                   u or "") or None)
        ma, mb = fid(a), fid(b)
        if ma and mb:
            gid = lambda m: m.group(1) or m.group(2) or m.group(3)
            return gid(ma) == gid(mb)
        return a == b

    for field, (name, url) in urls.items():
        got = stored_value(field)
        stored = same_file(got, url)
        live, detail = check_link(got) if got else (False, "no URL stored")
        good = stored and live
        ok &= good
        print(f"  {'✓' if good else '✗'} {FIELD_LABELS[field]}: {name}")
        if not stored:
            print(f"      ✗ LMS stored a different URL: {got or '(empty)'}")
        print(f"      {detail}\n      {got or ''}")
    for must in ("title", "courseCode", "trainingHours"):
        if course.get(must) and not after.get(must):
            ok = False
            print(f"  ✗ {must} was blanked by the update — investigate immediately.")
    if not ok:
        sys.exit(1)
    print(f"\nAll {len(urls)} courseware URLs are live on the LMS-TMS course page.")


if __name__ == "__main__":
    main()
