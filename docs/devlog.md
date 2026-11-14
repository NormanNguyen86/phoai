# Devlog

One short entry per week, newest first: done · blocked · decisions · next first step.

## Week of 2026-11-09
- Done: repo initialised (README, .gitignore, .env.example, handbook, spec v0.1, JD analysis).
- Done: project restructured for a public audience — English README/CLAUDE.md, STATUS.md,
  spec template, ADR folder, MIT license, Claude Code tutor skills.
- Decision: the repo is the single source of truth; `docs/STATUS.md` holds the current state.
- Next first step: create `pyproject.toml` with uv and write ADR 0001.

## Week of 2026-11-15
- Done: uv project with runtime/dev deps and lock file (PR #4); ADR 0001 accepted (PR #5); Python version aligned to 3.13.
- Done: scaffold drift fixes (ADR 0001 placeholder, English `.env.example`, STATUS refresh).
- Blocked: nothing reported.
- Decision: use uv over pip + venv (ADR 0001).
- Decision: the CLI entry point is the `phoai` script (`uv run phoai <image>`), replacing `python -m phoai.pipeline` from spec v0.1. The spec stays frozen; this entry is the record.
- Next first step: create `config/default.yaml` and `prompts/critique_v1.md`.
