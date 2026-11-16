# Status

_Last updated: 2026-11-16 · Overwritten at each status check; history lives in [devlog.md](devlog.md)._

## Current version
**v0.1 — Critique runs on 5 photos** · due 2026-11-22 · spec: [spec-v0.1](spec-versions/spec-v0.1.md)

## Definition of done
| # | Item | State | Evidence |
|---|---|---|---|
| 1 | 5/5 test photos produce schema-valid JSON | ⬜ | Test set defined in [test-photos.md](test-photos.md) |
| 2 | Outputs record `prompt_version`, `model_id`, `schema_version` | ⬜ | |
| 3 | Unit tests pass without the real API | 🟨 | `tests/test_pipeline.py` (6 pass); schema/critique tests pending |
| 4 | No secrets / raw images / `runs/` committed | 🟨 | `.gitignore` covers `.env`, `data/raw/`, `runs/` |
| 5 | README explains how to run v0.1 | ⬜ | |
| 6 | ADRs for every row in spec "Tech introduced" | 🟨 | 1/4: 0001 (uv). Left: 0002 pydantic, 0003 Anthropic SDK, 0004 YAML + .env |
| 7 | Tagged `v0.1.0` with a GitHub Release | ⬜ | |

⬜ not started · 🟨 in progress · ✅ done

## Next tasks (max 3)
1. Add `config/default.yaml`, `prompts/critique_v1.md`, `prompts/CHANGELOG.md`; write ADR 0004.
2. Design the `Critique` schema on paper, then `docs/schema.md`, `schema.py`, ADR 0002.
3. Test one Orientation = 8 photo on the API to see whether it auto-rotates; decide the image preprocessing (rotate in memory, PNG) for ADR 0003.

## Milestones to due date
| Date | Milestone |
|---|---|
| 2026-11-16 | Test photo set merged; config + prompt v1 + changelog; ADR 0004 |
| 2026-11-17 | `schema.py` + `docs/schema.md` + schema tests pass; ADR 0002 |
| 2026-11-19 | `critique.py` calls the model, retries on invalid JSON; mocked tests pass; ADR 0003 |
| 2026-11-20 | `pipeline.py` creates `runs/<run_id>/` and writes output + metadata |
| 2026-11-21 | 5 photos run end to end; README run section + results verified |
| 2026-11-22 | Release checklist passed; `v0.1.0` tagged |

## Blockers / risks
- Part-time schedule: if `critique.py` is not done by 2026-11-19, cut retry sophistication (one retry), never tests or ADRs.
- Need an Anthropic API key and credit before 2026-11-18.
- 8 of 9 photos have EXIF Orientation = 8; sending raw bytes may make the model judge composition on a rotated image. Verify before 2026-11-19.

## Backlog (out of scope for this version)
- Caching, cost limits, eval harness (v0.2)
- RAW image support (convert before sending to the API)
- Validate image content (not only extension), e.g. with Pillow
- Pytest `slow` marker (add with the first e2e test)
- Pass shooting settings (ISO, shutter, aperture) to the model; needed to score the `iso_too_high_for_light` label of `02a`
- Put the photo measurement script in the repo so the numbers in `docs/test-photos.md` can be regenerated (v0.2)
- Use the a/b photo pairs as a comparison set with known answers (v0.2)