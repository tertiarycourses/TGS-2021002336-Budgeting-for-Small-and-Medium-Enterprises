---
description: Install or update the WSQ courseware toolchain (skills, commands, the courseware-qa agent, the push scripts and the three hooks) in this project or at user level, from github.com/tertiarycourses/wsqskills. Never overwrites a course-customised generator.
argument-hint: [--user] [--force] [--ato]
---

# /wsq-setup — install / update the WSQ toolchain

Bring the WSQ courseware toolchain up to date from the single source of truth: <https://github.com/tertiarycourses/wsqskills>.

**Arguments:** `$ARGUMENTS`

| Flag | Effect |
|---|---|
| *(none)* | install into **this course repo** (`./.claude`) — the usual case |
| `--user` | install into **`~/.claude`** (available in every project) |
| `--force` | overwrite files that already exist — **careful**, this can clobber a course-customised generator |
| `--ato` | also install the ATO-only skills (`create-tms-ato`, `gdrive-push-ato`) — a normal course repo does not want these |

## Run

```bash
npx github:tertiarycourses/wsqskills $ARGUMENTS
```

If `npx` is unavailable, clone and run the installer directly:

```bash
git clone https://github.com/tertiarycourses/wsqskills /tmp/wsqskills
node /tmp/wsqskills/bin/install.js $ARGUMENTS
```

## What it installs

- **Skills** — `courseware-build`, `wsq-slides`, `wsq-lesson-plan`, `wsq-learner-guide`, `wsq-assessment`, and the `tertiary-*` generators + design system.
- **Commands** — `/courseware-gen`, `/assessment-gen`, `/courseware-qa`, `/gdrive-push`, `/tms-push`, `/wsq-setup`.
- **Agent** — `courseware-qa`.
- **Scripts** — `gdrive_push.py`, `lms_push.py` (used by the push commands).
- **Hooks** — `courseware-pre-hook.py`, `courseware-post-hook.py`, `courseware-tms-push-hook.py` — and it registers all three in `settings.json`.

## Rules

- **Existing files are never overwritten** unless `--force` is passed. A course repo often carries a generator customised for *that* course; clobbering it destroys work. The installer reports what it skipped.
- **ATO skills are opt-in** (`--ato`) — an ordinary course is not an ATO submission.
- After installing, verify with **`/courseware-qa`**.

## The pipeline

`/courseware-gen` → `/assessment-gen` → `/courseware-qa` → `/gdrive-push` → `/tms-push`
