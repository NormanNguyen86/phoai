# PhoAI Project Management Handbook

How PhoAI (an AI photography tutor that gives evidence-grounded critiques) is organised, versioned, tested, released and developed with AI assistance. The goal is a project that is reproducible, small-step and honest about what works.

## Contents

1. Principles
2. Roadmap: infrastructure grows with the product
3. Repository layout
4. Git workflow
5. Versioning and release checklist
6. Keeping each version's scope under control
7. Data, prompts and evaluation
8. Docker, database, CI/CD and environments
9. Working with Claude on this project
10. Templates
11. Management cadence

---

## 1. Principles

1. **Everything lives in git**, except secrets, large data and model weights. Servers only run what is in git; nobody edits a server by hand.
2. **Prompts are code.** They are versioned, have a changelog, and every change is checked by evaluation.
3. **Small steps.** One pull request does one thing; one release has one theme.
4. **"Better" needs numbers.** Every release ships an evaluation report compared with the previous version.
5. **When behind schedule, cut scope**, not quality checks.
6. **The author understands every module.** AI assistance speeds work up; it does not replace understanding (see section 9).

## 2. Roadmap: infrastructure grows with the product

Infrastructure is added when a version needs it, not in advance.

| Version | Theme | Infrastructure added |
|---|---|---|
| v0.1 | Critique runs on a handful of images, outputs validated JSON | Repo, `.env`, `pyproject.toml`, YAML config, structured logs |
| v0.2 | First measurements | `evals/` harness, pytest, pre-commit, result cache |
| v0.3 | Grounding and evidence verification | Versioned runs, feature flags, smoke test |
| v0.5 | Public demo | Gradio app, Hugging Face Spaces + secrets, spend limits, Docker, GitHub Actions |
| v0.8 | Backend service | FastAPI, PostgreSQL, Docker Compose, staging/production |

## 3. Repository layout

```
phoai/
├── CLAUDE.md               # project memory for Claude Code (section 9)
├── README.md               # problem, architecture, how to run, results, demo link
├── CHANGELOG.md
├── pyproject.toml          # dependencies + project version (managed with uv)
├── .env.example            # variable names only, never real values
├── .gitignore              # .env, data/raw/, runs/, cache/, __pycache__/
├── config/default.yaml     # model_id, temperature, paths (no secrets)
├── prompts/
│   ├── critique_v1.md
│   ├── critique_v2.md
│   └── CHANGELOG.md        # what changed in each prompt and why
├── src/phoai/
│   ├── critique.py         # image -> model -> validated JSON
│   ├── schema.py           # pydantic models (the data contract)
│   ├── grounding.py        # evidence phrase -> box / mask
│   ├── verify.py           # evidence verification
│   └── pipeline.py         # one command end to end
├── evals/
│   ├── run.py              # python -m evals.run
│   ├── human_labels/       # hand-labelled data (committed)
│   └── reports/            # v0.2.md, v0.3.md, model-comparison.md
├── tests/                  # unit tests (mocked API) + slow end-to-end test
├── data/
│   ├── README.md           # sources, licences, counts, naming convention
│   ├── manifest.csv        # file list + sha256
│   ├── annotations.csv     # small text file, committed
│   └── raw/                # images, NOT committed
├── runs/                   # outputs of each run, NOT committed
├── notebooks/              # experiments, kept out of src/
├── docs/
│   ├── PROJECT_MANAGEMENT.md   # this file
│   ├── spec-v0.1.md, schema.md, annotation-guide.md
│   ├── failure-cases.md, failure-taxonomy.md
│   ├── devlog.md           # one short entry per week
│   ├── adr/                # architecture decision records
│   └── img/
├── app.py                  # Gradio UI (v0.5); only calls the pipeline
├── Dockerfile, .dockerignore
├── .github/
│   ├── workflows/ci.yml
│   └── pull_request_template.md
└── .claude/
    ├── settings.json       # permissions for Claude Code
    └── skills/             # project skills (section 9.4)
```

## 4. Git workflow

### 4.1 Branches
- `main` is always runnable and protected: pull request required; from v0.5 also required status checks.
- One short-lived branch per task: `feat/critique-cli`, `feat/grounding`, `fix/json-retry`, `prompt/v2`, `docs/readme-v05`. Delete after merging.

