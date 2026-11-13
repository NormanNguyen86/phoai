# Spec v0.1 — Critique runs on 5 photos

**Frozen:** 2026-11-12 · **Due:** 2026-11-22 · **Milestone:** v0.1

## Goal
A user can run one command on a photo and get a structured critique for novice photographers
(Observation → Evidence → Why → What to try) as schema-validated JSON.

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
For each: why it is here, the main alternative, and the ADR that records the choice.
Each ADR goes in `docs/adr/` before `v0.1.0` is tagged; the alternatives listed are
starting points for the decision, not the answer.

| Tech | Role in PhoAI | Alternative considered | ADR |
|---|---|---|---|
| uv + `pyproject.toml` | Dependencies, lock file, virtual env, `uv run` | pip + venv + requirements.txt, Poetry | 0001 |
| pydantic | `Critique` schema: validate model output, version the data contract | dataclasses + manual checks, JSON Schema | to write |
| Anthropic SDK (Claude, vision) | Send image + prompt, receive critique | OpenAI / Gemini SDK, raw HTTP | to write |
| YAML config + `.env` | Non-secret settings vs secrets, outside code | env vars only, TOML | to write |
| pytest + fixtures (mocked API) | Test parsing/validation without cost or network | live API tests only | — |

## JD skills this version proves
Rows from [jd-analysis.md](../jd-analysis.md) and the evidence that will exist when done.

| Row | Skill | Evidence (file / PR / report) |
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
- [ ] README updated (how to run v0.1, results on the 5 test photos)
- [ ] ADRs written for every row in "Tech introduced"
- [ ] Tagged `v0.1.0` with a GitHub Release
