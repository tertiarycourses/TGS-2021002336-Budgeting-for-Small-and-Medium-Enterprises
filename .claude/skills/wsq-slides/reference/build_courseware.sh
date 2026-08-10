#!/usr/bin/env bash
# Single-command aligned build of all AZ-104 courseware from the single source
# (course_data.py + data_domainN.py). Produces in courseware/: the PPT, LP and
# LG as DOCX + PDF, with page-numbered Tables of Contents in the LP/LG PDFs.
#
# Pipeline: run the python-pptx / python-docx generators, render to PDF with
# LibreOffice, inject a static page-numbered TOC (LibreOffice can't update the
# TOC field headless), then re-render the LP/LG PDFs.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
CW="$REPO/courseware"
SOFFICE="${SOFFICE:-soffice}"

echo "==> Generate PPT / LP / LG from the single source"
python3 "$HERE/build_slides.py"
python3 "$HERE/build_lesson_plan.py"
python3 "$HERE/build_learner_guide.py"

PPT="$(ls -t "$CW"/*.pptx | head -1)"
LP="$CW/LP-Microsoft Azure Administrator (AZ-104).docx"
LG="$CW/LG-Microsoft Azure Administrator (AZ-104).docx"

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