### 4.2 Conventional Commits
```
feat: add critique.py to read an image and save JSON
fix: retry when the model returns invalid JSON (Fixes #7)
prompt: v2 asks for more specific evidence phrases
eval: add per-dimension precision/recall
docs: README run instructions for v0.1
test: unit tests for schema
chore: update .gitignore
```
One idea per commit. `Fixes #N` closes the issue on merge.

### 4.3 Pull requests, even when working alone
A PR is where the whole diff gets re-read once before merging, the checklist in the PR template is filled in, and (from v0.5) CI must pass.

### 4.4 Tags and releases
```bash
git tag -a v0.1.0 -m "v0.1.0: critique on a first image set"
git push origin v0.1.0
```
Then create a GitHub Release from the tag and paste the matching CHANGELOG entry.

### 4.5 Never commit
`.env`, API keys, `data/raw/`, `runs/`, `cache/`, model weights, notebook checkpoints. If a key is ever committed, **revoke it immediately**: deleting it from git is not enough because it stays in history.

## 5. Versioning and release checklist

### 5.1 Semantic Versioning `MAJOR.MINOR.PATCH`
- `0.x.y` means the product is not yet stable.
- Bump MINOR for new features (`0.2.0 → 0.3.0`), PATCH for fixes only (`0.3.0 → 0.3.1`).
- Three more things are versioned separately and **stored with every result**, so any output can be traced back:
  - `prompt_version` (e.g. `critique_v2`)
  - `model_id` (the exact model name)
  - `schema_version` (shape of the JSON output)

### 5.2 Release checklist (paste into the release PR)

**Code and configuration**
- [ ] `version` in `pyproject.toml` bumped
- [ ] `.env.example` lists every new variable
- [ ] Dependencies pinned, lock file updated
- [ ] (v0.8+) database migrations tested on staging

**AI**
- [ ] `prompts/CHANGELOG.md` updated if prompts changed
- [ ] Evaluation run; `evals/reports/vX.Y.md` compares against the previous version
- [ ] Cost per image and average latency recorded

**Documentation**
- [ ] `CHANGELOG.md` has an `[X.Y.0]` entry (Added / Changed / Fixed / Removed)
- [ ] README updated (how to run, results, demo link)
- [ ] New ADR if an architectural decision was made

**Release**
- [ ] Smoke test passed (end-to-end on 3 images)
- [ ] Rollback path known (previous tag)
- [ ] `git tag vX.Y.0` + GitHub Release
- [ ] Current milestone closed, next milestone created (at most 8 issues)

## 6. Keeping each version's scope under control

Scope creep is the most common failure of solo projects. Rules against it:

1. **One theme per version** (section 2). Off-theme ideas go to the Backlog.
2. **At most 8 issues per milestone.** Once full, new issues wait for the next milestone.
3. **"Done" criteria are frozen up front** in a one-page spec.
4. **Fixed release dates.** On the date, ship what is done; move the rest to the next version with a written reason, or drop it.
5. **Never mix refactoring, new features and bug fixes** in one PR.
6. **Feature flags** for unfinished larger features (e.g. `verify_evidence: false` in config): code can merge to `main` while the feature stays off.
7. **Feedback on a tagged version never changes that version.** It becomes issues for a later milestone.

Kanban board (GitHub Projects):

| Column | Meaning |
|---|---|
| Backlog | Ideas, not in any milestone |
| To do | In the current milestone |
| In progress | Being worked on (**at most 2 cards**) |
| Done | Merged to `main` |

Labels: `bug`, `prompt`, `eval`, `data`, `grounding`, `ui`, `infra`, `docs`.

## 7. Data, prompts and evaluation

### 7.1 Data
- Images stay out of git (`data/raw/` plus an off-repo backup). Git holds `manifest.csv` (filename + sha256) and `annotations.csv`.
- Public datasets: record **source and licence** in `data/README.md` and download with a script; do not commit images.
- The annotation guide is versioned; if it changes mid-way, record the date and reason.
- Photos from other people need their consent before being stored or used as data.

### 7.2 Prompts
- Each version is its own file; **old versions are never deleted**.
- `prompts/CHANGELOG.md` entry format: `v2 (20/11): evidence_phrase must be a concrete noun phrase — fixes #7, #9`.

### 7.3 Every run is reproducible
Each run creates `runs/<run_id>/` containing the config used, `prompt_version`, `model_id`, `git_sha`, the output JSON and `log.jsonl` (latency, tokens, cost).

