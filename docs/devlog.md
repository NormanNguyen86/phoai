# Devlog

One short entry per week, newest first: done · blocked · decisions · next first step.
## Week of 2026-11-15
- Done: `docs/schema.md` (Critique and RunRecord contract), `prompts/critique_v1.md` with one lake example, `prompts/CHANGELOG.md` v1 entry (PR #10, #11); expected output per dimension in `docs/test-photos.md` §9, not yet confirmed by the author (PR #12); review fixes (PR #13).
- Blocked: `schema.py` (planned 2026-11-17) and `critique.py` (planned 2026-11-19) not done; API key and credit status unknown.
- Decision: two objects: `Critique` (model output) and `RunRecord` (metadata set by the pipeline); `extra="forbid"`; invariants are validators in code and a violation counts as invalid output and is retried.
- Decision: `schema_version` is independent of release tags and starts at 0.1.0.
- Decision: `strengths` may be empty; `analysis_limits` is required and may be empty; `priority_problems` is required only when a dimension is `needs_work` (a `fine`-only photo may have none).
- Decision: JSON field order follows the steps: `intent, analysis_limits, dimensions, priority_problems, strengths, overall_summary`.
- Decision: the prompt tells the model not to use code fences; the parser strips one fence around the whole output (middle level); `stop_reason == "max_tokens"` is a separate error, not counted as a validation retry; plain retry without error feedback in v0.1.
- Decision: rotation is done offline by `data/processed_raw/preprocess.py` (Pillow: EXIF Orientation applied, metadata stripped, lossless PNG, 0.9–2.1 MB each, no resize). The model input is the upright PNG set; the pipeline does not rotate in v0.1 and no API orientation test is needed. Auto-orient for arbitrary uploads goes to Backlog; the input decision is recorded in ADR 0004.
- Next first step: get an API key and credit, run one photo through the API, then `schema.py`.
- Done: uv project with runtime/dev deps and lock file (PR #4); ADR 0001 accepted (PR #5).
- Done: scaffold drift fixes; CLI skeleton with `phoai` entry point, image path validation and 6 unit tests (PR #6).
- Done: test photo set described and labelled before any model run (`docs/test-photos.md`): 5 test photos plus 4 same-scene references.
- Blocked: nothing reported.
- Decision: use uv over pip + venv (ADR 0001).
- Decision: CLI is `uv run phoai <image>` (positional argument), replacing `python -m phoai.pipeline` from spec v0.1. Spec stays frozen; this entry is the record.
- Decision: v0.1 validates the image by extension only; content validation and RAW support go to Backlog.
- Decision: the test set is exactly 5 photos to match the DoD; `01b` moved to the references because its label rests on an eyeballed estimate.
- Decision: the `iso_too_high_for_light` label of `02a` is scored only when shooting settings are passed to the model (Backlog).
- Finding: 8 of 9 photos have EXIF Orientation = 8, so rotation had to be handled (resolved 2026-11-19: offline preprocessing, see the decision in the week of 2026-11-15).
- Next first step: create `config/default.yaml` and `prompts/critique_v1.md`.

## Week of 2026-11-09
- Done: repo initialised (README, .gitignore, .env.example, handbook, spec v0.1, JD analysis).
- Done: project restructured for a public audience — English README/CLAUDE.md, STATUS.md,
  spec template, ADR folder, MIT license, Claude Code tutor skills.
- Decision: the repo is the single source of truth; `docs/STATUS.md` holds the current state.
- Next first step: create `pyproject.toml` with uv and write ADR 0001.
