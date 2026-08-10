#!/usr/bin/env python3
"""Push WSQ courseware + labs DIRECTLY to the user's Google Drive courseware folder via
rclone, archiving old versions. Upload-and-move only — nothing on Drive is ever deleted.

Usage:  python3 gdrive_push.py [<drive-folder-link-or-id>] [--repo DIR] [--dry-run]

The destination folder: if no link is given it is resolved FROM THE LMS — the course's
"Courseware Link" field (courseLink / DB courseware_link) on lms-tms.tertiaryinfotech.com,
looked up by the TGS- course code READ OUT OF THE COURSEWARE ITSELF (deck cover / LG / LP),
never from the repo folder name. A link passed on the command line always wins, and if it
disagrees with the LMS the script says so and aborts unless --force-folder is given — a
renamed or copied repo must never be able to publish one course's material into another
course's Drive folder.

Routing (folders matched case-insensitively under the given root; created if missing):
  Master Trainer Slides : slides .pptx + .pdf
  Learner Guide         : LG .docx + .pdf, plus the slides .pdf
  Lesson Plan           : LP .docx + .pdf
  Assessment            : all assessment .docx (question papers + answer keys)
  Activities            : the whole labs/ tree (rclone sync with --backup-dir)

Change detection: files whose MD5 already matches the Drive copy are SKIPPED (no
re-upload, no archiving). Only changed/new files are pushed.

Archiving: in each courseware folder, EVERY pre-existing file that is not identical
to a file being pushed (old versions, old names, Google-native docs) is MOVED
server-side into that folder's "archive" subfolder first. The archive folder is
created if absent, and any "Archive"/"archives" variant is renamed to the canonical
lowercase "archive"; any "old versions"-style folder is merged into archive/. For labs, changed/removed files are MOVED to Activities/archive
by rclone's --backup-dir. Nothing is ever deleted.

Every newly uploaded courseware file is set to "anyone with the link can view".

Prerequisite (one-time): `rclone config create gdrive drive scope=drive`.
"""
import glob
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

REMOTE = os.environ.get("GDRIVE_REMOTE", "gdrive")
API = os.environ.get("LMS_TMS_API", "https://lms-tms.tertiaryinfotech.com")
CODE_RE = re.compile(r"\bTGS-\d{6,}\b")


# ------------------------------------------- destination folder, resolved from the LMS

def folder_id(link):
    """Accept a Drive folder URL, an 'open?id=' URL, or a bare id."""
    if not link:
        return None
    m = re.search(r"(?:folders/|[?&]id=)([A-Za-z0-9_-]{10,})", link)
    return m.group(1) if m else link.strip()


# ------------------------------------------- .env: the offline record of the course link
# The LMS API needs an authenticated session, so it 401s in headless/CI runs. The course's
# .env is the durable local record of the same Courseware Link: every successful push
# WRITES it, and a push that cannot reach the LMS READS it instead of asking the user to
# retype the folder. The LMS still wins whenever it is reachable.

ENV_KEYS = ("COURSEWARE_LINK", "COURSE_LINK")   # first key wins on read


def env_path(repo):
    return os.path.join(repo, ".env")