### 7.4 The evaluation harness: "unit tests" for AI
- One command: `python -m evals.run --run runs/<run_id>`.
- Fixed metrics measured for **every** release: valid-JSON rate, stability across 3 runs, per-dimension precision/recall, claim–evidence rate, cost per image, latency. From v0.3: an image-shuffle control.
- After changing a prompt or model, re-run and compare with the baseline. **If it is worse, it does not ship.**
- Any number quoted outside the repo (README, CV) must trace back to a file in `evals/reports/`.

## 8. Docker, database, CI/CD and environments

### 8.1 Environments

| Environment | v0.1–v0.5 | v0.8+ |
|---|---|---|
| Local | Developer machine, `uv run` | `docker compose up` |
| Staging | none (private Space if needed) | VPS, identical to production |
| Production | Hugging Face Spaces | VPS + domain |

Rule: **the same image everywhere**; only `.env` differs.

### 8.2 Docker
- Image = immutable package; container = a running image; registry (GHCR) = where images are stored.
- Inside the image: code, pinned dependencies, start command.
- Outside the image: secrets, data, weights, user images — supplied at run time via `--env-file` or volumes.
- Multi-stage build and a `.dockerignore` (exclude `data/`, `runs/`, `.env`, `.git`).
- Tag images with version + git SHA (e.g. `phoai:0.5.0-3f2a1c9`) so you always know what is running.

### 8.3 Database (from v0.8)
- PostgreSQL (+ pgvector if embeddings are needed). Images go to object storage (S3/R2/MinIO); the database stores paths and metadata.
- **Every schema change is a migration (Alembic) committed to git.** Never alter production tables by hand.
- Automated daily backups, and **a restore tested at least once**.
- Seed script for fake local/staging data.

### 8.4 CI/CD (GitHub Actions, from v0.5)
```
PR / push   ->  ruff  ->  pytest (mocked API)  ->  build Docker image
merge main  ->  (v0.8) push image to GHCR -> deploy staging -> smoke test
tag v*      ->  deploy production -> health check -> roll back to previous tag on failure
```

### 8.5 Monitoring
- Structured JSON logs with `request_id`, latency, tokens and cost.
- Spend limit at the API provider plus a per-day call cap in the app.
- (v0.8) Sentry for errors, an uptime monitor on `/health`, Langfuse for agent traces.

## 9. Working with Claude on this project

Treat Claude as a very fast colleague who forgets everything between sessions. The job is to give it the right context, hand over small well-defined tasks, verify the results, and write lessons down so mistakes are not repeated.

### 9.1 Two places to work

| Where | Used for | Memory |
|---|---|---|
| Claude (claude.ai / desktop), project workspace | Planning, proposal review, research, writing docs | Project documents + project memory |
| Claude Code, inside the repo | Writing code, running tests, reading errors, reviewing diffs | `CLAUDE.md` + auto memory + skills |

Major decisions are discussed in the first place and **recorded in `docs/adr/` or `docs/devlog.md`**, so the repository stays the single source of truth.

### 9.2 Context and tokens
- The **context window** holds everything Claude can currently see: CLAUDE.md, files read, the whole conversation, command output.
- **Every new message re-sends the whole context.** Long sessions cost more per message and degrade quality ("context rot").

| Command (Claude Code) | Use it when |
|---|---|
| `/clear` | Switching to an unrelated task. Free. |
| `/compact` | Mid-task but the context is long (e.g. after a long debugging detour). |
| `/context` | Seeing what occupies the context. |
| `/usage` (or `/cost`) | Checking token use and cost. |
| `/rewind` (Esc Esc) | Claude went the wrong way: roll back instead of stacking corrections. |
| `/memory` | Viewing/editing CLAUDE.md files and auto memory. |
| `@path/to/file` | Pointing Claude straight at a file instead of letting it search. |
| Plan mode (Shift+Tab) | Larger tasks: review the plan before any code is changed. |

Project rules:
1. **One work block (or one issue) = one Claude session.** `/clear` when it ends.
2. Open a session with scope: *"Read @docs/devlog.md (last entry) and issue #N. Today: X. Touch only file Y."*
3. Do not paste thousand-line logs: paste the relevant lines, or save the log to a file and point at it.
4. Use a smaller, cheaper model for simple edits; keep the strongest model for design and hard debugging.
5. For wide exploration, delegate to a **subagent** (separate context, returns a summary).

