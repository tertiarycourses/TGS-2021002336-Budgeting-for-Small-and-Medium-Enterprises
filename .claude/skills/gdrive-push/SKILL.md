---
name: gdrive-push
description: Push the current WSQ courseware (slides PPT/PDF, Learner Guide, Lesson Plan, assessments) to the course's Google Drive courseware folder — resolved automatically from the course's Courseware Link on lms-tms.tertiaryinfotech.com — auto-archiving old versions, then output a verified link block (Trainer Slide PPT / Learner Slide PDF / LG PDF / LP PDF / Assessment DOCX) for the LMS. Use when the user runs /gdrive-push or asks to upload/push courseware to Google Drive.
---

# GDrive Push — WSQ courseware to Google Drive

Uploads the course's current artifacts into the right subfolders of a Google Drive
courseware folder, moving all superseded files into an `archive` subfolder first.
**Upload-only: nothing on Drive is ever deleted.**

## Where the destination folder comes from — the LMS, then `.env`

**No folder link needs to be supplied.** The destination is resolved in this order:

1. **A link passed as the first argument** — wins over everything (see *Overriding* below).
2. **The LMS Courseware Link** — the course's `courseLink` field (DB `courseware_link`) read
   from `lms-tms.tertiaryinfotech.com` via `GET /api/courses/edit-data`, the same field
   `/lms-push` uses.
3. **`COURSEWARE_LINK` in the course `.env`** — the offline fallback (below).

The lookup is keyed on the **`TGS-` course code read out of the courseware itself** (the
deck cover / LG / LP text), never the repo folder name, so a renamed or copied repo cannot
publish one course's material into another course's Drive folder. If the courseware names
more than one course code, the script **aborts rather than guessing**.

```bash
python3 <skill-dir>/gdrive_push.py --repo "<course repo>" --dry-run   # folder auto-resolved
```

### The course `.env` — always written, used when the LMS is unreachable

**Every real push records the resolved folder in the course's `.env`** at the repo root:

```
COURSE_LINK=https://drive.google.com/drive/folders/<id>
COURSEWARE_LINK=https://drive.google.com/drive/folders/<id>
GDRIVE_FOLDER_ID=<id>
```

This matters because **the LMS API requires an authenticated session and returns
`401 Not authenticated` in headless, CI and non-interactive runs.** Without a local record,
such a run cannot resolve the folder at all and the operator has to retype the link every
time. With it, the push just works offline.

- The write is **idempotent** and **preserves every other key** in the file — re-running
  with the same link rewrites the same bytes and reports "already current".
- A **dry run never writes** `.env`.
- The **LMS still wins whenever it is reachable**; `.env` is only consulted as a fallback,
  so a Courseware Link corrected in the LMS is picked up on the next online run.
- The **cross-course guard still applies offline**: if a passed link disagrees with the
  `.env` link, the push is refused (naming `.env` as the source) unless `--force-folder`.
- `.env` holds an internal Drive link — keep it **gitignored**.

**Overriding the folder.** A link passed as the first argument wins, but if it disagrees
with the reference link (the LMS when reachable, otherwise `.env`) the script aborts and
prints both ids; re-run with `--force-folder` only if the passed folder is genuinely
correct. Use the override when the course is not in the LMS yet, or when pushing to a
scratch/handover folder.

Only if **all three** sources are empty — no link passed, LMS unreachable, and no
`COURSEWARE_LINK` in `.env` — ASK the user for the folder link (AskUserQuestion) rather
than falling back to a remembered or previously used folder.

## Routing

| Drive subfolder (created if missing) | Files pushed |
|---|---|
| Master Trainer Slides | slide deck `.pptx` + `.pdf` (current version only) |
| Learner Guide | `LG-*.docx` + `LG-*.pdf` + the slides `.pdf` |
| Lesson Plan | `LP-*.docx` + `LP-*.pdf` |
| Assessment | all `assessment/*.docx` (WA + PP papers and answer keys) |
| Activities | the whole `labs/` tree (structure preserved) |