def read_env(repo):
    """{KEY: value} from the course .env (blank/comment lines and inline quotes ignored)."""
    out = {}
    try:
        with open(env_path(repo), encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                out[k.strip()] = v.strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    return out


def courseware_link_from_env(repo):
    """(link, id) recorded by a previous push, or (None, None)."""
    env = read_env(repo)
    for k in ENV_KEYS:
        if env.get(k):
            return env[k], folder_id(env[k])
    return None, None


def write_env(repo, link, code=None, title=None):
    """Record the Courseware Link in the course .env, preserving every other key.

    Idempotent: re-running with the same link rewrites the same file. Returns True if the
    file changed, so the caller can say so rather than claiming a write that did nothing.
    """
    fid = folder_id(link)
    if not fid:
        return False
    desired = {"COURSE_LINK": link, "COURSEWARE_LINK": link, "GDRIVE_FOLDER_ID": fid}
    path = env_path(repo)
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        lines = [f"# Course: {title}" if title else "# WSQ course",
                 f"# WSQ Course Code: {code}" if code else "",
                 "",
                 "# Google Drive courseware folder for this course",
                 "# Written automatically by gdrive_push.py — used as the fallback when",
                 "# the LMS-TMS API is unreachable (it requires an authenticated session).",
                 ""]
        lines = [l for l in lines if l != ""] + [""]

    out, seen = [], set()
    for line in lines:
        s = line.strip()
        if s and not s.startswith("#") and "=" in s:
            k = s.split("=", 1)[0].strip()
            if k in desired:
                if k not in seen:
                    out.append(f"{k}={desired[k]}")
                    seen.add(k)
                continue          # drop duplicate/stale copies of the same key
        out.append(line)
    for k, v in desired.items():
        if k not in seen:
            out.append(f"{k}={v}")

    new = "\n".join(out).rstrip() + "\n"
    try:
        with open(path, encoding="utf-8") as f:
            if f.read() == new:
                return False
    except FileNotFoundError:
        pass
    with open(path, "w", encoding="utf-8") as f:
        f.write(new)
    return True


def codes_in_docx_or_pptx(path):
    """Every TGS- course code appearing in an Office file's text (docx/pptx are zipped XML)."""
    found = set()
    with zipfile.ZipFile(path) as z:
        parts = [n for n in z.namelist()
                 if n.startswith(("word/document", "ppt/slides/slide")) and n.endswith(".xml")]
        for n in sorted(parts)[:40]:  # cover slides / first pages are enough
            found |= set(CODE_RE.findall("".join(ET.fromstring(z.read(n)).itertext())))
    return found


def course_code_from_courseware(repo):
    """Read the course code OUT OF the courseware itself, so a renamed or copied repo can
    never publish one course's material into another course's Drive folder."""
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
                         "which course's Drive folder to push to:\n  " +
                         "\n  ".join(f"{f}: {', '.join(c)}" for f, c in evidence))
    return next(iter(seen)), evidence


def get_json(url):
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"GET {url} -> {e.code}: {e.read()[:300].decode(errors='replace')}")
    except urllib.error.URLError as e:
        raise SystemExit(f"GET {url} failed: {e.reason}")


def courseware_link_from_lms(repo):
    """(link, code, title) from the course's Courseware Link field on LMS-TMS."""
    code, evidence = course_code_from_courseware(repo)
    if not code:
        raise SystemExit(
            "No TGS- course code found in the courseware (courseware/*.pptx|*.docx), so the "
            "Drive folder cannot be resolved from the LMS.\nPass the folder link explicitly:\n"
            "  gdrive_push.py <drive-folder-link> --repo <dir>")
    print(f"  course code (from {', '.join(f for f, _ in evidence)}): {code}")
    courses = (get_json(f"{API}/api/courses/list") or {}).get("data", [])
    hit = next((c for c in courses
                if (c.get("courseCode") or "").strip().upper() == code.upper()), None)
    if not hit:
        raise SystemExit(f"Course code {code} not found in LMS-TMS ({len(courses)} courses listed).")
    course = (get_json(f"{API}/api/courses/edit-data?courseId={hit['id']}") or {}).get("data", {})
    link = (course.get("courseLink") or "").strip()
    if not link:
        raise SystemExit(
            f"Course {code} ({hit.get('title','')}) has NO Courseware Link set on LMS-TMS, so "
            "there is no folder to push to.\nSet the Courseware Link on the course, or pass the "
            "folder explicitly:\n  gdrive_push.py <drive-folder-link> --repo <dir>")
    return link, code, hit.get("title", "")


def rc(args, root, parse=False, ok_codes=(0,)):
    cmd = ["rclone", *args, "--drive-root-folder-id", root]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode not in ok_codes:
        err = r.stderr.strip()
        if "couldn't fetch token" in err or "didn't find section" in err:
            raise SystemExit(f"rclone is not authorised yet.\nRun once:  rclone config create {REMOTE} drive scope=drive\n"
                             f"and complete the Google sign-in in the browser.\n\nrclone said: {err[:300]}")
        raise SystemExit(f"rclone {' '.join(args[:2])} failed: {err[:600]}")
    return json.loads(r.stdout or "[]") if parse else (r.stdout + r.stderr)


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def list_dirs(root, path=""):
    return rc(["lsjson", f"{REMOTE}:{path}", "--dirs-only"], root, parse=True)


def list_files(root, path):
    return rc(["lsjson", f"{REMOTE}:{path}", "--files-only", "--hash"], root, parse=True)


def find_or_create_dir(root, parent_path, canonical, hint, dry):
    dirs = list_dirs(root, parent_path)
    match = next((d for d in dirs if d["Name"].strip().lower() == canonical.lower()), None) \
        or next((d for d in dirs if hint in d["Name"].strip().lower()), None)
    if match:
        d = match
        return (f"{parent_path}/{d['Name']}" if parent_path else d["Name"]), d["Name"], False
    path = f"{parent_path}/{canonical}" if parent_path else canonical
    if not dry:
        rc(["mkdir", f"{REMOTE}:{path}"], root)
    return path, canonical, True


