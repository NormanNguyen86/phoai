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

## Tech introduced in this version
Each row needs an ADR in `docs/adr/` before v0.1.0 is tagged. The alternatives are
starting points for the decision, not the answer.

| Tech | Role in PhoAI | Alternatives to compare | ADR |
|---|---|---|---|
| uv + `pyproject.toml` | Dependencies, lock file, virtual env, `uv run` | pip + venv + requirements.txt, Poetry | 0001 |
| pydantic | `Critique` schema: validate model output, version the data contract | dataclasses + manual checks, JSON Schema | to write |
| Anthropic SDK (Claude, vision) | Send image + prompt, receive critique | OpenAI / Gemini SDK, raw HTTP | to write |
| YAML config + `.env` | Non-secret settings vs secrets, outside code | env vars only, TOML | to write |
| pytest + fixtures (mocked API) | Test parsing/validation without cost or network | live API tests only | — |

## JD skills this version proves
Rows from [jd-analysis.md](../jd-analysis.md).

| Row | Skill | Evidence when done |
|---|---|---|
| 1 | Clean Python packaging (uv, type hints) | `pyproject.toml`, `src/phoai/` |
| 2 | Git workflow, SemVer tag | PR history, tag `v0.1.0` |
| 3 | Calling an MLLM with image input | `src/phoai/critique.py` |
| 4 | Structured output + validation + retry | `src/phoai/schema.py`, `docs/schema.md` |
| 5 | Versioned prompts | `prompts/critique_v1.md`, `prompts/CHANGELOG.md` |
| 9 | Reproducible runs (config, run metadata) | `config/default.yaml`, `runs/<run_id>/` (not committed) |

## Input / Output
- **Input:** one JPG or PNG image
- **Output:** JSON matching the `Critique` schema, saved to `runs/<run_id>/`.
  Field definitions: `docs/schema.md` (written in this version).

## Definition of done
- [ ] 5/5 test photos produce schema-valid JSON
- [ ] Every output records `prompt_version`, `model_id`, `schema_version`
- [ ] Unit tests pass without calling the real API (fixtures in `tests/fixtures/`)
- [ ] No secrets, raw images or `runs/` committed
- [ ] README explains how to run v0.1
- [ ] ADRs written for every row in "Tech introduced"
- [ ] Tagged `v0.1.0` with a GitHub Release