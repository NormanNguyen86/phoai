# Devlog

One short entry per week, newest first: done · blocked · decisions · next first step.
## Week of 2026-11-15
- Done: uv project with runtime/dev deps and lock file (PR #4); ADR 0001 accepted (PR #5).
- Done: scaffold drift fixes; CLI skeleton with `phoai` entry point, image path validation and 6 unit tests (PR #6).
- Done: test photo set described and labelled before any model run (`docs/test-photos.md`): 5 test photos plus 4 same-scene references.
- Blocked: nothing reported.
- Decision: use uv over pip + venv (ADR 0001).
- Decision: CLI is `uv run phoai <image>` (positional argument), replacing `python -m phoai.pipeline` from spec v0.1. Spec stays frozen; this entry is the record.
- Decision: v0.1 validates the image by extension only; content validation and RAW support go to Backlog.
- Decision: the test set is exactly 5 photos to match the DoD; `01b` moved to the references because its label rests on an eyeballed estimate.
- Decision: the `iso_too_high_for_light` label of `02a` is scored only when shooting settings are passed to the model (Backlog).
- Finding: 8 of 9 photos have EXIF Orientation = 8, so the pipeline must handle rotation (to be decided in ADR 0003).
- Next first step: create `config/default.yaml` and `prompts/critique_v1.md`.

## Week of 2026-11-09
- Done: repo initialised (README, .gitignore, .env.example, handbook, spec v0.1, JD analysis).
- Done: project restructured for a public audience — English README/CLAUDE.md, STATUS.md,
  spec template, ADR folder, MIT license, Claude Code tutor skills.
- Decision: the repo is the single source of truth; `docs/STATUS.md` holds the current state.
- Next first step: create `pyproject.toml` with uv and write ADR 0001.