def ensure_archive(root, folder_path, dry):
    """Return <folder>/archive, creating it if absent and renaming any Archive/archives
    variant to the canonical lowercase 'archive'."""
    for d in list_dirs(root, folder_path):
        name = d["Name"]
        if not name.strip().lower().startswith("archiv"):
            continue
        if name == "archive":
            return f"{folder_path}/archive"
        print(f"    rename: {name}/  ->  archive/")
        if not dry:
            if name.lower() == "archive":  # case-only rename needs a two-step move
                rc(["moveto", f"{REMOTE}:{folder_path}/{name}", f"{REMOTE}:{folder_path}/__archive_tmp__"], root)
                rc(["moveto", f"{REMOTE}:{folder_path}/__archive_tmp__", f"{REMOTE}:{folder_path}/archive"], root)
            else:
                rc(["moveto", f"{REMOTE}:{folder_path}/{name}", f"{REMOTE}:{folder_path}/archive"], root)
        return f"{folder_path}/archive"
    print("    create: archive/")
    if not dry:
        rc(["mkdir", f"{REMOTE}:{folder_path}/archive"], root)
    return f"{folder_path}/archive"


def merge_old_versions(root, folder_path, archive_path, dry):
    """Merge any 'old versions'-style folder into archive/ (contents moved in,
    the emptied folder removed). Upload/move only — no file is ever deleted."""
    for d in list_dirs(root, folder_path):
        name = d["Name"]; low = name.strip().lower()
        if "old" in low and "version" in low:
            print(f"    merge:   {name}/  ->  archive/")
            if dry:
                continue
            for e in rc(["lsjson", f"{REMOTE}:{folder_path}/{name}"], root, parse=True):
                rc(["moveto", f"{REMOTE}:{folder_path}/{name}/{e['Name']}",
                    f"{REMOTE}:{archive_path}/{e['Name']}"], root)
            rc(["rmdir", f"{REMOTE}:{folder_path}/{name}"], root)


def push_folder(root, folder_path, files, dry):
    """Push files into folder_path. Unchanged files are kept in place; EVERY other
    pre-existing file in the folder (old versions, old names, Google-native docs)
    is moved to <folder>/archive first. Nothing is ever deleted."""
    archive_path = ensure_archive(root, folder_path, dry)
    merge_old_versions(root, folder_path, archive_path, dry)
    remote_files = list_files(root, folder_path)
    keep, to_upload = set(), []
    for path in files:
        fn = os.path.basename(path)
        same = next((f for f in remote_files if f["Name"] == fn), None)
        if same and (same.get("Hashes") or {}).get("md5") == md5(path):
            print(f"    unchanged: {fn} — skipped")
            keep.add(fn)
        else:
            to_upload.append(path)
    for f in remote_files:
        name = f["Name"]
        if name in keep:
            continue
        print(f"    archive: {name}  ->  archive/")
        if not dry:
            try:
                rc(["moveto", f"{REMOTE}:{folder_path}/{name}", f"{REMOTE}:{archive_path}/{name}"], root)
            except SystemExit as e:
                print(f"      WARNING: could not archive '{name}' — {str(e)[:200]}; continuing")
    for path in to_upload:
        fn = os.path.basename(path)
        print(f"    upload:  {fn}")
        if not dry:
            rc(["copyto", path, f"{REMOTE}:{folder_path}/{fn}"], root)
            link = rc(["link", f"{REMOTE}:{folder_path}/{fn}"], root).strip()
            print(f"      view link (anyone with the link): {link}")


def push_labs(root, labs_dir, dry):
    folder_path, real_name, created = find_or_create_dir(root, "", "Activities", "activit", dry)
    arch_name = "archive"
    excludes = {arch_name}
    if not created:
        # remember every archiv* variant so a pending (dry-run) rename can't leak
        # the old archive's contents into the sync plan
        excludes |= {d["Name"] for d in list_dirs(root, folder_path)
                     if d["Name"].strip().lower().startswith("archiv")}
        ensure_archive(root, folder_path, dry)
    print(f"  {real_name}{' (will be created)' if created else ''}:  syncing labs/ "
          f"(changed files only; replaced/removed files -> {real_name}/{arch_name}/)")
    args = ["sync", labs_dir, f"{REMOTE}:{folder_path}",
            "--backup-dir", f"{REMOTE}:{folder_path}/{arch_name}",
            "--exclude", ".DS_Store",
            "--checksum", "-v", "--stats-log-level", "NOTICE"]
    for e in excludes:
        args += ["--exclude", f"/{e}/**"]
    if dry:
        args.append("--dry-run")
    out = rc(args, root)
    moved, copied = [], []
    for line in out.splitlines():
        m = re.search(r"(?:INFO|NOTICE)\s*:\s*(.+?):\s*(Copied|Moved|Skipped copy|Skipped move)", line)
        if not m:
            continue
        name, action = m.group(1), m.group(2)
        (copied if "opy" in action or "opied" in action else moved).append(name)
    for name in sorted(set(moved)):
        print(f"    archive: {name}  ->  {arch_name}/")
    for name in sorted(set(copied)):
        print(f"    upload:  {name}")
    print(f"    labs sync: {len(set(copied))} file(s) uploaded, {len(set(moved))} archived "
          f"(unchanged files skipped automatically)")


