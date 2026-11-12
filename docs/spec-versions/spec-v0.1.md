# Spec v0.1 — Critique runs on 5 photos

**Frozen:** 2026-11-12 · **Due:** 2026-11-22 · **Milestone:** v0.1

## Goal
Given a photo, produce a structured critique for novice photographers
(Observation → Evidence → Why → What to try) as validated JSON.

## In scope
- CLI: `uv run python -m phoai.pipeline <image>` → print and save JSON
- Model: Claude via API (`model_id` set in `config/default.yaml`)
- Prompt loaded from `prompts/critique_v1.md` (not hard-coded)
- Output validated against a pydantic schema; retry when the model returns invalid JSON

## Out of scope (→ Backlog)
- FastAPI / Gradio / any web UI
- Grounding (bounding boxes / masks) and evidence verification
- Eval harness and metrics
- Caching, cost limits, Docker, CI

## Input / Output
- **Input:** one JPG or PNG image
- **Output:** JSON matching the `Critique` schema, saved to `runs/<run_id>/`.
  Field definitions: see `docs/schema.md`.

## Definition of done
- [ ] 5/5 test photos produce schema-valid JSON
- [ ] Every output records `prompt_version`, `model_id`, `schema_version`
- [ ] Unit tests pass without calling the real API (fixtures in `tests/fixtures/`)
- [ ] No secrets, raw images or `runs/` committed
- [ ] README explains how to run v0.1
- [ ] Tagged `v0.1.0` with a GitHub Release