### 9.3 CLAUDE.md: project memory
- Lives at the repo root, committed, and is read at the **start of every session**, so it costs tokens every session. Keep it short: aim for **under ~150 lines** (the official guidance is under 200).
- Include only what Claude cannot infer from the code: goal, commands, conventions, prohibitions, current status.
- Link long documents with `@docs/schema.md` instead of copying them.
- Private notes go in `CLAUDE.local.md` (git-ignored).
- Claude Code also keeps **auto memory** (notes it writes from your corrections). Review it with `/memory` now and then and delete anything wrong or stale.
- **Update rule:** the second time Claude makes the same mistake, add one line to CLAUDE.md.

### 9.4 Skills (SKILL.md): workflows as commands
- A skill is a folder `.claude/skills/<name>/` with a `SKILL.md` (frontmatter `name` + `description`, then instructions). The folder name becomes the `/name` command.
- Only the **description** is loaded at session start (cheap); the full skill is loaded when used. Long procedures belong in skills, not in CLAUDE.md.
- Write the `description` as "use when …": it decides when Claude picks the skill.
- Create a skill when a procedure has been repeated twice.

| Skill | Does | Create when |
|---|---|---|
| `/release-check` | Runs the section 5.2 checklist and reports gaps | first release after v0.1 |
| `/run-eval` | Runs evaluation on the latest run, compares with baseline, drafts the report | first evaluation |
| `/explain-module` | Explains a module: data flow, inputs/outputs, three self-check questions | early |
| `/devlog` | Summarises a session into 3–5 lines for `docs/devlog.md` | early |

### 9.5 Permissions and guardrails
`.claude/settings.json`:
```json
{
  "permissions": {
    "deny": ["Read(./.env)", "Read(./.env.*)", "Read(./data/raw/**)"],
    "ask":  ["Bash(git push:*)", "Bash(git tag:*)"]
  }
}
```
- Claude cannot read `.env` or raw images, and must ask before pushing or tagging.
- Rules that must never be broken (e.g. never commit `.env`) belong in a **hook** (PreToolUse), because CLAUDE.md is guidance, not enforcement.
- From v0.5, a hook can run `ruff format` after Claude edits Python files.

### 9.6 AI-assisted development policy
1. **Plan first**: write 3–5 lines of intent or pseudo-code before asking.
2. **When stuck**: spend a few minutes reading the error and write a one-line hypothesis, ask Claude with it, then record "the real cause was…".
3. **Small tasks with a done-criterion**: *"Write `parse_critique(text) -> Critique`. Done when the 3 tests in `tests/test_schema.py` pass. Touch no other file."*
4. **Plan mode for larger changes.**
5. **Verify everything Claude writes**: read the full diff, run the tests, ask for an explanation of each change (if it cannot be explained back, it is not merged), and for important changes get a review from a fresh session or subagent.
6. **Core modules** (schema, critique, grounding, evaluation) are written by the author with Claude as reviewer; **supporting code** (boilerplate, Dockerfile, CI, plotting scripts) may be drafted by Claude and reviewed by the author.
7. **Transparency**: commits with substantial AI help carry a `Co-Authored-By` trailer; the PR template asks which parts were AI-assisted.

### 9.7 Common problems

| Symptom | Likely cause | Fix |
|---|---|---|
| Claude ignores conventions | Context or CLAUDE.md too long | `/clear`, shorten CLAUDE.md, put key rules first |
| Edits spread over unrelated files | Vague task | State "only edit file X" |
| Repeated failed fixes | Context full of dead ends | `/rewind` or `/clear`, restate the problem with a hypothesis |
| Tokens climbing fast | Long session, many files, big logs | One block = one session; `@file`; subagents |
| Code works but isn't understood | Claude wrote too much | `/explain-module`; rewrite the core part yourself |

## 10. Templates