def is_learner_guide(n):
    """The Learner Guide document, as opposed to the slide-deck PDF that also lives in the
    Learner Guide folder."""
    low = n.lower()
    return bool(re.match(r"^lg[-_ ]", low)) or ("learner guide" in low and "slide" not in low)


def print_link_block(root):
    """Emit the LMS-TMS link block for what is CURRENTLY in the folder (archive/ excluded),
    ensuring each file is 'anyone with the link can view'. Safe to run on an unchanged push,
    where nothing was re-uploaded and so no link was printed."""
    pdf = lambda n: n.lower().endswith(".pdf")

    def files_of(canonical, hint):
        dirs = list_dirs(root, "")
        d = (next((x for x in dirs if x["Name"].strip().lower() == canonical.lower()), None)
             or next((x for x in dirs if hint in x["Name"].strip().lower()), None))
        if not d:
            return None, []
        return d["Name"], rc(["lsjson", f"{REMOTE}:{d['Name']}", "--files-only"], root, parse=True)

    def link_for(folder, f):
        rc(["link", f"{REMOTE}:{folder}/{f['Name']}"], root)  # creates the reader permission
        return f"https://drive.google.com/file/d/{f['ID']}/view?usp=sharing"

    def one(canonical, hint, pred, label, prefer=None):
        folder, files = files_of(canonical, hint)
        hits = [f for f in files if pred(f["Name"])]
        if not hits:
            print(f"{label}: !! MISSING in '{canonical}'")
            return
        hits.sort(key=lambda f: (bool(prefer and prefer(f["Name"])), f.get("ModTime", "")), reverse=True)
        if len(hits) > 1:
            print(f"  ! {len(hits)} candidates in '{folder}' — using '{hits[0]['Name']}' "
                  f"(not: {', '.join(h['Name'] for h in hits[1:])})")
        print(f"{label}: {link_for(folder, hits[0])}   [{hits[0]['Name']}]")

    print("\n--- LMS-TMS link block ---")
    one("Master Trainer Slides", "master trainer", lambda n: n.lower().endswith(".pptx"),
        "Trainer Slide — PPT", prefer=lambda n: "master" in n.lower())
    one("Learner Guide", "learner guide", lambda n: pdf(n) and not is_learner_guide(n),
        "Learner Slide - PDF (get from LG folder)")
    one("Learner Guide", "learner guide", lambda n: pdf(n) and is_learner_guide(n), "LG - PDF")
    one("Lesson Plan", "lesson plan", pdf, "LP - PDF")
    folder, files = files_of("Assessment", "assess")
    qp = [f for f in files if f["Name"].lower().endswith(".docx")
          and not f["Name"].lower().startswith("answer")]
    if not qp:
        print("Assessment - DOCX: !! MISSING (no question paper .docx on Drive)")
    for f in sorted(qp, key=lambda f: f["Name"]):
        print(f"Assessment - DOCX: {link_for(folder, f)}   [{f['Name']}]")


def newest(pattern):
    hits = sorted((h for h in glob.glob(pattern)
                   if not os.path.basename(h).startswith("~$")), key=os.path.getmtime)
    return hits[-1] if hits else None


