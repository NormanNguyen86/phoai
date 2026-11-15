# Status

_Last updated: 2026-11-15 · Overwritten at each status check; history lives in [devlog.md](devlog.md)._

## Current version
**v0.1 — Critique runs on 5 photos** · due 2026-11-22 · spec: [spec-v0.1](spec-versions/spec-v0.1.md)

## Definition of done
| # | Item | State | Evidence |
|---|---|---|---|
| 1 | 5/5 test photos produce schema-valid JSON | ⬜ | |
| 2 | Outputs record `prompt_version`, `model_id`, `schema_version` | ⬜ | |
| 3 | Unit tests pass without the real API | ⬜ | |
| 4 | No secrets / raw images / `runs/` committed | 🟨 | `.gitignore` covers `.env`, `data/raw/`, `runs/` |
| 5 | README explains how to run v0.1 | ⬜ | |
| 6 | ADRs for every row in spec "Tech introduced" | 🟨 | 1/4: 0001 (uv). Left: 0002 pydantic, 0003 Anthropic SDK, 0004 YAML + .env |
| 7 | Tagged `v0.1.0` with a GitHub Release | ⬜ | |

⬜ not started · 🟨 in progress · ✅ done

## Next tasks (max 3)
1. Fix scaffold drift: `phoai:main` script entry, placeholder in ADR 0001, English `.env.example`, pytest `slow` marker (`chore/fix-scaffold-drift`).
2. Add `config/default.yaml`, `prompts/critique_v1.md`, `prompts/CHANGELOG.md`; write ADR 0004 (and 0003 once the SDK is used).
3. Design the `Critique` schema on paper, then write `docs/schema.md`, `schema.py` and ADR 0002.

## Milestones to due date
| Date | Milestone |
|---|---|
| 2026-11-15 | Drift PR merged; `config/default.yaml` exists |
| 2026-11-16 | `prompts/critique_v1.md` + changelog; 5 test photos chosen; ADR 0004 |
| 2026-11-17 | `schema.py` + `docs/schema.md` + schema tests pass; ADR 0002 |
| 2026-11-19 | `critique.py` calls the model, retries on invalid JSON; mocked tests pass; ADR 0003 |
| 2026-11-20 | `pipeline.py` CLI writes `runs/<run_id>/` with metadata |
| 2026-11-21 | 5 photos run end to end; README run section + results verified |
| 2026-11-22 | Release checklist passed; `v0.1.0` tagged |

## Blockers / risks
- Part-time schedule: if `critique.py` is not done by 2026-11-19, cut retry sophistication (one retry), never tests or ADRs.
- The 5 test photos are not chosen yet (blocks DoD 1 and 5).
- ADRs 0002–0004 must be written the day each tech is introduced, not at release.

## Backlog (out of scope for this version)
- Caching, cost limits, eval harness (v0.2)