### 10.1 `CLAUDE.md`
```markdown
# PhoAI — AI Photography Tutor

## Goal
Critique photos for beginners; every comment is grounded in visible evidence
(Observation -> Evidence -> Why -> What to try).

## Current status  (update weekly)
- Working on: v0.1 — see the GitHub milestone
- Prompt: prompts/critique_v2.md · model: see config/default.yaml

## Commands
- Install: `uv sync`
- Run: `uv run python -m phoai.pipeline <image>`
- Test: `uv run pytest -m "not slow"`
- Eval: `uv run python -m evals.run --run runs/<run_id>`
- Format: `uv run ruff format . && uv run ruff check .`

## Conventions
- Python 3.12, type hints, pydantic for all data going to/from the model
- Prompts live in prompts/, never hard-coded
- Every output stores prompt_version, model_id, schema_version, git_sha
- Tests never call the real API — use fixtures in tests/fixtures/
- Conventional Commits; never push or tag on your own

## Working with me
- Core modules (schema, critique, grounding, evals) are written by me;
  you review and explain. Do not rewrite whole files when I ask a question.
- Before changing more than 2 files: propose a plan and wait.
- When fixing a bug: state the root cause in one sentence.

## Never
- Read or print .env
- Commit data/raw/, runs/, cache/
- Add a dependency without asking

## Docs
- Spec: @docs/spec-v0.1.md · Schema: @docs/schema.md
- Decisions: docs/adr/ · Log: docs/devlog.md
```

### 10.2 `.claude/skills/release-check/SKILL.md`
```markdown
---
name: release-check
description: Check the PhoAI release checklist before tagging. Use when asked to "prepare a release", "tag v0.x", or when /release-check is invoked.
---

# Release check

1. Read the version in pyproject.toml and the latest tag (`git describe --tags --abbrev=0`).
2. Check each item and report ✅ / ❌ with a reason:
   - version bumped since the last tag
   - CHANGELOG.md has an entry for the new version
   - prompts/CHANGELOG.md updated if prompts/ changed since the last tag
   - evals/reports/ has a report for the new version with a comparison table
   - .env.example lists every environment variable used in src/
   - `uv run pytest -m "not slow"` passes
   - no files from data/raw/, runs/ or .env are tracked by git
3. Do NOT create a tag or push. Only print what is missing.
```

### 10.3 `.github/pull_request_template.md`
```markdown
## What
<!-- 1–3 lines. Link the issue: Fixes #... -->

## Checks
- [ ] I read the whole diff
- [ ] Tests pass (`pytest -m "not slow"`)
- [ ] If prompt/model changed: evaluation run, results in evals/reports/
- [ ] No secrets or raw data in the diff
- [ ] I can explain every changed line

## AI assistance
<!-- e.g. drafted sample tests, reviewed; core logic written by me -->
```

### 10.4 `CHANGELOG.md`
```markdown
# Changelog

## [0.2.0] — 2026-12-04
### Added
- Evaluation harness: per-dimension precision/recall, stability over 3 runs
- Result cache keyed by hash(image + prompt_version + model_id)
### Changed
- Prompt v2 -> v3 (see prompts/CHANGELOG.md)
### Fixed
- Retry on invalid JSON (#7)

## [0.1.0] — 2026-11-22
### Added
- critique.py runs on the first image set, 100% valid JSON
```

### 10.5 `docs/devlog.md`
```markdown
## Week 3 (15–21 Nov)
- Done: schema + pydantic, prompt v1 -> v2, critique.py on first image set
- Blocked: model returns generic evidence ("whole image") -> issue #9
- Decision: JSON mode instead of function calling (ADR 0002)
- Next first step: tag v0.1.0, show it to one reviewer
- Claude: added rule "tests never call the real API" to CLAUDE.md
```

## 11. Management cadence

**Every work block**
- Start: open the issue, create/switch branch, start a fresh Claude session (`/clear`).
- End: commit, push, move the Kanban card, write down the next first step.

**Weekly (about 10 minutes)**
- Write the week's `docs/devlog.md` entry and update "Current status" in CLAUDE.md.
- Review the milestone: close finished issues; move late ones (with a reason) or drop them.
- Check the week's API spend.
- Review CLAUDE.md and auto memory (`/memory`): add new rules, remove stale notes.
- Re-read section 6 (scope control).

**Every release**
- Run `/release-check`, follow the section 5.2 checklist.

---

### References
- Claude Code — Memory: https://code.claude.com/docs/en/memory
- Claude Code — Skills: https://code.claude.com/docs/en/skills
- Conventional Commits: https://www.conventionalcommits.org
- Semantic Versioning: https://semver.org
- Keep a Changelog: https://keepachangelog.com
