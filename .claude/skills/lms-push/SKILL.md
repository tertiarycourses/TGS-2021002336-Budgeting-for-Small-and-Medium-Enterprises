---
name: lms-push
description: Push the current courseware's Google Drive links into the course record on lms-tms.tertiaryinfotech.com via its API — sets Trainer Slides URL (PPT from Master Trainer Slides), Learner Slides URL (slide PDF from Learner Guide), Learner Guide URL (LG PDF) and Lesson Plan URL (LP PDF). The Drive folder is read from the course's own Courseware Link field via the API. Use when the user runs /lms-push or asks to update/sync the LMS-TMS course links.
---

# LMS Push — Google Drive courseware links → LMS-TMS

Runs *after* `/gdrive-push`. It reads what is currently in the course's Google Drive
folder, takes each file's "anyone with the link can view" URL, and writes those URLs into
the course record on `lms-tms.tertiaryinfotech.com` — so nobody has to paste links into
the Courseware form by hand.

## It links what is ON DRIVE — not what is in the repo

This is the failure mode that looks like "the command didn't work": the LMS still shows
old material even though the push reported success. It linked Drive faithfully; **Drive
was stale.** `/lms-push` never uploads anything.

So the chain is always **build → `/gdrive-push` → `/lms-push`**. Before pushing links,
sanity-check that the Drive files are the current build (version in the filename, modified
date) — and if the repo has newer artifacts, run `/gdrive-push` first. Note `/gdrive-push`
expects PDFs (deck, LG, LP) that the build does not produce; generate them first:

```bash
cd <repo>/courseware
soffice --headless --convert-to pdf --outdir . *.pptx *.docx   # skip ~$ lock files
```

## Course code — taken from the courseware, not the folder name

The code is read out of the **deck cover / LG / LP** themselves (the `TGS-…` in their
text). It is cross-checked against the repo folder name and any `--course-code`, and any
disagreement is a hard abort — a renamed or copied repo folder must never be able to
publish one course's material onto another course's LMS record.

## Where the Drive folder comes from

**From the LMS itself** — the course's **Courseware Link** field (`courseLink`, DB
`courseware_link`), read via `GET /api/courses/edit-data`. No folder link needs to be
supplied. Pass `--drive-folder <link>` only to override it; if the course has no Courseware
Link set, the script stops and says so rather than guessing.

## Field mapping

| LMS-TMS form field | Payload key | Source on Google Drive |
|---|---|---|
| Trainer Slides URL | `trainerSlidesUrl` | the `.pptx` in **Master Trainer Slides** (prefers the one named `*Master*` over a trainer-personalised copy) |
| Learner Slides URL | `slidesUrl` | the `.pdf` **with "slide" in its name** in **Learner Guide** |
| Learner Guide URL | `learnerGuideUrl` | the `.pdf` **without "slide" in its name** in **Learner Guide** |
| Lesson Plan URL | `lessonPlanUrl` | the `.pdf` in **Lesson Plan** |
| Written Assessment URL | `writtenAssessmentLink` | the **WA / SAQ question paper `.docx`** in **Assessment** |
| Practical Performance URL | `practicalPerformanceAssessmentLink` | the **PP / Case Study question paper `.docx`** in **Assessment** |

**The ANSWER KEYS are never linked.** "Answer to …" / marking-guide documents are trainer-only;
`is_answer_key()` filters them out, so only the two question papers reach the LMS.

**Why the assessment links matter.** They were originally left out, and the result is a silent
failure: after an assessment revision the LMS keeps serving the PREVIOUS version's paper. The old
link still resolves — `gdrive-push` **archives** the superseded file rather than deleting it — so
nothing looks broken while learners sit the wrong paper. Always fetch each link afterwards and read
the served filename/version; do not trust a 200.

Where several files match, the newest by modified time wins and the script prints which
ones it passed over — read that line, it is how you catch a stale deck being linked.