def resolve_root(repo, given, force):
    """The destination folder id.

    Precedence: an explicitly passed link > the LMS Courseware Link > the link recorded in
    the course .env by a previous push. The .env fallback exists because the LMS API needs
    an authenticated session and 401s in headless runs — without it a push that cannot
    reach the LMS has to be re-run by hand with the folder typed out.
    """
    lms_link = lms_id = None
    lms_err = None
    try:
        lms_link, code, title = courseware_link_from_lms(repo)
        lms_id = folder_id(lms_link)
        print(f"  LMS Courseware Link ({title or code}): {lms_link}")
    except SystemExit as e:
        lms_err = str(e).splitlines()[0]
        print(f"  ! could not read the Courseware Link from LMS-TMS — {lms_err}")

    env_link, env_id = courseware_link_from_env(repo)

    if not given:
        if lms_id:
            return lms_id
        if env_id:
            print(f"  using the Courseware Link recorded in .env: {env_link}")
            print("    (the LMS was unreachable; re-run once signed in to re-verify it)")
            return env_id
        raise SystemExit(
            (lms_err or "Could not resolve the Courseware Link from LMS-TMS.") +
            "\nNo COURSEWARE_LINK is recorded in the course .env either.\n"
            "Pass the folder link explicitly:\n"
            "  gdrive_push.py <drive-folder-link> --repo <dir>")

    given_id = folder_id(given)
    # Guard against pushing one course's material into another course's folder. The LMS is
    # the authority; .env stands in for it only when the LMS could not be read.
    ref_id, ref_src = (lms_id, "LMS") if lms_id else (env_id, ".env")
    if ref_id and given_id != ref_id and not force:
        raise SystemExit(
            f"The folder you passed is NOT the course's Courseware Link ({ref_src}):\n"
            f"  passed: {given_id}\n  {ref_src + ':':8}{ref_id}\n"
            "Refusing to push one course's material into another course's folder.\n"
            "Fix the Courseware Link on the course, or re-run with --force-folder if the "
            "folder you passed is genuinely the right one.")
    if ref_id and given_id != ref_id:
        print(f"  ! --force-folder: pushing to {given_id}, NOT the {ref_src} link {ref_id}")
    return given_id


def main():
    argv = sys.argv[1:]
    dry = "--dry-run" in argv
    force = "--force-folder" in argv
    repo = "."
    args = [a for a in argv if not a.startswith("--")]
    if "--repo" in argv:
        repo = argv[argv.index("--repo") + 1]
        args = [a for a in args if a != repo]

    print("Destination:")
    root = resolve_root(repo, args[0] if args else None, force)
    if not root:
        raise SystemExit("No Drive folder to push to.")

    # ALWAYS record the resolved folder in the course .env, so the next run still knows
    # where this course publishes even if the LMS API is unreachable. Skipped on a dry run
    # so a preview never writes to the repo.
    if not dry:
        link = f"https://drive.google.com/drive/folders/{root}"
        code = None
        try:
            code, _ = course_code_from_courseware(repo)
        except SystemExit:
            pass
        if write_env(repo, link, code=code):
            print(f"  recorded COURSEWARE_LINK in {env_path(repo)}")
        else:
            print(f"  COURSEWARE_LINK already current in {env_path(repo)}")

    if "--links-only" in argv:
        print_link_block(root)
        return

    cw = os.path.join(repo, "courseware")
    deck_ppt = newest(os.path.join(cw, "*v[0-9]*.pptx"))
    if not deck_ppt:
        raise SystemExit(f"No versioned slide deck found in {cw}")
    deck_pdf = os.path.splitext(deck_ppt)[0] + ".pdf"
    lg_docx = newest(os.path.join(cw, "LG-*.docx")); lg_pdf = newest(os.path.join(cw, "LG-*.pdf"))
    lp_docx = newest(os.path.join(cw, "LP-*.docx")); lp_pdf = newest(os.path.join(cw, "LP-*.pdf"))
    assessments = sorted(glob.glob(os.path.join(repo, "assessment", "*.docx")))

    routing = [
        ("Master Trainer Slides", "master trainer", [deck_ppt, deck_pdf]),
        ("Learner Guide", "learner guide", [lg_docx, lg_pdf, deck_pdf]),
        ("Lesson Plan", "lesson plan", [lp_docx, lp_pdf]),
        ("Assessment", "assess", assessments),
    ]
    print(f"Root folder: {root}{'  (DRY RUN — no changes will be made)' if dry else ''}")
    for canonical, hint, files in routing:
        files = [f for f in files if f and os.path.exists(f)
                 and not os.path.basename(f).startswith("~$")]
        if not files:
            print(f"  {canonical}: no local files found — skipped"); continue
        folder_path, real_name, created = find_or_create_dir(root, "", canonical, hint, dry)
        print(f"  {real_name}{' (will be created)' if created else ''}:")
        push_folder(root, folder_path, files, dry)

    labs_dir = os.path.join(repo, "labs")
    if os.path.isdir(labs_dir):
        push_labs(root, labs_dir, dry)
    else:
        print("  Activities: no labs/ folder found — skipped")
    if dry:
        print("Dry run complete — nothing was modified.")
        return
    print("Done.")
    print_link_block(root)


if __name__ == "__main__":
    main()
