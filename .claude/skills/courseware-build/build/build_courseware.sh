#!/usr/bin/env bash
# Single-command aligned build of the WSQ courseware from the single source
# (course_data.py + data_domainN.py). Produces in the course's courseware/: the
# PPT, LP and LG as DOCX + PDF, with page-numbered Tables of Contents in LP/LG.
#
# Generic: the course repo and the LP/LG filenames are derived from
# course_data.py, so this orchestrator is course-agnostic. Override the target
# repo with the COURSE_REPO environment variable.
#
# Pipeline: run the python-pptx / python-docx generators, render to PDF with
# LibreOffice, inject a static page-numbered TOC (LibreOffice can't update the
# TOC field headless), then re-render the LP/LG PDFs.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
SOFFICE="${SOFFICE:-soffice}"

# Resolve the course repo + short title from the single source (course_data.py).
IFS=$'\t' read -r REPO SHORT <<< "$(python3 - "$HERE" <<'PY'
import os, sys
here = sys.argv[1]; sys.path.insert(0, here)
import course_data as C
def find_repo(start):
    env = os.environ.get("COURSE_REPO")
    if env and os.path.isdir(env): return env
    d = start
    for _ in range(8):
        d = os.path.dirname(d)
        if os.path.isdir(os.path.join(d,"courseware")) and os.path.isdir(os.path.join(d,"labs")): return d
    return os.path.dirname(os.path.dirname(start))
print(find_repo(here) + "\t" + C.SHORT_TITLE)
PY
)"
CW="$REPO/courseware"

echo "==> Generate PPT / LP / LG from the single source"
python3 "$HERE/build_slides.py"
python3 "$HERE/build_lesson_plan.py"
python3 "$HERE/build_learner_guide.py"

PPT="$(ls -t "$CW"/*.pptx | head -1)"
LP="$CW/LP-$SHORT.docx"
LG="$CW/LG-$SHORT.docx"

echo "==> Render PDFs (pass 1)"
"$SOFFICE" --headless --convert-to pdf --outdir "$CW" "$PPT" >/dev/null 2>&1
"$SOFFICE" --headless --convert-to pdf --outdir "$CW" "$LP"  >/dev/null 2>&1
"$SOFFICE" --headless --convert-to pdf --outdir "$CW" "$LG"  >/dev/null 2>&1

echo "==> Inject page-numbered Table of Contents (LP + LG)"
python3 "$HERE/inject_toc.py" "$LP" "${LP%.docx}.pdf" 2
python3 "$HERE/inject_toc.py" "$LG" "${LG%.docx}.pdf" 2

echo "==> Render PDFs (pass 2 — with built TOC)"
"$SOFFICE" --headless --convert-to pdf --outdir "$CW" "$LP" >/dev/null 2>&1
"$SOFFICE" --headless --convert-to pdf --outdir "$CW" "$LG" >/dev/null 2>&1

echo "==> Done. Artifacts in courseware/:"
ls -1 "$CW"/*.pptx "$CW"/*.docx "$CW"/*.pdf