Note the key mismatch: the field labelled *Learner Slides URL* is `slidesUrl` in the
payload and `slides_url` in the DB. `trainerSlidesUrl` is the separate PPT field.
Facilitator Guide URL and Assessment Plan URL are **not touched**.

## When a PDF is missing

Real courseware folders often hold only the `.docx` for the Learner Guide / Lesson Plan.
The script does **not** invent a link: it lists every field it could not fill and aborts.
Two ways forward:

- Produce the PDF, then re-run. To convert what is already on Drive:
  ```bash
  rclone copyto "gdrive:Lesson Plan/<name>.docx" "<tmp>/<name>.docx" --drive-root-folder-id <folder-id>
  soffice --headless --convert-to pdf --outdir <tmp> "<tmp>/<name>.docx"
  rclone copyto "<tmp>/<name>.pdf" "gdrive:Lesson Plan/<name>.pdf" --drive-root-folder-id <folder-id>
  ```
  Check the converted PDF's page count and cover page before uploading — LibreOffice can
  silently mangle a bad DOCX.
- Or re-run with `--allow-missing` to set only the fields that were found; the rest keep
  their current LMS value.

## How to run

```bash
python3 <this-skill-dir>/lms_push.py --dry-run   # preview (folder comes from the LMS)
python3 <this-skill-dir>/lms_push.py             # real push + verify
```

Always `--dry-run` first and show the user the old → new URL diff, then do the real push.
Override the course code with `--course-code` (it must still match the courseware), and
point at a different instance with `LMS_TMS_API` (default
`https://lms-tms.tertiaryinfotech.com`).

After the real push the script re-reads the course from the API **and fetches every link**,
confirming each one returns HTTP 200, is anyone-with-link public, and serves the expected
filename. A ✗ on any line means the course page is wrong — never report success over it.

Watch for **duplicate filenames on Drive** (Drive allows them). `/gdrive-push` archives by
name and can leave one instance of a same-named old file behind, which then looks like a
valid current file. If the verification names a file you did not expect, list the folder
and move the stray into `archive/` before re-running.

## How it talks to the API (and why it is careful)

Three calls against the Next.js API in `~/projects/tertiary/ai-lms-tms`:

1. `GET /api/courses/list` — resolve the course code (e.g. `TGS-2020505042`) to its UUID.
2. `GET /api/courses/edit-data?courseId=<uuid>` — read the **full** course object.
3. `PUT /api/courses/update-course?courseId=<uuid>` — `multipart/form-data` with one text
   field, `courseData` = the JSON of that full object with the four URLs replaced.

**Read-modify-write is mandatory, not a style choice.** `update-course` is *not* a partial
update: only the six courseware-URL columns are `COALESCE`d — every other column
(`title`, `course_code`, `training_hours`, `course_fee`, `trainers_list`, …) is assigned
unconditionally, so any key missing from `courseData` lands in the DB as `NULL`. It also
**deletes and recreates** the course's learning units and re-syncs its assessments from the
payload. Sending a four-key patch would gut the course record. The script therefore
mirrors `CourseEditor.tsx`'s payload exactly (incl. `topics` → `learningUnits` with
positions, `assessments` with `action: 'update'`, `isLeaderboardEnabled` → `isGamified`),
refuses to PUT if the read-back object is empty or has no `title`/`courseCode`, and
re-reads the course afterwards to verify the four URLs — and that nothing was blanked.

**Auth:** these endpoints require none (no key, no cookie). That means a typo in the course
code writes to a real, live course — hence the dry-run-first rule. It also means the prod
write endpoint is unauthenticated; worth raising with whoever owns the LMS.

## Prerequisites

Same rclone setup as `gdrive-push` (remote `gdrive`, override with `GDRIVE_REMOTE`):
`rclone config create gdrive drive scope=drive`. The script only *reads* Drive and creates
reader permissions — it never moves, uploads, or deletes anything there.
