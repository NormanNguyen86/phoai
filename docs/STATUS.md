# Status

_Last updated: 2026-11-13 · Overwritten at each status check; history lives in [devlog.md](devlog.md)._

## Current version
**v0.1 — Critique runs on 5 photos** · due 2026-11-22 · spec: [spec-v0.1](spec-versions/spec-v0.1.md)

## Definition of done
| # | Item | State | Evidence |
|---|---|---|---|
| 1 | 5/5 test photos produce schema-valid JSON | ⬜ | |
| 2 | Outputs record `prompt_version`, `model_id`, `schema_version` | ⬜ | |
| 3 | Unit tests pass without the real API | ⬜ | |
| 4 | No secrets / raw images / `runs/` committed | ⬜ | |
| 5 | README explains how to run v0.1 | ⬜ | |
| 6 | ADRs for every row in spec "Tech introduced" | ⬜ | |
| 7 | Tagged `v0.1.0` with a GitHub Release | ⬜ | |

⬜ not started · 🟨 in progress · ✅ done

## Next tasks (max 3)
1. Create `pyproject.toml` and `uv.lock` with uv; record the choice in `docs/adr/0001-use-uv.md`.
2. Add `config/default.yaml` and `prompts/critique_v1.md`.
3. Design the `Critique` schema on paper, then write `docs/schema.md`.

## Milestones to due date
| Date | Milestone |
|---|---|
| 2026-11-15 | Project installs with `uv sync`; config + prompt v1 exist |
| 2026-11-17 | `schema.py` + `docs/schema.md` + schema tests pass |
| 2026-11-19 | `critique.py` calls the model, retries on invalid JSON; mocked tests pass |
| 2026-11-20 | `pipeline.py` CLI writes `runs/<run_id>/` with metadata |
| 2026-11-21 | 5 photos run end to end; README run section verified |
| 2026-11-22 | Release checklist passed; `v0.1.0` tagged |

## Blockers / risks
- Part-time schedule: milestones are tight; cut scope (not tests) if 2026-11-19 slips.

## Backlog (out of scope for this version)
- Caching, cost limits, eval harness (v0.2)