**Change detection — only changed files are pushed.** Every file's MD5 is compared
with the Drive copy first; identical files are skipped (no re-upload, no archiving).
The labs sync uses `rclone sync --checksum --backup-dir Activities/archive`, so
unchanged lab files are skipped and replaced/removed ones are MOVED to the archive,
never deleted.

**Archiving — each courseware folder ends up holding ONLY the current files.**
Before uploading, EVERY pre-existing file that is not identical to a pushed file —
old versions, differently-named old decks, Google-native Docs/Slides — is MOVED
server-side into that folder's `archive/` subfolder. The archive folder is
**created if absent**, and any existing `Archive`/`archives` variant is **renamed
to the canonical lowercase `archive`** (case-only renames via a two-step move).
Any **"old versions"-style folder is MERGED into `archive/`** — its contents are
moved in server-side and the emptied folder is removed.
A file that cannot be moved is reported as a WARNING and skipped, never deleted.
Target subfolders are matched case-insensitively (an existing "Assessments" folder
is reused, not duplicated).

Every uploaded file is then set to **"anyone with the link can view"** (via
`rclone link`, which creates the reader permission) and its view link is printed —
include the links in the report to the user.

A real push **ends by printing the LMS-TMS link block** for whatever is currently in the
folder. Emit it on demand (without pushing) with `--links-only` — needed whenever a push
uploaded nothing because every file was unchanged, since `rclone link` is only printed for
files that were actually uploaded:

```bash
python3 -u <skill-dir>/gdrive_push.py --repo "<repo>" --links-only
```

## How to run

```bash
python3 -u <this-skill-dir>/gdrive_push.py --repo "<course repo>" --dry-run   # preview (folder from the LMS)
python3 -u <this-skill-dir>/gdrive_push.py --repo "<course repo>"             # real push
python3 -u <this-skill-dir>/gdrive_push.py "<link>" --repo "<repo>" --force-folder   # override the LMS folder
```

Always run `--dry-run` first and show the user the plan (including which folder the LMS
resolved to); then do the real push. Report per-folder what was archived and uploaded.

**Run the real push in the BACKGROUND** (`run_in_background: true`) and use `python3 -u`:
a full labs sync routinely exceeds the 10-minute foreground Bash timeout, and buffered
output is lost when the call is killed. The push is checksum-based and upload-only, so a
killed run is safely resumed by simply re-running it — unchanged files are skipped.

## FINAL STEP — LMS-TMS link block + link check

After the real push, ALWAYS end with an LMS-ready link block for
`lms-tms.tertiaryinfotech.com`, in EXACTLY this format (one artifact per line,
its "anyone with the link" view link appended):

```
Trainer Slide — PPT: <link to the current slides .pptx in Master Trainer Slides>
Learner Slide - PDF (get from LG folder): <link to the slides .pdf inside the Learner Guide folder>
LG - PDF: <link to LG-*.pdf>
LP - PDF: <link to LP-*.pdf>
Assessment - DOCX: <link(s) to the assessment .docx question papers>
```

Note the **Learner Slide PDF is the copy in the Learner Guide folder** (not the
Master Trainer Slides one). These links are what gets pasted into the course page
on lms-tms.tertiaryinfotech.com.

Then do a **final link check** before reporting done — for every link in the block:

1. Verify it resolves (e.g. `rclone lsjson --drive-root-folder-id ... ` by file id,
   or fetch the link and confirm it is not a 404/permission page).
2. Confirm it points to the RIGHT file — correct file name, correct extension
   (PPT vs PDF vs DOCX), and the CURRENT version (not an archived one).
3. Confirm sharing is "anyone with the link can view".

Report the check result per link (✓/✗). If any link fails, fix it (re-share or
re-link the correct file) and re-check before finishing.

## Transport / prerequisites

The script talks to Google Drive **directly via rclone** (remote name `gdrive`,
override with env `GDRIVE_REMOTE`). All Drive operations are upload (`copyto`) or
server-side move to Archive (`moveto`) — there is no delete anywhere.

- One-time setup if the remote is missing: `brew install rclone` then
  `rclone config create gdrive drive scope=drive` and complete the Google sign-in
  in the browser (use the account that owns the courseware folder).
- The `--drive-root-folder-id` flag scopes every call to the user-supplied folder,
  so the script cannot touch anything outside it.
