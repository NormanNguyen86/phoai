---
name: check
description: Self-check the user's uncommitted or staged PhoAI changes before a commit or PR. Use when he runs /check or says "ready to commit", "check my changes".
---

# Pre-commit check

Read-only: report, do not fix.

1. `git status` and `git diff` (staged and unstaged). Read the current spec via `docs/STATUS.md`.
2. Run what exists: `uv run ruff check .`, `uv run ruff format --check .`,
   `uv run pytest -m "not slow"`. Report failures with the key lines.
3. Check against `CLAUDE.md` conventions: type hints, pydantic at model boundaries, prompts not
   hard-coded, output metadata, tests not calling the real API, no secrets / `data/raw/` /
   `runs/` / `cache/` in the diff, no new dependency without a decision.
4. Scope: anything outside the current task or spec → suggest moving it to another branch.
5. Commits: propose how to split the diff into one-idea commits, each with a
   Conventional Commit message. He runs the git commands.
6. Report as **Blocking / Should fix / Nit**, each with `file:line` and why.
   For core modules give a hint, not replacement code.
