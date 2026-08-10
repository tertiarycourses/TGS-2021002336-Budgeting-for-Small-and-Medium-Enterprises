---
description: Update the course on lms-tms.tertiaryinfotech.com — set the Trainer Slides / Learner Slides / Learner Guide / Lesson Plan / Activities-Lab URLs from the course's Google Drive folder, and attach the assessment. QUESTION PAPERS ONLY (WA + PP/CS); the answer keys are trainer-only and never reach the LMS.
argument-hint: [course-code | drive-folder-link]   (both optional — resolved from the repo + the LMS)
---

# /tms-push — push the courseware links + assessment to the LMS/TMS

Write this course's Google Drive links into its course record on **lms-tms.tertiaryinfotech.com**.

**It links what is on Drive — it uploads nothing.** If the repo has a newer build than Drive, the LMS keeps showing old material and the push still reports success. So confirm the Drive files ARE the current build; if not, run **`/gdrive-push`** first. The chain is **`/courseware-gen` → `/courseware-qa` → `/gdrive-push` → `/tms-push`**.

**Optional argument:** `$ARGUMENTS` — a course code (`TGS-…`) and/or a Drive folder link. Both are normally resolved automatically: the course code from the repo, the Drive folder from the course's own **Courseware Link** field on the LMS. Supply one only to override.

## HARD RULES

1. **QA must pass first.** Run **`/courseware-qa`** — **do not push on a failing audit.**
2. **The course code is read from the courseware itself** (deck cover / LG / LP) and must match the course being written to. **A mismatch is a hard abort** — this is a live write to a production course page, and a wrong code silently overwrites a real course.
3. **ASSESSMENT: QUESTION PAPERS ONLY — NEVER THE ANSWER KEYS.** See below.
4. **Dry-run first, always.**

## API auth

The push goes through the **LMS-TMS REST API** (`GET /api/courses/list`, `GET /api/courses/edit-data`, `PUT /api/courses/update-course`), which requires the machine service key (`EXTERNAL_API_KEY_FOR_CLAWDBOT` in ai-lms-tms) in the `x-api-key` header. The scripts resolve the key automatically, in this order:

1. **Shell env** — `LMS_TMS_API_KEY`
2. **Project level** — `./.claude/lms_tms_api_key` (plain key file), or `LMS_TMS_API_KEY=…` in `./.claude/.env` / `./.env`
3. **User level** — `~/.claude/lms_tms_api_key`, or `LMS_TMS_API_KEY=…` in `~/.claude/.env`

If every source is empty the API returns **401** — stop and ask the user for the service key, then store it at the **user level** (`~/.claude/lms_tms_api_key`, `chmod 600`) so every course repo can push, or at the **project level** for a repo-specific key. **A project-level key file is a credential: it must be gitignored and is never pushed to GitHub.**

## Steps

1. **Run the pusher** from the course repo root — the script lives in `.claude/scripts/` (project) or `~/.claude/scripts/`:
   ```bash
   python3 <scripts-dir>/lms_push.py --dry-run   # preview — always
   python3 <scripts-dir>/lms_push.py             # real push + verify
   ```
   Add `--course-code TGS-…` / `--drive-folder <link>` only if `$ARGUMENTS` overrides them.
2. **Show the dry-run plan** — the resolved LMS course (title + code), the Drive folder read from the Courseware Link, and per field the **old → new** URL:

   | LMS-TMS field | Source file on Drive |
   |---|---|
   | Trainer Slides URL | the `.pptx` in **Master Trainer Slides** |
   | Learner Slides URL | the `.pdf` with "slide" in its name in **Learner Guide** (not the trainer folder) |
   | Learner Guide URL | the `.pdf` without "slide" in its name in **Learner Guide** |
   | Lesson Plan URL | the `.pdf` in **Lesson Plan** |
   | **Activities/Lab URL** | the **Activities** FOLDER itself (the labs are a tree, not one file) |
   | **Written Assessment** | the **WA (SAQ) question paper** — `WA (SAQ) - <Title> - <VER>.docx` |
   | **Practical Performance** *or* **Case Study** | the **PP** *or* **CS** question paper — whichever instrument this course uses |

   **Question-paper filenames the resolver accepts.** House naming varies between courses, and a
   paper the resolver does not recognise is reported as *missing* — so the LMS silently keeps
   serving the old document. Both spellings of each instrument resolve:
   - **Case Study** — `Case Study …`, `… (CS) …`, or a leading `CS ` (e.g. `CS Assessment - <Title> - <VER>.docx`).
   - **Practical Performance** — `Practical Performance …`, `Practical Test …`, `… (PP) …`, or a leading `PP `.

   If the script reports it passed over other candidate files, surface that — it is how a stale deck gets caught.
3. **If a PDF is missing**, the script aborts and names the field. Do not invent a link and do not silently fall back to the `.docx`. Tell the user, and offer to convert the newest DOCX in that Drive folder to PDF and upload it, or re-run with `--allow-missing` to set only the found fields.
   To write **one** verified field while others are still blocked on QA, use `--only <field>` (repeatable, e.g. `--only activitiesUrl`) — every field not listed keeps its current LMS value rather than being blanked.
4. **Confirm the course is the right one**, then push for real.
5. The script re-reads the course afterwards and prints ✓/✗ per URL, plus a check that no other column was blanked. **Report that verification; never claim success on a ✗.**

## Where the assessment actually lives on the LMS

The LMS stores each instrument **twice**, and the course page renders the **`assessmentMethods`** entry — so **both** must be written, or the page keeps showing the old document even though the flat column looks updated:

| Instrument | Flat column | `assessmentMethods` entry |
|---|---|---|
| Written Assessment | `writtenAssessmentLink` | `writtenAssessment` → `{link, enabled: true}` |
| Case Study | *(none — lives only in `assessmentMethods`)* | `caseStudy` → `{link, enabled: true}` |
| Practical Performance | `practicalPerformanceAssessmentLink` | `practicalExam` → `{link, enabled: true}` |

A course has **exactly one** practical instrument. Set the one it has and **clear the other** (`{link: "", enabled: false}`) — otherwise a stale PP link survives on a Case Study course, which is precisely how the LMS ends up serving the wrong paper. `lms_push.py` does this automatically from whichever question paper it finds on Drive, and aborts if it finds both.

Note the LMS **normalises Drive URLs** (it strips `?usp=sharing`), so verify by **file ID**, not by string equality.

## The answer-key rule

**Any file named `Answer to …` / `Answers to …` is trainer-only.** It stays in the Google Drive courseware folder and is **never** attached to the LMS, **never** placed on a learner-visible field, and **never** pushed to GitHub. Filter before attaching:

```bash
# the ONLY two files eligible for the LMS
ls assessment/*.docx | grep -viE '/(Answer|Answers) to '
```

If that yields anything other than **the WA paper plus exactly one PP/CS paper**, **stop and ask the user** — do not guess which file to attach.

## Report

State the courseware links that were set, **which two question papers** were attached, and confirm explicitly that the **answer keys were withheld** as trainer-only.
